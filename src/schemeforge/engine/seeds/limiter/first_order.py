"""Calibration seed: phi = 0 (first-order upwind)."""
import jax.numpy as jnp


def phi(r):
    return jnp.zeros_like(r)
