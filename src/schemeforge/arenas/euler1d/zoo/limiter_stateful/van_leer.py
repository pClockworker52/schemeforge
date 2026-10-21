"""Van Leer (1974) as a stateful limiter (state passed through: stateless baseline)."""
import jax.numpy as jnp


def _phi(r):
    return (r + jnp.abs(r)) / (1.0 + jnp.abs(r))


def phi_s(r, s):
    return _phi(r), s
