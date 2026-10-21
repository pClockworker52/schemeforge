"""Van Albada (1982) as a stateful limiter (state passed through: stateless baseline)."""
import jax.numpy as jnp


def _phi(r):
    rp = jnp.maximum(r, 0.0)
    return rp * (rp + 1.0) / (rp * rp + 1.0)


def phi_s(r, s):
    return _phi(r), s
