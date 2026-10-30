"""Exact references for the homogeneous Arena 2 cases (PLAN §14.2 C0a, C0b), for any medium energy psi(C, p).

Both cases are homogeneous by construction (laterally confined column; simple shear), so the deformation of each
layer is a single stretch or shear and the exact solution follows from scalar equations. Bi-quadratic elements
represent homogeneous fields exactly, so the FE result must agree to round-off (tests, `sforge judge verify`).
Forces are per unit thickness, compressive positive; stresses are first Piola-Kirchhoff.
"""

from __future__ import annotations

from collections.abc import Callable

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from scipy.optimize import brentq  # noqa: E402

from .cases import GapClosureCase  # noqa: E402


def lame(E: float, nu: float) -> tuple[float, float]:
    """(mu, lmbda) of an isotropic body from Young's modulus and Poisson's ratio."""
    return E / (2.0 * (1.0 + nu)), E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))


def body_stress(stretch: float, mu: float, lmbda: float) -> float:
    """P_yy of the compressible neo-Hookean body (felupe NeoHookeCompressible) under confined stretch F = diag(1, s, 1):
    d/ds [mu/2 (s^2 - 1) - mu ln s + lmbda/2 ln^2 s]."""
    return mu * (stretch - 1.0 / stretch) + lmbda * np.log(stretch) / stretch


def medium_stress_fn(psi: Callable, p: dict[str, float]) -> Callable[[float], float]:
    """P_yy of the medium under confined stretch, by JAX: d/ds psi(diag(1, s^2, 1), p)."""
    pj = {k: jnp.asarray(v) for k, v in p.items()}
    d = jax.grad(lambda s: psi(jnp.diag(jnp.array([1.0, s**2, 1.0])), pj))
    return lambda s: float(d(jnp.asarray(s)))


def shear_stress(psi: Callable, p: dict[str, float], shear: float) -> tuple[float, float]:
    """(P_xy, P_yy) of the medium in simple shear F = [[1, shear, 0], [0, 1, 0], [0, 0, 1]]: P = 2 F dpsi/dC."""
    pj = {k: jnp.asarray(v) for k, v in p.items()}
    F = jnp.eye(3).at[0, 1].set(shear)
    P = 2.0 * F @ jax.grad(lambda C: psi(C, pj))(F.T @ F)
    return float(P[0, 1]), float(P[1, 1])


def ideal_gap_force(case: GapClosureCase, push: np.ndarray) -> np.ndarray:
    """Ideal contact: no force until the gap closes, then the confined body alone, compressed by push - gap."""
    mu, lmbda = lame(case.E, case.nu)
    over = np.clip(np.asarray(push, float) - case.gap, 0.0, None)
    s = (case.height - over) / case.height
    return np.where(over > 0.0, -case.width * body_stress(s, mu, lmbda), 0.0)


def exact_gap_closure(psi: Callable, case: GapClosureCase, push: float) -> tuple[float, float]:
    """(force, medium thickness) of the confined column at a given push, for the candidate medium: equal P_yy in body
    and medium, h s_b + g s_m = h + g - push. Brent's method on the medium stretch."""
    mu, lmbda = lame(case.E, case.nu)
    pm = medium_stress_fn(psi, {"mu": mu, "lmbda": lmbda, "gamma": case.gamma})
    h, g = case.height, case.gap

    def residual(sm: float) -> float:
        sb = (h + g - push - g * sm) / h
        return body_stress(sb, mu, lmbda) - pm(sm)

    hi = (h + g - push - 1e-9 * h) / g  # body stretch -> 0+
    sm = brentq(residual, 1e-14, hi, xtol=1e-15, rtol=4 * np.finfo(float).eps, maxiter=500)
    return -case.width * pm(sm), g * sm
