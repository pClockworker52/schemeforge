"""Steady quasi-1D nozzle solver (PLAN §9.3): explicit LTS SSP-RK3 and implicit backward-Euler pseudo-time.

State per cell: U_i = (rho A, rho u A, E A) with A_i = A(x_i). Semi-discretization
    dU_i/dt = -(F_{i+1/2} A_{i+1/2} - F_{i-1/2} A_{i-1/2}) / dx + [0, S_i, 0],  S_i = p_i (A_{i+1/2} - A_{i-1/2}) / dx,
which balances flow at rest exactly but is not well-balanced for moving steady flow (Target B).
Units as in exact_nozzle: inlet stagnation p0 = rho0 = 1, so T0 = 1 and a0^2 = gamma (T = p / rho).

Jitted functions take the grid, pb and gamma as traced arguments, so a p_b sweep compiles once per operator.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from functools import cache, partial

import jax
import jax.numpy as jnp
import numpy as np

from .exact_nozzle import (
    Nozzle,
    area_ratio,
    back_pressure_for_shock,
    critical_pressures,
    mach_from_area_ratio,
    p_over_p0,
    solve_nozzle,
)
from .numerics import (
    NG,
    Flux,
    Reconstruction,
    cons_to_prim,
    hllc,
    initial_limiter_state,
    prim_to_cons,
    reconstruct_with_state,
)

CONVERGED = 1e-12
EXPLICIT_CFL = 0.8
EXPLICIT_MAX_ITERS = 50_000
IMPLICIT_CFL0 = 1.0
IMPLICIT_CFL_MAX = 1e8
IMPLICIT_MAX_ITERS = 300
SUBSONIC_GUESS_MACH = 0.5  # throat Mach of the initial guess for unchoked cases

# operator(U, A_face, dx, gamma, W_padded, S) -> (F_face * A_face: (n + 1, 3), S_mom: (n,), S_new); S is the limiter
# state (n + 4, 3) of a stateful reconstruction, passed through unchanged otherwise; see euler1d_slots.md
Operator = Callable[..., tuple[jax.Array, jax.Array, jax.Array]]


@dataclass(frozen=True)
class Grid:
    nozzle: Nozzle
    n: int
    x: np.ndarray  # (n,) cell centres
    x_face: np.ndarray  # (n + 1,)
    A: np.ndarray  # (n,)
    A_face: np.ndarray  # (n + 1,)
    dx: float


def make_grid(nz: Nozzle, n: int) -> Grid:
    x_face = np.linspace(nz.x_in, nz.x_exit, n + 1)
    x = 0.5 * (x_face[1:] + x_face[:-1])
    A = np.asarray(nz.area(x), float)
    A_face = np.asarray(nz.area(x_face), float)
    return Grid(nz, n, x, x_face, A, A_face, float(x_face[1] - x_face[0]))


# --- boundary conditions (judge-owned) ---------------------------------------------------------------------
def pressure_outlet(nz: Nozzle, pb: float, g: float) -> bool:
    """True when the case is a pressure outlet: p_b > p_crit2, so the exact flow has a subsonic exit (shock or
    unchoked regime). Decided from geometry and p_b alone, never from the exact solution."""
    return bool(pb > critical_pressures(nz, g).p_crit2)


def boundary_states(W: jax.Array, pb, g, force_pb=False) -> tuple[jax.Array, jax.Array]:
    """Inlet and outlet ghost states (3,) from the interior primitive states W (n, 3).

    Outlet: p = pb with entropy and J+ extrapolated when the last cell is subsonic or force_pb is set (pressure
    outlet; without forcing, a shock that leaves the domain during the pseudo-time transient never returns and the
    discrete problem settles on a spurious supersonic-exit state); otherwise everything is extrapolated."""
    # Inlet: p0 = T0 = 1; extrapolate the outgoing invariant J- = u - 2a/(g-1) from the first cell.
    k = 0.5 * (g - 1.0)
    J = W[0, 1] - jnp.sqrt(g * W[0, 2] / W[0, 0]) / k
    # a = k (u - J) and a0^2 = a^2 + k u^2 = g  ->  (k^2 + k) u^2 - 2 k^2 J u + k^2 J^2 - g = 0
    qa, qb, qc = k * k + k, -2.0 * k * k * J, k * k * J * J - g
    u_in = (-qb + jnp.sqrt(jnp.maximum(qb * qb - 4.0 * qa * qc, 0.0))) / (2.0 * qa)
    T_in = 1.0 - k * u_in * u_in / g
    p_in = T_in ** (g / (g - 1.0))
    inlet = jnp.stack([p_in / T_in, u_in, p_in])

    rn, un, pn = W[-1, 0], W[-1, 1], W[-1, 2]
    an = jnp.sqrt(g * pn / rn)
    rb = rn * (pb / pn) ** (1.0 / g)
    ab = jnp.sqrt(g * pb / rb)
    ub = un + (an - ab) / k
    outlet = jnp.where((un < an) | force_pb, jnp.stack([rb, ub, pb * jnp.ones_like(rb)]), W[-1])
    return inlet, outlet


def pad_nozzle(W: jax.Array, pb, g, force_pb=False) -> jax.Array:
    inlet, outlet = boundary_states(W, pb, g, force_pb)
    return jnp.concatenate([jnp.tile(inlet, (NG, 1)), W, jnp.tile(outlet, (NG, 1))])


# --- operator slot -----------------------------------------------------------------------------------------
@cache
def default_operator(reconstruct: Reconstruction, flux: Flux = hllc) -> Operator:
    """Reconstruction + flux at faces (times A_face), and the simple source p_i (A_{i+1/2} - A_{i-1/2}) / dx."""

    def operator(U, A_face, dx, gamma, W_pad, S):
        WL, WR, S_new = reconstruct_with_state(reconstruct, W_pad, gamma, S)
        F = flux(prim_to_cons(WL, gamma), prim_to_cons(WR, gamma), gamma) * A_face[:, None]
        return F, W_pad[NG:-NG, 2] * (A_face[1:] - A_face[:-1]) / dx, S_new

    return operator


def rhs_with_state(U, S, A, A_face, dx, pb, g, operator: Operator, force_pb=False):
    """(dU/dt, S_new): dU/dt = -(F[1:] - F[:-1]) / dx + [0, S_mom, 0], shape (n, 3), for U = (rho A, rho u A, E A),
    with limiter state S (n + 4, 3)."""
    W = cons_to_prim(U / A[:, None], g)
    F, S_mom, S_new = operator(U, A_face, dx, g, pad_nozzle(W, pb, g, force_pb), S)
    return (-(F[1:] - F[:-1]) / dx).at[:, 1].add(S_mom), S_new


def rhs(U, A, A_face, dx, pb, g, operator: Operator, force_pb=False) -> jax.Array:
    """dU/dt with zero limiter state, shape (n, 3)."""
    return rhs_with_state(U, initial_limiter_state(U.shape[0] + 2 * NG), A, A_face, dx, pb, g, operator, force_pb)[0]


def initial_state(grid: Grid, pb: float, g: float) -> jax.Array:
    """Initial guess U (n, 3); it depends on the geometry and the regime of p_b, never on the case's own solution.

    - p_crit2 < p_b <= p_crit1 (choked, shock inside): the exact flow with a standing shock in the middle of the
      divergent section (a different back pressure). Its exit is subsonic, so the imposed p_b moves the shock to
      its place; an isentropic guess has a supersonic exit and lets shocks near the exit escape.
    - p_b > p_crit1 (unchoked): the exact subsonic flow with throat Mach SUBSONIC_GUESS_MACH (a different back
      pressure). From the linear guess below, low-Mach subsonic cases often did not converge in 300 Newton steps.
    - otherwise: isentropic, p falling linearly from 1 at the inlet to p_b at the exit.
    """
    nz = grid.nozzle
    cp = critical_pressures(nz, g)
    pb_guess = None
    if cp.p_crit2 < pb <= cp.p_crit1:
        pb_guess = back_pressure_for_shock(nz, nz.x_throat + 0.5 * (nz.x_exit - nz.x_throat), g)
    elif pb > cp.p_crit1:
        a_star = nz.A_throat / float(area_ratio(SUBSONIC_GUESS_MACH, g))
        pb_guess = float(p_over_p0(mach_from_area_ratio(nz.A_exit / a_star, g, supersonic=False), g))
    if pb_guess is not None:
        prof = solve_nozzle(nz, pb_guess, g).profile(grid.x)
        W = np.stack([prof["rho"], prof["u"], prof["p"]], axis=1)
    else:
        s = (grid.x - nz.x_in) / (nz.x_exit - nz.x_in)
        p = 1.0 + (pb - 1.0) * s
        rho = p ** (1.0 / g)
        u = np.sqrt(np.maximum(2.0 * g / (g - 1.0) * (1.0 - p / rho), 0.0))
        W = np.stack([rho, u, p], axis=1)
    return prim_to_cons(jnp.asarray(W), g) * jnp.asarray(grid.A)[:, None]


@dataclass(frozen=True)
class SteadyResult:
    W: np.ndarray  # (n, 3) primitive state per unit area
    residuals: np.ndarray  # R_k / R_0 for k = 0 .. iterations
    iterations: int
    converged: bool
    limit_cycle: bool
    failed: bool  # non-physical state or NaN

    @property
    def orders(self) -> float:
        """Orders of magnitude of residual drop reached (best value over the run)."""
        return float(-np.log10(np.nanmin(self.residuals)))


def residual_norm(dU: jax.Array) -> jax.Array:
    return jnp.sqrt(jnp.sum(dU * dU))


def detect_limit_cycle(res: np.ndarray, converged: bool) -> bool:
    """Not converged, no net decrease over the last 10 % of iterations, and the residual still oscillates."""
    if converged or res.size < 100:
        return False
    w = res[-max(res.size // 10, 10) :]
    h = w.size // 2
    flat = np.median(w[h:]) >= 0.9 * np.median(w[:h])
    oscillating = np.max(w) > 1.01 * np.min(w)
    return bool(flat and oscillating)


def _physical(U, A, g):
    W = cons_to_prim(U / A[:, None], g)
    return jnp.all(jnp.isfinite(W)) & jnp.all(W[:, 0] > 0.0) & jnp.all(W[:, 2] > 0.0)


def _local_dt(U, A, dx, g, cfl):
    W = cons_to_prim(U / A[:, None], g)
    return cfl * dx / (jnp.abs(W[:, 1]) + jnp.sqrt(g * W[:, 2] / W[:, 0]))


# --- explicit pseudo-time ----------------------------------------------------------------------------------
@partial(jax.jit, static_argnames=("operator", "max_iters"))
def _explicit_loop(U0, A, A_face, dx, pb, g, cfl, force_pb, operator, max_iters):
    L = partial(rhs_with_state, A=A, A_face=A_face, dx=dx, pb=pb, g=g, operator=operator, force_pb=force_pb)
    S0 = initial_limiter_state(U0.shape[0] + 2 * NG)
    R0 = residual_norm(L(U0, S0)[0])
    hist = jnp.full(max_iters + 1, jnp.nan).at[0].set(R0)

    def body(state):
        U, S, k, hist, _ = state
        dt = _local_dt(U, A, dx, g, cfl)[:, None]
        dU, S_next = L(U, S)  # limiter state: fixed within the iteration, updated from its first stage
        U1 = U + dt * dU
        U2 = 0.75 * U + 0.25 * (U1 + dt * L(U1, S)[0])
        U3 = U / 3.0 + 2.0 / 3.0 * (U2 + dt * L(U2, S)[0])
        R = residual_norm(L(U3, S_next)[0])
        return U3, S_next, k + 1, hist.at[k + 1].set(R), _physical(U3, A, g) & jnp.isfinite(R)

    def cond(state):
        _, _, k, hist, ok = state
        return ok & (k < max_iters) & (hist[k] > CONVERGED * R0)

    U, _, k, hist, ok = jax.lax.while_loop(cond, body, (U0, S0, jnp.asarray(0), hist, jnp.asarray(True)))
    return U, k, hist, ok


def solve_explicit(grid: Grid, pb: float, g: float, operator: Operator, U0=None,
                   cfl: float = EXPLICIT_CFL, max_iters: int = EXPLICIT_MAX_ITERS) -> SteadyResult:
    """SSP-RK3 in pseudo-time with local time steps dt_i = cfl dx / (|u_i| + a_i)."""
    A, A_face = jnp.asarray(grid.A), jnp.asarray(grid.A_face)
    U0 = initial_state(grid, pb, g) if U0 is None else U0
    force = pressure_outlet(grid.nozzle, pb, g)
    U, k, hist, ok = _explicit_loop(U0, A, A_face, grid.dx, float(pb), float(g), float(cfl), force, operator,
                                    int(max_iters))
    k = int(k)
    res = np.asarray(hist[: k + 1])
    res = res / res[0]
    converged = bool(res[-1] <= CONVERGED)
    W = np.asarray(cons_to_prim(U / A[:, None], g))
    return SteadyResult(W, res, k, converged, detect_limit_cycle(res, converged), not bool(ok))


# --- implicit pseudo-time ----------------------------------------------------------------------------------
STENCIL = NG  # assumed half-width (cells) of the dependence of dU_i/dt on U_j; reconstructions only see NG ghosts


@cache
def _coloring(n: int, h: int = STENCIL) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Seed matrix (3n, 3(2h+1)), column colours (3n,) and band mask (3n, 3n) for a Jacobian whose cell i depends
    only on cells |i - j| <= h. Cells with the same colour are 2h+1 apart, so at most one is in any row's band."""
    period = 2 * h + 1
    cell = np.repeat(np.arange(n), 3)
    comp = np.tile(np.arange(3), n)
    colors = (cell % period) * 3 + comp
    seeds = np.zeros((3 * n, 3 * period))
    seeds[np.arange(3 * n), colors] = 1.0
    mask = np.abs(cell[:, None] - cell[None, :]) <= h
    return seeds, colors, mask


