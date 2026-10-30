"""Arena 2 metric helpers: contact pressure from nodal reactions on a straight edge."""

from __future__ import annotations

import numpy as np


def edge_traction(x: np.ndarray, f: np.ndarray) -> np.ndarray:
    """Nodal traction t (n,) on a straight edge of quadratic elements from the consistent nodal forces f (n,), with x
    (n,) sorted, nodes ordered corner, mid, corner, mid, ... (n odd). Solves M t = f with the consistent mass matrix of
    the 3-node line elements, so a traction that is quadratic per element (uniform in particular) comes back exactly;
    dividing by a tributary length does not (quadratic elements carry 1/6, 2/3, 1/6 of a uniform load)."""
    x, f = np.asarray(x, float), np.asarray(f, float)
    n = x.size
    if n < 3 or n % 2 == 0:
        raise ValueError("a quadratic edge needs an odd number (>= 3) of nodes")
    M = np.zeros((n, n))
    local = np.array([[4.0, 2.0, -1.0], [2.0, 16.0, 2.0], [-1.0, 2.0, 4.0]]) / 30.0  # times element length
    for e in range(0, n - 2, 2):
        idx = np.array([e, e + 1, e + 2])
        M[np.ix_(idx, idx)] += local * (x[e + 2] - x[e])
    return np.linalg.solve(M, f)
