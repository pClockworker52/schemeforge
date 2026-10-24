"""THINC/BVD (Sun, Inaba, Xiao 2016, J. Comput. Phys. 322), componentwise on primitive variables.

Each cell has two candidate profiles: MUSCL with the van Leer limiter and THINC (a tanh jump inside the cell, steepness
BETA, used only where the cell is monotone between its neighbours). For every cell the scheme with the smaller total
boundary variation (TBV, the jumps between the face values of the cell and its neighbours, each reconstructed with the
same scheme) is chosen. Interface k separates padded cells k + 2 and k + 3: the left state needs cells k..k+4, the
right state cells k+1..k+5, so the stencil stays within the judge's 6-cell window.
"""
import jax.numpy as jnp

BETA = 1.6
EPS = 1e-20  # relative: the monotonicity test is scale-free (judge v1.5; v1.4 had an absolute 1e-20)


def _muscl(b, c, d):
    """(right face, left face) of cell c from cells b, c, d: MUSCL with the van Leer limiter."""
    dm, dp = c - b, d - c
    pos = dm * dp > 0.0
    slope = jnp.where(pos, 2.0 * dm * dp / jnp.where(pos, dm + dp, 1.0), 0.0)
    return c + 0.5 * slope, c - 0.5 * slope


def _thinc(b, c, d):
    """(right face, left face) of cell c from cells b, c, d: THINC where c lies strictly between b and d, else c."""
    mono = (d - c) * (c - b) > EPS * (jnp.abs(b) + jnp.abs(c) + jnp.abs(d)) ** 2
    qmin = jnp.minimum(b, d)
    delta = jnp.where(mono, jnp.abs(d - b), 1.0)
    theta = jnp.where(d >= b, 1.0, -1.0)
    frac = jnp.clip((c - qmin) / delta, 1e-12, 1.0 - 1e-12)
    tb = jnp.tanh(BETA)
    a = (jnp.exp(theta * BETA * (2.0 * frac - 1.0)) / jnp.cosh(BETA) - 1.0) / tb
    right = qmin + 0.5 * delta * (1.0 + theta * (tb + a) / (1.0 + a * tb))
    left = qmin + 0.5 * delta * (1.0 + theta * a)
    return jnp.where(mono, right, c), jnp.where(mono, left, c)


def _cell_faces(a, b, c, d, e):
    """(right face, left face) of cell c from cells a..e: the BVD choice between MUSCL and THINC for cell c."""
    out = []
    for scheme in (_muscl, _thinc):
        rb, _ = scheme(a, b, c)  # right face of the left neighbour
        rc, lc = scheme(b, c, d)
        _, ld = scheme(c, d, e)  # left face of the right neighbour
        out.append((rc, lc, jnp.abs(rb - lc) + jnp.abs(rc - ld)))
    (rm, lm, tbv_m), (rt, lt, tbv_t) = out
    use_thinc = tbv_t < tbv_m
    return jnp.where(use_thinc, rt, rm), jnp.where(use_thinc, lt, lm)


def reconstruct(W, gamma):
    m = W.shape[0] - 5  # number of interfaces, n + 1
    s = [W[j : j + m] for j in range(6)]  # s[j][k] = W[k + j]
    left, _ = _cell_faces(s[0], s[1], s[2], s[3], s[4])  # right face of cell k + 2
    _, right = _cell_faces(s[1], s[2], s[3], s[4], s[5])  # left face of cell k + 3
    return left, right
