# Round 3 — euler1d / reconstruction_stateful, Target A and the swarm test (2026-10-22 … 2026-10-24)

Third hunch round and the swarm test of PLAN §11.5 step 3d (criterion pre-registered in docs/targets/swarm.md).
Judge `euler1d-v1.4` throughout (72b1b8daddcf). Run per scripts/headless/round3.txt from the interactive WSL session;
the headless run.sh session could not use the shell.

**Who did what.** Hunches: the **hunch-generator** agent (6 drafts, registered as written, author `hunch-generator/<lens>`).
Candidates: one **proposer** agent per hunch (≤ 8 evaluations each), then `sforge evolve` (claude-cli, sonnet; haiku
for `wild`). Attacks: one **breaker** agent per top-5 candidate. The orchestrator registered, evaluated promo, ran
evolve, and wrote this summary; it did not edit any agent hunch or candidate. No hunch is closed here: verdicts below
are suggestions for Peter.

Supporting files: docs/rounds/2026-10-23-round3/ (proposer_promo.txt, evolve_promo.txt, s2_h0012_promo.txt,
breaker/*.md); runs/round3-evolve.log (local).

## Hunches and suggested verdicts

Zoo dev references (judge v1.4): muscl_van_leer (reconstruction_stateful) r-20261022-164139-960f — R1 shock 2.92,
contact 6.29, B-0010 overshoot 0.0249, R6 overshoot 0.0151, S1 1.98, N5/N6 explicit 2/3 / 1. thinc_bvd
(reconstruction) r-20261023-035530-454a — R1 shock 2.47, contact 2.65, B-0010 0.0261, R6 0.0164, S1 1.96, N4
roughness 4.6e-4, N5/N6 explicit 1/3 / 0.

| Hunch | Lens | Idea | Agent's verdict | Suggested verdict | Evidence (dev unless stated) |
|---|---|---|---|---|---|
| H-0012 | shock physics | THINC/BVD only on the entropy characteristic field, van Leer MUSCL on the acoustic fields | partly | **supported** | c-975db22244 r-20261023-034330-2669: contact 3.06 (≤ 4.0), shock 2.91 (vL 2.92), B-0010 0.0203 and R6 0.0147 (≤ 1.1 × vL = 0.0274 / 0.0166), N5/N6 explicit 1/1 (vL 2/3, 1), S1 1.958: no kill clause fires. Promo r-20261023-040031-554c: LF1 contact median 2.89 (≤ 24.76, A8a clause passes), but **REJECTED, LF1 1 of 5 hard-constraint violation**. Prediction misses: B-0002 order 1.8995 (< 1.9 by 5e-4). Label: rediscovery / variant of characteristic THINC on the linearly degenerate field (Chamarthi 2024; the hunch's own known_relatives). |
| H-0013 | steady-convergence | count BVD choice flips, lock chattering cells to MUSCL, release on a decisive margin | partly | **inconclusive** | Only 2 of the 8 grid points run: (λ 0.9, S* 2, μ 0.3) c-2ca8842812 r-20261023-034337-d53f, N5/N6 explicit 2/3 / 1; (μ 0.1) c-735e50fb20 r-20261023-034911-0443, 1/3 / 2/3. Neither reaches N5 = N6 = 1; 6 grid points untested. Never-release (c-5edfe0f663 r-20261023-034619-b52c) is worse: N1/N6 limit cycles. Roughness prediction failed: N4 0.0109 is **≈ 24×** thinc_bvd's 4.6e-4 (the proposer wrote 2.4×). Promo r-20261023-040314-a528: best Target A result of the round (below). |
| H-0014 | structure preservation | blend thinc_bvd towards van Albada by the local Riemann problem's entropy production | partly | **refuted** | Kill clause needs R6 and B-0010 overshoot ≤ 1.1 × vL (0.0166 / 0.0274) with shock ≤ 2.75 and contact ≤ 3.0 for some κ ∈ {0.03, 0.1, 0.3}. R6 overshoot misses at every κ run: 0.1 → 0.0199 (r-20261023-034338-fe5a, also shock 3.48), 0.3 → 0.0196 (r-20261023-034637-3074, shock 2.90), 0.6 (off-grid) → 0.0190 (r-20261023-035305-d9f5). κ 0.03 not run (the trend makes shocks wider). The proposer did not check R6. Structural claim held (S1 1.958 at every κ). |
| H-0015 | contrarian | steeper THINC gives narrower and less oscillatory shocks | refuted | **refuted** | B-0010 overshoot rises with β: 0.0261 / 0.0580 / 0.0871 at β 1.6 / 2.2 / 3.0 (r-20261023-035530-454a, -034330-6b60, -034731-4dee); R6 0.0164 / 0.0171 / 0.0327. Extends H-0011 from TVD limiters to THINC profiles. |
| H-0016 | transfer | MOOD-style one-step-late admissibility flag on WENO5-Z | refuted | **refuted** | c-0f73739944 r-20261023-034330-6cdf: B-0010 0.0448 (−35 % vs weno5z's 0.0684, still 1.8 × vL); N1 Newton 300, limit cycle (weno5z 83). cand_2 r-20261023-034700-8de8 the same. Second kill clause (flag-every-jump control) not run. |
| H-0017 | approximation theory | add a κ = 1/3 quadratic to thinc_bvd's BVD dictionary | partly | **refuted** | c-a4173db23e r-20261023-034424-bc55: S1 2.31 (kill line 2.3, prediction 2.6), but B-0010 0.0367 > 1.2 × thinc_bvd's 0.0261 = 0.0313 and R6 0.026 > 1.2 × 0.0164 = 0.0197: the overshoot clause fires (the proposer did not look up the thinc_bvd values). Label: variant of P_nT_m-BVD. |

Corrections to agent reports: (1) the H-0013 proposer called N4 roughness 0.0109 "2.4×" thinc_bvd; it is ≈ 24×. (2) The
H-0014 proposer cited r-20261023-034337-d53f as its thinc_bvd reference; that run is H-0013's c-2ca8842812 (it matches
thinc_bvd's widths, not its overshoot: 0.0241 vs 0.0261). thinc_bvd's v1.4 dev run is r-20261023-035530-454a. (3) The
H-0014 and H-0017 proposers did not check the overshoot clause of their kill criteria; with it, both are refuted.

## Proposers → promo → islands

Promo + `promote --target A` on the best three proposer candidates (docs/rounds/2026-10-23-round3/proposer_promo.txt;
references limiter/mc r-20261022-164508-76ad, limiter/van_albada r-20261022-164507-b391, limiter/van_leer
r-20261022-164508-7c66):

| Candidate | Promo run | A1 | A2 | A3 | A4 | A5 | A6 | A7a | A7b | A8a | A8b | B1 B2 B5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c-2ca8842812 (H-0013) | r-20261023-040314-a528 | **2.18** ✓ | 2.92 ✓ | 0.90 ✗ | 1 ✓ | 0.0765 ✗ | 1.956 ✓ | 0.0216 ✓ | 0.0239 ✓ | 2.95 ✓ | 1.96 ✓ | ✓ ✓ ✓ |
| c-920a251254 (H-0014 κ 0.6) | r-20261023-040946-4698 | 2.80 ✗ | 3.10 ✓ | 0.95 ✓ | 1 ✓ | 0.0190 ✗ | 1.958 ✓ | 0.0176 ✓ | 0.0314 ✗ | 2.77 ✓ | 1.97 ✓ | ✓ ✓ ✓ |
| c-975db22244 (H-0012) | r-20261023-040031-554c | REJECTED: LF1 1 of 5 instances violate hard constraints; promote does not run |

c-2ca8842812 is the first candidate in three rounds to pass A1, A2, A6, A7a/b and A8 together on held-out data. It
fails only A3 (NF1 explicit 0.90) and A5 (NF3 roughness 0.077, 38 × the bound).

Islands: H-0013, H-0014, H-0012, seeded with these three files.

## Engine run

`sforge evolve` e-20261023-041826-802c: 3 islands × 20 generations × 8 children, budget 480. Finished 2026-10-24 00:29.

| | |
|---|---|
| children | 480 (20 generations × 24) |
| rejected on dev | 29 |
| duplicates (fingerprint) | 70 |
| LLM errors | 62: usage-limit pauses in gens 6 (19), 12 (18), 18 (24, the whole generation), 1 other; each pause resumed with `--resume` |
| archive front at the end | 289 (MAP-Elites grid: 6 elites) |
| cost | $33.99 list (subscription) = $7.08 per 100 children; $8.13 per 100 children that reached the model (418) |
| wall clock | ~9 min per generation at K = 7 |

**What the islands converged on.** As in round 2 (lesson 4), crossover spread one mechanism to every island: H-0012's
characteristic split (THINC/BVD on the entropy field, van Albada on the acoustic fields), with a smooth (Lipschitz)
BVD weight and, in most H-0013/H-0014 descendants, H-0013's flip-counting lock. H-0014's entropy-production weight
did not survive in the leading candidates. The islands' results therefore say little about their own hunches;
verdicts above are judged on the proposer runs.

**Leaderboard** (`--pareto --vs-zoo`): top five all rank 0, 0.489–0.492 × zoo: c-58306b67e7, c-2637af56a6,
c-b799935c6b, c-954f644254 (H-0014 island), c-140c60abbe (H-0013 island). Four of the five give the same promo
aggregates to three digits; they are one scheme in four spellings. Against the zoo they trade a much sharper contact
(R1 0.50 × zoo) for a wider shock (R1 1.25 × zoo, 3.64 cells; c-58306b67e7 dev r-20261023-171400-1476).

### Promo and Target A, top five (docs/rounds/2026-10-23-round3/evolve_promo.txt)

| Candidate | Promo run | A1 | A2 | A3 | A4 | A5 | A6 | A7a | A7b | A8a | A8b | B1 | B2 | B5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c-58306b67e7 | r-20261023-223047-396c | REJECTED: NF1 3/20, NF2 1/10, NF3 1/5 instances violate hard constraints; promote does not run |||||||||||||
| c-2637af56a6 | r-20261023-223342-7d47 | 3.41 ✗ | 3.07 ✓ | 0.90 ✗ | 0.95 ✗ | 1.7e-5 ✓ | 1.939 ✓ | 0.0049 ✓ | 0.0255 ✓ | 2.84 ✓ | 1.96 ✓ | ✗ | ✓ | ✓ |
| c-b799935c6b | r-20261023-223643-b06a | 3.41 ✗ | 3.07 ✓ | 0.90 ✗ | 0.95 ✗ | 1.7e-5 ✓ | 1.939 ✓ | 0.0049 ✓ | 0.0255 ✓ | 2.84 ✓ | 1.96 ✓ | ✗ | ✓ | ✓ |
| c-954f644254 | r-20261023-223942-56d7 | 3.41 ✗ | 3.07 ✓ | 0.90 ✗ | 1 ✓ | 1.7e-5 ✓ | 1.939 ✓ | 0.0049 ✓ | 0.0255 ✓ | 2.84 ✓ | 1.96 ✓ | ✗ | ✓ | ✓ |
| c-140c60abbe | r-20261023-224257-ef55 | 3.41 ✗ | 3.07 ✓ | 0.90 ✗ | 1 ✓ | 1.6e-4 ✓ | 1.939 ✓ | 0.0078 ✓ | 0.0255 ✓ | 2.84 ✓ | 1.96 ✓ | ✗ | ✓ | ✓ |

Thresholds: A7a ≤ 0.02411, A7b ≤ 0.02559, A8a ≤ 24.76; B1 fails at ratio 0.991, CI [−0.024, +0.000]. Nothing is
promoted. The engine's leaders fix A5 (roughness 1.7e-5 vs the seed's 0.077) and halve A7a, but lose A1: their RF1
shock median is 3.41, against 2.18 for the H-0013 seed. The leaderboard's scalar `vs zoo` score rewards the contact
gain more than it penalises the shock loss.

## Breakers (top five, ≤ 10 cases each; reports in docs/rounds/2026-10-23-round3/breaker/)

21 cases proposed to quarantine, B-0016 … B-0036; none accepted. Grouped by failure (the agents' claims, with their run ids
in the reports):

| Failure | Cases | Candidates hit | Zoo on the same case |
|---|---|---|---|
| LeBlanc tube at N 400: contact never completes (width = full window 45 vs van Leer 18.9) | B-0021 (N 450: 21.9 vs 18.1), B-0025, B-0029, B-0032, B-0036 | all five | van Leer completes; at N 800 the gap closes (19.4–19.7 vs 18.3) |
| Cold symmetric collision, γ 1.4, p ≤ 1e-4: non-finite state | B-0016, B-0017 (γ 1.2), B-0026, B-0027, B-0028, B-0034 | c-b799935c6b, c-954f644254, c-140c60abbe; c-58306b67e7 survived planar Noh at p 1e-6 / 1e-10 (r-20261023-230542-2fef, -230754-5686) | both van Leer members ok; zoo thinc_bvd also NaN |
| Unit scaling: absolute EPS = 1e-20 in THINC switches it off at ρ, p × ≤ 1e-9 | B-0019, B-0022, B-0023, B-0024 | c-b799935c6b, c-58306b67e7 tested; all five top candidates contain `EPS = 1e-20` | van Leer invariant; zoo thinc_bvd has the same EPS and fails the same way |
| Double rarefaction across a 10:1 step, Δu ≥ 4.2: non-finite state | B-0030, B-0031 | c-2637af56a6 | van Leer ok; thinc_bvd NaN; weno5z NaN on B-0031 only |
| Low-γ blast (R3 states, γ ≤ 1.15): non-finite state | B-0018 | c-b799935c6b | van Leer ok |
| Collision at γ 5/3: TV increase 2.5 × van Leer | B-0020 | c-b799935c6b | — |
| Stationary Mach 20 shock not preserved (round-off amplified) | B-0033 | c-2637af56a6 | van Leer and thinc_bvd exact; weno5z fails too; with rounded inputs van Leer drifts as well |
| Anderson nozzle γ 1.2, nine back pressures: Newton 3/9 | B-0035 | c-140c60abbe | van Leer 9/9 |

Common cause suggested by three breakers independently (code reading, not judged): the characteristic back-projection
at the centre cell, with separately limited acoustic amplitudes, has no positivity guarantee. Two zoo failures were
found along the way and **not** proposed: muscl_van_leer_frozen negative pressure on a parabolic nozzle at N 240
(r-20261023-225103-d50b), thinc_bvd NaN on planar Noh (r-20261023-230653-0866).

Breaker agents' token use: 88 k, 91 k, 121 k, 138 k, 165 k (subscription; no list price recorded).

## Swarm criterion (docs/targets/swarm.md)

### S1, new ideas: **met** (suggested; Peter decides from the ledger text)

H-0001 … H-0011 are all limiter functions φ(r) or states on a limiter factor. None of the round-3 hunches only changes
constants or the base limiter of one of them:

| Agent hunch | Nearest earlier hunch | Difference |
|---|---|---|
| H-0012 | H-0003 (compressive branch for contacts) | acts per characteristic field in the reconstruction, with THINC on the linearly degenerate field only; not a φ(r) |
| H-0013 | H-0008 (dead-band hysteresis) | counts flips of a discrete BVD choice and locks/releases on the BVD margin, not on the limiter value |
| H-0014 | H-0004 (structure-preserving rational family) | weight from the entropy production of the local Riemann problem; no earlier hunch uses entropy |
| H-0015 | H-0011 (sharpness forces overshoot for TVD φ) | claims the opposite outside the TVD family, for THINC steepness |
| H-0016 | H-0007 (local freeze once settled) | a posteriori maximum-principle check against the previous step (MOOD transfer) on WENO5-Z |
| H-0017 | H-0001 (smooth superbee) | enlarges the BVD dictionary with a third-order polynomial |

Known-method labels apply (H-0012 rediscovery/variant of characteristic THINC, H-0017 variant of P_nT_m-BVD); S1 is
about sweeps, not novelty.

### S2, the engine improves on its seeds: **met on one island of three** (suggested)

(a) Dev non-dominance against the seed and better on at least one objective (engine/objectives.py): 22 of 22 H-0013,
22 of 22 H-0014 and 20 of 21 H-0012 final island members meet it (script: scratchpad, not committed; seed dev runs
r-20261023-034337-d53f, r-20261023-035305-d9f5, r-20261023-045157-26d7). (a) is weak; (b) decides.

(b) Promo within 2 % of the seed or better on A1–A5, A7a, A7b:

| Island | Seed (promo run) | Elites checked on promo | Result |
|---|---|---|---|
| H-0013 | c-2ca8842812 (r-20261023-040314-a528) | c-140c60abbe r-20261023-224257-ef55 | ✗ A1 3.41 vs 2.18, A2 3.07 vs 2.92, A7b 0.0255 vs 0.0239. Dev screen: no island member within 2 % of the seed's R1 shock (2.475) and contact (2.65) |
| H-0014 | c-920a251254 (r-20261023-040946-4698) | c-2637af56a6, c-954f644254, c-58306b67e7 (runs above) | ✗ A1 3.41 vs 2.79, A3 0.90 vs 0.95 (c-2637af56a6 also A4). Dev screen: no member within 2 % of the seed's R1 shock (2.70) and contact (2.64) |
| H-0012 | c-975db22244 (r-20261023-040031-554c) | all 20 members that meet (a) (s2_h0012_promo.txt, evolve_promo.txt) | ✓ **c-a411e8accb** r-20261023-232730-c8f5 (wild child, smooth BVD weight): A4 1.00 vs 0.95, A7b 0.0236 vs 0.0250, A7a 0.0066 vs 0.0068, the rest within 0.1 %. ✓ c-c0644880db r-20261023-230405-e34b and c-0428b6020b r-20261023-232157-60f3 (identical numbers): A7a 0.0067 vs 0.0068, rest within 2 %; dev S1 1.98 vs 1.958, B-0002 1.908 vs 1.8995, Newton 64 vs 67. 16 others fail one of A3/A4/A5/A7a |

Caveats for the gate: (1) the improvements are small (≤ 5 % on promo); the H-0012 island stayed close to its seed.
(2) Every H-0012 elite, like the seed, is REJECTED on promo for one LF1 hard-constraint violation; S2 does not require
an accepted promo run, but none of them can be promoted. (3) c-64b8c61c53 also passes (a) and (b) but is a refactor of
the seed whose dev numbers differ by ≤ 3e-8 relative (r-20261023-043502-a273); it is not counted. (4) For H-0013 and
H-0014 only the leaderboard elites were run on promo; the "no" rests on those plus the dev screen, not on promo runs of
every member.

swarm.md asks for the outcome to be recorded as a closed ledger hunch (author `orchestrator/method`). round3.txt says
not to close hunches, so this is left to Peter.

### Numbers to report

| Quantity | Round 1 (orchestrator) | Round 3 (agents) |
|---|---|---|
| hunches registered / refuted / inconclusive / supported | 4 / 3 / 1 / 0 | 6 / 4 / 1 / 1 (suggested, above) |
| engine children / duplicates | 48 / 6 | 480 / 70 (plus 29 rejected, 62 LLM errors) |
| islands whose elite meets S2 | not measured | 1 of 3 (H-0012: c-a411e8accb, c-c0644880db/c-0428b6020b) |
| list price per 100 candidates | $5.6 | $7.08 (engine only, $33.99 / 480; agents not metered) |
| cases quarantined by breakers | 0 (breaker not run) | 21 (B-0016 … B-0036) |

## Lessons for the next round

1. **The best Target A candidate came from a proposer, not the engine.** c-2ca8842812 (H-0013 proposer) passes A1, A2,
   A6, A7 and A8 on held-out data; the engine's leaders all lose A1. The leaderboard's `vs zoo` score ranks a 0.5 ×
   contact gain above a 1.25 × shock loss; selection should not use the scalar score for Target A work.
2. **Top-k by leaderboard picks duplicates.** Four of the five promo/breaker slots went to one scheme. Deduplicate the
   top k by promo-level behaviour (or fingerprint) before spending breakers.
3. **Positivity is the shared hole.** Nine crash cases (B-0016/17/18, B-0026/27/28, B-0030/31, B-0034) across four candidates; van Leer survives all
   of them. Three breakers point at the characteristic back-projection; the zoo thinc_bvd, which has no
   characteristic projection, also crashes on several, so THINC may contribute (not diagnosed). A positivity fallback
   belongs in the proposer traps.
4. **THINC's absolute EPS is inherited from the zoo.** The dev metamorphic scaling check (×10) does not catch it.
   Whether the judge's scaling check should use a larger factor is a judge question for Peter, not for this round.
5. **Proposers skip reference lookups.** Two of six did not check the overshoot clause of their own kill criterion,
   and both turn out refuted. The proposer prompt should require every kill-criterion number with a run id.
6. **Usage limits cost a whole generation.** Gen 18 lost all 24 requests and still counted against the budget.

## Open questions for Peter (gate 3e)

- S1 met? S2 met on the strength of one island with small gains (caveats above)? Record the swarm outcome as a ledger
  hunch?
- The suggested verdicts: close H-0012 supported, H-0013 inconclusive, H-0014/15/16/17 refuted?
- 21 quarantined cases (several duplicates by mechanism: LeBlanc ×5, cold collision ×6, scaling ×4). Which to accept?
  And the two zoo failures found along the way?
- Next: c-2ca8842812 fails only A3 and A5. A proposer round on its roughness (A5) with a positivity fallback, rather
  than another engine run?
