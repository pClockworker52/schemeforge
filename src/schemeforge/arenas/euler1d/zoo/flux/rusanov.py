"""Rusanov (local Lax-Friedrichs) flux: F = (FL + FR)/2 - smax (UR - UL)/2, smax = max(|u| + a)."""
import jax.numpy as jnp


def _prim(U, g):
    rho, m, E = U[:, 0], U[:, 1], U[:, 2]
    u = m / rho
    return rho, u, (g - 1.0) * (E - 0.5 * m * u)


def _phys(U, rho, u, p):
    return jnp.stack([rho * u, rho * u * u + p, (U[:, 2] + p) * u], axis=1)


def flux(UL, UR, gamma):
    rL, uL, pL = _prim(UL, gamma)
    rR, uR, pR = _prim(UR, gamma)
    s = jnp.maximum(jnp.abs(uL) + jnp.sqrt(gamma * pL / rL), jnp.abs(uR) + jnp.sqrt(gamma * pR / rR))
    return 0.5 * (_phys(UL, rL, uL, pL) + _phys(UR, rR, uR, pR)) - 0.5 * s[:, None] * (UR - UL)
