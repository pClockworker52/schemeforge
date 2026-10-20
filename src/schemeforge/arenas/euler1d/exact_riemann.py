"""Exact solution of the Riemann problem for the 1D Euler equations (Toro 2009, ch. 4). NumPy float64.

Usage:
    sol = solve_riemann((1.0, 0.0, 1.0), (0.125, 0.0, 0.1), gamma=1.4)
    sol.p_star, sol.u_star
    W = sol.sample(x, t, x0=0.5)          # (n, 3) primitive [rho, u, p]
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike
from scipy.optimize import brentq

from .gas import F64, sound_speed

_RTOL = 4.0 * np.finfo(float).eps  # the smallest rtol brentq accepts
_XTOL = 1e-300


class VacuumError(ValueError):
    """The data generate a vacuum: (2/(gamma-1)) (aL + aR) <= uR - uL. Excluded from all families."""


@dataclass(frozen=True)
class Wave:
    """A left (side=-1) or right (side=+1) nonlinear wave.

    kind "shock": speeds = (S, S). kind "rarefaction": speeds = (head, tail).
    """

    side: int
    kind: str
    speeds: tuple[float, float]


@dataclass(frozen=True)
class RiemannSolution:
    WL: tuple[float, float, float]
    WR: tuple[float, float, float]
    gamma: float
    p_star: float
    u_star: float
    rho_star_L: float
    rho_star_R: float
    left: Wave
    right: Wave

    @property
    def contact_speed(self) -> float:
        return self.u_star

    def sample(self, x: ArrayLike, t: float, x0: float = 0.0) -> F64:
        """Primitive state (n, 3) at positions x (n,) and time t > 0, initial discontinuity at x0."""
        if t <= 0.0:
            raise ValueError("t must be positive")
        return self.sample_xi((np.asarray(x, dtype=float) - x0) / t)

    def sample_xi(self, xi: ArrayLike) -> F64:
        """Primitive state (n, 3) along rays xi = (x - x0) / t (Toro §4.5)."""
        xi = np.atleast_1d(np.asarray(xi, dtype=float))
        g = self.gamma
        out = np.empty((xi.size, 3))
        sides = ((self.left, self.WL, self.rho_star_L), (self.right, self.WR, self.rho_star_R))
        for wave, W, rho_star in sides:
            mask = (xi < self.u_star) if wave.side < 0 else (xi >= self.u_star)
            # Mirror the right side (x -> -x, u -> -u) onto the left-wave formulas: m = +1 left, -1 right.
            m = -wave.side
            rho, u, p = W
            a = float(sound_speed(rho, p, g))
            star = np.array([rho_star, self.u_star, self.p_star])
            s = m * xi[mask]
            res = np.empty((s.size, 3))
            if wave.kind == "shock":
                outside = s < m * wave.speeds[0]
                res[outside] = W
                res[~outside] = star
            else:
                head, tail = m * wave.speeds[0], m * wave.speeds[1]
                res[s <= head] = W
                res[s >= tail] = star
                fan = (s > head) & (s < tail)
                um, sf = m * u, s[fan]
                c = 2.0 / (g + 1.0) + (g - 1.0) / ((g + 1.0) * a) * (um - sf)  # Toro (4.56)
                res[fan, 0] = rho * c ** (2.0 / (g - 1.0))
                res[fan, 1] = m * 2.0 / (g + 1.0) * (a + 0.5 * (g - 1.0) * um + sf)
                res[fan, 2] = p * c ** (2.0 * g / (g - 1.0))
            out[mask] = res
        return out


def pressure_function(p: float, rho: float, pk: float, a: float, g: float) -> float:
    """f_K(p): Toro (4.6) shock branch for p > p_K, (4.7) rarefaction branch otherwise."""
    if p > pk:
        A = 2.0 / ((g + 1.0) * rho)
        B = (g - 1.0) / (g + 1.0) * pk
        return (p - pk) * np.sqrt(A / (p + B))
    return 2.0 * a / (g - 1.0) * ((p / pk) ** ((g - 1.0) / (2.0 * g)) - 1.0)


def solve_riemann(WL: ArrayLike, WR: ArrayLike, gamma: float) -> RiemannSolution:
    """Exact Riemann solution for primitive states WL, WR = (rho, u, p). Raises VacuumError for vacuum data."""
    rhoL, uL, pL = (float(v) for v in WL)
    rhoR, uR, pR = (float(v) for v in WR)
    g = float(gamma)
    if min(rhoL, rhoR, pL, pR) <= 0.0:
        raise ValueError("density and pressure must be positive")
    aL, aR = float(sound_speed(rhoL, pL, g)), float(sound_speed(rhoR, pR, g))
    du = uR - uL
    if 2.0 / (g - 1.0) * (aL + aR) <= du:
        raise VacuumError("initial data generate a vacuum")

    def f(p: float) -> float:
        return pressure_function(p, rhoL, pL, aL, g) + pressure_function(p, rhoR, pR, aR, g) + du

    # f is increasing in p and f(0+) < 0 when there is no vacuum; grow the upper bracket until f > 0.
    hi = max(pL, pR)
    while f(hi) <= 0.0:
        hi *= 4.0
    p_star = float(brentq(f, _XTOL, hi, xtol=_XTOL, rtol=_RTOL, maxiter=500))
    fL = pressure_function(p_star, rhoL, pL, aL, g)
    fR = pressure_function(p_star, rhoR, pR, aR, g)
    u_star = 0.5 * (uL + uR) + 0.5 * (fR - fL)

    gm = (g - 1.0) / (g + 1.0)
    waves: list[Wave] = []
    rho_stars: list[float] = []
    for side, rho, u, p, a in ((-1, rhoL, uL, pL, aL), (+1, rhoR, uR, pR, aR)):
        ratio = p_star / p
        if p_star > p:  # shock, Toro (4.50)-(4.52), (4.57)-(4.59)
            rho_stars.append(rho * (ratio + gm) / (gm * ratio + 1.0))
            S = u + side * a * np.sqrt((g + 1.0) / (2.0 * g) * ratio + (g - 1.0) / (2.0 * g))
            waves.append(Wave(side, "shock", (float(S), float(S))))
        else:  # rarefaction, Toro (4.53)-(4.55), (4.60)-(4.62)
            rho_stars.append(rho * ratio ** (1.0 / g))
            a_star = a * ratio ** ((g - 1.0) / (2.0 * g))
            waves.append(Wave(side, "rarefaction", (u + side * a, u_star + side * a_star)))

    return RiemannSolution(
        WL=(rhoL, uL, pL),
        WR=(rhoR, uR, pR),
        gamma=g,
        p_star=p_star,
        u_star=float(u_star),
        rho_star_L=float(rho_stars[0]),
        rho_star_R=float(rho_stars[1]),
        left=waves[0],
        right=waves[1],
    )
