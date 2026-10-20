"""Metrics, hard constraints and metamorphic measurements on known schemes."""

import jax.numpy as jnp
import numpy as np
import pytest

from schemeforge.arenas.euler1d import constraints, metamorphic, metrics
from schemeforge.arenas.euler1d.exact_nozzle import anderson_nozzle, solve_nozzle
from schemeforge.arenas.euler1d.exact_riemann import solve_riemann
from schemeforge.arenas.euler1d.numerics import first_order, hllc, muscl, physical_flux
from schemeforge.arenas.euler1d.steady import default_operator, make_grid, solve_implicit
from schemeforge.arenas.euler1d.unsteady import solve_unsteady

G = 1.4
SOD = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))


def minmod(r):
    return jnp.maximum(0.0, jnp.minimum(1.0, r))


def superbee(r):
    return jnp.maximum(0.0, jnp.maximum(jnp.minimum(2.0 * r, 1.0), jnp.minimum(r, 2.0)))


def koren(r):
    return jnp.maximum(0.0, jnp.minimum(jnp.minimum(2.0 * r, (1.0 + 2.0 * r) / 3.0), 2.0))


def sod_metrics(reconstruct, n=200):
    x = (np.arange(n) + 0.5) / n
    W0 = np.where((x < 0.5)[:, None], SOD[0], SOD[1])
    W = np.asarray(solve_unsteady(W0, 1.0 / n, 0.2, G, reconstruct).W)
    return metrics.riemann_metrics(x, W, solve_riemann(*SOD, G), 0.5, 0.2, (0.0, 1.0), 1.0 / n)


def test_exact_solution_scores_perfectly() -> None:
    n = 200
    x = (np.arange(n) + 0.5) / n
    sol = solve_riemann(*SOD, G)
    m = metrics.riemann_metrics(x, sol.sample(x, 0.2, 0.5), sol, 0.5, 0.2, (0.0, 1.0), 1.0 / n)
    assert m["l1_smooth"] == 0.0 and m["overshoot"] == 0.0 and m["tv_increase"] == 0.0
    assert m["shock_width"] < 1.0 and m["contact_width"] < 1.0


def test_sod_ranking_superbee_sharpest_minmod_most_diffusive() -> None:
    fo, mm, sb = sod_metrics(first_order), sod_metrics(muscl(minmod)), sod_metrics(muscl(superbee))
    assert sb["contact_width"] < mm["contact_width"] < fo["contact_width"]
    assert sb["shock_width"] <= mm["shock_width"] <= fo["shock_width"]
    assert fo["l1_smooth"] > mm["l1_smooth"]


def test_riemann_jumps_of_sod() -> None:
    sol = solve_riemann(*SOD, G)
    jumps = metrics.riemann_jumps(sol, 0.5, 0.2, (0.0, 1.0))
    assert [j.kind for j in jumps] == ["contact", "shock"]
    contact, shock = jumps
    assert contact.x == pytest.approx(0.5 + sol.u_star * 0.2)
    assert contact.lo < contact.x < contact.hi == pytest.approx(0.5 * (contact.x + shock.x))
    assert (shock.a, shock.b) == (sol.p_star, 0.1)


def test_jump_width_of_a_linear_ramp() -> None:
    x = np.linspace(0.0, 1.0, 101)
    q = np.clip((x - 0.4) / 0.2, 0.0, 1.0)  # ramp over 20 cells of 0.01
    assert metrics.jump_width(x, q, 0.0, 1.0, 0.01) == pytest.approx(18.0)


def test_nozzle_metrics_on_n1() -> None:
    nz = anderson_nozzle()
    grid = make_grid(nz, 120)
    exact = solve_nozzle(nz, 0.6784, G)
    r = solve_implicit(grid, 0.6784, G, default_operator(muscl(minmod)))
    m = metrics.nozzle_metrics(grid.x, r.W, grid.A, exact, grid.dx)
    assert m["shock_pos_err"] < 1.0
    assert 0.0 < m["shock_width"] < 4.0  # steady shocks are captured with about one intermediate cell
    assert m["mdot_var"] < 0.05 and m["h0_var"] < 0.05
    prof = exact.profile(grid.x)
    W_ex = np.stack([prof["rho"], prof["u"], prof["p"]], axis=1)
    perfect = metrics.nozzle_metrics(grid.x, W_ex, grid.A, exact, grid.dx)
    assert perfect["mdot_var"] < 1e-12 and perfect["entropy_spurious"] < 1e-12 and perfect["l1_smooth"] == 0.0


