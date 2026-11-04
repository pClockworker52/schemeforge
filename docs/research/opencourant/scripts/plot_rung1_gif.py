"""GIF for rung 1: OpenCourant (Isolid 17) sphere at the contact, pressure field (zoomed, mirrored), and the wall
force history against the JAX code and Hertz.

Usage: python plot_rung1_gif.py <work_dir> <jax.npy> <out_gif>
"""

import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import ocdeck as oc  # noqa: E402
import rung1 as r1  # noqa: E402
import vtkread  # noqa: E402

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE = "#2a78d6", "#eb6834"
DIV = LinearSegmentedColormap.from_list("blue_red", ["#104281", "#3987e5", "#f0efec", "#e34948", "#8f1f1f"])


def main(work, jax_npy, out_gif):
    H = r1.hertz()
    tc = H["t_contact"]
    name = "SGIF"
    d = os.path.join(work, name)
    rz, q = oc.sphere_mesh(r1.R, 15, 30)
    oc.write_deck(d, name, oc.Elastic(r1.E, r1.NU, r1.RHO), rz, q, velocity=r1.V, t_end=1.2 * tc, dt_th=tc / 2000,
                  dt_anim=tc / 30, q=(1e-30, 1e-30), dt_scale=0.4, anim_fields=("P", "VONM"))
    oc.run(d, name)
    frames = [vtkread.read(v) for v in oc.convert_anim(d, name)]
    head, a = oc.read_th(d, name)
    t = a[:, 0]
    zmom = a[:, [i for i, h in enumerate(head) if h.startswith("plate") and h.endswith("ZMOM")][0]]
    f = 2 * math.pi * np.diff(zmom) / np.diff(t) / H["F_max"]
    jx = np.load(jax_npy, allow_pickle=True).item()[15]
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
    a_h = math.sqrt(r1.R * H["d_max"]) * 1e6

    def draw(i):
        fr = frames[i]
        ax.clear()
        bx.clear()
        sel = fr["cell"]["ELEMENT_ID"] > 0
        cells = [c for c, s in zip(fr["cells"], sel, strict=True) if s]
        p = fr["cell"]["2DELEM_Pressure"][sel] * 1e-9
        xy = fr["xyz"][:, 1:3] * 1e6
        for sgn in (1.0, -1.0):
            ax.add_collection(PolyCollection([xy[c] * np.array([sgn, 1.0]) for c in cells], array=p, cmap=DIV,
                                             norm=norm, edgecolors=(0.3, 0.3, 0.3, 0.25), linewidths=0.2))
        ax.axhline(0, color=INK2, lw=1.5)
        for sgn in (1, -1):
            ax.plot([sgn * a_h, sgn * a_h], [-0.15, 0.0], color=BLUE, lw=1.2)
        ax.text(a_h + 0.1, -0.12, "Hertz a at d_max", fontsize=6.5, color=BLUE, va="center")
        ax.set_xlim(-4, 4)
        ax.set_ylim(-0.3, 3.5)
        ax.set_aspect("equal")
        ax.set_xlabel("r (µm), mirrored; sphere R = 10 µm")
        ax.set_ylabel("z (µm)")
        ax.set_title(f"Contact zone, OpenCourant Isolid 17, t = {fr['time'] / tc:4.2f} t_Hertz", loc="left",
                     fontsize=8.5)
        bx.grid(color=GRID, lw=0.6)
        bx.plot(H["t"] / tc, H["F"] / H["F_max"], color=INK2, lw=2.2, label="Hertz")
        bx.plot(jx["t"], jx["f"], color=BLUE, lw=1.4, label="JAX 15×30")
        bx.plot(t[1:] / tc, f, color=ORANGE, lw=1.2, label="OpenCourant 15×30")
        bx.axvline(fr["time"] / tc, color=MUTED, lw=0.8, ls=":")
        bx.set_xlim(0, 1.2)
        bx.set_ylim(-0.05, 1.2)
        bx.set_xlabel("t / t_Hertz")
        bx.set_ylabel("wall force / F_Hertz")
        bx.legend(frameon=False, fontsize=6.5, loc="upper right")
        return []

    FuncAnimation(fig, draw, frames=len(frames), blit=False).save(out_gif, writer=PillowWriter(fps=6), dpi=72)


if __name__ == "__main__":
    main(*sys.argv[1:4])
