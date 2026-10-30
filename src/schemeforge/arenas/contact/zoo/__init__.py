"""The Arena 2 zoo: published third-medium formulations as candidate-style files, one directory per slot.

Zoo files obey the candidate rules (sandbox and hard constraints), so the zoo is both the baseline and a test of the
judge.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from pathlib import Path

from schemeforge.core.loader import load_function

ZOO_DIR = Path(__file__).parent
SLOT_FUNCTIONS = {"medium": "psi_medium"}


def members(slot: str) -> dict[str, Path]:
    """Zoo members of a slot: name -> file."""
    d = ZOO_DIR / slot
    return {p.stem: p for p in sorted(d.glob("*.py"))} if d.is_dir() else {}


@cache
def load(slot: str, name: str) -> Callable:
    return load_function(members(slot)[name], SLOT_FUNCTIONS[slot])
