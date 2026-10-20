"""The Arena 1 zoo: known methods as candidate-style files, one directory per slot (PLAN §9.8).

Zoo files obey the same rules as candidates (they must pass the sandbox and the hard constraints), so the zoo is
both the baseline and a test of the judge.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from pathlib import Path

from schemeforge.core.loader import load_function

ZOO_DIR = Path(__file__).parent
SLOT_FUNCTIONS = {
    "limiter": "phi",
    "limiter_stateful": "phi_s",
    "flux": "flux",
    "reconstruction": "reconstruct",
    "operator": "fluxes_and_source",
}


def members(slot: str) -> dict[str, Path]:
    """Zoo members of a slot: name -> file."""
    d = ZOO_DIR / slot
    return {p.stem: p for p in sorted(d.glob("*.py"))} if d.is_dir() else {}


@cache
def load(slot: str, name: str) -> Callable:
    return load_function(members(slot)[name], SLOT_FUNCTIONS[slot])
