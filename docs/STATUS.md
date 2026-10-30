# STATUS
Phase: 3 — Production search, Arena 1 (started 2026-10-21)  Judge version: euler1d-v1.5 (2026-10-24, 919c544)  Plan: v1.2
Last session: 2026-10-29/30 (WSL) — Phase 3 wrap-up: H-0019 evidence (2 kill rows), breakers on the round-4 top 3
Handoff 2026-10-28: docs/HANDOFF.md (next steps, open items, traps). sforge MCP server did not connect from the
desktop session on 2026-10-28; restart it before round-4 evolve.
2026-10-28 (desktop): evolve e-20261028-201918-36b6 stopped after gen 0 (16/16 rejected, 14 false timeouts, $1.17;
seed alone: smoke 57.6 s r-20261028-204346-2c47, dev 406–492 s). Peter chose option 1: timeouts raised to smoke 300 s /
dev 1500 s (DECISIONS 2026-10-28). Rerun e-20261028-212642-e595 failed the same way ($0.87): the real cause is memory
(4.4 GB peak per worker, r-20261028-220113-4600, vs 2 GB assumed for K = 7). Round-4 evolve restarted with
SFORGE_MAX_PARALLEL=3 (~1 h per generation).
2026-10-29: **round 4 done, waiting at the step-5 gate.** Evolve e-20261028-220902-e988 completed (15 gens, 240
children, front 200, $20.34; Windows Update restart at 03:34, resumed 06:52). Promo + promote A/Ac on the top 5: none
promoted. Nearest miss c-4ece6bb6f7 r-20261029-122317-32a7 fails only A4 (NF1 Newton 0.85) and passes A1 2.243, A5
1.47e-5 and A7b together; c-82efea7caf r-20261029-122320-15bb fails only A4 (0.75). H-0019 table: 0 kill rows,
ρ = −0.936 (n = 12; −0.943 over the 6 distinct rows). Summary + proposed verdicts:
docs/rounds/2026-10-29-euler1d-reconstruction_stateful-r4.md. Open: breakers on the top 3 (need WSL claude + sforge
MCP), Peter's call on H-0024, then the negative-result note per the stop rule.
2026-10-29: **negative-result note drafted**, docs/results/arena1-negative.md (Peter's choice at the step-5 gate):
what was tried per round, the conflict between Target A's criteria (overshoot → long-run accuracy → roughness → Newton),
the v1.5 zoo front with run ids, every hunch verdict (round 4 proposed), method results, limits. Next: Peter closes
H-0019..H-0025, breakers on the round-4 top 3, benchmark release (PLAN §20), Phase 6.
2026-10-29/30 (WSL): **Phase 3 wrap-up done, waiting for Peter.** Pre-checks: merged 864641b, pytest 277, judge
euler1d-v1.5 integrity ok, sforge MCP connected (its process has no SFORGE_MAX_PARALLEL; breakers evaluated strictly
one at a time). (1) H-0019 evidence: v1.5 promo of the round-2 limiters, both ok and both meet the kill criterion:
c-b5cb82a0ef r-20261029-185257-3e4a (shock 2.581, Newton 1.00, roughness 0.00175), c-fb8db52bca
r-20261029-185256-7cd3 (2.582, 1.00, 0.00142); neither promoted (A7, A8; A6 nan, no v1.5 dev run). Table rerun:
2 kill rows, ρ −0.592 (n 14). H-0019 proposed *refuted*, not closed. (2) Breakers, one at a time:
c-4ece6bb6f7 B-0037..B-0044, c-82efea7caf B-0045..B-0051, c-60c5ed6928 B-0052..B-0056 (20 cases in quarantine;
17 nozzle Newton stalls where both van Leer members converge, worst in low-Mach flow; 3 slow-shock overshoot up to
5.96 × vL). Report docs/rounds/2026-10-29-round4-breakers.md; note updated (H-0019 table, Limits). Next (Peter):
close H-0019..H-0025, decide H-0024, review B-0037..B-0056 (any acceptance = new judge version + zoo eval + rescore).
Open: add `"env": {"SFORGE_MAX_PARALLEL": "3"}` to .mcp.json so MCP evals respect the memory cap.

## Gate 1 — passed 2026-10-20
Blind audit (audit/euler1d/REPORT.md): 1,002 random instances agree to 6.5e-13; the one judge bug it found
(p_b within rounding of p_crit2) is fixed. Peter's decisions: Roe dropped, Target A thresholds accepted
(docs/targets/A.md), Target B and Venkatakrishnan K > 0 later. Judge tagged `euler1d-v1.0`; zoo re-evaluated.

## Round 4 running (plan step 4; scripts/headless/round4.txt; interactive WSL session, 2026-10-24)
- Pre-checks passed: merged f30cb60; pytest 277; judge euler1d-v1.5 integrity ok; H-0019 open; sforge MCP server
  restarted by Peter (stale since 08:50) and tested (smoke r-20261024-194523-43d5 ok, v1.5); nothing else evaluating.
- Hunches registered 2026-10-24 from the hunch-generator, as written: H-0020 strength-inverse compression (shock
  physics), H-0021 motion-gated compression (steady-convergence), H-0022 positivity scaling (structure preservation),
  H-0023 history not sharpness (contrarian), H-0024 diffused BVD weight (transfer), H-0025 characteristic WENO
  (approximation theory). Four target the steady shock-position / roughness problem directly (generator's count:
  H-0021, H-0023, H-0024, H-0025).
- Proposers done 2026-10-24 (reports: docs/rounds/2026-10-24-round4/proposers/; agents' own verdicts, dev, v1.5):
  H-0020 c-cb9fe80826 r-20261024-202537-69d0 (R1 shock 2.48, N4 roughness 1.3e-5; kill clause 2 fires: B-0010
  overshoot +18.5 % over base); H-0021 c-698b39759f r-20261024-204336-e65e (R1 shock 2.48, N4 roughness = base 1.27e-5,
  B-0011 Newton 0.5; "supported on dev"); H-0022 c-9a3faab538 r-20261024-202309-21b3 (hunch's ε still non-finite on
  B-0030, r-20261024-201321-dc41: "refuted as specified"); H-0023 c-af3143be0c r-20261024-202133-76b1 (N4 roughness
  6.8e-4, R1 2.475, extra safety switches; "partly"); H-0024 c-5ff53c2690 r-20261024-201845-0539 **rejected** (B-0016,
  B-0030; "inconclusive"); H-0025 c-47838d9365 r-20261024-201754-e32b (char. WENO5-Z + van Leer fallback, R1 2.56, N4
  roughness 8.1e-6; promo pending). Most proposers needed positivity/expansion fallbacks outside their mechanism.
- Promo + promote A on the leaderboard top 3 (docs/rounds/2026-10-24-round4/proposer_promo.txt; references limiter/mc
  r-20261024-153251-db77, van_albada r-20261024-153252-8783, van_leer r-20261024-153251-4a12): **c-698b39759f**
  (H-0021) r-20261024-210131-4dcc fails only A4 (NF1 Newton 0.85) and A7b (RF2 overshoot 0.0295 vs 0.0256); passes
  A1 2.19 and A5 0.0014 together (A4 < 1, so not an H-0019 kill). c-9a3faab538 (H-0022) r-20261024-211946-b555 fails
  A1 (2.90) and A4 (0.85). c-47838d9365 (H-0025) r-20261024-205819-e795 fails A3 (0.85), A5 (0.31), A7b (0.0314).
  Islands: H-0021, H-0022 (seeds candidates/H-0021/proposer/cand_1.py, candidates/H-0022/proposer/cand_3.py).
- **Evolve e-20261024-213316-3d46 stopped at 23:33 in generation 0 (0 children)**: Claude Code killed the background
  command because the system was low on memory (its reaper, not the run's own memory use). 7 seeding runs left (1
  rejected, 6 `running`). Not restarted; waiting for Peter.

## Round-4 plan step 2.6 done — judge euler1d-v1.5 tagged and checked (WSL, 2026-10-24)
- Tag commit 919c544 `euler1d-v1.5` (pushed with the tag); `judge version` euler1d-v1.5 (8a8b8304…), integrity ok;
  pytest 277 passed after the registry fix 26818b5 (a changed zoo file gets its own id; failed inserts roll back).
  The first two `zoo eval` attempts died with "database is locked" (duplicate id for the changed thinc_bvd); their
  18 runs stay in status `running` (nothing reads them).
- **Zoo dev** (runs/zoo_v15.log; r-20261024-1526..1529): 19 ok; rejected exactly limiter/koren (B-0030,
  r-20261024-152652-a5d6) and reconstruction/thinc_bvd, now id `zoo-reconstruction-thinc_bvd-f23f9c` (B-0016, B-0030,
  r-20261024-152919-1578). All 20 unchanged members (incl. limiter/van_leer c-38addf805f r-20261024-152651-8c93) are
  identical to their v1.4 zoo runs on the 18 old cases (89 scores each, wall times and wall-time `cost` excepted).
  thinc_bvd vs v1.4 r-20261022-164139-e8e3: 7 scores at rounding level (≤ 8e-9), Newton means B-0011 137.5 → 135.5
  (−1.5 %; the cloud record said < 1 %) and N4 126.7 → 127.4.
- **Zoo promo** (r-20261024-1532..1540): all 168 aggregates identical to v1.4 for the 20 unchanged members (e.g.
  limiter/van_leer r-20261024-153251-4a12 = r-20261022-164508-7c66, limiter_stateful/van_leer r-20261024-153727-dffe
  = r-20261022-164948-bba4, reconstruction_stateful/muscl_van_leer r-20261024-154024-c9f9 = r-20261022-165255-03a8;
  superbee_frozen rejected in both). thinc_bvd r-20261024-154009-f309 vs r-20261022-165235-e685: 38 aggregates differ,
  mostly < 2e-5; beyond rounding only NF1 Newton: converged_impl 0.60 → 0.65, newton_iters median 177 → 153.5
  (relative EPS changes the steady nozzle iteration).
- **Rescore reconstruction_stateful** (2026-10-24, runs/rescore_v15.log; stands, not repeated): 376 candidates, 0 ok;
  360 rejected for the scaling constraint alone, 4 scaling + another violation, 3 TypeError, 2 shape, 1 ValueError,
  2 B-0030 crash, 1 B-0021 + B-0030 crash, 4 not run (file changed since registration). Round-4 parents, rejected for
  scaling only: c-2ca8842812 r-20261024-123127-eb8e, c-a411e8accb r-20261024-130330-3ce1, c-2637af56a6
  r-20261024-125340-04f6. Peter keeps the constraint (DECISIONS "2026-10-24 — scaling constraint kept"): round-4
  proposers start from the parent files and make thresholds relative.
- Open (Peter, own terminal): `sforge case accept` B-0016 B-0019 B-0021 B-0030 (registry only; files already in
  cases/accepted, so the judge is unaffected). Next: round 4 (scripts/headless/round4.txt), started by Peter.

## Round-4 plan step 2 — prepared on the branch, waiting for WSL (2026-10-24)
- Done (cloud): judge clean-up with zoo dev scores identical to v1.4 (21/21), then v1.5 contents: B-0016, B-0019,
  B-0021, B-0030 in dev; zoo thinc_bvd relative EPS; scaling hard constraint (ρ, p × 1e-12 / 1e12, reconstructions
  and fluxes); target Ac; engine selection by failed Target A dev screens, duplicates removed, unreached requests
  free; promote takes references from the target; run-id rule in the agent prompts; scripts/headless/round4.txt.
  Record with run ids: docs/judge/2026-10-24-v15-refactor-check.md; DECISIONS "Judge v1.5 contents".
- Decided (Peter, DECISIONS 2026-10-24): under v1.5 two zoo members stay rejected on dev: limiter/koren (B-0030
  crash) and reconstruction/thinc_bvd (B-0016, B-0030). Target A's references (van Leer, van Albada, MC) are unaffected; the
  limiter and reconstruction leaderboards lose those members from their vs-zoo comparison.
- Deferred: stateless-as-stateful unification and one limiter checker (behaviour-neutral; not needed for round 4).
- Next (WSL): merge; pytest; `sforge case accept` B-0016 B-0019 B-0021 B-0030 (registry only, files already moved);
  zoo eval dev + promo, checking promo of the 19 unaffected members against v1.4; tag euler1d-v1.5 (version string
  without .dev); rescore reconstruction_stateful; then round 4 (scripts/headless/round4.txt).

## Gate 3e passed 2026-10-24 (Peter: round-4 plan docs/plans/2026-10-24-round4.md approved with defaults D1–D5)
- Step 1 done: round-3 hunches closed (D1): H-0012 supported, H-0013 inconclusive, H-0014..H-0017 refuted. Swarm
  outcome (D2) recorded as **H-0018** (orchestrator/method), closed supported (S1 met, S2 weakly). DECISIONS.md
  "2026-10-24 — Gate 3e (Peter)".
- Step 3 done: pre-registered hunch H-SR registered as **H-0019** (ledger/drafts/r4_sharp_vs_smooth.yaml), open.
- Not done yet: quarantine cases are **not** accepted (D3 lands with judge v1.5 from the branch); no evaluations.
- Next: step 2 of the plan (judge v1.5 and engine changes, prepared on the branch; WSL tags, zoo eval, rescore), then
  step 4 (round 4).

## Round 3 results (2026-10-24)
Summary: docs/rounds/2026-10-23-euler1d-reconstruction_stateful.md (all run ids there).
- Suggested verdicts (not closed): H-0012 supported; H-0013 inconclusive (2 of 8 grid points run); H-0014, H-0015,
  H-0016, H-0017 refuted. H-0014 and H-0017 are refuted by the overshoot clauses their proposers did not check (R6
  0.0190–0.0199 vs 1.1 × vL 0.0166; H-0017 B-0010 0.0367 vs 1.2 × thinc_bvd 0.0313).
- Target A: nothing promoted. Best held-out result is still the H-0013 proposer's c-2ca8842812 (fails only A3 0.90,
  A5 0.077; r-20261023-040314-a528). Engine top five (one scheme in four spellings plus one) fail A1 (RF1 shock 3.41)
  and A3 (0.90), c-58306b67e7 REJECTED on promo (NF1 3/20).
- Swarm (docs/targets/swarm.md): S1 met (suggested); S2 met on one island of three, with small gains: H-0012 island
  c-a411e8accb (promo r-20261023-232730-c8f5: A4 1.00 vs 0.95, A7b 0.0236 vs 0.0250, rest within 0.1 %) and
  c-c0644880db / c-0428b6020b. H-0013 and H-0014 islands lose A1 against their seeds.
- Evolve e-20261023-041826-802c: 480 children, 70 duplicates, 29 rejected, 62 LLM errors, $33.99 ($7.08 / 100).
- Breakers: 21 cases in quarantine (B-0016 … B-0036): LeBlanc contact ×5, cold-collision NaN ×6, THINC EPS
  scale dependence ×4, double-rarefaction NaN ×2, low-γ blast, γ 5/3 collision TV, stationary Mach 20, Anderson γ 1.2.
  Two zoo failures found and not proposed (frozen van Leer on a parabolic nozzle; thinc_bvd on planar Noh).

## Earlier results (2026-10-22): round 2 closed (PLAN §11.5 step 3a)
- e-20261021-123207-3146 finished: 20 generations, 480 children, $25.71 list ($11.81 for gens 11–19 against the
  plan's ~$5 estimate; ~$1.3 and ~35 min per generation of 24 at K = 7). Stagnation stop never fired.
- The 90 evolve-time timeouts were memory, not CPU: a `limiter_stateful` dev worker peaks at ~1.45 GB, and 15 of them
  thrash a 15.6 GB machine (reproduced: 15/15 timed out at ~606 s). Fix 2fc0fa7: K is capped at one worker per 2 GB of
  RAM (K = 7 here). All 90 were ok when re-evaluated alone. `scripts/readmit_timeouts.py` put them back into the
  archive (26 duplicates; 64 returned to islands = 5 new cells + 3 replaced elites + 56 declined by the archive;
  backup state.before-readmit.json). Gens 11–19: 0 timeouts.
- Verdicts: H-0006 (ratchet) supported; H-0005, H-0007, H-0009, H-0010 refuted; H-0008 inconclusive. No open hunch.
- Target A: nothing promoted. Near misses on held-out data: c-b5cb82a0ef passes A1–A5, B1, B2, B5 and fails A6
  (S1 order 0.13) and A7 (r-20261022-060255-0a90); c-fb8db52bca passes A1, A2, A4–A6, B1, B2, B5 and fails A3 (0.90)
  and A7 (r-20261022-060626-894c). A7 (overshoot ≤ 1.1 × van Leer) is now the binding criterion.

## Earlier results (2026-10-20, evening)
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
State: judge euler1d-v1.4 on main (71a3d94, tagged); rounds 2 and 3 closed; open hunch: H-0019 (H-SR). Peter's review
2026-10-22 (DECISIONS.md "Judge v1.4"): accept B-0002, B-0004, B-0010, B-0011; add held-out long-run families LF1,
LF2. **Step 0 done 2026-10-22 (see below). 3b(i) closed without an independent cheater (DECISIONS.md).**
**Round 3 done 2026-10-24; gate 3e passed (see top)** (reconstruction_stateful, scripts/headless/round3.txt, run from the interactive WSL session
because the headless run.sh session could not use the shell). Hunches registered 2026-10-22 from the
hunch-generator, as written: H-0012 field-selective compression (shock physics), H-0013 chatter lock
(steady-convergence), H-0014 entropy-production blend (structure preservation), H-0015 steep shock less overshoot
(contrarian), H-0016 delayed MOOD (transfer), H-0017 dictionary BVD (approximation theory).
Proposers done 2026-10-23 (first launch got 0 evals: the sforge MCP server was stale since 2026-10-21 and failed
every `eval`; Peter restarted it, proposers resumed with full budget). Suggested (agents' own, dev, judge v1.4):
H-0012 partly (c-975db22244 r-20261023-034330-2669: R1 contact 3.06 vs van Leer 6.29, shock 2.92, N5/N6 converge);
H-0013 partly (c-2ca8842812 r-20261023-034337-d53f); H-0014 partly (c-920a251254 κ 0.6 r-20261023-035305-d9f5,
c-7246c9ff18 κ 0.3); H-0015 refuted (overshoot rises with THINC β: B-0010 0.026 / 0.058 / 0.087 at β 1.6 / 2.2 /
3.0); H-0016 refuted (B-0010 overshoot only −35 %, nozzle convergence lost); H-0017 partly (c-a4173db23e, S1 2.31).
Promo (docs/rounds/2026-10-23-round3/proposer_promo.txt): c-975db22244 **rejected** (LF1 1/5 hard constraints,
r-20261023-040031-554c); **c-2ca8842812 r-20261023-040314-a528 passes A1 (2.18), A2, A4, A6, A7a/b, A8a/b, B1, B2,
B5; fails only A3 (0.90) and A5 (NF3 roughness 0.077)**; c-920a251254 r-20261023-040946-4698 fails A1 (2.80), A5,
A7b. Tool gap: `promote --slot reconstruction_stateful` found no zoo references; fixed on the branch (0e9586b, merged:
Target A references always come from the limiter zoo, and promote prints them). Re-run without --slot gives the same
verdicts for c-2ca8842812; references: limiter/mc r-20261022-164508-76ad, limiter/van_albada r-20261022-164507-b391,
limiter/van_leer r-20261022-164508-7c66. **Van Leer check (2026-10-23): no inconsistency.** limiter/van_leer
r-20261022-164508-7c66 and limiter_stateful/van_leer r-20261022-164948-bba4 agree exactly: LF1 n = 5, contact_width
median 16.507, mean 15.723, p90 18.255 (n 5); per family LF1 5, LF2 5, NF1 20, NF2 10, NF3 5, RF1 20, RF2 10
instances, all pass rate 1.00, no violations. The "24.76" was the orchestrator's misreading: promote prints the A8a
threshold 1.5 × 16.507 = 24.76, not van Leer's value.
Islands: H-0013, H-0014, H-0012 (seeds = the three promo candidates). Evolve e-20261023-041826-802c started
06:18: gens 0–6 done (168 children, ~9 min per generation, $11.77), then paused on the usage limit in gen 6
(19 LLM errors); resumed with --resume. **Evolve finished 2026-10-24 00:29:** 20 generations, 480 children, archive
front 289; 29 rejected, 70 duplicates, 62 LLM errors (usage-limit pauses in gens 6, 12, 18; gen 18 lost all 24 to the
limit and still counts against the budget); cost $33.99 list (runs/round3-evolve.log). Leaderboard top 5
(`--pareto --vs-zoo`): c-58306b67e7 (H-0014 island, dev r-20261023-171400-1476, 0.489 × zoo), c-2637af56a6,
c-b799935c6b, c-954f644254 (H-0014, same dev numbers to 1e-9: R1 contact 3.16, shock 3.64, S1 1.94), c-140c60abbe
(H-0013). Promo + promote on these five (docs/rounds/2026-10-23-round3/evolve_promo.txt), S2 promo on the H-0012
island (s2_h0012_promo.txt), five breakers (breaker/*.md): see the round summary.
Target A gained A8 (long runs, LF1/LF2) on 2026-10-22, before round 3 (DECISIONS.md, docs/targets/A.md).
Evaluation slots K = 7.
Step 3d prerequisite done 2026-10-22 (WSL): pytest 264 passed; judge verify 49/49; worker peak RSS thinc_bvd
(reconstruction) 1.80 GiB / 160 s, muscl_van_leer_frozen (reconstruction_stateful) 1.76 GiB / 68 s, so the 2 GB
per-worker cap (K = 7, 12.6 of 15.5 GiB) still fits. Zoo v1.3: dev r-20261022-065926-0314 .. r-20261022-070148-7b30
(20 runs, all ok), promo r-20261022-070434-1135 .. r-20261022-071140-e7de (20 runs; superbee_frozen rejected 2/20
NF1 as under v1.2); limiter, stateful and flux scores unchanged from v1.2 (runs/zoo_dev_v13.txt, zoo_promo_v13.txt).
Rescore (scripts/rescore.sh, SKIP_ZOO=1 for the second slot): limiter 64 → 59 ok / 5 rejected, limiter_stateful
493 → 489 ok / 4 rejected; all 9 rejections were rejected under v1.2 too. 15 stateful candidates whose latest v1.2
run was not ok are ok now: 14 round-2 timeouts and 1 run left `running` by the timeout reproduction.
0. Judge v1.4 done 2026-10-22 (WSL, nothing else running). Branch merged (3de614a); pytest 269 passed, ruff clean.
   First registry open (schema-v2 indexes) 9.2 s, second 3.1 s; the limiter_stateful leaderboard that hung > 1800 s
   now answers in seconds. B-0002, B-0004, B-0010, B-0011 recorded as accepted by Peter (`case accept` needs a TTY).
   JUDGE_VERSION euler1d-v1.4 (71a3d94, tagged); judge verify 49/49. Zoo v1.4: dev r-20261022-163902-3046 ..
   r-20261022-164145-f56b (20, all ok), promo r-20261022-164507-7f58 .. r-20261022-165311-dc5d (20; superbee_frozen
   rejected, NF1 2/20, as under v1.2/v1.3). Rescore (dev): limiter 96 → 91 ok / 5 rejected, limiter_stateful
   493 → 489 ok / 4 rejected, reconstruction and reconstruction_stateful 0 candidates (runs/rescore_v14.log).
   **LF1/LF2 (held-out, v1.4 promo; LF1 shock / contact width median in cells, LF2 smooth order median / p90):**

   | | run | status | LF1 shock | LF1 contact | LF2 order |
   |---|---|---|---|---|---|
   | van_leer (reference) | r-20261022-164948-bba4 | ok | 3.35 | 16.5 | 1.97 / 1.96 |
   | van_leer_frozen | r-20261022-164957-2c18 | ok | 11.2 | 90.6 | 1.11 / 0.89 |
   | superbee_frozen | r-20261022-164737-d545 | rejected (NF1) | 11.2 | 90.4 | 2.32 / 2.06 |
   | muscl_van_leer_frozen | r-20261022-165311-dc5d | ok | – | 90.6 | 1.11 / 0.89 |
   | first_order (reconstruction) | r-20261022-165215-3367 | ok | – | 96.0 | 0.83 / 0.79 |
   | c-a84758f0e8 (ratchet seed) | r-20261022-193105-eeb2 | ok | 11.2 | 106.6 | −1.41 / −2.88 |
   | c-b5cb82a0ef | r-20261022-193422-b79e | ok | 11.2 | 111.2 | 0.26 / −0.54 |
   | c-fb8db52bca | r-20261022-193859-3650 | ok | 11.2 | 106.8 | −1.50 / −3.91 |
   | c-3e9a18586c | r-20261022-194241-014d | ok | 11.2 | 94.7 | −1.40 / −1.59 |

   Every frozen or ratcheted limiter is first-order-like on LF1 (contact ~90–111 cells vs 16.5 for van Leer, shock
   11.2 vs 3.35); on LF2 the frozen van Leer drops to order ~1, the round-2 ratchets to negative order (error grows
   with refinement), confirming the breakers' ψ = 0 lock-in on held-out data. All runs still pass the hard
   constraints (status ok), so LF hurts only via scores; whether LF becomes a promotion criterion is Peter's call
   (DECISIONS.md). Round-2 promo outputs: runs/round2_promo_v14.txt.
1. 3b: swarm test from WSL. (i) Red team: **closed 2026-10-22 (Peter, DECISIONS.md)** as "independent cheater
   agent not available (two classifier halts, v1.3 and v1.4)"; covered by structural defenses, regression tests,
   Target A8 and breakers; residual gaps: metric skipping and unanticipated attacks; revisit at gate 3e. (ii) Breaker done 2026-10-22 11:51–16:15
   (`run.sh breaker_ratchet.txt breaker-round2`, opus orchestrator + 3 breaker subagents, $16.03, judge v1.3).
   **15 cases quarantined, B-0001..B-0015** (cases/quarantine/, plus drafts/ with the probes they were cut from);
   none breaks every zoo member, so none is a hard case. Reports verbatim in docs/rounds/2026-10-22-breaker-round2/.
   Shared cause in all three reports: constant-state cells get r = 0 → φ = ψ = 0, the ratchet stores ψ = 0 at
   K0 there and at extrema, so those cells stay first order for the rest of the run. Main findings: smooth wave past
   K0 drops to order 0.31 / negative (B-0001, B-0002, all three candidates); explicit stall near critical back
   pressure in the Anderson nozzle (B-0005, B-0011..B-0013); K0 = 600 hits before the frozen zoo freezes
   (B-0007, B-0008, c-b5cb82a0ef only). B-0011/B-0012 may be merged (same stall, γ 1.2 vs 5/3). Side note:
   c-a84758f0e8 R1 mirror error 0.0188 vs ~1e-15 for the zoo. Peter accepted B-0002, B-0004, B-0010, B-0011
   (judge v1.4); B-0001, B-0003, B-0005..B-0009, B-0012..B-0015 stay in quarantine.
2. 3c done 2026-10-22 16:16–17:06: **H-0011 supported (for this family only)**. Dev sweep of
   phi = max(0, smin_10(s0 r, 1 + (c-1) tanh(r-1))), 30 points + the stateless bases of c-b5cb82a0ef and
   c-fb8db52bca (judge v1.3, r-20261022-141618-00a7 .. r-20261022-145146-bcea): no point meets R1 shock <= 2.6 and
   R1/R6 overshoot <= 1.1 x van Leer together (best corner ratio 1.22, s0 2 c 1.8); the family's sharpest shock is
   2.80 cells; the two round-2 bases are sharp (2.69 / 2.71) but overshoot ~3 x on R6. Promo + promote --target A
   on the three points nearest the corner, all not promoted: c-6711291203 r-20261022-145321-e725 (RF1 shock 2.72,
   A7a 0.049), c-b3897b3f5e r-20261022-145609-942b (2.85, 0.035), c-c04b63eb05 r-20261022-145855-58d9 (3.04, 0.032;
   A7b passes). None meets A1 or A7a; all three also miss A3 (NF1 explicit 0.50–0.55). Table, plot, promo output
   and the two base files: docs/rounds/2026-10-22-h0011/. Supports PLAN step 3d: sharpness has to come from a
   richer slot than phi(r). Caveat (cloud review): the dev threshold R1 shock <= 2.6 was too strict (dev R1 runs
   ~0.1 cell above the RF1 median; superbee itself is ~2.67 on dev), so the family never reached A1 on dev and
   the evidence rests on the three promo points and the two round-2 bases.
3. 3d: judge v1.3, red team, then round 3 on `reconstruction` with agent-written hunches. Measure worker RSS for
   the new slot first. Done on the branch (`euler1d-v1.3.dev`): reconstruction constraints (one 6-cell interface
   window per call; locality, grid size, position, constant state), THINC/BVD zoo member, the
   `reconstruction_stateful` slot (state layout of `limiter_stateful`; zoo `muscl_van_leer`,
   `muscl_van_leer_frozen`), probes, archive grids and objectives for both reconstruction slots. Cloud-registry
   dev checks only (not in the WSL registry): thinc_bvd r-20261022-054308-f275 (R1 shock 2.47, contact 2.65; N5/N6
   stall), muscl_van_leer_frozen r-20261022-054646-b2c7 = limiter_stateful van_leer_frozen r-20261022-054759-f751.
   Version bump, tag, zoo eval and rescore done (see State). Cheater pass (redteam_v13.txt) **not run**, see
   Blockers.
4. 3e: decision point with Peter after round 3; §11.4 kill criterion still applies (4 rounds / ~2,000 candidates).

## Blockers / questions for Peter
- *(Gate 3e answered 2026-10-24, DECISIONS.md.)* Open: the two zoo failures found by round-3 breakers (frozen van Leer
  on a parabolic nozzle, thinc_bvd on planar Noh) are not covered by D1–D5.
- *(3b(i) closed by Peter 2026-10-22, see DECISIONS.md; the two halts below are kept for the record.)*
- **Red team v1.4 did not run either** (2026-10-22 ~21:55–22:20, interactive WSL session, cheater subagent, task
  from redteam_v13.txt verbatim with folder candidates/redteam/v13/). A safety classifier stopped the cheater while it
  was planning attacks, after reading only the slot docs, sandbox.py and the judge sources: 0 files, 0 eval runs
  (docs/rounds/2026-10-22-redteam-v14-halted.md). The write-guard folder was not the cause (stop came before any
  write). Not resent reworded. 3b(i) stays open; judge v1.4 has not been red-teamed by an independent agent.
  Options for Peter: run the cheater himself interactively, or narrow the task (one concrete probe per run).
- **Red team v1.3 did not run** (2026-10-22 11:17–11:50, `run.sh redteam_v13.txt redteam-v13`, $1.10, 4 turns).
  A safety classifier stopped the cheater subagent before it wrote any file: 0 candidates, 0 eval runs, no
  LOG.md. All 12 planned attempts are "not attempted" (candidates/redteam-v13/REPORT.md, gitignored;
  runs/headless/redteam-v13.json). Not resent with reworded instructions. v1.3 is therefore not red-teamed. Options:
  resend unchanged, split by slot/idea, or run the cheater interactively. Side finding: the cheater's MCP
  `leaderboard` query for `limiter_stateful` timed out after 1800 s (the reconstruction one returned). The
  registry on /mnt/c is slow and needs a look before round 3.
- Round 2 questions answered 2026-10-22 (DECISIONS.md): A7 stays as written; breaker on all three candidates.
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
- Machine: 16 physical cores / 32 threads, 15.6 GB RAM in WSL → evaluation lock K = 7 (memory cap, 2 GB per worker;
  was 15). `limiter_stateful` dev worker: ~1.45 GB peak RSS, ~70 s alone; promo ~2.5–4.5 min alone.
- Round 2: 480 children, $25.71 list ($5.36 per 100); best held-out: c-b5cb82a0ef (RF1 2.58 / 5.11, NF1 expl 0.95).
- Dev suite 25.7 s per candidate alone; zoo dev ~70 s, zoo promo ~5 min wall (12 members in parallel).
- Engine (dummy backend): ~1.5 min per generation of 16 children on the dev suite.
- Zoo results: docs/judge/euler1d_baseline.md; Target A: docs/targets/A.md.
