"""The B06 scorer applies rule S1, rule B6 and the CS-07 sign test, on synthetic outcome rows only."""

import csv
import shutil
from pathlib import Path

import pytest

from schemeforge.research import coldspray_blind_b06_score as sc
from schemeforge.research.coldspray import DATA

HEADER = ("id,particle,substrate,particle_condition,substrate_condition,oxide_state,oxide_source,d_um,d_um_spread,"
          "T_substrate_K,vcr_low_mps,vcr_high_mps,vcr_mid_mps,vcr_definition,n_impacts,regime,read_from,"
          "primary_source,extraction,notes")


def _setup(tmp_path: Path, rows: list[dict]) -> Path:
    shutil.copy(DATA / "predictions_b06.csv", tmp_path / "predictions_b06.csv")
    with open(tmp_path / "vcr_lipit.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER.split(","), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in HEADER.split(",")})
    return tmp_path


def _row(cid: str, mid: float, lo: str = "", hi: str = "", notes: str = "") -> dict:
    return {"id": f"B-{cid}", "particle": "Al", "substrate": "Al", "vcr_low_mps": lo, "vcr_high_mps": hi,
            "vcr_mid_mps": str(mid), "notes": notes}


def test_no_outcome_rows(tmp_path: Path) -> None:
    res = sc.write(_setup(tmp_path, []))
    assert res["CS07_B06"] == "no outcome rows" and res["n_scored"] == 0


@pytest.mark.parametrize(("v1", "v2", "verdict"), [(800, 790, "refuted"), (800, 810, "inconclusive"),
                                                    (800, 900, "supported")])
def test_cs07_branches_with_rule_b6_windows(tmp_path: Path, v1: float, v2: float, verdict: str) -> None:
    u = "velocity uncertainty +-2 %"
    rows = [_row("B06-c1", v1, notes=u), _row("B06-c2", v2, notes=u)]
    res = sc.write(_setup(tmp_path, rows))
    assert res["CS07_B06"] == verdict
    assert res["w_B06"] == pytest.approx(0.04 * (v1 + v2) / 2)  # median of the two B6 widths


def test_s1_inside_and_outside_printed_window(tmp_path: Path) -> None:
    rows = [_row("B06-c1", 805, lo="795", hi="815"), _row("B06-c2", 700, lo="690", hi="710")]
    sc.write(_setup(tmp_path, rows))
    with open(tmp_path / "scores_b06.csv", newline="") as fh:
        s = {(r["model"], r["row"]): float(r["S1"]) for r in csv.DictReader(fh)}
    assert s[("Z6_a015", "B06-c1")] == 0.0
    assert s[("Z6_a015", "B06-c2")] == pytest.approx((805.1 - 710) / 700)
    assert ("CS-10", "B06-c1") not in s  # no prediction, not scored
