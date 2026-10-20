"""Held-out families: deterministic, admissible, within the ranges of PLAN §9.5. Uses a test seed only."""

import numpy as np
import pytest

from schemeforge.arenas.euler1d import families
from schemeforge.arenas.euler1d.exact_nozzle import solve_nozzle
from schemeforge.arenas.euler1d.exact_riemann import solve_riemann

SEED = "test-seed-0123456789abcdef"  # never the real one


def test_instances_are_deterministic_and_seed_dependent() -> None:
    a = families.promo_suite(SEED, {"RF1": 3, "NF1": 2})
    b = families.promo_suite(SEED, {"RF1": 3, "NF1": 2})
    c = families.promo_suite(SEED + "x", {"RF1": 3, "NF1": 2})
    assert a == b and a != c
    assert families.seed_fingerprint(SEED) != families.seed_fingerprint(SEED + "x")
    assert SEED not in families.seed_fingerprint(SEED)


def test_rf1_ranges() -> None:
    for i in range(30):
        c = families.rf1(SEED, i)
        rp = max(c.left[2], c.right[2]) / min(c.left[2], c.right[2])
        assert 10**0.5 <= rp <= 10**5 and 0.1 <= c.right[0] / c.left[0] <= 10
        assert c.gamma in families.ALL_GAMMAS
        solve_riemann(c.left, c.right, c.gamma)  # no vacuum


def test_rf2_is_a_single_slow_shock() -> None:
    for i in range(10):
        c = families.rf2(SEED, i)
        sol = solve_riemann(c.left, c.right, c.gamma)
        assert sol.right.kind == "shock"
        vmax = max(abs(c.left[1]) + (c.gamma * c.left[2] / c.left[0]) ** 0.5,
                   abs(c.right[1]) + (c.gamma * c.right[2] / c.right[0]) ** 0.5)
        assert 0.0 <= sol.right.speeds[0] <= 0.2 * vmax + 1e-12


def test_nf1_shock_position_and_cell_fraction() -> None:
    fracs = []
    for i in range(20):
        c = families.nf1(SEED, i)
        nz = c.nozzle.build()
        ex = solve_nozzle(nz, c.pb, c.gamma)
        assert ex.regime == "shock"
        f_div = (ex.x_shock - nz.x_throat) / (nz.x_exit - nz.x_throat)
        assert 0.15 - 1e-9 <= f_div <= 0.9 + 1e-9
        dx = (nz.x_exit - nz.x_in) / c.n
        fracs.append(((ex.x_shock - nz.x_in) / dx) % 1.0)
        assert nz.x_in < nz.x_throat
    assert np.ptp(fracs) > 0.5  # spread over the cell, not aligned


def test_nf2_regimes() -> None:
    regimes = {solve_nozzle(c.nozzle.build(), c.pb, c.gamma).regime
               for c in (families.nf2(SEED, i) for i in range(10))}
    assert regimes <= {"subsonic", "supersonic"} and len(regimes) == 2


def test_nf3_sweeps_move_the_shock() -> None:
    c = families.nf3(SEED, 0)
    nz = c.nozzle.build()
    xs = [solve_nozzle(nz, pb, c.gamma).x_shock for pb in c.pbs]
    assert np.all(np.diff(xs) > 0)
    assert (xs[-1] - xs[0]) / ((nz.x_exit - nz.x_in) / c.n) == pytest.approx(30.0, rel=1e-6)


@pytest.mark.parametrize("kind", ["parabolic", "conical"])
def test_geometries_have_a_single_throat(kind) -> None:
    from schemeforge.arenas.euler1d.cases import NozzleSpec

    nz = NozzleSpec(type=kind, area_ratio=6.0, length=3.0, inlet_ratio=2.0).build()
    x = np.linspace(nz.x_in, nz.x_exit, 3001)
    A = nz.area(x)
    assert A[np.argmin(np.abs(x - 1.0))] == pytest.approx(1.0) and np.argmin(A) == np.argmin(np.abs(x - 1.0))
    assert nz.A_exit == pytest.approx(6.0)
    assert np.all(np.diff(A[x > 1.0]) > 0) and np.all(np.diff(A[x < 1.0]) < 0)
