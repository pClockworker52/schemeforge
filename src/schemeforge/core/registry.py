"""SQLite registry of candidates, runs, scores, cases and LLM calls (PLAN §5.1, §8 task 6).

Hunches are not stored here: `ledger/hunches.yaml` is their only source of truth, and rows refer to them by id.
Agents never write to the database directly; they go through the `sforge` CLI.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_VERSION = 2
BUSY_TIMEOUT = 120.0  # seconds to wait for a lock held by another writer
DEFAULT_PATH = Path("runs") / "registry.sqlite"

SCHEMA = """
CREATE TABLE IF NOT EXISTS candidates (
    id          TEXT PRIMARY KEY,
    arena       TEXT NOT NULL,
    slot        TEXT NOT NULL,
    hunch_id    TEXT,                      -- id in ledger/hunches.yaml; NULL for zoo members
    code_hash   TEXT NOT NULL,             -- sha256 of the source
    path        TEXT NOT NULL,
    parents     TEXT NOT NULL DEFAULT '[]',-- JSON list of candidate ids
    origin      TEXT NOT NULL,             -- zoo | proposer | engine | redteam | peter
    created_at  TEXT NOT NULL,
    UNIQUE (arena, slot, code_hash)
);

CREATE TABLE IF NOT EXISTS runs (
    id            TEXT PRIMARY KEY,
    kind          TEXT NOT NULL,           -- eval | zoo | evolve | promo
    candidate_id  TEXT REFERENCES candidates(id),
    arena         TEXT NOT NULL,
    slot          TEXT,
    suite         TEXT,                    -- smoke | dev | promo
    judge_version TEXT NOT NULL,
    judge_hash    TEXT NOT NULL,
    status        TEXT NOT NULL,           -- running | ok | rejected | error
    started_at    TEXT NOT NULL,
    finished_at   TEXT,
    report_path   TEXT
);

CREATE TABLE IF NOT EXISTS scores (
    id            INTEGER PRIMARY KEY,
    run_id        TEXT NOT NULL REFERENCES runs(id),
    candidate_id  TEXT NOT NULL REFERENCES candidates(id),
    case_id       TEXT,                    -- NULL for family aggregates (promo)
    family        TEXT,
    metric        TEXT NOT NULL,
    value         REAL,
    judge_version TEXT NOT NULL,
    judge_hash    TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS scores_by_candidate ON scores (candidate_id, metric);
-- schema v2: the leaderboard looks up a candidate's latest run and that run's scores for every candidate; without
-- these, each lookup scanned the whole scores table (a 30-min leaderboard on the round-2 registry on /mnt/c)
CREATE INDEX IF NOT EXISTS scores_by_run ON scores (run_id);
CREATE INDEX IF NOT EXISTS runs_by_candidate ON runs (candidate_id, suite, judge_version, status, started_at);

CREATE TABLE IF NOT EXISTS cases (
    id                     TEXT PRIMARY KEY,
    arena                  TEXT NOT NULL,
    family                 TEXT,
    status                 TEXT NOT NULL,  -- quarantine | accepted | rejected
    path                   TEXT NOT NULL,
    proposed_by            TEXT NOT NULL,
    created_at             TEXT NOT NULL,
    accepted_judge_version TEXT
);

CREATE TABLE IF NOT EXISTS llm_calls (
    id            INTEGER PRIMARY KEY,
    backend       TEXT NOT NULL,
    model         TEXT NOT NULL,
    prompt_hash   TEXT NOT NULL,
    latency_s     REAL,
    cost_usd      REAL,
    input_tokens  INTEGER,
    output_tokens INTEGER,
    candidate_id  TEXT REFERENCES candidates(id),
    created_at    TEXT NOT NULL
);
"""

TABLES = ("candidates", "runs", "scores", "cases", "llm_calls")


def connect(path: Path | str = DEFAULT_PATH) -> sqlite3.Connection:
    """Open the registry, creating the file and schema if needed. Foreign keys are enforced."""
    file_db = str(path) != ":memory:"
    if file_db:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    # Many engine threads and evaluations write concurrently: wait up to BUSY_TIMEOUT for locks, use WAL.
    conn = sqlite3.connect(path, timeout=BUSY_TIMEOUT)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    # setting the journal mode needs a lock even when it is already WAL (zoo eval with 12 parallel members hit
    # "database is locked" here), so set it only once per file
    if file_db and conn.execute("PRAGMA journal_mode").fetchone()[0].lower() != "wal":
        conn.execute("PRAGMA journal_mode = WAL")
    init_db(conn)
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create the schema (idempotent) and record its version in PRAGMA user_version. An up-to-date registry is
    left untouched, so that opening a connection takes no write lock."""
    (version,) = conn.execute("PRAGMA user_version").fetchone()
    if version > SCHEMA_VERSION:
        raise RuntimeError(f"registry schema v{version} is newer than this code (v{SCHEMA_VERSION})")
    if version == SCHEMA_VERSION:
        return
    conn.executescript(SCHEMA)
    conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
    conn.commit()
