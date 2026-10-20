"""`sforge judge verify` and `sforge judge exact` for Arena 1 (PLAN §5.5, §9.10, §9.11)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from . import constraints, metamorphic, metrics, zoo
from .cases import Case, NozzleCase, NozzleSweepCase, RiemannCase
from .exact_nozzle import anderson_nozzle, critical_pressures, solve_nozzle
from .exact_riemann import solve_riemann
from .numerics import muscl
from .unsteady import solve_unsteady

# Appendix H (gamma = 1.4): (left, right, p*, u*, tolerances)
TORO = [
    ("Toro 1", (1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 0.30313, 0.92745, 5e-6, 5e-6),
    ("Toro 2", (1.0, -2.0, 0.4), (1.0, 2.0, 0.4), 0.00189, 0.0, 5e-6, 1e-12),
    ("Toro 3", (1.0, 0.0, 1000.0), (1.0, 0.0, 0.01), 460.894, 19.5975, 5e-4, 5e-5),
    ("Toro 4", (1.0, 0.0, 0.01), (1.0, 0.0, 100.0), 46.0950, -6.19633, 5e-5, 5e-6),
    ("Toro 5", (5.99924, 19.5975, 460.894), (5.99242, -6.19633, 46.0950), 1691.65, 8.68977, 5e-3, 5e-6),
]
NOZZLE_H = {"A_e/A_t": (5.95, 1e-12), "p_crit1": (0.99333, 5e-6), "M_e,sub": (0.09782, 5e-6),
            "p_crit2": (0.20854, 5e-6), "p_crit3": (0.016046, 5e-7), "M_e,sup": (3.35897, 5e-6),
            "x_s": (2.0993, 5e-5), "M1": (2.0700, 5e-5), "p02/p01": (0.68817, 5e-6), "M_e": (0.14308, 5e-6)}


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def _close(name: str, value: float, expected: float, tol: float) -> Check:
    return Check(name, abs(value - expected) <= tol, f"{value:.8g} (expected {expected} +- {tol:g})")


def check_reference_values() -> list[Check]:
    out = []
    for name, WL, WR, p, u, tp, tu in TORO:
        sol = solve_riemann(WL, WR, 1.4)
        out += [_close(f"{name} p*", sol.p_star, p, tp), _close(f"{name} u*", sol.u_star, u, tu)]
    nz = anderson_nozzle()
    cp = critical_pressures(nz, 1.4)
    sol = solve_nozzle(nz, 0.6784, 1.4)
    got = {"A_e/A_t": nz.A_exit / nz.A_throat, "p_crit1": cp.p_crit1, "M_e,sub": cp.M_exit_sub,
           "p_crit2": cp.p_crit2, "p_crit3": cp.p_crit3, "M_e,sup": cp.M_exit_sup, "x_s": sol.x_shock,
           "M1": sol.M1, "p02/p01": sol.p0_ratio, "M_e": sol.M_exit}
    out += [_close(f"Anderson {k}", got[k], *NOZZLE_H[k]) for k in NOZZLE_H]
    return out


def _run(left, right, n, t, reconstruct, flux):
    x = (np.arange(n) + 0.5) / n
    W0 = np.where((x < 0.5)[:, None], left, right)
    W = np.asarray(solve_unsteady(W0, 1.0 / n, t, 1.4, reconstruct, flux=flux).W)
    return x, W


def check_zoo_sanity() -> list[Check]:
    """Gate 1: superbee sharpest and minmod most diffusive limiter on Sod; HLLC keeps R5 exactly."""
    from .numerics import hllc

    sod = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))
    sol = solve_riemann(*sod, 1.4)
    widths = {}
    for name in zoo.members("limiter"):
        x, W = _run(*sod, 200, 0.2, muscl(zoo.load("limiter", name)), hllc)
        widths[name] = metrics.riemann_metrics(x, W, sol, 0.5, 0.2, (0.0, 1.0), 1 / 200)["contact_width"]
    order = sorted(widths, key=widths.get)
    out = [Check("superbee has the narrowest Sod contact", order[0] == "superbee", f"{widths}"),
           Check("minmod has the widest Sod contact (limiters)", order[-1] == "minmod", f"{widths}")]
    mm = muscl(zoo.load("limiter", "minmod"))
    exact = solve_riemann((1.4, 0.0, 1.0), (1.0, 0.0, 1.0), 1.4)
    for name in zoo.members("flux"):
        x, W = _run((1.4, 0.0, 1.0), (1.0, 0.0, 1.0), 100, 2.0, mm, zoo.load("flux", name))
        err = float(np.max(np.abs(W - exact.sample(x, 2.0, 0.5))))
        keeps = name == "hllc"
        out.append(Check(f"{name} {'keeps' if keeps else 'smears'} the stationary contact",
                         err < 1e-12 if keeps else err > 1e-2, f"max error {err:.2e}"))
    return out


def check_zoo_constraints() -> list[Check]:
    out = []
    for name in zoo.members("limiter"):
        v = constraints.check_limiter(zoo.load("limiter", name))
        out.append(Check(f"limiter {name} hard constraints", not v, "; ".join(v) or "ok"))
    for name in zoo.members("flux"):
        v = constraints.check_flux(zoo.load("flux", name))
        out.append(Check(f"flux {name} hard constraints", not v, "; ".join(v) or "ok"))
    return out


def check_zoo_metamorphic() -> list[Check]:
    """Mirror symmetry is exact for symmetric limiters (all but Koren); scaling is exact for all."""
    from .numerics import hllc

    n = 200
    x = (np.arange(n) + 0.5) / n
    W0 = np.where((x < 0.5)[:, None], (1.0, 0.0, 1.0), (0.125, 0.0, 0.1))
    out = []
    for name in zoo.members("limiter"):
        rec = muscl(zoo.load("limiter", name))

        def run(W0_, dx_, t_, g_, rec=rec):
            return np.asarray(solve_unsteady(W0_, dx_, t_, g_, rec, flux=hllc).W)

        W = run(W0, 1 / n, 0.2, 1.4)
        mirror = metamorphic.mirror_error(run, W0, 1 / n, 0.2, 1.4, W=W)
        scaling = metamorphic.scaling_error(run, W0, 1 / n, 0.2, 1.4, W=W)
        sym = name != "koren"
        out.append(Check(f"limiter {name} mirror {'exact' if sym else 'inexact (asymmetric)'}",
                         mirror < 1e-12 if sym else mirror > 1e-6, f"{mirror:.2e}"))
        out.append(Check(f"limiter {name} scaling exact", scaling < 1e-12, f"{scaling:.2e}"))
    return out


def verify() -> list[Check]:
    return [*check_reference_values(), *check_zoo_constraints(), *check_zoo_sanity(), *check_zoo_metamorphic()]


# --- exact solutions for the blind audit ----------------------------------------------------------------------
def exact_report(case: Case) -> dict[str, Any]:
    """The judge's exact solution for one case: star/regime data plus the solution sampled at cell centres."""
    if isinstance(case, RiemannCase):
        sol = solve_riemann(case.left, case.right, case.gamma)
        a, b = case.domain
        x = a + (np.arange(case.n) + 0.5) * (b - a) / case.n
        W = sol.sample(x, case.t_end, case.x0)
        return {"kind": "riemann", "p_star": sol.p_star, "u_star": sol.u_star, "rho_star_L": sol.rho_star_L,
                "rho_star_R": sol.rho_star_R,
                "waves": [{"side": w.side, "kind": w.kind, "speeds": list(w.speeds)} for w in (sol.left, sol.right)],
                "x": x.tolist(), "rho": W[:, 0].tolist(), "u": W[:, 1].tolist(), "p": W[:, 2].tolist()}
    if isinstance(case, NozzleCase):
        return _nozzle_report(case.nozzle.build(), case.pb, case.gamma, case.n)
    if isinstance(case, NozzleSweepCase):
        nz = case.nozzle.build()
        return {"kind": "nozzle_sweep", "points": [_nozzle_report(nz, pb, case.gamma, case.n) for pb in case.pbs]}
    raise ValueError(f"no exact solution for case kind {case.kind!r}")


def _nozzle_report(nz, pb: float, g: float, n: int) -> dict[str, Any]:
    sol = solve_nozzle(nz, pb, g)
    cp = critical_pressures(nz, g)
    x_face = np.linspace(nz.x_in, nz.x_exit, n + 1)
    x = 0.5 * (x_face[1:] + x_face[:-1])
    prof = sol.profile(x)
    return {"kind": "nozzle", "pb": pb, "regime": sol.regime, "x_shock": sol.x_shock, "M1": sol.M1,
            "p0_ratio": sol.p0_ratio, "A_star_1": sol.A_star_1, "A_star_2": sol.A_star_2,
            "mass_flow": sol.mass_flow, "p_crit1": cp.p_crit1, "p_crit2": cp.p_crit2, "p_crit3": cp.p_crit3,
            "x": x.tolist(), **{k: prof[k].tolist() for k in ("M", "rho", "u", "p")}}
