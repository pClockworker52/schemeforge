"""`sforge dossier build ID`: the evidence folder for a promoted candidate (PLAN Appendix F).

Everything numeric comes from the registry and the run reports; candidate code never runs here (the phi(r) plot
uses the probe values the sandboxed worker recorded). The analyst fills Mechanism, Properties, Failure cases and
Literature; the referee adds the verdict.
"""

from __future__ import annotations

import ast
import json
import math
from pathlib import Path

from . import leaderboard, registry
from .integrity import REPO_ROOT, judge_version, tree_hash

DOSSIERS = REPO_ROOT / "dossiers"


def _docstring(source: str) -> str:
    try:
        doc = ast.get_docstring(ast.parse(source)) or ""
    except SyntaxError:
        doc = ""
    return " ".join(doc.split())[:120] or "(no description)"


def _lineage(conn, cid: str, depth: int = 6) -> str:
    chain, cur = [], cid
    for _ in range(depth):
        row = conn.execute("SELECT parents FROM candidates WHERE id = ?", (cur,)).fetchone()
        parents = json.loads(row["parents"]) if row else []
        if not parents:
            break
        chain.append(" + ".join(parents))
        cur = parents[0]
    return " ← ".join([cid, *chain]) if chain else f"{cid} (no recorded parents)"


def _latest_run(conn, cid: str, suite: str, version: str):
    return conn.execute("SELECT * FROM runs WHERE candidate_id = ? AND suite = ? AND status = 'ok' AND "
                        "judge_version = ? ORDER BY started_at DESC LIMIT 1", (cid, suite, version)).fetchone()


