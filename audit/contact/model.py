"""Blind audit of the Arena 2 (contact) judge: exact solutions from docs/judge/contact_spec.md only.

Plane strain, forces per unit thickness, first Piola-Kirchhoff stresses, compressive forces positive.
Written without reading src/schemeforge/arenas/. numpy/scipy float64, mpmath for the reference roots.
"""

from __future__ import annotations

import math

import mpmath as mp
import numpy as np
from scipy.optimize import brentq

mp.mp.dps = 50


# ----------------------------------------------------------------------------------------------------------------
# Materials
# ----------------------------------------------------------------------------------------------------------------
def lame(E: float, nu: float) -> tuple[float, float]:
    """Textbook Lame moduli (3D, used unchanged in plane strain): mu = E/(2(1+nu)), lambda = E nu/((1+nu)(1-2nu))."""
    return E / (2.0 * (1.0 + nu)), E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))


def psi_body(C: np.ndarray, mu: float, lmbda: float) -> float:
    """Compressible neo-Hookean psi_b = mu/2 (tr C - 3) - mu ln J + lambda/2 ln^2 J, C (3, 3), J = sqrt(det C)."""
    lnJ = 0.5 * math.log(np.linalg.det(C))
    return 0.5 * mu * (np.trace(C) - 3.0) - mu * lnJ + 0.5 * lmbda * lnJ**2


def dpsi_dC_body(C: np.ndarray, mu: float, lmbda: float) -> np.ndarray:
    """d psi_b / dC = mu/2 I + (lambda ln J - mu)/2 C^-1 (textbook), shape (3, 3)."""
    Ci = np.linalg.inv(C)
    lnJ = 0.5 * math.log(np.linalg.det(C))
    return 0.5 * mu * np.eye(3) + 0.5 * (lmbda * lnJ - mu) * Ci


def P_from_psi(F: np.ndarray, mu: float, lmbda: float, scale: float = 1.0) -> np.ndarray:
    """P = 2 F dpsi/dC at C = F^T F, for psi = scale * psi_b. F, P (3, 3)."""
    C = F.T @ F
    return 2.0 * scale * F @ dpsi_dC_body(C, mu, lmbda)


def P_stretch(s, mu, lmbda, scale=1.0):
    """Confined-stretch stress P_yy for F = diag(1, s, 1): d/ds psi(diag(1, s^2, 1)) = mu (s - 1/s) + lambda ln(s)/s.

    Works for floats, numpy arrays and mpmath numbers (log dispatches on type).
    """
    log = mp.log if isinstance(s, mp.mpf) else np.log
    return scale * (mu * (s - 1 / s) + lmbda * log(s) / s)


# ----------------------------------------------------------------------------------------------------------------
# C0a / C1: confined gap closure
# ----------------------------------------------------------------------------------------------------------------
def ideal_force(d: float, g: float, h: float, w: float, mu: float, lmbda: float) -> float:
    """Ideal contact force (compressive positive): 0 for d <= g, -w P_b((h - (d - g))/h) for d > g."""
    if d <= g:
        return 0.0
    return float(-w * P_stretch(mp.mpf(h - (d - g)) / h, mp.mpf(mu), mp.mpf(lmbda)))


def exact_homogeneous(d: float, g: float, h: float, w: float, mu: float, lmbda: float, gamma: float):
    """Exact two-layer homogeneous solution with the audit medium psi_m = gamma psi_b.

    Solves P_b(s_b) = gamma P_b(s_m), h s_b + g s_m = h + g - d for s_m (via t = ln s_m: the residual is strictly
    decreasing in t). Float64 bracketing, then an mpmath (50 digits) Newton polish.
    Returns (force = -w P_m(s_m), medium thickness g s_m, s_m, s_b).
    """
    L = h + g - d

    def r64(t):
        sm = math.exp(t)
        sb = (L - g * sm) / h
        return P_stretch(sb, mu, lmbda) - P_stretch(sm, mu, lmbda, gamma)

    t_hi = math.log(L / g) + math.log1p(-1e-15)  # s_b -> 0+, residual -> -inf
    t_lo = -600.0
    while r64(t_hi) > 0:  # numerical guard
        t_hi = 0.5 * (t_hi + math.log(L / g))
    t0 = brentq(r64, t_lo, t_hi, xtol=1e-15, rtol=8.9e-16, maxiter=500)

    M = mp.mpf
    mu_, la_, ga_, g_, h_, L_ = M(mu), M(lmbda), M(gamma), M(g), M(h), M(L)

    def rmp(t):
        sm = mp.exp(t)
        sb = (L_ - g_ * sm) / h_
        return P_stretch(sb, mu_, la_) - P_stretch(sm, mu_, la_, ga_)

    t = mp.findroot(rmp, M(t0), solver="newton", tol=mp.mpf(10) ** -45, maxsteps=100)
    sm = mp.exp(t)
    sb = (L_ - g_ * sm) / h_
    force = -M(w) * P_stretch(sm, mu_, la_, ga_)
    return float(force), float(g_ * sm), float(sm), float(sb)


