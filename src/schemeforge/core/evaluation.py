"""Parent side of `sforge eval` (PLAN §5.5-5.7): run a job in the sandboxed worker and record it in the registry."""

from __future__ import annotations

import json
import secrets
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import registry
from .integrity import REPO_ROOT, judge_version, tree_hash
from .loader import code_hash
from .locks import acquire_core
from .worker import MARKER

TIMEOUTS = {"smoke": 120, "dev": 600, "promo": 3600}  # wall-clock seconds, JIT included
MEMORY_BYTES = 0  # RLIMIT_AS; 0 = off (JAX reserves large virtual address ranges, see DECISIONS.md)
REPORTS_DIR = Path("runs") / "reports"
HELDOUT_DIR = Path.home() / ".schemeforge" / "heldout_runs"  # per-instance promo details; denied to Claude Code


def store_heldout(run_id: str, instances: dict, heldout_dir: Path = HELDOUT_DIR) -> Path:
    """Write per-instance promo details outside the repo (owner-readable only)."""
    heldout_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = heldout_dir / f"{run_id}.json"
    path.write_text(json.dumps(instances, indent=1, default=float), encoding="utf-8")
    path.chmod(0o600)
    return path


@dataclass(frozen=True)
class EvalResult:
    run_id: str
    candidate_id: str
    report: dict[str, Any]


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def run_worker(job: dict[str, Any], timeout: float) -> dict[str, Any]:
    """Run one job in a fresh worker process on a locked core. Timeouts and crashes become rejections."""
    with acquire_core() as core:
        payload = json.dumps({**job, "core": core, "cpu_seconds": int(timeout), "memory_bytes": MEMORY_BYTES})
        try:
            proc = subprocess.run([sys.executable, "-m", "schemeforge.core.worker"], input=payload, text=True,
                                  capture_output=True, timeout=timeout, cwd=REPO_ROOT, check=False)
        except subprocess.TimeoutExpired:
            return {"status": "rejected", "violations": [f"timeout after {timeout:.0f} s"], "cases": {},
                    "metamorphic": {}}
    for line in reversed(proc.stdout.splitlines()):
        if line.startswith(MARKER):
            return json.loads(line[len(MARKER):])
    tail = " | ".join(proc.stderr.strip().splitlines()[-3:])
    reason = "CPU time limit exceeded" if proc.returncode in (-24, 152) else f"worker exited with {proc.returncode}"
    return {"status": "rejected", "violations": [f"{reason}: {tail}"], "cases": {}, "metamorphic": {}}


def _candidate_id(conn: sqlite3.Connection, arena: str, slot: str, chash: str) -> str | None:
    row = conn.execute("SELECT id FROM candidates WHERE arena = ? AND slot = ? AND code_hash = ?",
                       (arena, slot, chash)).fetchone()
    return row["id"] if row else None


def register_candidate(conn: sqlite3.Connection, path: Path, arena: str, slot: str, origin: str,
                       candidate_id: str | None = None, hunch_id: str | None = None,
                       parents: list[str] | None = None) -> str:
    """Return the id of the candidate with this code (registering it if new)."""
    chash = code_hash(path.read_text(encoding="utf-8"))
    existing = _candidate_id(conn, arena, slot, chash)
    if existing:
        return existing
    cid = candidate_id or f"c-{chash[:10]}"
    try:
        rel = str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        rel = str(path.resolve())
    conn.execute(
        "INSERT INTO candidates (id, arena, slot, hunch_id, code_hash, path, parents, origin, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (cid, arena, slot, hunch_id, chash, rel, json.dumps(parents or []), origin, _now()),
    )
    conn.commit()
    return cid


