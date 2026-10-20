# DECISIONS

## 2026-10-20 — Plan v1.1 simplifications
*Context:* The v1.0 plan had a few internal contradictions (mirror symmetry vs. the Koren limiter, judge hash not
covering accepted cases) and more Phase 1–2 scope than the gates need.
*Decision:* Adopt plan v1.1 (see the change note at the top of docs/PLAN.md), including the `sforge` MCP server
and project skills in Phase 2.
*Consequences:* Smaller Phase 1 zoo and slot set; Phases 5, 8, 9 parked; `Bash` is removed from the proposer,
breaker and hunch-generator once the MCP server exists.

## 2026-10-20 — Run everything inside WSL2
*Context:* Peter's machine is Windows 11. The sandbox needs POSIX `resource.setrlimit`, the agent hooks call
`python3`, and Claude Code is installed in WSL (`~/.local/bin/claude`).
*Decision:* The repo stays at `C:\Users\peter\schemeforge` (`/mnt/c/Users/peter/schemeforge` in WSL). Python,
`uv`, tests and Claude Code sessions that use the subagents run inside WSL (Ubuntu 24.04, Python 3.12).
`.gitattributes` forces LF line endings. `uv` was installed from PyPI into `~/.local/share/uv-bootstrap` and
linked into `~/.local/bin`.
*Consequences:* A Claude Code session started on the Windows side can edit files but must not be used for
subagent runs: its hooks would call a Windows `python3`, which may not exist, and a failing hook does not block.
The venv sits in the repo on the Windows file system (`.venv/`); if imports or JIT times turn out slow in
Phase 1, move it to the WSL file system with `UV_PROJECT_ENVIRONMENT`.

## 2026-10-20 — Appendices A–C adaptations
*Context:* Phase 0 creates CLAUDE.md, the agents, the hook and the settings verbatim from the plan.
*Decision:* Two changes. CLAUDE.md says to run commands inside WSL. The CLI exits with code 3 for "not
implemented", so tests can tell it apart from usage errors (2).
*Consequences:* None for later phases.

## 2026-10-20 — Sandbox validator scope
*Context:* PLAN §5.6 lists the static checks.
*Decision:* Beyond the plan's list, the validator also rejects decorators (they run code at import time),
non-constant default arguments, attribute assignment, class definitions, `print`/`id`/`hash`/`type`, unaliased
`import jax.numpy` (it binds `jax`, which exposes `jax.random`), the file-I/O helpers of `jax.numpy`
(`load`, `save`, ...), and `str.format` (format fields can reach dunder attributes). Module-level values must be
numeric constants, tuples of them, `math.*` expressions or lambdas. "No Python loops over cells" is left to the
cost metric.
*Consequences:* The engine prompt (Appendix E) should mention these rules once the first rejections show which
ones models trip over.
