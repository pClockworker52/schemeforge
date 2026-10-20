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
    _not_implemented("eval")


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
    """Evaluate every zoo member."""
    _not_implemented("zoo eval")


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
def judge_version() -> None:
    """Print the judge version and content hash."""
    _not_implemented("judge version")


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
