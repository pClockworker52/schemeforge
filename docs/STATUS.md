# STATUS
Phase: 0 — Setup (at Gate 0, two checks need Peter)      Judge version: —
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
- [ ] Agents visible in Claude Code, and the hook blocks a proposer write outside `candidates/`.
      The hook logic is tested directly (tests/test_guard_paths.py); the live check needs a Claude Code session in WSL.
- [ ] Seed file exists, and Claude Code is denied when it tries to read it (Peter)
- [x] `STATUS.md` is filled in

## Next (ordered)
1. Peter: create the seed and run the two live checks (commands below).
2. Phase 1 (§9): exact Riemann and nozzle solutions with tests against Appendix H.

## Blockers / questions for Peter
- Create the held-out seed in WSL:
  `mkdir -p ~/.schemeforge && python3 -c "import secrets; print(secrets.token_hex(16))" > ~/.schemeforge/heldout_seed`
- Start Claude Code **inside WSL** for anything that uses subagents: `cd /mnt/c/Users/peter/schemeforge && claude`.
  Then: `/agents` should list the 7 agents; ask it to "use the proposer subagent to write a file docs/x.md"
  (should be blocked by the hook); ask it to "read ~/.schemeforge/heldout_seed" (should be denied).

## Numbers to remember (run ids, best candidates, costs)
- Machine: 16 physical cores / 32 threads, 15 GB RAM in WSL → evaluation lock default K = 15.
- JAX core pinning: `os.sched_setaffinity` before importing JAX gives CPU/wall 0.98; the XLA flag alone used ~23 cores.
