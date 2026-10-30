# Breaker report: c-4ece6bb6f7 (H-0021 island, g012_003_refine.py), euler1d / reconstruction_stateful, judge euler1d-v1.5

Breaker agent report, saved by the orchestrator. Claims are the agent's; run ids are from its own evals (orchestrator
spot-checked six of them in the registry: candidate, status and judge version match). Eight cases proposed
(B-0037 … B-0044); none accepted; no code changed. Drafts B-17NN. 28 eval calls, one at a time; 147 k tokens, 2 h 05 min.
Orchestrator correction: the agent's opening paragraph says "7 cases (B-0037 to B-0043)"; it is 8 (B-0037 … B-0044),
as the agent notes under its own table.

## Summary

All proposed cases break the candidate's implicit Newton convergence on steady nozzles; on each one both stateful
zoo members converge on every back pressure (except B-0043, where muscl_van_leer_frozen crashes in its explicit run).
The weakness was already visible on dev: baseline r-20261029-102400-ed25 has Newton failing on N2 (0/1, 300 steps),
B-0011 (0.5) and N6 (0.67), where muscl_van_leer converges on all (1/1/1, r-20261029-191136-ba1c) and so does
frozen (r-20261029-191249-a225).

Aimed at A4, the only Target A check the candidate fails. NF1-like nozzle sweeps at N = 120 with other geometries and
γ fail on 9–36 % of back pressures; a coarse grid (N = 60), a fine one (N = 240) and an unchoked conical nozzle are
worse. So the 0.85 held-out NF1 rate is not a quirk of a few instances. The unsteady attack found nothing: shocks
moving at ~0.14 cells per step (inside the motion gate's transition band) are clean and better than van Leer.

Mechanism unknown (the judge reports only a converged share). Suspects from code reading:
- The entropy-wave amplitude always goes through the BVD/THINC blend (no motion gate), and the THINC `mono` switch
  and the smoothstep BVD weight are not smooth.
- The gate depends on the previous-step state S, which the solver updates after every Newton step, so the operator
  keeps changing as long as the iterate moves.

thinc_bvd / weno5z not run: every failure is Newton convergence on a MUSCL-type base, and those are
reconstruction-slot members, not stateful ones.

## Proposed cases

All `nozzle_sweep`, explicit + implicit. Implicit share converged / mean Newton steps; explicit share in brackets.

| Quarantine | Draft | Case | Candidate (run id) | Zoo on the same case (run ids) |
|---|---|---|---|---|
| B-0037 | B-1701_conical_g13_sweep | conical R 3, L 1.2, Ri 2, γ 1.3, N 120, 11 pbs 0.95…0.45 | impl 9/11, 147 [10/11] (r-20261029-190206-21a5) | vL 11/11, 103 [7/11] (r-20261029-191136-ba1c); frozen 11/11, 104 [10/11] (r-20261029-191249-a225) |
| B-0038 | B-1702_parabolic_g13_sweep | parabolic R 3, L 1.2, Ri 2, γ 1.3, N 120, 11 pbs 0.95…0.45 | impl 9/11, 132 [10/11] (r-20261029-191410-0bf1) | vL 11/11, 84 [9/11] (r-20261029-192322-14c5); frozen 11/11, 84 [11/11] (r-20261029-192436-7000) |
| B-0039 | B-1703_conical_r2_g14_sweep | conical R 2, L 1.0, Ri 3, γ 1.4, N 120, 14 pbs 0.92…0.53 | impl 9/14, 197 [14/14] (r-20261029-192609-c22a) | vL 14/14, 123 [11/14] (r-20261029-193600-ce42); frozen 14/14, 123 [13/14] (r-20261029-193726-cffd) |
| B-0040 | B-1704_conical_r2_unchoked | conical R 2 (as B-0039), γ 1.4, N 120, pbs 0.945…0.995 (unchoked) | impl 4/6, 192 [4/6] (r-20261029-193932-099b) | vL 6/6, 56 [4/6] (r-20261029-195250-b3d4); frozen 6/6, 56 [4/6] (r-20261029-195405-b6c9) |
| B-0041 | B-1705_parabolic_r5_g53_sweep | parabolic R 5, L 2, Ri 2, γ 5/3, N 120, 9 pbs 0.95…0.25 | impl 8/9, 116 [9/9] (r-20261029-195553-a539) | vL 9/9, 87 [9/9] (r-20261029-200455-ccaf); frozen 9/9, 87 [9/9] (r-20261029-200604-540c) |
| B-0042 | B-1707_anderson_n60_sweep | Anderson, γ 1.4, N 60, 11 pbs 0.95…0.25 | impl 6/11, 165 [9/11] (r-20261029-201644-c309) | vL 11/11, 43 [10/11] (r-20261029-202631-c516); frozen 11/11, 43 [10/11] (r-20261029-202732-d5b6) |
| B-0043 | B-1708_conical_r2_n240_sweep | conical R 2 (as B-0039), γ 1.4, N 240, 8 pbs 0.90…0.55 | impl 4/8, 274 [8/8] (r-20261029-202852-9769) | vL 8/8, 239 steps [7/8] (r-20261029-203948-101e); **frozen rejected**, explicit negative pressure (r-20261029-204151-7207) |
| B-0044 | B-1709_parabolic_n5geom_g115_sweep | parabolic (R 4, L 1.5, Ri 2.5), γ 1.15, N 120, 11 pbs 0.97…0.30 | impl 8/11, 148 [10/11] (r-20261029-204424-9a6a) | vL 11/11, 87 [8/11] (r-20261029-205337-9e5d); frozen 11/11, 87 [10/11] (r-20261029-205446-4a02) |

**Caveat on B-0043:** not a clean candidate-only weakness (frozen crashes explicitly, vL needs 239 of 300 Newton
steps); may be classified partly hard. Its point: refining N 120 → 240 makes the candidate worse (9/14 on B-0039,
4/8 here).

**Overlap:** no duplicates. Earlier nozzle cases cover Anderson near-throat (B-0005, B-0012, B-0013, B-0014), conical
R 3 near-throat at γ 1.4 (B-0015) and Anderson γ 1.2 (B-0011 accepted, B-0035).

**Back pressures:** critical pressures estimated by hand, so some end-of-sweep pbs may be unchoked or supersonic-exit;
the judge's exact solution covers every regime.

## Failure signature

- Newton runs out at 300 pseudo-time steps on 9–50 % of back pressures; mean step count 1.4–3.8 × the zoo's.
- The explicit solver mostly converges (B-0039 14/14, B-0041 9/9), often better than plain vL.
- Nothing crashes or goes non-physical on the candidate's side.
- Every geometry type (conical, parabolic, Anderson), every γ tried (1.15, 1.3, 1.4, 5/3), with and without a shock
  (unchoked B-0040); worse on coarser and finer grids. No near-miss variants: every nozzle sweep tried failed.

## Tried without a failure (not proposed)

- B-1706, Mach 3 shock (γ 1.4) into (1, −2.5, 1), ~0.14 cells/step: l1 1.08e-4, tv 0.039, width 1.91, overshoot
  9.3e-4 (r-20261029-200810-edfe); zoo not run.
- B-1710, Mach 10 shock into (1, −9, 1): l1 7.0e-4, tv 0.080, width 1.67, overshoot 7.1e-4 (r-20261029-205627-6a2b),
  better than vL on every metric (l1 7.7e-4, tv 0.132, width 1.81, overshoot 0.0178; r-20261029-210407-16c8).
- A first B-1710 draft (Δu given to 9 digits) returned an eval error without a run id; the agent's unverified guess is
  the judge's wave-speed check. Corrected before the run above.
- Sub-cell stationary shocks and the round-3 families not attacked (covered by B-0016, B-0033, B-0034, B-0036; the
  motion gate is off on a stationary shock).
