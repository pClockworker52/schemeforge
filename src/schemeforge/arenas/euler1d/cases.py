"""Arena 1 cases: the dev suite (PLAN §9.5) and the case YAML format (docs/judge/euler1d_cases.md).

Every case has an exact reference. Held-out families (RF*, NF*) are generated in families.py from the secret seed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from .exact_nozzle import Nozzle, anderson_nozzle, back_pressure_for_shock, mach_from_area_ratio
from .exact_nozzle import shock_mach2 as _shock_mach2
from .exact_nozzle import shock_p_ratio as _shock_p_ratio
from .gas import sound_speed


@dataclass(frozen=True)
class RiemannCase:
    id: str
    left: tuple[float, float, float]
    right: tuple[float, float, float]
    t_end: float
    n: int
    gamma: float = 1.4
    x0: float = 0.5
    domain: tuple[float, float] = (0.0, 1.0)
    kind: str = field(default="riemann", init=False)


@dataclass(frozen=True)
class SmoothCase:
    """rho = 1 + amp sin(2 pi x), u = u0, p = 1 on the periodic unit interval; exact = pure translation."""

    id: str
    ns: tuple[int, ...]
    t_end: float = 1.0
    amp: float = 0.2
    u0: float = 1.0
    gamma: float = 1.4
    kind: str = field(default="smooth", init=False)


@dataclass(frozen=True)
class NozzleSpec:
    """Geometry, throat area 1.

    - 'anderson': A = 1 + 2.2 (x - 1.5)^2 on [0, 3] (x_in is ignored).
    - 'parabolic': throat at x = 1; parabolic convergent part A = 1 + (inlet_ratio - 1)(1 - x)^2 and parabolic
      divergent part A = 1 + (area_ratio - 1)((x - 1)/length)^2.
    - 'conical': same convergent part; smoothed-conical divergent part with radius
      r = 1 + k (sqrt(d^2 + delta^2) - delta), d = x - 1, delta = 0.2, k chosen so that r(length)^2 = area_ratio.
    x_in (default 0) moves the inlet inside or before the convergent part; the families use it to shift the grid.
    """

    type: str = "anderson"
    area_ratio: float = 5.95
    length: float = 1.5
    inlet_ratio: float = 2.0
    x_in: float = 0.0

    def build(self) -> Nozzle:
        if self.type == "anderson":
            return anderson_nozzle()
        ci, cd, L = self.inlet_ratio - 1.0, self.area_ratio - 1.0, self.length
        if self.type == "parabolic":

            def area(x):
                x = np.asarray(x, dtype=float)
                return np.where(x < 1.0, 1.0 + ci * (1.0 - x) ** 2, 1.0 + cd * ((x - 1.0) / L) ** 2)

        elif self.type == "conical":
            delta = 0.2
            k = (np.sqrt(self.area_ratio) - 1.0) / (np.sqrt(L * L + delta * delta) - delta)

            def area(x):
                x = np.asarray(x, dtype=float)
                r = 1.0 + k * (np.sqrt((x - 1.0) ** 2 + delta * delta) - delta)
                return np.where(x < 1.0, 1.0 + ci * (1.0 - x) ** 2, r * r)

        else:
            raise ValueError(f"unknown nozzle type {self.type!r}")
        return Nozzle(area, float(self.x_in), 1.0 + L, 1.0)


@dataclass(frozen=True)
class NozzleCase:
    id: str
    pb: float
    n: int
    gamma: float = 1.4
    nozzle: NozzleSpec = NozzleSpec()
    kind: str = field(default="nozzle", init=False)


@dataclass(frozen=True)
class NozzleSweepCase:
    """Several back pressures on one nozzle and grid (smoothness metrics, PLAN §9.6)."""

    id: str
    pbs: tuple[float, ...]
    n: int
    gamma: float = 1.4
    nozzle: NozzleSpec = NozzleSpec()
    solvers: tuple[str, ...] = ("implicit",)
    kind: str = field(default="nozzle_sweep", init=False)


@dataclass(frozen=True)
class ReferenceCase:
    """Unsteady case without an exact solution, scored against a cached fine-grid reference in references/."""

    id: str
    init: str  # name of an initial-data function in INITS
    n: int
    t_end: float
    domain: tuple[float, float]
    reference: str  # file name in references/
    gamma: float = 1.4
    kind: str = field(default="reference", init=False)


def shu_osher_initial(x: np.ndarray) -> np.ndarray:
    """Shu & Osher (1989): Mach 3 shock at x = -4 running into rho = 1 + 0.2 sin(5x), on [-5, 5]."""
    left = np.array([3.857143, 2.629369, 10.333333])
    right = np.stack([1.0 + 0.2 * np.sin(5.0 * x), np.zeros_like(x), np.ones_like(x)], axis=1)
    return np.where((x < -4.0)[:, None], left, right)


INITS = {"shu_osher": shu_osher_initial}
REFERENCES_DIR = Path(__file__).parent / "references"


def load_reference(case: ReferenceCase) -> np.ndarray:
    """Reference primitive state averaged onto the case grid (n, 3). The fine grid must be a multiple of n."""
    W = np.load(REFERENCES_DIR / case.reference)["W"]
    if W.shape[0] % case.n:
        raise ValueError(f"reference grid {W.shape[0]} is not a multiple of n = {case.n}")
    return W.reshape(case.n, W.shape[0] // case.n, 3).mean(axis=1)


Case = RiemannCase | SmoothCase | NozzleCase | NozzleSweepCase | ReferenceCase


def slowly_moving_shock(mach: float = 3.0, speed_frac: float = 0.05, gamma: float = 1.4):
    """Left (post-shock) and right (pre-shock) states of a right-moving shock with speed
    s = speed_frac * max(|u| + a) over both states, pre-shock state (1, 0-ish, 1). Exact by Rankine-Hugoniot."""
    g = gamma
    rho1, p1 = 1.0, 1.0
    a1 = float(sound_speed(rho1, p1, g))
    # shock frame: pre-shock gas flows in from the right at -mach * a1
    p2 = p1 * _shock_p_ratio(mach, g)
    rho2 = rho1 * (g + 1.0) * mach**2 / ((g - 1.0) * mach**2 + 2.0)
    w1 = -mach * a1
    w2 = w1 * rho1 / rho2
    s = 0.0
    for _ in range(100):  # fixed point for s = frac * max(|u| + a) in the lab frame, u = w + s
        u1, u2 = w1 + s, w2 + s
        s_new = speed_frac * max(abs(u1) + a1, abs(u2) + float(sound_speed(rho2, p2, g)))
        if abs(s_new - s) < 1e-15:
            break
        s = s_new
    assert abs(_shock_mach2(mach, g) - abs(w2) / float(sound_speed(rho2, p2, g))) < 1e-12
    return (rho2, w2 + s, p2), (rho1, w1 + s, p1), s


def _n4_back_pressures(n_points: int = 11, n_cells: int = 120, cells_crossed: float = 30.0) -> tuple[float, ...]:
    """Back pressures that move the Anderson-nozzle shock over about `cells_crossed` cells around x = 2.1."""
    nz = anderson_nozzle()
    dx = (nz.x_exit - nz.x_in) / n_cells
    xs = np.linspace(2.1 - 0.5 * cells_crossed * dx, 2.1 + 0.5 * cells_crossed * dx, n_points)
    return tuple(float(back_pressure_for_shock(nz, x, 1.4)) for x in xs)


def dev_suite() -> list[Case]:
    """The fixed dev suite of PLAN §9.5."""
    r6_left, r6_right, _ = slowly_moving_shock()
    return [
        RiemannCase("R1", (1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 0.2, 200),
        RiemannCase("R2", (1.0, -2.0, 0.4), (1.0, 2.0, 0.4), 0.15, 200),
        RiemannCase("R3", (1.0, 0.0, 1000.0), (1.0, 0.0, 0.01), 0.012, 200),
        RiemannCase("R4", (5.99924, 19.5975, 460.894), (5.99242, -6.19633, 46.0950), 0.035, 200, x0=0.4),
        RiemannCase("R5", (1.4, 0.0, 1.0), (1.0, 0.0, 1.0), 2.0, 100),
        RiemannCase("R6", r6_left, r6_right, 0.95, 200, x0=0.2),
        ReferenceCase("R7", "shu_osher", 400, 1.8, (-5.0, 5.0), "shu_osher_weno5z_hllc_N12800.npz"),
        SmoothCase("S1", (50, 100, 200)),
        NozzleCase("N1", 0.6784, 120),
        NozzleCase("N2", 0.995, 120),
        NozzleCase("N3", 0.01, 120),
        NozzleSweepCase("N4", _n4_back_pressures(), 120),
    ]


# --- YAML -------------------------------------------------------------------------------------------------
def case_from_dict(d: dict[str, Any]) -> Case:
    d = dict(d)
    kind = d.pop("kind")
    if kind == "riemann":
        for k in ("left", "right", "domain"):
            if k in d:
                d[k] = tuple(float(v) for v in d[k])
        return RiemannCase(**d)
    if kind == "smooth":
        d["ns"] = tuple(int(v) for v in d["ns"])
        return SmoothCase(**d)
    if kind in ("nozzle", "nozzle_sweep"):
        if "nozzle" in d:
            d["nozzle"] = NozzleSpec(**d["nozzle"])
        if kind == "nozzle":
            return NozzleCase(**d)
        d["pbs"] = tuple(float(v) for v in d["pbs"])
        if "solvers" in d:
            d["solvers"] = tuple(d["solvers"])
        return NozzleSweepCase(**d)
    raise ValueError(f"unknown case kind {kind!r}")


def load_case(path: Path | str) -> Case:
    with open(path, encoding="utf-8") as fh:
        return case_from_dict(yaml.safe_load(fh))


def validate_case(case: Case) -> None:
    """Admissibility checks: positive states, no vacuum, valid nozzle back pressure, sane grids."""
    if isinstance(case, RiemannCase):
        from .exact_riemann import solve_riemann

        sol = solve_riemann(case.left, case.right, case.gamma)  # raises on vacuum or non-positive states
        if not (case.domain[0] < case.x0 < case.domain[1]) or case.t_end <= 0 or case.n < 10:
            raise ValueError("bad domain, x0, t_end or n")
        # Only waves of nonzero strength must stay inside (R5 and R6 have zero-strength waves).
        speeds = [0.0]  # x0 itself must lie inside the domain
        if abs(sol.rho_star_L / sol.rho_star_R - 1.0) > 1e-12:
            speeds.append(sol.u_star)
        for wave, W in ((sol.left, case.left), (sol.right, case.right)):
            if abs(sol.p_star / W[2] - 1.0) > 1e-12:
                speeds.extend(wave.speeds)
        lo = case.x0 + min(speeds) * case.t_end
        hi = case.x0 + max(speeds) * case.t_end
        if lo <= case.domain[0] or hi >= case.domain[1]:
            raise ValueError("waves reach the boundary before t_end")
    elif isinstance(case, (NozzleCase, NozzleSweepCase)):
        nz = case.nozzle.build()
        mach_from_area_ratio(nz.A_exit / nz.A_throat, case.gamma, supersonic=True)
        pbs = (case.pb,) if isinstance(case, NozzleCase) else case.pbs
        if not all(0.0 < p < 1.0 for p in pbs) or case.n < 10:
            raise ValueError("need 0 < pb < 1 and n >= 10")
