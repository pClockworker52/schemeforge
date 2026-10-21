"""Limiter freezing (Venkatakrishnan 1995, J. Comput. Phys. 118) applied to Van Leer: after K steps the limiter
factor is fixed. It is frozen in centred form, psi = 2 phi(r) / (1 + r), so the slope stays psi times the centred
difference; freezing phi itself would fix a multiple of the downwind difference, which is linearly unstable.
One state value per slope ratio: s < K counts steps; at step K the state becomes K + 1 + psi (psi in [0, 1.34]),
and from then on phi = psi (1 + r) / 2 for r > -1 (0 otherwise). Unsteady dev cases and Newton take fewer than K
steps, so there it is the plain limiter."""
import jax.numpy as jnp

K = 1000.0


def _phi(r):
    return (r + jnp.abs(r)) / (1.0 + jnp.abs(r))


def phi_s(r, s):
    live = _phi(r)
    psi_live = 2.0 * live / jnp.maximum(1.0 + r, 1e-12)
    frozen = s > K
    psi = s - K - 1.0
    phi = jnp.where(frozen, jnp.where(r > -1.0, 0.5 * psi * (1.0 + r), 0.0), live)
    s_new = jnp.where(frozen, s, jnp.where(s + 1.0 >= K, K + 1.0 + jnp.where(r > 0.0, psi_live, 0.0), s + 1.0))
    return phi, s_new
