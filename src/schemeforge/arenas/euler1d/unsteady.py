"""Unsteady 1D Euler finite-volume solver (PLAN §9.3): reconstruction + flux slots, SSP-RK3, jit-compiled loop."""

from __future__ import annotations

from dataclasses import dataclass
from functools import partial

import jax
import jax.numpy as jnp

from .numerics import Flux, Reconstruction, cons_to_prim, hllc, max_wave_speed, pad, prim_to_cons


@dataclass(frozen=True)
class UnsteadyResult:
    W: jax.Array  # (n, 3) primitive state at t_end
    steps: int


def rhs(U: jax.Array, dx: float, gamma: float, reconstruct: Reconstruction, flux: Flux, bc: str) -> jax.Array:
    """dU/dt = -(F_{i+1/2} - F_{i-1/2}) / dx for U: (n, 3)."""
    W = pad(cons_to_prim(U, gamma), bc)
    WL, WR = reconstruct(W, gamma)
    F = flux(prim_to_cons(WL, gamma), prim_to_cons(WR, gamma), gamma)
    return -(F[1:] - F[:-1]) / dx


@partial(jax.jit, static_argnames=("reconstruct", "flux", "bc", "max_steps"))
def _run(U0, dx, t_end, gamma, cfl, reconstruct, flux, bc, max_steps):
    def body(state):
        U, t, k = state
        dt = jnp.minimum(cfl * dx / max_wave_speed(U, gamma), t_end - t)
        L = partial(rhs, dx=dx, gamma=gamma, reconstruct=reconstruct, flux=flux, bc=bc)
        U1 = U + dt * L(U)
        U2 = 0.75 * U + 0.25 * (U1 + dt * L(U1))
        U3 = U / 3.0 + 2.0 / 3.0 * (U2 + dt * L(U2))
        return U3, t + dt, k + 1

    def cond(state):
        _, t, k = state
        return (t < t_end) & (k < max_steps)

    U, _, k = jax.lax.while_loop(cond, body, (U0, jnp.asarray(0.0), jnp.asarray(0)))
    return U, k


def solve_unsteady(
    W0: jax.Array,
    dx: float,
    t_end: float,
    gamma: float,
    reconstruct: Reconstruction,
    flux: Flux = hllc,
    bc: str = "transmissive",
    cfl: float = 0.5,
    max_steps: int = 1_000_000,
) -> UnsteadyResult:
    """Advance primitive initial data W0 (n, 3) to t_end with SSP-RK3 at the given CFL number."""
    U0 = prim_to_cons(jnp.asarray(W0, dtype=jnp.float64), gamma)
    U, k = _run(U0, float(dx), float(t_end), float(gamma), float(cfl), reconstruct, flux, bc, int(max_steps))
    return UnsteadyResult(cons_to_prim(U, gamma), int(k))
