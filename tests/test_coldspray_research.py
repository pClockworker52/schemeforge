"""Tests for the cold-spray retrospective zoo helpers (src/schemeforge/research/coldspray.py)."""

import math

import pytest

from schemeforge.research import coldspray as cs


@pytest.fixture(scope="module")
def rows():
    return cs.load_rows()


@pytest.fixture(scope="module")
def props():
    return cs.load_properties()


def test_distance_rule():
    assert cs.distance(800.0, 790.0, 835.0) == 0.0
    assert cs.distance(790.0, 790.0, 835.0) == 0.0
    assert cs.distance(700.0, 790.0, 830.0) == pytest.approx(90.0 / 810.0)
    assert cs.distance(900.0, 790.0, 830.0) == pytest.approx(70.0 / 810.0)


def test_matched_source_first(props):
    # Cu density: Table S1 (8960) wins over the handbook row (8935)
    assert props["Cu"]["rho_kg_m3"] == (8960.0, "P-H20-Cu")
    # a field Table S1 lacks falls through to the next source in order
    assert props["Cu"]["Tm_K"][1] == "P-HG-Cu"
    # Al alloys have no handbook rows: nothing is invented
    assert "Tm_K" not in props["Al 7075"]


def test_bulk_modulus_from_table_s1(props):
    b, src = cs.bulk_modulus_pa(props["Al"])
    assert b == pytest.approx(70e9 / (3 * (1 - 2 * 0.35)))
    assert src.startswith("P-H20-Al")


def test_z6_value_and_domain(rows, props):
    row = next(r for r in rows if r.id == "H20-17")  # Al-Al, 14 um, room temperature, polished
    p = cs.z6_sound_speed(0.15)(row, props)
    b, _ = cs.bulk_modulus_pa(props["Al"])
    assert p.v == pytest.approx(0.15 * math.sqrt(b / 2700.0))
    assert p.in_domain
    heated = next(r for r in rows if r.id == "CH-01")
    assert not cs.z6_sound_speed(0.15)(heated, props).in_domain


def test_mismatched_pairs_not_predicted_by_z6(rows, props):
    row = next(r for r in rows if r.id == "H20-01")  # Al on Ni
    assert cs.z6_sound_speed(0.15)(row, props).v is None


def test_impact_ratio_is_reciprocal(props):
    r1 = cs.impact_ratio(props["Al"], props["Ni"])
    r2 = cs.impact_ratio(props["Ni"], props["Al"])
    assert r1 * r2 == pytest.approx(1.0)


def test_predictions_do_not_read_windows(rows, props):
    blank = [cs.Row(r.id, r.particle, r.substrate, r.substrate_condition, r.d_um, r.T_substrate, None, None,
                    None, r.regime) for r in rows]
    # baseline uses H20 midpoints by design; every other model must be independent of the windows
    a = [p for p in cs.predict(rows, props) if p["model"] != "baseline_LOMO"]
    b = [p for p in cs.predict(blank, props) if p["model"] != "baseline_LOMO"]
    assert a == b


def test_cs10_nnls2_exact_and_bounded():
    from schemeforge.research.coldspray_cs10 import nnls2

    x1, x2 = [1.0, 2.0, 3.0], [1.0, 0.0, 1.0]
    assert nnls2(x1, x2, [2 * a + 3 * b for a, b in zip(x1, x2, strict=True)]) == pytest.approx((2.0, 3.0))
    # a negative unconstrained coefficient is clipped to the bound
    b1, b2 = nnls2(x1, x2, [2 * a - 3 * b for a, b in zip(x1, x2, strict=True)])
    assert b2 == 0.0 and b1 > 0.0


def test_cs10_fit_frozen_constants():
    from schemeforge.research.coldspray_cs10 import calibration_data, fit

    rows = calibration_data()
    assert [r["cond_id"] for r in rows] == [f"B10-c{i}" for i in range(1, 6)]
    m = fit(rows)
    # frozen in docs/research/coldspray-cs10-fit.md
    assert m.beta == pytest.approx(0.3774, rel=1e-3)
    assert m.gamma == pytest.approx(3.190e11, rel=1e-3)
