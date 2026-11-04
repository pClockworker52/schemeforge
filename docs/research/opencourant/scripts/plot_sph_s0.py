"""Figure for SPH rungs S0 and S0p: wall-force histories and metric convergence against the exact solution and the
2D Isolid = 17 quads.

Usage: python plot_sph_s0.py <work_dir> <s0_csv> <s0p_csv> <rung0_quad_csv> <rung0p_quad_csv> <out_png>
"""

import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
SEQ = {25: "#9ec5f4", 50: "#3987e5", 100: "#184f95", 200: "#0b0b0b"}
VAR = {"h11": ("#2a78d6", "o", "SPH h = 1.12 s"), "h12": ("#1baf7a", "^", "SPH h = 1.25 s"),
       "base": ("#eb6834", "s", "SPH h = 1.5 s"), "quad": ("#52514e", "D", "2D quad, Isolid 17")}
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "text.color": INK,
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 8.5,
                     "axes.spines.top": False, "axes.spines.right": False})


def main(work, s0_csv, s0p_csv, q0_csv, q0p_csv, out):
    s0 = list(csv.DictReader(open(s0_csv)))
    s0p = list(csv.DictReader(open(s0p_csv)))
    q0 = [r for r in csv.DictReader(open(q0_csv)) if r["variant"] == "A_q0_dt0.4"]
    q0p = [r for r in csv.DictReader(open(q0p_csv)) if r["variant"] == "q_default_dt0.4" and float(r["V"]) == 50]
    fig, axs = plt.subplots(2, 3, figsize=(11, 6.2), constrained_layout=True)
    for ax in axs.ravel():
        ax.grid(color=GRID, lw=0.6)
    a = axs[0, 0]
    for n in (25, 50, 100, 200):
        d = np.load(os.path.join(work, f"S0h11{n:04d}", "trace.npy"), allow_pickle=True).item()
        a.plot(d["t"], -d["fw"], color=SEQ[n], lw=1.3, label=f"{n} particles along L")
    a.axhline(1.0, color=INK2, lw=0.8, ls=":")
    a.set_xlim(0, 1.3)
    a.set_ylim(-0.05, 1.15)
    a.set_xlabel("t / (2L/c_d)")
    a.set_ylabel("wall stress / ρ c_d V")
    a.set_title("(a) S0 wall stress, SPH h = 1.12 s", loc="left")
    a.legend(frameon=False, fontsize=7, loc="lower left")

    def series(rows, key, nkey="n_z"):
        rs = sorted(rows, key=lambda r: int(r[nkey]))
        return np.array([int(r[nkey]) for r in rs]), np.array([float(r[key]) for r in rs])

    for ax, key, title in ((axs[0, 1], "contact", "(b) S0 contact time / (2L/c_d)"),
                           (axs[0, 2], "rebound", "(c) S0 rebound / V")):
        for var, (col, mk, lab) in VAR.items():
            rows = q0 if var == "quad" else [r for r in s0 if r["variant"] == var]
            if rows:
                n, y = series(rows, key)
                ax.plot(n, y, color=col, marker=mk, ms=6, lw=1.4, label=lab)
        ax.axhline(1.0, color=INK2, lw=0.8, ls=":")
        ax.set_xscale("log")
        ax.set_xticks([25, 50, 100, 200])
        ax.set_xticklabels(["25", "50", "100", "200"])
        ax.minorticks_off()
        ax.set_xlabel("particles (elements) along L")
        ax.set_title(title, loc="left")
    axs[0, 2].legend(frameon=False, fontsize=7, loc="lower right")
    for ax, key, title in ((axs[1, 0], "sigma2_profile", "(d) S0p plastic plateau / σ₂"),
                           (axs[1, 1], "sigmaHEL_profile", "(e) S0p elastic precursor / σ_HEL"),
                           (axs[1, 2], "epsp_behind_plastic_wave", "(f) S0p ε_p behind plastic wave / exact")):
        for var, (col, mk, lab) in VAR.items():
            rows = q0p if var == "quad" else [r for r in s0p if r["variant"] == var]
            rows = [r for r in rows if r[key] not in ("", "nan")]
            if rows:
                n, y = series(rows, key)
                ax.plot(n, y, color=col, marker=mk, ms=6, lw=1.4, label=lab)
        ax.axhline(1.0, color=INK2, lw=0.8, ls=":")
        ax.set_xscale("log")
        ax.set_xticks([25, 50, 100, 200])
        ax.set_xticklabels(["25", "50", "100", "200"])
        ax.minorticks_off()
        ax.set_xlabel("particles (elements) along L")
        ax.set_title(title, loc="left")
    axs[1, 2].legend(frameon=False, fontsize=7, loc="lower right")
    fig.suptitle("3D SPH confined column (S0 elastic, S0p elastic-perfectly-plastic) against the exact 1D solution; "
                 "default artificial viscosity; quads with q ≈ 0 (S0) and default q (S0p)", x=0.01, ha="left",
                 fontsize=9)
    fig.savefig(out, dpi=130)


if __name__ == "__main__":
    main(*sys.argv[1:7])