def build(cid: str, target: str = "A") -> Path:
    conn = registry.connect()
    cand = conn.execute("SELECT * FROM candidates WHERE id = ?", (cid,)).fetchone()
    if cand is None:
        raise KeyError(f"unknown candidate {cid}")
    arena, slot = cand["arena"], cand["slot"]
    version = judge_version(arena)
    path = Path(cand["path"]) if Path(cand["path"]).is_absolute() else REPO_ROOT / cand["path"]
    source = path.read_text(encoding="utf-8")
    out = DOSSIERS / cid
    (out / "analysis").mkdir(parents=True, exist_ok=True)
    (out / "candidate.py").write_text(source, encoding="utf-8")

    dev = _latest_run(conn, cid, "dev", version)
    promo = _latest_run(conn, cid, "promo", version)
    lines = [f"# {cid} — {_docstring(source)}",
             "Label: rediscovery | variant of <X> | plausibly new (analyst proposes, referee decides) · "
             "Referee: (pending)",
             f"Arena/slot: {arena}/{slot} · Hunch: {cand['hunch_id'] or '-'} · Lineage: {_lineage(conn, cid)} · "
             f"Judge: {version} ({tree_hash()[:12]})", ""]

    lines += [f"## Result vs zoo (held-out, Target {target})", ""]
    if promo is None:
        lines += [f"No promo run under {version} yet: `uv run sforge eval {cid} --arena {arena} --slot {slot} "
                  "--suite promo`, then rebuild.", ""]
    else:
        from .evaluation import zoo_candidate_id
        from .promotion import TARGETS, check_target

        spec = TARGETS[target]
        members = {m for _, _, _, m in spec["bootstrap"]} | {m for *_, m in spec["relative"]}
        zoo_runs = {}
        for m in members:
            zid = zoo_candidate_id(conn, arena, spec["reference_slot"], m)
            run = _latest_run(conn, zid, "promo", version) if zid else None
            if run is not None:
                zoo_runs[m] = run["id"]
        dev_vals = {f"{r['case_id']}.{r['metric']}": r["value"] for r in conn.execute(
            "SELECT case_id, metric, value FROM scores WHERE run_id = ?", (dev["id"],))} if dev else {}
        if len(zoo_runs) == len(members):
            lines += ["| Check | Criterion | Value | Met |", "|---|---|---|---|"]
            for c in check_target(target, promo["id"], zoo_runs, dev_vals):
                lines.append(f"| {c.id} | {c.description} | {c.detail} | {'yes' if c.ok else 'no'} |")
            lines += ["", f"Promo run {promo['id']}; zoo references {zoo_runs}.", ""]
        else:
            lines += ["Zoo references lack promo runs under this judge: `uv run sforge zoo eval --suite promo`.", ""]

    lines += ["## Dev suite vs zoo", ""]
    rows = {r.candidate_id: r for r in leaderboard.build(conn, arena, slot, version)}
    if cid in rows:
        r = rows[cid]
        lines += [f"Run {r.run_id}, Pareto rank {r.rank}, geometric-mean ratio to the best zoo member "
                  f"{r.score:.3f}.", "", "| Metric | Candidate | Ratio to best zoo |", "|---|---|---|"]
        for case, metric, _ in leaderboard.objectives(arena, slot):
            k = f"{case}.{metric}"
            v, q = r.values.get(k), r.vs_zoo.get(k)
            lines.append(f"| {k} | {'-' if v is None else f'{v:.4g}'} | {'-' if q is None else f'{q:.3f}'} |")
    else:
        lines.append("No ok dev run under this judge.")
    lines.append("")

    if slot == "limiter" and dev is not None and dev["report_path"]:
        plot = _phi_plot(Path(dev["report_path"]), out / "phi.png")
        if plot:
            lines += ["![phi(r)](phi.png)", ""]

    lines += ["## Mechanism", "(analyst) Plain words; every claim backed by a run id or a script in analysis/.", "",
              "## Properties", "(analyst) Proved / numerically checked / conjectured — one list each.", "",
              "## Failure cases and limits", "(analyst, breakers) Including cases that break the zoo too.", "",
              "## Closest literature", "(analyst) Up to 5 entries with links and the precise difference.", "",
              "## Reproduce", "```bash",
              f"uv run sforge eval {cand['path']} --arena {arena} --slot {slot} --suite dev",
              f"uv run sforge eval {cid} --arena {arena} --slot {slot} --suite promo",
              f"uv run sforge promote {cid} --target {target} --arena {arena}",
              f"uv run sforge dossier build {cid}", "```", "",
              "## Code", "```python", source.rstrip(), "```", ""]
    (out / "README.md").write_text("\n".join(lines), encoding="utf-8")
    conn.close()
    return out / "README.md"


def _phi_plot(report_path: Path, dest: Path) -> bool:
    """phi(r) of the candidate (probe values from its dev report) against the zoo limiters."""
    rp = report_path if report_path.is_absolute() else Path.cwd() / report_path
    if not rp.exists():
        return False
    fp = json.loads(rp.read_text(encoding="utf-8")).get("probe", {}).get("fingerprint")
    if not fp:
        return False
    import jax.numpy as jnp
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    from schemeforge.arenas.euler1d import zoo
    from schemeforge.engine.probes import LIMITER_FINGERPRINT_R

    r = LIMITER_FINGERPRINT_R
    fig, ax = plt.subplots(figsize=(6, 4))
    rr = np.linspace(-1.0, 6.0, 400)
    ax.fill_between(rr, 0, np.where(rr > 0, np.minimum(2 * rr, 2), 0), color="0.9", label="Sweby TVD region")
    for name in ("minmod", "van_albada", "van_leer", "superbee"):
        ax.plot(rr, np.asarray(zoo.load("limiter", name)(jnp.asarray(rr))), lw=1, alpha=0.7, label=name)
    ax.plot(r, fp, "k.-", lw=2, label="candidate")
    ax.set(xlim=(-1, 6), ylim=(-0.2, 2.2), xlabel="r", ylabel="phi(r)")
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(dest, dpi=120)
    plt.close(fig)
    return not math.isnan(float(fp[0]))
