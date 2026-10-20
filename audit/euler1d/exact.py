"""Blind-audit exact solutions for Arena 1 (euler1d).

Written from docs/judge/euler1d_spec.md sections 1-4 and textbook formulas (Toro 2009 ch. 4,
Anderson 1995 ch. 7) only. No code from src/schemeforge/arenas/ was read or imported.
float64 throughout (plain Python floats / numpy float64).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# --------------------------------------------------------------------------------------------
# Riemann problem (Toro 2009, ch. 4)
# --------------------------------------------------------------------------------------------


def _fk(p: float, rho: float, pk: float, ak: float, g: float) -> tuple[float, float]:
    """Toro pressure function f_K and its derivative."""
    if p > pk:
        A = 2.0 / ((g + 1.0) * rho)
        B = (g - 1.0) / (g + 1.0) * pk
        s = math.sqrt(A / (p + B))
        return (p - pk) * s, s * (1.0 - 0.5 * (p - pk) / (p + B))
    pr = p / pk
    f = 2.0 * ak / (g - 1.0) * (pr ** ((g - 1.0) / (2.0 * g)) - 1.0)
    df = 1.0 / (rho * ak) * pr ** (-(g + 1.0) / (2.0 * g))
    return f, df


@dataclass
class RiemannSolution:
    p_star: float
    u_star: float
    rho_star_L: float
    rho_star_R: float
    waves: list  # [(side, kind, (s1, s2))]


def riemann_star(WL, WR, g: float) -> RiemannSolution:
    rl, ul, pl = map(float, WL)
    rr, ur, pr = map(float, WR)
    al = math.sqrt(g * pl / rl)
    ar = math.sqrt(g * pr / rr)
    du = ur - ul
    if 2.0 / (g - 1.0) * (al + ar) <= du:
        raise ValueError("vacuum generation")

    def f(p):
        fl, dfl = _fk(p, rl, pl, al, g)
        fr, dfr = _fk(p, rr, pr, ar, g)
        return fl + fr + du, dfl + dfr

    # Bracket: f is monotone increasing on (0, inf), f(0+) < 0 (no vacuum).
    lo = 0.0
    hi = max(pl, pr)
    while f(hi)[0] < 0.0:
        lo = hi
        hi *= 2.0
    # two-rarefaction guess as start (Toro 4.46), clipped into bracket
    z = (g - 1.0) / (2.0 * g)
    p = ((al + ar - 0.5 * (g - 1.0) * du) / (al / pl**z + ar / pr**z)) ** (1.0 / z)
    if not (lo < p < hi):
        p = 0.5 * (lo + hi)
    # safeguarded Newton, then bisection-polish to full precision
    for _ in range(200):
        fv, dfv = f(p)
        if fv == 0.0:
            break
        if fv < 0.0:
            lo = p
        else:
            hi = p
        pn = p - fv / dfv
        if not (lo < pn < hi):
            pn = 0.5 * (lo + hi)
        if abs(pn - p) <= 1e-16 * p:
            p = pn
            break
        p = pn
    # final: a few bisection/secant checks so that the result is the double nearest the root
    for _ in range(4):
        fv, dfv = f(p)
        if fv == 0.0:
            break
        pn = p - fv / dfv
        if pn == p:
            break
        p = pn
    ps = p
    fl, _ = _fk(ps, rl, pl, al, g)
    fr, _ = _fk(ps, rr, pr, ar, g)
    us = 0.5 * (ul + ur) + 0.5 * (fr - fl)
    gm = (g - 1.0) / (g + 1.0)
    waves = []
    if ps > pl:
        rsl = rl * (ps / pl + gm) / (gm * ps / pl + 1.0)
        S = ul - al * math.sqrt((g + 1.0) / (2.0 * g) * ps / pl + (g - 1.0) / (2.0 * g))
        waves.append((-1, "shock", (S, S)))
    else:
        rsl = rl * (ps / pl) ** (1.0 / g)
        asl = al * (ps / pl) ** ((g - 1.0) / (2.0 * g))
        waves.append((-1, "rarefaction", (ul - al, us - asl)))
    if ps > pr:
        rsr = rr * (ps / pr + gm) / (gm * ps / pr + 1.0)
        S = ur + ar * math.sqrt((g + 1.0) / (2.0 * g) * ps / pr + (g - 1.0) / (2.0 * g))
        waves.append((1, "shock", (S, S)))
    else:
        rsr = rr * (ps / pr) ** (1.0 / g)
        asr = ar * (ps / pr) ** ((g - 1.0) / (2.0 * g))
        waves.append((1, "rarefaction", (ur + ar, us + asr)))
    return RiemannSolution(ps, us, rsl, rsr, waves)


def riemann_sample(WL, WR, g: float, sol: RiemannSolution, xi: float) -> tuple[float, float, float]:
    rl, ul, pl = map(float, WL)
    rr, ur, pr = map(float, WR)
    al = math.sqrt(g * pl / rl)
    ar = math.sqrt(g * pr / rr)
    ps, us = sol.p_star, sol.u_star
    if xi < us:
        side, kind, (s1, s2) = sol.waves[0]
        if kind == "shock":
            if xi < s1:
                return rl, ul, pl
            return sol.rho_star_L, us, ps
        # rarefaction: head s1, tail s2
        if xi < s1:
            return rl, ul, pl
        if xi >= s2:
            return sol.rho_star_L, us, ps
        if xi == s1:  # exactly on head: inner side value equals the fan value at head = W_L
            pass
        c = 2.0 / (g + 1.0) + (g - 1.0) / ((g + 1.0) * al) * (ul - xi)
        return (
            rl * c ** (2.0 / (g - 1.0)),
            2.0 / (g + 1.0) * (al + 0.5 * (g - 1.0) * ul + xi),
            pl * c ** (2.0 * g / (g - 1.0)),
        )
    side, kind, (s1, s2) = sol.waves[1]
    if kind == "shock":
        if xi > s1:
            return rr, ur, pr
        return sol.rho_star_R, us, ps
    if xi > s1:
        return rr, ur, pr
    if xi <= s2:
        return sol.rho_star_R, us, ps
    c = 2.0 / (g + 1.0) - (g - 1.0) / ((g + 1.0) * ar) * (ur - xi)
    return (
        rr * c ** (2.0 / (g - 1.0)),
        2.0 / (g + 1.0) * (-ar + 0.5 * (g - 1.0) * ur + xi),
        pr * c ** (2.0 * g / (g - 1.0)),
    )


def riemann_case(case: dict) -> dict:
    g = float(case.get("gamma", 1.4))
    WL, WR = case["left"], case["right"]
    x0 = float(case.get("x0", 0.5))
    a, b = map(float, case.get("domain", [0.0, 1.0]))
    n = int(case["n"])
    t = float(case["t_end"])
    sol = riemann_star(WL, WR, g)
    dx = (b - a) / n
    x = a + (np.arange(n) + 0.5) * dx
    rho = np.empty(n)
    u = np.empty(n)
    p = np.empty(n)
    for i, xi in enumerate(x):
        rho[i], u[i], p[i] = riemann_sample(WL, WR, g, sol, (xi - x0) / t)
    return {
        "kind": "riemann",
        "p_star": sol.p_star,
        "u_star": sol.u_star,
        "rho_star_L": sol.rho_star_L,
        "rho_star_R": sol.rho_star_R,
        "waves": [{"side": s, "kind": k, "speeds": list(sp)} for s, k, sp in sol.waves],
        "x": x.tolist(),
        "rho": rho.tolist(),
        "u": u.tolist(),
        "p": p.tolist(),
    }


# --------------------------------------------------------------------------------------------
# Quasi-1D nozzle (Anderson 1995 ch. 7; spec section 3)
# --------------------------------------------------------------------------------------------


def psi(M: float, g: float) -> float:
    return 1.0 + 0.5 * (g - 1.0) * M * M


def area_mach(M: float, g: float) -> float:
    return (1.0 / M) * ((2.0 / (g + 1.0)) * psi(M, g)) ** ((g + 1.0) / (2.0 * (g - 1.0)))


def _log_am(M: float, g: float) -> float:
    return -math.log(M) + (g + 1.0) / (2.0 * (g - 1.0)) * math.log((2.0 / (g + 1.0)) * psi(M, g))


def mach_from_area(r: float, g: float, supersonic: bool) -> float:
    """Root of A/A*(M) = r, r >= 1. Bisection on log form, then Newton polish."""
    if r <= 1.0:
        return 1.0
    lr = math.log(r)
    if supersonic:
        lo, hi = 1.0, 2.0
        while _log_am(hi, g) < lr:
            lo, hi = hi, hi * 2.0
        # F increasing in M on (1, inf)
        sgn = 1.0
    else:
        lo, hi = 0.0, 1.0
        sgn = -1.0  # F decreasing on (0,1)
    for _ in range(2000):
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            break
        v = sgn * (_log_am(mid, g) - lr)
        if v < 0.0:
            lo = mid
        else:
            hi = mid
    M = 0.5 * (lo + hi)
    for _ in range(5):
        # d/dM log(A/A*) = -1/M + (g+1)/2 * M/psi  = (M^2-1)/(M psi)
        d = (M * M - 1.0) / (M * psi(M, g))
        if d == 0.0:
            break
        Mn = M - (_log_am(M, g) - lr) / d
        if not (Mn > 0) or abs(Mn - M) > 1e-6 * M:
            break
        if Mn == M:
            break
        M = Mn
    return M


def p_ratio(M: float, g: float) -> float:
    return psi(M, g) ** (-g / (g - 1.0))


def shock_p0_ratio(M1: float, g: float) -> float:
    m2 = M1 * M1
    return ((g + 1.0) * m2 / ((g - 1.0) * m2 + 2.0)) ** (g / (g - 1.0)) * (
        (g + 1.0) / (2.0 * g * m2 - (g - 1.0))
    ) ** (1.0 / (g - 1.0))


def shock_p_jump(M1: float, g: float) -> float:
    return 1.0 + 2.0 * g / (g + 1.0) * (M1 * M1 - 1.0)


class Geometry:
    x_in: float
    x_exit: float
    x_t: float
    A_t: float

    def area(self, x: float) -> float:  # pragma: no cover
        raise NotImplementedError

    def x_of_area_div(self, a: float) -> float:  # pragma: no cover
        """x in [x_t, x_exit] with A(x) = a (divergent part)."""
        raise NotImplementedError


class Anderson(Geometry):
    def __init__(self):
        self.x_in, self.x_exit, self.x_t, self.A_t = 0.0, 3.0, 1.5, 1.0

    def area(self, x):
        return 1.0 + 2.2 * (x - 1.5) ** 2

    def x_of_area_div(self, a):
        return 1.5 + math.sqrt((a - 1.0) / 2.2)


class Parabolic(Geometry):
    def __init__(self, R, L, Ri, x_in=0.0):
        self.R, self.L, self.Ri = R, L, Ri
        self.x_in, self.x_exit, self.x_t, self.A_t = x_in, 1.0 + L, 1.0, 1.0

    def area(self, x):
        if x < 1.0:
            return 1.0 + (self.Ri - 1.0) * (1.0 - x) ** 2
        return 1.0 + (self.R - 1.0) * ((x - 1.0) / self.L) ** 2

    def x_of_area_div(self, a):
        return 1.0 + self.L * math.sqrt((a - 1.0) / (self.R - 1.0))


class Conical(Geometry):
    delta = 0.2

    def __init__(self, R, L, Ri, x_in=0.0):
        self.R, self.L, self.Ri = R, L, Ri
        self.x_in, self.x_exit, self.x_t, self.A_t = x_in, 1.0 + L, 1.0, 1.0
        d = self.delta
        self.k = (math.sqrt(R) - 1.0) / (math.sqrt(L * L + d * d) - d)

    def area(self, x):
        if x < 1.0:
            return 1.0 + (self.Ri - 1.0) * (1.0 - x) ** 2
        d = self.delta
        r = 1.0 + self.k * (math.sqrt((x - 1.0) ** 2 + d * d) - d)
        return r * r

    def x_of_area_div(self, a):
        d = self.delta
        s = (math.sqrt(a) - 1.0) / self.k + d
        return 1.0 + math.sqrt(max(s * s - d * d, 0.0))


def make_geometry(spec: dict | None) -> Geometry:
    spec = spec or {"type": "anderson"}
    t = spec.get("type", "anderson")
    if t == "anderson":
        return Anderson()
    args = (float(spec["area_ratio"]), float(spec["length"]), float(spec["inlet_ratio"]),
            float(spec.get("x_in", 0.0)))
    if t == "parabolic":
        return Parabolic(*args)
    if t == "conical":
        return Conical(*args)
    raise ValueError(t)


def _bisect(f, lo, hi):
    flo = f(lo)
    for _ in range(2000):
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            break
        fm = f(mid)
        if fm == 0.0:
            return mid
        if (fm < 0.0) == (flo < 0.0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


def nozzle_case(case: dict) -> dict:
    g = float(case.get("gamma", 1.4))
    pb = float(case["pb"])
    n = int(case["n"])
    geo = make_geometry(case.get("nozzle"))
    Ae = geo.area(geo.x_exit)
    At = geo.A_t
    er = Ae / At
    Me_sub = mach_from_area(er, g, False)
    Me_sup = mach_from_area(er, g, True)
    pc1 = p_ratio(Me_sub, g)
    pc3 = p_ratio(Me_sup, g)
    pc2 = pc3 * shock_p_jump(Me_sup, g)
    a0 = math.sqrt(g)
    dx = (geo.x_exit - geo.x_in) / n
    xs_cells = geo.x_in + (np.arange(n) + 0.5) * dx

    x_shock = None
    M1 = None
    p0r = 1.0
    if pb > pc1:
        regime = "subsonic"
        Me = math.sqrt(2.0 / (g - 1.0) * (pb ** (-(g - 1.0) / g) - 1.0))
        Astar1 = Ae / area_mach(Me, g)
        Astar2 = Astar1
    elif pb > pc2:
        regime = "shock"
        Astar1 = At

        def pexit(M):
            r0 = shock_p0_ratio(M, g)
            Me2 = mach_from_area(Ae / (At / r0), g, False)
            return r0 * p_ratio(Me2, g) - pb

        # pb == p_crit1 exactly: degenerate shock of zero strength at the throat. p_exit - p_b
        # behaves like (M1 - 1)^3 there, so a root finder only resolves M1 to ~eps^(1/3).
        M1 = 1.0 if pb == pc1 else _bisect(pexit, 1.0, Me_sup)
        p0r = shock_p0_ratio(M1, g)
        Astar2 = At / p0r
        x_shock = geo.x_of_area_div(At * area_mach(M1, g))
    else:
        regime = "supersonic"
        Astar1 = At
        Astar2 = At
    choked = regime != "subsonic"
    mass_flow = Astar1 * (2.0 / (g + 1.0)) ** ((g + 1.0) / (2.0 * (g - 1.0))) * a0  # rho0=1

    M = np.empty(n)
    rho = np.empty(n)
    u = np.empty(n)
    p = np.empty(n)
    for i, x in enumerate(xs_cells):
        A = geo.area(float(x))
        p0 = 1.0
        if not choked:
            m = mach_from_area(A / Astar1, g, False)
        elif x == geo.x_t:
            m = 1.0
        elif x < geo.x_t:
            m = mach_from_area(A / At, g, False)
        elif regime == "shock" and x > x_shock:
            m = mach_from_area(A / Astar2, g, False)
            p0 = p0r
        else:
            m = mach_from_area(A / At, g, True)
        ps_ = psi(m, g)
        M[i] = m
        p[i] = p0 * ps_ ** (-g / (g - 1.0))
        rho[i] = p0 * ps_ ** (-1.0 / (g - 1.0))
        u[i] = m * a0 * math.sqrt(1.0 / ps_)
    return {
        "kind": "nozzle",
        "pb": pb,
        "regime": regime,
        "x_shock": x_shock,
        "M1": M1,
        "p0_ratio": p0r,
        "A_star_1": Astar1,
        "A_star_2": Astar2,
        "mass_flow": mass_flow,
        "p_crit1": pc1,
        "p_crit2": pc2,
        "p_crit3": pc3,
        "x": xs_cells.tolist(),
        "M": M.tolist(),
        "rho": rho.tolist(),
        "u": u.tolist(),
        "p": p.tolist(),
    }


def solve(case: dict) -> dict:
    if case["kind"] == "riemann":
        return riemann_case(case)
    if case["kind"] == "nozzle":
        return nozzle_case(case)
    raise ValueError(case["kind"])
