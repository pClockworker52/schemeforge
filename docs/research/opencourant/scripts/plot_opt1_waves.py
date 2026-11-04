"""Explain the centre lift-off of the unconfined JC + Grueneisen plate (run J7 of opt1_jc_gruneisen.py).

Left: pressure on the deformed mesh (compression red, tension blue; asymmetric scale) with velocity arrows,
mirrored about the axis. Right: gap between the underside and the wall at three initial radii vs time.

Usage: python plot_opt1_waves.py <J7_run_dir> <out_gif>
"""

import glob
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "openradioss", "scripts"))
import vtkread  # noqa: E402

N_R = N_Z = 50
SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
DIV = LinearSegmentedColormap.from_list("blue_red", ["#104281", "#3987e5", "#f0efec", "#e34948", "#8f1f1f"])
LINES = (("#2a78d6", 0, "r₀ = 0 (axis)"), ("#eb6834", 25, "r₀ = 0.5 R"), ("#1baf7a", 37, "r₀ = 0.74 R"))


def main(run_dir, out_gif):
    frames = [vtkread.read(v) for v in sorted(glob.glob(os.path.join(run_dir, "J7A*.vtk")))]
    pos = {int(i): k for k, i in enumerate(frames[0]["point"]["NODE_ID"])}

    def nid(ir, iz):
        return ir * (N_Z + 1) + iz + 1

    t = np.array([f["time"] for f in frames]) * 1e9
    gaps = {ir: np.array([f["xyz"][pos[nid(ir, 0)], 2] for f in frames]) * 1e9 for _, ir, _ in LINES}
    plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                         "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
                         "font.size": 8, "axes.spines.top": False, "axes.spines.right": False})
    fig = plt.figure(figsize=(8.0, 3.4))
    ax = fig.add_axes([0.065, 0.15, 0.535, 0.72])
    cax = fig.add_axes([0.605, 0.2, 0.012, 0.6])
    bx = fig.add_axes([0.77, 0.15, 0.21, 0.72])
    norm = TwoSlopeNorm(vmin=-3.0, vcenter=0.0, vmax=20.0)
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=DIV), cax=cax)
    cb.set_label("pressure (GPa)", color=INK2)
    cb.set_ticks([-3, 0, 5, 10, 15, 20])
    cb.outline.set_visible(False)
    sub = [pos[nid(ir, iz)] for ir in range(0, N_R + 1, 5) for iz in range(0, N_Z + 1, 5)]

    def draw(i):
        f = frames[i]
        ax.clear()
        bx.clear()
        rz = f["xyz"][:, 1:3] * 1e6
        p = f["cell"]["2DELEM_Pressure"][: N_R * N_Z] * 1e-9
        v = f["point"]["Velocity"]
        for s in (1.0, -1.0):
            polys = [rz[c] * np.array([s, 1.0]) for c in f["cells"][: N_R * N_Z]]
            ax.add_collection(PolyCollection(polys, array=p, cmap=DIV, norm=norm, edgecolors="none"))
        ax.quiver(rz[sub, 0], rz[sub, 1], v[sub, 1], v[sub, 2], color=INK, scale=12000, width=0.003, alpha=0.7)
        ax.axhline(0, color=INK2, lw=1.5)
        ax.set_xlim(-21, 21)
        ax.set_ylim(-0.5, 11)
        ax.set_aspect("equal")
        ax.set_xlabel("r (µm)  (mirrored; arrows: velocity, 500 m/s ≈ 1 µm)")
        ax.set_ylabel("z (µm)")
        ax.set_title(f"Pressure and velocity, t = {f['time'] * 1e9:4.2f} ns", loc="left", fontsize=8.5)
        bx.grid(color=GRID, lw=0.6)
        for col, ir, lab in LINES:
            bx.plot(t, gaps[ir], color=col, lw=1.6, label=lab)
            bx.plot(t[i], gaps[ir][i], "o", color=col, ms=6)
        bx.axvline(2 * 10e-6 / 4685 * 1e9, color=MUTED, lw=0.8, ls=":")
        bx.text(2 * 10e-6 / 4685 * 1e9 + 0.2, 1850, "top-face release\nback at the wall", fontsize=6.5, color=INK2,
                va="top")
        bx.set_xlim(0, t[-1])
        bx.set_ylim(-50, 1900)
        bx.set_xlabel("t (ns)")
        bx.set_ylabel("underside gap (nm)")
        bx.legend(frameon=False, fontsize=6.5, loc="center right")
        return []

    FuncAnimation(fig, draw, frames=len(frames), blit=False).save(out_gif, writer=PillowWriter(fps=6), dpi=72)


if __name__ == "__main__":
    main(*sys.argv[1:3])
