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
