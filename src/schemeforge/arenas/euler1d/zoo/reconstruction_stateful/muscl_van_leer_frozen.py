"""Limiter freezing (Venkatakrishnan 1995, J. Comput. Phys. 118) for MUSCL with the van Leer limiter, as a stateful
reconstruction: the same method as the `limiter_stateful` zoo member `van_leer_frozen`. One state value per cell
1 .. n+4 and variable (the cells with a slope ratio): s < K counts steps; at step K the centred factor
psi = 2 phi(r) / (1 + r) is stored as K + 1 + psi, and from then on the slope is psi times the centred difference."""
import jax.numpy as jnp

K = 1000.0
R_CLIP = 1e10


def reconstruct_s(W, gamma, s):
    dm = W[1:-1] - W[:-2]  # cells 1 .. n+4
    dp = W[2:] - W[1:-1]
    safe = jnp.where(dp == 0.0, 1.0, dp)
    r = jnp.clip(jnp.where(dp == 0.0, 0.0, dm / safe), -R_CLIP, R_CLIP)
    live = (r + jnp.abs(r)) / (1.0 + jnp.abs(r))
    psi_live = 2.0 * live / jnp.maximum(1.0 + r, 1e-12)
    frozen = s > K
    psi = s - K - 1.0
    phi = jnp.where(frozen, jnp.where(r > -1.0, 0.5 * psi * (1.0 + r), 0.0), live)
    s_new = jnp.where(frozen, s, jnp.where(s + 1.0 >= K, K + 1.0 + jnp.where(r > 0.0, psi_live, 0.0), s + 1.0))
    sigma = phi * dp
    Wc = W[1:-1]
    return (Wc + 0.5 * sigma)[1:-2], (Wc - 0.5 * sigma)[2:-1], s_new
