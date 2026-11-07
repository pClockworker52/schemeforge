"""Figures for the geometric (rigid-sphere) impact view: docs/research/coldspray-kinematics.md.

Usage: python scripts/plot_kinematics.py -> docs/research/figures/kinematics/{edge_speed.png, contact_al900.gif}
Geometry only: a rigid sphere entering a rigid flat. Not a v_cr prediction.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

from schemeforge.research import impact_kinematics as k  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "docs" / "research" / "figures" / "kinematics"
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
S1, S2 = "#2a78d6", "#eb6834"  # categorical slots 1-2 (reference palette)
BLUES = ["#86b6ef", "#3987e5", "#256abf", "#104281"]  # sequential steps 250 / 400 / 500 / 650
R = 7.5e-6  # d = 15 um; every time scales with R / V, every length with R
VS = (500.0, 700.0, 900.0, 1100.0)

plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
                     "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def fig_static():
    mats = {m: k.bulk_sound_speed(m)[0] for m in ("Al", "Cu")}
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4), gridspec_kw={"width_ratios": [1, 1, 0.9]})
    t_ps = np.linspace(1e-3, 400, 4000)
    for ax, (m, c) in zip(axes[:2], mats.items(), strict=True):
        for v, col in zip(VS, BLUES, strict=True):
            d = np.minimum(v * t_ps * 1e-12, R)
            ax.plot(t_ps, k.edge_speed(v, d, R) / c, color=col, lw=2, label=f"{v:.0f} m/s")
            s = k.critical_state(v, c, R)
            ax.plot([s["t_c"] * 1e12], [1.0], "o", color=col, ms=8, mec=SURFACE, mew=2, zorder=5)
        ax.axhline(1.0, color=INK2, lw=1, ls=(0, (4, 3)), label="edge speed = c_b")
        ax.text(395, 5.0, "above 1: supersonic edge,\nshock attached, no jet", ha="right", va="center",
                fontsize=8.5, color=INK2)
        ax.text(8, 0.34, "below 1: subsonic edge, jetting geometrically possible", ha="left", va="bottom",
                fontsize=8.5, color=INK2)
        ax.set_yscale("log")
        ax.set_ylim(0.3, 30)
        ax.set_xlim(0, 400)
        ax.set_xlabel("time after first touch (ps)")
        ax.set_ylabel("contact-edge speed / bulk sound speed")
        ax.set_title(f"{'a' if m == 'Al' else 'b'}  {m}, d = 15 µm (c_b = {c:.0f} m/s)", loc="left")
        ax.grid(color=GRID, lw=0.6, which="both")
        ax.legend(frameon=False, loc="upper center", ncol=2, fontsize=8.5, title="impact speed (dots: switch)",
                  title_fontsize=8.5)
    ax = axes[2]
    vv = np.linspace(300, 1300, 200)
    for (m, c), col in zip(mats.items(), (S1, S2), strict=True):
        ac = [k.critical_state(v, c, R)["a_c"] / R for v in vv]
        ax.plot(vv, ac, color=col, lw=2)
        ax.text(vv[-1] + 15, ac[-1], m, color=INK, va="center")
    ax.set_xlabel("impact speed (m/s)")
    ax.set_ylabel("contact radius at the subsonic switch, a_c / R")
    ax.set_title("c  Where the switch happens", loc="left")
    ax.set_xlim(300, 1400)
    ax.grid(color=GRID, lw=0.6)
    fig.suptitle("Rigid sphere entering a rigid flat: geometry only, no material response, not a v_cr prediction",
                 x=0.01, ha="left", fontsize=10, color=INK2)
    fig.tight_layout()
    fig.savefig(OUT / "edge_speed.png", dpi=200)
    plt.close(fig)


def anim_al900(v=900.0, n=70):
    c, _ = k.bulk_sound_speed("Al")
    s = k.critical_state(v, c, R)
    dmax = 0.06 * R
    deltas = dmax * (np.arange(1, n + 1) / n) ** 2
    fig = plt.figure(figsize=(9, 6.2))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.25, 1], hspace=0.35)
    ax, ac = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    xr = 0.45
    ax.set_xlim(-xr, xr)
    ax.set_ylim(-0.08, 0.15)
    ax.set_aspect("equal")
    ax.fill_between([-xr, xr], -0.08, 0, color=GRID, zorder=0)
    ax.axhline(0, color=INK2, lw=1)
    ax.set_xlabel("x / R")
    ax.set_ylabel("z / R")
    ax.text(-xr + 0.01, -0.07, "substrate (rigid, flat)", fontsize=8.5, color=INK2)
    th = np.linspace(-math.pi / 2 - 0.5, -math.pi / 2 + 0.5, 400)
    arc, = ax.plot([], [], color=INK, lw=1.5)
    cap = ax.fill_between([0, 0], 0, 0, color=S2, alpha=0.15)
    edges, = ax.plot([], [], "o", ms=9, mec=SURFACE, mew=2)
    note = ax.text(0, 0.135, "", ha="center", fontsize=9)
    ax.text(xr - 0.01, -0.035, "shaded: geometric overlap of rigid bodies\n(a real particle deforms instead)",
            ha="right", fontsize=8, color=INK2)
    t_ps = deltas / v * 1e12
    u = k.edge_speed(v, deltas, R) / c
    ac.plot(t_ps, u, color=S1, lw=2)
    ac.axhline(1.0, color=INK2, lw=1, ls=(0, (4, 3)))
    ac.axvline(s["t_c"] * 1e12, color=INK2, lw=0.8, ls=":")
    ac.text(s["t_c"] * 1e12 + 5, 6, f"switch at {s['t_c'] * 1e12:.0f} ps,\nβ = {math.degrees(s['beta_c']):.1f}°, "
            f"a = {s['a_c'] / R:.2f} R", fontsize=8.5, color=INK2)
    ac.set_yscale("log")
    ac.set_ylim(0.3, 30)
    ac.set_xlabel("time after first touch (ps)")
    ac.set_ylabel("edge speed / c_b")
    ac.grid(color=GRID, lw=0.6, which="both")
    pt, = ac.plot([], [], "o", color=S1, ms=8, mec=SURFACE, mew=2)
    sup = fig.suptitle("", x=0.02, ha="left", fontsize=10.5)

    def draw(i):
        nonlocal cap
        d = deltas[i] / R
        zc = 1.0 - d
        arc.set_data(np.cos(th), zc + np.sin(th))
        cap.remove()
        xs = np.linspace(-math.sqrt(max(2 * d - d * d, 0)), math.sqrt(max(2 * d - d * d, 0)), 100)
        cap = ax.fill_between(xs, zc - np.sqrt(np.maximum(1 - xs ** 2, 0)), 0, color=S2, alpha=0.15, lw=0)
        a = k.contact_radius(deltas[i], R) / R
        sub = u[i] < 1.0
        edges.set_data([-a, a], [0, 0])
        edges.set_color(S1 if sub else S2)
        note.set_text("edge subsonic: jetting geometrically possible" if sub
                      else "edge supersonic: shock attached to the edge")
        note.set_color(S1 if sub else S2)
        pt.set_data([t_ps[i]], [u[i]])
        sup.set_text(f"Al, d = 15 µm, 900 m/s, rigid sphere into rigid flat (geometry only).  "
                     f"t = {t_ps[i]:.0f} ps, depth = {d:.4f} R")
        return arc, edges, note, pt, sup

    idx = list(range(n)) + [n - 1] * 10
    anim = FuncAnimation(fig, lambda j: draw(idx[j]), frames=len(idx), blit=False)
    anim.save(OUT / "contact_al900.gif", writer=PillowWriter(fps=8), dpi=100)
    i_c = int(np.searchsorted(deltas, s["delta_c"]))
    draw(min(i_c, n - 1))
    fig.savefig(OUT / "contact_al900_switch.png", dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fig_static()
    anim_al900()


if __name__ == "__main__":
    main()
