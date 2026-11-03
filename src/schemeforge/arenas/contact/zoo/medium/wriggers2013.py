"""Transversely isotropic third medium of Wriggers, Schroeder and Schwarz (2013, Comput. Mech. 52:837-847), as
implemented in felupe's example ex20 (felupe v9 documentation; the paper itself was not available to us). Isotropic part
W_iso = a1 I1 + a2 I2 + a3 I3 - d ln(I3)/2 with d = 2 a1 + 4 a2 + 2 a3 (stress-free at rest); anisotropic part
W_aniso = c / (a4 + 1) (1 - J4)^(a4 + 1) acting along the smallest principal squared stretch, with c = a5 / lam^2 if
lam < tol, else 0. J4 = n.C.n for the eigenvector n of the smallest eigenvalue lam, so J4 = lam: the term depends on C
alone. ex20's values: a1 = a2 = a3 = 1, a4 = 23, tol = 0.5, medium mu = 1 and a5 = 1e-2, i.e. a5 relative to the
medium's mu; here the medium's mu is gamma * mu of the body. W_iso(I) = 3 a1 + 3 a2 + a3 is subtracted so psi(I) = 0."""
import jax.numpy as jnp

A1 = 1.0
A2 = 1.0
A3 = 1.0
A4 = 23.0
A5 = 1e-2
TOL = 0.5


def psi_medium(C, p):
    """C: (3, 3) right Cauchy-Green tensor (plane strain: C[2, 2] == 1). p: body moduli mu, lmbda [force/area] and the
    medium stiffness scale gamma [-]. Returns the strain energy per unit reference volume [force/area]."""
    i1 = jnp.trace(C)
    i2 = (i1**2 - jnp.trace(C @ C)) / 2.0
    i3 = jnp.linalg.det(C)
    d = 2.0 * A1 + 4.0 * A2 + 2.0 * A3
    w_iso = A1 * i1 + A2 * i2 + A3 * i3 - d * jnp.log(i3) / 2.0 - (3.0 * A1 + 3.0 * A2 + A3)
    # smallest in-plane principal squared stretch, with safe square root and branch (finite derivatives at rest)
    disc = ((C[0, 0] - C[1, 1]) / 2.0) ** 2 + C[0, 1] ** 2
    root = jnp.where(disc > 0.0, jnp.sqrt(jnp.where(disc > 0.0, disc, 1.0)), 0.0)
    lam = (C[0, 0] + C[1, 1]) / 2.0 - root
    active = lam < TOL
    lam_a = jnp.where(active, lam, TOL)
    w_aniso = jnp.where(active, A5 / lam_a**2 / (A4 + 1.0) * (1.0 - lam_a) ** (A4 + 1.0), 0.0)
    return p["gamma"] * p["mu"] * (w_iso + w_aniso)
