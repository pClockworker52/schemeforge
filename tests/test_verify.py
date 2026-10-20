"""judge verify and judge exact."""

import json

import pytest
from typer.testing import CliRunner

from schemeforge.arenas.euler1d import verify
from schemeforge.arenas.euler1d.cases import RiemannCase
from schemeforge.cli import app


def test_reference_values_pass() -> None:
    failed = [c for c in verify.check_reference_values() if not c.ok]
    assert not failed, failed


def test_full_verify_passes() -> None:
    failed = [c for c in verify.verify() if not c.ok]
    assert not failed, failed


def test_exact_report_riemann() -> None:
    rep = verify.exact_report(RiemannCase("X", (1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 0.2, 50))
    assert rep["p_star"] == pytest.approx(0.30313, abs=5e-6) and len(rep["rho"]) == 50
    assert [w["kind"] for w in rep["waves"]] == ["rarefaction", "shock"]


def test_exact_report_nozzle_cli(tmp_path) -> None:
    path = tmp_path / "c.yaml"
    path.write_text("kind: nozzle\nid: X\npb: 0.6784\nn: 30\n")
    res = CliRunner().invoke(app, ["judge", "exact", "--arena", "euler1d", "--case", str(path), "--json"])
    assert res.exit_code == 0, res.output
    rep = json.loads(res.output)
    assert rep["regime"] == "shock" and rep["x_shock"] == pytest.approx(2.0993, abs=5e-5) and len(rep["p"]) == 30


def test_exact_batch_cli(tmp_path) -> None:
    path = tmp_path / "batch.yaml"
    path.write_text("- {kind: nozzle, id: A, pb: 0.9, n: 10}\n"
                    "- {kind: riemann, id: B, left: [1, 0, 1], right: [0.125, 0, 0.1], t_end: 0.2, n: 10}\n")
    res = CliRunner().invoke(app, ["judge", "exact", "--arena", "euler1d", "--case", str(path), "--json"])
    assert res.exit_code == 0, res.output
    reps = json.loads(res.output)
    assert [r["kind"] for r in reps] == ["nozzle", "riemann"]


def test_exact_report_rejects_reference_cases() -> None:
    from schemeforge.arenas.euler1d.cases import dev_suite

    r7 = next(c for c in dev_suite() if c.id == "R7")
    with pytest.raises(ValueError):
        verify.exact_report(r7)
