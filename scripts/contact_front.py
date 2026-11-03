"""Phase 6 step 5: the zoo front of Arena 2 over the medium stiffness scale gamma (PLAN §14.7).

For every zoo medium and gamma in GAMMAS: C0a gap closure (leak_pre, gap_res) and C2 Hertz on the dev mesh (a_err,
p0_err, leak_out, newton_iters, converged) plus max_step on C2. Classical frictionless contact (no medium) is the
reference point. Judge functions only; nothing is registered, so these are measurements for the baseline note, not
run ids (the zoo's registered dev and promo runs are in STATUS).

    uv run python scripts/contact_front.py [out.json]      (default docs/judge/baseline/contact_front.json)
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import replace
from pathlib import Path

from schemeforge.arenas.contact import evaluate as ev
from schemeforge.arenas.contact import solve, zoo
from schemeforge.arenas.contact.cases import GapClosureCase, HertzCase

GAMMAS = (1e-3, 1e-4, 1e-5, 1e-6, 1e-7)
OUT = Path(next((a for a in sys.argv[1:] if not a.startswith("--")), "docs/judge/baseline/contact_front.json"))


def classical_max_step(case: HertzCase) -> float:
    for n in ev.MAX_STEP_TRIALS:
        try:
            solve.hertz_classical(replace(case, steps=n))
            return 1.0 / n
        except Exception:  # noqa: BLE001 - felupe's NewtonConvergenceError
            continue
    return 0.0


def main() -> None:
    rows = []
    for name in zoo.members("medium"):
        psi = zoo.load("medium", name)
        for g in GAMMAS:
            t0 = time.perf_counter()
            gap, _ = ev.run_case(GapClosureCase("front-C0a", gamma=g), psi)
            hz, _ = ev.run_case(HertzCase("front-C2", gamma=g), psi)
            ms = ev.max_step(psi, HertzCase("front-C2", gamma=g)) if hz.get("converged") == 1.0 else 0.0
            rows.append({"medium": name, "gamma": g, "c0a": gap, "c2": hz, "max_step": ms,
                         "seconds": time.perf_counter() - t0})
            print(f"{name:14s} gamma {g:.0e}: C0a leak {gap.get('leak_pre', float('nan')):.2e} gap "
                  f"{gap.get('gap_res', float('nan')):.2e} | C2 conv {hz.get('converged')} a_err "
                  f"{hz.get('a_err', float('nan')):+.3f} leak_out {hz.get('leak_out', float('nan')):.3f} iters "
                  f"{hz.get('newton_iters', float('nan'))} | max_step {ms:.3f}  ({rows[-1]['seconds']:.0f} s)",
                  flush=True)
    case = HertzCase("front-C2-classical")
    cl, _ = ev.hertz_metrics(case, solve.hertz_classical(case))
    rows.append({"medium": "classical", "gamma": None, "c0a": {"leak_pre": 0.0, "gap_res": 0.0}, "c2": cl,
                 "max_step": classical_max_step(case)})
    print(f"classical: a_err {cl['a_err']:+.4f} p0_err {cl['p0_err']:+.4f} iters {cl['newton_iters']} "
          f"max_step {rows[-1]['max_step']:.3f}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, indent=1, default=float), encoding="utf-8")




def plot(rows: list[dict], out: Path) -> None:
    """Two panels over gamma per medium: accuracy (Hertz |a_err|, C0a gap_res) against robustness (max_step)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    for name in sorted({r["medium"] for r in rows if r["gamma"] is not None}):
        rs = [r for r in rows if r["medium"] == name and r["c2"].get("converged") == 1.0]
        for ax, metric in ((axes[0], lambda r: abs(r["c2"]["a_err"])), (axes[1], lambda r: r["c0a"]["gap_res"])):
            xs, ys = [metric(r) for r in rs], [r["max_step"] for r in rs]
            ax.plot(xs, ys, "o-", label=name)
            for r, x, y in zip(rs, xs, ys, strict=True):
                ax.annotate(f"{r['gamma']:.0e}", (x, y), textcoords="offset points", xytext=(4, 4), fontsize=7)
    cl = next(r for r in rows if r["medium"] == "classical")
    axes[0].plot([abs(cl["c2"]["a_err"])], [cl["max_step"]], "k*", ms=12, label="classical contact")
    for ax, xl in ((axes[0], "Hertz contact-width error |a_err| (lower: better contact)"),
                   (axes[1], "gap closure residual gap gap_res (lower: better contact)")):
        ax.set_xscale("log")
        ax.set_xlabel(xl)
        ax.set_ylabel("max_step: largest stable load step (higher: more robust)")
        ax.set_ylim(-0.05, 1.1)
        ax.grid(alpha=0.3)
    axes[0].legend(fontsize=8)
    fig.suptitle("Arena 2 zoo front over the medium stiffness gamma (labels); the neo-Hookean media fail at gamma = 1e-7",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    if "--plot" in sys.argv:  # re-plot from the saved JSON without rerunning the sweep
        plot(json.loads(OUT.read_text(encoding="utf-8")), Path("docs/judge/figures/contact_front.png"))
    else:
        main()
        plot(json.loads(OUT.read_text(encoding="utf-8")), Path("docs/judge/figures/contact_front.png"))
