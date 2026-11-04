"""Figure for SPH rung S1 (Hertz sphere, quarter symmetry): force histories at 20 m/s and metric convergence at
20 m/s and 2 m/s, against Hertz, the JAX code and OpenCourant Isolid = 17 (rung 1).

Usage: python plot_sph_s1.py <work_dir> <s1_csv> <rung1_jax.npy> <rung1_oc.npy> <out_png>
"""

import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rung1 as r1  # noqa: E402

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
SEQ = {16: "#9ec5f4", 32: "#3987e5", 64: "#0d366b"}
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "text.color": INK,
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 8.5,
                     "axes.spines.top": False, "axes.spines.right": False})
# rung 1 reference values (opencourant-verification.md section 5): 20 m/s at 20 x 40, 2 m/s at 15 x 30
REF = {20.0: {"JAX 20×40": (0.953, 1.073, 0.957, 0.9996), "Isolid 17, 20×40": (0.956, 1.075, 0.958, 0.9996)},
       2.0: {"JAX 15×30": (0.972, 1.045, 0.983, float("nan")), "Isolid 17, 15×30": (0.975, 1.043, 0.994, float("nan"))}}


def main(work, s1_csv, jax_npy, oc_npy, out):
    rows = [r for r in csv.DictReader(open(s1_csv)) if r.get("surface") == "conform" and r["wall"] == "rwall"
            and r["sym"] == "quarter" and float(r.get("xi_stab") or 0) == 0.0]
    H = r1.hertz()
    fig, axs = plt.subplots(2, 3, figsize=(11.5, 6.4), constrained_layout=True)
    for ax in axs.ravel():
        ax.grid(color=GRID, lw=0.6)
    a = axs[0, 0]
    a.plot(H["t"] / H["t_contact"], H["F"] / H["F_max"], color=INK2, lw=2.4, label="Hertz")
    jx = np.load(jax_npy, allow_pickle=True).item()
    a.plot(jx[20]["t"], jx[20]["f"], color=ORANGE, lw=1.2, label="JAX 20×40")
    for r in sorted([r for r in rows if float(r["V"]) == 20.0], key=lambda r: int(r["n_r"])):
        d = np.load(os.path.join(work, r["name"], "trace.npy"), allow_pickle=True).item()
        f = np.convolve(d["f"], np.ones(5) / 5, "same")
        a.plot(d["t"], f, color=SEQ[int(r["n_r"])], lw=1.3, label=f"SPH s = R/{r['n_r']}")
    a.set_xlim(0, 1.6)
    a.set_ylim(-0.1, 1.35)
    a.set_xlabel("t / t_Hertz")
    a.set_ylabel("wall force / F_Hertz")
    a.set_title("(a) Wall force, 20 m/s (SPH: 5-sample mean)", loc="left")
    a.legend(frameon=False, fontsize=7)
    b = axs[1, 0]
    for r in sorted([r for r in rows if float(r["V"]) == 20.0], key=lambda r: int(r["n_r"])):
        d = np.load(os.path.join(work, r["name"], "trace.npy"), allow_pickle=True).item()
        b.plot(d["tv"], d["v"], color=SEQ[int(r["n_r"])], lw=1.3, label=f"SPH s = R/{r['n_r']}")
    b.plot(jx[20]["t"], jx[20]["v"], color=ORANGE, lw=1.2, label="JAX 20×40")
    b.set_xlim(0, 1.6)
    b.set_xlabel("t / t_Hertz")
    b.set_ylabel("centre-of-mass velocity / V")
    b.set_title("(d) Centre-of-mass velocity, 20 m/s", loc="left")
    b.legend(frameon=False, fontsize=7, loc="lower right")
    panels = [(axs[0, 1], 20.0, ("contact", "peak"), "(b) 20 m/s: contact (—), peak (···)"),
              (axs[0, 2], 20.0, ("approach", "rebound"), "(c) 20 m/s: approach (—), rebound (···)"),
              (axs[1, 1], 2.0, ("contact", "peak"), "(e) 2 m/s: contact (—), peak (···)"),
              (axs[1, 2], 2.0, ("approach", "rebound"), "(f) 2 m/s: approach (—), rebound (···)")]
    idx = {"contact": 0, "peak": 1, "approach": 2, "rebound": 3}
    for ax, V, keys, title in panels:
        rs = sorted([r for r in rows if float(r["V"]) == V], key=lambda r: int(r["n_r"]))
        n = np.array([int(r["n_r"]) for r in rs])
        for key, ls, mk in ((keys[0], "-", "o"), (keys[1], ":", "s")):
            ax.plot(n, [float(r[key]) for r in rs], color=BLUE, ls=ls, marker=mk, ms=6, lw=1.5,
                    label=f"SPH {key}")
            for (lab, vals), col in zip(REF[V].items(), (ORANGE, AQUA), strict=True):
                if vals[idx[key]] == vals[idx[key]]:
                    ax.axhline(vals[idx[key]], color=col, lw=1.0, ls=ls, label=f"{lab} {key}")
        ax.axhline(1.0, color=INK2, lw=0.8)
        ax.set_xscale("log")
        ax.set_xticks([16, 32, 64])
        ax.set_xticklabels(["R/16", "R/32", "R/64"])
        ax.minorticks_off()
        ax.set_xlabel("particle spacing s")
        ax.set_ylabel("ratio to Hertz")
        ax.set_title(title, loc="left")
        ax.legend(frameon=False, fontsize=6.3, loc="best")
    fig.suptitle("3D SPH Hertz sphere, quarter symmetry, rigid wall on particle nodes, surface particles on the sphere",
                 x=0.01, ha="left", fontsize=9.5)
    fig.savefig(out, dpi=130)


if __name__ == "__main__":
    main(*sys.argv[1:6])
