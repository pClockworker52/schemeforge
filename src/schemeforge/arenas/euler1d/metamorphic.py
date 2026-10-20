"""Metamorphic measurements on unsteady runs (PLAN §9.7, "measured but not required").

Each function takes `run(W0, dx, t_end, gamma) -> W` (transmissive boundaries) and a base problem, and returns
the largest relative deviation between the transformed run and the transformed base run (0 = exact invariance).
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

Run = Callable[[np.ndarray, float, float, float], np.ndarray]


def _scale(W: np.ndarray) -> np.ndarray:
    a = np.sqrt(1.4 * W[:, 2] / W[:, 0])
    return np.array([np.max(np.abs(W[:, 0])), np.max(np.abs(W[:, 1]) + a), np.max(np.abs(W[:, 2]))])


def mirror_error(run: Run, W0: np.ndarray, dx: float, t_end: float, gamma: float, W: np.ndarray | None = None) -> float:
    """Run on the mirrored domain (x -> -x, u -> -u) and compare with the mirrored base run."""
    W = run(W0, dx, t_end, gamma) if W is None else W
    flip = np.array([1.0, -1.0, 1.0])
    Wm = run(W0[::-1] * flip, dx, t_end, gamma)[::-1] * flip
    return float(np.max(np.abs(Wm - W) / _scale(W)))


def scaling_error(run: Run, W0: np.ndarray, dx: float, t_end: float, gamma: float, alpha: float = 10.0,
                  W: np.ndarray | None = None) -> float:
    """(rho, p, E) -> alpha (rho, p, E) with u unchanged is a symmetry of the Euler equations."""
    W = run(W0, dx, t_end, gamma) if W is None else W
    s = np.array([alpha, 1.0, alpha])
    Ws = run(W0 * s, dx, t_end, gamma) / s
    return float(np.max(np.abs(Ws - W) / _scale(W)))


def galilean_error(run: Run, W0: np.ndarray, dx: float, t_end: float, gamma: float, shift_cells: int = 10,
                   W: np.ndarray | None = None) -> float:
    """Add U0 = shift_cells dx / t_end to u and compare, shifted by shift_cells, away from the boundaries.
    Numerical dissipation usually depends on |u|, so this is rarely exactly zero."""
    W = run(W0, dx, t_end, gamma) if W is None else W
    U0 = shift_cells * dx / t_end
    Wg = run(W0 + np.array([0.0, U0, 0.0]), dx, t_end, gamma) - np.array([0.0, U0, 0.0])
    k = shift_cells
    margin = 3 * k
    diff = Wg[k + margin : -margin] - W[margin : -margin - k]
    return float(np.max(np.abs(diff) / _scale(W)))
