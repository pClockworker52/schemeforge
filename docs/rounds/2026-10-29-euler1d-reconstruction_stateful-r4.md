# Round 4 — euler1d / reconstruction_stateful (2026-10-24 to 2026-10-29)

Last round of Phase 3 (stop rule: docs/plans/2026-10-24-round4.md §3.3). Judge `euler1d-v1.5` (8a8b830456a8),
integrity ok throughout. Raw outputs: docs/rounds/2026-10-24-round4/ (proposer reports, proposer_promo.txt,
evolve_leaderboard_top5.txt, evolve_promo.txt, h0019_table.txt).

## Result in one paragraph

No candidate is promoted for Target A or Target A-c. The closest one so far is the evolve child **c-4ece6bb6f7**
(H-0021 island). Its promo run is r-20261029-122317-32a7, and it fails only **A4** (NF1 converged_impl mean 0.85 < 1.00).
On the same run it passes A1 (shock 2.243), A5 (roughness 1.47e-5) and A7b (0.02507 vs 0.02559) together, plus every
bootstrap. A6 (1.915 vs 1.9) and A7b pass narrowly. c-82efea7caf (H-0022 island, r-20261029-122320-15bb) also fails
only A4 (0.75). H-0019's kill criterion is not met: no row in the evidence table, i.e. no candidate with NF1 Newton = 1.00,
is both sharp (≤ 2.6) and smooth (≤ 0.002). What has changed is where the conflict lies. Round 3 had sharp shocks
with a rough objective. Round 4 has candidates that are both sharp and smooth, but then Newton fails on some
held-out NF1 instances.

## Hunches (registered 2026-10-24; proposed verdicts, none closed)

