"""Venkatakrishnan-type limiter in 1D slope-ratio form, epsilon = 0 (Venkatakrishnan 1995).

Unlimited slope s = (d- + d+)/2, limited slope psi s with psi = min over both faces of f(y),
f(y) = (y^2 + 2y)/(y^2 + y + 2), y = (room to the neighbour extremum)/(unlimited face increment).
In 1D with r = d-/d+ > 0 this gives y = 4/(1 + r) and 4r/(1 + r), and phi(r) = psi (1 + r)/2; phi = 0 for r <= 0.
The K > 0 variants add eps^2 = (K dx)^3 and need the absolute differences, so they do not fit the phi(r) slot.
"""
import jax.numpy as jnp


def _f(y):
    return (y * y + 2.0 * y) / (y * y + y + 2.0)


def phi(r):
    rp = jnp.maximum(r, 0.0)
    psi = jnp.minimum(_f(4.0 / (1.0 + rp)), _f(4.0 * rp / (1.0 + rp)))
    return jnp.where(r > 0.0, psi * 0.5 * (1.0 + rp), 0.0)
