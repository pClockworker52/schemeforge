"""Closed-form checks of the rigid-sphere impact kinematics (src/schemeforge/research/impact_kinematics.py)."""

import math

import numpy as np
import pytest

from schemeforge.research import impact_kinematics as k

R = 7.5e-6


def test_contact_radius_limits():
    assert k.contact_radius(0.0, R) == 0.0
    assert k.contact_radius(R, R) == pytest.approx(R)
    # a^2 + (R - delta)^2 = R^2 at any depth
    d = np.linspace(0, R, 7)
    assert np.allclose(k.contact_radius(d, R) ** 2 + (R - d) ** 2, R * R)


def test_edge_speed_is_derivative_and_cot_beta():
    v = 900.0
    d = np.linspace(0.01 * R, 0.5 * R, 50)
    h = 1e-14
    fd = (k.contact_radius(d + v * h, R) - k.contact_radius(d - v * h, R)) / (2 * h)  # da/dt with delta = V t
    assert np.allclose(k.edge_speed(v, d, R), fd, rtol=1e-5)
    assert np.allclose(k.edge_speed(v, d, R), v / np.tan(k.edge_angle(d, R)), rtol=1e-12)
    assert np.isinf(k.edge_speed(v, np.array([0.0]), R)[0])


def test_critical_state_edge_speed_equals_c():
    c = 5000.0
    for v in (500.0, 900.0, 1100.0):
        s = k.critical_state(v, c, R)
        assert k.edge_speed(v, s["delta_c"], R) == pytest.approx(c, rel=1e-10)
        assert math.tan(s["beta_c"]) == pytest.approx(v / c)
        assert s["a_c"] == pytest.approx(k.contact_radius(s["delta_c"], R))
    # small-angle limit: t_c -> R V / (2 c^2) as V / c -> 0
    s = k.critical_state(50.0, c, R)
    assert s["t_c"] / s["t_c_small_angle"] == pytest.approx(1.0, rel=1e-3)


def test_bulk_sound_speed_from_table_s1():
    c_al, src = k.bulk_sound_speed("Al")
    assert c_al == pytest.approx(math.sqrt(70e9 / (3 * (1 - 2 * 0.35)) / 2700))
    assert "P-H20-Al" in src
