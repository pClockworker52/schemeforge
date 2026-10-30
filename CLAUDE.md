# schemeforge

AI-swarm search for numerical scheme components, judged by exact solutions.
Plan: docs/PLAN.md · State: docs/STATUS.md · Decisions: docs/DECISIONS.md

## Iron rules
1. The judge decides. Every claim about a candidate cites an `sforge eval` run id. Never estimate or invent scores.
2. Never edit `src/schemeforge/arenas/**` during a search round. A judge change is its own commit, bumps the judge
   version, and is followed by `sforge zoo eval` and an archive rescore.
3. Never read `~/.schemeforge/` or try to reconstruct held-out instances.
4. Candidates are pure functions: imports only from jax.numpy, jax.lax, math; no I/O, no hidden state,
   no Python loops over cells.
5. Register a hunch (`sforge hunch add`) with mechanism, predicted effect and kill criterion before testing it.
6. Never call a result novel. Labels: rediscovery / variant of X / plausibly new. Only the referee assigns
   "plausibly new".
7. Record negative results in the ledger.
8. float64 everywhere: `jax.config.update("jax_enable_x64", True)`.

## Session protocol
- Start: read docs/STATUS.md and the current phase in docs/PLAN.md; state the session goal in one sentence.
- During: small commits; tests green before each commit.
- End: update docs/STATUS.md (done / next / blockers / numbers), commit.
- Stop at every phase gate and ask Peter.

## Commands (prefix with `uv run` unless the venv is active; run inside WSL)
- Tests: `pytest -q` · Lint: `ruff check .`
- Evaluate: `sforge eval <file> --arena euler1d --slot limiter --suite dev`
- Leaderboard: `sforge leaderboard --arena euler1d --slot limiter --pareto --vs-zoo`
- Ledger: `sforge hunch add ledger/drafts/<file>.yaml` · `sforge hunch list --open`
- Judge self-check: `sforge judge verify --arena euler1d`

## Layout
src/schemeforge/{core,arenas,engine} · candidates/ (agent workspaces, gitignored) · cases/quarantine
dossiers/ · ledger/ · runs/ (gitignored) · audit/

## Style
Python >= 3.11, type hints, ruff, pytest + hypothesis. Docstrings state array shapes and units.
