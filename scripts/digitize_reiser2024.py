"""Digitize Reiser & Schuh 2024 (arXiv:2404.05601v1) Figs. 3b and 5b into a per-shot CSV.

Input: the two embedded raster figures, extracted from the arXiv PDF with
``pdfimages -png -f 5 -l 7 reiser2024.pdf nat`` (nat-001.png = Fig. 3, 1202 x 809 px;
nat-003.png = Fig. 5, 1376 x 720 px; both 220 ppi). The PDF is not committed.

Method (per panel):
- velocity axis: the top tick comb (50 m/s per tick, first tick = 0) fitted linearly;
  size axis: the bottom (pink) major ticks (10 um per tick, first = 0);
- one row per shot, found as a non-white run in the column 12 px right of the frame,
  ordered bottom (shot 1) to top;
- velocity v [m/s]: the midpoint of the +-5 % error-bar caps when a cap pair straddling
  the bar end is found and its width is 8.5-11.5 % of v ("cap midpoint"); otherwise the
  end of the grey bar ("bar end");
- size d [um]: end of the pink bar.

Fracture events (Fig. 5b arrows) are listed in FRACTURE_EVENTS: six were detected as
dark connected components (width ~25 px) on a shot row; the seventh (F1 shot 7) was
confirmed by eye on a 4x zoom. Validation: see docs/research/coldspray-buildup-track.md.

Usage: python scripts/digitize_reiser2024.py nat-001.png nat-003.png out.csv
"""

from __future__ import annotations

import csv
import sys

import numpy as np
from PIL import Image

# (stack id prefix, figure, outcome, panels as (x_left_frame, x_right_frame, top_frame_row, size_axis_row))
FIG3 = ("I", "3b", "intact", [(71, 302, 428, 746), (370, 601, 428, 746), (668, 899, 428, 746),
                              (966, 1197, 428, 746)])
FIG5 = ("F", "5b", "fractured", [(64, 270, 380, 665), (330, 536, 380, 665), (596, 802, 380, 665),
                                 (863, 1069, 380, 665), (1129, 1335, 383, 667)])
FRACTURE_EVENTS = {("F1", 5), ("F1", 7), ("F2", 8), ("F2", 13), ("F3", 9), ("F4", 11), ("F5", 14)}


def _clusters(xs: list[int], gap: int = 2) -> list[float]:
    out: list[float] = []
    cur = [xs[0]]
    for x in xs[1:]:
        if x - cur[-1] <= gap:
            cur.append(x)
        else:
            out.append(float(np.mean(cur)))
            cur = [x]
    out.append(float(np.mean(cur)))
    return out


def _calibrate(a: np.ndarray, x0: int, x1: int, top: int, bot: int):
    """Return (px per m/s, px at v=0), (px per um, px at d=0) from the axis ticks."""
    dark = a.sum(2) < 250
    pink = (a[:, :, 0] > 190) & (a[:, :, 0] - a[:, :, 1] > 50)
    t = _clusters([x for x in range(x0 + 3, x1 - 2) if dark[top + 3, x] and dark[top + 4, x]])
    step = float(np.median(np.diff(t)))
    comb = [t[0]]
    for x in t[1:]:
        if abs((x - comb[-1]) - step) < 2.5:
            comb.append(x)
    pv = np.polyfit(np.arange(len(comb)) * 50.0, comb, 1)
    b = _clusters([x for x in range(x0 + 3, x1 - 2) if pink[bot - 4, x] and pink[bot - 5, x]])
    ps = np.polyfit(np.arange(len(b)) * 10.0, b, 1)
    return pv, ps


def digitize(path: str, prefix: str, panels) -> list[dict]:
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    s = a.sum(2)
    rows: list[dict] = []
    for k, (x0, x1, top, bot) in enumerate(panels):
        pv, ps = _calibrate(a, x0, x1, top, bot)
        xs = x0 + 12
        col = s[top + 3:bot - 3, xs] < 700
        runs = []
        y = 0
        while y < len(col):
            if col[y]:
                y1 = y
                while y1 < len(col) and col[y1]:
                    y1 += 1
                if y1 - y >= 6:
                    runs.append((top + 3 + y, top + 3 + y1 - 1))
                y = y1
            else:
                y += 1
        for i, (ya, yb) in enumerate(runs[::-1]):
            ends = []
            for yy in (ya + 1, yb - 1):
                x = xs
                while x < x1 - 1 and s[yy, x] <= 450:
                    x += 1
                ends.append(x - 0.5)
            xend = float(np.mean(ends))
            v_bar = (xend - pv[1]) / pv[0]
            blk = a[ya - 2:yb + 3, :, :].max(2) < 90
            caps = [x for x in range(xs, x1 - 1) if blk[:, x].sum() >= max(5, (yb - ya) - 1)]
            capc = _clusters(caps) if caps else []
            left = [c for c in capc if c < xend]
            right = [c for c in capc if c > xend]
            v, method, cross = v_bar, "bar end", ""
            if left and right:
                v_cap = ((left[-1] + right[0]) / 2 - pv[1]) / pv[0]
                width = (right[0] - left[-1]) / pv[0]
                if 0.085 < width / v_cap < 0.115:
                    v, method, cross = v_cap, "cap midpoint", str(round(v_bar))
            pr = [(a[yy, :, 0] > 170) & (a[yy, :, 0] - a[yy, :, 1] > 45) for yy in range(ya, yb + 1)]
            prow = max(pr, key=lambda r: r[x0:x1].sum())
            px = [x for x in range(xs - 8, x1) if prow[x]]
            d = ((max(px) + 0.5) - ps[1]) / ps[0]
            sid = f"{prefix}{k + 1}"
            rows.append(dict(stack=sid, panel=k + 1, shot=i + 1, v_mps=round(v), v_method=method,
                             v_bar_end_mps=cross, d_um=round(d, 1),
                             fracture_event=int((sid, i + 1) in FRACTURE_EVENTS)))
    return rows


def main(fig3: str, fig5: str, out: str) -> None:
    rows = []
    for path, (prefix, fig, outcome, panels) in ((fig3, FIG3), (fig5, FIG5)):
        for r in digitize(path, prefix, panels):
            rows.append(dict(stack=r["stack"], figure=f"Reiser2024 Fig. {fig}", stack_outcome=outcome, **{
                k: r[k] for k in ("shot", "v_mps", "v_method", "v_bar_end_mps", "d_um", "fracture_event")}))
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main(*sys.argv[1:4])
