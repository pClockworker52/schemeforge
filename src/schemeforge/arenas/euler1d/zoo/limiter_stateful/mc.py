"""Monotonized central (van Leer 1977) as a stateful limiter (state passed through: stateless baseline)."""
import jax.numpy as jnp


def _phi(r):
    return jnp.maximum(0.0, jnp.minimum(jnp.minimum(2.0 * r, 0.5 * (1.0 + r)), 2.0))


def phi_s(r, s):
    return _phi(r), s
