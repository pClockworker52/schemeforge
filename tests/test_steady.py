"""Steady quasi-1D nozzle solver: Jacobian colouring, balance at rest, convergence to exact solutions."""

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from schemeforge.arenas.euler1d.exact_nozzle import anderson_nozzle, solve_nozzle
from schemeforge.arenas.euler1d.numerics import first_order, muscl, prim_to_cons
from schemeforge.arenas.euler1d.steady import (
    colored_jacobian,
    default_operator,
    initial_state,
    make_grid,
    rhs,
    solve_explicit,
    solve_implicit,
)

G = 1.4
NZ = anderson_nozzle()
VAN_LEER = default_operator(muscl(lambda r: (r + jnp.abs(r)) / (1.0 + jnp.abs(r))))
MINMOD = default_operator(muscl(lambda r: jnp.maximum(0.0, jnp.minimum(1.0, r))))
FIRST = default_operator(first_order)


@pytest.mark.parametrize("op", [FIRST, MINMOD, VAN_LEER], ids=["first", "minmod", "vanleer"])
def test_colored_jacobian_is_exact(op) -> None:
    n = 24
    grid = make_grid(NZ, n)
    A, Af = jnp.asarray(grid.A), jnp.asarray(grid.A_face)
    U = initial_state(grid, 0.6784, G) * (1.0 + 0.05 * jnp.sin(jnp.arange(3 * n).reshape(n, 3)))
    f = lambda v: rhs(v.reshape(n, 3), A, Af, grid.dx, 0.6784, G, op).reshape(-1)  # noqa: E731
    np.testing.assert_allclose(colored_jacobian(f, U.reshape(-1), n), jax.jacfwd(f)(U.reshape(-1)), atol=1e-12)


def test_flow_at_rest_is_balanced() -> None:
    grid = make_grid(NZ, 60)
    W = jnp.tile(jnp.array([1.0, 0.0, 1.0]), (60, 1))
    U = prim_to_cons(W, G) * jnp.asarray(grid.A)[:, None]
    dU = rhs(U, jnp.asarray(grid.A), jnp.asarray(grid.A_face), grid.dx, 1.0, G, VAN_LEER)
    assert float(jnp.max(jnp.abs(dU))) < 1e-12


def shock_cell_error(W: np.ndarray, grid, exact) -> float:
    """Distance in cells between the numerical shock (p crossing the mid jump pressure) and the exact one."""
    a = exact.profile([exact.x_shock - 1e-9])["p"][0]
    b = exact.profile([exact.x_shock + 1e-9])["p"][0]
    mid = 0.5 * (a + b)
    i_min = int(np.argmin(W[:, 2]))  # the shock compresses the flow downstream of the pressure minimum
    i = i_min + int(np.argmax(W[i_min:, 2] > mid))
    x_num = np.interp(mid, W[i - 1 : i + 1, 2], grid.x[i - 1 : i + 1])
    return abs(x_num - exact.x_shock) / grid.dx


def test_explicit_first_order_converges_on_N1() -> None:
    grid = make_grid(NZ, 120)
    exact = solve_nozzle(NZ, 0.6784, G)
    r = solve_explicit(grid, 0.6784, G, FIRST)
    assert r.converged and not r.failed
    assert shock_cell_error(r.W, grid, exact) < 1.0


def test_implicit_van_leer_converges_on_N1() -> None:
    grid = make_grid(NZ, 120)
    exact = solve_nozzle(NZ, 0.6784, G)
    r = solve_implicit(grid, 0.6784, G, VAN_LEER)
    assert r.converged and r.iterations < 300
    assert shock_cell_error(r.W, grid, exact) < 1.0
    prof = exact.profile(grid.x)
    smooth = np.abs(grid.x - exact.x_shock) > 5 * grid.dx
    assert np.mean(np.abs(r.W[smooth, 2] - prof["p"][smooth])) < 2e-3


def test_both_solvers_agree_on_supersonic_N3() -> None:
    grid = make_grid(NZ, 120)
    prof = solve_nozzle(NZ, 0.01, G).profile(grid.x)
    re, ri = solve_explicit(grid, 0.01, G, VAN_LEER), solve_implicit(grid, 0.01, G, VAN_LEER)
    assert re.converged and ri.converged
    np.testing.assert_allclose(re.W, ri.W, rtol=1e-9, atol=1e-11)
    assert np.mean(np.abs(ri.W[:, 2] - prof["p"])) < 1e-3
