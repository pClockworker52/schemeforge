# Arena 1 (euler1d): no promotion on Target A after four rounds

Negative-result note required by PLAN §11.4 and the round-4 stop rule (docs/plans/2026-10-24-round4.md §3.3).
Written 2026-10-29 by the orchestrator, after round 4. Judge `euler1d-v1.5` (8a8b830456a8) unless a row says
otherwise. Every number cites a judge run; the per-round details are in docs/rounds/.

**Judge v1.6 (2026-10-30) changes no verdict here.** v1.6 adds three of the round-4 breaker cases to dev (B-0042,
B-0052, B-0054) and changes no code. Every zoo member's promo aggregates are identical under v1.5 and v1.6, and so
are its dev scores on the old cases (docs/judge/2026-10-30-v16-check.md). The verdicts here rest on promo runs, plus
A6 on the old dev case S1, so they hold under both versions. The candidates have not been rescored on v1.6 dev
(deferred, DECISIONS 2026-10-30).

## Result

Four rounds (2026-10-21 to 2026-10-29) searched four slots: `limiter`, `limiter_stateful`, `reconstruction_stateful`,
and the stateless `reconstruction` slot through the zoo and the 3c sweep. **No candidate is promoted for Target A**,
and none for the round-4 secondary target A-c. The registry holds 1,316 non-zoo candidates (95 limiter,
493 limiter_stateful, 728 reconstruction_stateful), 1,288 of them evaluated, with 3,492 dev and 228 promo runs.

The nearest miss is **c-4ece6bb6f7** (round 4, H-0021 island; promo r-20261029-122317-32a7). It passes 12 of 13
Target A checks, including sharp shocks (A1 2.243), a smooth steady objective (A5 1.47e-5), van-Leer-level overshoot
(A7b 0.02507 vs 0.02559) and all three bootstraps. It fails A4: Newton converges on 0.85 of the held-out NF1 nozzle
instances, where 1.00 is required.

Each round's best candidate failed on a different criterion of Target A. Taken together, the rounds show that its
criteria pull against each other in every scheme family that was tried. The results suggest that this
is structural, but they do not prove it for all schemes.

## What Target A asks

Target A (docs/targets/A.md, pre-registered 2026-10-20) asks for a scheme that is as sharp as superbee/MC/Koren on
moving discontinuities and as convergent and smooth as van Albada on steady nozzle flow:

- **A1, A2 (sharpness):** RF1 shock ≤ 2.6 cells, contact ≤ 6.5 cells.
- **A3, A4 (steady convergence):** NF1 explicit convergence ≥ 0.95 and Newton convergence = 1.00 of instances.
- **A5 (smooth objective):** NF3 roughness_J p90 ≤ 0.002.
- **A6 (accuracy):** S1 order ≥ 1.9 on dev.
- **A7 (overshoot):** ≤ 1.1 × van Leer on RF1 and RF2.
- **A8 (long runs):** added before round 3; it rules out state that drops a scheme to first order on long runs.
- **B1, B2, B5:** paired bootstraps against van Albada and MC.

No zoo member meets A1–A5 together.

## What was tried

