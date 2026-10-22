# Round 2 — euler1d / limiter_stateful, Target A (2026-10-21 … 2026-10-22)

Second hunch round (PLAN §11.3; closed as step 3a of §11.5). New slot `limiter_stateful` (judge `euler1d-v1.2`
throughout): `(φ, s′) = φ_s(r, s)`, one state value per cell and variable, updated after each step. Six hunches,
proposer sweeps, one engine run with 3 islands × 20 generations × 8 children (480 children).

**How it was run.** As in round 1, the orchestrator wrote and registered the hunches (author `orchestrator/<lens>`)
and implemented the proposer sweeps itself; no hunch-generator, proposer or breaker agent ran. The engine islands
used the `claude-cli` backend (sonnet, haiku for `wild`). The swarm itself is tested in step 3b. All hunches were
registered (`sforge hunch add`) before any of their candidates was evaluated.

## Hunches and verdicts

Base for the comparisons: round 1's tanh-cap limiter c-44f8015f87 as a stateless `limiter_stateful`
(dev r-20261021-123016-c10a: R1 shock 2.80, contact 5.46, N5 explicit 2/3, Newton 62).

| Hunch | Lens | Idea | Verdict | Evidence |
|---|---|---|---|---|
| H-0005 | steady-convergence | exponential relaxation of the centred factor ψ in pseudo-time | **refuted** | no w keeps the contact within 0.5 cells: w = 0.03 / 0.1 / 0.3 give 12.4 / 8.51 / 6.56 (r-20261021-121337-aa4c, -121336-1d7f, -121337-964d); all lose Newton on N1 (300 iterations). |
| H-0006 | contrarian | one-way ratchet on ψ after K0 steps: ψ = min(ψ(r), s) | **supported** | dev ties the centred freeze (N5 = N6 = 1, contact 5.46, Newton 62; r-20261021-121336-d8d5, -121442-ae91); held-out NF1 explicit 20/20 (promo r-20261021-122840-1c71) vs freeze 18/20 (r-20261021-122541-ac84). Label: variant of limiter freezing (Venkatakrishnan 1995). |
| H-0007 | practitioner | freeze each factor locally once it has settled | **refuted** | all four variants rejected on dev: non-physical state in the explicit solver on N1 and N5 (r-20261021-121517-62f1, -121519-766b, -121523-25a8, -121547-1b09). |
| H-0008 | approximation theory | hysteresis with a dead band d on ψ | **inconclusive** | kill criterion not met (d = 0.1: N5 = N6 = 1, r-20261021-121713-2521), but the prediction missed: contact 5.90 (+0.44), N1 explicit convergence lost, N4 roughness ×6; dominated by the ratchet. |
| H-0009 | transfer | centred freeze after K steps on the round-1 leader | **refuted** | dev N5 = N6 = 1 for K = 1000 / 2000, but both promo runs are rejected with 2 of 20 NF1 instances violating hard constraints (r-20261021-122541-ac84, r-20261022-060927-dc65), below the 0.95 kill line. |
| H-0010 | structure preservation | relaxation towards superbee, clipped to Sweby's TVD region every step | **refuted** | N5 explicit 0 for w = 0.05 and 0.2, superbee 1/3 (r-20261021-121845-f1c8, -122231-2562). |

## Engine run

`sforge evolve` e-20261021-123207-3146, islands H-0006, H-0009, H-0010, seeded with ratchet_k1000 (c-a84758f0e8),
freeze_tanhcap_k1000 (c-c455b124d8) and tvd_relax_w0p2 (c-0cdb29a87f); budget 480 children; stagnation stop never
fired. 480 children: 356 ok on dev on first evaluation, 90 rejected as timeouts (all ok when re-evaluated, see
below), 34 LLM errors (requests that never reached the model: subscription usage limit, gens 4–5, paused and resumed).
88 duplicates by fingerprint in the generation logs. Archive 25 cells at the end (14 before the readmission). Operators:
refine 231, crossover 102, explore 59, wild 45, simplify 43.

All three islands converged on one mechanism: a sharper stateless base φ(r) (tanh-cap variants, some blended
towards a smoothed superbee) plus the H-0006 ratchet after K0 = 600–1000 steps. The H-0009 and H-0010 islands
got there through crossover and explore; their own mechanisms (plain freeze, clipped relaxation) did not survive.

### Timeouts, readmission and the fix

- 90 children of the H-0006 and H-0009 islands (generations 1, 2, 3, 6, 9, 10; 15 per generation) were
  rejected with "timeout after 600 s". Re-evaluated alone, one at a time, on 2026-10-21/22: all 90 ok on dev
  (runs/round2_reeval.log; reports in runs/reeval/).
- **Cause, reproduced:** a `limiter_stateful` dev worker peaks at ~1.45 GB RSS; 15 parallel workers need ~22 GB on
  a 15.6 GB WSL machine. Starting 15 of the gen-9 children in parallel filled RAM and 4 GB of swap and all 15
  timed out at ~606 s. Whether a generation hit it depended on how many workers peaked at once.
  **Fix** (2fc0fa7): `max_parallel()` is now also capped at one worker per 2 GB of MemTotal (K = 7 here instead of
  15; `SFORGE_MAX_PARALLEL` still overrides). Generations 11–19 after the fix: 216 children, 0 timeouts.
