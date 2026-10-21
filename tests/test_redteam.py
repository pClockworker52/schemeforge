"""Red-team regressions (docs/judge/redteam.md): each attack that got through judge v1.0 must now be caught."""

import jax.numpy as jnp
import numpy as np

from schemeforge.arenas.euler1d import constraints, zoo
from schemeforge.arenas.euler1d.numerics import elementwise, rowwise
from schemeforge.core.sandbox import validate_source


def _superbee(r):
    return jnp.maximum(0.0, jnp.maximum(jnp.minimum(2.0 * r, 1.0), jnp.minimum(r, 2.0)))


def _van_albada(r):
    rp = jnp.maximum(r, 0.0)
    return rp * (rp + 1.0) / (rp * rp + 1.0)


def test_s01_size_switch_is_rejected() -> None:
    def phi(r):
        return _superbee(r) if r.size > 500 else _van_albada(r)

    assert any("not elementwise" in v for v in constraints.check_limiter(phi))


def test_s02_statistics_switch_is_rejected() -> None:
    def phi(r):
        return jnp.where(jnp.mean(r == 0.0) > 0.2, _superbee(r), _van_albada(r))

    assert any("not elementwise" in v for v in constraints.check_limiter(phi))


def test_f01_flux_size_switch_is_rejected() -> None:
    hllc, hll = zoo.load("flux", "hllc"), zoo.load("flux", "hll")

    def flux(UL, UR, g):
        return hllc(UL, UR, g) if UL.shape[0] > 150 else hll(UL, UR, g)

    assert any("not row-wise" in v for v in constraints.check_flux(flux))


def test_runs_never_show_the_batch() -> None:
    # a size switch that slipped past the checks would still see one item at a time in a run
    def phi(r):
        return _superbee(r) if r.size > 500 else _van_albada(r)

    r = jnp.asarray(np.resize(constraints.limiter_probes(), (204, 3)))
    np.testing.assert_array_equal(np.asarray(elementwise(phi)(r)), np.asarray(_van_albada(r)))
    hllc = zoo.load("flux", "hllc")
    UL, UR = (jnp.asarray(np.resize(u, (201, 3))) for u in constraints.flux_probes())
    np.testing.assert_allclose(np.asarray(rowwise(hllc)(UL, UR, 1.4)), np.asarray(hllc(UL, UR, 1.4)), rtol=1e-13)


def test_s08_stop_gradient_is_rejected() -> None:
    src = "from jax import lax\nimport jax.numpy as jnp\n\ndef phi(r):\n    return r + lax.stop_gradient(0.0 * r)\n"
    assert "forbidden-attr" in validate_source(src).rules
