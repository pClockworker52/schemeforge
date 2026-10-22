"""Judge v1.3 reconstruction slot: zoo members pass the hard constraints, and reconstructions that see more than the
cells around an interface are rejected (the batch-visibility hole v1.1 closed for limiters and fluxes)."""

import jax.numpy as jnp
import numpy as np
import pytest

from schemeforge.arenas.euler1d import constraints, zoo
from schemeforge.arenas.euler1d.evaluate import slot_constraints, slot_scheme
from schemeforge.arenas.euler1d.numerics import muscl, stencilwise

FIRST, WENO = zoo.load("reconstruction", "first_order"), zoo.load("reconstruction", "weno5z")
SHARP = muscl(zoo.load("limiter", "superbee"))
SMOOTH = muscl(zoo.load("limiter", "van_albada"))


@pytest.mark.parametrize("name", sorted(zoo.members("reconstruction")))
def test_zoo_reconstructions_pass(name) -> None:
    assert constraints.check_reconstruction(zoo.load("reconstruction", name)) == []


@pytest.mark.parametrize("limiter", ["minmod", "van_leer", "superbee"])
def test_muscl_with_zoo_limiters_passes(limiter) -> None:
    assert constraints.check_reconstruction(muscl(zoo.load("limiter", limiter))) == []


def test_slot_wiring() -> None:
    assert slot_constraints(WENO, "reconstruction") == []
    W = jnp.asarray(constraints.reconstruction_probes()[3])
    rec, _ = slot_scheme(WENO, "reconstruction")
    for a, b in zip(rec(W, 1.4), WENO(W, 1.4), strict=True):
        np.testing.assert_allclose(np.asarray(a), np.asarray(b), rtol=1e-13)


def _not_local(rec) -> bool:
    return any("not local" in v for v in constraints.check_reconstruction(rec))


def test_grid_size_switch_is_rejected() -> None:
    # sharp on Riemann grids (N = 200, 400), smooth on nozzle grids (N = 120): red team s01 for this slot
    def rec(W, g):
        return SHARP(W, g) if W.shape[0] > 150 else SMOOTH(W, g)

    assert _not_local(rec)


def test_statistics_switch_is_rejected() -> None:
    def rec(W, g):
        a, b = SHARP(W, g), SMOOTH(W, g)
        big = jnp.max(W[:, 2]) / jnp.min(W[:, 2]) > 50.0
        return jnp.where(big, a[0], b[0]), jnp.where(big, a[1], b[1])

    assert _not_local(rec)


def test_position_dependence_is_rejected() -> None:
    # extra dissipation only in a band of interfaces (red team s05)
    def rec(W, g):
        a, b = SHARP(W, g), FIRST(W, g)
        band = ((jnp.arange(W.shape[0] - 5) > 40) & (jnp.arange(W.shape[0] - 5) < 70))[:, None]
        return jnp.where(band, b[0], a[0]), jnp.where(band, b[1], a[1])

    assert _not_local(rec)


def test_wide_stencil_is_rejected() -> None:
    # uses the cell three to the left of the left state's cell (one beyond the window)
    def rec(W, g):
        WL, WR = FIRST(W, g)
        far = jnp.roll(W, 3, axis=0)[2:-3]
        return WL + 0.1 * (WL - far), WR

    assert _not_local(rec)


def test_constant_state_must_be_reproduced() -> None:
    def rec(W, g):
        WL, WR = FIRST(W, g)
        return WL * (1.0 + 1e-6), WR

    assert "reconstruct does not reproduce a constant state" in constraints.check_reconstruction(rec)


def test_shape_and_finiteness() -> None:
    assert "shapes" in constraints.check_reconstruction(lambda W, g: (W, W))[0]
    nan = constraints.check_reconstruction(lambda W, g: (W[2:-3] * jnp.nan, W[3:-2]))
    assert "reconstruct is not finite on admissible cell values" in nan


def test_runs_never_show_the_grid() -> None:
    # a size switch that slipped past the checks would still see one 6-cell window at a time in a run
    def rec(W, g):
        return SHARP(W, g) if W.shape[0] > 150 else SMOOTH(W, g)

    W = jnp.asarray(constraints.reconstruction_probes()[-2])
    assert W.shape[0] > 150
    for a, b in zip(stencilwise(rec)(W, 1.4), SMOOTH(W, 1.4), strict=True):
        np.testing.assert_allclose(np.asarray(a), np.asarray(b), rtol=1e-13)


