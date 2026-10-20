"""Ideal, calorically perfect gas in nondimensional units (PLAN §9.1). NumPy float64.

Primitive state W = (rho, u, p); conserved state U = (rho, rho*u, E) with E = p/(gamma-1) + rho*u^2/2.
Arrays have shape (..., 3) with the variable in the last axis.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

F64 = NDArray[np.float64]

GAMMAS: tuple[float, ...] = (1.4, 5.0 / 3.0, 1.405)  # N2, He, H2
GAMMA_STRESS = 1.2


def sound_speed(rho: ArrayLike, p: ArrayLike, gamma: float) -> F64:
    """a = sqrt(gamma p / rho)."""
    return np.sqrt(gamma * np.asarray(p, dtype=float) / np.asarray(rho, dtype=float))


def prim_to_cons(W: ArrayLike, gamma: float) -> F64:
    """(..., 3) primitive [rho, u, p] -> (..., 3) conserved [rho, rho u, E]."""
    W = np.asarray(W, dtype=float)
    rho, u, p = W[..., 0], W[..., 1], W[..., 2]
    return np.stack([rho, rho * u, p / (gamma - 1.0) + 0.5 * rho * u * u], axis=-1)


def cons_to_prim(U: ArrayLike, gamma: float) -> F64:
    """(..., 3) conserved [rho, rho u, E] -> (..., 3) primitive [rho, u, p]."""
    U = np.asarray(U, dtype=float)
    rho, m, E = U[..., 0], U[..., 1], U[..., 2]
    u = m / rho
    return np.stack([rho, u, (gamma - 1.0) * (E - 0.5 * m * u)], axis=-1)


def euler_flux(U: ArrayLike, gamma: float) -> F64:
    """Physical flux F(U) = [rho u, rho u^2 + p, (E + p) u], shape (..., 3)."""
    U = np.asarray(U, dtype=float)
    rho, u, p = np.moveaxis(cons_to_prim(U, gamma), -1, 0)
    E = U[..., 2]
    return np.stack([rho * u, rho * u * u + p, (E + p) * u], axis=-1)


def entropy(rho: ArrayLike, p: ArrayLike, gamma: float) -> F64:
    """Specific entropy up to constants: s = ln(p / rho^gamma) / (gamma - 1)."""
    return np.log(np.asarray(p, dtype=float) / np.asarray(rho, dtype=float) ** gamma) / (gamma - 1.0)
