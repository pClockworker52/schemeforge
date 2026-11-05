"""Figures for the CS-14 rung (docs/research/coldspray-cs14-rung.md): cell schematic, R0 curves, R0 crack animation.

Usage: python scripts/plot_cs14_r0.py  -> docs/research/figures/cs14/{cell.png, r0_curves.png, r0_nt8.gif}
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402
from matplotlib.collections import LineCollection  # noqa: E402

from schemeforge.research import blanket_dem as bd  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "docs" / "research" / "figures" / "cs14"
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"  # categorical slots 1-3 (reference palette)
CRIT = "#d03b3b"  # status: critical (broken bonds)
BLUES = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
                     "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def bond_segments(film, x):
    return np.stack([x[film.bi], x[film.bj]], axis=1)


def fig_cell():
    """Panel a: the R1 cell (film on a stretched substrate). Panel b: the shear-lag stress in one fragment."""
    film = bd.build_film(4, 18, seed=0)
    x = film.x0
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.0), gridspec_kw={"width_ratios": [1.4, 1]})
    a.add_collection(LineCollection(bond_segments(film, x), colors=BLUES[3], linewidths=1.0))
    a.scatter(x[:, 0], x[:, 1], s=28, color=BLUES[5], zorder=3)
    xb = x[film.bottom]
    ys = -0.9
    for xi in xb[:, 0]:
        a.plot([xi, xi], [0, ys], color=INK2, lw=0.8, ls=(0, (2, 2)))
    a.fill_between([xb[0, 0] - 1, xb[-1, 0] + 1], ys - 0.6, ys, color=GRID)
    a.annotate("", xy=(xb[-1, 0] + 1.8, ys - 0.3), xytext=(xb[-1, 0] + 0.2, ys - 0.3),
               arrowprops={"arrowstyle": "->", "color": INK})
    a.annotate("", xy=(xb[0, 0] - 1.8, ys - 0.3), xytext=(xb[0, 0] - 0.2, ys - 0.3),
               arrowprops={"arrowstyle": "->", "color": INK})
    a.text(0, ys - 1.15, "substrate, stretched to strain ε (not resolved)", ha="center", color=INK2)
    a.text(xb[-1, 0] + 0.6, 1.4, "oxide film:\ngrains on a\ntriangular lattice,\nbrittle bonds", va="center",
           fontsize=9)
    a.text(xb[0, 0] - 0.5, -0.45, "tie: elastic–perfectly plastic\nin shear (yields at τ_i)", ha="right",
           fontsize=8, color=INK2)
    a.set_xlim(xb[0, 0] - 7, xb[-1, 0] + 6)
    a.set_ylim(ys - 1.5, 3.6)
    a.set_aspect("equal")
    a.axis("off")
    a.set_title("a  Rung-R1 cell (4 rows shown; runs use 4, 8, 16)", loc="left")

    ls = 1.0
    for x0, ell in ((0.0, 1.5), (1.7, 1.2), (3.1, 1.9)):
        xs = np.linspace(0, ell, 100)
        sig = np.minimum(xs, ell - xs) / ls
        b.plot(x0 + xs, sig, color=S1, lw=2)
    b.axhline(1.0, color=INK2, lw=1, ls=(0, (4, 3)))
    b.text(5.25, 1.03, "σ_f", va="bottom", ha="right", color=INK2)
    b.set_xlabel("position along the film / L_s   (L_s = σ_f t / τ_i)")
    b.set_ylabel("film stress / σ_f")
    b.set_ylim(0, 1.3)
    b.set_xlim(0, 5.3)
    b.set_title("b  Shear-lag theory: stress in three fragments", loc="left")
    note = ("stress rises from each crack at slope τ_i / t; a fragment\n"
            "breaks only if ℓ ≥ 2 L_s, so at saturation L_s ≤ ℓ < 2 L_s")
    b.text(0.05, 1.22, note,
           fontsize=8.5, color=INK2, va="top")
    fig.tight_layout()
    fig.savefig(OUT / "cell.png", dpi=200)
    plt.close(fig)


def fig_r0_curves(runs):
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for (nt, r), col in zip(runs.items(), (S1, S2, S3), strict=True):
        c = r["curve"]
        ax.plot(c[:, 0] / bd.EPS_B, c[:, 1] / r["sigma_f"], color=col, lw=2, label=f"{nt} rows")
        ax.text(1.5 * 1.005, c[-1, 1] / r["sigma_f"], "", color=col)
    ax.axvspan(0, 0, color=GRID)
    ax.set_xlabel("imposed film strain / bond breaking strain ε_b")
    ax.set_ylabel("film stress / peak stress σ_f")
    ax.set_title("R0, free film in tension (seed 0)", loc="left")
    ax.grid(color=GRID, lw=0.6)
    ax.legend(frameon=False, loc="upper left")
    ax.annotate("8 rows: crack arrests,\nstress stays at 0.54 σ_f,\nthen fails at +0.25 ε_b",
                xy=(0.95, 0.56), xytext=(1.08, 0.75), fontsize=8.5, color=INK2,
                arrowprops={"arrowstyle": "-", "color": INK2, "lw": 0.8})
    ax.annotate("4 rows: drops to 0.05 σ_f,\nreloads to 0.59 σ_f, fails at 1.35 ε_b",
                xy=(1.2, 0.47), xytext=(1.08, 0.3), fontsize=8.5, color=INK2,
                arrowprops={"arrowstyle": "-", "color": INK2, "lw": 0.8})
    fig.tight_layout()
    fig.savefig(OUT / "r0_curves.png", dpi=200)
    plt.close(fig)


def anim_r0(run, zoom_cols=18):
    """R0, 8 rows, true scale: full-film strip, zoom on the held grip, stress curve. Red points = broken bonds."""
    film = run["film"]
    frames = run["frames"]
    curve = run["curve"]
    x0 = film.x0
    fig = plt.figure(figsize=(9, 7.2))
    gs = fig.add_gridspec(3, 1, height_ratios=[0.55, 1.6, 1.2], hspace=0.45)
    a_full, a_zoom, ac = fig.add_subplot(gs[0]), fig.add_subplot(gs[1]), fig.add_subplot(gs[2])
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("b", BLUES)
    lcs, dots = [], []
    for ax in (a_full, a_zoom):
        lc = LineCollection(bond_segments(film, x0), linewidths=0.6 if ax is a_full else 1.6)
        ax.add_collection(lc)
        d, = ax.plot([], [], "o", color=CRIT, ms=2.5 if ax is a_full else 6, mec=SURFACE, mew=0.6)
        lcs.append(lc)
        dots.append(d)
        ax.set_aspect("equal")
        ax.axis("off")
    xmin, xmax = x0[:, 0].min(), x0[:, 0].max()
    a_full.set_xlim(xmin - 2, xmax + 4)
    a_full.set_ylim(-1, x0[:, 1].max() + 1)
    a_full.set_title("whole film (64 columns × 8 rows), true scale", loc="left", fontsize=9, color=INK2)
    a_full.axvspan(xmin - 0.5, xmin + zoom_cols, color=GRID, zorder=0)
    a_zoom.set_xlim(xmin - 1.5, xmin + zoom_cols)
    a_zoom.set_ylim(-0.8, x0[:, 1].max() + 0.8)
    a_zoom.axvline(xmin - 0.6, color=INK2, lw=4)
    a_zoom.text(xmin - 1.3, -0.7, "held grip", color=INK2, fontsize=8, rotation=90, va="bottom")
    a_zoom.set_title("zoom: the held end (grey band above). Bond colour = strain / threshold, light → dark;"
                     " red points = broken bonds", loc="left", fontsize=9, color=INK2)
    ac.plot(curve[:, 0] / bd.EPS_B, curve[:, 1] / run["sigma_f"], color=S1, lw=2)
    pt, = ac.plot([], [], "o", color=S1, ms=8, mec=SURFACE, mew=2)
    ac.set_xlabel("imposed strain / ε_b")
    ac.set_ylabel("stress / σ_f")
    ac.grid(color=GRID, lw=0.6)
    sup = fig.suptitle("", x=0.02, ha="left", fontsize=11)

    def draw(k):
        _, x, alive = frames[k]
        seg = bond_segments(film, x)
        strain = np.linalg.norm(x[film.bj] - x[film.bi], axis=1) / film.r0 - 1.0
        col = cmap(np.clip(strain / film.eps_b, 0, 1))
        mid = 0.5 * (x[film.bi] + x[film.bj])
        for lc, d in zip(lcs, dots, strict=True):
            lc.set_segments(seg[alive])
            lc.set_color(col[alive])
            d.set_data(mid[~alive, 0], mid[~alive, 1])
        pt.set_data([curve[k, 0] / bd.EPS_B], [curve[k, 1] / run["sigma_f"]])
        sup.set_text(f"R0: free 8-row film pulled at the right end (seed 0), load step {k + 1} of {len(frames)}, "
                     f"broken bonds: {int((~alive).sum())}")
        return (*lcs, *dots, pt, sup)

    idx = list(range(len(frames))) + [len(frames) - 1] * 8
    anim = FuncAnimation(fig, lambda i: draw(idx[i]), frames=len(idx), blit=False)
    anim.save(OUT / "r0_nt8.gif", writer=PillowWriter(fps=5), dpi=100)
    for k, name in ((33, "r0_nt8_step34.png"), (len(frames) - 1, "r0_nt8_final.png")):
        draw(k)
        fig.savefig(OUT / name, dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fig_cell()
    runs = {nt: bd.run_r0(nt, 0, record=(nt == 8)) for nt in (4, 8, 16)}
    fig_r0_curves(runs)
    anim_r0(runs[8])


if __name__ == "__main__":
    main()
