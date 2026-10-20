"""Van Leer limiter (1974): phi(r) = (r + |r|) / (1 + |r|)."""
import jax.numpy as jnp


def phi(r):
    return (r + jnp.abs(r)) / (1.0 + jnp.abs(r))
