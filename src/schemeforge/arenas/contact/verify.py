"""`sforge judge verify` and `sforge judge exact` for Arena 2 (plan step 6, docs/judge/contact_spec.md §Audit).

verify(): the judge's self-checks against the spec's own claims (exact homogeneous cases, classical reference, patch
test, Hertz error floor, zoo constraints).
exact_report(case): the judge's exact and reference values for one case, for the blind audit. The audit medium is the
zoo neo-Hooke, psi = gamma psi_body (spec §Audit), so the auditor can re-implement it from the spec alone.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from . import constraints, reference, zoo
from .cases import Case, GapClosureCase, HertzCase, SimpleShearCase, dev_suite
from .metrics import edge_traction

AUDIT_MEDIUM = "neo_hooke"
CLASSICAL_MULTIPLIERS = (1e2, 1e3, 1e4)  # spec §C0a: Richardson extrapolation over these penalties


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def _rel(a: float, b: float) -> float:
    return abs(a - b) / max(abs(b), 1e-300)


# --- exact and reference values for the blind audit ----------------------------------------------------------------
def _gap_closure_report(case: GapClosureCase) -> dict[str, Any]:
    """Exact homogeneous solution (audit medium), ideal contact, the judge's FE solve with the audit medium, and the
    extrapolated classical reference. Forces per unit thickness, compressive positive."""
    from . import evaluate, solve

    psi = zoo.load("medium", AUDIT_MEDIUM)
    f_ideal = float(reference.ideal_gap_force(case, case.push))
    f_ex, t_ex = reference.exact_gap_closure(psi, case, case.push)
    f_half, t_half = reference.exact_gap_closure(psi, case, 0.5 * case.gap)
    res = solve.gap_closure(psi, case)
    m, _ = evaluate.gap_closure_metrics(case, res)
    cl = {k: solve.gap_closure_classical(case, k) for k in CLASSICAL_MULTIPLIERS}
    push = cl[CLASSICAL_MULTIPLIERS[0]][0]
    f_cl = [solve.classical_extrapolated({k: float(cl[k][1][i]) for k in CLASSICAL_MULTIPLIERS})
            for i in range(push.size)]
    return {"kind": "gap_closure", "id": case.id, "medium": AUDIT_MEDIUM,
            "ideal_force": f_ideal,
            "exact_force": f_ex, "exact_thickness": t_ex, "exact_force_half": f_half, "exact_thickness_half": t_half,
            "exact_leak_pre": f_half / f_ideal, "exact_gap_res": t_ex / case.gap,
            "exact_force_err": f_ex / f_ideal - 1.0,
            "fe_push": res.push.tolist(), "fe_force": res.force.tolist(), "fe_thickness": res.medium_thickness,
            "fe_wall_pressure": res.wall_pressure.tolist(),
            "fe_leak_pre": m["leak_pre"], "fe_gap_res": m["gap_res"], "fe_force_err": m["force_err"],
            "fe_pressure_spread": m["pressure_spread"], "fe_min_J_medium": m["min_J_medium"],
            "classical_push": push.tolist(), "classical_force": f_cl}


def _simple_shear_report(case: SimpleShearCase) -> dict[str, Any]:
    psi = zoo.load("medium", AUDIT_MEDIUM)
    mu, lmbda = reference.lame(case.E, case.nu)
    pxy, pyy = reference.shear_stress(psi, {"mu": mu, "lmbda": lmbda, "gamma": case.gamma}, case.shear)
    return {"kind": "simple_shear", "id": case.id, "medium": AUDIT_MEDIUM, "mu": mu, "lmbda": lmbda,
            "P_xy": pxy, "P_yy": pyy, "shear_parasitic": pxy / (mu * case.shear),
            "normal_parasitic": pyy / (mu * case.shear)}


def _hertz_report(case: HertzCase) -> dict[str, Any]:
    """The classical reference (no medium) and the judge's Hertz metrics computed on it: the nodal contact forces x,
    f on the flat (half model) let the auditor recompute every metric from the spec."""
    from . import evaluate, solve

    res = solve.hertz_classical(case)
    m, _ = evaluate.hertz_metrics(case, res)
    es = case.E / (1.0 - case.nu**2)
    a_h = float(np.sqrt(4.0 * res.load * case.R / (np.pi * es)))
    return {"kind": "hertz", "id": case.id, "reference": "classical", "x": res.x.tolist(), "f": res.f.tolist(),
            "p": edge_traction(res.x, res.f).tolist(), "load": res.load, "E_star": es, "a_hertz": a_h,
            "p0_hertz": 2.0 * res.load / (np.pi * a_h),
            **{k: m[k] for k in ("a_err", "p0_err", "p_l2", "leak_out")}}


def exact_report(case: Case) -> dict[str, Any]:
    """The judge's exact and reference values for one case (spec §Audit)."""
    if isinstance(case, GapClosureCase):
        return _gap_closure_report(case)
    if isinstance(case, SimpleShearCase):
        return _simple_shear_report(case)
    if isinstance(case, HertzCase):
        return _hertz_report(case)
    raise ValueError(f"no exact solution for case {type(case).__name__}")


