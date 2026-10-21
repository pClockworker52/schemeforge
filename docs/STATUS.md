# STATUS
Phase: 2 — Engine, calibration, red team (in progress)      Judge version: euler1d-v1.1 (tagged 2026-10-21)
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
- Red team done 2026-10-21 by the orchestrator (the cheater subagent could not be launched; docs/judge/redteam.md):
  12 attempts. Four got through v1.0: case detection from the batch size or from batch statistics (limiter:
  superbee sharpness on Riemann cases plus van Albada convergence on nozzles; flux: HLLC contacts plus HLL
  convergence), and cost gaming via the same channel. Fixed in judge v1.1 (2f4652f, tagged): candidates are
  applied one item at a time in runs, plus a hard batch-independence check; `lax.stop_gradient` rejected. All 12
  attempts caught under v1.1 (run ids in the log). Zoo re-evaluated (dev + promo) with unchanged scores;
  `judge verify` 49/49. Known gap: derivative decoupling via zero-derivative ops (no gain seen; Phase 5
  `grad_mismatch`).
- Registry: `connect` no longer re-sets WAL mode on every open (it took a lock and crashed 6 of 12 parallel zoo
  dev evaluations with "database is locked").

## Gate 2 (PLAN §10)
- [x] `sforge evolve` runs ≥ 200 candidates unattended and resumes after an interruption — dummy backend,
      208 children in runs/e2e-dummy; survived a kill, a SQLite lock crash and its stagnation stop, each resumed.
- [x] C1: fingerprints recognize ≥ 4 different zoo limiters (5: MC, van Leer, Koren, van Albada, superbee) and
      archive entries spread over the descriptor grid — after the 2026-10-21 re-binning: C1 14 cells, round-1
      evolve 7 cells from two smooth seeds (were 6 for C1 on the old grid).
- [x] Every red-team strategy caught and documented — docs/judge/redteam.md, judge v1.1 (attacks run by the
      orchestrator, not an independent cheater agent; a cheater run against v1.1 from WSL is still advisable).
- [ ] Cost per 100 candidates measured and the Phase 3 budget agreed — from the C1 run; Peter agrees the budget.
- [x] Proposer, breaker and hunch-generator run without Bash, through the `sforge` MCP server (.mcp.json).
- [x] First hunch round with ledger verdicts and a docs/rounds/ summary — 2026-10-21,
      docs/rounds/2026-10-21-euler1d-limiter.md: H-0001, H-0002, H-0004 refuted, H-0003 inconclusive; evolve
      e-20261021-045407-c003 (48 children, $2.70); best candidate c-44f8015f87 not promoted for Target A (promo
      r-20261021-050453-0b6a). Run by the orchestrator without subagents (see the summary).

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
4. ~~Red team~~ and ~~first hunch round~~ done (orchestrator, 2026-10-21).
5. **Gate 2 with Peter** — all work items are done; open decisions under "Blockers / questions".

## Blockers / questions for Peter
- LLM budget (proposal for Gate 2, not agreed): measured list price per 100 single-shot candidates is $4.34
  (limiter, C1) and $6.43 (flux, C2), sonnet + haiku for wild; ~520–570 candidates/h. PLAN §18's example round
  (~500 single-shot calls) is then ~$22–32 list and ~1 h of engine time, plus ~10 opus agent sessions not yet
  measured (the red-team run will give the first number). On the subscription, the 2026-10-20 limit ran out
  after C1 (96 calls) plus that day's other work, so a full round likely spans two or more usage windows; the
  engine already pauses and resumes when requests stop reaching the model. Proposal: default mix as in C1/C2;
  first Phase 3 round at half the example size (3 hunches, 2 islands × 10 gens × 8 ≈ 160 calls ≈ $10 list), then
  set the per-round budget from its measured agent-session cost.
- Selection objectives (open): with 7 objectives, 40 of C2's 48 children are non-dominated, so the "no new
  non-dominated candidate for 8 generations" stop never fires. Options: stop on archive progress (new cell or
  better elite) instead, or select on 2–3 target objectives. Not changed — it alters PLAN §5.9 behaviour.
- Subagents: launching `scripts/headless/run.sh … redteam` from the desktop session was blocked by the auto-mode
  classifier ("Create Unsafe Agents"), and the desktop session has no sforge MCP tools. The red team and round 1
  were therefore run by the orchestrator itself. Recommended before Phase 3: one cheater-agent run against v1.1
  from WSL (independent attacker), and proposer/breaker agents for round 2.
- Round 1 questions (docs/rounds/2026-10-21-euler1d-limiter.md): continue H-0003's tanh-cap family or move to
  `limiter_stateful`; add more nozzle instances to dev (judge v1.2), since one N1 instance overstated explicit
  convergence.

## Notes
- Run everything in WSL; the venv lives at ~/.venvs/schemeforge behind the `.venv` symlink (DECISIONS.md).
- Calibration runs use their own working directory (own registry, ledger, candidates): scripts/e2e_evolve.py.
- Use `set -o pipefail` when chaining tests with `| tail` before a commit.

## Numbers to remember (run ids, best candidates, costs)
- Machine: 16 physical cores / 32 threads, 15 GB RAM in WSL → evaluation lock default K = 15.
- Dev suite 25.7 s per candidate alone; zoo dev ~70 s, zoo promo ~5 min wall (12 members in parallel).
- Engine (dummy backend): ~1.5 min per generation of 16 children on the dev suite.
- Zoo results: docs/judge/euler1d_baseline.md; Target A: docs/targets/A.md.
