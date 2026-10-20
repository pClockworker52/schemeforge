"""Pareto ranking (non-dominated sorting) for objective vectors where lower is better in every component."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def dominates(a: Sequence[float], b: Sequence[float]) -> bool:
    """a dominates b: no worse in every component and strictly better in at least one (lower is better)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    return bool(np.all(a <= b) and np.any(a < b))


def pareto_ranks(vectors: Sequence[Sequence[float]]) -> list[int]:
    """Rank 0 = non-dominated set, rank 1 = non-dominated after removing rank 0, and so on.
    NaN components are treated as worst (+inf)."""
    V = np.nan_to_num(np.asarray(vectors, float), nan=np.inf)
    n = len(V)
    ranks = [-1] * n
    remaining = set(range(n))
    r = 0
    while remaining:
        front = {i for i in remaining if not any(dominates(V[j], V[i]) for j in remaining if j != i)}
        for i in front:
            ranks[i] = r
        remaining -= front
        r += 1
    return ranks
