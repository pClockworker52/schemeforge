"""Verification ladder of the JAX impact solver (src/schemeforge/research/impact_axisym.py)."""

import numpy as np
import pytest

from schemeforge.research import impact_axisym as ia

E, NU, RHO = 70e9, 0.35, 2700.0


def _rung0(n_z):
    res, ex = ia.confined_plate_on_rigid_wall(10e-6, 100.0, E, NU, RHO, n_z=n_z)
    contact = res.t[res.force > 1e-9 * ex["force"]].max()
    mid = (res.t > 0.2 * ex["t_contact"]) & (res.t < 0.8 * ex["t_contact"])
    return np.mean(res.force[mid]) / ex["force"], contact / ex["t_contact"], res.v_cm[-1] / 100.0


def test_rung0_confined_plate_matches_exact_1d_solution():
    plateau, t_ratio, rebound = _rung0(50)
    assert plateau == pytest.approx(1.0, abs=1e-3)  # rho c_d V
    assert t_ratio == pytest.approx(1.0, abs=0.02)  # 2 L / c_d
    assert rebound == pytest.approx(1.0, abs=0.03)  # elastic rebound at V


def test_rung0_converges_with_refinement():
    _, t25, r25 = _rung0(25)
    _, t100, r100 = _rung0(100)
    assert abs(t100 - 1) < abs(t25 - 1)
    assert abs(r100 - 1) < abs(r25 - 1)


def test_hertz_reference_energy_balance():
    ref = ia.hertz_reference(10e-6, 20.0, E, NU, RHO)
    e_star = E / (1 - NU**2)
    m = RHO * 4 / 3 * np.pi * (10e-6) ** 3
    stored = 4 / 3 * e_star * np.sqrt(10e-6) * 0.4 * ref["d_max"] ** 2.5
    assert stored == pytest.approx(0.5 * m * 20.0**2, rel=1e-12)


def test_time_step_length_handles_distorted_corner_elements():
    mesh = ia.sphere_mesh(10e-6, 15, 30)
    xe = mesh.X[mesh.conn]
    edges = np.linalg.norm(xe[:, 1] - xe[:, 0], axis=1)
    assert ia.characteristic_length(mesh) < edges.min()