| Round | Slot | Hunches | Engine | Best held-out result | What failed |
|---|---|---|---|---|---|
| 1 (10-21) | limiter φ(r) | H-0001..H-0004 (orchestrator) | e-20261021-045407-c003, 48 children | c-44f8015f87 r-20261021-050453-0b6a: soft min(2r, tanh cap) | A1 2.99, A2 6.60, A3 0.60, A7 |
| 2 (10-21/22) | limiter_stateful (one state value per cell) | H-0005..H-0010 (orchestrator) | e-20261021-123207-3146, 480 children | c-b5cb82a0ef r-20261022-060255-0a90: sharp base + one-way ratchet on ψ | A6 (S1 0.13), A7a/b (0.067 / 0.078); A1 2.58, A2, A3 0.95, A4 pass. Later A8 also rules out the ratchets |
| 3c (10-22) | limiter, sweep | H-0011 (contrarian) | 30-point family sweep | c-6711291203 r-20261022-145321-e725 (nearest corner) | no φ(r) in the family meets A1 and A7 together |
| 3 (10-22/24) | reconstruction_stateful | H-0012..H-0017 (hunch-generator agent) | e-20261023-041826-802c, 480 children | proposer c-2ca8842812 r-20261023-040314-a528 (THINC/BVD + flip lock); engine c-954f644254 r-20261023-223942-56d7 | proposer: A3 0.90, A5 0.077 (38 × the limit); engine: A1 3.41, A3 0.90, B1 |
| 4 (10-24/29) | reconstruction_stateful | H-0019 (pre-registered), H-0020..H-0025 (hunch-generator) | e-20261028-220902-e988, 240 children | c-4ece6bb6f7 r-20261029-122317-32a7 (motion-gated compression, evolved) | A4 0.85 only |

The engine used claude-cli (sonnet, haiku for the wild operator) with MAP-Elites islands seeded from the proposers'
best files. LLM cost recorded in the main registry (runs/registry.sqlite, `llm_calls`; calibration runs have
their own registry): $92.77 over 1,351 calls. Agent sessions (hunch-generator, proposers,
breakers) are not included; they ran on the subscription.

## Why it failed: one conflict, moved around

Each round removed one obstacle and exposed the next one:

1. **Sharpness vs overshoot (rounds 1–3c).** Within TVD limiters φ(r), sharp shocks come with overshoot above van
   Leer. H-0011 supports this for the family swept in 3c (docs/rounds/2026-10-22-h0011/). H-0015 extends it to THINC
   steepness: B-0010 overshoot rises with β, 0.0261 / 0.0580 / 0.0871 at β 1.6 / 2.2 / 3.0 (r-20261023-035530-454a,
   -034330-6b60, -034731-4dee). Round 2's sharp candidates overshoot 2–3 × van Leer.
2. **Steady convergence vs long-run accuracy (round 2).** Memory on the limiter factor fixes pseudo-time convergence.
   The one-way ratchet H-0006 converges explicitly on 20/20 held-out NF1 instances (promo r-20261021-122840-1c71).
   But that memory locks cells close to first order on long unsteady runs (LF1/LF2). Target A gained A8 for this
   before round 3; docs/targets/A.md lists LF2 order −1.5 to 0.26 for the round-2 ratchets.
3. **Sharp shocks vs a smooth steady objective (round 3).** Characteristic splitting (THINC on the entropy field
   only) gives sharp contacts without the overshoot. But in round 3 the steady objective was rough wherever the steady
   shock was sharp (c-2ca8842812, A5 0.077) and smooth only where the shock was wide (engine leaders, A5 1.7e-5 at
   A1 3.41). H-0019 was pre-registered to test this as the mechanism: a sharp steady shock snaps to sub-cell
   positions, which puts steps into J(p_b). It was not a general rule even then: the round-2 limiter c-b5cb82a0ef
   passed A1 (2.58), A4 (Newton 1.00) and A5 together on held-out data under judge v1.2 (r-20261022-060255-0a90), and
   failed on overshoot (A7) and smooth accuracy (A6, S1 order 0.13) instead. Under v1.5 it does so again
   (r-20261029-185257-3e4a), and so does c-fb8db52bca (r-20261029-185256-7cd3). The pre-registration's mechanism
   paragraph said the round-2 near misses all had roughness ≥ 0.077 or failed Newton; that was an orchestrator error
   at registration (see the H-0019 table below).
