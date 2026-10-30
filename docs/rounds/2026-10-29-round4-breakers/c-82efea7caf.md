# Breaker report: c-82efea7caf (H-0022 island, g014_013_simplify.py), euler1d / reconstruction_stateful, judge euler1d-v1.5

Breaker agent report, saved by the orchestrator. Claims are the agent's; run ids are from its own evals (orchestrator
spot-checked six of them in the registry: candidate, status and judge version match). Seven cases proposed
(B-0045 … B-0051); none accepted; no code changed. Drafts B-18NN. 27 eval calls, one at a time; 162 k tokens, 1 h 05 min.

## Candidate and attack

MUSCL/THINC (BETA 1.6) blend on characteristic amplitudes with a BVD weight. The two acoustic fields also pass a
motion gate comparing each cell with its previous-step value (state `s` = previous W); the entropy field goes
through the BVD/THINC blend without a gate. Two hard switches: first-order fallback when a face goes non-positive,
and plain primitive MUSCL in strong expansions (Δu over two cells > a).

Dev already shows the weakness: N2 Newton 0/1 after 300 steps (r-20261029-120946-85b2), where muscl_van_leer
converges in 58 steps (r-20261029-211718-5f1b). Aimed at A4, in nozzle regimes the first breaker had not covered:
area ratio 8, inlet next to the throat and far upstream (`x_in`), very-low-Mach unchoked flow, γ 1.05 and 3, a long
gently diverging nozzle. Every one broke it; two non-nozzle probes did not. New sweeps are implicit-only, because
frozen's explicit solver crashed on the both-solver version of B-1801.

## Proposed cases

| Quarantine | Draft | Case | Candidate (run id) | Zoo on the same case (run ids) |
|---|---|---|---|---|
| B-0045 | B-1801_conical_r8_strong_shock_sweep | conical R 8, L 3, Ri 2, γ 1.4, N 120, 8 pbs 0.95…0.22, implicit | 6/8, 184 steps, roughness_J 0.0225 (r-20261029-212043-d909); both-solver version: same implicit, explicit 8/8 (r-20261029-211318-ebed) | vL 8/8, 140.6, roughness 4.1e-4, explicit 6/8 in both-solver run (r-20261029-211718-5f1b); frozen 8/8, 139.3 (r-20261029-211927-4da6), explicit crash (negative pressure) in both-solver run (r-20261029-211820-3f69, rejected) |
| B-0046 | B-1802_parabolic_inlet_near_throat_sweep | parabolic R 4, L 1.5, Ri 2.5, x_in 0.6 (inlet Mach ~0.6), γ 1.4, N 120, 12 pbs 0.95…0.40 | 9/12, 165.2 (r-20261029-212451-ef5b) | vL 12/12, 109.3 (r-20261029-212837-59d0); frozen 12/12, 109.4 (r-20261029-212950-435a) |
| B-0047 | B-1803_parabolic_very_low_mach_unchoked | parabolic R 4, L 1.5, Ri 2.5, γ 1.4, N 120, unchoked pbs 0.9995…0.993 (exit Mach ~0.03–0.1) | 3/5, 241.4 (r-20261029-213125-55f3) | vL 5/5, 66 (r-20261029-213505-d3f8); frozen 5/5, 66 (r-20261029-213558-fdd3) |
| B-0048 | B-1805_anderson_gamma105_sweep | Anderson, γ 1.05, N 120, 11 pbs 0.97…0.32 | 10/11, 125.9 (r-20261029-214114-4b5c) | vL 11/11, 97.9 (r-20261029-214456-f301); frozen 11/11, 97 (r-20261029-214559-ce93) |
| B-0049 | B-1806_conical_long_lowmach_inlet_sweep | conical R 3, L 1.2, Ri 2, x_in −2 (inlet area 10), γ 1.4, N 120, 11 pbs 0.95…0.45 | **5/11**, 203.6 (r-20261029-214730-b186) | vL 10/11, 79.2 (r-20261029-215119-d122); frozen 11/11, 71.3 (r-20261029-215216-00cd) |
| B-0050 | B-1807_conical_gamma3_sweep | conical R 3, L 1.2, Ri 2, γ 3, N 120, 10 pbs 0.94…0.32 | 9/10, 125.9 (r-20261029-215339-76e0) | vL 10/10, 93.8 (r-20261029-215720-2633); frozen 10/10, 93.8 (r-20261029-215823-6eb8) |
| B-0051 | B-1809_parabolic_long_gentle_sweep | parabolic R 2.5, L 4, Ri 2, γ 1.4, N 120, 11 pbs 0.95…0.46 | 7/11, 196.9, roughness_J 0.84 (r-20261029-220439-c44e) | vL 11/11, 122.1, roughness 0.0046 (r-20261029-220830-02fd); frozen 11/11, 122.1 (r-20261029-220936-ef7d) |

Caveats:
- B-0049: vL also misses one back pressure (10/11); frozen 11/11; candidate 5/11.
- B-0048, B-0050: mild breaks (one back pressure each).
- Back pressures estimated by hand; the judge's exact solution covers every regime.
- Checked against B-0001 … B-0044: no duplicates. New: area ratio 8, `x_in` offset both ways, unchoked below exit
  Mach 0.1, γ 1.05 and 3, L = 4.
- thinc_bvd / weno5z not run (stateless reconstruction-slot members; every failure is nozzle Newton convergence).

## Also fails on existing cases

- B-0039: implicit 10/14, 180.4 steps; explicit 14/14 (r-20261029-210904-2519). Zoo 14/14 for both (first
  breaker's runs r-20261029-193600-ce42, r-20261029-193726-cffd).
- Dev r-20261029-120946-85b2: N2 Newton 0/1; on N1 and N3 the explicit solver ends in a limit cycle at 8.4 and 8.5
  orders (vL N3 explicit 12.0 orders, r-20261029-211718-5f1b).

## Failure signatures

- Newton runs out at 300 steps on 9–55 % of back pressures; 1.3–3.7 × the zoo's mean Newton steps; roughness_J
  inflated in sweeps with failures (B-0045 0.0225 vs 4.1e-4; B-0051 0.84 vs 0.0046). No crash or violation on the
  candidate's side.
- Worst in low-Mach or weak-gradient flow: low-Mach inlet (B-0049, 5/11), very-low-Mach unchoked (B-0047, 3/5), long
  gentle divergence (B-0051, 7/11); matches dev N2.
- Untested hypothesis (code reading): the ungated entropy-field BVD/THINC weight with `mono` threshold
  (1e-12·ρ)² switches on very small entropy amplitudes; the motion gate depends on the previous Newton iterate, so
  the discrete operator changes between iterates.
- Extreme γ and strong shocks: milder (1–2 back pressures).

## Tried without a failure (not proposed)

- B-1804, conical R 3 (N6 geometry), supersonic exit, pb 0.1: explicit 12.0 orders, implicit 48 Newton steps, l1
  9.6e-5 (r-20261029-213728-c1f4); zoo not run.
- B-1808, double rarefaction (1, ∓0.65, 1), γ 1.4, t 0.25, N 200 (strong-expansion switch): l1 2.18e-3, tv 0.042
  (r-20261029-220008-0166), better than vL (l1 3.35e-3, tv 0.055; r-20261029-220340-8122).
