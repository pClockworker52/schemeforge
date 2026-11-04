"""Figures for the option-1 diagnostic (option1_alal.py): edge plastic strain histories and an impact GIF.

Usage: python plot_option1.py <work_dir> <option1_csv> <out_png> <gif_case> <out_gif>
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

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "openradioss", "scripts"))
import vtkread  # noqa: E402

R = 10e-6
SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
MESH_COL = {"coarse": "#86b6ef", "medium": "#2a78d6", "fine": "#0d366b"}
SEQ = LinearSegmentedColormap.from_list("b", ["#f0efec", "#9ec5f4", "#3987e5", "#184f95", "#0d366b"])
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                     "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
                     "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})


def main(work, csv_path, out_png, gif_case, out_gif):
    rows = list(csv.DictReader(open(csv_path)))
    vs = sorted({float(r["V"]) for r in rows})
    t_ref = {}  # reference penetration time (D/V units) per velocity, from the coarsest run that reached it
    for mesh in ("coarse", "medium", "fine"):
        for r in rows:
            tp = float(r["t_pen_over_D_V"]) if r["t_pen_over_D_V"] not in ("", "nan") else float("nan")
            if r["mesh"] == mesh and tp == tp:
                t_ref.setdefault(float(r["V"]), tp)
    fig, axs = plt.subplots(1, len(vs), figsize=(3.0 * len(vs) + 0.6, 3.4), sharey=True, constrained_layout=True)
    for ax, V in zip(np.atleast_1d(axs), vs, strict=True):
        ax.grid(color=GRID, lw=0.6)
        for r in [r for r in rows if float(r["V"]) == V]:
            name = f"A{int(V):04d}{r['mesh'][0].upper()}"
            em = np.load(os.path.join(work, name, "edge.npy"), allow_pickle=True)
            t = np.array([e["t"] for e in em]) * V / (2 * R)
            keep = t <= t_ref[V] + 1e-9  # after the end of penetration the contact edge is not defined
            t = t[keep]
            ep = np.array([e["ep_edge_particle"] for e in em])[keep]
            es = np.array([e["ep_edge_substrate"] for e in em])[keep]
            col = MESH_COL[r["mesh"]]
            ax.plot(t, ep, color=col, lw=1.8, label=f"{r['mesh']} (h = {float(r['h_um']):.3g} µm), particle")
            ax.plot(t, es, color=col, lw=1.0, ls=(0, (4, 2)), label=f"{r['mesh']}, substrate")
            if not r["stop_reason"].startswith("reached"):
                ax.plot(t[-1], ep[-1], "X", color=col, ms=10, mec=SURF)
                ax.plot(t[-1], es[-1], "X", color=col, ms=8, mec=SURF)
        ax.axvline(t_ref[V], color=INK2, lw=0.8, ls=":")
        ax.text(t_ref[V], 0.98, " t_p", transform=ax.get_xaxis_transform(), fontsize=7.5, color=INK2, va="top")
        ax.set_title(f"V = {V:.0f} m/s", loc="left")
        ax.set_xlabel("t / (D/V)")
        ax.set_xlim(0, 1.4)
    np.atleast_1d(axs)[0].set_ylabel("max. eq. plastic strain near contact edge")
    np.atleast_1d(axs)[-1].legend(frameon=False, fontsize=6.5, loc="upper left")
    fig.suptitle("Al on Al, Lagrangian, Isolid 17, no erosion: plastic strain within 2.5 h of the contact edge, "
                 "up to t_p (× = mesh failure)", x=0.06, ha="left", fontsize=9.5)
    fig.savefig(out_png, dpi=130)
    plt.close(fig)

    d = os.path.join(work, gif_case)
    vt = sorted(glob.glob(os.path.join(d, f"{gif_case}A*.vtk")))
    frames = [vtkread.read(v) for v in vt]
    n_p = int(next(r for r in rows if f"A{int(float(r['V'])):04d}{r['mesh'][0].upper()}" == gif_case)["particle_el"])
    norm = Normalize(0, 3)
    fig = plt.figure(figsize=(6.4, 4.0))
    ax = fig.add_axes([0.08, 0.12, 0.78, 0.78])
    cax = fig.add_axes([0.88, 0.2, 0.02, 0.6])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=SEQ), cax=cax)
    cb.set_label("eq. plastic strain (–)", color=INK2)
    cb.outline.set_visible(False)
    V = float(gif_case[1:5])

    def draw(i):
        fr = frames[i]
        ax.clear()
        eid = fr["cell"]["ELEMENT_ID"].astype(int)
        xy = fr["xyz"][:, 1:3] * 1e6
        ep = fr["cell"]["2DELEM_Plastic_Strain"]
        for lo, hi, edge in ((n_p + 1, 10**9, "#a23a12"), (1, n_p, "#0d366b")):
            sel = (eid >= lo) & (eid <= hi)
            cells = [c for c, s in zip(fr["cells"], sel, strict=True) if s]
            for sgn in (1.0, -1.0):
                ax.add_collection(PolyCollection([xy[c] * np.array([sgn, 1.0]) for c in cells], array=ep[sel],
                                                 cmap=SEQ, norm=norm, edgecolors=edge, linewidths=0.08))
        ax.set_xlim(-22, 22)
        ax.set_ylim(-10, 12)
        ax.set_aspect("equal")
        ax.set_xlabel("r (µm), mirrored")
        ax.set_ylabel("z (µm)")
        ax.set_title(f"Al on Al, {V:.0f} m/s, {gif_case[-1]} mesh, t = {fr['time'] * V / (2 * R):4.2f} D/V",
                     loc="left", fontsize=9)
        return []

    FuncAnimation(fig, draw, frames=len(frames), blit=False).save(out_gif, writer=PillowWriter(fps=8), dpi=56)


if __name__ == "__main__":
    main(*sys.argv[1:6])
