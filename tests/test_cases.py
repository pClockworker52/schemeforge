"""Dev suite definitions and case YAML loading."""

import numpy as np
import pytest
import yaml

from schemeforge.arenas.euler1d.cases import (
    NozzleSpec,
    case_from_dict,
    dev_suite,
    load_reference,
    slowly_moving_shock,
    validate_case,
)
from schemeforge.arenas.euler1d.exact_nozzle import anderson_nozzle, solve_nozzle
from schemeforge.arenas.euler1d.exact_riemann import solve_riemann
from schemeforge.arenas.euler1d.gas import sound_speed


def test_dev_suite_ids_and_admissibility() -> None:
    suite = dev_suite()
    assert [c.id for c in suite] == ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "S1", "N1", "N2", "N3", "N4", "N5",
                                     "N6", "B-0002", "B-0004", "B-0010", "B-0011"]  # accepted breaker cases (v1.4)
    for case in suite:
        validate_case(case)


def test_r7_reference_is_cached_and_averaged() -> None:
    r7 = next(c for c in dev_suite() if c.id == "R7")
    ref = load_reference(r7)
    assert ref.shape == (400, 3) and np.all(np.isfinite(ref)) and np.all(ref[:, [0, 2]] > 0)
    # post-shock state on the far left, undisturbed wave on the far right
    np.testing.assert_allclose(ref[0], (3.857143, 2.629369, 10.333333), rtol=1e-6)
    x = -5.0 + (np.arange(400) + 0.5) * 0.025
    np.testing.assert_allclose(ref[-20:, 0], 1.0 + 0.2 * np.sin(5.0 * x[-20:]), atol=2e-3)


def test_r6_is_a_single_slow_shock() -> None:
    left, right, s = slowly_moving_shock()
    sol = solve_riemann(left, right, 1.4)
    assert sol.right.kind == "shock"
    assert sol.right.speeds[0] == pytest.approx(s, rel=1e-10)
    assert sol.p_star == pytest.approx(left[2], rel=1e-10)  # the left wave has zero strength
    vmax = max(abs(left[1]) + sound_speed(left[0], left[2], 1.4), abs(right[1]) + sound_speed(right[0], right[2], 1.4))
    assert s == pytest.approx(0.05 * vmax, rel=1e-12)


def test_n4_sweep_moves_the_shock_about_30_cells() -> None:
    n4 = next(c for c in dev_suite() if c.id == "N4")
    nz = anderson_nozzle()
    xs = [solve_nozzle(nz, pb, 1.4).x_shock for pb in n4.pbs]
    assert len(xs) == 11 and np.all(np.diff(xs) > 0)
    assert (xs[-1] - xs[0]) / (3.0 / n4.n) == pytest.approx(30.0, rel=1e-6)


def test_yaml_roundtrip() -> None:
    text = """
kind: riemann
id: B-0001
left: [1.0, 0.0, 100.0]
right: [0.01, 0.0, 0.001]
t_end: 0.01
n: 200
"""
    case = case_from_dict(yaml.safe_load(text))
    validate_case(case)
    assert case.left == (1.0, 0.0, 100.0) and case.gamma == 1.4

    noz = case_from_dict({"kind": "nozzle", "id": "B-0002", "pb": 0.5, "n": 60,
                          "nozzle": {"type": "parabolic", "area_ratio": 4.0, "length": 2.0}})
    validate_case(noz)
    nz = noz.nozzle.build()
    assert nz.A_throat == pytest.approx(1.0) and nz.A_exit == pytest.approx(4.0)


def test_vacuum_case_is_inadmissible() -> None:
    bad = case_from_dict({"kind": "riemann", "id": "B-0003", "left": [1, -20, 0.4], "right": [1, 20, 0.4],
                          "t_end": 0.1, "n": 100})
    with pytest.raises(ValueError):
        validate_case(bad)


def test_waves_reaching_the_boundary_are_inadmissible() -> None:
    late = case_from_dict({"kind": "riemann", "id": "B-0004", "left": [1, 0, 1], "right": [0.125, 0, 0.1],
                           "t_end": 0.5, "n": 100})
    with pytest.raises(ValueError, match="boundary"):
        validate_case(late)


def test_parabolic_nozzle_throat_is_minimum() -> None:
    nz = NozzleSpec(type="parabolic", area_ratio=3.0, length=2.5).build()
    x = np.linspace(nz.x_in, nz.x_exit, 1001)
    assert np.argmin(nz.area(x)) == np.argmin(np.abs(x - nz.x_throat))
