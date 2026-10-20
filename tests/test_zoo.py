"""Zoo members pass the sandbox and the hard constraints, and behave like the textbook says (Gate 1 sanity)."""

import jax.numpy as jnp
import numpy as np
import pytest

from schemeforge.arenas.euler1d import constraints, zoo
from schemeforge.arenas.euler1d.exact_riemann import solve_riemann
from schemeforge.arenas.euler1d.numerics import muscl
from schemeforge.arenas.euler1d.unsteady import solve_unsteady

LIMITERS = sorted(zoo.members("limiter"))
FLUXES = sorted(zoo.members("flux"))
RECONSTRUCTIONS = sorted(zoo.members("reconstruction"))
G = 1.4


def test_expected_members() -> None:
    assert LIMITERS == ["koren", "mc", "minmod", "superbee", "van_albada", "van_leer", "venkatakrishnan"]
    assert FLUXES == ["hll", "hllc", "rusanov"]  # Roe dropped at Gate 1 (fails positivity on R2)
    assert RECONSTRUCTIONS == ["first_order", "weno5z"]


@pytest.mark.parametrize("name", LIMITERS)
def test_limiter_hard_constraints(name) -> None:
    assert constraints.check_limiter(zoo.load("limiter", name)) == []


@pytest.mark.parametrize("name", LIMITERS)
def test_limiter_textbook_properties(name) -> None:
    phi = zoo.load("limiter", name)
    r = np.linspace(-3.0, 10.0, 1301)
    v = np.asarray(phi(jnp.asarray(r)))
    assert float(phi(jnp.asarray(1.0))) == pytest.approx(1.0, abs=1e-15)  # second order at r = 1
    assert np.all(v[r <= 0] == 0.0)
    pos = r > 0
    # Sweby's second-order TVD region: max(0, min(r, 1)) <= phi <= min(2r, 2) ... and phi <= superbee
    lo = np.minimum(r[pos], 1.0)
    hi = np.maximum(np.minimum(2 * r[pos], 1.0), np.minimum(r[pos], 2.0))
    assert np.all(v[pos] >= lo - 1e-14) and np.all(v[pos] <= hi + 1e-14)
    symmetric = np.allclose(v[pos] * 0 + np.asarray(phi(jnp.asarray(1.0 / r[pos]))) * r[pos], v[pos], atol=1e-12)
    assert symmetric == (name != "koren")


@pytest.mark.parametrize("name", FLUXES)
def test_flux_hard_constraints(name) -> None:
    assert constraints.check_flux(zoo.load("flux", name)) == []


def test_judge_default_flux_is_the_zoo_hllc() -> None:
    from schemeforge.arenas.euler1d.numerics import hllc

    assert hllc is zoo.load("flux", "hllc")


def riemann(WL, WR, n, t, flux, reconstruct):
    x = (np.arange(n) + 0.5) / n
    W0 = np.where((x < 0.5)[:, None], WL, WR)
    W = np.asarray(solve_unsteady(W0, 1.0 / n, t, G, reconstruct, flux=flux).W)
    return W, solve_riemann(WL, WR, G).sample(x, t, 0.5)


@pytest.mark.parametrize("name,exact", [("hllc", True), ("hll", False), ("rusanov", False)])
def test_stationary_contact(name, exact) -> None:
    """Gate 1: HLLC keeps the stationary contact R5 exactly, HLL and Rusanov smear it."""
    W, Wx = riemann((1.4, 0.0, 1.0), (1.0, 0.0, 1.0), 100, 2.0, zoo.load("flux", name),
                    muscl(zoo.load("limiter", "minmod")))
    err = np.max(np.abs(W - Wx))
    assert (err < 1e-12) if exact else (err > 1e-2), err


@pytest.mark.parametrize("name", FLUXES)
def test_positivity_on_123(name) -> None:
    """All zoo fluxes stay positive on the 123 problem (Roe, which does not, was dropped at Gate 1)."""
    W, _ = riemann((1.0, -2.0, 0.4), (1.0, 2.0, 0.4), 200, 0.15, zoo.load("flux", name),
                   muscl(zoo.load("limiter", "minmod")))
    assert constraints.check_run(W) == []


def test_weno5z_is_high_order_on_the_smooth_wave() -> None:
    rec = zoo.load("reconstruction", "weno5z")
    errs = []
    for n in (25, 50, 100):
        x = (np.arange(n) + 0.5) / n
        W0 = np.stack([1.0 + 0.2 * np.sin(2 * np.pi * x), np.ones(n), np.ones(n)], axis=1)
        W = np.asarray(solve_unsteady(W0, 1.0 / n, 1.0, G, rec, bc="periodic").W)
        errs.append(np.mean(np.abs(W[:, 0] - W0[:, 0])))
    order = np.log2(errs[1] / errs[2])
    assert order > 2.8, (errs, order)  # SSP-RK3 at fixed CFL caps the observed order near 3


def test_weno5z_sod_is_sharp_and_bounded() -> None:
    W, Wx = riemann((1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 200, 0.2, zoo.load("flux", "hllc"),
                    zoo.load("reconstruction", "weno5z"))
    assert constraints.check_run(W) == []
    assert np.mean(np.abs(W[:, 0] - Wx[:, 0])) < 3e-3