# --- self-checks -------------------------------------------------------------------------------------------------
def check_exact_cases() -> list[Check]:
    """C0a and C1 (FE with the audit medium vs the exact homogeneous solution; classical vs ideal) and C0b."""
    out = []
    for case in dev_suite():
        if isinstance(case, GapClosureCase):
            r = exact_report(case)
            e_f = _rel(r["fe_force"][-1], r["exact_force"])
            e_t = _rel(r["fe_thickness"], r["exact_thickness"])
            e_c = _rel(r["classical_force"][-1], r["ideal_force"])
            pre = max(abs(f) for p, f in zip(r["classical_push"], r["classical_force"], strict=True) if p <= case.gap)
            ok = max(e_f, e_t) <= 1e-9 and e_c <= 1e-9 and pre <= 1e-12 and r["fe_pressure_spread"] <= 1e-7
            out.append(Check(f"{case.id} exact", ok, f"FE force {e_f:.1e}, thickness {e_t:.1e}; classical {e_c:.1e}, "
                             f"pre-contact {pre:.1e}; pressure spread {r['fe_pressure_spread']:.1e}"))
        elif isinstance(case, SimpleShearCase):
            r = exact_report(case)
            err = abs(r["shear_parasitic"] - case.gamma) / case.gamma
            out.append(Check(f"{case.id} neo-Hooke shear = gamma", err <= 1e-12, f"rel. error {err:.1e}"))
    return out


def check_hertz_floor() -> list[Check]:
    """Classical Hertz on the dev mesh within the stated error floor (spec §C2: a +0.9 %, p0 -0.5 %)."""
    r = exact_report(HertzCase("C2-classical"))
    ok = abs(r["a_err"]) <= 0.015 and abs(r["p0_err"]) <= 0.01
    return [Check("C2 classical vs Hertz (dev mesh)", ok, f"a_err {r['a_err']:+.4f}, p0_err {r['p0_err']:+.4f}")]


def check_edge_traction() -> list[Check]:
    """A traction quadratic per element comes back exactly from its consistent nodal forces."""
    x = np.array([0.0, 0.1, 0.2, 0.35, 0.5, 0.6, 0.7])
    t = 1.0 + 2.0 * x - 3.0 * x**2
    f = np.zeros_like(x)
    local = np.array([[4.0, 2.0, -1.0], [2.0, 16.0, 2.0], [-1.0, 2.0, 4.0]]) / 30.0
    for e in range(0, x.size - 2, 2):
        idx = np.array([e, e + 1, e + 2])
        f[idx] += local @ t[idx] * (x[e + 2] - x[e])
    err = float(np.max(np.abs(edge_traction(x, f) - t)))
    return [Check("edge traction (quadratic)", err <= 1e-12, f"max error {err:.1e}")]


def check_zoo_constraints() -> list[Check]:
    out = []
    for name in zoo.members("medium"):
        v = constraints.check_medium(zoo.load("medium", name))
        out.append(Check(f"zoo {name} constraints", not v, "; ".join(v) or "all pass"))
    return out


def verify() -> list[Check]:
    return [*check_edge_traction(), *check_exact_cases(), *check_hertz_floor(), *check_zoo_constraints()]
