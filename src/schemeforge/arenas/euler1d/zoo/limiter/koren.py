"""Koren limiter (1993): phi(r) = max(0, min(2r, (1 + 2r)/3, 2)). Third-order upwind-biased, not symmetric."""
import jax.numpy as jnp


def phi(r):
    return jnp.maximum(0.0, jnp.minimum(jnp.minimum(2.0 * r, (1.0 + 2.0 * r) / 3.0), 2.0))
