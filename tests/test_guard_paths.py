"""Tests for the subagent path guard (.claude/hooks/guard_paths.py)."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "guard_paths.py"


def run_hook(args: list[str], tool: str, tool_input: dict) -> int:
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(ROOT)}
    payload = json.dumps({"tool_name": tool, "tool_input": tool_input, "cwd": str(ROOT)})
    proc = subprocess.run(
        [sys.executable, str(HOOK), *args], input=payload, text=True, capture_output=True, env=env, check=False
    )
    return proc.returncode


@pytest.mark.parametrize(
    "path,expected",
    [
        ("candidates/H-0001/a/cand_1.py", 0),
        (str(ROOT / "candidates" / "H-0001" / "a" / "notes.md"), 0),
        ("src/schemeforge/arenas/euler1d/metrics.py", 2),
        ("candidates/../src/schemeforge/cli.py", 2),
        ("../outside.txt", 2),
        ("candidatesX/evil.py", 2),
    ],
)
def test_proposer_writes(path: str, expected: int) -> None:
    assert run_hook(["candidates/"], "Write", {"file_path": path}) == expected


@pytest.mark.parametrize(
    "tool,tool_input,expected",
    [
        ("Read", {"file_path": "src/schemeforge/arenas/euler1d/exact_riemann.py"}, 2),
        ("Read", {"file_path": "docs/judge/euler1d_spec.md"}, 0),
        ("Grep", {"pattern": "gamma"}, 2),  # no path means the repo root, which contains the judge
        ("Grep", {"pattern": "gamma", "path": "src"}, 2),
        ("Grep", {"pattern": "gamma", "path": "docs"}, 0),
        ("Glob", {"pattern": "**/*.py", "path": "audit"}, 0),
    ],
)
def test_auditor_deny(tool: str, tool_input: dict, expected: int) -> None:
    assert run_hook(["--deny", "src/schemeforge/arenas/"], tool, tool_input) == expected
