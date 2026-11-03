"""Arena 2 held-out families (PLAN §14.2, plan step 4), generated deterministically from the secret seed.

The seed lives outside the repo at ~/.schemeforge/heldout_seed, as for Arena 1 (Claude Code is denied access; the
promo suite is run on Peter's machine). Every generator takes the seed explicitly; tests use their own. Instance
parameters never leave the judge: reports carry family aggregates only (core/evaluation.py stores the instances
outside the repo). The salt "contact" keeps these instances independent of Arena 1's from the same seed.

Families:
    GF  gap closure (C0a/C1 kind): random gap, column height and width, E, nu, medium stiffness, push, distortion
    SF  simple shear (C0b): random shear, E, nu, medium stiffness
    HF  Hertz (C2): random R, E, nu, initial gap, indentation, medium stiffness, mesh offsets
    HX  one Hertz instance for the promo-only metrics mesh_sens and max_step (evaluate.py)
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from .cases import Case, GapClosureCase, HertzCase, SimpleShearCase, validate_case

SEED_FILE = Path.home() / ".schemeforge" / "heldout_seed"
FAMILY_SIZES = {"GF": 10, "SF": 10, "HF": 6, "HX": 1}


def read_seed(path: Path | None = None) -> str:
    seed = (path or SEED_FILE).read_text(encoding="utf-8").strip()
    if len(seed) < 16:
        raise ValueError("held-out seed is missing or too short")
    return seed


def seed_fingerprint(seed: str) -> str:
    """Identifies the seed in reports without revealing it (same fingerprint as Arena 1 for the same seed)."""
    return hashlib.sha256(f"schemeforge-seed:{seed}".encode()).hexdigest()[:16]


def _rng(seed: str, family: str, index: int) -> np.random.Generator:
    digest = hashlib.sha256(f"{seed}:contact:{family}:{index}".encode()).digest()
    return np.random.Generator(np.random.PCG64(int.from_bytes(digest, "big")))


def _log_uniform(rng: np.random.Generator, lo: float, hi: float) -> float:
    return float(10.0 ** rng.uniform(np.log10(lo), np.log10(hi)))


def gap_family(seed: str, i: int) -> GapClosureCase:
    rng = _rng(seed, "GF", i)
    gap = float(rng.uniform(0.03, 0.2))
    height = float(rng.uniform(0.6, 1.5))
    return GapClosureCase(
        f"GF-{i:03d}", gap=gap, height=height, width=float(rng.uniform(0.1, 0.4)),
        push=gap + float(rng.uniform(0.02, 0.08)) * height, steps=8, nx=3, ny_body=3, ny_medium=int(rng.integers(2, 5)),
        E=_log_uniform(rng, 0.1, 10.0), nu=float(rng.uniform(0.15, 0.45)), gamma=_log_uniform(rng, 1e-6, 1e-3),
        distort=float(rng.uniform(0.0, 0.35)), seed=int(rng.integers(0, 2**31)))


def shear_family(seed: str, i: int) -> SimpleShearCase:
    rng = _rng(seed, "SF", i)
    return SimpleShearCase(f"SF-{i:03d}", shear=float(rng.uniform(0.1, 3.0)), E=_log_uniform(rng, 0.1, 10.0),
                           nu=float(rng.uniform(0.15, 0.45)), gamma=_log_uniform(rng, 1e-6, 1e-3))


def hertz_family(seed: str, i: int, family: str = "HF") -> HertzCase:
    """Contact half-width a/R about 0.03-0.06 (Hertz validity a/R <= 0.1) with W = H = R."""
    rng = _rng(seed, family, i)
    R = _log_uniform(rng, 0.5, 2.0)
    gap = float(rng.uniform(0.0015, 0.003)) * R
    return HertzCase(f"{family}-{i:03d}", R=R, W=R, H=R, gap=gap, push=gap + float(rng.uniform(0.003, 0.005)) * R,
                     steps=12, nx=int(rng.integers(28, 37)), ny=16, ny_medium=4, E=_log_uniform(rng, 0.1, 10.0),
                     nu=float(rng.uniform(0.15, 0.45)), gamma=_log_uniform(rng, 1e-6, 1e-5))


GENERATORS = {"GF": gap_family, "SF": shear_family, "HF": hertz_family,
              "HX": lambda seed, i: hertz_family(seed, i, "HX")}


def promo_suite(seed: str, sizes: dict[str, int] | None = None) -> list[tuple[str, Case]]:
    """(family, case) pairs of the held-out suite; every case passes validate_case."""
    sizes = FAMILY_SIZES if sizes is None else sizes
    suite = [(fam, GENERATORS[fam](seed, i)) for fam, k in sizes.items() for i in range(k)]
    for _, case in suite:
        validate_case(case)
    return suite
