"""Score one Arena 2 slot function on a suite. Runs inside the sandboxed worker process.

evaluate(fn, slot, suite, extra_cases) -> report (JSON-serializable dict), the same shape as Arena 1's:
    status       "ok" | "rejected"
    violations   hard-constraint violations (any -> rejected)
    cases        {case_id: {metric: value, "seconds": wall time}}
    metamorphic  {} (none yet)
Step 1 has the smoke suite only; dev follows in step 2, promo in step 4 (docs/plans/2026-10-30-phase6.md).
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterable
from typing import Any

import numpy as np

from . import constraints
from .cases import Case, GapClosureCase, smoke_suite

# slot -> hard-constraint checker. The solver wraps the candidate itself (solve.medium_material).
SLOT_TABLE: dict[str, Callable[[Callable], list[str]]] = {"medium": constraints.check_medium}
SLOTS = tuple(SLOT_TABLE)
SUITES = ("smoke",)


def suite_cases(suite: str) -> list[Case]:
    if suite == "smoke":
        return smoke_suite()
    raise ValueError(f"suite {suite!r} is not available in Arena 2 yet")


def gap_closure_metrics(case: GapClosureCase, res) -> tuple[dict[str, float], list[str]]:
    """C0a metrics. leak_pre: force at half the gap over the ideal force at full push; gap_res: medium thickness left
    at full push over the gap; stiffness_err: post-contact stiffness relative to the column's E/(1-nu^2) w/h."""
    k_ideal = case.E / (1.0 - case.nu**2) * case.width / case.height
    f_ideal = k_ideal * (case.push - case.gap)
    f_half = float(np.interp(0.5 * case.gap, res.push, res.force))
    k_last = float((res.force[-1] - res.force[-2]) / (res.push[-1] - res.push[-2]))
    m = {"converged": 1.0, "leak_pre": f_half / f_ideal, "gap_res": res.medium_thickness / case.gap,
         "stiffness_err": k_last / k_ideal - 1.0, "newton_iters": float(sum(res.newton_iters)),
         "min_J_medium": res.min_j_medium}
    v = [] if res.min_j_medium > 0.0 else ["medium inverted (min J <= 0)"]
    return m, v


def run_case(case: Case, psi: Callable) -> tuple[dict[str, float], list[str]]:
    """Metrics and violations of one case. A Newton failure is a result (converged = 0: soft media without
    regularization fail to close the gap, and robustness is what Target D measures), not a violation."""
    import felupe as fem

    from . import solve

    try:
        if isinstance(case, GapClosureCase):
            return gap_closure_metrics(case, solve.gap_closure(psi, case))
        raise TypeError(type(case).__name__)
    except fem.tools.NewtonConvergenceError:
        return {"converged": 0.0}, []
    except Exception as exc:  # noqa: BLE001 - candidate code and Newton can fail in any way
        return {}, [f"{type(exc).__name__}: {exc}"]


def evaluate(fn: Callable, slot: str, suite: str, extra_cases: Iterable[Case] = ()) -> dict[str, Any]:
    t_start = time.perf_counter()
    report: dict[str, Any] = {"slot": slot, "suite": suite, "violations": [], "cases": {}, "metamorphic": {}}
    if slot not in SLOT_TABLE:
        raise ValueError(f"slot {slot!r} is not evaluated in Arena 2 yet")
    v = SLOT_TABLE[slot](fn)
    if v:
        report.update(status="rejected", violations=v, seconds=time.perf_counter() - t_start)
        return report
    for case in [*suite_cases(suite), *extra_cases]:
        t0 = time.perf_counter()
        m, v = run_case(case, fn)
        report["cases"][case.id] = {**m, "seconds": time.perf_counter() - t0}
        report["violations"] += [f"{case.id}: {msg}" for msg in v]
    report["status"] = "rejected" if report["violations"] else "ok"
    report["seconds"] = time.perf_counter() - t_start
    return report
