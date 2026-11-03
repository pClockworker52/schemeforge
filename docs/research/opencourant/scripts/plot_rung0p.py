"""Figures for rung 0p (elastic-perfectly-plastic confined plate): static summary PNG and a profile GIF.

Usage: python plot_rung0p.py <traces.npy> <rung0p_csv> <out_png> <out_gif>
"""

import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rung0p as rp  # noqa: E402

SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "axes.edgecolor": AXIS,
    "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK, "font.size": 9,
    "axes.titlesize": 9.5, "axes.spines.top": False, "axes.spines.right": False,
})
tr = np.load(sys.argv[1], allow_pickle=True).item()
rows = [r for r in csv.DictReader(open(sys.argv[2])) if not r.get("failed")]
V = 50.0
ex = rp.exact(V)
MPA = 1e-6
VAR = {"q0_dt0.4": ("q≈0", ORANGE, "s", "-"), "q_default_dt0.4": ("q default", AQUA, "^", (0, (4, 2)))}

fig, axs = plt.subplots(2, 2, figsize=(8.6, 6.4), constrained_layout=True)
(a, b), (c, d) = axs
for ax in axs.ravel():
    ax.grid(color=GRID, lw=0.6)

for var, (lab, col, _, ls) in VAR.items():
    key = [k for k, v in tr.items() if v["V"] == V and v["n"] == 200 and v["var"] == var][0]
    a.plot(tr[key]["tf"], tr[key]["f"], color=col, lw=1.6, ls=ls, label=f"OpenCourant, 200 el., {lab}")
a.plot([0, 1, 1], [1, 1, 0], color=BLUE, lw=2, label="closed form σ₂ (until 2L/c_d)", zorder=0)
a.set_xlim(0, 1.5)
a.set_ylim(-0.1, 1.5)
a.set_xlabel("t / (2L/c_d)")
a.set_ylabel("wall force / (σ₂ πL²)")
a.set_title(f"(a) Wall force, V = {V:.0f} m/s", loc="left")
a.legend(frameon=False, fontsize=7.5, loc="upper right")

t_snap = 0.75 * rp.L / rp.C_D
zz = np.linspace(0, rp.L, 2001)
b.plot(zz * 1e6, rp.exact_profile(V, t_snap, zz) * MPA, color=BLUE, lw=2, label="closed form")
for n, col, ls in ((50, MUTED, (0, (4, 2))), (200, ORANGE, "-")):
    key = [k for k, v in tr.items() if v["V"] == V and v["n"] == n and v["var"] == "q0_dt0.4"][0]
    prof = tr[key]["profiles"]
    k = int(np.argmin([abs(p[0] - t_snap) for p in prof]))
    b.plot(prof[k][1] * 1e6, prof[k][2] * MPA, color=col, lw=1.6, ls=ls, label=f"OpenCourant {n} el., q≈0")
b.set_xlabel("initial position z₀ (µm), wall at 0")
b.set_ylabel("|σ_zz| = p + ⅔σ_vM (MPa)")
b.set_title("(b) Stress profile at t = 0.75 L/c_d", loc="left")
b.annotate("plastic wave (c_b)", (rp.C_B * t_snap * 1e6, 0.5 * (ex["sigma_2"] + rp.S_HEL) * MPA), xytext=(1.0, 380),
           fontsize=7.5, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
b.annotate("elastic precursor σ_HEL (c_d)", (rp.C_D * t_snap * 1e6 - 0.3, rp.S_HEL * MPA), xytext=(6.9, 470),
           fontsize=7.5, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
b.legend(frameon=False, fontsize=7.5, loc="lower left")


def series(var, key):
    rs = sorted([r for r in rows if r["variant"] == var and float(r["V"]) == V], key=lambda r: int(r["n_z"]))
    return np.array([int(r["n_z"]) for r in rs]), np.array([float(r[key]) for r in rs])


for var, (lab, col, mk, ls) in VAR.items():
    n_, wp = series(var, "wall_plateau")
    c.plot(n_, wp, color=col, marker=mk, ms=8, lw=1.6, ls=ls, label=f"wall plateau / σ₂, {lab}")
    n_, cb = series(var, "c_b_front")
    d.plot(n_, cb, color=col, marker=mk, ms=8, lw=1.6, ls=ls, label=f"plastic front / c_b, {lab}")
    n_, cdf = series(var, "c_d_front")
    d.plot(n_, cdf, color=col, marker="o", ms=6, lw=1.0, ls=":", label=f"elastic front / c_d, {lab}")
for ax in (c, d):
    ax.axhline(1.0, color=BLUE, lw=2, zorder=0)
    ax.set_xscale("log")
    ax.set_xticks([25, 50, 100, 200])
    ax.set_xticklabels(["25", "50", "100", "200"])
    ax.minorticks_off()
    ax.set_xlabel("elements through the thickness")
c.set_ylabel("ratio to closed form")
c.set_title("(c) Wall stress plateau", loc="left")
c.legend(frameon=False, fontsize=7.5, loc="lower right")
d.set_ylabel("front speed / closed form")
d.set_title("(d) Front speeds at t = 0.75 L/c_d (mid-level crossing)", loc="left")
d.legend(frameon=False, fontsize=7, loc="upper right")
fig.savefig(sys.argv[3], dpi=130)
plt.close(fig)

# ---- GIF: stress profile vs time, 200 elements, q≈0 ----
key = [k for k, v in tr.items() if v["V"] == V and v["n"] == 200 and v["var"] == "q0_dt0.4"][0]
prof = tr[key]["profiles"]
fig, ax = plt.subplots(figsize=(6.0, 3.6), constrained_layout=True)


def draw(i):
    ax.clear()
    ax.grid(color=GRID, lw=0.6)
    t, z0, s = prof[i]
    if t <= rp.L / rp.C_D:
        ax.plot(zz * 1e6, rp.exact_profile(V, t, zz) * MPA, color=BLUE, lw=2, label="closed form")
    else:
        ax.text(0.98, 0.95, "precursor reflected at the back face:\nclosed form not drawn", transform=ax.transAxes,
                ha="right", va="top", fontsize=7.5, color=INK2)
    ax.plot(z0 * 1e6, s * MPA, color=ORANGE, lw=1.6, label="OpenCourant, 200 el., q≈0")
    ax.set_xlim(0, rp.L * 1e6)
    ax.set_ylim(-150, 1000)
    ax.set_xlabel("initial position z₀ (µm); rigid wall at z₀ = 0")
    ax.set_ylabel("|σ_zz| (MPa)")
    ax.set_title(f"Elastic-plastic plate, V = {V:.0f} m/s     t = {t * 1e9:5.2f} ns  ({t * rp.C_D / rp.L:4.2f} L/c_d)",
                 loc="left", fontsize=9)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    return []


anim = FuncAnimation(fig, draw, frames=len(prof), blit=False)
anim.save(sys.argv[4], writer=PillowWriter(fps=8), dpi=80)
print("frames", len(prof))
