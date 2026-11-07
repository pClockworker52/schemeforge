"""Geometric (kinematic) view of a normal particle impact: a rigid sphere entering a rigid flat at constant speed.

Geometry only. No material response, no deformation, no v_cr prediction. Note: docs/research/coldspray-kinematics.md.

A sphere of radius R moves at speed V into the plane z = 0; its penetration depth is delta = V t (0 <= delta <= R).
- contact radius:            a = sqrt(2 R delta - delta^2)
- edge collision angle:      beta, the angle between the sphere surface and the plane at the contact edge,
                             sin(beta) = a / R, cos(beta) = (R - delta) / R
- contact-edge speed:        u = da/dt = V (R - delta) / a = V cot(beta)
- subsonic edge (Walsh 1953 / Hassani-Gangaraj 2018 jetting condition, simplified): u < c, i.e. beta > beta_c with
  tan(beta_c) = V / c, where c is the bulk sound speed sqrt(B / rho).

Units: SI (m, s, m/s). Angles in radians.
"""

from __future__ import annotations

import math

import numpy as np

from schemeforge.research.coldspray import bulk_modulus_pa, load_properties


def contact_radius(delta: np.ndarray | float, r: float) -> np.ndarray | float:
    """a = sqrt(2 R delta - delta^2), for 0 <= delta <= R."""
    return np.sqrt(np.maximum(2.0 * r * delta - delta * delta, 0.0))


def edge_angle(delta: np.ndarray | float, r: float) -> np.ndarray | float:
    """beta with cos(beta) = (R - delta) / R."""
    return np.arccos(np.clip((r - delta) / r, -1.0, 1.0))


def edge_speed(v: float, delta: np.ndarray | float, r: float) -> np.ndarray | float:
    """u = V (R - delta) / a = V cot(beta). Infinite at first touch (delta = 0)."""
    a = contact_radius(delta, r)
    with np.errstate(divide="ignore"):
        return np.where(a > 0, v * (r - delta) / np.where(a > 0, a, 1.0), np.inf)


def critical_state(v: float, c: float, r: float) -> dict[str, float]:
    """State at which the contact edge slows to the sound speed c (u = c).

    Returns beta_c (rad), a_c, delta_c (m), t_c (s), and the small-angle estimate t_c ~ R V / (2 c^2).
    """
    beta = math.atan(v / c)
    delta = r * (1.0 - math.cos(beta))
    return {"beta_c": beta, "a_c": r * math.sin(beta), "delta_c": delta, "t_c": delta / v,
            "t_c_small_angle": r * v / (2.0 * c * c)}


def bulk_sound_speed(material: str) -> tuple[float, str]:
    """c = sqrt(B / rho) with B = E / (3 (1 - 2 nu)) and rho by rule P1 (properties.csv). Returns (c, provenance)."""
    p = load_properties()[material]
    b, src = bulk_modulus_pa(p)
    rho, rsrc = p["rho_kg_m3"]
    return math.sqrt(b / rho), f"B {src}; rho {rsrc}"
