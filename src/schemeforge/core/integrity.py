"""Judge integrity (PLAN §5.6): content hash of the judge tree and the checks `sforge eval` runs before scoring.

Everything that affects a score lives under src/schemeforge/arenas/<arena>/ (code, dev and accepted cases, cached
references) plus the shared src/schemeforge/arenas/__init__.py. Each arena is its own judge: its hash, its version
tag and the refusal to score cover only those files, so work on one arena never blocks another (Phase 6 step 1).
"""

from __future__ import annotations

import hashlib
import importlib
import subprocess
from pathlib import Path

ARENAS_DIR = Path(__file__).resolve().parents[1] / "arenas"
REPO_ROOT = ARENAS_DIR.parents[2]
JUDGE_REL = "src/schemeforge/arenas"


def judge_paths(arena: str) -> list[str]:
    """Repo-relative paths that make up one arena's judge."""
    return [f"{JUDGE_REL}/__init__.py", f"{JUDGE_REL}/{arena}"]


def tree_hash(root: Path = ARENAS_DIR, arena: str | None = None) -> str:
    """sha256 over (relative path, content) of every file in the tree, ignoring Python caches. With an arena, only
    that arena's judge: root/__init__.py and root/<arena>/."""
    h = hashlib.sha256()
    files = root.rglob("*") if arena is None else [root / "__init__.py", *(root / arena).rglob("*")]
    for p in sorted(files):
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


def integrity_problems(arena: str, repo: Path = REPO_ROOT, judge_rel: str | None = None) -> list[str]:
    """Reasons to refuse scoring: uncommitted changes in this arena's judge, or a tagged version whose files differ
    from the tag. `judge_rel` replaces the arena's paths (tests)."""
    paths = [judge_rel] if judge_rel else judge_paths(arena)
    status = _git(["status", "--porcelain", "--untracked-files=all", "--", *paths], repo)
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
    if _git(["diff", "--quiet", version, "--", *paths], repo).returncode != 0:
        return [f"the judge tree differs from tag {version}; bump JUDGE_VERSION and tag the new judge"]
    return []
