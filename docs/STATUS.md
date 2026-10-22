# STATUS
Phase: 3 — Production search, Arena 1 (started 2026-10-21)  Judge version: euler1d-v1.4 (2026-10-22, 71a3d94)  Plan: v1.2
Last session: 2026-10-22 — step 3a done: round 2 closed (docs/rounds/2026-10-21-euler1d-limiter_stateful.md)

## Gate 1 — passed 2026-10-20
Blind audit (audit/euler1d/REPORT.md): 1,002 random instances agree to 6.5e-13; the one judge bug it found
(p_b within rounding of p_crit2) is fixed. Peter's decisions: Roe dropped, Target A thresholds accepted
(docs/targets/A.md), Target B and Venkatakrishnan K > 0 later. Judge tagged `euler1d-v1.0`; zoo re-evaluated.

## Latest results (2026-10-22): round 2 closed (PLAN §11.5 step 3a)
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
State: judge euler1d-v1.4 on main (71a3d94, tagged); round 2 closed; H-0011 closed; no open hunch. Peter's review
2026-10-22 (DECISIONS.md "Judge v1.4"): accept B-0002, B-0004, B-0010, B-0011; add held-out long-run families LF1,
LF2. **Step 0 done 2026-10-22 (see below). 3b(i) closed without an independent cheater (DECISIONS.md). Round 3 next.**
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
