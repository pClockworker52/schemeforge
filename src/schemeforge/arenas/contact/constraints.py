"""Hard constraints on Arena 2 slot functions, checked on fixed probe sets before any case runs (PLAN §14.3).

Step 1 checks the medium energy at rest and on a probe set of deformations; unit scaling, positivity under
compression and batch independence follow in step 4 (docs/plans/2026-10-30-phase6.md).
"""

from __future__ import annotations

from collections.abc import Callable

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

P_PROBE = {"mu": 0.3846153846153846, "lmbda": 0.5769230769230769, "gamma": 1e-3}  # E = 1, nu = 0.3
REST_TOL = 1e-12  # relative to mu * gamma


def deformation_probes(seed: int = 20261030) -> list[np.ndarray]:
    """Plane-strain deformation gradients (3, 3) with F[2, 2] = 1: rest, uniaxial stretch and compression down to a
    thickness ratio of 1e-3, simple shear, and random admissible F (det F in [1e-3, 10])."""
    rng = np.random.default_rng(seed)
    out = [np.eye(3)]
    for s in (1e-3, 1e-2, 0.1, 0.5, 0.9, 1.1, 2.0, 5.0):
        out.append(np.diag([1.0, s, 1.0]))
    for g in (0.1, 1.0, 5.0):
        F = np.eye(3)
        F[0, 1] = g
        out.append(F)
    while len(out) < 40:
        F = np.eye(3)
        F[:2, :2] += rng.normal(0.0, 0.6, (2, 2))
        if 1e-3 <= np.linalg.det(F) <= 10.0:
            out.append(F)
    return out


def check_medium(psi: Callable) -> list[str]:
    """medium: psi(C, p) -> scalar energy density. Finite with finite gradient on the probes, deterministic, zero and
    stress-free at rest (C = I)."""
    p = {k: jnp.asarray(v) for k, v in P_PROBE.items()}
    scale = P_PROBE["mu"] * P_PROBE["gamma"]
    grad = jax.grad(lambda C: psi(C, p))
    v: list[str] = []
    try:
        for F in deformation_probes():
            C = jnp.asarray(F.T @ F)
            e, dC = np.asarray(psi(C, p)), np.asarray(grad(C))
            if e.shape != ():
                return [f"psi_medium returned shape {e.shape}, expected a scalar"]
            if e.dtype != np.float64:
                return [f"psi_medium returned dtype {e.dtype}, expected float64"]
            if not (np.isfinite(e) and np.all(np.isfinite(dC))):
                v.append("psi_medium or its derivative is not finite on admissible deformations")
                break
            if not np.array_equal(e, np.asarray(psi(C, p))):
                v.append("psi_medium is not deterministic")
                break
        rest = jnp.eye(3)
        if abs(float(psi(rest, p))) > REST_TOL * scale:
            v.append("psi_medium is not zero at rest (C = I)")
        if np.max(np.abs(np.asarray(grad(rest)))) > REST_TOL * scale:
            v.append("psi_medium is not stress-free at rest (dpsi/dC != 0 at C = I)")
    except Exception as exc:  # noqa: BLE001 - candidate code can fail in any way
        return [f"psi_medium raised {type(exc).__name__}: {exc}"]
    return v
