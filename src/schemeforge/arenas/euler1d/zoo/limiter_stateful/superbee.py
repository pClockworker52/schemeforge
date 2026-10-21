"""Superbee (Roe 1985) as a stateful limiter (state passed through: stateless baseline)."""
import jax.numpy as jnp


def _phi(r):
    return jnp.maximum(0.0, jnp.maximum(jnp.minimum(2.0 * r, 1.0), jnp.minimum(r, 2.0)))


def phi_s(r, s):
    return _phi(r), s