- **Readmission** (`scripts/readmit_timeouts.py`, committed in 2fc0fa7 so the step can be repeated): a resumed run
  keeps false rejections out of its archive and islands, so each of the 90 was probed in the sandbox (smoke run with
  probes) and offered to the archive as `run_generation` does. Of the 90: **26 duplicates** (not placed) and
  **64 returned to their islands**. The 64 split by archive outcome into 5 new cells, 3 replaced elites and 56
  that the archive declined (they still join their island, as in a normal generation). 26 + 64 = 90. The state
  before the readmission is kept in `runs/evolve/e-20261021-123207-3146/state.before-readmit.json`, the
  per-child outcomes in `readmitted.jsonl` next to it, so the archive change is traceable.

### Cost

| Part | LLM cost (list price, subscription) |
|---|---|
| Generations 0–10 (2026-10-21) | $13.91 |
| Generations 11–19 (resume, 2026-10-22) | $11.81 |
| Whole run | $25.71 for 480 children ($5.36 per 100) |

**Overrun:** PLAN §11.5 step 3a estimated about $5 to finish the run; finishing cost $11.81 (9 generations ×
$1.19–1.48). $5 covers about 4 generations at that rate; the run went to the full 20 because the stagnation stop
never fired. Round 3 budgets should use ~$1.3 per generation of 24 children (sonnet + haiku) and ~35 min per
generation at K = 7 for this slot. Re-evaluation, readmission, the timeout reproduction and promo cost no LLM calls.

## Promo and Target A

Top three after the run (dev filter: explicit and Newton convergence on N1, N5, N6), then the held-out promo
suite and `sforge promote --target A --slot limiter_stateful`:

| Candidate | What it is | Dev (run) | Promo (run) | Target A |
|---|---|---|---|---|
| c-b5cb82a0ef (H-0009 island, explore) | tanh-cap blended 60 % towards smoothed superbee, clipped to TVD; ratchet after 600 steps | R1 shock 2.69, contact 3.94, overshoot 0.036 (r-20261022-051832-5d7d) | RF1 shock 2.58, contact 5.11; NF1 explicit 0.95, Newton 1.00 (r-20261022-060255-0a90) | not promoted: **A6** (S1 order 0.13) and **A7a/b** (overshoot 0.067 / 0.078 vs ≤ 0.024 / 0.026) fail; A1–A5, B1, B2, B5 pass |
| c-fb8db52bca (H-0006 island, crossover; leaderboard top, 1.120 × zoo) | tanh-cap with r-dependent cap amplitude; ratchet after 1000 steps | R1 2.71 / 4.49, overshoot 0.031 (r-20261022-044326-83d1) | RF1 2.58 / 5.81; NF1 explicit 0.90 (r-20261022-060626-894c) | not promoted: **A3** (0.90) and **A7a/b** (0.055 / 0.084) fail; A1, A2, A4–A6, B1, B2, B5 pass |
| c-3e9a18586c (H-0010 island, crossover) | clipped relaxation for 1000 steps, then ratchet | R1 2.66 / 4.44, overshoot 0.015 (r-20261022-010913-e65b) | RF1 3.41 / 8.24 (r-20261022-055754-c173) | not promoted: A1, A2, A6 (1.07), A7b, B1 fail; A7a passes (0.0240 vs 0.0241) |
| c-a84758f0e8 (round-2 seed, reference) | ratchet on the round-1 tanh-cap | — | RF1 2.99 / 6.60; NF1 explicit 1.00 (r-20261021-122840-1c71) | not promoted: A1, A2, A7a/b fail |

Leaderboard delta: the round moved the front. Two candidates now meet the sharpness criteria A1 and A2 on held-out
data with Newton converging everywhere and explicit convergence at 90–95 %. The ratchet seed met neither. What
stops them is **overshoot (A7)**: every candidate that is sharp enough overshoots 2–3× van Leer. The one candidate
with van Leer-level overshoot on RF1 (c-3e9a18586c) is not sharp on held-out data. Labels: variants of limiter
freezing on a superbee/MC-family base. Nothing here is a novelty claim.

## Lessons for the next round

1. **A7 is now the binding criterion, as §11.5 step 3c suspects.** Sharpness (A1, A2) and convergence (A3–A5) are
   each reachable with a ratchet, but not together with van Leer-level overshoot. 3c's feasibility sweep should
   include c-b5cb82a0ef's and c-fb8db52bca's bases as points.
2. Blending towards superbee costs smooth-order accuracy (c-b5cb82a0ef: S1 order 0.13, A6). Clipping at smooth
   extrema should be in the proposer prompt next to round 1's soft-max and `1/r` traps.
3. Dev is too lenient on overshoot and explicit convergence: dev ranks by R1 overshoot, while A7b is judged on
   RF2 (strong shocks), and dev N5/N6 = 1 coexists with 0.90 held-out (c-fb8db52bca). Check promo before seeding.
4. Islands do not keep their hunch's mechanism. Crossover spreads the best mechanism to every island, so the island
   result says little about the island's hunch. Verdicts above are judged on the proposer sweeps.
5. Memory, not CPU, limits parallel evaluation for stateful slots. Reconstruction (round 3) will need its own RSS
   measurement before choosing K.

## Open questions for Peter

- Should A7 (overshoot ≤ 1.1 × van Leer on RF1 and RF2) stay as written? The two near-misses fail only on A7 plus
  A6 or A3. Changing it is a target change and would be decided before any further promotion test, not after.
- Step 3b next (swarm test from a WSL session, with breaker on c-b5cb82a0ef and c-fb8db52bca instead of only
  c-a84758f0e8)?
