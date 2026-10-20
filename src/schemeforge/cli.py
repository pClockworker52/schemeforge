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

    if suite == Suite.promo:
        _fail("the promo suite needs the held-out families, which are not built yet", 2)
    _check_integrity(arena)
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

    if suite == ZooSuite.promo:
        _fail("the promo suite needs the held-out families, which are not built yet", 2)
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
    key = [("R1", "shock_width"), ("R1", "contact_width"), ("S1", "order_smooth"), ("R7", "l1_ref"),
           ("N1", "res_orders_expl"), ("N1", "newton_iters"), ("N4", "roughness_J")]
    typer.echo(f"{'slot':15s}{'member':17s}{'status':9s}{'s':>6s}  " + "  ".join(f"{c}.{m}" for c, m in key))
    for slot, name, res in results:
        r = res.report
        cells = "  ".join(
            f"{_fmt(r['cases'][c][m]) if m in r['cases'].get(c, {}) else '-':>{len(c) + len(m) + 1}s}" for c, m in key
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
def judge_verify() -> None:
    """Check exact solutions against Appendix H, the zoo sanity ranking and the metamorphic tests."""
    _not_implemented("judge verify")


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
    _not_implemented("judge exact")


@app.command()
def reveal(run: Annotated[str, typer.Argument(help="Run id.")]) -> None:
    """Show full held-out diagnostics. Refuses to run without an interactive terminal."""
    _not_implemented("reveal")


if __name__ == "__main__":
    app()
