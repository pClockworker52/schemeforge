"""HLL flux (Harten, Lax, van Leer 1983) with Einfeldt (Roe-average) wave-speed estimates."""
import jax.numpy as jnp


def _prim(U, g):
    rho, m, E = U[:, 0], U[:, 1], U[:, 2]
    u = m / rho
    return rho, u, (g - 1.0) * (E - 0.5 * m * u)


def _phys(U, rho, u, p):
    return jnp.stack([rho * u, rho * u * u + p, (U[:, 2] + p) * u], axis=1)


def flux(UL, UR, gamma):
    g = gamma
    rL, uL, pL = _prim(UL, g)
    rR, uR, pR = _prim(UR, g)
    aL, aR = jnp.sqrt(g * pL / rL), jnp.sqrt(g * pR / rR)
    sl, sr = jnp.sqrt(rL), jnp.sqrt(rR)
    u_t = (sl * uL + sr * uR) / (sl + sr)
    H_t = (sl * (UL[:, 2] + pL) / rL + sr * (UR[:, 2] + pR) / rR) / (sl + sr)
    a_t = jnp.sqrt(jnp.maximum((g - 1.0) * (H_t - 0.5 * u_t * u_t), 0.0))
    SL = jnp.minimum(uL - aL, u_t - a_t)[:, None]
    SR = jnp.maximum(uR + aR, u_t + a_t)[:, None]
    FL, FR = _phys(UL, rL, uL, pL), _phys(UR, rR, uR, pR)
    Fs = (SR * FL - SL * FR + SL * SR * (UR - UL)) / (SR - SL)
    return jnp.where(SL >= 0.0, FL, jnp.where(SR <= 0.0, FR, Fs))
