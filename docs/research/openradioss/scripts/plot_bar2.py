"""Plots for the OpenCourant axisymmetric ALE QA deck BAR2V41B (Taylor-type copper rod impact).

Inputs: anim_to_vtk output (81 frames, 1 us apart) and th_to_csv output of the same run.
Deck units are g, cm, us (inferred): energy unit g cm^2/us^2 = 1e5 J, pressure unit Mbar = 100 GPa.
Usage: python plot_bar2.py <vtk_dir> <th_csv> <out_dir>
"""
import csv
import glob
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vtkread  # noqa: E402

VTK_DIR, TH_CSV, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)

# palette (dataviz reference instance, light mode)
SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE = "#2a78d6", "#eb6834"
SEQ = LinearSegmentedColormap.from_list(
    "blue_seq", ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"])
DIV = LinearSegmentedColormap.from_list("blue_red", ["#104281", "#3987e5", "#f0efec", "#e34948", "#8f1f1f"])
E_UNIT_J = 1e5
P_UNIT_GPA = 100.0

plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": INK, "font.size": 9, "axes.titlesize": 9.5, "axes.titlecolor": INK,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
})

frames = [vtkread.read(f) for f in sorted(glob.glob(os.path.join(VTK_DIR, "BAR2V41BA*.vtk")))]
times = np.array([f["time"] for f in frames])
R0 = frames[0]["xyz"][:, 1].max()
L0 = frames[0]["xyz"][:, 2].max()


def polys(fr, mirror):
    """Quads in the (r, z) plane; y is radial, z is the axis (N2D3D = 1). mirror=-1 gives r -> -r."""
    yz = fr["xyz"][:, 1:3] * np.array([mirror, 1.0])
    return [yz[c] for c in fr["cells"]]


def section(ax, fr, field, cmap, norm):
    vals = fr["cell"][field]
    for m in (1.0, -1.0):
        pc = PolyCollection(polys(fr, m), array=vals, cmap=cmap, norm=norm,
                            edgecolors=(0.32, 0.32, 0.31, 0.35), linewidths=0.25)
        ax.add_collection(pc)
    ax.axvline(0, color=MUTED, lw=0.6, ls=(0, (4, 3)))
    ax.axhline(0, color=INK2, lw=1.2)
    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(-0.08, 3.35)
    ax.set_aspect("equal")
    ax.set_xticks([-0.5, 0, 0.5])
    return pc


def frame_at(t):
    return frames[int(np.argmin(abs(times - t)))]


# ---- figure 1: energy history and rod shape ratios ----
rows = list(csv.reader(open(TH_CSV)))
head, th = rows[0], np.array(rows[1:], float)
col = {n: head.index(n) for n in ("time", "INTERNAL ENERGY", "KINETIC ENERGY", "PLASTIC WORK")}
t = th[:, col["time"]]
ie = th[:, col["INTERNAL ENERGY"]] * E_UNIT_J
ke = th[:, col["KINETIC ENERGY"]] * E_UNIT_J
tot = ie + ke
L = np.array([f["xyz"][:, 2].max() for f in frames])
Rf = np.array([f["xyz"][:, 1].max() for f in frames])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 3.2), constrained_layout=True)
for ax in (a1, a2):
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_xlabel("time (µs)")
    ax.set_xlim(0, 80)
a1.plot(t, ke, color=BLUE, lw=2, label="kinetic")
a1.plot(t, ie, color=ORANGE, lw=2, label="internal")
a1.plot(t, tot, color=MUTED, lw=1.2, ls=(0, (4, 2)), label="internal + kinetic")
a1.set_ylabel("energy (J)")
a1.set_ylim(0, 40)
a1.text(78, tot[-1] + 0.6, f"total −{100 * (1 - tot[-1] / tot[0]):.1f} %", ha="right", va="bottom",
        color=INK2, fontsize=8)
a1.legend(frameon=False, loc="center right", fontsize=8)
a1.set_title("(a) Energy history (time-history file, 800 samples)", loc="left")
a2.plot(times, L / L0, color=BLUE, lw=2, label="length L / L₀")
a2.plot(times, Rf / R0, color=ORANGE, lw=2, label="max. radius R / R₀")
a2.set_ylabel("ratio (–)")
a2.set_ylim(0, 2.4)
a2.text(80, L[-1] / L0 - 0.08, f"{L[-1] / L0:.3f}", ha="right", va="top", color=INK2, fontsize=8)
a2.text(80, Rf[-1] / R0 + 0.06, f"{Rf[-1] / R0:.2f}", ha="right", va="bottom", color=INK2, fontsize=8)
a2.legend(frameon=False, loc="center right", fontsize=8)
a2.set_title("(b) Rod shape from mesh nodes (81 frames)", loc="left")
fig.savefig(os.path.join(OUT, "bar2_history.png"), dpi=130)
plt.close(fig)

