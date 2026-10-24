"""Hunch ledger, submit and leaderboard (temporary ledger and registry only)."""

import json

import pytest

from schemeforge.core import evaluation, leaderboard, ledger, registry
from schemeforge.core.pareto import dominates, pareto_ranks

DRAFT = {
    "arena": "euler1d", "slot": "limiter", "lens": "steady-convergence",
    "statement": "A smooth limiter with tunable compressiveness converges and stays sharp.",
    "mechanism": "No kinks in phi, so the Newton Jacobian is continuous at the shock.",
    "predicted_effect": [{"metric": "newton_iters", "direction": "down", "size": ">= 2x vs superbee on N1"}],
    "kill_criterion": "No candidate reaches 1e-12 on N1 with shock width <= 2.8 cells within two rounds.",
    "known_relatives": ["van Albada", "Venkatakrishnan"], "author": "peter",
}


@pytest.fixture
def tmp_ledger(tmp_path, monkeypatch):
    path = tmp_path / "hunches.yaml"
    path.write_text("[]\n")
    monkeypatch.setattr(ledger, "LEDGER", path)
    return path


def test_ledger_add_list_close(tmp_ledger) -> None:
    assert ledger.add(DRAFT) == "H-0001" and ledger.add(DRAFT) == "H-0002"
    h = ledger.get("H-0002")
    assert h["status"] == "open" and h["verdict_note"] == ""
    ledger.close("H-0001", "refuted", "run r-x: stalls like superbee")
    assert ledger.get("H-0001")["status"] == "refuted"
    assert "only source of truth" in tmp_ledger.read_text()
    with pytest.raises(ledger.LedgerError):
        ledger.close("H-0002", "refuted", "  ")


@pytest.mark.parametrize("bad,msg", [
    ({k: v for k, v in DRAFT.items() if k != "mechanism"}, "missing field 'mechanism'"),
    ({**DRAFT, "lens": "vibes"}, "lens"),
    ({**DRAFT, "predicted_effect": [{"metric": "x", "direction": "sideways", "size": "1"}]}, "direction"),
    ({**DRAFT, "known_relatives": "van Albada"}, "known_relatives"),
])
def test_ledger_rejects_bad_drafts(tmp_ledger, bad, msg) -> None:
    with pytest.raises(ledger.LedgerError, match=msg):
        ledger.add(bad)


def test_pareto() -> None:
    assert dominates([1, 1], [1, 2]) and not dominates([1, 2], [2, 1]) and not dominates([1, 1], [1, 1])
    assert pareto_ranks([[1, 2], [2, 1], [2, 2], [3, 3], [float("nan"), 0]]) == [0, 0, 1, 2, 0]


def _fake_run(conn, cid, run_id, values, origin="eval", path="candidates/x.py"):
    conn.execute("INSERT OR IGNORE INTO candidates (id, arena, slot, code_hash, path, origin, created_at) "
                 "VALUES (?, 'euler1d', 'limiter', ?, ?, ?, 't')", (cid, cid, path, origin))
    conn.execute("INSERT INTO runs (id, kind, candidate_id, arena, slot, suite, judge_version, judge_hash, status, "
                 "started_at) VALUES (?, 'eval', ?, 'euler1d', 'limiter', 'dev', 'v-test', 'h', 'ok', ?)",
                 (run_id, cid, run_id))
    for key, v in values.items():
        case, metric = key.split(".")
        conn.execute("INSERT INTO scores (run_id, candidate_id, case_id, metric, value, judge_version, judge_hash) "
                     "VALUES (?, ?, ?, ?, ?, 'v-test', 'h')", (run_id, cid, case, metric, v))


