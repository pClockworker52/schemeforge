"""H-0019 evidence table (docs/plans/2026-10-24-round4.md): every Arena 1 candidate or zoo member whose latest ok
promo run under the current judge has NF1 converged_impl mean = 1.00, with RF1 shock_width median and NF3
roughness_J p90 from that run. Marks rows that meet the kill criterion and prints Spearman rho over all rows.

    uv run python scripts/h0019_table.py [judge_version]
"""

from __future__ import annotations

import sqlite3
import sys

SHOCK_MAX, ROUGH_MAX = 2.6, 0.002


def _ranks(xs: list[float]) -> list[float]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1  # average rank for ties
        i = j + 1
    return ranks


def spearman(xs: list[float], ys: list[float]) -> float:
    rx, ry = _ranks(xs), _ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry, strict=True))
    vx = sum((a - mx) ** 2 for a in rx) ** 0.5
    vy = sum((b - my) ** 2 for b in ry) ** 0.5
    return cov / (vx * vy)


def main() -> int:
    judge = sys.argv[1] if len(sys.argv) > 1 else "euler1d-v1.5"
    conn = sqlite3.connect("file:runs/registry.sqlite?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    runs = conn.execute(
        "SELECT r.id, r.candidate_id, r.slot, c.path FROM runs r JOIN candidates c ON c.id = r.candidate_id "
        "WHERE r.arena = 'euler1d' AND r.suite = 'promo' AND r.status = 'ok' AND r.judge_version = ? "
        "AND r.started_at = (SELECT max(r2.started_at) FROM runs r2 WHERE r2.candidate_id = r.candidate_id "
        "AND r2.suite = 'promo' AND r2.status = 'ok' AND r2.judge_version = ?)", (judge, judge)).fetchall()
    rows = []
    for r in runs:
        vals = {(s["family"], s["metric"]): s["value"] for s in conn.execute(
            "SELECT family, metric, value FROM scores WHERE run_id = ? AND case_id IS NULL", (r["id"],))}
        conv = vals.get(("NF1", "converged_impl:mean"))
        shock = vals.get(("RF1", "shock_width:median"))
        rough = vals.get(("NF3", "roughness_J:p90"))
        if conv is None or conv < 1.0 or shock is None or rough is None:
            continue
        zoo = "/zoo/" in (r["path"] or "")
        name = r["path"].rsplit("/", 1)[-1].removesuffix(".py") if zoo else ""
        rows.append((r["candidate_id"], r["slot"], name, shock, rough, r["id"]))
    rows.sort(key=lambda x: x[3])
    print(f"judge {judge}: rows with an ok promo run and NF1 converged_impl mean = 1.00")
    print(f"{'candidate':50} {'slot':24} {'zoo':22} {'RF1 shock med':>13} {'NF3 rough p90':>13}  run           kill")
    for cid, slot, name, shock, rough, rid in rows:
        kill = "KILL" if shock <= SHOCK_MAX and rough <= ROUGH_MAX else ""
        print(f"{cid:50} {slot:24} {name:22} {shock:13.3f} {rough:13.3g}  {rid}  {kill}")
    if len(rows) >= 3:
        rho = spearman([x[3] for x in rows], [x[4] for x in rows])
        print(f"Spearman rho(RF1 shock median, NF3 roughness p90) = {rho:.3f}, n = {len(rows)}")
    print(f"kill rows: {sum(1 for x in rows if x[3] <= SHOCK_MAX and x[4] <= ROUGH_MAX)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
