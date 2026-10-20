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

from .exact_nozzle import Nozzle, back_pressure_for_shock, critical_pressures, solve_nozzle
from .numerics import NG, Flux, Reconstruction, cons_to_prim, hllc, prim_to_cons

CONVERGED = 1e-12
EXPLICIT_CFL = 0.8
EXPLICIT_MAX_ITERS = 50_000
IMPLICIT_CFL0 = 1.0
IMPLICIT_CFL_MAX = 1e8
IMPLICIT_MAX_ITERS = 300

# operator(U, A_face, dx, gamma, W_padded) -> (F_face * A_face: (n + 1, 3), S_mom: (n,)); see euler1d_slots.md
Operator = Callable[[jax.Array, jax.Array, float, float, jax.Array], tuple[jax.Array, jax.Array]]


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

    def operator(U, A_face, dx, gamma, W_pad):
        WL, WR = reconstruct(W_pad, gamma)
        F = flux(prim_to_cons(WL, gamma), prim_to_cons(WR, gamma), gamma) * A_face[:, None]
        return F, W_pad[NG:-NG, 2] * (A_face[1:] - A_face[:-1]) / dx

    return operator


def rhs(U, A, A_face, dx, pb, g, operator: Operator, force_pb=False) -> jax.Array:
    """dU/dt = -(F[1:] - F[:-1]) / dx + [0, S_mom, 0], shape (n, 3), for U = (rho A, rho u A, E A)."""
    W = cons_to_prim(U / A[:, None], g)
    F, S = operator(U, A_face, dx, g, pad_nozzle(W, pb, g, force_pb))
    return (-(F[1:] - F[:-1]) / dx).at[:, 1].add(S)


def initial_state(grid: Grid, pb: float, g: float) -> jax.Array:
    """Initial guess U (n, 3); it depends on the geometry and the regime of p_b, never on the case's own solution.

    - p_crit2 < p_b <= p_crit1 (choked, shock inside): the exact flow with a standing shock in the middle of the
      divergent section (a different back pressure). Its exit is subsonic, so the imposed p_b moves the shock to
      its place; an isentropic guess has a supersonic exit and lets shocks near the exit escape.
    - otherwise: isentropic, p falling linearly from 1 at the inlet to p_b at the exit.
    """
    nz = grid.nozzle
    cp = critical_pressures(nz, g)
    if cp.p_crit2 < pb <= cp.p_crit1:
        x_g = nz.x_throat + 0.5 * (nz.x_exit - nz.x_throat)
        prof = solve_nozzle(nz, back_pressure_for_shock(nz, x_g, g), g).profile(grid.x)
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
    L = partial(rhs, A=A, A_face=A_face, dx=dx, pb=pb, g=g, operator=operator, force_pb=force_pb)
    R0 = residual_norm(L(U0))
    hist = jnp.full(max_iters + 1, jnp.nan).at[0].set(R0)

    def body(state):
        U, k, hist, _ = state
        dt = _local_dt(U, A, dx, g, cfl)[:, None]
        U1 = U + dt * L(U)
        U2 = 0.75 * U + 0.25 * (U1 + dt * L(U1))
        U3 = U / 3.0 + 2.0 / 3.0 * (U2 + dt * L(U2))
        R = residual_norm(L(U3))
        return U3, k + 1, hist.at[k + 1].set(R), _physical(U3, A, g) & jnp.isfinite(R)

    def cond(state):
        _, k, hist, ok = state
        return ok & (k < max_iters) & (hist[k] > CONVERGED * R0)

    U, k, hist, ok = jax.lax.while_loop(cond, body, (U0, jnp.asarray(0), hist, jnp.asarray(True)))
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
def _implicit_step(U, A, A_face, dx, pb, g, cfl, force_pb, operator):
    n = U.shape[0]
    flat = lambda v: rhs(v.reshape(n, 3), A, A_face, dx, pb, g, operator, force_pb).reshape(-1)  # noqa: E731
    u = U.reshape(-1)
    J = colored_jacobian(flat, u, n)
    dt = jnp.repeat(_local_dt(U, A, dx, g, cfl), 3)
    U_new = (u + jnp.linalg.solve(jnp.diag(1.0 / dt) - J, flat(u))).reshape(n, 3)
    return U_new, residual_norm(flat(U_new.reshape(-1)))


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
    R0 = float(residual_norm(rhs(U, A, A_face, grid.dx, pb, g, operator, force)))
    res = [1.0]
    scale, rejects, solves, failed = 1.0, 0, 0, False
    while solves < max_iters and res[-1] > CONVERGED:
        cfl = min(cfl_max, scale * cfl0 / res[-1])
        U_new, R_new = _implicit_step(U, A, A_face, grid.dx, float(pb), float(g), cfl, force, operator)
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
        U = U_new
        res.append(float(R_new) / R0)
    res_arr = np.asarray(res)
    converged = bool(res_arr[-1] <= CONVERGED)
    W = np.asarray(cons_to_prim(U / A[:, None], g))
    return SteadyResult(W, res_arr, solves, converged, detect_limit_cycle(res_arr, converged), failed)
