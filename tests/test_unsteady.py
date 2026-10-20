"""Unsteady solver checks: convergence to exact Riemann solutions, smooth-wave order, conservation, R5."""

import jax.numpy as jnp
import numpy as np
import pytest

from schemeforge.arenas.euler1d.exact_riemann import solve_riemann
from schemeforge.arenas.euler1d.numerics import first_order, muscl
from schemeforge.arenas.euler1d.unsteady import solve_unsteady

G = 1.4


def minmod(r):
    return jnp.maximum(0.0, jnp.minimum(1.0, r))


def van_leer(r):
    return (r + jnp.abs(r)) / (1.0 + jnp.abs(r))


def unlimited(r):
    return jnp.ones_like(r)


MINMOD, VAN_LEER, UNLIMITED = muscl(minmod), muscl(van_leer), muscl(unlimited)


def riemann_run(WL, WR, n, t_end, reconstruct, x0=0.5):
    x = (np.arange(n) + 0.5) / n
    W0 = np.where((x < x0)[:, None], WL, WR)
    res = solve_unsteady(W0, 1.0 / n, t_end, G, reconstruct)
    exact = solve_riemann(WL, WR, G).sample(x, t_end, x0)
    return np.asarray(res.W), exact


@pytest.mark.parametrize("reconstruct", [first_order, MINMOD, VAN_LEER], ids=["first-order", "minmod", "van-leer"])
def test_sod_converges(reconstruct) -> None:
    errs = []
    for n in (100, 200, 400):
        W, exact = riemann_run((1.0, 0.0, 1.0), (0.125, 0.0, 0.1), n, 0.2, reconstruct)
        errs.append(np.mean(np.abs(W[:, 0] - exact[:, 0])))
    assert errs[0] > errs[1] > errs[2]
    assert errs[2] < 0.01


def test_sod_second_order_is_sharper() -> None:
    e = {}
    for name, rec in (("fo", first_order), ("vl", VAN_LEER)):
        W, exact = riemann_run((1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 200, 0.2, rec)
        e[name] = np.mean(np.abs(W[:, 0] - exact[:, 0]))
    assert e["vl"] < 0.6 * e["fo"]


def smooth_wave_error(n, reconstruct):
    x = (np.arange(n) + 0.5) / n
    W0 = np.stack([1.0 + 0.2 * np.sin(2 * np.pi * x), np.ones(n), np.ones(n)], axis=1)
    res = solve_unsteady(W0, 1.0 / n, 1.0, G, reconstruct, bc="periodic")
    return np.mean(np.abs(np.asarray(res.W)[:, 0] - W0[:, 0])), res


@pytest.mark.parametrize("reconstruct,lo,hi", [(first_order, 0.8, 1.2), (UNLIMITED, 1.8, 2.2), (VAN_LEER, 1.5, 2.2)],
                         ids=["first-order", "unlimited", "van-leer"])
def test_smooth_wave_order(reconstruct, lo, hi) -> None:
    e1, _ = smooth_wave_error(50, reconstruct)
    e2, _ = smooth_wave_error(200, reconstruct)
    order = np.log(e1 / e2) / np.log(4.0)
    assert lo < order < hi, order


def test_periodic_run_conserves_mass_momentum_energy() -> None:
    n = 100
    x = (np.arange(n) + 0.5) / n
    W0 = np.stack([1.0 + 0.2 * np.sin(2 * np.pi * x), 1.0 + 0.1 * np.cos(2 * np.pi * x), np.ones(n)], axis=1)
    from schemeforge.arenas.euler1d.numerics import prim_to_cons

    res = solve_unsteady(W0, 1.0 / n, 0.5, G, VAN_LEER, bc="periodic")
    np.testing.assert_allclose(
        np.sum(prim_to_cons(res.W, G), axis=0), np.sum(prim_to_cons(jnp.asarray(W0), G), axis=0), rtol=1e-13
    )


def test_hllc_keeps_stationary_contact_exactly() -> None:
    """R5: rho_L = 1.4, rho_R = 1, u = 0, p = 1 must not move or smear with HLLC."""
    W, exact = riemann_run((1.4, 0.0, 1.0), (1.0, 0.0, 1.0), 100, 1.0, VAN_LEER)
    np.testing.assert_allclose(W, exact, atol=1e-13)
