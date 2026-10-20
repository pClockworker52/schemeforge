"""Superbee limiter (Roe 1985): phi(r) = max(0, min(2r, 1), min(r, 2))."""
import jax.numpy as jnp


def phi(r):
    return jnp.maximum(0.0, jnp.maximum(jnp.minimum(2.0 * r, 1.0), jnp.minimum(r, 2.0)))
