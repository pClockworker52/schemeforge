"""The `sforge` command line (PLAN §5.5).

Phase 0: every command exists with its options and `--help`, and exits with "not implemented".
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Annotated, NoReturn

import typer

app = typer.Typer(
    help="schemeforge: propose, judge and archive numerical scheme components.",
    no_args_is_help=True,
    add_completion=False,
)
zoo_app = typer.Typer(help="Evaluate the zoo of known methods.", no_args_is_help=True)
hunch_app = typer.Typer(help="Manage the hunch ledger (ledger/hunches.yaml).", no_args_is_help=True)
case_app = typer.Typer(help="Breaker cases: propose into quarantine, accept into the judge.", no_args_is_help=True)
dossier_app = typer.Typer(help="Evidence folders for promoted candidates.", no_args_is_help=True)
judge_app = typer.Typer(help="Judge self-checks, version and exact solutions.", no_args_is_help=True)
app.add_typer(zoo_app, name="zoo")
app.add_typer(hunch_app, name="hunch")
app.add_typer(case_app, name="case")
app.add_typer(dossier_app, name="dossier")
app.add_typer(judge_app, name="judge")

NOT_IMPLEMENTED_EXIT = 3


class Suite(StrEnum):
    smoke = "smoke"
    dev = "dev"
    promo = "promo"


class ZooSuite(StrEnum):
    dev = "dev"
    promo = "promo"


class Verdict(StrEnum):
    supported = "supported"
    refuted = "refuted"
    inconclusive = "inconclusive"
    merged = "merged"


def _not_implemented(command: str) -> NoReturn:
    typer.echo(f"sforge {command}: not implemented", err=True)
    raise typer.Exit(code=NOT_IMPLEMENTED_EXIT)


Arena = Annotated[str, typer.Option("--arena", help="Arena, e.g. euler1d or contact.")]
Slot = Annotated[str, typer.Option("--slot", help="Slot, e.g. limiter or flux.")]
JsonOut = Annotated[bool, typer.Option("--json", help="Machine-readable output.")]


@app.command("eval")
def eval_cmd(
    target: Annotated[str, typer.Argument(help="Candidate file or registered candidate id.")],
    arena: Arena,
    slot: Slot,
    suite: Annotated[Suite, typer.Option("--suite", help="smoke, dev or promo (promo: family aggregates only).")],
    case: Annotated[Path | None, typer.Option("--case", help="Add one extra case from a YAML file.")] = None,
    json_out: JsonOut = False,
) -> None:
    """Sandboxed evaluation; stores scores and prints the report and run id."""
    import json

    from schemeforge.core import evaluation, registry

    _check_integrity(arena)
    if suite == Suite.promo and case:
        _fail("--case cannot be combined with the promo suite", 2)
    path = Path(target)
    if not path.is_file():
        try:
            path, arena_reg, slot_reg = evaluation.candidate_path(registry.connect(), target)
        except KeyError:
            _fail(f"{target} is neither a file nor a registered candidate id", 2)
        if (arena_reg, slot_reg) != (arena, slot):
            _fail(f"{target} is registered for {arena_reg}/{slot_reg}, not {arena}/{slot}", 2)
    extra = [_load_case(arena, case)] if case else []
    res = evaluation.evaluate_file(path, arena, slot, suite.value, extra)
    if json_out:
        typer.echo(json.dumps(res.report, indent=1, default=float))
    else:
        _print_report(res.report)
    raise typer.Exit(code=0 if res.report["status"] == "ok" else 1)


def _fail(message: str, code: int) -> NoReturn:
    typer.echo(f"sforge: {message}", err=True)
    raise typer.Exit(code=code)


def _check_integrity(arena: str) -> None:
    from schemeforge.core.integrity import integrity_problems

    problems = integrity_problems(arena)
    if problems:
        _fail("refusing to score: " + "; ".join(problems), 4)


def _load_case(arena: str, path: Path) -> dict:
    import importlib

    import yaml

    cases = importlib.import_module(f"schemeforge.arenas.{arena}.cases")
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    try:
        cases.validate_case(cases.case_from_dict(d))
    except (ValueError, TypeError, KeyError) as exc:
        _fail(f"inadmissible case {path}: {exc}", 2)
    return d


def _fmt(v: float) -> str:
    return f"{v:.3g}" if abs(v) >= 1e-3 or v == 0 else f"{v:.2e}"


def _print_report(r: dict) -> None:
    typer.echo(f"run {r['run_id']}  candidate {r['candidate_id']}  judge {r['judge_version']} "
               f"({r['judge_hash'][:12]})  status {r['status'].upper()}  {r.get('seconds', 0.0):.1f} s")
    for case_id, ms in r.get("cases", {}).items():
        body = "  ".join(f"{k}={_fmt(v)}" for k, v in ms.items() if k != "seconds")
        typer.echo(f"  {case_id:9s} {ms.get('seconds', 0.0):6.2f} s  {body}")
    for fam, agg in r.get("families", {}).items():
        typer.echo(f"  {fam} (n={agg['n']}, pass rate {agg['pass_rate']:.2f})")
        for k, v in agg.items():
            if isinstance(v, dict):
                typer.echo(f"      {k:18s} median={_fmt(v['median'])}  p90={_fmt(v['p90'])}  worst={_fmt(v['worst'])}")
    if "max_cfl" in r:
        typer.echo(f"  max_cfl: {r['max_cfl']}")
    if r.get("metamorphic"):
        typer.echo("  measured: " + "  ".join(f"{k}={_fmt(v)}" for k, v in r["metamorphic"].items()))
    if "cost" in r:
        typer.echo(f"  cost: {r['cost']:.1f} ns per cell update (R1)")
    for v in r.get("violations", []):
        typer.echo(f"  VIOLATION: {v}")


@app.command()
def submit(
    file: Annotated[Path, typer.Argument(help="Candidate file.")],
    hunch: Annotated[str, typer.Option("--hunch", help="Hunch id, e.g. H-0007.")],
    parent: Annotated[list[str] | None, typer.Option("--parent", help="Parent candidate id (repeatable).")] = None,
) -> None:
    """Register a candidate with its lineage and code hash."""
    _not_implemented("submit")


@app.command()
def leaderboard(
    arena: Arena,
    slot: Slot,
    pareto: Annotated[bool, typer.Option("--pareto", help="Show the Pareto set.")] = False,
    vs_zoo: Annotated[bool, typer.Option("--vs-zoo", help="Show ratios against the best zoo member.")] = False,
    top: Annotated[int | None, typer.Option("--top", help="Show only the top K.")] = None,
    json_out: JsonOut = False,
) -> None:
    """Show rankings and the Pareto set."""
    _not_implemented("leaderboard")


@zoo_app.command("eval")
def zoo_eval(
    arena: Arena,
    suite: Annotated[ZooSuite, typer.Option("--suite", help="dev or promo.")] = ZooSuite.dev,
) -> None:
    """Evaluate every zoo member (in parallel, one locked core each)."""
    import importlib
    from concurrent.futures import ThreadPoolExecutor

    from schemeforge.core import evaluation
    from schemeforge.core.locks import max_parallel

    _check_integrity(arena)
    zoo = importlib.import_module(f"schemeforge.arenas.{arena}.zoo")
    ev = importlib.import_module(f"schemeforge.arenas.{arena}.evaluate")
    jobs = [(slot, name, path) for slot in ev.SLOTS for name, path in zoo.members(slot).items()]

    def one(job):
        slot, name, path = job
        return slot, name, evaluation.evaluate_file(path, arena, slot, suite.value, origin="zoo",
                                                    candidate_id=f"zoo-{slot}-{name}")

    with ThreadPoolExecutor(max_workers=max_parallel()) as pool:
        results = list(pool.map(one, jobs))
    if suite == ZooSuite.promo:  # family medians
        key = [("RF1", "l1_smooth"), ("RF1", "shock_width"), ("RF2", "tv_increase"), ("NF1", "shock_pos_err"),
               ("NF1", "res_orders_expl"), ("NF1", "newton_iters"), ("NF3", "roughness_J")]

        def value(r, c, m):
            v = r.get("families", {}).get(c, {}).get(m)
            return v["median"] if isinstance(v, dict) else None
    else:
        key = [("R1", "shock_width"), ("R1", "contact_width"), ("S1", "order_smooth"), ("R7", "l1_ref"),
               ("N1", "res_orders_expl"), ("N1", "newton_iters"), ("N4", "roughness_J")]

        def value(r, c, m):
            return r.get("cases", {}).get(c, {}).get(m)

    typer.echo(f"{'slot':15s}{'member':17s}{'status':9s}{'s':>6s}  " + "  ".join(f"{c}.{m}" for c, m in key))
    for slot, name, res in results:
        r = res.report
        cells = "  ".join(
            f"{_fmt(value(r, c, m)) if value(r, c, m) is not None else '-':>{len(c) + len(m) + 1}s}" for c, m in key
        )
        typer.echo(f"{slot:15s}{name:17s}{r['status']:9s}{r.get('seconds', 0.0):6.1f}  {cells}")
        for v in r.get("violations", [])[:2]:
            typer.echo(f"{'':32s}VIOLATION: {v}")
    typer.echo(f"{len(results)} members; reports in {evaluation.REPORTS_DIR}/")


@hunch_app.command("add")
def hunch_add(yaml_file: Annotated[Path, typer.Argument(help="Hunch draft YAML.")]) -> None:
    """Validate a hunch draft against ledger/schema.yaml and register it."""
    _not_implemented("hunch add")


@hunch_app.command("list")
def hunch_list(open_only: Annotated[bool, typer.Option("--open", help="Only open hunches.")] = False) -> None:
    """List hunches."""
    _not_implemented("hunch list")


@hunch_app.command("show")
def hunch_show(hunch_id: Annotated[str, typer.Argument(help="Hunch id.")]) -> None:
    """Show one hunch."""
    _not_implemented("hunch show")


@hunch_app.command("close")
def hunch_close(
    hunch_id: Annotated[str, typer.Argument(help="Hunch id.")],
    verdict: Annotated[Verdict, typer.Option("--verdict", help="Ledger verdict.")],
    note: Annotated[str, typer.Option("--note", help="Verdict note with evidence (run ids).")],
) -> None:
    """Close a hunch with a verdict."""
    _not_implemented("hunch close")


@case_app.command("propose")
def case_propose(yaml_file: Annotated[Path, typer.Argument(help="Case YAML.")]) -> None:
    """Put a breaker case into cases/quarantine/."""
    _not_implemented("case propose")


@case_app.command("accept")
def case_accept(case_id: Annotated[str, typer.Argument(help="Quarantined case id.")]) -> None:
    """Move a case into the judge tree (interactive confirmation; bumps the judge version)."""
    _not_implemented("case accept")


@app.command()
def evolve(
    arena: Arena,
    slot: Slot,
    hunch: Annotated[list[str], typer.Option("--hunch", help="Hunch id (repeatable, one island each).")],
    islands: Annotated[int, typer.Option("--islands", help="Number of islands.")] = 3,
    gens: Annotated[int, typer.Option("--gens", help="Generations.")] = 20,
    children: Annotated[int, typer.Option("--children", help="Children per generation and island.")] = 8,
    backend: Annotated[str, typer.Option("--backend", help="LLM backend: claude-cli or dummy.")] = "claude-cli",
    model: Annotated[str, typer.Option("--model", help="Model alias for the backend.")] = "sonnet",
    budget: Annotated[int | None, typer.Option("--budget", help="Maximum number of candidates.")] = None,
) -> None:
    """Run the inner evolutionary loop (resumable)."""
    _not_implemented("evolve")


@dossier_app.command("build")
def dossier_build(candidate_id: Annotated[str, typer.Argument(help="Promoted candidate id.")]) -> None:
    """Build a dossier skeleton with tables and plots."""
    _not_implemented("dossier build")


@judge_app.command("verify")
def judge_verify(
    arena: Annotated[str, typer.Option("--arena", help="Arena.")] = "euler1d",
) -> None:
    """Check exact solutions against Appendix H, the zoo sanity ranking and the metamorphic tests."""
    import importlib

    checks = importlib.import_module(f"schemeforge.arenas.{arena}.verify").verify()
    for c in checks:
        typer.echo(f"{'PASS' if c.ok else 'FAIL'}  {c.name}: {c.detail}")
    failed = [c for c in checks if not c.ok]
    typer.echo(f"{len(checks) - len(failed)} of {len(checks)} checks passed")
    raise typer.Exit(code=1 if failed else 0)


@judge_app.command("version")
def judge_version(
    arena: Annotated[str, typer.Option("--arena", help="Arena.")] = "euler1d",
) -> None:
    """Print the judge version, content hash and integrity state."""
    from schemeforge.core import integrity

    problems = integrity.integrity_problems(arena)
    typer.echo(f"{integrity.judge_version(arena)}  {integrity.tree_hash()}")
    typer.echo("integrity: ok" if not problems else "integrity: " + "; ".join(problems))


@judge_app.command("exact")
def judge_exact(
    arena: Arena,
    case: Annotated[Path, typer.Option("--case", help="Case YAML.")],
    json_out: JsonOut = False,
) -> None:
    """Print the exact or reference solution for one case (for the blind audit)."""
    import importlib
    import json

    import yaml

    cases = importlib.import_module(f"schemeforge.arenas.{arena}.cases")
    verify = importlib.import_module(f"schemeforge.arenas.{arena}.verify")
    data = yaml.safe_load(case.read_text(encoding="utf-8"))
    batch = isinstance(data, list)  # a YAML list of cases is answered with a JSON list, in one process
    try:
        reps = [verify.exact_report(cases.case_from_dict(d)) for d in (data if batch else [data])]
    except (ValueError, TypeError, KeyError) as exc:
        _fail(str(exc), 2)
    if json_out:
        typer.echo(json.dumps(reps if batch else reps[0]))
    else:
        for rep in reps:
            typer.echo("  ".join(f"{k}={v}" for k, v in rep.items() if not isinstance(v, list)))


@app.command()
def reveal(run: Annotated[str, typer.Argument(help="Run id.")]) -> None:
    """Show full held-out diagnostics. Refuses to run without an interactive terminal."""
    import json
    import sys

    from schemeforge.core.evaluation import HELDOUT_DIR

    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        _fail("reveal needs an interactive terminal (held-out details are for Peter only)", 5)
    path = HELDOUT_DIR / f"{run}.json"
    if not path.is_file():
        _fail(f"no held-out details for run {run}", 2)
    for inst_id, d in json.loads(path.read_text(encoding="utf-8")).items():
        state = "OK" if not d["violations"] else "VIOLATION: " + "; ".join(d["violations"])
        typer.echo(f"{inst_id} [{d['family']}] {state}")
        typer.echo(f"    case: {json.dumps(d['case'])}")
        typer.echo("    " + "  ".join(f"{k}={_fmt(v)}" for k, v in d["metrics"].items()))


if __name__ == "__main__":
    app()
