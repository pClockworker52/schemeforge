"""Minmod limiter (Roe 1986): phi(r) = max(0, min(1, r))."""
import jax.numpy as jnp


def phi(r):
    return jnp.maximum(0.0, jnp.minimum(1.0, r))
