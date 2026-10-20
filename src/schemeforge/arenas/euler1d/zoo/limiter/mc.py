"""Monotonized central limiter (van Leer 1977): phi(r) = max(0, min(2r, (1 + r)/2, 2))."""
import jax.numpy as jnp


def phi(r):
    return jnp.maximum(0.0, jnp.minimum(jnp.minimum(2.0 * r, 0.5 * (1.0 + r)), 2.0))
