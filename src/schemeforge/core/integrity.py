"""Judge integrity (PLAN §5.6): content hash of the judge tree and the checks `sforge eval` runs before scoring.

Everything that affects a score lives under src/schemeforge/arenas/ (code, dev and accepted cases, cached
references), so one hash over that tree identifies the judge.
"""

from __future__ import annotations

import hashlib
import importlib
import subprocess
from pathlib import Path

ARENAS_DIR = Path(__file__).resolve().parents[1] / "arenas"
REPO_ROOT = ARENAS_DIR.parents[2]
JUDGE_REL = "src/schemeforge/arenas"


def tree_hash(root: Path = ARENAS_DIR) -> str:
    """sha256 over (relative path, content) of every file in the tree, ignoring Python caches."""
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts or p.suffix == ".pyc":
            continue
        h.update(p.relative_to(root).as_posix().encode())
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def judge_version(arena: str) -> str:
    return importlib.import_module(f"schemeforge.arenas.{arena}").JUDGE_VERSION


def _git(args: list[str], repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=False)


def integrity_problems(arena: str, repo: Path = REPO_ROOT, judge_rel: str = JUDGE_REL) -> list[str]:
    """Reasons to refuse scoring: uncommitted judge changes, or a tagged version whose tree differs from the tag."""
    status = _git(["status", "--porcelain", "--untracked-files=all", "--", judge_rel], repo)
    if status.returncode != 0:
        return [f"git status failed: {status.stderr.strip()}"]
    dirty = [line for line in status.stdout.splitlines() if "__pycache__" not in line]
    if dirty:
        return [f"uncommitted changes in the judge tree ({len(dirty)} files), e.g. {dirty[0].strip()}"]
    version = judge_version(arena)
    if version.endswith(".dev"):
        return []
    if _git(["rev-parse", "-q", "--verify", f"refs/tags/{version}"], repo).returncode != 0:
        return [f"judge version {version} has no git tag"]
    if _git(["diff", "--quiet", version, "--", judge_rel], repo).returncode != 0:
        return [f"the judge tree differs from tag {version}; bump JUDGE_VERSION and tag the new judge"]
    return []