def gap_closure_exact(case: dict) -> dict:
    """All exact C0a/C1 quantities of spec §Audit for one case (defaults from contact_cases.md)."""
    g, h, w = case["gap"], case["height"], case["width"]
    push = case["push"]
    mu, lmbda = lame(case["E"], case["nu"])
    gam = case["gamma"]
    Fi = ideal_force(push, g, h, w, mu, lmbda)
    F, t, sm, sb = exact_homogeneous(push, g, h, w, mu, lmbda, gam)
    Fh, th, _, _ = exact_homogeneous(0.5 * g, g, h, w, mu, lmbda, gam)
    steps = case["steps"]
    pushes = [push * k / steps for k in range(steps + 1)]
    return dict(
        mu=mu, lmbda=lmbda,
        ideal_force=Fi, exact_force=F, exact_thickness=t,
        exact_force_half=Fh, exact_thickness_half=th,
        exact_leak_pre=Fh / Fi, exact_gap_res=t / g, exact_force_err=F / Fi - 1.0,
        exact_pressure=F / w,
        steps_push=pushes,
    )


# ----------------------------------------------------------------------------------------------------------------
# C0b: simple shear
# ----------------------------------------------------------------------------------------------------------------
def simple_shear(case: dict) -> dict:
    """P = 2 F dpsi/dC for the audit medium in F = [[1, s, 0], [0, 1, 0], [0, 0, 1]].

    Numerically via the general formula, and in closed form: J = 1 so P = gamma mu (F - F^-T) = gamma mu s (e_x e_y
    + e_y e_x): P_xy = gamma mu s, P_yy = 0, shear_parasitic = gamma, normal_parasitic = 0.
    """
    s = case["shear"]
    mu, lmbda = lame(case["E"], case["nu"])
    gam = case["gamma"]
    F = np.array([[1.0, s, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    P = P_from_psi(F, mu, lmbda, gam)
    return dict(
        mu=mu, lmbda=lmbda,
        P_xy=P[0, 1], P_yy=P[1, 1],
        shear_parasitic=P[0, 1] / (mu * s), normal_parasitic=P[1, 1] / (mu * s),
        P_xy_closed=gam * mu * s, P_yy_closed=0.0, shear_parasitic_closed=gam, normal_parasitic_closed=0.0,
    )


# ----------------------------------------------------------------------------------------------------------------
# C2: Hertz for a rigid flat, and pressure recovery on quadratic edges
# ----------------------------------------------------------------------------------------------------------------
def hertz(P: float, R: float, E: float, nu: float):
    """Textbook plane-strain Hertz, cylinder on rigid flat: 1/E* = (1 - nu^2)/E, a = sqrt(4PR/(pi E*)),
    p0 = 2P/(pi a). P is the load per unit thickness of the full model."""
    Es = E / (1.0 - nu**2)
    a = math.sqrt(4.0 * P * R / (math.pi * Es))
    p0 = 2.0 * P / (math.pi * a)
    return Es, a, p0


def hertz_p(x: np.ndarray, a: float, p0: float) -> np.ndarray:
    """p(x) = p0 sqrt(1 - x^2/a^2) for |x| < a, else 0."""
    r = 1.0 - (np.asarray(x) / a) ** 2
    return p0 * np.sqrt(np.clip(r, 0.0, None))


_GP, _GW = np.polynomial.legendre.leggauss(4)


def _N(xi):
    """Quadratic Lagrange shape functions on [-1, 1], node order (left, mid, right). xi (q,) -> (q, 3)."""
    return np.stack([0.5 * xi * (xi - 1.0), 1.0 - xi**2, 0.5 * xi * (xi + 1.0)], axis=-1)


def _dN(xi):
    return np.stack([xi - 0.5, -2.0 * xi, xi + 0.5], axis=-1)


def consistent_mass(x: np.ndarray) -> np.ndarray:
    """Consistent 1D 'mass' matrix M_ij = int N_i N_j dx of quadratic edges on the sorted nodes x (2n+1,).

    Elements are (x[2k], x[2k+1], x[2k+2]); isoparametric with 4-point Gauss (exact for any mid-node position up to
    degree 7; reduces to L/30 [[4, 2, -1], [2, 16, 2], [-1, 2, 4]] for a centred mid-node)."""
    n = len(x)
    assert n % 2 == 1
    M = np.zeros((n, n))
    N = _N(_GP)
    dN = _dN(_GP)
    for k in range(0, n - 1, 2):
        idx = [k, k + 1, k + 2]
        J = dN @ x[idx]
        Me = np.einsum("q,qi,qj->ij", _GW * J, N, N)
        M[np.ix_(idx, idx)] += Me
    return M


def recover_pressure(x: np.ndarray, f: np.ndarray) -> np.ndarray:
    """Nodal pressure p from consistent nodal forces f: M p = f."""
    return np.linalg.solve(consistent_mass(x), f)


def p_interp(x: np.ndarray, p: np.ndarray, xq: np.ndarray) -> np.ndarray:
    """Quadratic FE interpolant of nodal p at points xq (within [x0, x_end])."""
    out = np.empty_like(xq)
    ne = (len(x) - 1) // 2
    for j, xv in enumerate(xq):
        k = min(int(np.searchsorted(x[0::2], xv, side="right")) - 1, ne - 1)
        k = max(k, 0)
        x0, xm, x1 = x[2 * k], x[2 * k + 1], x[2 * k + 2]
        # affine mapping assumed for the inverse (mid-nodes centred, checked by the caller)
        xi = (2.0 * xv - x0 - x1) / (x1 - x0)
        out[j] = _N(np.array([xi]))[0] @ p[2 * k: 2 * k + 3]
    return out


def hertz_metrics(x: np.ndarray, f: np.ndarray, R: float, E: float, nu: float, load: float | None = None) -> dict:
    """Recompute load, p, Hertz values and the C2 metrics from the half-model contact nodes x (n,) and forces f (n,).

    - load P = 2 sum f (full model; the half model carries half the load). `load` overrides P (to separate the
      effect of the judge's load from the metric definitions).
    - a_meas from the second moment: int p x^2 dx = P a^2/4 over the full model, so a_meas^2 = 4 (2 sum f x^2) / P
      (exact for consistent forces on affine quadratic edges since x^2 is in the element space).
    - p0_err = max(p)/p0 - 1 ("peak of the recovered pressure"); also the variant p(0)/p0 - 1.
    - p_l2 over |x| < 1.5 a_hertz. The spec does not say how the L2 norm is integrated. The judge's value is
      reproduced by the trapezoidal rule over the nodes (p_l2); the nodal-sum and quadratic-FE-interpolant
      variants are kept for the report.
    - leak_out = sum_{x > 1.2 a_hertz} |f| / (P/2); also the |sum f| variant.
    """
    x = np.asarray(x, float)
    f = np.asarray(f, float)
    p = recover_pressure(x, f)
    P2 = 2.0 * f.sum()
    P = P2 if load is None else float(load)
    Es, a, p0 = hertz(P, R, E, nu)
    a_meas = math.sqrt(4.0 * 2.0 * (f * x**2).sum() / P)
    pH = hertz_p(x, a, p0)
    sel = x < 1.5 * a
    e = p - pH
    pl2_nodal = math.sqrt((e[sel] ** 2).sum() / (pH[sel] ** 2).sum())
    pl2_trap = math.sqrt(np.trapezoid(e[sel] ** 2, x[sel]) / np.trapezoid(pH[sel] ** 2, x[sel]))
    # FE-interpolant integral (composite Gauss on [0, 1.5 a], breaking at nodes and at a)
    brk = np.unique(np.concatenate([[0.0, 1.5 * a, a], x[(x > 0) & (x < 1.5 * a)]]))
    num = den = 0.0
    gp, gw = np.polynomial.legendre.leggauss(20)
    for lo, hi in zip(brk[:-1], brk[1:]):
        xq = 0.5 * (hi - lo) * gp + 0.5 * (hi + lo)
        wq = 0.5 * (hi - lo) * gw
        ph = p_interp(x, p, xq)
        pe = hertz_p(xq, a, p0)
        num += (wq * (ph - pe) ** 2).sum()
        den += (wq * pe**2).sum()
    pl2_int = math.sqrt(num / den)
    out_sel = x > 1.2 * a
    mid_offset = np.abs(x[1::2] - 0.5 * (x[0:-1:2] + x[2::2])).max() / x[-1]
    return dict(
        p=p, load=P2, E_star=Es, a_hertz=a, p0_hertz=p0, a_meas=a_meas,
        a_err=a_meas / a - 1.0,
        p0_err=p.max() / p0 - 1.0, p0_err_at0=p[0] / p0 - 1.0, argmax_p=int(np.argmax(p)),
        p_l2=pl2_trap, p_l2_trap=pl2_trap, p_l2_nodal=pl2_nodal, p_l2_int=pl2_int,
        leak_out=np.abs(f[out_sel]).sum() / (0.5 * P),
        leak_out_abs_sum=abs(f[out_sel].sum()) / (0.5 * P),
        load_mass=float(2.0 * consistent_mass(x).sum(axis=0) @ p),  # 2 int p dx, must equal 2 sum f
        mid_offset=float(mid_offset),
    )