def colored_jacobian(f, u: jax.Array, n: int) -> jax.Array:
    """Exact dense Jacobian of f: R^{3n} -> R^{3n} from 3(2h+1) forward-mode products (banded dependence)."""
    seeds, colors, mask = _coloring(n)
    JS = jax.vmap(lambda v: jax.jvp(f, (u,), (v,))[1], in_axes=1, out_axes=1)(jnp.asarray(seeds))
    return jnp.where(jnp.asarray(mask), JS[:, jnp.asarray(colors)], 0.0)


@partial(jax.jit, static_argnames=("operator",))
def _implicit_step(U, S, A, A_face, dx, pb, g, cfl, force_pb, operator):
    """One backward-Euler step with the limiter state S held fixed (the Jacobian differentiates through U only).
    Returns (U_new, S_next, residual of U_new under S_next); S_next is computed at U."""
    n = U.shape[0]

    def flat(v, state):
        return rhs_with_state(v.reshape(n, 3), state, A, A_face, dx, pb, g, operator, force_pb)[0].reshape(-1)

    u = U.reshape(-1)
    J = colored_jacobian(lambda v: flat(v, S), u, n)
    dt = jnp.repeat(_local_dt(U, A, dx, g, cfl), 3)
    U_new = (u + jnp.linalg.solve(jnp.diag(1.0 / dt) - J, flat(u, S))).reshape(n, 3)
    S_next = rhs_with_state(U, S, A, A_face, dx, pb, g, operator, force_pb)[1]
    return U_new, S_next, residual_norm(flat(U_new.reshape(-1), S_next))


