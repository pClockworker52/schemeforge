"""Figure for the CS-11 prerequisite rungs F0 (SPH sphere on TYPE7 bricks) and W0 (SPH sphere on an SPH block):
contact force and centre-of-mass approach against two-body Hertz at 20 m/s.

Usage: python plot_f0w0.py <work_dir> <out_png> <run name>:<label> [...]
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sph_f0w0 as fw  # noqa: E402

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
COL = {"F": ("#9ec5f4", "#2a78d6"), "W": ("#f5b59b", "#eb6834")}
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "text.color": INK,
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 8.5,
                     "axes.spines.top": False, "axes.spines.right": False})


def main(work, out, *runs):
    H = fw.hertz2()
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 3.8), constrained_layout=True)
    for ax in (a, b):
        ax.grid(color=GRID, lw=0.6)
    a.plot(H["t"] / H["t_contact"], H["F"] / H["F_max"], color=INK2, lw=2.4, label="two-body Hertz")
    th = H["t"]
    # Hertz approach from the force: m d'' = -F  ->  d = (F / k)^(2/3)
    k = 4 / 3 * fw.r1.E / 2 / (1 - fw.r1.NU**2) * np.sqrt(fw.r1.R)
    b.plot(th / H["t_contact"], (H["F"] / k) ** (2 / 3) / H["d_max"], color=INK2, lw=2.4, label="two-body Hertz")
    for spec in runs:
        name, label = spec.split(":", 1)
        tr = np.load(os.path.join(work, name, "trace.npy"), allow_pickle=True).item()
        setup = "W" if name.startswith("W") else "F"
        fine = "n032" in name
        col = COL[setup][1 if fine else 0]
        f = np.convolve(tr["f"], np.ones(5) / 5, "same")
        a.plot(tr["t"], f, color=col, lw=1.4, label=label)
        b.plot(tr["tv"], tr["appr"], color=col, lw=1.4, label=label)
    a.set_xlim(0, 1.6)
    a.set_ylim(-0.1, 1.5)
    a.set_xlabel("t / t_Hertz (two-body)")
    a.set_ylabel("contact force / F_Hertz")
    a.set_title("(a) Contact force, 20 m/s (5-sample mean)", loc="left")
    a.legend(frameon=False, fontsize=7)
    b.set_xlim(0, 1.6)
    b.set_ylim(-0.1, 1.2)
    b.set_xlabel("t / t_Hertz (two-body)")
    b.set_ylabel("centre-of-mass approach / d_Hertz")
    b.set_title("(b) Approach from geometric first contact", loc="left")
    b.legend(frameon=False, fontsize=7)
    fig.suptitle("CS-11 rungs F0 (SPH sphere on Isolid = 17 bricks, TYPE7, friction 0) and W0 (SPH sphere on SPH "
                 "block, kernel-welded), elastic, quarter symmetry", x=0.01, ha="left", fontsize=9.5)
    fig.savefig(out, dpi=130)


if __name__ == "__main__":
    main(*sys.argv[1:])
