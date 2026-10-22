"""Readmit evolve children that were rejected by an evaluation timeout and are ok when re-evaluated alone.

A resumed run keeps such false rejections out of its archive and islands (docs/STATUS.md). After the children
have been re-evaluated on dev by id (`sforge eval <id> ... --suite dev`), this script probes each one in the
sandbox (a smoke run with probes), offers it to the run's MAP-Elites archive and places it on its hunch's island,
exactly as `run_generation` does. One at a time; run it with nothing else evaluating.

    python scripts/readmit_timeouts.py <evolve run id>

Writes runs/evolve/<run>/readmitted.jsonl and updates state.json (children.jsonl stays the original history).
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from schemeforge.core import evaluation, leaderboard, registry
from schemeforge.core.integrity import REPO_ROOT
from schemeforge.engine.archive import Archive
from schemeforge.engine.evolve import ISLAND_CAP, State


def main(run_id: str) -> int:
    state = State.load(run_id)
    cfg = state.config
    conn = registry.connect()
    rows = {r.candidate_id: r for r in leaderboard.build(conn, cfg.arena, cfg.slot, suite=cfg.suite)}
    children = [json.loads(line) for line in (state.dir / "children.jsonl").open(encoding="utf-8")]
    timed_out = [c for c in children if c.get("status") == "rejected" and "timeout" in str(c.get("violations"))]
    archive = Archive.from_dict(state.archive)
    out = []
    for c in timed_out:
        cid = c["id"]
        if cid not in rows:
            out.append({"id": cid, "hunch": c["hunch"], "archive": "still not ok on dev"})
            continue
        path = conn.execute("SELECT path FROM candidates WHERE id = ?", (cid,)).fetchone()["path"]
        p = Path(path) if Path(path).is_absolute() else REPO_ROOT / path
        smoke = evaluation.evaluate_file(p, cfg.arena, cfg.slot, "smoke", probe=True)
        probe = smoke.report.get("probe") or {}
        if smoke.report["status"] != "ok" or "error" in probe:
            out.append({"id": cid, "hunch": c["hunch"], "archive": f"probe failed ({smoke.run_id})"})
            continue
        outcome = archive.offer(cid, probe, rows[cid].score, lambda x: rows[x].score if x in rows else math.inf)
        if not outcome.startswith("duplicate"):
            island = state.islands[c["hunch"]]
            island.append(cid)
            island.sort(key=lambda x: (rows[x].rank, rows[x].score) if x in rows else (math.inf, math.inf))
            del island[ISLAND_CAP:]
        out.append({"id": cid, "hunch": c["hunch"], "generation": c["generation"], "archive": outcome,
                    "probe_run": smoke.run_id})
        print(cid, c["hunch"], outcome, flush=True)
    conn.close()
    state.archive = archive.to_dict()
    state.front = sorted(x for x, r in rows.items() if r.rank == 0)
    state.save()
    with (state.dir / "readmitted.jsonl").open("a", encoding="utf-8") as fh:
        for r in out:
            fh.write(json.dumps(r) + "\n")
    placed = sum(not r["archive"].startswith(("duplicate", "still", "probe")) for r in out)
    print(f"{len(timed_out)} timed out, {sum(r['id'] in rows for r in timed_out)} ok on dev now, {placed} placed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
