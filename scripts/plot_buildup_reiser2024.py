"""Small multiples of the digitized Reiser2024 stacks: impact velocity per shot, fracture events marked.

Writes docs/research/figures/buildup/reiser2024_stacks.png. Palette slots 1-2 of the dataviz
reference palette (validated light mode): grey for ordinary shots, orange triangles for shots
that fractured the stack.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CSV = Path("docs/research/data/buildup_reiser2024.csv")
OUT = Path("docs/research/figures/buildup/reiser2024_stacks.png")
VCR = 253.0
INK, MUTED, GRID, SURF = "#1f1f1e", "#6b6b68", "#e4e4e1", "#fcfcfb"
SHOT, EVENT = "#8a8a86", "#eb6834"


def main() -> None:
    stacks: dict[str, list[dict]] = {}
    for r in csv.DictReader(CSV.open()):
        stacks.setdefault(r["stack"], []).append(r)
    order = ["I1", "I2", "I3", "I4", "F1", "F2", "F3", "F4", "F5"]
    fig, axes = plt.subplots(2, 5, figsize=(13, 5.6), sharey=True, facecolor=SURF)
    axes = axes.ravel()
    slots = [0, 1, 2, 3, 5, 6, 7, 8, 9]
    axes[4].axis("off")
    for sid, slot in zip(order, slots, strict=True):
        ax = axes[slot]
        ax.set_facecolor(SURF)
        rows = sorted(stacks[sid], key=lambda r: int(r["shot"]))
        x = [int(r["shot"]) for r in rows]
        v = [float(r["v_mps"]) for r in rows]
        ev = [(int(r["shot"]), float(r["v_mps"])) for r in rows if r["fracture_event"] == "1"]
        ax.axhline(VCR, color=MUTED, lw=1, ls=(0, (4, 3)), zorder=1)
        ax.axhline(1.3 * VCR, color=MUTED, lw=1, ls=(0, (1, 2)), zorder=1)
        ax.vlines(x, [v_ * 0.95 for v_ in v], [v_ * 1.05 for v_ in v], color=GRID, lw=2, zorder=2)
        ax.plot(x, v, "o", ms=4.5, color=SHOT, mec=SURF, mew=1, zorder=3)
        if ev:
            ax.plot(*zip(*ev, strict=True), "v", ms=9, color=EVENT, mec=SURF, mew=1.2, zorder=4)
        mean = sum(v) / len(v)
        outcome = "intact" if sid.startswith("I") else "fractured"
        ax.set_title(f"{sid} · {outcome} · {len(v)} shots · mean {mean:.0f}", fontsize=9, color=INK, loc="left")
        ax.set_xlim(0, 25)
        ax.set_ylim(150, 460)
        ax.grid(axis="y", color=GRID, lw=0.6)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=8)
        if slot in (0, 5):
            ax.set_ylabel("impact velocity [m/s]", fontsize=9, color=INK)
        if slot >= 5:
            ax.set_xlabel("shot number", fontsize=9, color=INK)
    leg = axes[4]
    leg.plot([], [], "o", color=SHOT, label="shot (bar: ±5 % velocity error)")
    leg.plot([], [], "v", ms=9, color=EVENT, label="shot that fractured the stack")
    leg.plot([], [], color=MUTED, ls=(0, (4, 3)), label="v_cr = 253 m/s (single Au particle)")
    leg.plot([], [], color=MUTED, ls=(0, (1, 2)), label="1.3 v_cr")
    leg.legend(loc="center left", frameon=False, fontsize=8.5, labelcolor=INK)
    fig.suptitle("Reiser2024 Au stacks, digitized from Figs. 3b and 5b (top row intact, bottom row fractured)",
                 fontsize=10.5, color=INK, x=0.01, ha="left")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, facecolor=SURF)


if __name__ == "__main__":
    main()
