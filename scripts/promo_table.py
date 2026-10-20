"""Print the latest promo aggregates of every zoo member from the registry (family aggregates only).

    uv run python scripts/promo_table.py [metric ...]
"""

from __future__ import annotations

import sqlite3
import sys

DEFAULT = ["RF1.l1_smooth", "RF1.shock_width", "RF1.overshoot", "RF2.tv_increase", "NF1.shock_pos_err",
           "NF1.overshoot", "NF1.res_orders_expl", "NF1.newton_iters", "NF1.converged_impl", "NF1.limit_cycle",
           "NF2.l1_smooth", "NF2.mdot_var", "NF3.roughness_J", "NF3.converged_impl"]


def main() -> int:
    metrics = sys.argv[1:] or DEFAULT
    conn = sqlite3.connect("runs/registry.sqlite")
    conn.row_factory = sqlite3.Row
    cands = conn.execute("SELECT id, slot, path FROM candidates WHERE path LIKE 'src/schemeforge/arenas/%/zoo/%' "
                         "ORDER BY slot, path").fetchall()
    for m in metrics:
        fam, name = m.split(".")
        print(f"\n{m}  (median / p90 / worst)")
        for c in cands:
            run = conn.execute("SELECT id FROM runs WHERE candidate_id = ? AND suite = 'promo' AND status != 'running' "
                               "ORDER BY started_at DESC LIMIT 1", (c["id"],)).fetchone()
            if run is None:
                continue
            vals = {r["metric"]: r["value"] for r in conn.execute(
                "SELECT metric, value FROM scores WHERE run_id = ? AND family = ?", (run["id"], fam))}
            cells = [vals.get(f"{name}:{s}") for s in ("median", "p90", "worst")]
            label = c["path"].rsplit("/", 1)[-1][:-3]
            print(f"  {c['slot']:14s} {label:16s} " + "  ".join("     -    " if v is None else f"{v:10.4g}"
                                                                for v in cells))
    return 0


if __name__ == "__main__":
    sys.exit(main())
