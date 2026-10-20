"""Phase 0 CLI skeleton: every command from PLAN §5.5 exists, has --help and reports "not implemented"."""

import pytest
from typer.testing import CliRunner

from schemeforge.cli import NOT_IMPLEMENTED_EXIT, app

runner = CliRunner()

COMMANDS = [
    ["eval"], ["submit"], ["leaderboard"], ["zoo", "eval"],
    ["hunch", "add"], ["hunch", "list"], ["hunch", "show"], ["hunch", "close"],
    ["case", "propose"], ["case", "accept"], ["evolve"], ["dossier", "build"],
    ["judge", "verify"], ["judge", "version"], ["judge", "exact"], ["reveal"],
]


def test_top_level_help_lists_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for name in ("eval", "submit", "leaderboard", "zoo", "hunch", "case", "evolve", "dossier", "judge", "reveal"):
        assert name in result.output


@pytest.mark.parametrize("cmd", COMMANDS, ids=[" ".join(c) for c in COMMANDS])
def test_command_help(cmd: list[str]) -> None:
    result = runner.invoke(app, [*cmd, "--help"])
    assert result.exit_code == 0, result.output


@pytest.mark.parametrize(
    "argv",
    [
        ["eval", "cand.py", "--arena", "euler1d", "--slot", "limiter", "--suite", "dev"],
        ["hunch", "list", "--open"],
        ["judge", "version"],
        ["evolve", "--arena", "euler1d", "--slot", "limiter", "--hunch", "H-0001", "--backend", "dummy"],
    ],
)
def test_commands_are_not_implemented_yet(argv: list[str]) -> None:
    result = runner.invoke(app, argv)
    assert result.exit_code == NOT_IMPLEMENTED_EXIT
