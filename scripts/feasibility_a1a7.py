"""PLAN §11.5 step 3c: can a limiter phi(r) meet Target A's A1 (sharp shocks) and A7 (low overshoot) together?

Sweeps phi = max(0, smin_k(s0 r, 1 + (c - 1) tanh(r - 1))) over s0 (compressive slope at r = 0) and c (cap height)
on the dev suite, under hunch H-0011 (ledger/drafts/r3_feasibility_a1a7.yaml; register it first). Round 1's
c-44f8015f87 is the family member s0 = 2, c = 1.5, between grid points. Run inside WSL, with nothing else evaluating:

    uv run python scripts/feasibility_a1a7.py write                # candidate files, no evaluation
    uv run python scripts/feasibility_a1a7.py run --hunch H-0011   # dev evaluations, one at a time (~30 x 30 s)
    uv run python scripts/feasibility_a1a7.py report               # table, plot, promo commands for the top 3

Dev values are proxies only: A1 and A7 are judged on promo (docs/targets/A.md). Results go to
runs/feasibility-a1a7/ (results.json, front.png); candidate files to candidates/feasibility-a1a7/.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CAND_DIR = REPO / "candidates" / "feasibility-a1a7"
OUT_DIR = REPO / "runs" / "feasibility-a1a7"
S0 = (1.0, 1.25, 1.5, 1.75, 2.0)
CAPS = (1.0, 1.2, 1.4, 1.6, 1.8, 2.0)
K = 10.0
A1_SHOCK = 2.6  # cells, Target A
A7_FACTOR = 1.1  # x van Leer's overshoot
COLUMNS = [("R1.shock_width", 8, 2), ("R1.contact_width", 7, 2), ("R1.overshoot", 8, 4), ("R6.overshoot", 8, 4),
           ("N1.converged_expl", 7, 0), ("N1.converged_impl", 7, 0)]  # report table: metric, width, decimals
METRICS = [("R1", "shock_width"), ("R1", "contact_width"), ("R1", "overshoot"), ("R6", "overshoot"),
           ("N1", "converged_expl"), ("N1", "converged_impl"), ("N4", "roughness_J")]

TEMPLATE = '''"""H-0011 sweep: phi = max(0, smin_k(s0 r, 1 + (c - 1) tanh(r - 1))), s0 = {s0}, c = {c}, k = {k}."""
import jax.numpy as jnp

S0 = {s0}
CAP = {c}
K = {k}


def phi(r):
    a = S0 * r
    b = 1.0 + (CAP - 1.0) * jnp.tanh(r - 1.0)
    return jnp.maximum(0.0, -jnp.logaddexp(-K * a, -K * b) / K)
'''


def name(s0: float, c: float) -> str:
    return f"s0_{s0:.2f}_c_{c:.1f}".replace(".", "p")


def write(_: argparse.Namespace) -> int:
    from schemeforge.core.sandbox import validate_source

    CAND_DIR.mkdir(parents=True, exist_ok=True)
    for s0 in S0:
        for c in CAPS:
            src = TEMPLATE.format(s0=s0, c=c, k=K)
            res = validate_source(src)
            if not res.ok:
                print(f"{name(s0, c)} fails the sandbox: {res.rules}", file=sys.stderr)
                return 1
            (CAND_DIR / f"{name(s0, c)}.py").write_text(src, encoding="utf-8")
    print(f"{len(S0) * len(CAPS)} files in {CAND_DIR.relative_to(REPO)}")
    return 0


def _load() -> dict:
    p = OUT_DIR / "results.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def run(args: argparse.Namespace) -> int:
    from schemeforge.core import evaluation, integrity, ledger

    if args.hunch:
        h = ledger.get(args.hunch)
        if (h["arena"], h["slot"]) != ("euler1d", "limiter"):
            print(f"{args.hunch} is not a euler1d/limiter hunch", file=sys.stderr)
            return 2
    elif args.suite == "dev":
        print("--hunch is required for dev runs (iron rule 5: register the hunch first)", file=sys.stderr)
        return 2
    problems = integrity.integrity_problems("euler1d")
    if problems:
        print("refusing to score: " + "; ".join(problems), file=sys.stderr)
        return 2
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = _load()
    files = sorted(CAND_DIR.glob("s0_*.py"))[: args.limit or None]
    if not files:
        print("no candidate files: run `write` first", file=sys.stderr)
        return 2
    kw = {"registry_path": Path(args.registry)} if args.registry else {}
    for f in files:
        if f.stem in results and results[f.stem]["suite"] == args.suite:
            continue
        if args.hunch:
            evaluation.submit_candidate(f, args.hunch, origin="eval", **kw)
        res = evaluation.evaluate_file(f, "euler1d", "limiter", args.suite, **kw)
        cases = res.report.get("cases", {})
        results[f.stem] = {"suite": args.suite, "run_id": res.run_id, "candidate_id": res.candidate_id,
                           "status": res.report["status"], "violations": res.report.get("violations", [])[:3],
                           "metrics": {f"{c}.{m}": cases.get(c, {}).get(m) for c, m in METRICS}}
        print(f"{f.stem:16s} {res.run_id}  {res.candidate_id}  {res.report['status']}", flush=True)
        (OUT_DIR / "results.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
    return 0


def zoo_dev(registry_path: Path) -> dict[str, dict[str, float]]:
    """Latest dev values of every zoo limiter under the current judge version: name -> {"R1.shock_width": …}."""
    from schemeforge.core.integrity import judge_version

    conn = sqlite3.connect(registry_path)
    conn.row_factory = sqlite3.Row
    out: dict[str, dict[str, float]] = {}
    for c in conn.execute("SELECT id, path FROM candidates WHERE slot = 'limiter' AND path LIKE "
                          "'src/schemeforge/arenas/euler1d/zoo/limiter/%'"):
        run = conn.execute("SELECT id FROM runs WHERE candidate_id = ? AND suite = 'dev' AND status = 'ok' AND "
                           "judge_version = ? ORDER BY started_at DESC LIMIT 1",
                           (c["id"], judge_version("euler1d"))).fetchone()
        if run:
            out[c["path"].rsplit("/", 1)[-1][:-3]] = {
                f"{r['case_id']}.{r['metric']}": r["value"] for r in conn.execute(
                    "SELECT case_id, metric, value FROM scores WHERE run_id = ?", (run["id"],))}
    return out


def _fmt(v: float | None, width: int, prec: int) -> str:
    return f"{'-':>{width}s}" if v is None else f"{v:{width}.{prec}f}"


def report(args: argparse.Namespace) -> int:
    need = ("R1.shock_width", "R1.overshoot", "R6.overshoot")
    results = {k: v for k, v in _load().items()
               if v["status"] == "ok" and all(v["metrics"].get(m) is not None for m in need)}
    zoo = zoo_dev(Path(args.registry or REPO / "runs" / "registry.sqlite"))
    vl = zoo.get("van_leer")
    if vl is None:
        print("no dev run of the zoo van Leer under this judge version: run `sforge zoo eval --suite dev` first",
              file=sys.stderr)
        return 2
    lim = {"R1.overshoot": A7_FACTOR * vl["R1.overshoot"], "R6.overshoot": A7_FACTOR * vl["R6.overshoot"]}

    def corner(m: dict) -> float:
        """<= 1 meets all three dev proxies; the largest ratio to its threshold otherwise."""
        return max(m["R1.shock_width"] / A1_SHOCK, m["R1.overshoot"] / lim["R1.overshoot"],
                   m["R6.overshoot"] / lim["R6.overshoot"])

    rows = sorted(((corner(v["metrics"]), k, v) for k, v in results.items()), key=lambda t: t[0])
    print(f"thresholds on dev: R1 shock <= {A1_SHOCK}, R1 overshoot <= {lim['R1.overshoot']:.4g}, "
          f"R6 overshoot <= {lim['R6.overshoot']:.4g} (1.1 x van Leer)")
    print(f"{'point':16s} {'corner':>6s} {'R1 shock':>8s} {'R1 cont':>7s} {'R1 ovs':>8s} {'R6 ovs':>8s} "
          f"{'N1 expl':>7s} {'N1 impl':>7s}  run")
    for d, k, v in rows:
        m = v["metrics"]
        cells = [_fmt(m.get(key), w, prec) for key, w, prec in COLUMNS]
        print(f"{k:16s} {d:6.2f} " + " ".join(cells) + f"  {v['run_id']}")
    print("\npromo for the three points closest to the corner (H-0011 kill criterion):")
    for _, k, v in rows[:3]:
        print(f"  uv run sforge eval {v['candidate_id']} --arena euler1d --slot limiter --suite promo   # {k}")
        print(f"  uv run sforge promote {v['candidate_id']} --target A")

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharex=True)
    for ax, case in zip(axes, ("R1", "R6"), strict=True):
        key = f"{case}.overshoot"
        xs = [v["metrics"]["R1.shock_width"] for v in results.values()]
        ys = [v["metrics"][key] for v in results.values()]
        cs = [float(k.split("_")[1].replace("p", ".")) for k in results]
        sc = ax.scatter(xs, ys, c=cs, cmap="viridis", s=28, label="family (colour: s0)")
        for zname, zm in zoo.items():
            if "R1.shock_width" in zm and key in zm:
                ax.scatter(zm["R1.shock_width"], zm[key], marker="s", color="0.4", s=30)
                ax.annotate(zname, (zm["R1.shock_width"], zm[key]), fontsize=8, xytext=(4, 2),
                            textcoords="offset points", color="0.3")
        ax.axvline(A1_SHOCK, color="tab:green", lw=1)
        ax.axhline(lim[key], color="tab:green", lw=1)
        ax.set_xlabel("R1 shock width [cells] (dev)")
        ax.set_ylabel(f"{case} overshoot (dev)")
        ax.set_title(f"{case}: Target A corner is bottom left of the green lines", fontsize=10)
    fig.colorbar(sc, ax=axes, label="s0 (slope at r = 0)")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / "front.png", dpi=130, bbox_inches="tight")
    print(f"\nplot: {OUT_DIR / 'front.png'}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("write", help="write the candidate files")
    r = sub.add_parser("run", help="evaluate the candidates one at a time")
    r.add_argument("--hunch", help="registered hunch id (H-0011); required for dev")
    r.add_argument("--suite", default="dev", choices=["smoke", "dev"])
    r.add_argument("--limit", type=int, default=0, help="evaluate only the first N files (testing)")
    r.add_argument("--registry", help="registry path (testing; default runs/registry.sqlite)")
    rep = sub.add_parser("report", help="table, plot and promo commands")
    rep.add_argument("--registry", help="registry path (default runs/registry.sqlite)")
    args = p.parse_args()
    return {"write": write, "run": run, "report": report}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
