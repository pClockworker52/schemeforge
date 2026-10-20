"""Held-out case families (PLAN §9.5), generated deterministically from the secret seed.

The seed lives outside the repo at ~/.schemeforge/heldout_seed (Claude Code is denied access). There is no
override: every function takes the seed explicitly, and the promo suite reads only that file. Instance
parameters never leave the judge: reports carry family aggregates only (evaluate.py, core/evaluation.py).
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

import numpy as np

from .cases import Case, NozzleCase, NozzleSpec, NozzleSweepCase, RiemannCase, slowly_moving_shock, validate_case
from .exact_nozzle import area_ratio, back_pressure_for_shock, critical_pressures, mach_from_area_ratio, p_over_p0
from .exact_riemann import VacuumError, solve_riemann
from .gas import GAMMA_STRESS, GAMMAS, sound_speed

SEED_FILE = Path.home() / ".schemeforge" / "heldout_seed"
FAMILY_SIZES = {"RF1": 20, "RF2": 10, "NF1": 20, "NF2": 10, "NF3": 5}
ALL_GAMMAS = (*GAMMAS, GAMMA_STRESS)
N_RIEMANN = 200
N_NOZZLE = 120


def read_seed(path: Path | None = None) -> str:
    seed = (path or SEED_FILE).read_text(encoding="utf-8").strip()
    if len(seed) < 16:
        raise ValueError("held-out seed is missing or too short")
    return seed


def seed_fingerprint(seed: str) -> str:
    """Identifies the seed in reports without revealing it."""
    return hashlib.sha256(f"schemeforge-seed:{seed}".encode()).hexdigest()[:16]


def _rng(seed: str, family: str, index: int) -> np.random.Generator:
    digest = hashlib.sha256(f"{seed}:{family}:{index}".encode()).digest()
    return np.random.Generator(np.random.PCG64(int.from_bytes(digest, "big")))


def _riemann_t_end(left, right, g, x0: float, room: float) -> float:
    """End time at which the fastest nontrivial feature has travelled `room` (domain is [0, 1])."""
    sol = solve_riemann(left, right, g)
    speeds = [abs(sol.u_star)]
    for wave, W in ((sol.left, left), (sol.right, right)):
        if abs(sol.p_star / W[2] - 1.0) > 1e-12:
            speeds += [abs(s) for s in wave.speeds]
    return room / max(max(speeds), 1e-12)


def rf1(seed: str, i: int) -> RiemannCase:
    """Random Riemann problems: pressure ratio 10^0.5..10^5, density ratio 0.1..10, no vacuum, gamma from §9.1."""
    rng = _rng(seed, "RF1", i)
    for _ in range(1000):
        g = float(rng.choice(ALL_GAMMAS))
        rp = 10.0 ** rng.uniform(0.5, 5.0)
        rr = 10.0 ** rng.uniform(-1.0, 1.0)
        pL, pR = (1.0, 1.0 / rp) if rng.random() < 0.5 else (1.0 / rp, 1.0)
        rhoL, rhoR = 1.0, rr
        a_ref = max(float(sound_speed(rhoL, pL, g)), float(sound_speed(rhoR, pR, g)))
        uL, uR = (float(v) for v in rng.uniform(-1.0, 1.0, 2) * a_ref)
        try:
            t_end = _riemann_t_end((rhoL, uL, pL), (rhoR, uR, pR), g, 0.5, 0.45)
        except VacuumError:
            continue
        case = RiemannCase(f"RF1-{i:03d}", (rhoL, uL, pL), (rhoR, uR, pR), t_end, N_RIEMANN, gamma=g)
        validate_case(case)
        return case
    raise RuntimeError("RF1: could not draw an admissible instance")


def rf2(seed: str, i: int) -> RiemannCase:
    """Slowly moving shocks: shock Mach 1.5..10, shock speed 0..0.2 of the maximum wave speed."""
    rng = _rng(seed, "RF2", i)
    g = float(rng.choice(ALL_GAMMAS))
    left, right, _ = slowly_moving_shock(float(rng.uniform(1.5, 10.0)), float(rng.uniform(0.0, 0.2)), g)
    vmax = max(abs(left[1]) + float(sound_speed(left[0], left[2], g)),
               abs(right[1]) + float(sound_speed(right[0], right[2], g)))
    case = RiemannCase(f"RF2-{i:03d}", left, right, 0.6 / vmax, N_RIEMANN, gamma=g, x0=0.3)
    validate_case(case)
    return case


def _geometry(rng: np.random.Generator) -> NozzleSpec:
    return NozzleSpec(
        type=str(rng.choice(["parabolic", "conical"])),
        area_ratio=float(rng.uniform(2.0, 10.0)),
        length=float(rng.uniform(2.0, 4.0)),
        inlet_ratio=float(rng.uniform(1.5, 3.0)),
    )


def _shift_inlet(spec: NozzleSpec, x_shock: float, frac: float, n: int) -> NozzleSpec:
    """Move the inlet so that (x_shock - x_in)/dx = k + frac with dx = (x_exit - x_in)/n (k from the unshifted grid)."""
    x_exit = 1.0 + spec.length
    k = math.floor(x_shock / (x_exit / n))
    D = (x_exit - x_shock) / (1.0 - (k + frac) / n)
    return NozzleSpec(spec.type, spec.area_ratio, spec.length, spec.inlet_ratio, x_in=x_exit - D)


def nf1(seed: str, i: int) -> NozzleCase:
    """Nozzles with a shock at 15..90 % of the divergent length, landing at a random fraction of a cell."""
    rng = _rng(seed, "NF1", i)
    spec = _geometry(rng)
    g = float(rng.choice(ALL_GAMMAS))
    x_shock = 1.0 + float(rng.uniform(0.15, 0.9)) * spec.length
    pb = back_pressure_for_shock(spec.build(), x_shock, g)
    spec = _shift_inlet(spec, x_shock, float(rng.uniform(0.0, 1.0)), N_NOZZLE)
    case = NozzleCase(f"NF1-{i:03d}", pb, N_NOZZLE, gamma=g, nozzle=spec)
    validate_case(case)
    return case


def nf2(seed: str, i: int) -> NozzleCase:
    """Shock-free nozzles, half each: subsonic with throat Mach 0.3..0.9 (unchoked), or supersonic exit
    (p_b below p_crit2). Drawing p_b between p_crit1 and 1 instead gives exit Mach ~0.02 for large area ratios,
    where every upwind scheme fails by low-Mach dissipation alone."""
    rng = _rng(seed, "NF2", i)
    spec = _geometry(rng)
    g = float(rng.choice(ALL_GAMMAS))
    nz = spec.build()
    cp = critical_pressures(nz, g)
    if rng.random() < 0.5:
        m_throat = float(rng.uniform(0.3, 0.9))
        a_star = nz.A_throat / float(area_ratio(m_throat, g))
        pb = float(p_over_p0(mach_from_area_ratio(nz.A_exit / a_star, g, supersonic=False), g))
    else:
        pb = float(rng.uniform(0.2, 0.9)) * cp.p_crit2
    case = NozzleCase(f"NF2-{i:03d}", pb, N_NOZZLE, gamma=g, nozzle=spec)
    validate_case(case)
    return case


def nf3(seed: str, i: int, n_points: int = 11, cells_crossed: float = 30.0) -> NozzleSweepCase:
    """Back-pressure sweeps that move the shock over about 30 cells around 30..70 % of the divergent length."""
    rng = _rng(seed, "NF3", i)
    spec = _geometry(rng)
    g = float(rng.choice(ALL_GAMMAS))
    nz = spec.build()
    dx = (nz.x_exit - nz.x_in) / N_NOZZLE
    centre = 1.0 + float(rng.uniform(0.3, 0.7)) * spec.length
    xs = np.linspace(centre - 0.5 * cells_crossed * dx, centre + 0.5 * cells_crossed * dx, n_points)
    pbs = tuple(float(back_pressure_for_shock(nz, x, g)) for x in xs)
    case = NozzleSweepCase(f"NF3-{i:03d}", pbs, N_NOZZLE, gamma=g, nozzle=spec)
    validate_case(case)
    return case


GENERATORS = {"RF1": rf1, "RF2": rf2, "NF1": nf1, "NF2": nf2, "NF3": nf3}


def promo_suite(seed: str, sizes: dict[str, int] | None = None) -> list[tuple[str, Case]]:
    """(family, case) pairs of the held-out suite."""
    sizes = FAMILY_SIZES if sizes is None else sizes
    return [(fam, GENERATORS[fam](seed, i)) for fam, k in sizes.items() for i in range(k)]
