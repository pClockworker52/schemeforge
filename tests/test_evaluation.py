"""sforge eval machinery: tree hash, integrity check, core locks, sandboxed worker, registry rows."""

import json
import subprocess

import pytest

from schemeforge.arenas.euler1d import zoo
from schemeforge.core import evaluation, integrity, locks, registry


def test_tree_hash_tracks_content_and_ignores_caches(tmp_path) -> None:
    (tmp_path / "a.py").write_text("x = 1\n")
    h1 = integrity.tree_hash(tmp_path)
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "a.cpython-312.pyc").write_bytes(b"junk")
    assert integrity.tree_hash(tmp_path) == h1
    (tmp_path / "a.py").write_text("x = 2\n")
    assert integrity.tree_hash(tmp_path) != h1


def _git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def test_integrity_refuses_uncommitted_judge_changes(tmp_path) -> None:
    judge = tmp_path / "judge"
    judge.mkdir()
    (judge / "metrics.py").write_text("A = 1\n")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A")
    _git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init")
    assert integrity.integrity_problems("euler1d", repo=tmp_path, judge_rel="judge") == []
    (judge / "metrics.py").write_text("A = 2\n")
    assert "uncommitted" in integrity.integrity_problems("euler1d", repo=tmp_path, judge_rel="judge")[0]
    (judge / "metrics.py").write_text("A = 1\n")
    (judge / "new_case.yaml").write_text("kind: riemann\n")
    assert integrity.integrity_problems("euler1d", repo=tmp_path, judge_rel="judge")  # untracked files count


def test_core_locks_are_exclusive(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("SFORGE_MAX_PARALLEL", "2")
    with locks.acquire_core(tmp_path) as a, locks.acquire_core(tmp_path) as b:
        assert {a, b} == {1, 2}
        with pytest.raises(TimeoutError):
            with locks.acquire_core(tmp_path, timeout=0.3):
                pass


@pytest.fixture
def in_tmp(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SFORGE_MAX_PARALLEL", "2")
    return tmp_path


def test_smoke_eval_of_a_zoo_limiter_records_everything(in_tmp) -> None:
    path = zoo.members("limiter")["minmod"]
    res = evaluation.evaluate_file(path, "euler1d", "limiter", "smoke", registry_path=in_tmp / "reg.sqlite")
    assert res.report["status"] == "ok", res.report["violations"]
    assert set(res.report["cases"]) == {"smoke-R1"} and res.report["cost"] > 0
    conn = registry.connect(in_tmp / "reg.sqlite")
    run = conn.execute("SELECT * FROM runs WHERE id = ?", (res.run_id,)).fetchone()
    assert run["status"] == "ok" and run["judge_version"] == "euler1d-v0.dev" and len(run["judge_hash"]) == 64
    metrics = {r[0] for r in conn.execute("SELECT metric FROM scores WHERE run_id = ?", (res.run_id,))}
    assert {"l1_smooth", "tv_increase", "seconds", "cost"} <= metrics  # widths are unresolved at N = 50
    assert json.loads((in_tmp / run["report_path"]).read_text())["run_id"] == res.run_id
    # the same code is the same candidate
    again = evaluation.evaluate_file(path, "euler1d", "limiter", "smoke", registry_path=in_tmp / "reg.sqlite")
    assert again.candidate_id == res.candidate_id and again.run_id != res.run_id


@pytest.mark.parametrize(
    "source,expected",
    [
        ("import os\ndef phi(r):\n    return r\n", "import of 'os'"),
        ("import jax.numpy as jnp\ndef limiter(r):\n    return r\n", "does not define a function 'phi'"),
        ("import jax.numpy as jnp\ndef phi(r):\n    return 1.0 / r\n", "not finite"),
        ("import jax.numpy as jnp\nX = 1 / 0\ndef phi(r):\n    return r\n", "loading failed: ZeroDivisionError"),
    ],
    ids=["sandbox", "missing-function", "hard-constraint", "module-body-raises"],
)
def test_bad_candidates_are_rejected_in_the_worker(in_tmp, source, expected) -> None:
    path = in_tmp / "cand.py"
    path.write_text(source)
    res = evaluation.evaluate_file(path, "euler1d", "limiter", "smoke", registry_path=in_tmp / "reg.sqlite")
    assert res.report["status"] == "rejected"
    assert any(expected in v for v in res.report["violations"]), res.report["violations"]


def test_worker_timeout_is_a_rejection(in_tmp, monkeypatch) -> None:
    monkeypatch.setitem(evaluation.TIMEOUTS, "smoke", 1)
    path = zoo.members("limiter")["minmod"]
    res = evaluation.evaluate_file(path, "euler1d", "limiter", "smoke", registry_path=in_tmp / "reg.sqlite")
    assert res.report["status"] == "rejected"
    assert any("timeout" in v or "CPU time" in v for v in res.report["violations"]), res.report["violations"]
