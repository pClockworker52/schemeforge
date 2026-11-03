"""Neo-Hookean third medium as written in Faltus, Amato and Horak (2026, arXiv 2603.13063), Eq. (1)-(2):
W = kappa/2 ln^2 J + kappa/2 (J^(-2/3) I1 - 3)^2 with kappa_vol = kappa_iso = gamma kappa_char; the isochoric term is
squared as printed. kappa_char, the characteristic bulk modulus of the body, is taken as K = lmbda + 2 mu / 3. (The
paper's further linear-elastic pre-contact term needs F, not C, so it does not fit this slot.)"""
import jax.numpy as jnp


def psi_medium(C, p):
    """C: (3, 3) right Cauchy-Green tensor (plane strain: C[2, 2] == 1). p: body moduli mu, lmbda [force/area] and the
    medium stiffness scale gamma [-]. Returns the strain energy per unit reference volume [force/area]."""
    j = jnp.sqrt(jnp.linalg.det(C))
    kappa = p["gamma"] * (p["lmbda"] + 2.0 * p["mu"] / 3.0)
    return kappa / 2.0 * jnp.log(j) ** 2 + kappa / 2.0 * (j ** (-2.0 / 3.0) * jnp.trace(C) - 3.0) ** 2
