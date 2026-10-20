"""WENO5-Z reconstruction (Borges, Carmona, Costa, Don 2008), componentwise on primitive variables.

Interface k (k = 0..n) separates padded cells k + 2 and k + 3. The left state uses the stencil k..k+4 centred on
cell k + 2; the right state uses the mirrored stencil k+5..k+1 centred on cell k + 3.
"""
import jax.numpy as jnp

EPS = 1e-40
D0, D1, D2 = 0.1, 0.6, 0.3


def _weno5z(a, b, c, d, e):
    """Value at the right face of cell c from cell averages a, b, c, d, e (left to right)."""
    q0 = (2.0 * a - 7.0 * b + 11.0 * c) / 6.0
    q1 = (-b + 5.0 * c + 2.0 * d) / 6.0
    q2 = (2.0 * c + 5.0 * d - e) / 6.0
    b0 = 13.0 / 12.0 * (a - 2.0 * b + c) ** 2 + 0.25 * (a - 4.0 * b + 3.0 * c) ** 2
    b1 = 13.0 / 12.0 * (b - 2.0 * c + d) ** 2 + 0.25 * (b - d) ** 2
    b2 = 13.0 / 12.0 * (c - 2.0 * d + e) ** 2 + 0.25 * (3.0 * c - 4.0 * d + e) ** 2
    tau = jnp.abs(b0 - b2)
    w0 = D0 * (1.0 + tau / (b0 + EPS))
    w1 = D1 * (1.0 + tau / (b1 + EPS))
    w2 = D2 * (1.0 + tau / (b2 + EPS))
    return (w0 * q0 + w1 * q1 + w2 * q2) / (w0 + w1 + w2)


def reconstruct(W, gamma):
    m = W.shape[0] - 5  # number of interfaces, n + 1
    s = [W[j : j + m] for j in range(6)]  # s[j][k] = W[k + j]
    left = _weno5z(s[0], s[1], s[2], s[3], s[4])
    right = _weno5z(s[5], s[4], s[3], s[2], s[1])
    return left, right
