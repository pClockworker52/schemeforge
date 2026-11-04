"""Figure: rung 0, OpenCourant vs the JAX code vs the exact 1D solution.

Usage: python plot_rung0.py <oc_traces.npy> <jax_traces.npy> <oc_csv> <out_png>
oc_traces: {"<variant>|<n>": (t_f/t_c, F/F_ex, t/t_c, v/V)} from rung0.py
jax_traces: {n: (t/t_c, F/F_ex, v/V)} from impact_axisym.confined_plate_on_rigid_wall
"""

import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SER = {"JAX": "#2a78d6", "A_q0_dt0.4": "#eb6834", "B_q0_dt0.9": "#1baf7a", "C_default": "#eda100"}
LAB = {"JAX": "JAX (rung 0)", "A_q0_dt0.4": "OpenCourant A: q≈0, dt×0.4",
       "B_q0_dt0.9": "OpenCourant B: q≈0, dt×0.9", "C_default": "OpenCourant C: defaults"}
MRK = {"JAX": "o", "A_q0_dt0.4": "s", "B_q0_dt0.9": "^", "C_default": "D"}
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "axes.edgecolor": AXIS,
    "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK, "font.size": 9,
    "axes.titlesize": 9.5, "axes.spines.top": False, "axes.spines.right": False,
})

oc = np.load(sys.argv[1], allow_pickle=True).item()
jx = np.load(sys.argv[2], allow_pickle=True).item()
rows = [r for r in csv.DictReader(open(sys.argv[3])) if not r.get("failed")]
N = 100

fig, axs = plt.subplots(2, 2, figsize=(8.6, 6.4), constrained_layout=True)
(a, b), (c, d) = axs
for ax in axs.ravel():
    ax.grid(color=GRID, lw=0.6)

t, f, v = jx[N]
a.plot(t, f, color=SER["JAX"], lw=2, label=LAB["JAX"])
b.plot(t, v, color=SER["JAX"], lw=2, label=LAB["JAX"])
for var, ls in (("A_q0_dt0.4", "-"), ("C_default", (0, (4, 2)))):
    tf, ff, tt, vv = oc[f"{var}|{N}"]
    a.plot(tf, ff, color=SER[var], lw=1.6, ls=ls, label=LAB[var])
    b.plot(tt, vv, color=SER[var], lw=1.6, ls=ls, label=LAB[var])
for ax in (a, b):
    ax.axvline(1.0, color=MUTED, lw=0.8, ls=":")
    ax.set_xlim(0, 1.5)
    ax.set_xlabel("t / (2L/c_d)")
a.axhline(1.0, color=INK2, lw=0.8)
a.set_ylim(-0.1, 1.6)
oc_plateau = np.mean([float(r["plateau"]) for r in rows if r["variant"] == "A_q0_dt0.4"])
a.text(0.5, 0.45, f"OpenCourant plateau {oc_plateau:.4f}\n(all meshes; finite strain)\nJAX plateau 1.0000", ha="center",
       va="bottom", fontsize=7.5, color=INK2)
a.set_ylabel("wall force / (ρ c_d V πL²)")
a.set_title(f"(a) Wall force, {N} elements through the thickness", loc="left")
a.legend(frameon=False, fontsize=7.5, loc="upper right")
b.axhline(1.0, color=INK2, lw=0.8)
b.set_ylim(-1.1, 1.1)
b.set_ylabel("centre-of-mass velocity / V")
b.set_title(f"(b) Centre-of-mass velocity, {N} elements", loc="left")


def series(var, key):
    rs = [r for r in rows if r["variant"] == var]
    return np.array([int(r["n_z"]) for r in rs]), np.array([float(r[key]) for r in rs])


ns = np.array(sorted(jx))
jc = np.array([jx[n][0][jx[n][1] > 1e-9].max() for n in ns])
jr = np.array([jx[n][2][-1] for n in ns])
c.plot(ns, 100 * (jc - 1), color=SER["JAX"], marker=MRK["JAX"], ms=8, lw=2, label=LAB["JAX"])
d.plot(ns, 1 - jr, color=SER["JAX"], marker=MRK["JAX"], ms=8, lw=2, label=LAB["JAX"])
for var in ("A_q0_dt0.4", "B_q0_dt0.9", "C_default"):
    n_, ct = series(var, "contact")
    _, rb = series(var, "rebound")
    c.plot(n_, 100 * (ct - 1), color=SER[var], marker=MRK[var], ms=8, lw=1.6, label=LAB[var])
    d.plot(n_, 1 - rb, color=SER[var], marker=MRK[var], ms=8, lw=1.6, label=LAB[var])
for ax in (c, d):
    ax.set_xscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([str(n) for n in ns])
    ax.minorticks_off()
    ax.set_xlabel("elements through the thickness")
c.axhline(0, color=INK2, lw=0.8)
c.set_ylabel("contact time error (%)")
c.set_title("(c) Contact time vs 2L/c_d", loc="left")
d.set_yscale("log")
d.set_ylabel("1 − rebound velocity / V")
d.set_title("(d) Rebound deficit (exact: 0)", loc="left")
d.legend(frameon=False, fontsize=7.5, loc="lower left")
d.text(195, 0.024, "C at 200 elements:\nrun stopped\n(negative volume)", ha="right", va="center", fontsize=7.5,
       color=INK2)
fig.savefig(sys.argv[4], dpi=130)
