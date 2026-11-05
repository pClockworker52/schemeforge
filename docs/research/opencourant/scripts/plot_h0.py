"""Figure for CS-13 rung H0: temperature profiles at t_end (Isolid = 17 quads and bricks) against erfc.

Usage: python plot_h0.py <work_dir> <out_png>
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h0_conduction as h  # noqa: E402

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "text.color": INK,
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 8.5,
                     "axes.spines.top": False, "axes.spines.right": False})


def main(work, out):
    fig, ax = plt.subplots(figsize=(6.4, 3.6), constrained_layout=True)
    ax.grid(color=GRID, lw=0.6)
    zz = np.linspace(0, h.L, 801)
    q = np.load(os.path.join(work, "H0q0156", "profile.npy"), allow_pickle=True).item()
    ax.plot((zz - h.L / 2) * 1e6, h.exact(zz, q["t"]), color=INK2, lw=2.4, label=f"erfc, t = {q['t'] * 1e9:.2f} ns")
    b = np.load(os.path.join(work, "H0b0625", "profile.npy"), allow_pickle=True).item()
    ax.plot((b["z"] - h.L / 2) * 1e6, b["T"], "o", color="#2a78d6", ms=4, label="bricks Isolid 17, h = 0.625 µm")
    ax.plot((q["z"] - h.L / 2) * 1e6, q["T"], "-", color="#eb6834", lw=1.4, drawstyle="steps-mid",
            label="axisymmetric quads Isolid 17, h = 0.156 µm")
    ax.set_xlim(-4, 4)
    ax.set_xlabel("z − L/2 (µm)")
    ax.set_ylabel("T (K)")
    ax.set_title("CS-13 rung H0: conduction of a 100 K step, Al, k = 237 W/(m K)", loc="left")
    ax.legend(frameon=False, fontsize=7)
    fig.savefig(out, dpi=130)


if __name__ == "__main__":
    main(*sys.argv[1:3])
