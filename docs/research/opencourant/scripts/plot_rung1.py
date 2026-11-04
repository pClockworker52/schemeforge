"""Figure for rung 1 (Hertz sphere): force histories and metric convergence, OpenCourant vs JAX vs Hertz.

Usage: python plot_rung1.py <oc_traces.npy> <jax.npy> <oc_csv> <out_png>
"""

import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rung1  # noqa: E402

SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "axes.edgecolor": AXIS,
    "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK, "font.size": 9,
    "axes.titlesize": 9.5, "axes.spines.top": False, "axes.spines.right": False,
})
oc = np.load(sys.argv[1], allow_pickle=True).item()
jx = np.load(sys.argv[2], allow_pickle=True).item()
rows = [r for r in csv.DictReader(open(sys.argv[3])) if not r.get("failed")]
H = rung1.hertz()
NU_FINE = max(jx)

fig, axs = plt.subplots(2, 2, figsize=(8.6, 6.4), constrained_layout=True)
(a, b), (c, d) = axs
for ax in axs.ravel():
    ax.grid(color=GRID, lw=0.6)

a.plot(H["t"] / H["t_contact"], H["F"] / H["F_max"], color=INK2, lw=2.4, label="Hertz (quasi-static)")
j = jx[NU_FINE]
a.plot(j["t"], j["f"], color=BLUE, lw=1.6, label=f"JAX {NU_FINE}×{2 * NU_FINE}")
for var, col, ls in (("I17_q0_dt0.4", ORANGE, "-"), ("I0_q0_dt0.4", AQUA, (0, (4, 2)))):
    key = next((k for k in (f"{var}|{NU_FINE}", f"{var}|15") if k in oc), None)
    if key:
        tf, f, _, _ = oc[key]
        a.plot(tf, f, color=col, lw=1.4, ls=ls, label=f"OpenCourant {key.split('|')[1]}×{2 * int(key.split('|')[1])}, Isolid {var[1:].split('_')[0]}")
a.set_xlim(0, 1.6)
a.set_ylim(-0.1, 1.9)
a.set_xlabel("t / t_Hertz")
a.set_ylabel("wall force / F_Hertz")
a.set_title("(a) Wall force", loc="left")
a.legend(frameon=False, fontsize=7, loc="upper right")

b.plot(j["t"], j["v"], color=BLUE, lw=1.6, label=f"JAX {NU_FINE}×{2 * NU_FINE}")
for var, col, ls in (("I17_q0_dt0.4", ORANGE, "-"), ("I0_q0_dt0.4", AQUA, (0, (4, 2)))):
    key = next((k for k in (f"{var}|{NU_FINE}", f"{var}|15") if k in oc), None)
    if key:
        _, _, tt, vv = oc[key]
        b.plot(tt, vv, color=col, lw=1.4, ls=ls, label=f"OpenCourant {key.split('|')[1]}×{2 * int(key.split('|')[1])}, Isolid {var[1:].split('_')[0]}")
b.axhline(1.0, color=INK2, lw=0.8)
b.set_xlim(0, 1.6)
b.set_xlabel("t / t_Hertz")
b.set_ylabel("centre-of-mass velocity / V")
b.set_title("(b) Centre-of-mass velocity", loc="left")
b.legend(frameon=False, fontsize=7, loc="lower right")

ns = sorted(jx)
STY = {"JAX": (BLUE, "o", "-"), "I17_q0_dt0.4": (ORANGE, "s", "-")}


def series(var, key):
    if var == "JAX":
        return np.array(ns), np.array([jx[n][key] for n in ns])
    rs = sorted([r for r in rows if r["variant"] == var], key=lambda r: int(r["n_u"]))
    return np.array([int(r["n_u"]) for r in rs]), np.array([float(r[key]) for r in rs])


for var, (col, mk, ls) in STY.items():
    lab = "JAX" if var == "JAX" else "OpenCourant Isolid 17"
    n_, ct = series(var, "contact")
    _, pk = series(var, "peak")
    c.plot(n_, ct, color=col, marker=mk, ms=8, lw=1.6, ls=ls, label=f"{lab}: contact time")
    c.plot(n_, pk, color=col, marker=mk, ms=6, lw=1.0, ls=":", mfc=SURF, label=f"{lab}: peak force")
    _, rb = series(var, "rebound")
    _, ap = series(var, "approach")
    d.plot(n_, rb, color=col, marker=mk, ms=8, lw=1.6, ls=ls, label=f"{lab}: rebound / V")
    d.plot(n_, ap, color=col, marker=mk, ms=6, lw=1.0, ls=":", mfc=SURF, label=f"{lab}: max approach")
for ax in (c, d):
    ax.axhline(1.0, color=INK2, lw=0.8)
    ax.set_xscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([f"{n}×{2 * n}" for n in ns])
    ax.minorticks_off()
    ax.set_xlabel("mesh n_u × n_v")
    ax.set_ylabel("ratio to Hertz")
c.set_title("(c) Contact time (solid), peak force (dotted)", loc="left")
d.set_title("(d) Rebound (solid), max approach (dotted)", loc="left")
c.legend(frameon=False, fontsize=6.5, loc="best")
d.legend(frameon=False, fontsize=6.5, loc="best")
fig.savefig(sys.argv[4], dpi=130)
