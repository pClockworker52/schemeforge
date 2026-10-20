"""Roe flux (Roe 1981) with Harten's entropy fix on the acoustic waves (Harten 1983, delta = 0.1 a~)."""
import jax.numpy as jnp

DELTA = 0.1


def _prim(U, g):
    rho, m, E = U[:, 0], U[:, 1], U[:, 2]
    u = m / rho
    return rho, u, (g - 1.0) * (E - 0.5 * m * u)


def _phys(U, rho, u, p):
    return jnp.stack([rho * u, rho * u * u + p, (U[:, 2] + p) * u], axis=1)


def _harten(lam, d):
    a = jnp.abs(lam)
    return jnp.where(a < d, 0.5 * (lam * lam + d * d) / d, a)


def flux(UL, UR, gamma):
    g = gamma
    rL, uL, pL = _prim(UL, g)
    rR, uR, pR = _prim(UR, g)
    sl, sr = jnp.sqrt(rL), jnp.sqrt(rR)
    u = (sl * uL + sr * uR) / (sl + sr)
    H = (sl * (UL[:, 2] + pL) / rL + sr * (UR[:, 2] + pR) / rR) / (sl + sr)
    a = jnp.sqrt(jnp.maximum((g - 1.0) * (H - 0.5 * u * u), 1e-300))
    rho = sl * sr
    dr, du, dp = rR - rL, uR - uL, pR - pL
    a1 = (dp - rho * a * du) / (2.0 * a * a)
    a2 = dr - dp / (a * a)
    a3 = (dp + rho * a * du) / (2.0 * a * a)
    d = DELTA * a
    l1, l2, l3 = _harten(u - a, d), jnp.abs(u), _harten(u + a, d)
    one = jnp.ones_like(u)
    r1 = jnp.stack([one, u - a, H - u * a], axis=1)
    r2 = jnp.stack([one, u, 0.5 * u * u], axis=1)
    r3 = jnp.stack([one, u + a, H + u * a], axis=1)
    diss = (l1 * a1)[:, None] * r1 + (l2 * a2)[:, None] * r2 + (l3 * a3)[:, None] * r3
    return 0.5 * (_phys(UL, rL, uL, pL) + _phys(UR, rR, uR, pR)) - 0.5 * diss
