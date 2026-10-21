# STATUS
Phase: 3 — Production search, Arena 1 (started 2026-10-21)  Judge version: euler1d-v1.2 (2026-10-21, c9f21da)  Plan: v1.2
Last session: 2026-10-20 — Gate 1 passed; Phase 2 engine, MCP server and calibration runs

## Gate 1 — passed 2026-10-20
Blind audit (audit/euler1d/REPORT.md): 1,002 random instances agree to 6.5e-13; the one judge bug it found
(p_b within rounding of p_crit2) is fixed. Peter's decisions: Roe dropped, Target A thresholds accepted
(docs/targets/A.md), Target B and Venkatakrishnan K > 0 later. Judge tagged `euler1d-v1.0`; zoo re-evaluated.

## Latest results (2026-10-20, evening)
- Reports 2026-10-21: docs/reports/2026-10-21-interim.html (the day's work, round 2 so far) and
  docs/reports/2026-10-21-big-picture.html (what was built, what it found, whether to continue → plan v1.2).
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
- [x] Cost per 100 candidates measured and the Phase 3 budget agreed — Peter 2026-10-21: full PLAN §18 round
      size (DECISIONS.md "Gate 2 decisions").

**Gate 2 passed 2026-10-21** (Peter's decisions on budget, stagnation stop, round 2 and dev nozzles: DECISIONS.md).
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

## Next (ordered; PLAN §11.5, plan v1.2, DECISIONS.md "Phase 3 revision")
State: judge euler1d-v1.2 is in use (dev nozzle sweeps N5/N6 and the `limiter_stateful` slot, c9f21da).
Round 2 (`limiter_stateful`) is paused at generation 11 of 20 (e-20261021-123207-3146), and H-0005…H-0010 are
still open in the ledger. The round-2 findings so far are in docs/reports/2026-10-21-interim.html.
1. 3a: close round 2: re-evaluate the ~90 timed-out children alone, resume or stop the run, promo +
   `sforge promote --target A` for the top 2–3, close H-0005…H-0010, write the round summary.
2. 3b: swarm test from WSL: check that the sforge MCP server connects; cheater against v1.2; breaker against
   c-a84758f0e8; the swarm criterion is fixed before round 3.
3. 3c: register H-0011 and run the A1 + A7 feasibility sweep for φ(r) (~30 dev points, promo on 3).
4. 3d: judge v1.3 (reconstruction constraints, stateful variant, zoo incl. THINC/BVD, descriptors), zoo eval,
   red team, then round 3 on `reconstruction` with agent-written hunches.
5. 3e: decision point with Peter after round 3; §11.4 kill criterion still applies (4 rounds / ~2,000 candidates).

## Blockers / questions for Peter
- Subagents: launching `scripts/headless/run.sh … redteam` from the desktop session was blocked by the auto-mode
  classifier ("Create Unsafe Agents"), and the desktop session has no sforge MCP tools. The red team and round 1
  were therefore run by the orchestrator itself. Recommended: one cheater-agent run against v1.1 from WSL
  (independent attacker), and proposer/breaker agents for round 2 from a WSL session.

## Notes
- Run everything in WSL; the venv lives at ~/.venvs/schemeforge behind the `.venv` symlink (DECISIONS.md).
- Calibration runs use their own working directory (own registry, ledger, candidates): scripts/e2e_evolve.py.
- Use `set -o pipefail` when chaining tests with `| tail` before a commit.
- Never run other evaluations next to `sforge evolve`: on 2026-10-21 evolve + a 6-way rescore + promo runs pushed
  dev evaluations from ~40 s to > 600 s (45 children rejected as timeouts, all ok when re-evaluated alone) and
  the WSL service crashed. A resumed run keeps such false rejections in its archive; re-evaluate them by id.
- Long WSL jobs need an attached `wsl.exe` client; processes started with setsid/nohup die when it exits.

## Numbers to remember (run ids, best candidates, costs)
- Machine: 16 physical cores / 32 threads, 15 GB RAM in WSL → evaluation lock default K = 15.
- Dev suite 25.7 s per candidate alone; zoo dev ~70 s, zoo promo ~5 min wall (12 members in parallel).
- Engine (dummy backend): ~1.5 min per generation of 16 children on the dev suite.
- Zoo results: docs/judge/euler1d_baseline.md; Target A: docs/targets/A.md.
