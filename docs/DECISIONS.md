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

## 2026-10-20 — Held-out family sizes and the NF3 sweep
*Context:* Promo must stay at "minutes" per candidate and give at least 50 held-out instances (PLAN §5.8).
*Decision:* RF1 20, RF2 10, NF1 20, NF2 10, NF3 5 instances (65 in total). NF3 sweeps 11 back pressures with the
implicit solver only; the 41-point sweep with both solvers is run once for the zoo in the baseline study, not
for every candidate. max_cfl uses the first 5 RF1 instances. Grid-convergence studies on held-out nozzles are
not in promo yet.
*Consequences:* PLAN §9.5 table note updated. Revisit the sizes when promotion tests need more power.

## 2026-10-20 — Venv on the WSL file system; no memory limit yet
*Context:* Every evaluation runs in a fresh worker process. With the venv on `/mnt/c`, a cold
`import schemeforge.arenas.euler1d.evaluate` took 27 s (9p file system); on ext4 it takes 4.8 s.
*Decision:* The venv lives at `~/.venvs/schemeforge` (WSL ext4) and the repo's `.venv` is a symlink to it, so
`uv run` works unchanged for Peter and the agents. `RLIMIT_AS` is off for now (JAX reserves large virtual
address ranges); the worker has a CPU-time limit and the parent a wall-clock timeout.
*Consequences:* After cloning elsewhere, recreate the link (`ln -s ~/.venvs/schemeforge .venv`, then
`uv sync`). Revisit a memory limit (RLIMIT_DATA or a cgroup) in the Phase 2 red-team work.

## 2026-10-20 — Appendices A–C adaptations
*Context:* Phase 0 creates CLAUDE.md, the agents, the hook and the settings verbatim from the plan.
*Decision:* Two changes. CLAUDE.md says to run commands inside WSL. The CLI exits with code 3 for "not
implemented", so tests can tell it apart from usage errors (2).
*Consequences:* None for later phases.

## 2026-10-20 — Zoo: Venkatakrishnan form and the Roe positivity failure
*Context:* PLAN §9.8 asks for a Venkatakrishnan-type limiter "with several values of K", and Gate 1 asks that
every zoo member passes the hard constraints.
*Decision:* (1) The zoo has the ε = 0 (K = 0) Venkatakrishnan limiter in exact 1D slope-ratio form. K > 0 adds
ε² = (K dx)³ to differences, which needs absolute differences and dx and breaks scaling homogeneity, so it does
not fit the φ(r) slot; it can return with the reconstruction slot. (2) Roe with Harten's entropy fix produces NaN
on R2 (123 problem) with MUSCL-minmod, as expected from Einfeldt et al. (1991). It stays in the zoo as a
documented known failure rather than being weakened (proposed; Peter decides at Gate 1).
*Consequences:* Gate 1's "hard constraints pass for every zoo member" reads "except the documented Roe/R2
failure". Roe is scored on the cases where it runs and marked "rejected: R2" on the leaderboard.

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
