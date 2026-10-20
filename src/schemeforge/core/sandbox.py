"""Static (AST) validation of candidate source code (PLAN §5.6, first defense layer).

The threat model is accidental overfitting and reward hacking by models, not a determined attacker. This check
rejects code that could do I/O, keep hidden state, reach outside the whitelisted modules or introspect the
interpreter. Process isolation, purity checks and held-out families are the later layers; the "no Python loops
over cells" rule is enforced by the cost metric, not here.
"""

from __future__ import annotations

import ast
from collections.abc import Iterable
from dataclasses import dataclass

DEFAULT_ALLOWED_IMPORTS: frozenset[str] = frozenset({"jax.numpy", "jax.lax", "math"})
DEFAULT_MAX_LINES = 150

# Builtins that give I/O, code execution, reflection or non-deterministic values (id, hash of str).
FORBIDDEN_NAMES: frozenset[str] = frozenset({
    "open", "eval", "exec", "compile", "__import__", "input", "print", "breakpoint", "help", "exit", "quit",
    "globals", "locals", "vars", "dir", "getattr", "setattr", "delattr", "hasattr",
    "id", "hash", "memoryview", "object", "type", "super", "classmethod", "staticmethod", "property",
})

# Attributes of whitelisted modules that do file I/O or host callbacks, and string formatting, which can reach
# attributes through format fields ("{0.__class__}") without an Attribute node.
FORBIDDEN_ATTRS: frozenset[str] = frozenset({
    "load", "save", "savez", "savez_compressed", "loadtxt", "savetxt", "genfromtxt", "fromfile", "tofile",
    "fromregex", "memmap", "infeed", "outfeed", "format", "format_map",
})

# Plain functions allowed in module-level constant expressions, besides math.<name>.
_CONST_FUNCS = frozenset({"float", "int", "abs", "min", "max"})


@dataclass(frozen=True)
class Violation:
    line: int
    rule: str
    message: str

    def __str__(self) -> str:
        return f"line {self.line}: [{self.rule}] {self.message}"


@dataclass(frozen=True)
class ValidationResult:
    violations: tuple[Violation, ...]

    @property
    def ok(self) -> bool:
        return not self.violations

    @property
    def rules(self) -> set[str]:
        return {v.rule for v in self.violations}


def _is_dunder(name: str) -> bool:
    return len(name) > 4 and name.startswith("__") and name.endswith("__")


def _is_const_expr(node: ast.expr) -> bool:
    """Immutable numeric expression: numbers, tuples, arithmetic, names, math.<attr> and math.<f>(...)."""
    if isinstance(node, ast.Constant):
        return node.value is None or isinstance(node.value, (bool, int, float, complex))
    if isinstance(node, ast.Name):
        return True
    if isinstance(node, ast.Tuple):
        return all(_is_const_expr(e) for e in node.elts)
    if isinstance(node, ast.UnaryOp):
        return _is_const_expr(node.operand)
    if isinstance(node, ast.BinOp):
        return _is_const_expr(node.left) and _is_const_expr(node.right)
    if isinstance(node, ast.Attribute):
        return isinstance(node.value, ast.Name) and node.value.id == "math"
    if isinstance(node, ast.Call):
        f = node.func
        allowed_func = (isinstance(f, ast.Name) and f.id in _CONST_FUNCS) or (
            isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == "math"
        )
        return allowed_func and not node.keywords and all(_is_const_expr(a) for a in node.args)
    return False


