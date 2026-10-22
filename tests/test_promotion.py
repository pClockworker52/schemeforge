"""Promotion test with synthetic held-out runs (never real held-out data)."""

import json

import numpy as np
import pytest

from schemeforge.core import promotion


def _write(d, run, rows):
    (d / f"{run}.json").write_text(json.dumps(rows))


def _instances(rng, shock, contact, rough, conv_e=1.0, conv_i=1.0, over=0.01, n=20, long_contact=16.0,
               long_order=1.95):
    rows = {}
    for i in range(n):
        rows[f"RF1-{i:03d}"] = {"family": "RF1", "violations": [], "metrics": {
            "shock_width": shock * (1 + 0.05 * rng.standard_normal()),
            "contact_width": contact * (1 + 0.05 * rng.standard_normal()), "overshoot": over}}
        rows[f"NF1-{i:03d}"] = {"family": "NF1", "violations": [], "metrics": {
            "converged_expl": conv_e, "converged_impl": conv_i}}
    for i in range(5):
        rows[f"NF3-{i:03d}"] = {"family": "NF3", "violations": [], "metrics": {"roughness_J": rough * (1 + 0.1 * i)}}
    for i in range(10):
        rows[f"RF2-{i:03d}"] = {"family": "RF2", "violations": [], "metrics": {"overshoot": over}}
    for i in range(5):
        rows[f"LF1-{i:03d}"] = {"family": "LF1", "violations": [], "metrics": {"contact_width": long_contact}}
        rows[f"LF2-{i:03d}"] = {"family": "LF2", "violations": [], "metrics": {"order_smooth": long_order}}
    return rows


def test_paired_bootstrap() -> None:
    rng = np.random.default_rng(0)
    ref = rng.uniform(2, 4, 50)
    m, lo, hi = promotion.paired_bootstrap(ref * 0.8, ref)
    assert m == pytest.approx(np.log(0.8)) and lo <= m <= hi < 0
    m, lo, hi = promotion.paired_bootstrap(ref * rng.uniform(0.9, 1.1, 50), ref)
    assert lo < 0 < hi


def test_target_a_pass_and_fail(tmp_path) -> None:
    rng = np.random.default_rng(1)
    _write(tmp_path, "zoo-va", _instances(rng, 3.4, 8.4, 0.0011))
    _write(tmp_path, "zoo-mc", _instances(rng, 2.5, 6.1, 10.0, conv_e=0.45, conv_i=0.35))
    _write(tmp_path, "zoo-vl", _instances(rng, 2.9, 7.1, 0.0012, over=0.02))
    zoo = {"van_albada": "zoo-va", "mc": "zoo-mc", "van_leer": "zoo-vl"}
    _write(tmp_path, "good", _instances(rng, 2.5, 6.2, 0.0012, over=0.015))
    checks = promotion.check_target("A", "good", zoo, {"S1.order_smooth": 1.95}, heldout_dir=tmp_path)
    assert all(c.ok for c in checks), [c for c in checks if not c.ok]
    _write(tmp_path, "sharp-but-stalls", _instances(rng, 2.4, 5.0, 8.0, conv_e=0.4, conv_i=0.3))
    bad = {c.id: c.ok for c in promotion.check_target("A", "sharp-but-stalls", zoo, {"S1.order_smooth": 1.95},
                                                       heldout_dir=tmp_path)}
    # sharp enough (A1, B1) but stalls (A3, A4) and stays rough (A5; still smoother than MC, so B5 passes)
    assert bad["A1"] and bad["B1"] and not bad["A3"] and not bad["A4"] and not bad["A5"] and bad["B5"]


def test_target_a8_long_runs(tmp_path) -> None:
    # A8 (2026-10-22): a ratchet that is sharp and convergent on the short families but first order after ~1000 steps
    rng = np.random.default_rng(2)
    zoo = {"van_albada": "zoo-va", "mc": "zoo-mc", "van_leer": "zoo-vl"}
    _write(tmp_path, "zoo-va", _instances(rng, 3.4, 8.4, 0.0011))
    _write(tmp_path, "zoo-mc", _instances(rng, 2.5, 6.1, 10.0, conv_e=0.45, conv_i=0.35))
    _write(tmp_path, "zoo-vl", _instances(rng, 2.9, 7.1, 0.0012, over=0.02, long_contact=16.5, long_order=1.97))
    _write(tmp_path, "ratchet", _instances(rng, 2.5, 6.2, 0.0012, over=0.015, long_contact=107.0, long_order=-1.4))
    c = {c.id: c for c in promotion.check_target("A", "ratchet", zoo, {"S1.order_smooth": 1.95}, heldout_dir=tmp_path)}
    assert c["A1"].ok and c["A3"].ok and not c["A8a"].ok and not c["A8b"].ok
    # a promo run from before judge v1.4 has no LF families: A8 fails rather than passing silently
    rows = _instances(rng, 2.5, 6.2, 0.0012, over=0.015)
    _write(tmp_path, "old", {k: v for k, v in rows.items() if not k.startswith("LF")})
    old = {c.id: c.ok for c in promotion.check_target("A", "old", zoo, {"S1.order_smooth": 1.95}, heldout_dir=tmp_path)}
    assert old["A1"] and not old["A8a"] and not old["A8b"]
