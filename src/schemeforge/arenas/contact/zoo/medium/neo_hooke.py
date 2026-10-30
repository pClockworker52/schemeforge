"""Compressible neo-Hookean medium scaled by gamma: the isotropic part of Bluhm, Sigmund and Poulios (2021), without
their Hessian regularization (which needs its own slot). psi = gamma (mu/2 (tr C - 3) - mu ln J + lmbda/2 ln^2 J)."""
import jax.numpy as jnp


def psi_medium(C, p):
    """C: (3, 3) right Cauchy-Green tensor (plane strain: C[2, 2] == 1). p: body moduli mu, lmbda [force/area] and the
    medium stiffness scale gamma [-]. Returns the strain energy per unit reference volume [force/area]."""
    ln_j = jnp.log(jnp.linalg.det(C)) / 2.0
    return p["gamma"] * (p["mu"] / 2.0 * (jnp.trace(C) - 3.0) - p["mu"] * ln_j + p["lmbda"] / 2.0 * ln_j**2)