4. **Sharp + smooth vs Newton convergence (round 4).** Three evolved candidates pass A1 and A5 together on held-out
   data: c-60c5ed6928 (r-20261029-122317-3b2e), c-4ece6bb6f7 and c-82efea7caf (r-20261029-122320-15bb). All three
   fail A4, with Newton means of 0.85, 0.85 and 0.75. In this family a sharp steady shock does not force a rough
   objective; what fails is Newton on some nozzle instances. Across Arena 1, H-0019's kill criterion is met: the
   round-2 limiters c-b5cb82a0ef and c-fb8db52bca are sharp, smooth and Newton-convergent together on v1.5 promo
   (H-0019 table below), and pay with overshoot (A7) and long-run accuracy (A8). So the conflict is not between
   sharpness, smoothness and Newton as such; with overshoot and long runs added, no candidate has resolved it.

Whether the round-4 Newton failures come from one localised cause has not been checked. The held-out instances are
not readable here (CLAUDE.md rule 3). That would be the question for any further work on Target A. The round-4
breakers then proposed such NF1-regime cases without reading the held-out set (B-0037 … B-0056, see Limits): the
failures are spread over the nozzle regime, worst in low-Mach flow, rather than localised.

## H-0019 evidence table

Every Arena 1 candidate or zoo member with an ok v1.5 promo run and NF1 converged_impl mean = 1.00
(scripts/h0019_table.py; output in docs/rounds/2026-10-24-round4/h0019_table.txt). Kill criterion: RF1 shock
≤ 2.6 and NF3 roughness ≤ 0.002 on the same row.

| Scheme (slot) | RF1 shock median | NF3 roughness p90 | Promo run |
|---|---|---|---|
| c-47838d9365, characteristic WENO5-Z (reconstruction_stateful) | 2.256 | 0.311 | r-20261024-205819-e795 |
| **c-b5cb82a0ef**, round 2, H-0009 island (limiter_stateful) — **kill** | 2.581 | 0.00175 | r-20261029-185257-3e4a |
| **c-fb8db52bca**, round 2, H-0006 island (limiter_stateful) — **kill** | 2.582 | 0.00142 | r-20261029-185256-7cd3 |
| venkatakrishnan (limiter) | 2.944 | 0.00179 | r-20261024-153251-de6a |
| van Leer (limiter; also limiter_stateful, reconstruction_stateful, frozen variants, flux hllc: 6 rows, identical scores) | 2.945 | 0.00178 | r-20261024-153251-4a12 |
| van Albada (limiter; also limiter_stateful) | 3.424 | 0.00146 | r-20261024-153252-8783 |
| minmod (limiter) | 3.894 | 0.000871 | r-20261024-153251-0b76 |
| first order (reconstruction) | 11.015 | 0.00112 | r-20261024-153949-68d1 |

The table has **2 kill rows** (rerun 2026-10-29). Spearman ρ(shock, roughness) = −0.592 over the 14 rows (script),
or −0.714 over the 8 distinct rows above (from the printed values). That is still within the predicted ρ ≤ −0.5,
which was registered as reported, not deciding. Before the rerun it was −0.936 over 12 rows.

The rerun closes the gap the first version had: the round-2 limiters had no v1.5 promo runs, and two of them had met
the kill criterion's three conditions under judge v1.2 (r-20261022-060255-0a90, r-20261022-060626-894c). Their v1.5
promo runs are ok and keep those values. `sforge promote --target A` on each (2026-10-29):

| Candidate | Promo run (v1.5, ok) | A1 shock | A4 Newton | A5 roughness p90 | A3 expl | Fails |
|---|---|---|---|---|---|---|
| c-b5cb82a0ef | r-20261029-185257-3e4a | 2.581 | 1.00 | 0.00175 | 0.95 | A7a 0.0667 / A7b 0.0776 (vs 0.0241 / 0.0256), A8a LF1 contact 111 (vs 24.8), A8b LF2 order 0.26, A6 nan |
| c-fb8db52bca | r-20261029-185256-7cd3 | 2.582 | 1.00 | 0.00142 | 0.90 | A3, A7a 0.0550 / A7b 0.0840, A8a 107, A8b −1.50, A6 nan |

