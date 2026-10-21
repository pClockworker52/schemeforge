"""Summarize an isolated engine run (scripts/e2e_evolve.py workdir) for the Gate 2 calibration checks.

    uv run python scripts/calibration_report.py WORKDIR [RUN_ID]
"""

from __future__ import annotations

import collections
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


def main() -> int:
    work = Path(sys.argv[1])
    runs = sorted((work / "runs" / "evolve").iterdir())
    run_dir = work / "runs" / "evolve" / sys.argv[2] if len(sys.argv) > 2 else runs[-1]
    state = json.loads((run_dir / "state.json").read_text())
    children = [json.loads(x) for x in (run_dir / "children.jsonl").read_text().splitlines()]
    status = collections.Counter(c.get("status") for c in children)
    stages = collections.Counter(f"{c.get('status')}@{c.get('stage', '-')}" for c in children)
    ops = collections.Counter(c.get("operator") for c in children)
    arch = state["archive"]
    dups = collections.Counter(v for v in arch.get("duplicates", {}).values())
    zoo_dups = {k: v for k, v in dups.items() if k.startswith("zoo:")}
    print(f"run {state['run_id']}: generations {state['generation']}, children {state['children_made']} "
          f"(log has {len(children)})")
    print(f"status: {dict(status)}")
    print(f"status@stage: {dict(stages)}")
    print(f"operators: {dict(ops)}")
    print(f"archive cells occupied: {len(arch['elites'])}  cells: {sorted(arch['elites'])}")
    print(f"duplicates: {sum(dups.values())} total; of zoo members: {zoo_dups} "
          f"({len(zoo_dups)} distinct zoo members rediscovered)")
    print(f"Pareto front size: {len(state['front'])}")
    for h in state["history"]:
        print(f"  gen {h['generation']}: ok {h['ok']}, rejected {h['rejected']}, llm errors {h['llm_errors']}, "
              f"dup {h['duplicates']}, placed {h['placed']}, new front {len(h['new_front'])}, "
              f"cost ${h['cost_usd']:.3f}, finished {h['finished']}")
    conn = sqlite3.connect(work / "runs" / "registry.sqlite")
    calls = conn.execute("SELECT COUNT(*), SUM(cost_usd), AVG(latency_s), SUM(input_tokens), SUM(output_tokens), "
                         "MIN(created_at), MAX(created_at) FROM llm_calls").fetchone()
    n, cost, lat, tin, tout, t0, t1 = calls
    if n:
        hours = (datetime.fromisoformat(t1) - datetime.fromisoformat(t0)).total_seconds() / 3600 or float("nan")
        print(f"LLM calls {n}: list-price cost ${cost or 0:.2f} (${100 * (cost or 0) / n:.2f} per 100), "
              f"mean latency {lat:.1f} s, tokens in/out {tin}/{tout} "
              f"({(tin or 0) / n:.0f}/{(tout or 0) / n:.0f} per call), span {hours:.2f} h "
              f"({n / hours:.0f} candidates/h)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
