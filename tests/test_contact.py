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
        case_from_dict({"kind": "ironing", "id": "y"})  # not a case kind (yet)


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
    assert ids == ["C0a-g3", "C0a-g5", "C0a-g6", "C0b-s05", "C0b-s2", "C2-g5", "C2-g6", "C1"]
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


def test_hertz_classical_reference_is_within_the_error_floor() -> None:
    # step 3 acceptance: classical frictionless contact within 1 % of Hertz on a and p0 (dev mesh); no traction
    # outside the contact
    from schemeforge.arenas.contact.cases import HertzCase

    m, v = ev.hertz_metrics(HertzCase("cl"), solve.hertz_classical(HertzCase("cl")))
    assert v == [] and abs(m["a_err"]) < 0.01 and abs(m["p0_err"]) < 0.01 and m["leak_out"] < 1e-9


def test_hertz_with_the_medium_shows_the_trade_off() -> None:
    # a stiffer medium carries load outside the contact (wider apparent contact); a softer one costs Newton steps
    from schemeforge.arenas.contact.cases import HertzCase

    m5, v5 = ev.run_case(HertzCase("g5", gamma=1e-5), NEO)
    m6, v6 = ev.run_case(HertzCase("g6", gamma=1e-6), NEO)
    assert v5 == v6 == [] and m5["converged"] == m6["converged"] == 1.0
    assert m5["a_err"] > m6["a_err"] and m6["newton_iters"] > m5["newton_iters"]
    assert abs(m5["p0_err"]) < 0.02 and abs(m6["p0_err"]) < 0.02  # the peak pressure itself is close to Hertz


def test_patch_test_on_distorted_meshes() -> None:
    # C1: the confined gap closure on randomly distorted, straight-edged Q2 meshes still has the homogeneous exact
    # solution; the FE result must reproduce it and the wall pressure must stay uniform
    case = next(c for c in dev_suite() if c.id == "C1")
    assert case.distort > 0.0
    res = solve.gap_closure(NEO, case)
    for k in (2, 4, 6):
        assert res.force[k] == pytest.approx(reference.exact_gap_closure(NEO, case, res.push[k])[0], rel=1e-9)
    m, v = ev.gap_closure_metrics(case, res)
    assert v == [] and m["pressure_spread"] < 1e-7
    with pytest.raises(ValueError):
        validate_case(GapClosureCase("bad", distort=0.6))


def test_hertz_width_and_peak_are_mesh_stable() -> None:
    # step 3 mesh_sens: the width and peak-pressure errors barely move between the coarse and the dev mesh
    from schemeforge.arenas.contact.cases import HertzCase

    m = ev.hertz_mesh_sensitivity(NEO, HertzCase("g5", gamma=1e-5), sizes=((24, 12), (32, 16)))
    assert m["mesh_sens_a_err"] < 0.01 and m["mesh_sens_p0_err"] < 0.01


def test_step4_constraints_reject_negative_soft_and_unit_dependent_media() -> None:
    def negative(C, p):  # rest is a saddle: energy below zero in extension
        return NEO(C, p) - p["gamma"] * p["mu"] * (jnp.trace(C) - 3.0) ** 2

    def no_compression(C, p):  # zero energy whenever the volume shrinks
        j = jnp.sqrt(jnp.linalg.det(C))
        return jnp.where(j < 1.0, 0.0, NEO(C, p))

    def absolute_eps(C, p):  # depends on units: an absolute floor on the moduli
        return p["gamma"] * jnp.maximum(p["mu"], 1e-3) * (jnp.trace(C) - 3.0 - jnp.log(jnp.linalg.det(C))) / 2.0

    assert "negative" in " ".join(constraints.check_medium(negative))
    assert "does not resist compression" in " ".join(constraints.check_medium(no_compression))
    assert "does not scale with the moduli" in " ".join(constraints.check_medium(absolute_eps))


def test_held_out_families_are_valid_seeded_and_independent_of_arena_1() -> None:
    from schemeforge.arenas.contact import families

    seed = "test-seed-not-the-real-one-0123456789"
    suite = families.promo_suite(seed)  # validates every case
    assert [f for f, _ in suite].count("GF") == 10 and [f for f, _ in suite].count("HF") == 6
    assert families.promo_suite(seed) == suite  # deterministic
    assert families.promo_suite(seed + "x") != suite
    hertz = [c for f, c in suite if f == "HF"]
    assert len({c.R for c in hertz}) == len(hertz) and all(1e-6 <= c.gamma <= 1e-5 for c in hertz)


def test_promo_report_aggregates_families_and_hides_nothing_it_should_not() -> None:
    import time

    report = {"slot": "medium", "suite": "promo", "violations": [], "cases": {}, "metamorphic": {}}
    r = ev.evaluate_promo(NEO, report, time.perf_counter(), seed="test-seed-not-the-real-one-0123456789",
                          sizes={"GF": 2, "SF": 2})
    assert r["status"] == "ok" and set(r["families"]) == {"GF", "SF"}
    assert r["families"]["GF"]["n"] == 2 and "median" in r["families"]["GF"]["gap_res"]
    assert len(r["instances"]) == 4 and len(r["seed_fingerprint"]) == 16  # the parent strips and stores instances
