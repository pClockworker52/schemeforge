"""Arena 1 metrics (PLAN §9.6). Pure NumPy functions of numerical results and exact solutions; lower is better
unless noted. Definitions are mirrored in docs/judge/euler1d_spec.md §7."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import quad

from .exact_nozzle import Nozzle, NozzleSolution
from .exact_riemann import RiemannSolution
from .gas import entropy, sound_speed

EXCLUDE_CELLS = 5  # cells excluded on each side of a discontinuity in smooth-region errors
LEVEL_LO, LEVEL_HI = 0.05, 0.95
NOZZLE_WINDOW = 12  # half-width in cells of the window around a nozzle shock


# --- discontinuities of an exact Riemann solution -----------------------------------------------------------
@dataclass(frozen=True)
class Jump:
    kind: str  # "shock" | "contact"
    x: float  # position at t_end
    lo: float  # window: the jump is the only feature in (lo, hi)
    hi: float
    var: int  # 2 (pressure) for shocks, 0 (density) for contacts
    a: float  # state value left of the jump
    b: float  # state value right of the jump


def riemann_jumps(sol: RiemannSolution, x0: float, t: float, domain: tuple[float, float]) -> list[Jump]:
    """Shocks and contacts of nonzero strength at time t, each with a window bounded by the neighbouring features."""
    strong = []
    for wave, W in ((sol.left, sol.WL), (sol.right, sol.WR)):
        if abs(sol.p_star / W[2] - 1.0) > 1e-12:
            strong.append(wave)
    features = sorted(x0 + s * t for w in strong for s in w.speeds)
    has_contact = abs(sol.rho_star_L / sol.rho_star_R - 1.0) > 1e-12
    if has_contact:
        features = sorted([*features, x0 + sol.u_star * t])

    def window(x: float) -> tuple[float, float]:
        left = [f for f in features if f < x - 1e-14]
        right = [f for f in features if f > x + 1e-14]
        lo = 0.5 * (x + left[-1]) if left else domain[0]
        hi = 0.5 * (x + right[0]) if right else domain[1]
        return lo, hi

    jumps = []
    for wave, W in ((sol.left, sol.WL), (sol.right, sol.WR)):
        if wave.kind == "shock" and wave in strong:
            x = x0 + wave.speeds[0] * t
            lo, hi = window(x)
            a, b = (W[2], sol.p_star) if wave.side < 0 else (sol.p_star, W[2])
            jumps.append(Jump("shock", x, lo, hi, 2, a, b))
    if has_contact:
        x = x0 + sol.u_star * t
        lo, hi = window(x)
        jumps.append(Jump("contact", x, lo, hi, 0, sol.rho_star_L, sol.rho_star_R))
    return sorted(jumps, key=lambda j: j.x)


# --- generic jump measures ------------------------------------------------------------------------------------
def jump_width(x: np.ndarray, q: np.ndarray, a: float, b: float, dx: float) -> float:
    """Cells between the LEVEL_LO and LEVEL_HI crossings of f = (q - a)/(b - a) in a window ordered left to right.
    Returns the window width in cells if the profile never completes the transition."""
    f = (q - a) / (b - a)
    above = np.nonzero(f >= LEVEL_HI)[0]
    if above.size == 0:
        return float(x.size)
    i_hi = int(above[0])
    below = np.nonzero(f[:i_hi] <= LEVEL_LO)[0]
    if below.size == 0 or i_hi == 0:
        return float(x.size)
    i_lo = int(below[-1])
    x_lo = np.interp(LEVEL_LO, f[i_lo : i_lo + 2], x[i_lo : i_lo + 2])
    x_hi = np.interp(LEVEL_HI, f[i_hi - 1 : i_hi + 1], x[i_hi - 1 : i_hi + 1])
    return float(max(x_hi - x_lo, 0.0) / dx)


def overshoot(q: np.ndarray, q_exact: np.ndarray, jump: float) -> float:
    """Largest excursion of q beyond the range of the exact values in the window, divided by |jump|."""
    over = max(0.0, float(np.max(q - np.max(q_exact))), float(np.min(q_exact) - np.min(q)))
    return over / abs(jump)


def l1_smooth(x: np.ndarray, W: np.ndarray, W_exact: np.ndarray, jump_x: list[float], dx: float,
              scales: tuple[float, float, float]) -> float:
    """Mean over rho, u, p of the L1 error (mean |error| / scale) on cells farther than EXCLUDE_CELLS from jumps."""
    mask = np.ones(x.size, bool)
    for xj in jump_x:
        mask &= np.abs(x - xj) > EXCLUDE_CELLS * dx
    if not mask.any():
        return float("nan")
    errs = [np.mean(np.abs(W[mask, k] - W_exact[mask, k])) / scales[k] for k in range(3)]
    return float(np.mean(errs))


def state_scales(W_exact: np.ndarray, gamma: float) -> tuple[float, float, float]:
    """rho and p: max |value|; u: max (|u| + a), so that flows at rest still have a velocity scale."""
    a = sound_speed(W_exact[:, 0], W_exact[:, 2], gamma)
    return (float(np.max(np.abs(W_exact[:, 0]))), float(np.max(np.abs(W_exact[:, 1]) + a)),
            float(np.max(np.abs(W_exact[:, 2]))))


def total_variation(q: np.ndarray) -> float:
    return float(np.sum(np.abs(np.diff(q))))


def tv_increase(W: np.ndarray, W_exact: np.ndarray) -> float:
    """Largest relative excess of the numerical total variation over the exact one, for rho and p."""
    out = 0.0
    for k in (0, 2):
        tv_ex = total_variation(W_exact[:, k])
        if tv_ex > 0:
            out = max(out, (total_variation(W[:, k]) - tv_ex) / tv_ex)
    return max(out, 0.0)


# --- Riemann case metrics -------------------------------------------------------------------------------------
def riemann_metrics(x: np.ndarray, W: np.ndarray, sol: RiemannSolution, x0: float, t: float,
                    domain: tuple[float, float], dx: float) -> dict[str, float]:
    W_exact = sol.sample(x, t, x0)
    jumps = riemann_jumps(sol, x0, t, domain)
    out = {
        "l1_smooth": l1_smooth(x, W, W_exact, [j.x for j in jumps], dx, state_scales(W_exact, sol.gamma)),
        "tv_increase": tv_increase(W, W_exact),
    }
    widths: dict[str, list[float]] = {"shock": [], "contact": []}
    overs: list[float] = []
    for j in jumps:
        m = (x > j.lo) & (x < j.hi)
        if m.sum() < 4:
            continue
        widths[j.kind].append(jump_width(x[m], W[m, j.var], j.a, j.b, dx))
        overs.append(overshoot(W[m, j.var], W_exact[m, j.var], j.b - j.a))
    if widths["shock"]:
        out["shock_width"] = float(np.mean(widths["shock"]))
    if widths["contact"]:
        out["contact_width"] = float(np.mean(widths["contact"]))
    if overs:
        out["overshoot"] = float(np.max(overs))
    return out


def smooth_order(errors: list[float], ns: tuple[int, ...]) -> float:
    """Observed order between the coarsest and finest grid (higher is better)."""
    return float(np.log(errors[0] / errors[-1]) / np.log(ns[-1] / ns[0]))


# --- nozzle metrics -------------------------------------------------------------------------------------------
def nozzle_shock_position(x: np.ndarray, p: np.ndarray, p_mid: float) -> float:
    """Position where p first rises through p_mid downstream of its minimum (linear interpolation)."""
    i_min = int(np.argmin(p))
    rise = np.nonzero(p[i_min:] > p_mid)[0]
    if rise.size == 0:
        return float(x[-1])
    i = i_min + int(rise[0])
    return float(np.interp(p_mid, p[i - 1 : i + 1], x[i - 1 : i + 1]))


def nozzle_metrics(x: np.ndarray, W: np.ndarray, A: np.ndarray, exact: NozzleSolution, dx: float) -> dict[str, float]:
    g = exact.gamma
    prof = exact.profile(x)
    W_exact = np.stack([prof["rho"], prof["u"], prof["p"]], axis=1)
    jump_x = [exact.x_shock] if exact.x_shock is not None else []
    mdot = W[:, 0] * W[:, 1] * A
    h0 = g / (g - 1.0) * W[:, 2] / W[:, 0] + 0.5 * W[:, 1] ** 2
    h0_exact = g / (g - 1.0)  # T0 = 1
    smooth = np.ones(x.size, bool)
    for xj in jump_x:
        smooth &= np.abs(x - xj) > EXCLUDE_CELLS * dx
    s_rise = entropy(W[smooth, 0], W[smooth, 2], g) - entropy(W_exact[smooth, 0], W_exact[smooth, 2], g)
    out = {
        "l1_smooth": l1_smooth(x, W, W_exact, jump_x, dx, state_scales(W_exact, g)),
        "mdot_var": float(np.max(np.abs(mdot / exact.mass_flow - 1.0))),
        "h0_var": float(np.max(np.abs(h0 / h0_exact - 1.0))),
        "entropy_spurious": float(max(0.0, np.max(s_rise))) if s_rise.size else 0.0,
    }
    if exact.x_shock is not None:
        pa = exact.profile([exact.x_shock])["p"][0]  # upstream state (the shock point takes the upstream value)
        pb = exact.profile([exact.x_shock + 1e-9])["p"][0]
        out["shock_pos_err"] = abs(nozzle_shock_position(x, W[:, 2], 0.5 * (pa + pb)) - exact.x_shock) / dx
        m = np.abs(x - exact.x_shock) < NOZZLE_WINDOW * dx
        out["shock_width"] = jump_width(x[m], W[m, 2], pa, pb, dx)
        out["overshoot"] = overshoot(W[m, 2], W_exact[m, 2], pb - pa)
    return out


def wall_force_numerical(W: np.ndarray, A_face: np.ndarray, x: np.ndarray, x_throat: float) -> float:
    """J = sum over divergent cells of p_i (A_{i+1/2} - A_{i-1/2}) (axial wall force on the divergent section)."""
    div = x > x_throat
    return float(np.sum(W[div, 2] * (A_face[1:] - A_face[:-1])[div]))


def wall_force_exact(exact: NozzleSolution, nz: Nozzle, x_from: float) -> float:
    """J = integral of p dA/dx over [x_from, x_exit] for the exact profile (split at the shock)."""
    h = 1e-6

    def dAdx(x):
        return (float(nz.area(x + h)) - float(nz.area(x - h))) / (2 * h)

    def integrand(x):
        return float(exact.profile([x])["p"][0]) * dAdx(x)

    pts = [x_from, nz.x_exit]
    if exact.x_shock is not None and x_from < exact.x_shock < nz.x_exit:
        pts = [x_from, exact.x_shock, nz.x_exit]
    segments = zip(pts, pts[1:], strict=False)
    return float(sum(quad(integrand, a, b, epsabs=1e-13, epsrel=1e-12, limit=200)[0] for a, b in segments))


def roughness(J_num: np.ndarray, J_exact: np.ndarray) -> float:
    """RMS second difference of (J_num - J_exact) over the sweep divided by the RMS second difference of J_exact."""
    d_err = np.diff(np.asarray(J_num) - np.asarray(J_exact), 2)
    d_ex = np.diff(np.asarray(J_exact), 2)
    return float(np.sqrt(np.mean(d_err**2)) / np.sqrt(np.mean(d_ex**2)))
