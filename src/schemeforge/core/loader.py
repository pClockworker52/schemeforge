"""Load a candidate file: static validation (sandbox.py), then execution in a fresh namespace.

The evaluator calls this inside its sandboxed subprocess; the zoo and tests use it directly.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Iterable
from pathlib import Path

from .sandbox import DEFAULT_ALLOWED_IMPORTS, DEFAULT_MAX_LINES, Violation, validate_source


class CandidateRejected(ValueError):
    def __init__(self, violations: Iterable[Violation | str]) -> None:
        self.violations = [str(v) for v in violations]
        super().__init__("; ".join(self.violations))


def code_hash(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def load_function(
    source_or_path: str | Path,
    function_name: str,
    *,
    allowed_imports: Iterable[str] = DEFAULT_ALLOWED_IMPORTS,
    max_lines: int = DEFAULT_MAX_LINES,
) -> Callable:
    """Validate and execute a candidate, returning its slot function. Raises CandidateRejected."""
    if isinstance(source_or_path, Path):
        source, filename = source_or_path.read_text(encoding="utf-8"), str(source_or_path)
    else:
        source, filename = source_or_path, "<candidate>"
    result = validate_source(source, allowed_imports=allowed_imports, max_lines=max_lines)
    if not result.ok:
        raise CandidateRejected(result.violations)
    namespace: dict = {"__name__": f"candidate_{code_hash(source)[:12]}"}
    exec(compile(source, filename, "exec"), namespace)  # noqa: S102 - the source passed the AST validator
    fn = namespace.get(function_name)
    if not callable(fn):
        raise CandidateRejected([f"the file does not define a function {function_name!r}"])
    return fn