# ---- figure 2: plastic strain, small multiples ----
snap = [0, 5, 10, 20, 40, 80]
pmax = max(f["cell"]["2DELEM_Plastic_Strain"].max() for f in frames)
norm = Normalize(0, np.ceil(pmax * 2) / 2)
fig, axs = plt.subplots(1, len(snap), figsize=(8.6, 3.9), sharey=True, constrained_layout=True)
for ax, ts in zip(axs, snap, strict=True):
    fr = frame_at(ts)
    pc = section(ax, fr, "2DELEM_Plastic_Strain", SEQ, norm)
    ax.set_title(f"t = {fr['time']:.0f} µs", fontsize=9)
    ax.set_xlabel("r (cm)")
axs[0].set_ylabel("z (cm)")
cb = fig.colorbar(pc, ax=axs, shrink=0.8, pad=0.01)
cb.set_label("equivalent plastic strain (–)", color=INK2)
cb.outline.set_visible(False)
fig.suptitle("Copper rod, 227 m/s onto a fixed face, axisymmetric ALE (mirrored about the axis)",
             x=0.01, ha="left", fontsize=9.5, color=INK)
fig.savefig(os.path.join(OUT, "bar2_plastic_strain.png"), dpi=130)
plt.close(fig)

# ---- figure 3: early pressure wave ----
snapp = [1, 2, 3, 4, 6, 8]
pk = max(abs(frame_at(s)["cell"]["2DELEM_Pressure"]).max() for s in snapp) * P_UNIT_GPA
lim = np.ceil(pk)
pnorm = Normalize(-lim, lim)
fig, axs = plt.subplots(1, len(snapp), figsize=(8.6, 3.9), sharey=True, constrained_layout=True)
for ax, ts in zip(axs, snapp, strict=True):
    fr = frame_at(ts)
    fr = dict(fr, cell=dict(fr["cell"], P_GPa=fr["cell"]["2DELEM_Pressure"] * P_UNIT_GPA))
    pc = section(ax, fr, "P_GPa", DIV, pnorm)
    ax.set_title(f"t = {fr['time']:.0f} µs", fontsize=9)
    ax.set_xlabel("r (cm)")
axs[0].set_ylabel("z (cm)")
cb = fig.colorbar(pc, ax=axs, shrink=0.8, pad=0.01)
cb.set_label("pressure (GPa), compression > 0", color=INK2)
cb.outline.set_visible(False)
fig.suptitle("Pressure in the first 8 µs: compression wave running up the rod from the impact face",
             x=0.01, ha="left", fontsize=9.5, color=INK)
fig.savefig(os.path.join(OUT, "bar2_pressure.png"), dpi=130)
plt.close(fig)

# ---- animation: plastic strain, 81 frames ----
fig = plt.figure(figsize=(4.4, 4.6))
ax = fig.add_axes([0.13, 0.1, 0.55, 0.82])
cax = fig.add_axes([0.74, 0.18, 0.04, 0.6])
sm = plt.cm.ScalarMappable(norm=norm, cmap=SEQ)
cb = fig.colorbar(sm, cax=cax)
cb.set_label("equiv. plastic strain (–)", color=INK2)
cb.outline.set_visible(False)


def draw(i):
    ax.clear()
    fr = frames[i]
    section(ax, fr, "2DELEM_Plastic_Strain", SEQ, norm)
    ax.set_xlabel("r (cm)")
    ax.set_ylabel("z (cm)")
    L_i = fr["xyz"][:, 2].max()
    ax.set_title(f"t = {fr['time']:4.0f} µs   L/L₀ = {L_i / L0:.3f}", loc="left", fontsize=9)
    return []


anim = FuncAnimation(fig, draw, frames=len(frames), blit=False)
anim.save(os.path.join(OUT, "bar2_plastic_strain.gif"), writer=PillowWriter(fps=10), dpi=72)
plt.close(fig)
print("frames", len(frames), "R0", R0, "L0", L0, "L_end", L[-1], "R_end", Rf[-1], "peeq_max", pmax,
      "p_peak_GPa(1-8us)", pk, "energy loss %", 100 * (1 - tot[-1] / tot[0]))
