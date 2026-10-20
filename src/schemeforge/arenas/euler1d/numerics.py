"""Shared JAX numerics for the Arena 1 solvers: state conversions, MUSCL reconstruction, HLLC flux, ghost cells.

All arrays are float64 (x64 is enabled on import). Primitive W = [rho, u, p], conserved U = [rho, rho u, E],
both with the variable in the last axis. Grids carry NG = 3 ghost cells per side.
"""

from __future__ import annotations

from collections.abc import Callable

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402

NG = 3
R_CLIP = 1e10  # slope ratios are clipped to [-R_CLIP, R_CLIP] before the limiter sees them

Array = jax.Array
Limiter = Callable[[Array], Array]
Reconstruction = Callable[[Array, float], tuple[Array, Array]]
Flux = Callable[[Array, Array, float], Array]


def prim_to_cons(W: Array, g: float) -> Array:
    rho, u, p = W[..., 0], W[..., 1], W[..., 2]
    return jnp.stack([rho, rho * u, p / (g - 1.0) + 0.5 * rho * u * u], axis=-1)


def cons_to_prim(U: Array, g: float) -> Array:
    rho, m, E = U[..., 0], U[..., 1], U[..., 2]
    u = m / rho
    return jnp.stack([rho, u, (g - 1.0) * (E - 0.5 * m * u)], axis=-1)


def physical_flux(U: Array, g: float) -> Array:
    W = cons_to_prim(U, g)
    rho, u, p = W[..., 0], W[..., 1], W[..., 2]
    return jnp.stack([rho * u, rho * u * u + p, (U[..., 2] + p) * u], axis=-1)


def max_wave_speed(U: Array, g: float) -> Array:
    W = cons_to_prim(U, g)
    return jnp.max(jnp.abs(W[..., 1]) + jnp.sqrt(g * W[..., 2] / W[..., 0]))


# --- reconstruction ----------------------------------------------------------------------------------------
def slope_ratio(dm: Array, dp: Array) -> Array:
    """r = dm / dp, safe for dp = 0 (then the slope phi(r) * dp is 0 anyway) and clipped to +-R_CLIP."""
    safe = jnp.where(dp == 0.0, 1.0, dp)
    return jnp.clip(jnp.where(dp == 0.0, 0.0, dm / safe), -R_CLIP, R_CLIP)


def muscl(phi: Limiter) -> Reconstruction:
    """MUSCL on primitive variables with slope sigma_i = phi(r_i) (W_{i+1} - W_i), r_i = dW_- / dW_+.

    Returns reconstruct(W, gamma): W (n + 6, 3) with ghosts -> (WL, WR), each (n + 1, 3), the states left and
    right of interfaces 0..n (interface k separates cells k + 2 and k + 3 of the padded array).
    """

    def reconstruct(W: Array, gamma: float) -> tuple[Array, Array]:
        dm = W[1:-1] - W[:-2]  # cells 1 .. n+4
        dp = W[2:] - W[1:-1]
        sigma = phi(slope_ratio(dm, dp)) * dp
        Wc = W[1:-1]
        left = (Wc + 0.5 * sigma)[1:-2]  # cells 2 .. n+2
        right = (Wc - 0.5 * sigma)[2:-1]  # cells 3 .. n+3
        return left, right

    return reconstruct


def first_order(W: Array, gamma: float) -> tuple[Array, Array]:
    return W[NG - 1 : -NG], W[NG : -NG + 1]


# --- flux ---------------------------------------------------------------------------------------------------
def hllc(UL: Array, UR: Array, g: float) -> Array:
    """HLLC (Toro 2009, §10.4) with Einfeldt/Roe-average wave-speed estimates. UL, UR: (m, 3) -> F: (m, 3)."""
    WL, WR = cons_to_prim(UL, g), cons_to_prim(UR, g)
    rL, uL, pL = WL[:, 0], WL[:, 1], WL[:, 2]
    rR, uR, pR = WR[:, 0], WR[:, 1], WR[:, 2]
    aL, aR = jnp.sqrt(g * pL / rL), jnp.sqrt(g * pR / rR)
    HL, HR = (UL[:, 2] + pL) / rL, (UR[:, 2] + pR) / rR
    sl, sr = jnp.sqrt(rL), jnp.sqrt(rR)
    u_roe = (sl * uL + sr * uR) / (sl + sr)
    H_roe = (sl * HL + sr * HR) / (sl + sr)
    a_roe = jnp.sqrt(jnp.maximum((g - 1.0) * (H_roe - 0.5 * u_roe * u_roe), 0.0))
    SL = jnp.minimum(uL - aL, u_roe - a_roe)
    SR = jnp.maximum(uR + aR, u_roe + a_roe)
    S_star = (pR - pL + rL * uL * (SL - uL) - rR * uR * (SR - uR)) / (rL * (SL - uL) - rR * (SR - uR))

    def star_state(U, r, u, p, S):
        coef = r * (S - u) / (S - S_star)
        E = U[:, 2]
        return jnp.stack(
            [coef, coef * S_star, coef * (E / r + (S_star - u) * (S_star + p / (r * (S - u))))], axis=1
        )

    FL, FR = physical_flux(UL, g), physical_flux(UR, g)
    FsL = FL + SL[:, None] * (star_state(UL, rL, uL, pL, SL) - UL)
    FsR = FR + SR[:, None] * (star_state(UR, rR, uR, pR, SR) - UR)
    return jnp.where(
        (SL >= 0.0)[:, None], FL, jnp.where((S_star >= 0.0)[:, None], FsL, jnp.where((SR > 0.0)[:, None], FsR, FR))
    )


# --- boundaries ---------------------------------------------------------------------------------------------
def pad(W: Array, bc: str) -> Array:
    """Add NG ghost cells per side: 'transmissive' (zero-gradient) or 'periodic'. W: (n, 3) -> (n + 6, 3)."""
    if bc == "periodic":
        return jnp.concatenate([W[-NG:], W, W[:NG]])
    if bc == "transmissive":
        return jnp.concatenate([jnp.repeat(W[:1], NG, axis=0), W, jnp.repeat(W[-1:], NG, axis=0)])
    raise ValueError(f"unknown boundary condition {bc!r}")