A6 reads nan because neither has a v1.5 dev run (latest dev: v1.4, r-20261022-192543-34c1 and r-20261022-191638-cfc9);
it does not enter H-0019. Both pass B1, B2 and B5.

**H-0019's kill criterion is met by both rows** (shock ≤ 2.6, roughness ≤ 0.002, Newton = 1.00, ok v1.5 promo run).
The suggested verdict is *refuted*: sharp, smooth and Newton-convergent together is possible in Arena 1, here by
one-way ratchets on the limiter factor, which buy it with overshoot 2–3 × van Leer and first-order long runs (A8).
Peter closes the hunch.

## The zoo front as a result

Promo aggregates of the zoo under judge v1.5. Members with identical scores in several slots are listed once.

| Member | Promo run | A1 shock | A2 contact | A3 expl | A4 Newton | A5 roughness p90 | RF1 / RF2 overshoot p90 |
|---|---|---|---|---|---|---|---|
| thinc_bvd (reconstruction) | r-20261024-154009-f309 | 2.182 | 2.918 | 0.35 | 0.65 | 0.0620 | 0.0193 / 0.0232 |
| weno5z (reconstruction) | r-20261024-154023-7489 | 2.350 | 4.312 | 0.65 | 0.65 | 22.2 | 0.0717 / 0.0696 |
| superbee (limiter) | r-20261024-153251-fc72 | 2.493 | 4.576 | 0.05 | 0 | 7.70 | 0.107 / 0.0915 |
| koren (limiter) | r-20261024-153251-5f10 | 2.529 | 6.370 | 0.55 | 0.25 | 17.6 | 0.0662 / 0.0531 |
| mc (limiter) | r-20261024-153251-db77 | 2.543 | 6.117 | 0.45 | 0.30 | 20.2 | 0.0601 / 0.0727 |
| hll (flux) | r-20261024-153824-a3d8 | 2.936 | 7.283 | 0.65 | 0.90 | 0.00179 | 0.0225 / 0.0241 |
| venkatakrishnan (limiter) | r-20261024-153251-de6a | 2.944 | 7.583 | 0.60 | 1.00 | 0.00179 | 0.0207 / 0.0284 |
| van Leer (limiter = hllc = muscl_van_leer) | r-20261024-153251-4a12 | 2.945 | 7.124 | 0.60 | 1.00 | 0.00179 | 0.0219 / 0.0233 |
| van Leer frozen (limiter_stateful) | r-20261024-153732-c287 | 2.945 | 7.124 | 0.85 | 1.00 | 0.00179 | 0.0219 / 0.0233 |
| van Albada (limiter) | r-20261024-153252-8783 | 3.424 | 8.416 | 0.95 | 1.00 | 0.00146 | 0.0136 / 0.0244 |
| rusanov (flux) | r-20261024-153939-d2af | 3.472 | 8.463 | 0.40 | 0.95 | 0.00184 | 0.0119 / 0.0162 |
| minmod (limiter) | r-20261024-153251-0b76 | 3.894 | 10.71 | 0.90 | 1.00 | 0.000871 | 0.0049 / 0.0294 |
| first order (reconstruction) | r-20261024-153949-68d1 | 11.01 | 46.0 | 1.00 | 1.00 | 0.00112 | 0.0031 / 0.0063 |

superbee_frozen's v1.5 promo run is rejected (r-20261024-153511-1da2). Under v1.5, koren and thinc_bvd are rejected
on dev (DECISIONS 2026-10-24) but have ok promo runs.

What the front shows:
- The zoo splits cleanly. Every member with shock ≤ 2.6 has Newton ≤ 0.65 and roughness ≥ 0.06. Every member with
  Newton = 1.00 has shock ≥ 2.94.
