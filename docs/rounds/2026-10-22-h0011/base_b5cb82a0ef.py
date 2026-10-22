"""Stateless base limiter of c-b5cb82a0ef (round 2, candidates/H-0009/e-20261021-123207-3146/g019_009_explore.py): its phi(r) before the ratchet starts. H-0011 extra point."""
import jax.numpy as jnp

KS = 12.0
W = 0.6


def _smin(a, b):
    return -jnp.logaddexp(-KS * a, -KS * b) / KS


def _smax(a, b):
    return jnp.logaddexp(KS * a, KS * b) / KS


def _superbee(r):
    return _smax(_smin(2.0 * r, 1.0), _smin(r, 2.0))


def _base(r):
    rp = jnp.maximum(r, 0.0)
    tc = jnp.maximum(_smin(2.0 * rp, 1.0 + 0.5 * jnp.tanh(rp - 1.0)), 0.0)
    relaxed = tc + W * (_superbee(rp) - tc)
    phi = jnp.clip(relaxed, 0.0, jnp.minimum(2.0 * rp, 2.0))
    return phi * (r > 0.0)


def phi(r):
    return _base(r)
