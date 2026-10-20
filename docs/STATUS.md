# STATUS
Phase: 0 — Setup (Gate 0 passed; next: Phase 1)      Judge version: —
Last session: 2026-10-20 — plan v1.1; Phase 0 scaffold: layout, CLI skeleton, sandbox validator, registry, agents, hook

## Done
- Plan v1.1 (simplifications, MCP server and project skills for Phase 2), saved as docs/PLAN.md.
- WSL2 toolchain: Ubuntu 24.04, Python 3.12.3, uv 0.13.3, jax 0.10.2 (CPU, float64 checked). `uv.lock` pins everything.
- Layout from PLAN §5.3, `.gitignore`, `.gitattributes` (LF), `pyproject.toml` with the `sforge` entry point.
- CLAUDE.md, the 7 subagents, `guard_paths.py` and `.claude/settings.json` from Appendices A–C (adaptations in DECISIONS.md).
- `sforge` CLI skeleton: all 16 commands from §5.5 with `--help`; each exits 3 "not implemented".
- `core/sandbox.py` AST validator: 36 hostile snippets rejected, 5 clean candidates pass.
- `core/registry.py`: tables candidates, runs, scores, cases, llm_calls; foreign keys on; schema version in user_version.
- Tests: 81 passed (`uv run pytest -q`), `uv run ruff check .` clean.

## Gate 0
- [x] `sforge --help` lists all commands
- [x] `pytest -q` and `ruff check .` pass; the sandbox tests include at least 10 hostile snippets (36)
- [x] Agents visible in Claude Code (WSL session lists all 7 project agents), and the hook blocks a proposer write
      outside `candidates/`: "Blocked: this agent may only write under candidates/ (tried docs/x.md)"; no file created.
- [x] Seed file exists (Peter created it in WSL), and Claude Code's Read is denied: "File is in a directory that is
      denied by your permission settings."
- [x] `STATUS.md` is filled in

**Gate 0 passed 2026-10-20.**

## Next (ordered)
1. Phase 1 (§9): exact Riemann and nozzle solutions with tests against Appendix H.

## Blockers / questions for Peter
- The WSL Claude Code install shows "API Usage Billing". Switch to the subscription (`/logout`, `/login`) before
  Phase 2 if usage should come from the plan rather than the API account.
- Run subagent work only from Claude Code inside WSL (see DECISIONS.md, 2026-10-20).

## Numbers to remember (run ids, best candidates, costs)
- Machine: 16 physical cores / 32 threads, 15 GB RAM in WSL → evaluation lock default K = 15.
- JAX core pinning: `os.sched_setaffinity` before importing JAX gives CPU/wall 0.98; the XLA flag alone used ~23 cores.
