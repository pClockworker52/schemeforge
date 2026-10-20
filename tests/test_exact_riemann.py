"""Exact Riemann solver: Appendix H values and property tests (PLAN §9.2, §9.10)."""

import numpy as np
import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from schemeforge.arenas.euler1d.exact_riemann import VacuumError, solve_riemann
from schemeforge.arenas.euler1d.gas import GAMMA_STRESS, GAMMAS, entropy, euler_flux, prim_to_cons, sound_speed

# Appendix H, gamma = 1.4: (WL, WR, p*, u*, absolute tolerances = half a unit in the last quoted digit)
TORO = [
    ("test1-sod", (1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 0.30313, 0.92745, 5e-6, 5e-6),
    ("test2-123", (1.0, -2.0, 0.4), (1.0, 2.0, 0.4), 0.00189, 0.0, 5e-6, 1e-12),
    ("test3", (1.0, 0.0, 1000.0), (1.0, 0.0, 0.01), 460.894, 19.5975, 5e-4, 5e-5),
    ("test4", (1.0, 0.0, 0.01), (1.0, 0.0, 100.0), 46.0950, -6.19633, 5e-5, 5e-6),
    # Recomputed values; Toro's table (1691.64, 8.68975) differs because these inputs are rounded to 6 digits.
    ("test5", (5.99924, 19.5975, 460.894), (5.99242, -6.19633, 46.0950), 1691.65, 8.68977, 5e-3, 5e-6),
]


@pytest.mark.parametrize("WL,WR,p_star,u_star,tol_p,tol_u", [t[1:] for t in TORO], ids=[t[0] for t in TORO])
def test_toro_star_states(WL, WR, p_star, u_star, tol_p, tol_u) -> None:
    sol = solve_riemann(WL, WR, 1.4)
    assert sol.p_star == pytest.approx(p_star, abs=tol_p)
    assert sol.u_star == pytest.approx(u_star, abs=tol_u)


def test_vacuum_is_rejected() -> None:
    with pytest.raises(VacuumError):
        solve_riemann((1.0, -10.0, 0.4), (1.0, 10.0, 0.4), 1.4)


def test_sod_wave_pattern() -> None:
    sol = solve_riemann((1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 1.4)
    assert sol.left.kind == "rarefaction" and sol.right.kind == "shock"
    W = sol.sample_xi([-10.0, 10.0])
    np.testing.assert_allclose(W[0], (1.0, 0.0, 1.0))
    np.testing.assert_allclose(W[1], (0.125, 0.0, 0.1))


# --- property tests ----------------------------------------------------------------------------------------
pos = st.floats(-1.0, 1.0).map(lambda e: 10.0**e)  # densities 0.1 .. 10
press = st.floats(-3.0, 3.0).map(lambda e: 10.0**e)  # pressures 1e-3 .. 1e3
vel = st.floats(-3.0, 3.0)
gammas = st.sampled_from([*GAMMAS, GAMMA_STRESS])
states = st.tuples(pos, vel, press)


def _solve(WL, WR, g):
    aL, aR = sound_speed(WL[0], WL[2], g), sound_speed(WR[0], WR[2], g)
    assume(2.0 / (g - 1.0) * (aL + aR) > (WR[1] - WL[1]) * 1.01)
    return solve_riemann(WL, WR, g)


@settings(max_examples=300, deadline=None)
@given(states, states, gammas)
def test_rankine_hugoniot_across_shocks(WL, WR, g) -> None:
    sol = _solve(WL, WR, g)
    for wave, W, rho_star in ((sol.left, WL, sol.rho_star_L), (sol.right, WR, sol.rho_star_R)):
        if wave.kind != "shock":
            continue
        S = wave.speeds[0]
        U0, U1 = prim_to_cons(W, g), prim_to_cons((rho_star, sol.u_star, sol.p_star), g)
        F0, F1 = euler_flux(U0, g), euler_flux(U1, g)
        scale = np.max(np.abs(np.concatenate([F0, F1, S * U0, S * U1])))
        np.testing.assert_allclose(S * (U1 - U0), F1 - F0, rtol=0, atol=1e-11 * scale)


@settings(max_examples=300, deadline=None)
@given(states, states, gammas)
def test_star_region_and_rarefactions(WL, WR, g) -> None:
    sol = _solve(WL, WR, g)
    for wave, W, rho_star in ((sol.left, WL, sol.rho_star_L), (sol.right, WR, sol.rho_star_R)):
        if wave.kind != "rarefaction":
            continue
        head, tail = wave.speeds
        xi = np.linspace(head, tail, 9)[1:-1]
        Wf = sol.sample_xi(xi)
        # isentropic fan with constant Riemann invariant u -/+ 2a/(g-1)
        s0 = entropy(W[0], W[2], g)
        np.testing.assert_allclose(entropy(Wf[:, 0], Wf[:, 2], g), s0, rtol=0, atol=1e-10 * max(1.0, abs(s0)))
        k = -wave.side * 2.0 / (g - 1.0)
        J_fan = Wf[:, 1] + k * sound_speed(Wf[:, 0], Wf[:, 2], g)
        np.testing.assert_allclose(J_fan, W[1] + k * sound_speed(W[0], W[2], g), rtol=1e-11, atol=1e-11)
        # the fan joins both neighbouring states continuously
        eps = 1e-9 * max(1.0, abs(tail - head))
        star_side = sol.sample_xi([tail - wave.side * eps])[0]  # the star region lies towards the contact
        tol = 1e-6 * (1.0 + abs(sol.u_star) + abs(W[1]))
        np.testing.assert_allclose(star_side, (rho_star, sol.u_star, sol.p_star), rtol=1e-6, atol=tol)
        outer_side = sol.sample_xi([head + wave.side * eps])[0]
        np.testing.assert_allclose(outer_side, W, rtol=1e-6, atol=tol)


@settings(max_examples=200, deadline=None)
@given(states, states, gammas)
def test_mirror_symmetry(WL, WR, g) -> None:
    sol = _solve(WL, WR, g)
    mir = solve_riemann((WR[0], -WR[1], WR[2]), (WL[0], -WL[1], WL[2]), g)
    assert mir.p_star == pytest.approx(sol.p_star, rel=1e-12)
    assert mir.u_star == pytest.approx(-sol.u_star, rel=1e-12, abs=1e-12 * (abs(WL[1]) + abs(WR[1]) + 1.0))
    xi = np.linspace(-20.0, 20.0, 41) + 0.0123
    W, Wm = sol.sample_xi(xi), mir.sample_xi(-xi)
    np.testing.assert_allclose(Wm[:, [0, 2]], W[:, [0, 2]], rtol=1e-10)
    np.testing.assert_allclose(Wm[:, 1], -W[:, 1], rtol=1e-10, atol=1e-10)
