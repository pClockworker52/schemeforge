"""Behaviour descriptors and novelty fingerprints (PLAN §5.8). Search policy, not scoring: this runs inside the
sandboxed worker (the candidate is untrusted code) but lives outside the judge tree.

probe(fn, arena, slot) -> {"descriptors": {...}, "fingerprint": [...]} (JSON-serializable)
"""

from __future__ import annotations

from typing import Any

import numpy as np

# limiter: descriptors on r in [0, 3]; fingerprint = phi at 64 fixed slope ratios
LIMITER_R = np.linspace(0.0, 3.0, 301)
LIMITER_FINGERPRINT_R = np.concatenate(
    [np.linspace(-1.0, 0.0, 8), np.linspace(0.05, 3.0, 48), np.geomspace(3.5, 50, 8)]
)


def probe(fn, arena: str, slot: str) -> dict[str, Any]:
    if arena == "euler1d" and slot == "limiter":
        return _limiter(fn)
    if arena == "euler1d" and slot == "limiter_stateful":
        return _limiter_stateful(fn)
    if arena == "euler1d" and slot == "flux":
        return _flux(fn)
    return {"descriptors": {}, "fingerprint": []}


def _limiter(phi) -> dict[str, Any]:
    import jax.numpy as jnp

    v = np.asarray(phi(jnp.asarray(LIMITER_R)), dtype=float)
    h = LIMITER_R[1] - LIMITER_R[0]
    second = np.abs(np.diff(v, 2)) / h**2
    inner = LIMITER_R[1:-1] >= 0.05  # skip the kink every TVD limiter has at r = 0
    return {
        "descriptors": {
            "compressiveness": float(np.mean(v)),  # mean phi on [0, 3]
            "smoothness": float(np.max(second[inner])),  # max |phi''| on [0.05, 3] (large = kinked)
        },
        "fingerprint": np.asarray(phi(jnp.asarray(LIMITER_FINGERPRINT_R)), dtype=float).tolist(),
    }


def _limiter_stateful(phi_s) -> dict[str, Any]:
    """Descriptors of phi at the initial state 0; the fingerprint adds the new state at 0 and phi at a later state
    (s = 1e4), so a frozen limiter differs from its plain version."""
    import jax.numpy as jnp

    def at(s):
        return lambda r: phi_s(r, jnp.full_like(r, s))

    out = _limiter(lambda r: at(0.0)(r)[0])
    rf = jnp.asarray(LIMITER_FINGERPRINT_R)
    out["fingerprint"] += [*np.asarray(at(0.0)(rf)[1], dtype=float).tolist(),
                           *np.asarray(at(1e4)(rf)[0], dtype=float).tolist()]
    return out


def _flux(flux) -> dict[str, Any]:
    import jax.numpy as jnp

    from schemeforge.arenas.euler1d.constraints import flux_probes
    from schemeforge.arenas.euler1d.numerics import physical_flux

    UL, UR = flux_probes(m=64, seed=7)
    F = np.asarray(flux(jnp.asarray(UL), jnp.asarray(UR), 1.4), dtype=float)
    central = 0.5 * np.asarray(physical_flux(jnp.asarray(UL), 1.4) + physical_flux(jnp.asarray(UR), 1.4))
    jump = np.abs(UR - UL) + 1e-300
    diss = np.abs(central - F) / jump  # effective dissipation coefficient per component
    # a stationary contact: zero dissipation keeps it exactly
    rho = np.array([[1.4, 0.0, 1.0 / 0.4]]), np.array([[1.0, 0.0, 1.0 / 0.4]])
    Fc = np.asarray(flux(jnp.asarray(rho[0]), jnp.asarray(rho[1]), 1.4), dtype=float)
    return {
        "descriptors": {
            "dissipation": float(np.median(diss)),
            "contact_dissipation": float(abs(Fc[0, 0])),
        },
        "fingerprint": (F / (np.abs(central) + 1.0)).ravel()[:192].tolist(),
    }


def fingerprint_distance(a: list[float], b: list[float]) -> float:
    """Max absolute difference, scaled by the larger magnitude (inf if the shapes differ)."""
    x, y = np.asarray(a, float), np.asarray(b, float)
    if x.shape != y.shape or x.size == 0:
        return float("inf")
    return float(np.max(np.abs(x - y)) / max(1.0, float(np.max(np.abs(x))), float(np.max(np.abs(y)))))