- The searched candidates fill in between. c-4ece6bb6f7 is sharper than every Newton-robust zoo member and has a
  lower roughness p90 than any zoo member (1.47e-5 vs minmod's 8.7e-4), at Newton 0.85. That is a point inside the gap, not past it.
- No candidate is labelled beyond "variant of" here. The closest candidates combine known pieces: characteristic
  THINC/BVD (Chamarthi 2024, per H-0012), van Albada/van Leer MUSCL, and stateful switching. None has been through
  an analyst or a referee.

## Every hunch verdict

Closed by Peter (gates 2–3e) unless marked *proposed*. Round-4 verdicts are proposals from
docs/rounds/2026-10-29-euler1d-reconstruction_stateful-r4.md; the ledger entries are still `open`.

| Hunch | Round, slot | Idea | Verdict |
|---|---|---|---|
| H-0001 | 1, limiter | smooth superbee (log-sum-exp) | refuted |
| H-0002 | 1, limiter | MC with smoothed kinks | refuted |
| H-0003 | 1, limiter | compressive below r = 1, flat above | inconclusive |
| H-0004 | 1, limiter | symmetric rational family van Albada ↔ van Leer | refuted (narrowly) |
| H-0005 | 2, limiter_stateful | exponential relaxation of ψ in pseudo-time | refuted |
| H-0006 | 2, limiter_stateful | one-way ratchet on ψ | supported; variant of limiter freezing (Venkatakrishnan 1995); A8 later rules out its use for Target A |
| H-0007 | 2, limiter_stateful | freeze each factor once settled | refuted |
| H-0008 | 2, limiter_stateful | dead-band hysteresis on ψ | inconclusive |
| H-0009 | 2, limiter_stateful | centred freeze after K steps on the round-1 leader | refuted |
| H-0010 | 2, limiter_stateful | relaxation towards superbee, clipped to TVD | refuted |
| H-0011 | 3c, limiter | no TVD φ(r) meets A1 and A7 together | supported for the swept family only |
| H-0012 | 3, reconstruction_stateful | THINC/BVD on the entropy field only | supported; rediscovery / variant of characteristic THINC on the linearly degenerate field |
| H-0013 | 3, reconstruction_stateful | flip-count lock on the BVD choice | inconclusive (6 of 8 grid points untested) |
| H-0014 | 3, reconstruction_stateful | entropy-production blend towards van Albada | refuted |
| H-0015 | 3, reconstruction_stateful | steeper THINC gives less overshoot | refuted |
| H-0016 | 3, reconstruction_stateful | MOOD-style flag on WENO5-Z | refuted |
| H-0017 | 3, reconstruction_stateful | κ = 1/3 quadratic in the BVD dictionary | refuted; variant of P_nT_m-BVD |
| H-0018 | 3, method | the agent swarm adds value (docs/targets/swarm.md) | supported weakly: S1 met, S2 met by 1 of 3 islands, ≤ 5 % |
| H-0019 | 4, all Arena 1 | no scheme with Newton = 1.00 is both sharp and smooth | *proposed:* refuted; kill criterion met by c-b5cb82a0ef (r-20261029-185257-3e4a) and c-fb8db52bca (r-20261029-185256-7cd3) on v1.5 promo (H-0019 table) |
| H-0020 | 4, reconstruction_stateful | strength-inverse compression | *proposed:* refuted (dev) |
| H-0021 | 4, reconstruction_stateful | motion-gated compression | *proposed:* refuted (promo, Newton 0.85); its island produced the nearest miss |
| H-0022 | 4, reconstruction_stateful | positivity scaling of face states | *proposed:* refuted as specified |
| H-0023 | 4, reconstruction_stateful | history, not sharpness, causes roughness | *proposed:* inconclusive (promo not run) |
| H-0024 | 4, reconstruction_stateful | diffused BVD weight (Barter–Darmofal transfer) | *proposed:* inconclusive or refuted; Peter's call |
| H-0025 | 4, reconstruction_stateful | characteristic WENO5-Z with Newton | *proposed:* refuted (promo roughness 0.311; dev had 8.1e-6) |

## Method results

- **Swarm (H-0018):** agent-written hunches were new ideas, not sweeps (S1). The engine improved on its seeds only
  weakly in round 3. In round 4 the engine, not a proposer, produced the nearest miss. That is one data point
  for S2, and it isn't scored against the round-3 criterion.
- **Crossover spreads one mechanism to every island** (rounds 2, 3, 4). Island results therefore say little about
  their own hunch. Verdicts were judged on the proposer runs.
- **Dev → held-out gaps are large.** Dev N1 explicit 1.00 became held-out 0.60 in round 1. H-0025 had dev
  roughness 8.1e-6 against promo 0.311. Promo before seeding islands is now part of the hunch-round skill.
- **Infrastructure cost runs.** False timeouts from memory pressure cost one round-2 readmission and two round-4
  restarts (DECISIONS 2026-10-28: 4.4 GB per worker vs the 2 GB the default parallelism assumes).

## Limits of this result

- **Families searched only.** Limiters φ(r), one-value stateful limiters, and characteristic MUSCL/THINC/WENO
  reconstructions with one state value were searched. Nothing here bounds other approaches, such as implicit
  shock fitting, sub-cell resolution with explicit shock tracking, or adjoint-consistent limiting.
- **Small held-out families.** NF1 has 20 instances, so A4 = 0.85 means 3 failures. The nearest misses could be
  closer to or further from A4 than that suggests.
- **Not red-teamed since judge v1.1.** Two cheater-agent runs (against v1.3 and v1.4) were stopped by safety
  classifiers (DECISIONS 3b(i)). Structural
  defences and breakers stand in for them (Peter's decision 3b(i)).
- **Breakers done on the round-4 top 3** (2026-10-29/30, docs/rounds/2026-10-29-round4-breakers.md): 20 cases in
  quarantine, B-0037 … B-0056; B-0042, B-0052 and B-0054 accepted into judge v1.6, the other 17 stay in
  quarantine. 17 break Newton convergence on steady nozzles where both stateful
  van Leer members converge, across geometries, γ 1.05–3 and N 60–240; the worst are low-Mach, weak-gradient flows,
  with or without a shock (c-60c5ed6928 0/5 on B-0047, 2/11 on B-0049, r-20261029-221507-59df, -233534-108c). All
  three already fail dev N2 (Newton 0/1). So the A4 gap of the nearest misses is a regime-wide weakness of the
  motion-gated family, not three unlucky held-out instances. Three cases (B-0053 … B-0055) show c-60c5ed6928
  overshooting up to 5.96 × van Leer on slowly moving strong shocks at γ 5/3 (r-20261029-235037-efff). The mechanism
  is suspected (motion gate on the previous iterate; ungated entropy-field BVD weight), not measured.
- **Not reviewed.** No analyst or referee has looked at any candidate, and nothing here is labelled "plausibly new".

## Next (PLAN §11.4, Phase 6)

1. ~~v1.5 promo runs of c-b5cb82a0ef and c-fb8db52bca, then the H-0019 table again~~ done 2026-10-29: 2 kill rows.
   Peter closes H-0019..H-0025 from the proposed verdicts and decides H-0024.
2. ~~Breakers on c-4ece6bb6f7, c-82efea7caf and c-60c5ed6928~~ done 2026-10-30: B-0037 … B-0056 in quarantine.
   Peter decides on them; any accepted case goes into the next judge version, followed by `sforge zoo eval` and an
   archive rescore.
3. Publish the judge, the zoo and the harness as a benchmark (PLAN §20), with this note and the ledger.
4. Phase 6. A round 5 on Target A needs a new decision in DECISIONS.md. The obvious candidate is A4 for
   c-4ece6bb6f7's family, approached through new NF1-regime dev cases (item 2 of the step above).
