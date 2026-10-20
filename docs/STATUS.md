# STATUS
Phase: 2 — Engine, calibration, red team (in progress)      Judge version: euler1d-v1.0 (tagged)
Last session: 2026-10-20 — Gate 1 passed; Phase 2 engine, MCP server and calibration runs

## Gate 1 — passed 2026-10-20
Blind audit (audit/euler1d/REPORT.md): 1,002 random instances agree to 6.5e-13; the one judge bug it found
(p_b within rounding of p_crit2) is fixed. Peter's decisions: Roe dropped, Target A thresholds accepted
(docs/targets/A.md), Target B and Venkatakrishnan K > 0 later. Judge tagged `euler1d-v1.0`; zoo re-evaluated.

## Gate 2 (PLAN §10)
- [ ] `sforge evolve` runs ≥ 200 candidates unattended and resumes after an interruption — running:
      dummy backend, 2 islands × 13 generations × 8 children (208) in runs/e2e-dummy; killed in generation 2
      and resumed successfully (scripts/e2e_evolve.py, scripts/calibration_report.py).
- [ ] C1: fingerprints recognize ≥ 4 different zoo limiters, archive entries spread over the descriptor grid —
      next: real LLM run, 3 islands × 4 generations × 8 children (96 calls) in runs/c1.
- [ ] Every red-team strategy caught and documented — needs a WSL Claude Code session (cheater subagent).
- [ ] Cost per 100 candidates measured and the Phase 3 budget agreed — from the C1 run; Peter agrees the budget.
- [x] Proposer, breaker and hunch-generator run without Bash, through the `sforge` MCP server (.mcp.json).
- [ ] First hunch round with ledger verdicts and a docs/rounds/ summary — WSL session.

## Done in Phase 2
- Build-or-adopt: own engine (OpenEvolve and ShinkaEvolve reviewed; DECISIONS.md).
- Ledger (`sforge hunch add|list|show|close`), `sforge submit`, `sforge leaderboard --pareto --vs-zoo`.
- Engine (`sforge evolve`): islands per hunch, Pareto/MAP-Elites selection from the registry, Appendix E
  operators, smoke → dev with probes, duplicate detection by fingerprint, stagnation stop, budget, resume.
- Backends: `dummy`, `claude-cli` (verified with real calls: ~19 s, ~20k in / 1.5k out tokens, list price
  ~$0.05 per call; subscription login, apiKeySource none).
- `sforge` MCP server; proposer, breaker, hunch-generator and cheater use it instead of Bash.
- `sforge case propose|accept`. Promo aggregates carry the mean (share of instances for 0/1 flags).

## Next (ordered)
1. Finish the dummy 208-candidate run; record it for Gate 2.
2. C1 with the real backend (96 calls), calibration report, cost per 100 candidates.
3. C2 (flux slot) — after Peter agrees the budget.
4. Peter, in a WSL session: red team with the cheater agent; first hunch round (Appendix D).

## Blockers / questions for Peter
- LLM budget: C1 at 96 calls is about $5 list price on the subscription. Full C1 (360 calls) and C2 need your OK.
- Red team and the first hunch round need subagents with hooks, i.e. a Claude Code session inside WSL.
- Observation for Phase 3: with 7 objectives almost every distinct candidate is Pareto-optimal, so the
  "8 generations without a new non-dominated candidate" stop rarely fires; consider fewer selection objectives.

## Notes
- Run everything in WSL; the venv lives at ~/.venvs/schemeforge behind the `.venv` symlink (DECISIONS.md).
- Calibration runs use their own working directory (own registry, ledger, candidates): scripts/e2e_evolve.py.
- Use `set -o pipefail` when chaining tests with `| tail` before a commit.

## Numbers to remember (run ids, best candidates, costs)
- Machine: 16 physical cores / 32 threads, 15 GB RAM in WSL → evaluation lock default K = 15.
- Dev suite 25.7 s per candidate alone; zoo dev ~70 s, zoo promo ~5 min wall (12 members in parallel).
- Engine (dummy backend): ~1.5 min per generation of 16 children on the dev suite.
- Zoo results: docs/judge/euler1d_baseline.md; Target A: docs/targets/A.md.
