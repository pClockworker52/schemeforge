"""Exact steady quasi-1D nozzle flow with an optional normal shock (PLAN §9.2). NumPy float64.

Units: stagnation p0 = rho0 = 1 upstream, so a0 = sqrt(gamma) and T/T0 = (p/p0) / (rho/rho0). Lengths in throat units.
The nozzle has one throat (the minimum of A on [x_in, x_exit]); the inlet is subsonic.

Usage:
    nz = Nozzle(lambda x: 1 + 2.2 * (x - 1.5) ** 2, 0.0, 3.0, x_throat=1.5)
    sol = solve_nozzle(nz, pb=0.6784, gamma=1.4)
    sol.regime, sol.x_shock, sol.profile(x)   # profile: dict of (n,) arrays
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike
from scipy.optimize import brentq

from .gas import F64

_RTOL = 4.0 * np.finfo(float).eps
_XTOL = 1e-300


# --- isentropic and normal-shock relations -------------------------------------------------------------------
def area_ratio(M: ArrayLike, g: float) -> F64:
    """A/A* = (1/M) [(2/(g+1)) (1 + (g-1)/2 M^2)]^((g+1)/(2(g-1)))."""
    M = np.asarray(M, dtype=float)
    return (1.0 / M) * ((2.0 / (g + 1.0)) * (1.0 + 0.5 * (g - 1.0) * M * M)) ** ((g + 1.0) / (2.0 * (g - 1.0)))


def mach_from_area_ratio(ar: float, g: float, supersonic: bool) -> float:
    """Invert A/A* = ar >= 1 on the subsonic or supersonic branch."""
    if ar < 1.0:
        if ar < 1.0 - 1e-12:
            raise ValueError(f"A/A* = {ar} < 1 has no solution")
        return 1.0
    if ar == 1.0:
        return 1.0

    def h(M: float) -> float:
        return float(area_ratio(M, g)) - ar

    if supersonic:
        hi = 2.0
        while h(hi) < 0.0:
            hi *= 2.0
        return float(brentq(h, 1.0, hi, xtol=_XTOL, rtol=_RTOL, maxiter=500))
    return float(brentq(h, 1e-300, 1.0, xtol=_XTOL, rtol=_RTOL, maxiter=500))


def _base(M: ArrayLike, g: float) -> F64:
    M = np.asarray(M, dtype=float)
    return 1.0 + 0.5 * (g - 1.0) * M * M


def p_over_p0(M: ArrayLike, g: float) -> F64:
    return _base(M, g) ** (-g / (g - 1.0))


def rho_over_rho0(M: ArrayLike, g: float) -> F64:
    return _base(M, g) ** (-1.0 / (g - 1.0))


def T_over_T0(M: ArrayLike, g: float) -> F64:
    return 1.0 / _base(M, g)


def mach_from_p_over_p0(pr: float, g: float) -> float:
    """Isentropic Mach number from p/p0 in (0, 1]."""
    return float(np.sqrt(2.0 / (g - 1.0) * (pr ** (-(g - 1.0) / g) - 1.0)))


def shock_p_ratio(M1: float, g: float) -> float:
    """p2/p1 = 1 + 2g/(g+1) (M1^2 - 1)."""
    return 1.0 + 2.0 * g / (g + 1.0) * (M1 * M1 - 1.0)


def shock_mach2(M1: float, g: float) -> float:
    """M2 behind a normal shock: M2^2 = (1 + (g-1)/2 M1^2) / (g M1^2 - (g-1)/2)."""
    return float(np.sqrt((1.0 + 0.5 * (g - 1.0) * M1 * M1) / (g * M1 * M1 - 0.5 * (g - 1.0))))


def shock_p0_ratio(M1: float, g: float) -> float:
    """p02/p01 = [(g+1)M1^2 / ((g-1)M1^2 + 2)]^(g/(g-1)) [(g+1) / (2g M1^2 - (g-1))]^(1/(g-1))."""
    m2 = M1 * M1
    return ((g + 1.0) * m2 / ((g - 1.0) * m2 + 2.0)) ** (g / (g - 1.0)) * (
        (g + 1.0) / (2.0 * g * m2 - (g - 1.0))
    ) ** (1.0 / (g - 1.0))


# --- nozzle --------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Nozzle:
    """Area distribution A(x) on [x_in, x_exit] with a single throat at x_throat (A minimal there)."""

    area: Callable[[ArrayLike], ArrayLike]
    x_in: float
    x_exit: float
    x_throat: float

    @property
    def A_throat(self) -> float:
        return float(self.area(self.x_throat))

    @property
    def A_exit(self) -> float:
        return float(self.area(self.x_exit))


def anderson_nozzle() -> Nozzle:
    """Anderson (1995): A(x) = 1 + 2.2 (x - 1.5)^2 on [0, 3]."""
    return Nozzle(lambda x: 1.0 + 2.2 * (np.asarray(x, dtype=float) - 1.5) ** 2, 0.0, 3.0, 1.5)


@dataclass(frozen=True)
class CriticalPressures:
    """Back-pressure thresholds p_b/p0 (PLAN §9.2)."""

    p_crit1: float  # choked, exit on the subsonic branch (A* = A_t)
    p_crit2: float  # normal shock exactly at the exit
    p_crit3: float  # design condition, exit on the supersonic branch
    M_exit_sub: float
    M_exit_sup: float


def critical_pressures(nz: Nozzle, g: float) -> CriticalPressures:
    ar = nz.A_exit / nz.A_throat
    Ms = mach_from_area_ratio(ar, g, supersonic=False)
    Mp = mach_from_area_ratio(ar, g, supersonic=True)
    p3 = float(p_over_p0(Mp, g))
    return CriticalPressures(float(p_over_p0(Ms, g)), p3 * shock_p_ratio(Mp, g), p3, Ms, Mp)


@dataclass(frozen=True)
class NozzleSolution:
    nozzle: Nozzle
    gamma: float
    pb: float
    regime: str  # "subsonic" | "shock" | "supersonic"
    A_star_1: float  # sonic area upstream (of the shock)
    A_star_2: float  # sonic area downstream of the shock (= A_star_1 without a shock)
    x_shock: float | None
    M1: float | None  # Mach number just upstream of the shock
    p0_ratio: float  # p02/p01 (1 without a shock)

    @property
    def M_exit(self) -> float:
        return float(self.profile(np.array([self.nozzle.x_exit]))["M"][0])

    @property
    def mass_flow(self) -> float:
        """rho u A at the inlet; constant along the nozzle in the exact solution."""
        s = self.profile(np.array([self.nozzle.x_in]))
        return float(s["rho"][0] * s["u"][0] * s["A"][0])

    def profile(self, x: ArrayLike) -> dict[str, F64]:
        """Exact state at stations x (n,): M, p, rho, T, u, a, p0 (local stagnation pressure)."""
        x = np.atleast_1d(np.asarray(x, dtype=float))
        g, nz = self.gamma, self.nozzle
        A = np.asarray(nz.area(x), dtype=float) * np.ones_like(x)
        M = np.empty_like(x)
        p0 = np.ones_like(x)
        for i, (xi, Ai) in enumerate(zip(x, A, strict=True)):
            downstream = self.x_shock is not None and xi > self.x_shock
            A_star = self.A_star_2 if downstream else self.A_star_1
            supersonic = self.regime != "subsonic" and xi > nz.x_throat and not downstream
            M[i] = mach_from_area_ratio(Ai / A_star, g, supersonic)
            if downstream:
                p0[i] = self.p0_ratio
        p = p0 * p_over_p0(M, g)
        rho = p0 * rho_over_rho0(M, g)  # T0 is constant across the shock, so rho0 scales with p0
        T = T_over_T0(M, g)
        a = np.sqrt(g * T)
        return {"M": M, "p": p, "rho": rho, "T": T, "u": M * a, "a": a, "p0": p0, "A": A}


def back_pressure_for_shock(nz: Nozzle, x_shock: float, gamma: float) -> float:
    """p_b/p0 that places the normal shock at x_shock in (x_throat, x_exit]."""
    g, At, Ae = float(gamma), nz.A_throat, nz.A_exit
    M1 = mach_from_area_ratio(float(nz.area(x_shock)) / At, g, supersonic=True)
    r0 = shock_p0_ratio(M1, g)
    Me = mach_from_area_ratio(Ae / (At / r0), g, supersonic=False)
    return r0 * float(p_over_p0(Me, g))


def solve_nozzle(nz: Nozzle, pb: float, gamma: float) -> NozzleSolution:
    """Exact steady solution for back pressure pb (= p_b/p0, 0 < pb < 1)."""
    g = float(gamma)
    if not 0.0 < pb < 1.0:
        raise ValueError("need 0 < p_b/p0 < 1")
    cp = critical_pressures(nz, g)
    At, Ae = nz.A_throat, nz.A_exit

    if pb > cp.p_crit1:  # not choked: A* from the exit conditions
        A_star = Ae / float(area_ratio(mach_from_p_over_p0(pb, g), g))
        return NozzleSolution(nz, g, pb, "subsonic", A_star, A_star, None, None, 1.0)

    if pb <= cp.p_crit2:  # supersonic exit; any shocks stand outside the nozzle
        return NozzleSolution(nz, g, pb, "supersonic", At, At, None, None, 1.0)

    xs = float(brentq(lambda s: back_pressure_for_shock(nz, s, g) - pb, nz.x_throat, nz.x_exit,
                      xtol=1e-15, rtol=_RTOL, maxiter=500))
    M1 = mach_from_area_ratio(float(nz.area(xs)) / At, g, supersonic=True)
    r0 = shock_p0_ratio(M1, g)
    return NozzleSolution(nz, g, pb, "shock", At, At / r0, xs, M1, r0)
