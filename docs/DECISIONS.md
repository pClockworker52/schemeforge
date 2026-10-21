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

## 2026-10-20 — Engine: build our own (OpenEvolve and ShinkaEvolve reviewed)
*Context:* PLAN §5.9/§10 task 1: adopt an existing framework only if it can use `sforge eval` unchanged as its
evaluator and our registry and ledger stay the source of truth.
*Findings:* OpenEvolve (Apache-2.0): Python `evaluate(program_path)` returning metrics (could wrap `sforge eval`),
MAP-Elites over evaluator metrics, ring-migration islands, a `claude_code` provider; but its own program
database and checkpoints drive parent selection. ShinkaEvolve (Apache-2.0): `evaluate.py` + `run_shinka_eval`,
its own SQLite program database, embedding-based novelty, `headless/claude` model strings.
https://github.com/algorithmicsuperintelligence/openevolve · https://github.com/SakanaAI/ShinkaEvolve
*Decision:* Write our own engine (~500 lines): islands keyed by registered hunches, Pareto/MAP-Elites selection
from our registry, operators and prompts from Appendix E, backends `dummy` and `claude-cli`. Ideas borrowed:
raw-metric descriptors binned by the engine, migration as a later option, CLI provider pattern.
*Consequences:* No second population database; every candidate and score lives in runs/registry.sqlite.

## 2026-10-20 — Gate 1 decisions (Peter)
*Context:* Gate 1 review of the Arena 1 judge, baseline report and blind audit.
*Decision:* (1) Roe is dropped from the zoo (positivity failure on R2 and some RF1 instances). (2) The Target A
thresholds proposed in the baseline report are accepted → docs/targets/A.md. (3) Target B thresholds are set
later, from the well-balanced `operator` baseline at the start of Phase 3. (4) Venkatakrishnan K > 0 waits for
the reconstruction slot. (5) The blind audit (audit/euler1d/REPORT.md) is accepted: 1,002 random instances
agree to 6.5e-13; the one judge bug it found (p_b within rounding of p_crit2) is fixed.
*Consequences:* Judge tagged `euler1d-v1.0` after these changes; zoo re-evaluated under v1.0.

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

## 2026-10-21 — MAP-Elites grids fitted to the populated descriptor range
*Context:* C1 filled 6 archive cells and C2 3. The descriptors were fine but the bins were not: limiter
compressiveness spans 0.83–1.42 over the whole zoo and 80 % of C1 children lie in 0.97–1.33 (about two of the
eight 0.25-wide bins); every kinked limiter (max |φ''| ≥ 50) shared one smoothness bin; flux dissipation spans
1.85–4.42, two of eight log bins over 1e-3–10. Superbee and Koren shared a cell.
*Decision:* (1) Limiter: compressiveness edges 0, 0.85, 0.95, …, 1.45 (0.1 wide); smoothness edges 0, 0.3, 1, 3,
10, 30, 75, 115, 150, which split the kinked limiters by kink size (minmod/MC 100, Koren 133, superbee 200).
(2) Flux: dissipation edges 0, 0.5, 1, 1.5, then 0.25 wide up to 2.5, then 0.5 wide up to 4.5. contact_dissipation
unchanged. (3) A test requires every zoo member of a slot to have its own cell. Proposed by the orchestrator
without Peter (session goal "continue without my help"); search policy only, judge untouched.
*Consequences:* Re-binning the existing children: C1 6 → 14 cells, C2 3 → 7. Old run states keep their old cell
keys; do not resume a pre-change run, start a new one. The 7-objective selection issue (STATUS) is separate and
still open.