| Hunch | Best candidate, run | Proposed verdict | Basis |
|---|---|---|---|
| H-0019 (contrarian, pre-registered) | — | supported for the families searched; mechanism in doubt | 0 kill rows (table below); but three promo runs show A1 + A5 together with Newton < 1, so "sharp ⇒ rough J" is not what blocks Target A in this family |
| H-0020 strength-inverse compression | c-cb9fe80826 r-20261024-202537-69d0 | refuted (dev) | dev clause 2: B-0010 overshoot +18.5 % over base (proposer report); promo part not run |
| H-0021 motion-gated compression | c-698b39759f r-20261024-210131-4dcc | refuted (promo) | promo clause: NF1 converged_impl mean 0.85 < 1.00; the island's best descendants (c-4ece6bb6f7 0.85, c-1a71c5a13b 0.90) show the same gap |
| H-0022 positivity scaling | c-9a3faab538 r-20261024-202309-21b3 | refuted as specified | clause (a): non-finite state on B-0030 with the hunch's ε, r-20261024-201321-dc41 (proposer report) |
| H-0023 history not sharpness | c-af3143be0c r-20261024-202133-76b1 | inconclusive (promo untested) | dev kill not met (N4 roughness 6.8e-4 with R1 2.475); not in the promo top 3, so no promo run |
| H-0024 diffused BVD weight | c-5ff53c2690 r-20261024-201845-0539 | inconclusive (proposer's call); could also be read as refuted (dev) | rejected on dev (B-0016, B-0030): no κ produced scores, so the dev clause "no κ reaches …" holds trivially. Peter's call |
| H-0025 characteristic WENO5-Z | c-47838d9365 r-20261024-205819-e795 | refuted (promo) | NF3 roughness_J p90 0.311 > 0.002 (Newton 1.00); dev N4 had 8.1e-6, a large dev → held-out gap |

## Engine (evolve e-20261028-220902-e988)

Islands H-0021 and H-0022, seeds candidates/H-0021/proposer/cand_1.py and candidates/H-0022/proposer/cand_3.py.
15 generations × 16 children = 240 (budget reached), Pareto front 200. 12–16 of 16 ok per generation. Rejections
were size (> 150 lines) and one shape error; no timeouts. Settings: sonnet, haiku for the wild operator,
SFORGE_MAX_PARALLEL=3.

Two failed attempts before it (DECISIONS 2026-10-28): e-20261028-201918-36b6 and e-20261028-212642-e595 rejected
16/16 in generation 0 with false timeouts. The cause was memory: this family peaks at 4.4 GB per worker
(r-20261028-220113-4600), and K = 7 assumes 2 GB. Smoke/dev timeouts were raised to 300/1500 s (commit d02255c),
and K = 3 is the fix. A Windows Update restart at 2026-10-29 03:34 killed the run during generation 6; it was resumed
from the saved state at 06:52 (`--resume`). The partly done generation 6 was redone.

## Promo and promote, top 5 of the leaderboard (`--pareto --vs-zoo --top 5`)

References for A: limiter/mc r-20261024-153251-db77, van_albada r-20261024-153252-8783, van_leer
r-20261024-153251-4a12 (A-c: van_leer only).

| Candidate | Origin | Promo run | Target A fails | Target A-c fails |
|---|---|---|---|---|
| c-4ece6bb6f7 | evolve, H-0021 | r-20261029-122317-32a7 | A4 0.85 | A4 |
| c-82efea7caf | evolve, H-0022 | r-20261029-122320-15bb | A4 0.75 | A4 |
| c-60c5ed6928 | evolve, H-0022 | r-20261029-122317-3b2e | A4 0.85, A7b 0.02899 | A4, A7b |
| c-1a71c5a13b | evolve, H-0021 | r-20261029-122321-9f52 | A4 0.90, A5 0.1643, A7b | A4, A5, A7b |
| c-47838d9365 | proposer, H-0025 | r-20261024-205819-e795 | A3 0.85, A5 0.3111, A7b 0.03139 | A3, A5, C1, A7b |

A1, A5 and A4 for the four evolve children (shock median, roughness p90, Newton mean): c-60c5ed6928 2.203 /
1.475e-5 / 0.85; c-4ece6bb6f7 2.243 / 1.471e-5 / 0.85; c-82efea7caf 2.267 / 1.474e-5 / 0.75; c-1a71c5a13b
2.211 / 0.1643 / 0.90. Full verdict blocks: docs/rounds/2026-10-24-round4/evolve_promo.txt.

## H-0019 evidence table

Every Arena 1 candidate or zoo member with an ok v1.5 promo run and NF1 converged_impl mean = 1.00
(scripts/h0019_table.py, read-only on the registry; output in h0019_table.txt):

| Candidate | Slot | RF1 shock median | NF3 roughness p90 | Promo run | Kill |
|---|---|---|---|---|---|
| c-47838d9365 | reconstruction_stateful | 2.256 | 0.311 | r-20261024-205819-e795 | |
| zoo venkatakrishnan | limiter | 2.944 | 0.00179 | r-20261024-153251-de6a | |
| zoo van_leer (c-38addf805f) | limiter | 2.945 | 0.00178 | r-20261024-153251-4a12 | |
| zoo van_leer | limiter_stateful | 2.945 | 0.00178 | r-20261024-153727-dffe | |
| zoo van_leer_frozen | limiter_stateful | 2.945 | 0.00178 | r-20261024-153732-c287 | |
| zoo hllc | flux | 2.945 | 0.00178 | r-20261024-153826-a803 | |
| zoo muscl_van_leer | reconstruction_stateful | 2.945 | 0.00178 | r-20261024-154024-c9f9 | |
| zoo muscl_van_leer_frozen | reconstruction_stateful | 2.945 | 0.00178 | r-20261024-154041-f18a | |
| zoo van_albada | limiter | 3.424 | 0.00146 | r-20261024-153252-8783 | |
| zoo van_albada | limiter_stateful | 3.424 | 0.00146 | r-20261024-153605-762c | |
| zoo minmod | limiter | 3.894 | 0.000871 | r-20261024-153251-0b76 | |
| zoo first_order | reconstruction | 11.015 | 0.00112 | r-20261024-153949-68d1 | |

Spearman ρ = −0.936, n = 12. This overstates the evidence. Six rows have identical scores (2.945 / 0.00178: van
Leer in three slots, its two frozen variants and zoo hllc), and van Albada appears twice. With one row per distinct score
pair (n = 6) ρ = −0.943, calculated by hand from the table. With n = 6 that carries little weight. The predicted ρ ≤ −0.5 is met, but that prediction was "reported, not
deciding". Only one non-zoo candidate reaches Newton = 1.00 on promo at all.

## Breakers, quarantine

Not run. The breaker agent needs the `sforge` MCP server, which did not connect from the desktop session
(2026-10-28/29). It starts cleanly in WSL. Run the breaker on c-4ece6bb6f7, c-82efea7caf and c-60c5ed6928 from a
WSL `claude` session (scripts/headless/round4.txt, last block). No cases quarantined this round.

## Cost

Evolve e-20261028-220902-e988: $20.34 (sum of the per-generation lines in the engine log). The two failed
attempts cost $2.04, and the killed 2026-10-24 run cost nothing (0 children). The LLM cost of the partial generation
6 lost in the restart is not in the engine log (see the `llm_calls` table if needed). Proposer and promo costs for
2026-10-24 are in STATUS.

## For the step-5 gate (Peter)

- Target A: not promoted. The nearest miss is c-4ece6bb6f7, which fails only A4 (Newton on 3 of 20 held-out NF1
  instances).
- A-c: not promoted. No candidate passes A4, which A-c also requires.
- By the pre-registered stop rule this leads to the negative-result note (docs/results/arena1-negative.md) and then
  Phase 6. A round 5 would need a new decision in DECISIONS.md.
- Open before writing the note: the breakers on the top 3, and Peter's call on H-0024.
