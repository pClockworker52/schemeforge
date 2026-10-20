"""Calibration seed: phi = 1 (unlimited, Lax-Wendroff-like slopes)."""
import jax.numpy as jnp


def phi(r):
    return jnp.ones_like(r)