def submit_candidate(path: Path, hunch_id: str, parents: list[str] | None = None,
                     registry_path: Path = registry.DEFAULT_PATH, origin: str = "proposer") -> str:
    """Register a candidate under a hunch (arena and slot come from the hunch). A file already registered by
    `sforge eval` keeps its id and gets the hunch and lineage attached."""
    from . import ledger

    h = ledger.get(hunch_id)
    conn = registry.connect(registry_path)
    for p in parents or []:
        if conn.execute("SELECT 1 FROM candidates WHERE id = ?", (p,)).fetchone() is None:
            raise KeyError(f"unknown parent candidate {p}")
    cid = register_candidate(conn, path, h["arena"], h["slot"], origin, hunch_id=hunch_id, parents=parents)
    conn.execute("UPDATE candidates SET hunch_id = ?, parents = ?, origin = CASE WHEN origin = 'eval' THEN ? "
                 "ELSE origin END WHERE id = ?", (hunch_id, json.dumps(parents or []), origin, cid))
    conn.commit()
    conn.close()
    return cid


def evaluate_file(path: Path, arena: str, slot: str, suite: str, extra_cases: list[dict] | None = None,
                  registry_path: Path = registry.DEFAULT_PATH, origin: str = "eval",
                  candidate_id: str | None = None, heldout_dir: Path = HELDOUT_DIR,
                  probe: bool = False) -> EvalResult:
    conn = registry.connect(registry_path)
    cid = register_candidate(conn, path, arena, slot, origin, candidate_id)
    version, jhash = judge_version(arena), tree_hash()
    run_id = f"r-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(2)}"
    conn.execute(
        "INSERT INTO runs (id, kind, candidate_id, arena, slot, suite, judge_version, judge_hash, status, started_at) "
        "VALUES (?, 'eval', ?, ?, ?, ?, ?, ?, 'running', ?)",
        (run_id, cid, arena, slot, suite, version, jhash, _now()),
    )
    conn.commit()
    job = {"arena": arena, "slot": slot, "suite": suite, "candidate": str(path.resolve()),
           "extra_cases": extra_cases or [], "probe": probe}
    report = run_worker(job, TIMEOUTS.get(suite, 600))
    instances = report.pop("instances", None)
    if instances is not None:
        store_heldout(run_id, instances, heldout_dir)
    report.update(run_id=run_id, candidate_id=cid, judge_version=version, judge_hash=jhash)

    report_path = REPORTS_DIR / f"{run_id}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=1, default=float), encoding="utf-8")
    rows = []
    for case_id, ms in report.get("cases", {}).items():
        rows += [(run_id, cid, case_id, None, k, float(v), version, jhash) for k, v in ms.items()]
    for k, v in report.get("metamorphic", {}).items():
        rows.append((run_id, cid, "R1", None, k, float(v), version, jhash))
    if "cost" in report:
        rows.append((run_id, cid, None, None, "cost", float(report["cost"]), version, jhash))
    for fam, agg in report.get("families", {}).items():
        for k, v in agg.items():
            if isinstance(v, dict):
                rows += [(run_id, cid, None, fam, f"{k}:{stat}", float(v[stat]), version, jhash)
                         for stat in ("median", "mean", "p90", "worst")]
            elif k == "pass_rate":
                rows.append((run_id, cid, None, fam, "pass_rate", float(v), version, jhash))
    if "max_cfl" in report:
        rows.append((run_id, cid, None, "RF1", "max_cfl", float(report["max_cfl"]), version, jhash))
    conn.executemany(
        "INSERT INTO scores (run_id, candidate_id, case_id, family, metric, value, judge_version, judge_hash) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows)
    conn.execute("UPDATE runs SET status = ?, finished_at = ?, report_path = ? WHERE id = ?",
                 (report["status"], _now(), str(report_path), run_id))
    conn.commit()
    conn.close()
    return EvalResult(run_id, cid, report)


def candidate_path(conn: sqlite3.Connection, candidate_id: str) -> tuple[Path, str, str]:
    row = conn.execute("SELECT path, arena, slot FROM candidates WHERE id = ?", (candidate_id,)).fetchone()
    if row is None:
        raise KeyError(candidate_id)
    p = Path(row["path"])
    return (p if p.is_absolute() else REPO_ROOT / p), row["arena"], row["slot"]
