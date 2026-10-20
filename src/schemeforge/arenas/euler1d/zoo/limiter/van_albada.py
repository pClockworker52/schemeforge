"""Van Albada limiter (van Albada, van Leer, Roberts 1982): phi(r) = (r^2 + r) / (r^2 + 1) for r > 0, else 0.

Written as r (r + 1) / (r^2 + 1) with r clipped first, so that r^2 cannot overflow for |r| up to 1e10.
"""
import jax.numpy as jnp


def phi(r):
    rp = jnp.maximum(r, 0.0)
    return rp * (rp + 1.0) / (rp * rp + 1.0)
