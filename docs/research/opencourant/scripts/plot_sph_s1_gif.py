"""GIF for SPH rung S1: quarter sphere (surface particles on the sphere, s = R/32) on the rigid wall at 20 m/s;
pressure of the particles in the slice 0 < y < s (mirrored to negative x), and the wall force against Hertz and JAX.

Usage: python plot_sph_s1_gif.py <work_dir> <rung1_jax.npy> <out_gif> [n_r] [threads]
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import ocdeck as oc  # noqa: E402
import rung1 as r1  # noqa: E402
import sph_rung1 as s1  # noqa: E402
import sphdeck as sd  # noqa: E402
import vtkread  # noqa: E402

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE = "#2a78d6", "#eb6834"
DIV = LinearSegmentedColormap.from_list("blue_red", ["#104281", "#3987e5", "#f0efec", "#e34948", "#8f1f1f"])


def main(work, jax_npy, out_gif, n_r=32, threads=2):
    n_r, threads = int(n_r), int(threads)
    H = r1.hertz()
    tc = H["t_contact"]
    s, p = s1.sphere(n_r, "quarter", conform=True)
    m_p = r1.RHO * 4 / 3 * np.pi * r1.R**3 / 4 / len(p)
    body = sd.Body(xyz=p, mass=m_p, mat=oc.Elastic(r1.E, r1.NU, r1.RHO), prop=sd.SphProp(h=2 ** (1 / 6) * s),
                   velocity=(0.0, 0.0, -r1.V), title="sphere")
    planes = [sd.SymPlane((0, 0, 0), (1, 0, 0)), sd.SymPlane((0, 0, 0), (0, 1, 0))]
    name = f"SGIF{n_r:03d}"
    d = os.path.join(work, name)
    sd.write_deck(d, name, [body], t_end=1.2 * tc, dt_th=tc / 2000, sym=planes, z_wall=0.0, dt_scale=0.3,
                  dt_anim=tc / 30, anim=("P",))
    res = sd.run(d, name, threads=threads)
    assert res.get("normal"), res
    frames = [vtkread.read(v) for v in oc.convert_anim(d, name)]
    head, a = oc.read_th(d, name)
    t = a[:, 0]
    zmom = 4 * a[:, [i for i, h in enumerate(head) if h.endswith("ZMOM")][0]]
    f = np.convolve(np.diff(zmom) / np.diff(t) / H["F_max"], np.ones(5) / 5, "same")
    jx = np.load(jax_npy, allow_pickle=True).item()[20]
    plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                         "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
                         "font.size": 8, "axes.spines.top": False, "axes.spines.right": False})
    fig = plt.figure(figsize=(8.0, 3.3))
    ax = fig.add_axes([0.07, 0.15, 0.42, 0.72])
    cax = fig.add_axes([0.50, 0.2, 0.012, 0.6])
    bx = fig.add_axes([0.64, 0.15, 0.34, 0.72])
    norm = TwoSlopeNorm(vmin=-1.0, vcenter=0.0, vmax=4.0)
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=DIV), cax=cax)
    cb.set_label("pressure (GPa)", color=INK2)
    cb.outline.set_visible(False)
    a_h = np.sqrt(r1.R * H["d_max"]) * 1e6

    def draw(i):
        fr = frames[i]
        ax.clear()
        bx.clear()
        sel = fr["cell"]["ELEMENT_ID"] > 0
        ids = fr["cell"]["ELEMENT_ID"][sel].astype(int)
        pos = {int(k): j for j, k in enumerate(fr["point"]["NODE_ID"].astype(int))}
        xyz = np.array([fr["xyz"][pos[k]] for k in ids]) * 1e6
        pr = fr["cell"]["SPHELEM_Pressure"][sel] * 1e-9
        sl = xyz[:, 1] < s * 1e6
        for sgn in (1.0, -1.0):
            ax.scatter(sgn * xyz[sl, 0], xyz[sl, 2], c=pr[sl], cmap=DIV, norm=norm, s=9 * (32 / n_r) ** 2, linewidths=0)
        ax.axhline(0, color=INK2, lw=1.5)
        for sgn in (1, -1):
            ax.plot([sgn * a_h, sgn * a_h], [-0.15, 0.0], color=BLUE, lw=1.2)
        ax.text(a_h + 0.1, -0.12, "Hertz a at d_max", fontsize=6.5, color=BLUE, va="center")
        ax.set_xlim(-4, 4)
        ax.set_ylim(-0.3, 3.5)
        ax.set_aspect("equal")
        ax.set_xlabel("x (µm), slice 0 < y < s, mirrored; sphere R = 10 µm")
        ax.set_ylabel("z (µm)")
        ax.set_title(f"SPH, s = R/{n_r}, particle centres, t = {fr['time'] / tc:4.2f} t_Hertz", loc="left",
                     fontsize=8.5)
        bx.grid(color=GRID, lw=0.6)
        bx.plot(H["t"] / tc, H["F"] / H["F_max"], color=INK2, lw=2.2, label="Hertz")
        bx.plot(jx["t"], jx["f"], color=ORANGE, lw=1.2, label="JAX 20×40")
        bx.plot(t[1:] / tc, f, color=BLUE, lw=1.3, label=f"SPH R/{n_r}")
        bx.axvline(fr["time"] / tc, color=MUTED, lw=0.8, ls=":")
        bx.set_xlim(0, 1.2)
        bx.set_ylim(-0.05, 1.2)
        bx.set_xlabel("t / t_Hertz")
        bx.set_ylabel("wall force / F_Hertz")
        bx.legend(frameon=False, fontsize=6.5, loc="upper right")
        return []

    FuncAnimation(fig, draw, frames=len(frames), blit=False).save(out_gif, writer=PillowWriter(fps=6), dpi=72)


if __name__ == "__main__":
    main(*sys.argv[1:6])
