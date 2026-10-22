"""MUSCL with the van Leer limiter on primitive variables, as a stateful reconstruction that passes its state through
unchanged: the stateless baseline of the slot."""
import jax.numpy as jnp

R_CLIP = 1e10


def reconstruct_s(W, gamma, s):
    dm = W[1:-1] - W[:-2]  # cells 1 .. n+4
    dp = W[2:] - W[1:-1]
    safe = jnp.where(dp == 0.0, 1.0, dp)
    r = jnp.clip(jnp.where(dp == 0.0, 0.0, dm / safe), -R_CLIP, R_CLIP)
    sigma = (r + jnp.abs(r)) / (1.0 + jnp.abs(r)) * dp
    Wc = W[1:-1]
    return (Wc + 0.5 * sigma)[1:-2], (Wc - 0.5 * sigma)[2:-1], s
