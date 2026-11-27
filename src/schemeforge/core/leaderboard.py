"""Leaderboard rows from the registry: the latest ok dev run per candidate under the current judge version."""

from __future__ import annotations

import math
import sqlite3
from dataclasses import dataclass, field

from .integrity import judge_version
from .pareto import pareto_ranks


@dataclass
class Row:
    candidate_id: str
    origin: str
    hunch_id: str | None
    path: str
    run_id: str
    values: dict[str, float]  # "CASE.metric" -> value
    rank: int = -1
    vs_zoo: dict[str, float] = field(default_factory=dict)  # lower is better; 1.0 = best zoo member
    score: float = math.inf  # geometric mean of vs_zoo ratios (sorts within a Pareto rank)
    fails: int = 0  # failed checks of the slot's target screen (engine/objectives.py SCREENS); sorts first
    duplicate_of: str | None = None  # an earlier row with the same objective values to 3 digits

    @property
    def key(self) -> tuple[int, int, float]:
        """Selection order: fewest failed screen checks, then Pareto rank, then score (lower is better)."""
        return self.fails, self.rank, self.score

    @property
    def is_zoo(self) -> bool:
        return self.origin == "zoo" or "/zoo/" in self.path


def objectives(arena: str, slot: str) -> list[tuple[str, str, str]]:
    from schemeforge.engine.objectives import OBJECTIVES

    return OBJECTIVES[arena][slot]


def build(conn: sqlite3.Connection, arena: str, slot: str, version: str | None = None,
          suite: str = "dev") -> list[Row]:
    version = version or judge_version(arena)
    objs = objectives(arena, slot)
    rows: list[Row] = []
    cands = conn.execute("SELECT id, origin, hunch_id, path FROM candidates WHERE arena = ? AND slot = ?",
                         (arena, slot)).fetchall()
    for c in cands:
        run = conn.execute(
            "SELECT id FROM runs WHERE candidate_id = ? AND suite = ? AND status = 'ok' AND judge_version = ? "
            "ORDER BY started_at DESC LIMIT 1", (c[0], suite, version)).fetchone()
        if run is None:
            continue
        vals = {f"{r[0]}.{r[1]}": r[2] for r in conn.execute(
            "SELECT case_id, metric, value FROM scores WHERE run_id = ?", (run[0],))}
        rows.append(Row(c[0], c[1], c[2], c[3], run[0], vals))
    if not rows:
        return rows

    keys = [f"{case}.{m}" for case, m, _ in objs]
    dirs = [d for _, _, d in objs]

    def oriented(r: Row, k: str, d: str) -> float:
        """The objective value in its own direction: |v| for "absmin" (signed errors such as a_err), else v."""
        v = r.values.get(k, math.nan)
        return abs(v) if d == "absmin" else v

    vectors = [[(-1.0 if d == "max" else 1.0) * oriented(r, k, d) for k, d in zip(keys, dirs, strict=True)]
               for r in rows]
    for r, rank in zip(rows, pareto_ranks(vectors), strict=True):
        r.rank = rank

    zoo = [r for r in rows if r.is_zoo]
    for k, d in zip(keys, dirs, strict=True):
        zv = [oriented(r, k, d) for r in zoo if k in r.values]
        zv = [v for v in zv if math.isfinite(v) and v > 0]
        if not zv:
            continue
        best = max(zv) if d == "max" else min(zv)
        for r in rows:
            v = oriented(r, k, d)
            if math.isfinite(v) and v > 0:
                r.vs_zoo[k] = best / v if d == "max" else v / best
    for r in rows:
        ratios = [v for v in r.vs_zoo.values() if v > 0]
        r.score = math.exp(sum(math.log(v) for v in ratios) / len(ratios)) if ratios else math.inf
    from schemeforge.engine.objectives import screen_fails

    for r in rows:
        r.fails = screen_fails(arena, slot, r.values)
    rows.sort(key=lambda r: r.key)
    seen: dict[tuple, str] = {}
    for r in rows:  # behaviourally identical candidates (round 3: one scheme in four spellings) are marked
        sig = tuple(f"{r.values.get(k, math.nan):.3g}" for k in keys)
        r.duplicate_of = seen.get(sig)
        seen.setdefault(sig, r.candidate_id)
    return rows
