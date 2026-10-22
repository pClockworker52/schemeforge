"""Stateless base limiter of c-fb8db52bca (round 2, candidates/H-0006/e-20261021-123207-3146/g018_006_crossover.py): its phi(r) before the ratchet starts. H-0011 extra point."""
import jax.numpy as jnp

KS = 10.0

A_LO = 0.1

A_HI = 0.85

W = 2.0

SLOPE = 0.8


def _smin(a, b):
    return -jnp.logaddexp(-KS * a, -KS * b) / KS


def _base(r):
    rp = jnp.maximum(r, 0.0)
    a = A_LO + 0.5 * (A_HI - A_LO) * (1.0 + jnp.tanh(W * (rp - 1.0)))
    cap = 1.0 + a * jnp.tanh(SLOPE * (rp - 1.0))
    return jnp.maximum(_smin(2.0 * rp, cap), 0.0) * (r > 0.0)


def phi(r):
    return _base(r)
