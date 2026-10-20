"""Problem-existence study for Arena 1 (PLAN §9.9): the zoo on a 41-point back-pressure sweep of the Anderson
nozzle with both pseudo-time solvers, plus the front plot. Held-out numbers come from the registry (promo runs);
this script never touches held-out instances.

    uv run python scripts/euler1d_baseline.py            # writes docs/judge/baseline/*.json and *.png
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

OUT = Path("docs/judge/baseline")
LIMITERS = ["minmod", "van_albada", "van_leer", "venkatakrishnan", "mc", "koren", "superbee"]
N_POINTS = 41


def sweep(name_core: tuple[str, int]) -> dict:
    name, core = name_core
    os.sched_setaffinity(0, {core})
    from schemeforge.arenas.euler1d import metrics, zoo
    from schemeforge.arenas.euler1d.exact_nozzle import anderson_nozzle, back_pressure_for_shock, solve_nozzle
    from schemeforge.arenas.euler1d.numerics import muscl
    from schemeforge.arenas.euler1d.steady import default_operator, make_grid, solve_explicit, solve_implicit

    nz = anderson_nozzle()
    grid = make_grid(nz, 120)
    xs = np.linspace(2.1 - 15 * grid.dx, 2.1 + 15 * grid.dx, N_POINTS)
    pbs = [back_pressure_for_shock(nz, x, 1.4) for x in xs]
    x_from = grid.x_face[int(np.argmax(grid.x > nz.x_throat))]
    op = default_operator(muscl(zoo.load("limiter", name)))
    J_ex = [metrics.wall_force_exact(solve_nozzle(nz, pb, 1.4), nz, x_from) for pb in pbs]
    out = {"limiter": name, "x_shock": xs.tolist(), "pb": pbs, "J_exact": J_ex}
    for label, solver in (("explicit", solve_explicit), ("implicit", solve_implicit)):
        J, orders, iters, conv = [], [], [], []
        for pb in pbs:
            r = solver(grid, pb, 1.4, op)
            J.append(metrics.wall_force_numerical(r.W, grid.A_face, grid.x, nz.x_throat))
            orders.append(r.orders)
            iters.append(r.iterations)
            conv.append(r.converged)
        out[label] = {"J": J, "orders": orders, "iterations": iters, "converged": conv,
                      "roughness_J": metrics.roughness(np.array(J), np.array(J_ex))}
    return out


def promo_medians(registry: Path) -> dict[str, dict[str, float]]:
    """Latest promo family medians per zoo limiter from the registry."""
    conn = sqlite3.connect(registry)
    conn.row_factory = sqlite3.Row
    out: dict[str, dict[str, float]] = {}
    for name in LIMITERS:
        # by file, not id: the registry deduplicates by code hash, so a zoo file first seen via `sforge eval`
        # keeps its c-... id
        cand = conn.execute("SELECT id FROM candidates WHERE path = ?",
                            (f"src/schemeforge/arenas/euler1d/zoo/limiter/{name}.py",)).fetchone()
        if cand is None:
            continue
        run = conn.execute("SELECT id FROM runs WHERE candidate_id = ? AND suite = 'promo' AND status != 'running' "
                           "ORDER BY started_at DESC LIMIT 1", (cand["id"],)).fetchone()
        if run is None:
            continue
        rows = conn.execute("SELECT family, metric, value FROM scores WHERE run_id = ?", (run["id"],)).fetchall()
        out[name] = {f"{r['family']}.{r['metric']}": r["value"] for r in rows}
    return out


def plot(sweeps: list[dict], promo: dict[str, dict[str, float]]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for s in sweeps:
        name = s["limiter"]
        p = promo.get(name, {})
        width = p.get("RF1.shock_width:median", np.nan)
        axes[0].scatter(width, p.get("NF1.res_orders_expl:median", np.nan), s=40)
        axes[0].annotate(name, (width, p.get("NF1.res_orders_expl:median", np.nan)), fontsize=8,
                         xytext=(4, 3), textcoords="offset points")
        rough = s["explicit"]["roughness_J"]
        axes[1].scatter(width, rough, s=40)
        axes[1].annotate(name, (width, rough), fontsize=8, xytext=(4, 3), textcoords="offset points")
    axes[0].set(xlabel="RF1 shock width, median [cells] (sharper ->left)",
                ylabel="NF1 explicit residual drop, median [orders]", title="Sharpness vs steady convergence")
    axes[1].set(xlabel="RF1 shock width, median [cells]", ylabel="roughness_J, 41-point sweep (explicit)",
                yscale="log", title="Sharpness vs objective smoothness")
    for ax in axes:
        ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "front.png", dpi=130)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    if "--plot-only" in sys.argv:  # reuse the sweep, refresh the promo medians and the plot
        sweeps = json.loads((OUT / "sweep41.json").read_text())
    else:
        k = max(1, len(os.sched_getaffinity(0)) // 2 - 1)
        with ProcessPoolExecutor(max_workers=min(k, len(LIMITERS))) as pool:
            sweeps = list(pool.map(sweep, [(n, 1 + i) for i, n in enumerate(LIMITERS)]))
        (OUT / "sweep41.json").write_text(json.dumps(sweeps, indent=1))
    promo = promo_medians(Path("runs/registry.sqlite"))
    (OUT / "promo_medians.json").write_text(json.dumps(promo, indent=1))
    plot(sweeps, promo)
    for s in sweeps:
        e, i = s["explicit"], s["implicit"]
        print(f"{s['limiter']:16s} explicit: conv {np.mean(e['converged']):.2f} median orders "
              f"{np.median(e['orders']):5.1f} rough {e['roughness_J']:.3g} | implicit: conv "
              f"{np.mean(i['converged']):.2f} median iters {np.median(i['iterations']):5.0f} "
              f"rough {i['roughness_J']:.3g}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
