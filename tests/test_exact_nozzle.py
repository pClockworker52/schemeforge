"""Exact quasi-1D nozzle solution: Appendix H values and property tests (PLAN §9.2, §9.10)."""

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from schemeforge.arenas.euler1d.exact_nozzle import (
    anderson_nozzle,
    area_ratio,
    critical_pressures,
    mach_from_area_ratio,
    shock_p_ratio,
    solve_nozzle,
)
from schemeforge.arenas.euler1d.gas import GAMMA_STRESS, GAMMAS, entropy

G = 1.4


def test_anderson_reference_values() -> None:
    nz = anderson_nozzle()
    assert nz.A_exit / nz.A_throat == pytest.approx(5.95, abs=1e-12)
    cp = critical_pressures(nz, G)
    assert cp.p_crit1 == pytest.approx(0.99333, abs=5e-6)
    assert cp.M_exit_sub == pytest.approx(0.09782, abs=5e-6)
    assert cp.p_crit2 == pytest.approx(0.20854, abs=5e-6)
    assert cp.p_crit3 == pytest.approx(0.016046, abs=5e-7)
    assert cp.M_exit_sup == pytest.approx(3.35897, abs=5e-6)


def test_anderson_shock_case() -> None:
    sol = solve_nozzle(anderson_nozzle(), 0.6784, G)
    assert sol.regime == "shock"
    assert sol.x_shock == pytest.approx(2.0993, abs=5e-5)
    assert sol.M1 == pytest.approx(2.0700, abs=5e-5)
    assert sol.p0_ratio == pytest.approx(0.68817, abs=5e-6)
    assert sol.M_exit == pytest.approx(0.14308, abs=5e-6)


def test_area_mach_inversion_roundtrip() -> None:
    for g in (*GAMMAS, GAMMA_STRESS):
        for M in (0.01, 0.3, 0.99, 1.01, 2.0, 7.0):
            assert mach_from_area_ratio(float(area_ratio(M, g)), g, supersonic=M > 1) == pytest.approx(M, rel=1e-11)


@pytest.mark.parametrize("pb,regime", [(0.995, "subsonic"), (0.6784, "shock"), (0.01, "supersonic")])
def test_dev_cases_regimes_and_exit_pressure(pb: float, regime: str) -> None:
    nz = anderson_nozzle()
    sol = solve_nozzle(nz, pb, G)
    assert sol.regime == regime
    p_exit = sol.profile([nz.x_exit])["p"][0]
    expected = critical_pressures(nz, G).p_crit3 if regime == "supersonic" else pb
    assert p_exit == pytest.approx(expected, rel=1e-12)


gammas = st.sampled_from([*GAMMAS, GAMMA_STRESS])


@settings(max_examples=150, deadline=None)
@given(st.floats(0.0, 1.0), gammas)
def test_shock_regime_invariants(frac: float, g: float) -> None:
    """In the shock regime: mdot and h0 are constant, entropy jumps only at the shock, RH holds there."""
    nz = anderson_nozzle()
    cp = critical_pressures(nz, g)
    pb = cp.p_crit2 + (0.02 + 0.96 * frac) * (cp.p_crit1 - cp.p_crit2)
    sol = solve_nozzle(nz, pb, g)
    assert sol.regime == "shock" and nz.x_throat < sol.x_shock < nz.x_exit

    x = np.linspace(nz.x_in, nz.x_exit, 301)
    s = sol.profile(x)
    mdot = s["rho"] * s["u"] * s["A"]
    np.testing.assert_allclose(mdot, sol.mass_flow, rtol=1e-11)
    h0 = s["a"] ** 2 / (g - 1.0) + 0.5 * s["u"] ** 2
    np.testing.assert_allclose(h0, h0[0], rtol=1e-11)

    ent = entropy(s["rho"], s["p"], g)
    up, down = x < sol.x_shock, x > sol.x_shock
    np.testing.assert_allclose(ent[up], ent[0], atol=1e-11)
    np.testing.assert_allclose(ent[down], ent[-1], atol=1e-11)
    assert ent[-1] > ent[0]  # the shock produces entropy

    # stationary normal shock: mass, momentum and enthalpy continuous across x_s
    eps = 1e-10
    a, b = sol.profile([sol.x_shock - eps]), sol.profile([sol.x_shock + eps])
    for q in (lambda w: w["rho"] * w["u"], lambda w: w["rho"] * w["u"] ** 2 + w["p"]):
        assert q(b)[0] == pytest.approx(q(a)[0], rel=1e-7)
    assert b["p"][0] / a["p"][0] == pytest.approx(shock_p_ratio(sol.M1, g), rel=1e-7)


@settings(max_examples=100, deadline=None)
@given(st.floats(0.0, 1.0), st.floats(0.0, 1.0), gammas)
def test_shock_moves_downstream_as_pb_drops(f1: float, f2: float, g: float) -> None:
    nz = anderson_nozzle()
    cp = critical_pressures(nz, g)
    lo, hi = sorted((f1, f2))
    if hi - lo < 1e-3:
        return
    span = cp.p_crit1 - cp.p_crit2
    x_hi_pb = solve_nozzle(nz, cp.p_crit2 + (0.01 + 0.98 * hi) * span, g).x_shock
    x_lo_pb = solve_nozzle(nz, cp.p_crit2 + (0.01 + 0.98 * lo) * span, g).x_shock
    assert x_lo_pb > x_hi_pb


@settings(max_examples=100, deadline=None)
@given(st.floats(0.0, 1.0), gammas, st.booleans())
def test_shock_free_regimes_are_isentropic(frac: float, g: float, subsonic: bool) -> None:
    nz = anderson_nozzle()
    cp = critical_pressures(nz, g)
    pb = cp.p_crit1 + (0.01 + 0.98 * frac) * (1.0 - cp.p_crit1) if subsonic else (0.01 + 0.98 * frac) * cp.p_crit2
    sol = solve_nozzle(nz, pb, g)
    assert sol.regime == ("subsonic" if subsonic else "supersonic")
    s = sol.profile(np.linspace(nz.x_in, nz.x_exit, 101))
    np.testing.assert_allclose(entropy(s["rho"], s["p"], g), 0.0, atol=1e-11)
    np.testing.assert_allclose(s["rho"] * s["u"] * s["A"], sol.mass_flow, rtol=1e-11)
    assert (np.all(s["M"] < 1.0) if subsonic else s["M"][-1] > 1.0)