def test_leaderboard_ranks_and_vs_zoo(tmp_path) -> None:
    conn = registry.connect(tmp_path / "reg.sqlite")
    base = {"R1.shock_width": 3.0, "R1.contact_width": 7.0, "N1.res_orders_expl": 12.0, "N1.newton_iters": 60.0,
            "N4.roughness_J": 0.002, "S1.order_smooth": 2.0, "R7.l1_ref": 0.006}
    _fake_run(conn, "zoo-a", "r1", base, origin="zoo", path="src/schemeforge/arenas/euler1d/zoo/limiter/a.py")
    _fake_run(conn, "c-better", "r2", {**base, "R1.shock_width": 2.5})
    _fake_run(conn, "c-worse", "r3", {**base, "N1.newton_iters": 300.0})
    rows = leaderboard.build(conn, "euler1d", "limiter", version="v-test")
    by_id = {r.candidate_id: r for r in rows}
    assert by_id["c-better"].rank == 0 and by_id["zoo-a"].rank == 1 and by_id["c-worse"].rank == 2
    assert by_id["c-better"].vs_zoo["R1.shock_width"] == pytest.approx(2.5 / 3.0)
    assert by_id["c-worse"].vs_zoo["N1.newton_iters"] == pytest.approx(5.0)
    assert rows[0].candidate_id == "c-better"


def test_leaderboard_screen_ranks_first_and_marks_duplicates(tmp_path) -> None:
    # round 3: the scalar score ranked a contact gain above an A1 loss, and four of five top picks were one scheme
    from schemeforge.engine.objectives import SCREENS

    conn = registry.connect(tmp_path / "reg.sqlite")
    passing = {f"{case}.{metric}": (thr * 0.9 if op == "<=" else thr) for case, metric, op, thr
               in SCREENS["euler1d"]["limiter"]}
    zoo = "src/schemeforge/arenas/euler1d/zoo/limiter/z.py"
    _fake_run(conn, "zoo-z", "r0", {**passing, "R1.contact_width": 6.4}, origin="zoo", path=zoo)
    _fake_run(conn, "c-sharp", "r1", passing)  # passes every screen check
    _fake_run(conn, "c-wide", "r2", {**passing, "R1.shock_width": 3.4, "R1.contact_width": 1.0})  # fails A1 only
    _fake_run(conn, "c-wide2", "r3", {**passing, "R1.shock_width": 3.4, "R1.contact_width": 1.0})  # same scheme
    rows = leaderboard.build(conn, "euler1d", "limiter", version="v-test")
    by_id = {r.candidate_id: r for r in rows}
    assert by_id["c-sharp"].fails == 0 and by_id["c-wide"].fails == 1
    # the scalar score prefers c-wide (its contact gain outweighs the wider shock) ...
    assert by_id["c-wide"].rank == by_id["c-sharp"].rank == 0 and by_id["c-wide"].score < by_id["c-sharp"].score
    # ... but the screen puts c-sharp first, and c-wide2 is marked as c-wide's duplicate
    assert rows.index(by_id["c-sharp"]) < rows.index(by_id["c-wide"])
    assert by_id["c-wide2"].duplicate_of == "c-wide" and by_id["c-wide"].duplicate_of is None


def test_submit_attaches_hunch_and_lineage(tmp_ledger, tmp_path) -> None:
    hid = ledger.add(DRAFT)
    f = tmp_path / "cand.py"
    f.write_text("import jax.numpy as jnp\ndef phi(r):\n    return jnp.clip(r, 0.0, 1.0)\n")
    reg = tmp_path / "reg.sqlite"
    first = evaluation.submit_candidate(f, hid, registry_path=reg)
    f2 = tmp_path / "cand2.py"
    f2.write_text("import jax.numpy as jnp\ndef phi(r):\n    return jnp.clip(r, 0.0, 2.0)\n")
    child = evaluation.submit_candidate(f2, hid, [first], registry_path=reg)
    row = registry.connect(reg).execute("SELECT * FROM candidates WHERE id = ?", (child,)).fetchone()
    assert row["hunch_id"] == hid and json.loads(row["parents"]) == [first] and row["origin"] == "proposer"
    with pytest.raises(KeyError):
        evaluation.submit_candidate(f2, hid, ["c-nope"], registry_path=reg)
