"""Arena 2 (third-medium contact), Phase 6 steps 1-2: the zoo passes, broken media are rejected, the FE model
reproduces the exact homogeneous solutions to round-off, pressure recovery is exact, the dev metrics make sense."""

import pytest

pytest.importorskip("felupe", reason="Arena 2 needs the optional 'contact' dependencies (uv sync --extra contact)")

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

from schemeforge.arenas.contact import constraints, reference, solve, zoo  # noqa: E402
from schemeforge.arenas.contact import evaluate as ev  # noqa: E402
from schemeforge.arenas.contact.cases import (  # noqa: E402
    GapClosureCase,
    SimpleShearCase,
    case_from_dict,
    dev_suite,
    validate_case,
)
from schemeforge.arenas.contact.metrics import edge_traction  # noqa: E402

NEO = zoo.load("medium", "neo_hooke")


def test_zoo_passes_the_medium_constraints() -> None:
    for name in zoo.members("medium"):
        assert constraints.check_medium(zoo.load("medium", name)) == [], name


def test_broken_media_are_rejected() -> None:
    def prestressed(C, p):  # energy not stationary at rest
        return NEO(C, p) + p["gamma"] * p["mu"] * (jnp.trace(C) - 3.0)

    def offset(C, p):
        return NEO(C, p) + 1.0

    def singular(C, p):
        return NEO(C, p) / (jnp.trace(C) - 3.0)

    assert "not stress-free at rest" in " ".join(constraints.check_medium(prestressed))
    assert "not zero at rest" in " ".join(constraints.check_medium(offset))
    assert "not finite" in " ".join(constraints.check_medium(singular))


def test_cases_round_trip_and_validate() -> None:
    c = case_from_dict({"kind": "gap_closure", "id": "x", "gap": 0.1, "push": 0.15})
    assert c == GapClosureCase("x", gap=0.1, push=0.15)
    validate_case(c)
    with pytest.raises(ValueError):
        validate_case(GapClosureCase("bad", push=0.05))  # does not close the gap
    with pytest.raises(ValueError):
        case_from_dict({"kind": "hertz", "id": "y"})


def test_smoke_runs_and_measures_the_trade_off() -> None:
    r = ev.evaluate(NEO, "medium", "smoke")
    assert r["status"] == "ok", r["violations"]
    m = r["cases"]["smoke-C0a"]
    # gamma = 1e-3: some force leaks before contact, a thin medium layer remains, the column's stiffness comes back
    assert m["converged"] == 1.0 and 0.0 < m["leak_pre"] < 0.1 and 0.0 < m["gap_res"] < 0.1
    assert 0.0 < m["force_err"] < 0.1 and m["min_J_medium"] > 0.0  # the residual layer compresses the body more


@pytest.mark.parametrize("gamma", [1e-3, 1e-5])
def test_gap_closure_matches_the_exact_homogeneous_solution(gamma) -> None:
    # confined column: each layer is homogeneous, which Q2 elements represent exactly
    case = GapClosureCase("t", gamma=gamma, nx=2)
    res = solve.gap_closure(NEO, case)
    for k in (2, 4, 6):
        exact, _ = reference.exact_gap_closure(NEO, case, res.push[k])
        assert res.force[k] == pytest.approx(exact, rel=1e-9)
    assert res.medium_thickness == pytest.approx(reference.exact_gap_closure(NEO, case, case.push)[1], rel=1e-9)
    # the wall pressure recovered from the nodal reactions is uniform and equals force / width
    assert np.allclose(res.wall_pressure, res.force[-1] / case.width, rtol=1e-10)


def test_edge_traction_recovers_quadratic_tractions_exactly() -> None:
    x = np.array([0.0, 0.05, 0.1, 0.25, 0.4])  # two quadratic elements of unequal length, mid-nodes centred
    t_true = 1.0 + 3.0 * x  # linear traction: consistent nodal forces by Simpson's rule per element
    f = np.zeros(5)
    for e in (0, 2):
        L = x[e + 2] - x[e]
        N = lambda s: np.array([(1 - s) * (1 - 2 * s), 4 * s * (1 - s), s * (2 * s - 1)])  # noqa: E731
        for s_, wgt in ((0.0, 1 / 6), (0.5, 4 / 6), (1.0, 1 / 6)):
            xx = x[e] + s_ * L
            f[e:e + 3] += wgt * L * N(s_) * (1.0 + 3.0 * xx) * 1.0
    assert np.allclose(edge_traction(x, f), t_true, rtol=1e-12)
    with pytest.raises(ValueError):
        edge_traction(x[:4], f[:4])


def test_simple_shear_is_exact_for_neo_hooke() -> None:
    # scaled neo-Hooke in simple shear: P_xy = gamma mu shear exactly, so shear_parasitic = gamma
    for shear in (0.5, 2.0):
        m, v = ev.simple_shear_metrics(SimpleShearCase("s", shear=shear, gamma=1e-5), NEO)
        assert v == [] and m["shear_parasitic"] == pytest.approx(1e-5, rel=1e-12)


def test_dev_suite_shows_the_stiffness_trade_off() -> None:
    ids = [c.id for c in dev_suite()]
    assert ids == ["C0a-g3", "C0a-g5", "C0a-g6", "C0b-s05", "C0b-s2"]
    r = ev.evaluate(NEO, "medium", "dev")
    assert r["status"] == "ok", r["violations"]
    c = r["cases"]
    # a softer medium leaks less force before contact (PLAN §14.7); Newton cost is the other side of the trade-off
    assert c["C0a-g3"]["leak_pre"] > c["C0a-g5"]["leak_pre"] > c["C0a-g6"]["leak_pre"] > 0.0
    assert all(c[k]["converged"] == 1.0 for k in ("C0a-g3", "C0a-g5", "C0a-g6"))


def test_unconfined_soft_medium_is_not_in_the_dev_suite() -> None:
    # step 1 found that an unconfined, unregularized gamma = 1e-6 column fails Newton (the medium bulges sideways);
    # the confined cases avoid that. A Newton failure still counts as a result, not a violation.
    assert all(isinstance(c, SimpleShearCase) or c.gamma >= 1e-6 for c in dev_suite())


def test_classical_contact_reproduces_ideal_gap_closure() -> None:
    # classical frictionless contact against a rigid plane: exactly no force before contact, and the ideal body force
    # after it once the penalty error is extrapolated away
    case = GapClosureCase("t", gamma=1e-5)
    full = {}
    for k in (1e2, 1e3, 1e4):
        push, force = solve.gap_closure_classical(case, k)
        assert abs(float(np.interp(0.5 * case.gap, push, force))) < 1e-14
        full[k] = force[-1]
    ideal = float(reference.ideal_gap_force(case, case.push))
    assert solve.classical_extrapolated(full) == pytest.approx(ideal, rel=1e-9)  # measured 1.9e-10 (Newton tol 1e-10)