class _Checker(ast.NodeVisitor):
    def __init__(self, allowed_imports: frozenset[str]) -> None:
        self.allowed = allowed_imports
        self.violations: list[Violation] = []

    def add(self, node: ast.AST, rule: str, message: str) -> None:
        self.violations.append(Violation(getattr(node, "lineno", 0), rule, message))

    # --- module level -------------------------------------------------------------------------------------
    def check_module(self, tree: ast.Module) -> None:
        for stmt in tree.body:
            if isinstance(stmt, (ast.Import, ast.ImportFrom, ast.FunctionDef)):
                continue
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and isinstance(
                stmt.value.value, str
            ):
                continue  # docstring
            if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
                targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
                if not all(self._is_name_target(t) for t in targets):
                    self.add(stmt, "module-statement", "module-level assignments may only bind plain names")
                value = stmt.value
                if value is None or not (isinstance(value, ast.Lambda) or _is_const_expr(value)):
                    self.add(stmt, "module-value", "module-level values must be numeric constants or lambdas")
                continue
            if isinstance(stmt, (ast.ClassDef, ast.AsyncFunctionDef)):
                continue  # reported by the visitor
            self.add(stmt, "module-statement", f"{type(stmt).__name__} is not allowed at module level")
        self.visit(tree)

    @staticmethod
    def _is_name_target(t: ast.expr) -> bool:
        if isinstance(t, ast.Name):
            return True
        return isinstance(t, ast.Tuple) and all(isinstance(e, ast.Name) for e in t.elts)

    # --- imports ------------------------------------------------------------------------------------------
    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if alias.name not in self.allowed:
                self.add(node, "import", f"import of {alias.name!r} is not allowed")
            elif "." in alias.name and alias.asname is None:
                root = alias.name.split(".")[0]
                self.add(node, "import", f"'import {alias.name}' binds {root!r}; use 'import {alias.name} as ...'")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level or node.module is None:
            self.add(node, "import", "relative imports are not allowed")
            return
        for alias in node.names:
            full = f"{node.module}.{alias.name}"
            if alias.name == "*":
                self.add(node, "import", "star imports are not allowed")
            elif node.module not in self.allowed and full not in self.allowed:
                self.add(node, "import", f"import of {full!r} is not allowed")
            elif alias.name in FORBIDDEN_ATTRS or alias.name in FORBIDDEN_NAMES or _is_dunder(alias.name):
                self.add(node, "forbidden-attr", f"{full!r} is not allowed")

    # --- names and attributes -----------------------------------------------------------------------------
    def visit_Name(self, node: ast.Name) -> None:
        if node.id in FORBIDDEN_NAMES:
            self.add(node, "forbidden-name", f"{node.id!r} is not allowed")
        elif _is_dunder(node.id):
            self.add(node, "dunder", f"dunder name {node.id!r} is not allowed")

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if _is_dunder(node.attr):
            self.add(node, "dunder", f"dunder attribute {node.attr!r} is not allowed")
        elif node.attr in FORBIDDEN_ATTRS:
            self.add(node, "forbidden-attr", f"attribute {node.attr!r} is not allowed")
        if isinstance(node.ctx, (ast.Store, ast.Del)):
            self.add(node, "attr-assign", "assigning or deleting attributes is not allowed (hidden state)")
        self.generic_visit(node)

    # --- state and structure ------------------------------------------------------------------------------
    def visit_Global(self, node: ast.Global) -> None:
        self.add(node, "global", "'global' is not allowed")

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        self.add(node, "global", "'nonlocal' is not allowed")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.add(node, "class", "class definitions are not allowed")
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.add(node, "async", "async functions are not allowed")
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for dec in node.decorator_list:
            self.add(dec, "decorator", "decorators are not allowed (they run code at import time)")
        self._check_defaults(node.args)
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self._check_defaults(node.args)
        self.generic_visit(node)

    def _check_defaults(self, args: ast.arguments) -> None:
        defaults: Iterable[ast.expr | None] = [*args.defaults, *args.kw_defaults]
        for d in defaults:
            if d is not None and not _is_const_expr(d):
                self.add(d, "default-arg", "default arguments must be numeric constants (hidden state)")


def validate_source(
    source: str,
    *,
    allowed_imports: Iterable[str] = DEFAULT_ALLOWED_IMPORTS,
    max_lines: int = DEFAULT_MAX_LINES,
) -> ValidationResult:
    """Statically check candidate source. Returns all violations found (empty means the code passes)."""
    violations: list[Violation] = []
    n_lines = len(source.splitlines())
    if n_lines > max_lines:
        violations.append(Violation(n_lines, "size", f"{n_lines} lines exceed the slot limit of {max_lines}"))
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        violations.append(Violation(exc.lineno or 0, "syntax", exc.msg))
        return ValidationResult(tuple(violations))
    checker = _Checker(frozenset(allowed_imports))
    checker.check_module(tree)
    violations.extend(checker.violations)
    return ValidationResult(tuple(sorted(violations, key=lambda v: (v.line, v.rule))))