def test_wall_force_and_roughness() -> None:
    nz = anderson_nozzle()
    grid = make_grid(nz, 120)
    x_from = grid.x_face[int(np.argmax(grid.x > nz.x_throat))]
    pbs = np.linspace(0.62, 0.72, 5)
    J_ex = np.array([metrics.wall_force_exact(solve_nozzle(nz, pb, G), nz, x_from) for pb in pbs])
    # the exact profile sampled at cell centres gives a nearly exact discrete J away from the shock cell
    J_num = []
    for pb in pbs:
        prof = solve_nozzle(nz, pb, G).profile(grid.x)
        J_num.append(metrics.wall_force_numerical(np.stack([prof["rho"], prof["u"], prof["p"]], 1),
                                                  grid.A_face, grid.x, nz.x_throat))
    assert np.allclose(J_num, J_ex, rtol=2e-2)
    assert metrics.roughness(J_ex, J_ex) == 0.0
    assert metrics.roughness(J_ex + 0.01 * np.array([0, 1, 0, 1, 0]), J_ex) > 0.1


# --- hard constraints ---------------------------------------------------------------------------------------
@pytest.mark.parametrize("phi", [minmod, superbee, koren, lambda r: (r + jnp.abs(r)) / (1 + jnp.abs(r))])
def test_zoo_like_limiters_pass(phi) -> None:
    assert constraints.check_limiter(phi) == []


def test_bad_limiters_fail() -> None:
    assert any("finite" in v for v in constraints.check_limiter(lambda r: 1.0 / r))
    assert any("shape" in v for v in constraints.check_limiter(lambda r: jnp.sum(r)))
    assert any("pointwise" in v for v in constraints.check_limiter(lambda r: r * 0 + jnp.mean(r)))


def test_hllc_passes_flux_constraints() -> None:
    assert constraints.check_flux(hllc) == []


def test_bad_fluxes_fail() -> None:
    def inconsistent(UL, UR, g):
        return 0.5 * (physical_flux(UL, g) + physical_flux(UR, g)) - 0.5 * (UR - UL) + 1e-6

    def asymmetric(UL, UR, g):  # upwinds with the left state only
        return physical_flux(UL, g) + 0.0 * UR

    assert any("consistency" in v for v in constraints.check_flux(inconsistent))
    assert any("mirror" in v for v in constraints.check_flux(asymmetric))


def test_run_constraints() -> None:
    assert constraints.check_run(np.ones((5, 3))) == []
    assert constraints.check_run(np.array([[1.0, 0.0, -1.0]])) == ["negative or zero pressure"]
    assert constraints.check_run(np.array([[np.nan, 0.0, 1.0]])) == ["non-finite state (NaN or Inf)"]


# --- metamorphic ------------------------------------------------------------------------------------------------
def _sod_problem(n=200):
    x = (np.arange(n) + 0.5) / n
    return np.where((x < 0.5)[:, None], SOD[0], SOD[1]), 1.0 / n


@pytest.mark.parametrize("phi,symmetric", [(minmod, True), (superbee, True), (koren, False)])
def test_mirror_symmetry_measures_limiter_symmetry(phi, symmetric) -> None:
    rec = muscl(phi)

    def run(W0, dx, t, g):
        return np.asarray(solve_unsteady(W0, dx, t, g, rec).W)

    W0, dx = _sod_problem()
    err = metamorphic.mirror_error(run, W0, dx, 0.2, G)
    assert (err < 1e-12) if symmetric else (err > 1e-6), err


def test_scaling_is_exact_and_galilean_is_not() -> None:
    rec = muscl(minmod)

    def run(W0, dx, t, g):
        return np.asarray(solve_unsteady(W0, dx, t, g, rec).W)

    W0, dx = _sod_problem()
    W = run(W0, dx, 0.2, G)
    assert metamorphic.scaling_error(run, W0, dx, 0.2, G, W=W) < 1e-12
    assert 1e-6 < metamorphic.galilean_error(run, W0, dx, 0.2, G, W=W) < 0.5
