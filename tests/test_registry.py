"""Tests for the SQLite registry schema."""

import sqlite3

import pytest

from schemeforge.core import registry


def test_schema_has_all_tables(tmp_path) -> None:
    conn = registry.connect(tmp_path / "runs" / "registry.sqlite")
    names = {r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert set(registry.TABLES) <= names
    assert "hunches" not in names  # hunches live in ledger/hunches.yaml only
    assert conn.execute("PRAGMA user_version").fetchone()[0] == registry.SCHEMA_VERSION


def test_init_is_idempotent(tmp_path) -> None:
    path = tmp_path / "registry.sqlite"
    registry.connect(path).close()
    registry.connect(path).close()


def test_foreign_keys_are_enforced() -> None:
    conn = registry.connect(":memory:")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO scores (run_id, candidate_id, metric, value, judge_version, judge_hash) "
            "VALUES ('no-run', 'no-cand', 'l1_smooth', 1.0, 'euler1d-v1.0', 'abc')"
        )


def test_duplicate_code_hash_is_rejected() -> None:
    conn = registry.connect(":memory:")
    row = ("c1", "euler1d", "limiter", None, "h", "p", "[]", "zoo", "2026-10-20")
    sql = (
        "INSERT INTO candidates (id, arena, slot, hunch_id, code_hash, path, parents, origin, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )
    conn.execute(sql, row)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(sql, ("c2", *row[1:]))


def test_concurrent_writers(tmp_path) -> None:
    """Regression: 16 engine threads hit 'database is locked' (5 s default timeout, a write on every connect)."""
    from concurrent.futures import ThreadPoolExecutor

    path = tmp_path / "reg.sqlite"
    registry.connect(path).close()

    def write(i: int) -> None:
        for k in range(20):
            conn = registry.connect(path)
            conn.execute("INSERT INTO llm_calls (backend, model, prompt_hash, created_at) VALUES ('t', 'm', ?, 't')",
                         (f"{i}-{k}",))
            conn.commit()
            conn.close()

    with ThreadPoolExecutor(max_workers=16) as pool:
        list(pool.map(write, range(16)))
    assert registry.connect(path).execute("SELECT COUNT(*) FROM llm_calls").fetchone()[0] == 320


def test_newer_schema_is_refused() -> None:
    conn = sqlite3.connect(":memory:")
    conn.execute(f"PRAGMA user_version = {registry.SCHEMA_VERSION + 1}")
    with pytest.raises(RuntimeError):
        registry.init_db(conn)


def test_v1_registry_gains_the_leaderboard_indexes(tmp_path) -> None:
    # a registry created before schema v2 has no index on scores.run_id or runs.candidate_id; opening it adds them,
    # so the leaderboard's per-candidate lookups stop scanning the whole scores table
    path = tmp_path / "old.sqlite"
    conn = registry.connect(path)
    conn.execute("DROP INDEX scores_by_run")
    conn.execute("DROP INDEX runs_by_candidate")
    conn.execute("PRAGMA user_version = 1")
    conn.commit()
    conn.close()
    conn = registry.connect(path)
    assert conn.execute("PRAGMA user_version").fetchone()[0] == registry.SCHEMA_VERSION
    plans = [conn.execute(f"EXPLAIN QUERY PLAN {q}").fetchone()[3] for q in (
        "SELECT id FROM runs WHERE candidate_id = 'c' AND suite = 'dev' AND status = 'ok' AND judge_version = 'v' "
        "ORDER BY started_at DESC LIMIT 1",
        "SELECT metric, value FROM scores WHERE run_id = 'r'")]
    assert "runs_by_candidate" in plans[0] and "scores_by_run" in plans[1]


def test_accept_records_a_case_already_moved_by_a_judge_commit(tmp_path, monkeypatch) -> None:
    # judge v1.4 moved accepted cases in a commit made in another checkout; `sforge case accept` on the machine
    # that holds the registry must then only record the acceptance
    from schemeforge.core import quarantine

    monkeypatch.setattr(quarantine, "ARENAS_DIR", tmp_path / "arenas")
    reg = tmp_path / "reg.sqlite"
    conn = registry.connect(reg)
    conn.execute("INSERT INTO cases (id, arena, family, status, path, proposed_by, created_at) VALUES "
                 "('B-0099', 'euler1d', 'riemann', 'quarantine', ?, 'breaker', 'now')",
                 (str(tmp_path / "quarantine" / "B-0099.yaml"),))
    conn.commit()
    dest = tmp_path / "arenas" / "euler1d" / "cases" / "accepted" / "B-0099.yaml"
    dest.parent.mkdir(parents=True)
    dest.write_text("kind: riemann\n")
    assert quarantine.accept("B-0099", registry_path=reg) == dest
    assert registry.connect(reg).execute("SELECT status FROM cases WHERE id = 'B-0099'").fetchone()[0] == "accepted"
    with pytest.raises(ValueError):
        quarantine.accept("B-0099", registry_path=reg)  # no longer quarantined


def test_changed_zoo_file_gets_its_own_id(tmp_path) -> None:
    # judge v1.5 (WSL zoo eval): the changed thinc_bvd reused id zoo-reconstruction-thinc_bvd; the duplicate INSERT
    # left a write transaction open and every other worker died with "database is locked"
    from schemeforge.core.evaluation import register_candidate

    conn = registry.connect(tmp_path / "r.sqlite")
    f = tmp_path / "member.py"
    f.write_text("EPS = 1e-20\n")
    old = register_candidate(conn, f, "euler1d", "reconstruction", "zoo", candidate_id="zoo-reconstruction-m")
    f.write_text("EPS = 1e-20  # relative\n")
    new = register_candidate(conn, f, "euler1d", "reconstruction", "zoo", candidate_id="zoo-reconstruction-m")
    assert old == "zoo-reconstruction-m" and new.startswith("zoo-reconstruction-m-") and new != old
    assert register_candidate(conn, f, "euler1d", "reconstruction", "zoo", candidate_id="zoo-reconstruction-m") == new
    assert not conn.in_transaction
