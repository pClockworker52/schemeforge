"""Unsteady 1D Euler finite-volume solver (PLAN §9.3): reconstruction + flux slots, SSP-RK3, jit-compiled loop."""

from __future__ import annotations

from dataclasses import dataclass
from functools import partial

import jax
import jax.numpy as jnp

from .numerics import (
    NG,
    Flux,
    Reconstruction,
    cons_to_prim,
    hllc,
    initial_limiter_state,
    max_wave_speed,
    pad,
    prim_to_cons,
    reconstruct_with_state,
)


@dataclass(frozen=True)
class UnsteadyResult:
    W: jax.Array  # (n, 3) primitive state at t_end
    steps: int


def rhs_with_state(U, S, dx, gamma, reconstruct: Reconstruction, flux: Flux, bc: str):
    """(dU/dt, S_new) for U: (n, 3) and limiter state S: (n + 4, 3) (unused by stateless reconstructions)."""
    W = pad(cons_to_prim(U, gamma), bc)
    WL, WR, S_new = reconstruct_with_state(reconstruct, W, gamma, S)
    F = flux(prim_to_cons(WL, gamma), prim_to_cons(WR, gamma), gamma)
    return -(F[1:] - F[:-1]) / dx, S_new


def rhs(U: jax.Array, dx: float, gamma: float, reconstruct: Reconstruction, flux: Flux, bc: str) -> jax.Array:
    """dU/dt = -(F_{i+1/2} - F_{i-1/2}) / dx for U: (n, 3) (zero limiter state)."""
    return rhs_with_state(U, initial_limiter_state(U.shape[0] + 2 * NG), dx, gamma, reconstruct, flux, bc)[0]


@partial(jax.jit, static_argnames=("reconstruct", "flux", "bc", "max_steps"))
def _run(U0, dx, t_end, gamma, cfl, reconstruct, flux, bc, max_steps):
    L = partial(rhs_with_state, dx=dx, gamma=gamma, reconstruct=reconstruct, flux=flux, bc=bc)

    def body(state):
        U, S, t, k = state
        dt = jnp.minimum(cfl * dx / max_wave_speed(U, gamma), t_end - t)
        dU, S_next = L(U, S)  # the limiter state is updated once per step, from the step's first stage
        U1 = U + dt * dU
        U2 = 0.75 * U + 0.25 * (U1 + dt * L(U1, S)[0])
        U3 = U / 3.0 + 2.0 / 3.0 * (U2 + dt * L(U2, S)[0])
        return U3, S_next, t + dt, k + 1

    def cond(state):
        _, _, t, k = state
        return (t < t_end) & (k < max_steps)

    S0 = initial_limiter_state(U0.shape[0] + 2 * NG)
    U, _, _, k = jax.lax.while_loop(cond, body, (U0, S0, jnp.asarray(0.0), jnp.asarray(0)))
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
