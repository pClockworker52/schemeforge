"""Score one Arena 1 slot function on a suite (PLAN §5.7-5.8). Runs inside the sandboxed worker process.

evaluate(fn, slot, suite, extra_cases) -> report (JSON-serializable dict):
    status       "ok" | "rejected"
    violations   hard-constraint violations (any -> rejected)
    cases        {case_id: {metric: value, "seconds": wall time}}
    metamorphic  {mirror_err, scaling_err, galilean_err} on R1 (measured, not required)
    cost         wall time per cell update on R1 [ns] (normalized to the zoo median by the leaderboard)
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterable
from typing import Any

import numpy as np

from . import constraints, metamorphic, metrics, zoo
from .cases import (
    INITS,
    Case,
    NozzleCase,
    NozzleSweepCase,
    ReferenceCase,
    RiemannCase,
    SmoothCase,
    dev_suite,
    load_reference,
)
from .exact_nozzle import solve_nozzle
from .exact_riemann import solve_riemann
from .numerics import hllc, muscl
from .steady import default_operator, make_grid, solve_explicit, solve_implicit
from .unsteady import solve_unsteady

SLOTS = ("limiter", "flux", "reconstruction")
SUITES = ("smoke", "dev")


def slot_scheme(fn: Callable, slot: str) -> tuple[Callable, Callable]:
    """(reconstruct, flux) for a candidate in the given slot; the other component is the judge default."""
    if slot == "limiter":
        return muscl(fn), hllc
    if slot == "flux":
        return muscl(zoo.load("limiter", "van_leer")), fn
    if slot == "reconstruction":
        return fn, hllc
    raise ValueError(f"slot {slot!r} is not evaluated in Arena 1 yet")


def slot_constraints(fn: Callable, slot: str) -> list[str]:
    if slot == "limiter":
        return constraints.check_limiter(fn)
    if slot == "flux":
        return constraints.check_flux(fn)
    return []  # reconstruction: only run-level constraints (zoo use only in Phase 1)


def smoke_suite() -> list[Case]:
    return [RiemannCase("smoke-R1", (1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 0.2, 50)]


def suite_cases(suite: str) -> list[Case]:
    if suite == "smoke":
        return smoke_suite()
    if suite == "dev":
        return dev_suite()
    raise ValueError(f"suite {suite!r} is not available")


# --- per-kind runners ---------------------------------------------------------------------------------------
def _grid(n: int, domain: tuple[float, float]) -> tuple[np.ndarray, float]:
    dx = (domain[1] - domain[0]) / n
    return domain[0] + (np.arange(n) + 0.5) * dx, dx


def _unsteady(W0, dx, t_end, g, reconstruct, flux, bc="transmissive"):
    res = solve_unsteady(W0, dx, t_end, g, reconstruct, flux=flux, bc=bc)
    return np.asarray(res.W), res.steps


def run_riemann(case: RiemannCase, reconstruct, flux) -> tuple[dict[str, float], list[str], np.ndarray]:
    x, dx = _grid(case.n, case.domain)
    W0 = np.where((x < case.x0)[:, None], case.left, case.right)
    W, _ = _unsteady(W0, dx, case.t_end, case.gamma, reconstruct, flux)
    v = constraints.check_run(W)
    if v:
        return {}, v, W
    sol = solve_riemann(case.left, case.right, case.gamma)
    return metrics.riemann_metrics(x, W, sol, case.x0, case.t_end, case.domain, dx), [], W


def run_reference(case: ReferenceCase, reconstruct, flux) -> tuple[dict[str, float], list[str]]:
    x, dx = _grid(case.n, case.domain)
    W, _ = _unsteady(INITS[case.init](x), dx, case.t_end, case.gamma, reconstruct, flux)
    v = constraints.check_run(W)
    if v:
        return {}, v
    ref = load_reference(case)
    scales = metrics.state_scales(ref, case.gamma)
    l1 = float(np.mean([np.mean(np.abs(W[:, k] - ref[:, k])) / scales[k] for k in range(3)]))
    return {"l1_ref": l1}, []


def run_smooth(case: SmoothCase, reconstruct, flux) -> tuple[dict[str, float], list[str]]:
    errs = []
    for n in case.ns:
        x, dx = _grid(n, (0.0, 1.0))
        W0 = np.stack([1.0 + case.amp * np.sin(2 * np.pi * x), np.full(n, case.u0), np.ones(n)], axis=1)
        W, _ = _unsteady(W0, dx, case.t_end, case.gamma, reconstruct, flux, bc="periodic")
        v = constraints.check_run(W)
        if v:
            return {}, v
        exact = 1.0 + case.amp * np.sin(2 * np.pi * (x - case.u0 * case.t_end))
        errs.append(float(np.mean(np.abs(W[:, 0] - exact))))
    return {"order_smooth": metrics.smooth_order(errs, case.ns), "l1_smooth": errs[-1]}, []


def run_nozzle(case: NozzleCase, reconstruct, flux) -> tuple[dict[str, float], list[str]]:
    nz = case.nozzle.build()
    grid = make_grid(nz, case.n)
    op = default_operator(reconstruct, flux)
    expl = solve_explicit(grid, case.pb, case.gamma, op)
    impl = solve_implicit(grid, case.pb, case.gamma, op)
    v = []
    for name, r in (("explicit", expl), ("implicit", impl)):
        if r.failed:
            v.append(f"{name} pseudo-time solver failed (non-physical state)")
        v += [f"{name}: {m}" for m in constraints.check_run(r.W)]
    if v:
        return {}, v
    best = impl if impl.converged or not expl.converged else expl
    out = metrics.nozzle_metrics(grid.x, best.W, grid.A, solve_nozzle(nz, case.pb, case.gamma), grid.dx)
    out.update(
        res_orders_expl=expl.orders,
        newton_iters=float(impl.iterations if impl.converged else 300),
        limit_cycle=float(expl.limit_cycle),
        converged_expl=float(expl.converged),
        converged_impl=float(impl.converged),
    )
    return out, []


def run_nozzle_sweep(case: NozzleSweepCase, reconstruct, flux) -> tuple[dict[str, float], list[str]]:
    nz = case.nozzle.build()
    grid = make_grid(nz, case.n)
    op = default_operator(reconstruct, flux)
    x_from = grid.x_face[int(np.argmax(grid.x > nz.x_throat))]
    J_num, J_ex, iters, conv = [], [], [], []
    for pb in case.pbs:
        r = solve_implicit(grid, pb, case.gamma, op)
        v = constraints.check_run(r.W)
        if r.failed:
            v.insert(0, "implicit pseudo-time solver failed (non-physical state)")
        if v:
            return {}, v
        J_num.append(metrics.wall_force_numerical(r.W, grid.A_face, grid.x, nz.x_throat))
        J_ex.append(metrics.wall_force_exact(solve_nozzle(nz, pb, case.gamma), nz, x_from))
        iters.append(r.iterations if r.converged else 300)
        conv.append(r.converged)
    return {
        "roughness_J": metrics.roughness(np.array(J_num), np.array(J_ex)),
        "newton_iters": float(np.mean(iters)),
        "converged_impl": float(np.mean(conv)),
    }, []


# --- evaluate -----------------------------------------------------------------------------------------------
def evaluate(fn: Callable, slot: str, suite: str, extra_cases: Iterable[Case] = ()) -> dict[str, Any]:
    t_start = time.perf_counter()
    report: dict[str, Any] = {"slot": slot, "suite": suite, "violations": [], "cases": {}, "metamorphic": {}}
    v = slot_constraints(fn, slot)
    if v:
        report.update(status="rejected", violations=v, seconds=time.perf_counter() - t_start)
        return report
    reconstruct, flux = slot_scheme(fn, slot)
    for case in [*suite_cases(suite), *extra_cases]:
        t0 = time.perf_counter()
        try:
            if isinstance(case, RiemannCase):
                m, v, W = run_riemann(case, reconstruct, flux)
                if case.id in ("R1", "smoke-R1") and not v:
                    v += _r1_extras(case, reconstruct, flux, W, report)
            elif isinstance(case, ReferenceCase):
                m, v = run_reference(case, reconstruct, flux)
            elif isinstance(case, SmoothCase):
                m, v = run_smooth(case, reconstruct, flux)
            elif isinstance(case, NozzleCase):
                m, v = run_nozzle(case, reconstruct, flux)
            elif isinstance(case, NozzleSweepCase):
                m, v = run_nozzle_sweep(case, reconstruct, flux)
            else:
                raise TypeError(type(case).__name__)
        except Exception as exc:  # noqa: BLE001 - candidate code can fail in any way
            m, v = {}, [f"{type(exc).__name__}: {exc}"]
        report["cases"][case.id] = {**m, "seconds": time.perf_counter() - t0}
        report["violations"] += [f"{case.id}: {msg}" for msg in v]
    report["status"] = "rejected" if report["violations"] else "ok"
    report["seconds"] = time.perf_counter() - t_start
    return report


def _r1_extras(case: RiemannCase, reconstruct, flux, W: np.ndarray, report: dict) -> list[str]:
    """Determinism (hard) plus cost and metamorphic measurements on R1."""
    x, dx = _grid(case.n, case.domain)
    W0 = np.where((x < case.x0)[:, None], case.left, case.right)
    t0 = time.perf_counter()
    W2, steps = _unsteady(W0, dx, case.t_end, case.gamma, reconstruct, flux)
    report["cost"] = (time.perf_counter() - t0) / (steps * 3 * case.n) * 1e9
    if not np.array_equal(W, W2):
        return ["run is not deterministic (two identical runs differ)"]
    if case.id == "R1":
        def run(W0_, dx_, t_, g_):
            return _unsteady(W0_, dx_, t_, g_, reconstruct, flux)[0]

        report["metamorphic"] = {
            "mirror_err": metamorphic.mirror_error(run, W0, dx, case.t_end, case.gamma, W=W),
            "scaling_err": metamorphic.scaling_error(run, W0, dx, case.t_end, case.gamma, W=W),
            "galilean_err": metamorphic.galilean_error(run, W0, dx, case.t_end, case.gamma, W=W),
        }
    return []
