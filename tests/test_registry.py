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