IMPLICIT_BACKTRACK = 0.25  # CFL factor after a rejected (non-physical) step
IMPLICIT_MAX_REJECTS = 12  # consecutive rejections before giving up


def solve_implicit(grid: Grid, pb: float, g: float, operator: Operator, U0=None,
                   cfl0: float = IMPLICIT_CFL0, cfl_max: float = IMPLICIT_CFL_MAX,
                   max_iters: int = IMPLICIT_MAX_ITERS) -> SteadyResult:
    """Backward-Euler pseudo-time with the exact Jacobian (dense LU) and the SER ramp
    CFL_k = min(cfl_max, s cfl0 R_0 / R_k). A step that gives a non-physical state is rejected and s is
    multiplied by IMPLICIT_BACKTRACK; each accepted step doubles s again up to 1. `iterations` counts every
    linear solve, rejected ones included; `residuals` holds the accepted steps."""
    A, A_face = jnp.asarray(grid.A), jnp.asarray(grid.A_face)
    U = initial_state(grid, pb, g) if U0 is None else U0
    force = pressure_outlet(grid.nozzle, pb, g)
    S = initial_limiter_state(U.shape[0] + 2 * NG)
    R0 = float(residual_norm(rhs(U, A, A_face, grid.dx, pb, g, operator, force)))
    res = [1.0]
    scale, rejects, solves, failed = 1.0, 0, 0, False
    while solves < max_iters and res[-1] > CONVERGED:
        cfl = min(cfl_max, scale * cfl0 / res[-1])
        U_new, S_next, R_new = _implicit_step(U, S, A, A_face, grid.dx, float(pb), float(g), cfl, force, operator)
        solves += 1
        if not bool(_physical(U_new, A, g)) or not np.isfinite(float(R_new)):
            rejects += 1
            scale *= IMPLICIT_BACKTRACK
            if rejects >= IMPLICIT_MAX_REJECTS:
                failed = True
                break
            continue
        rejects = 0
        scale = min(1.0, 2.0 * scale)
        U, S = U_new, S_next
        res.append(float(R_new) / R0)
    res_arr = np.asarray(res)
    converged = bool(res_arr[-1] <= CONVERGED)
    W = np.asarray(cons_to_prim(U / A[:, None], g))
    return SteadyResult(W, res_arr, solves, converged, detect_limit_cycle(res_arr, converged), failed)
