"""Figure for the CS-11 sweep, setup F: (a) jetting metric J(V) of the particle and J_s(V) of the substrate,
(b) time at which the brick mesh collapses (run stop), both against impact speed, for s = R/16 (full sweep) and
R/24, R/32 (diagnostic velocities). Unevaluable runs (stop before 0.1 D/V) are drawn hollow.

Usage: python plot_cs11_sweep.py <sweep.csv> <out_png>
"""

import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
SEQ = {16: "#9ec5f4", 24: "#3987e5", 32: "#0d366b"}
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "text.color": INK,
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 8.5,
                     "axes.spines.top": False, "axes.spines.right": False})


def main(sweep_csv, out):
    rows = [r for r in csv.DictReader(open(sweep_csv)) if r["setup"] == "F"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 3.9), constrained_layout=True)
    for ax in (a, b):
        ax.grid(color=GRID, lw=0.6)
    for n in (16, 24, 32):
        rs = sorted([r for r in rows if int(r["n_r"]) == n], key=lambda r: float(r["V"]))
        if not rs:
            continue
        V = [float(r["V"]) for r in rs]
        ev = [r["evaluable"] == "True" for r in rs]
        col = SEQ[n]
        for key, mk, ls, lab in (("J", "o", "-", "J (particle)"), ("J_s", "s", ":", "J_s (substrate)")):
            y = [float(r[key]) for r in rs]
            a.plot(V, y, color=col, ls=ls, lw=1.3)
            a.scatter([v for v, e in zip(V, ev, strict=True) if e], [q for q, e in zip(y, ev, strict=True) if e],
                      color=col, marker=mk, s=28, zorder=3, label=f"R/{n} {lab}")
            a.scatter([v for v, e in zip(V, ev, strict=True) if not e],
                      [q for q, e in zip(y, ev, strict=True) if not e], facecolor=SURF, edgecolor=col, marker=mk,
                      s=28, zorder=3)
        ts = [float(r["t_stop_over_D_V"]) for r in rs]
        b.plot(V, ts, color=col, lw=1.4, marker="o", ms=5, label=f"s = R/{n}")
    a.axhline(1.5, color=INK2, lw=1.0, ls="--")
    a.text(410, 1.53, "J* = 1.5", color=INK2, fontsize=7)
    for yv, txt in ((1.25, "1.25"), (2.0, "2.0")):
        a.axhline(yv, color=MUTED, lw=0.7, ls="--")
        a.text(410, yv + 0.03, f"J* = {txt} (sensitivity)", color=MUTED, fontsize=6.5)
    a.set_xlabel("impact speed V (m/s)")
    a.set_ylabel("max u_r / V up to the stop (≤ t_e)")
    a.set_title("(a) Jetting metric, setup F (hollow: unevaluable)", loc="left")
    a.legend(frameon=False, fontsize=6.5, ncol=2, loc="lower right")
    b.axhline(0.25, color=INK2, lw=1.0, ls="--")
    b.text(410, 0.255, "t_e = 0.25 D/V", color=INK2, fontsize=7)
    b.axhline(0.10, color=INK2, lw=1.0, ls=":")
    b.text(410, 0.103, "evaluability limit 0.1 D/V", color=INK2, fontsize=7)
    b.set_ylim(0, 0.28)
    b.set_xlabel("impact speed V (m/s)")
    b.set_ylabel("brick collapse time / (D/V)")
    b.set_title("(b) Run stop on time-step collapse (contact-edge bricks)", loc="left")
    b.legend(frameon=False, fontsize=7, loc="upper right")
    fig.suptitle("CS-11, Al–Al d = 15 µm, setup F (SPH particle on Isolid = 17 bricks, TYPE7 frictionless), quarter "
                 "symmetry", x=0.01, ha="left", fontsize=9.5)
    fig.savefig(out, dpi=130)


if __name__ == "__main__":
    main(*sys.argv[1:3])
