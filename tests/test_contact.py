"""Arena 2 (third-medium contact), Phase 6 step 1: the skeleton runs, the zoo passes, broken media are rejected."""

import pytest

pytest.importorskip("felupe", reason="Arena 2 needs the optional 'contact' dependencies (uv sync --extra contact)")

import jax.numpy as jnp  # noqa: E402

from schemeforge.arenas.contact import constraints, zoo  # noqa: E402
from schemeforge.arenas.contact import evaluate as ev  # noqa: E402
from schemeforge.arenas.contact.cases import GapClosureCase, case_from_dict, validate_case  # noqa: E402

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
    assert abs(m["stiffness_err"]) < 0.05 and m["min_J_medium"] > 0.0


def test_newton_failure_is_a_result_not_a_violation() -> None:
    # unregularized and very soft: the medium cannot be squeezed past closure, Newton fails
    m, v = ev.run_case(GapClosureCase("soft", gamma=1e-6), NEO)
    assert v == [] and m == {"converged": 0.0}