# --- THINC/BVD zoo member -------------------------------------------------------------------------------------
def test_thinc_bvd_is_sharp_on_a_contact() -> None:
    from schemeforge.arenas.euler1d.unsteady import solve_unsteady

    # an isolated contact moving right: rho jumps 1 -> 0.125 at u = 1, p = 1 (exact: pure translation)
    # measured: THINC/BVD 2 cells, WENO5-Z 4, van Albada MUSCL 9 (all without over- or undershoot)
    n, t = 100, 0.6
    x = (np.arange(n) + 0.5) / n
    W0 = np.stack([np.where(x < 0.2, 1.0, 0.125), np.ones(n), np.ones(n)], axis=1)

    def width(rec) -> int:
        rho = np.asarray(solve_unsteady(W0, 1.0 / n, t, 1.4, stencilwise(rec)).W)[:, 0]
        assert 0.125 - 1e-9 <= rho.min() and rho.max() <= 1.0 + 1e-9
        frac = (rho - 0.125) / 0.875
        return int(np.sum((frac > 0.05) & (frac < 0.95)))

    assert width(zoo.load("reconstruction", "thinc_bvd")) <= 2 < width(WENO) < width(SMOOTH)


# --- reconstruction_stateful -----------------------------------------------------------------------------------
STATEFUL = sorted(zoo.members("reconstruction_stateful"))


@pytest.mark.parametrize("name", STATEFUL)
def test_stateful_zoo_passes(name) -> None:
    assert constraints.check_reconstruction_stateful(zoo.load("reconstruction_stateful", name)) == []


def test_stateful_frozen_matches_the_limiter_stateful_zoo() -> None:
    # the same method in both slots: identical faces and identical states on the cells the judge keeps
    from schemeforge.arenas.euler1d.numerics import elementwise_stateful, muscl_stateful, stencilwise_stateful

    W = jnp.asarray(constraints.reconstruction_probes()[4])
    m = W.shape[0] - 5
    S = jnp.asarray(np.random.default_rng(0).choice([0.0, 998.0, 999.0, 1000.0, 1001.4], size=(W.shape[0] - 2, 3)))
    a = stencilwise_stateful(zoo.load("reconstruction_stateful", "muscl_van_leer_frozen"))(W, 1.4, S)
    b = muscl_stateful(elementwise_stateful(zoo.load("limiter_stateful", "van_leer_frozen")))(W, 1.4, S)
    for x, y in zip(a[:2], b[:2], strict=True):
        np.testing.assert_allclose(np.asarray(x), np.asarray(y), rtol=1e-13, atol=0.0)
    np.testing.assert_allclose(np.asarray(a[2])[1 : m + 2], np.asarray(b[2])[1 : m + 2], rtol=1e-13, atol=0.0)


def _stateful_not_local(rec) -> bool:
    return any("not local" in v for v in constraints.check_reconstruction_stateful(rec))


def test_stateful_grid_size_switch_is_rejected() -> None:
    base = zoo.load("reconstruction_stateful", "muscl_van_leer")

    def rec(W, g, s):
        WL, WR, s_new = base(W, g, s)
        return (WL, WR, s_new + 1.0) if W.shape[0] > 150 else (WL, WR, s_new)

    assert _stateful_not_local(rec)


def test_stateful_state_from_far_cells_is_rejected() -> None:
    # the new state of a cell copies the state three cells to the right (outside the window's 4 state rows)
    base = zoo.load("reconstruction_stateful", "muscl_van_leer")

    def rec(W, g, s):
        WL, WR, _ = base(W, g, s)
        return WL, WR, jnp.roll(s, -3, axis=0) + 1.0

    assert _stateful_not_local(rec)


def test_stateful_shapes_and_finiteness() -> None:
    base = zoo.load("reconstruction_stateful", "muscl_van_leer")
    assert "shapes" in constraints.check_reconstruction_stateful(lambda W, g, s: (*base(W, g, s)[:2], s[1:]))[0]
    bad = constraints.check_reconstruction_stateful(lambda W, g, s: (*base(W, g, s)[:2], s / (s - s)))
    assert "reconstruct_s is not finite (states or new state) on the probes" in bad


def test_stateful_slot_wiring() -> None:
    from schemeforge.arenas.euler1d.numerics import NG

    frozen = zoo.load("reconstruction_stateful", "muscl_van_leer_frozen")
    assert slot_constraints(frozen, "reconstruction_stateful") == []
    rec, _ = slot_scheme(frozen, "reconstruction_stateful")
    assert getattr(rec, "stateful", False)
    W = jnp.asarray(constraints.reconstruction_probes()[2])
    S = jnp.zeros((W.shape[0] - 2, 3))
    WL, WR, S_new = rec(W, 1.4, S)
    assert WL.shape == (W.shape[0] - 2 * NG + 1, 3) and S_new.shape == S.shape
    # one step counted on the cells the judge keeps, untouched elsewhere
    assert float(S_new[1, 0]) == 1.0 and float(S_new[0, 0]) == 0.0 and float(S_new[-1, 0]) == 0.0
