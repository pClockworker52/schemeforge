"""limiter_stateful slot (judge v1.2): state threading through the solvers, constraints, zoo, probes."""

import jax.numpy as jnp
import numpy as np

from schemeforge.arenas.euler1d import cases, constraints, zoo
from schemeforge.arenas.euler1d.evaluate import run_case, slot_scheme
from schemeforge.engine.probes import fingerprint_distance, probe

SUITE = {c.id: c for c in cases.dev_suite()}


def test_passthrough_state_matches_the_stateless_limiter() -> None:
    a = run_case(SUITE["R1"], *slot_scheme(zoo.load("limiter_stateful", "superbee"), "limiter_stateful"))[0]
    b = run_case(SUITE["R1"], *slot_scheme(zoo.load("limiter", "superbee"), "limiter"))[0]
    for k in ("shock_width", "contact_width", "l1_smooth"):
        assert a[k] == b[k]


def test_frozen_van_leer_converges_explicitly_where_van_leer_cycles() -> None:
    frozen = run_case(SUITE["N5"], *slot_scheme(zoo.load("limiter_stateful", "van_leer_frozen"), "limiter_stateful"))
    plain = run_case(SUITE["N5"], *slot_scheme(zoo.load("limiter_stateful", "van_leer"), "limiter_stateful"))
    assert frozen[1] == [] and frozen[0]["converged_expl"] == 1.0
    assert plain[0]["converged_expl"] < 1.0


def test_zoo_passes_the_stateful_constraints() -> None:
    for name in zoo.members("limiter_stateful"):
        assert constraints.check_limiter_stateful(zoo.load("limiter_stateful", name)) == [], name


def test_stateful_constraints_reject_batch_dependence_and_bad_state() -> None:
    def size_switch(r, s):
        return (jnp.minimum(2.0 * jnp.maximum(r, 0.0), 1.0) if r.size > 500 else jnp.maximum(r, 0.0) * 0.0), s

    def inf_state(r, s):
        return jnp.maximum(0.0, jnp.minimum(1.0, r)), s / (s * 0.0)

    assert any("elementwise" in v for v in constraints.check_limiter_stateful(size_switch))
    assert any("not finite" in v for v in constraints.check_limiter_stateful(inf_state))


def test_probes_tell_a_frozen_limiter_from_its_plain_version() -> None:
    a = probe(zoo.load("limiter_stateful", "superbee"), "euler1d", "limiter_stateful")
    b = probe(zoo.load("limiter_stateful", "superbee_frozen"), "euler1d", "limiter_stateful")
    assert a["descriptors"] == b["descriptors"]
    assert fingerprint_distance(a["fingerprint"], b["fingerprint"]) > 1e-2
    assert np.isfinite(b["fingerprint"]).all()
