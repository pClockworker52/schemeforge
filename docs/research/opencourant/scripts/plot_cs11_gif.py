"""GIF for the CS-11 sweep: one Al-Al impact of setup F (SPH particle on TYPE7 bricks) or W (SPH on SPH), slice
0 <= y < s (mirrored to negative x): particle (and W substrate) particles coloured by u_r / V, F substrate as the
deformed brick grid in the plane y = 0; right panel: J(t) and J_s(t) up to the time reached.

Usage: python plot_cs11_gif.py <work_dir> <W|F> <n_r> <V> <out_gif> [threads] [frames]
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
import cs11_sweep as cs  # noqa: E402
import ocdeck as oc  # noqa: E402
import sph_interface as si  # noqa: E402
import sphdeck as sd  # noqa: E402
import vtkread  # noqa: E402

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE = "#2a78d6", "#eb6834"
DIV = LinearSegmentedColormap.from_list("blue_red", ["#104281", "#3987e5", "#b9b7b0", "#e34948", "#8f1f1f"])


def main(work, setup, n_r, V, out_gif, threads=8, n_frames=40):
    n_r, V, threads, n_frames = int(n_r), float(V), int(threads), int(n_frames)
    R, t_e = cs.R, 0.25 * cs.D / float(V)
    s = R / n_r
    name = f"G{setup}{n_r:02d}v{int(V):04d}"
    d = os.path.join(work, name)
    info = si.write_case(d, name, setup, cs.AL, R, n_r, V, t_end=t_e, dt_th=t_e / 100, fs=cs.F_FROZEN,
                         dt_anim=t_e / n_frames, anim=("EPSP",), dt_min=cs.DT_SPH_PER_M * s / 50,
                         th_sub=(0.5 * R, 2 * R))
    res = sd.run(d, name, threads=threads)
    assert res.get("engine_s"), res
    head, a = cs.read_th_fast(d, name)
    n_part = info["n_particles"]
    _, _, _, tt, curve, _ = cs.jet_metric(head, a, range(1, n_part + 1), V, t_e)
    _, _, _, _, curve_s, _ = cs.jet_metric(head, a, info["th_sub_ids"], V, t_e)
    frames = [vtkread.read(v) for v in oc.convert_anim(d, name)]
    plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                         "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
                         "font.size": 8, "axes.spines.top": False, "axes.spines.right": False})
    fig = plt.figure(figsize=(8.8, 3.9))
    ax = fig.add_axes([0.06, 0.14, 0.47, 0.74])
    cax = fig.add_axes([0.545, 0.2, 0.012, 0.6])
    bx = fig.add_axes([0.685, 0.14, 0.295, 0.74])
    norm = TwoSlopeNorm(vmin=-1.0, vcenter=0.0, vmax=2.0)
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=DIV), cax=cax)
    cb.set_label("u_r / V", color=INK2)
    cb.outline.set_visible(False)
    xs = si.graded(1.5 * R, 3 * R, s)
    zs = -si.graded(1.5 * R, 2 * R, s)[::-1]
    nx, nz = len(xs), len(zs)

    def draw(i):
        fr = frames[i]
        ax.clear()
        bx.clear()
        ids = fr["point"]["NODE_ID"].astype(int)
        pos = {int(k): j for j, k in enumerate(ids)}
        xyz, vel = fr["xyz"], fr["point"]["Velocity"]
        sph = ids < si.BRICK_NODE0
        r = np.hypot(xyz[:, 0], xyz[:, 1])
        ur = np.where(r > 0, (xyz[:, 0] * vel[:, 0] + xyz[:, 1] * vel[:, 1]) / np.maximum(r, 1e-30), 0) / V
        sl = sph & (xyz[:, 1] < s)
        for sgn in (1.0, -1.0):
            ax.scatter(sgn * xyz[sl, 0] / R, xyz[sl, 2] / R, c=ur[sl], cmap=DIV, norm=norm,
                       s=9 * (16 / n_r) ** 2, linewidths=0)
        if setup == "F":  # deformed brick grid in the plane y = 0 (node index j = 0)
            g = np.full((nx, nz, 2), np.nan)
            for ii in range(nx):
                for kk in range(nz):
                    k = pos.get(int(si.BRICK_NODE0 + (ii * nx + 0) * nz + kk))
                    if k is not None:
                        g[ii, kk] = xyz[k, 0] / R, xyz[k, 2] / R
            for sgn in (1.0, -1.0):
                for ii in range(nx):
                    ax.plot(sgn * g[ii, :, 0], g[ii, :, 1], color=MUTED, lw=0.35)
                for kk in range(nz):
                    ax.plot(sgn * g[:, kk, 0], g[:, kk, 1], color=MUTED, lw=0.35)
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-0.9, 2.0)
        ax.set_aspect("equal")
        ax.set_xlabel("x / R (slice 0 ≤ y < s, mirrored)")
        ax.set_ylabel("z / R")
        ax.set_title(f"Al–Al {setup}, s = R/{n_r}, {V:.0f} m/s, t = {fr['time'] / (cs.D / V):.3f} D/V", loc="left",
                     fontsize=8.5)
        bx.grid(color=GRID, lw=0.6)
        bx.plot(tt / (cs.D / V), curve, color=BLUE, lw=1.4, label="J(t): particle")
        bx.plot(tt / (cs.D / V), curve_s, color=ORANGE, lw=1.4, label="J_s(t): substrate")
        bx.axhline(1.5, color=INK2, lw=0.9, ls="--", label="J* = 1.5")
        bx.axvline(fr["time"] / (cs.D / V), color=MUTED, lw=0.8, ls=":")
        bx.set_xlim(0, 0.25)
        bx.set_ylim(0, 2.6)
        bx.set_xlabel("t / (D/V)")
        bx.set_ylabel("max u_r / V at time t")
        bx.legend(frameon=False, fontsize=6.5, loc="upper left")
        return []

    FuncAnimation(fig, draw, frames=len(frames), blit=False).save(out_gif, writer=PillowWriter(fps=6), dpi=72)


if __name__ == "__main__":
    main(*sys.argv[1:8])
