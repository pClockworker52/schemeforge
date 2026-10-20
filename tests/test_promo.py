"""Promo suite: aggregation, max_cfl, and that instance details never reach reports, the registry or stdout.

Uses a temporary test seed and tiny family sizes; never reads ~/.schemeforge.
"""

import json

import numpy as np
import pytest

from schemeforge.arenas.euler1d import evaluate, families, zoo
from schemeforge.core import evaluation, registry


def test_aggregate_uses_the_bad_side() -> None:
    inst = {
        f"NF1-{i:03d}": {"family": "NF1", "violations": [] if i else ["x"],
                         "metrics": {"shock_pos_err": float(i), "res_orders_expl": float(10 - i)}}
        for i in range(11)
    }
    agg = evaluate.aggregate(inst)["NF1"]
    assert agg["n"] == 11 and agg["pass_rate"] == pytest.approx(10 / 11)
    assert agg["shock_pos_err"]["median"] == 5.0 and agg["shock_pos_err"]["worst"] == 10.0
    assert agg["shock_pos_err"]["p90"] == pytest.approx(9.0)
    assert agg["res_orders_expl"]["worst"] == 0.0 and agg["res_orders_expl"]["p90"] == pytest.approx(1.0)


@pytest.fixture
def test_seed(tmp_path, monkeypatch):
    seed_file = tmp_path / "heldout_seed"
    seed_file.write_text("test-seed-fedcba9876543210\n")
    monkeypatch.setattr(families, "SEED_FILE", seed_file)
    monkeypatch.setattr(families, "FAMILY_SIZES", {"RF1": 2, "RF2": 1, "NF1": 1, "NF2": 1, "NF3": 1})
    return seed_file


def test_promo_report_in_process(test_seed) -> None:
    rep = evaluate.evaluate(zoo.load("limiter", "minmod"), "limiter", "promo")
    assert rep["status"] == "ok", rep["violations"]
    assert set(rep["families"]) == {"RF1", "RF2", "NF1", "NF2", "NF3"}
    assert rep["families"]["NF1"]["pass_rate"] == 1.0 and "shock_pos_err" in rep["families"]["NF1"]
    assert rep["max_cfl"] >= 0.5
    assert rep["seed_fingerprint"] == families.seed_fingerprint("test-seed-fedcba9876543210")
    assert len(rep["instances"]) == 6 and "case" in rep["instances"]["NF1-000"]


def test_parent_strips_instances(tmp_path, monkeypatch) -> None:
    secret = {"NF1-000": {"family": "NF1", "violations": [], "metrics": {"shock_pos_err": 0.1},
                          "case": {"pb": 0.123456789}}}
    fake = {"status": "ok", "violations": [], "cases": {}, "metamorphic": {}, "max_cfl": 0.9,
            "families": evaluate.aggregate(secret), "instances": secret}
    monkeypatch.setattr(evaluation, "run_worker", lambda job, timeout: json.loads(json.dumps(fake)))
    monkeypatch.chdir(tmp_path)
    res = evaluation.evaluate_file(zoo.members("limiter")["minmod"], "euler1d", "limiter", "promo",
                                   registry_path=tmp_path / "reg.sqlite", heldout_dir=tmp_path / "heldout")
    assert "instances" not in res.report
    stored = json.loads((tmp_path / "heldout" / f"{res.run_id}.json").read_text())
    assert stored["NF1-000"]["case"]["pb"] == 0.123456789
    public = (tmp_path / "runs" / "reports" / f"{res.run_id}.json").read_text()
    assert "0.123456789" not in public and "NF1-000" not in public
    conn = registry.connect(tmp_path / "reg.sqlite")
    rows = conn.execute("SELECT family, metric, case_id FROM scores WHERE run_id = ?", (res.run_id,)).fetchall()
    assert {(r["family"], r["metric"]) for r in rows} >= {("NF1", "shock_pos_err:median"), ("NF1", "pass_rate"),
                                                         ("RF1", "max_cfl")}
    assert all(r["case_id"] is None for r in rows)


def test_max_cfl_detects_instability() -> None:
    cases = [families.rf1("test-seed-max-cfl-0000", i) for i in range(2)]
    stable = zoo.load("limiter", "minmod")
    from schemeforge.arenas.euler1d.numerics import hllc, muscl

    assert evaluate.max_cfl(cases, muscl(stable), hllc) >= 0.5

    def unlimited(r):
        return np.ones_like(r) * 1.0 + 0.0 * r

    assert evaluate.max_cfl(cases, muscl(unlimited), hllc) < 0.9
