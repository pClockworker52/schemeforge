"""Shared JAX numerics for the Arena 1 solvers: state conversions, MUSCL reconstruction, HLLC flux, ghost cells.

All arrays are float64 (x64 is enabled on import). Primitive W = [rho, u, p], conserved U = [rho, rho u, E],
both with the variable in the last axis. Grids carry NG = 3 ghost cells per side.
"""

from __future__ import annotations

from collections.abc import Callable

import jax

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402

from . import zoo  # noqa: E402  (after x64 is enabled)

NG = 3
R_CLIP = 1e10  # slope ratios are clipped to [-R_CLIP, R_CLIP] before the limiter sees them

Array = jax.Array
Limiter = Callable[[Array], Array]
StatefulLimiter = Callable[[Array, Array], tuple[Array, Array]]
Reconstruction = Callable[[Array, float], tuple[Array, Array]]
Flux = Callable[[Array, Array, float], Array]


def elementwise(phi: Limiter) -> Limiter:
    """phi applied to one slope ratio at a time (vmap over the flattened input), so a candidate cannot see the
    batch: no case detection from its size or statistics, no position dependence (red team s01, s02, s06)."""

    def wrapped(r: Array) -> Array:
        return jax.vmap(phi)(r.reshape(-1)).reshape(r.shape)

    return wrapped


def rowwise(flux: Flux) -> Flux:
    """flux applied to one interface at a time: each call sees a (1, 3) batch (red team f01)."""

    def wrapped(UL: Array, UR: Array, g: float) -> Array:
        return jax.vmap(lambda a, b: flux(a[None], b[None], g)[0])(UL, UR)

    return wrapped


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


def muscl_stateful(phi_s: StatefulLimiter) -> Reconstruction:
    """MUSCL with a stateful limiter (slot `limiter_stateful`): phi, S_new = phi_s(r, S), S of the shape of r,
    (n + 4, 3). Returns reconstruct(W, gamma, S) -> (WL, WR, S_new); marked `stateful` for the solvers, which
    hold S fixed within a step and replace it by S_new after an accepted step (docs/judge/euler1d_spec.md)."""

    def reconstruct(W: Array, gamma: float, S: Array) -> tuple[Array, Array, Array]:
        dm = W[1:-1] - W[:-2]
        dp = W[2:] - W[1:-1]
        phi, S_new = phi_s(slope_ratio(dm, dp), S)
        sigma = phi * dp
        Wc = W[1:-1]
        return (Wc + 0.5 * sigma)[1:-2], (Wc - 0.5 * sigma)[2:-1], S_new

    reconstruct.stateful = True  # type: ignore[attr-defined]
    return reconstruct


def elementwise_stateful(phi_s: StatefulLimiter) -> StatefulLimiter:
    """phi_s applied to one (r, state) pair at a time, like `elementwise`."""

    def wrapped(r: Array, S: Array) -> tuple[Array, Array]:
        phi, S_new = jax.vmap(phi_s)(r.reshape(-1), S.reshape(-1))
        return phi.reshape(r.shape), S_new.reshape(r.shape)

    return wrapped


def initial_limiter_state(n_padded: int) -> Array:
    """Zero state for a padded grid of n_padded cells: one value per slope ratio, (n_padded - 2, 3)."""
    return jnp.zeros((n_padded - 2, 3))


def reconstruct_with_state(reconstruct: Reconstruction, W: Array, gamma: float, S: Array):
    """(WL, WR, S_new) for stateful and stateless reconstructions alike (a stateless one keeps S)."""
    if getattr(reconstruct, "stateful", False):
        return reconstruct(W, gamma, S)
    WL, WR = reconstruct(W, gamma)
    return WL, WR, S


def first_order(W: Array, gamma: float) -> tuple[Array, Array]:
    return W[NG - 1 : -NG], W[NG : -NG + 1]


# --- flux ---------------------------------------------------------------------------------------------------
# The judge's default flux is the zoo's HLLC file (one implementation): HLLC (Toro 2009, §10.4) with Einfeldt
# wave-speed estimates. UL, UR: (m, 3) -> F: (m, 3).
hllc: Flux = zoo.load("flux", "hllc")


# --- boundaries ---------------------------------------------------------------------------------------------
def pad(W: Array, bc: str) -> Array:
    """Add NG ghost cells per side: 'transmissive' (zero-gradient) or 'periodic'. W: (n, 3) -> (n + 6, 3)."""
    if bc == "periodic":
        return jnp.concatenate([W[-NG:], W, W[:NG]])
    if bc == "transmissive":
        return jnp.concatenate([jnp.repeat(W[:1], NG, axis=0), W, jnp.repeat(W[-1:], NG, axis=0)])
    raise ValueError(f"unknown boundary condition {bc!r}")
