"""Isochoric-volumetric neo-Hookean medium scaled by gamma, the form of felupe's NeoHooke(mu, bulk): psi = gamma
(mu/2 (J^(-2/3) tr C - 3) + K/2 (J - 1)^2) with K = lmbda + 2 mu / 3. A FElupe variant, not a published third-medium
formulation: its volumetric term stays finite as J -> 0, unlike the ln J of neo_hooke (Bluhm et al. 2021)."""
import jax.numpy as jnp


def psi_medium(C, p):
    """C: (3, 3) right Cauchy-Green tensor (plane strain: C[2, 2] == 1). p: body moduli mu, lmbda [force/area] and the
    medium stiffness scale gamma [-]. Returns the strain energy per unit reference volume [force/area]."""
    j = jnp.sqrt(jnp.linalg.det(C))
    bulk = p["lmbda"] + 2.0 * p["mu"] / 3.0
    return p["gamma"] * (p["mu"] / 2.0 * (j ** (-2.0 / 3.0) * jnp.trace(C) - 3.0) + bulk / 2.0 * (j - 1.0) ** 2)
