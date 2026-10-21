# STATUS
Phase: 2 — Engine, calibration, red team (in progress)      Judge version: euler1d-v1.0 (tagged)
Last session: 2026-10-20 — Gate 1 passed; Phase 2 engine, MCP server and calibration runs

## Gate 1 — passed 2026-10-20
Blind audit (audit/euler1d/REPORT.md): 1,002 random instances agree to 6.5e-13; the one judge bug it found
(p_b within rounding of p_crit2) is fixed. Peter's decisions: Roe dropped, Target A thresholds accepted
(docs/targets/A.md), Target B and Venkatakrishnan K > 0 later. Judge tagged `euler1d-v1.0`; zoo re-evaluated.

## Latest results (2026-10-20, evening)
- Dummy engine run (runs/e2e-dummy): 208 children, all ok on dev; survived a kill, a SQLite lock crash (fixed:
  WAL + busy timeout) and its own stagnation stop, each resumed from state.json. → Gate 2 item 1 met.
- C1 real backend (runs/c1, sonnet + haiku for wild): 96 calls, 90 ok, 1 rejected, 5 LLM errors (gen 3);
  36 duplicates, 5 distinct zoo limiters rediscovered (MC 11, van Leer 7, Koren 4, van Albada 4, superbee 2)
  → fingerprints work (≥ 4 required); only 6 archive cells occupied (grid too coarse / descriptors cluster).
  Cost: $4.34 per 100 candidates (list price, subscription), 10.5 s mean latency, ~19k/630 tokens per call,
  ~570 candidates/h. The 5 LLM errors (all in the last generation, 20:44 UTC) had zero API time and zero
  tokens: the requests never reached the model — the subscription usage limit ran out at that time. Fixed:
  the backend now reports such calls as "did not reach the model" with the CLI's own message, and `evolve`
  pauses (state saved, `--resume`) when half a generation's requests do not reach the model.
- C2 done 2026-10-21 (runs/c2, run e-20261021-032121-30b5; flux slot, Rusanov seed, 2 islands × 3 gens × 8,
  sonnet + haiku for wild): 48 calls, 48 ok on dev, 0 rejected, 0 LLM errors, no interruption.
  9 duplicates, 2 distinct zoo fluxes rediscovered (HLLC 4, Rusanov 3); only 3 archive cells occupied
  (6,0 / 6,3 / 7,0) — same clustering as C1; Pareto front 40 of 48 (the 7-objective issue again).
  Cost $3.09 list = $6.43 per 100 candidates (longer outputs than limiters: ~20.8k/2.1k tokens per call),
  16.0 s mean latency, 516 candidates/h. Run took 8 min.
  PLAN task 4 (HLLC-level contact on R5 without losing robustness) — reached on dev:
  c-edd6d69254 (run r-20261021-032658-20c4; gen-2 crossover, HLLC star states with Rusanov speeds ±max(|u|+a))
  has R5 contact_width 0.90 cells and l1_smooth 0 (= zoo HLLC, r-20261020-194829-470b; Rusanov 10.5 cells) and
  converges explicitly on N1 like Rusanov/HLL (res_orders_expl 12.0, no limit cycle; HLLC: 2.5 orders, limit
  cycle), Newton 44 steps (HLLC 60, HLL 61, Rusanov 35). R1 contact 6.56 (HLLC 6.29, HLL 6.72), R7 l1_ref 0.0064
  (HLLC 0.0058). Label: variant of HLLC (wave-speed choice; Rusanov/Davis bounds are textbook options). Dev
  only, one instance per case — no held-out evidence. The leading c-6d6bcaf064 (r-20261021-032702-c051) is
  HLLC-like and inherits HLLC's N1 limit cycle.
  Caveat: in an isolated workdir `leaderboard --vs-zoo` compares against the seed only (no zoo in that
  registry), so its "best zoo member" ratios there are ratios to Rusanov.
- Archive grids re-binned 2026-10-21 (DECISIONS.md): every zoo member now has its own cell; re-binning the
  existing children gives C1 6 → 14 cells, C2 3 → 7. Gate 2's "spread over the descriptor grid" should be
  re-checked on the next real run.
- Next: red team and first hunch round via
  bash scripts/headless/run.sh scripts/headless/redteam.txt redteam; then Gate 2 with Peter (budget).
  All three use the subscription — wait until the usage limit has reset.

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
3. ~~C2 (flux slot)~~ done 2026-10-21 (see Latest results); descriptor grids re-binned the same day.
4. Peter, in a WSL session: red team with the cheater agent; first hunch round (Appendix D).

## Blockers / questions for Peter
- LLM budget: C1 at 96 calls is about $5 list price on the subscription. Full C1 (360 calls) and C2 need your OK.
- Red team and the first hunch round need subagents with hooks, i.e. a Claude Code session inside WSL.
  2026-10-21: launching `scripts/headless/run.sh … redteam` from the desktop session was blocked by the auto-mode
  classifier ("Create Unsafe Agents"). Peter: run it yourself in WSL, or allow it for this session.
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
