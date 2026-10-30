# Round 4 breakers: c-4ece6bb6f7, c-82efea7caf, c-60c5ed6928 (euler1d / reconstruction_stateful)

2026-10-29/30, judge `euler1d-v1.5` (8a8b830456a8), no judge change. One breaker agent per candidate, one after the
other, ≤ 10 cases each, every eval strictly sequential (the sforge MCP server ran without SFORGE_MAX_PARALLEL, so the
breakers were told to call eval one at a time; nothing else was evaluating). Reports, saved by the orchestrator:
docs/rounds/2026-10-29-round4-breakers/<id>.md. Claims are the agents'; the orchestrator spot-checked six run ids per
report in the registry (candidate, status, judge version match).

**20 cases proposed to quarantine, B-0037 … B-0056; none accepted (Peter reviews).** Drafts B-17NN, B-18NN, B-19NN in
cases/quarantine/drafts/ (31 drafts, 11 not proposed).

| Candidate | Promo (Target A) | Cases | Eval calls | Agent tokens / wall time |
|---|---|---|---|---|
| c-4ece6bb6f7 (H-0021 island) | r-20261029-122317-32a7, fails A4 0.85 | B-0037 … B-0044 (8) | 28 | 147 k / 2 h 05 |
| c-82efea7caf (H-0022 island) | r-20261029-122320-15bb, fails A4 0.75 | B-0045 … B-0051 (7) | 27 | 162 k / 1 h 05 |
| c-60c5ed6928 (H-0022 island) | r-20261029-122317-3b2e, fails A4 0.85, A7b | B-0052 … B-0056 (5) | 34 | 236 k / 2 h 23 |

Agent sessions ran on the subscription (no list price recorded).

## Cases by failure mechanism

"vL" is the stateful zoo member `reconstruction_stateful/muscl_van_leer`, "frozen" is `muscl_van_leer_frozen`.
Nozzle numbers: implicit (Newton) share converged / mean Newton steps, 300-step limit.

### 1. Newton stalls on steady nozzle shock sweeps (A4 regime, other geometries, γ and grids)

| Case | Setup | Candidate (run id) | van Leer (run id) | Frozen |
|---|---|---|---|---|
| B-0037 | conical R 3, γ 1.3, N 120, 11 pbs | c-4ece 9/11, 147 (r-20261029-190206-21a5) | 11/11, 103 (r-20261029-191136-ba1c) | 11/11 |
| B-0038 | parabolic R 3, γ 1.3, N 120, 11 pbs | c-4ece 9/11, 132 (r-20261029-191410-0bf1) | 11/11, 84 (r-20261029-192322-14c5) | 11/11 |
| B-0039 | conical R 2, γ 1.4, N 120, 14 pbs | c-4ece 9/14, 197 (r-20261029-192609-c22a); c-82ef 10/14, 180 (r-20261029-210904-2519) | 14/14, 123 (r-20261029-193600-ce42) | 14/14 |
| B-0041 | parabolic R 5, γ 5/3, N 120, 9 pbs | c-4ece 8/9, 116 (r-20261029-195553-a539) | 9/9, 87 (r-20261029-200455-ccaf) | 9/9 |
| B-0042 | Anderson, γ 1.4, **N 60**, 11 pbs | c-4ece 6/11, 165 (r-20261029-201644-c309) | 11/11, 43 (r-20261029-202631-c516) | 11/11 |
| B-0043 | conical R 2, γ 1.4, **N 240**, 8 pbs | c-4ece 4/8, 274 (r-20261029-202852-9769) | 8/8 but 239 steps (r-20261029-203948-101e) | **rejected**, explicit negative pressure (r-20261029-204151-7207) |
| B-0044 | parabolic R 4, γ 1.15, N 120, 11 pbs | c-4ece 8/11, 148 (r-20261029-204424-9a6a) | 11/11, 87 (r-20261029-205337-9e5d) | 11/11 |
| B-0045 | conical **R 8**, γ 1.4, N 120, 8 pbs | c-82ef 6/8, 184 (r-20261029-212043-d909); c-60c5 7/8, 186 (r-20261029-234305-0dd6) | 8/8, 141 (r-20261029-211718-5f1b) | 8/8 implicit; explicit crash in the both-solver version (r-20261029-211820-3f69) |
| B-0046 | parabolic R 4, inlet at x_in 0.6 (Mach ~0.6), 12 pbs | c-82ef 9/12, 165 (r-20261029-212451-ef5b) | 12/12, 109 (r-20261029-212837-59d0) | 12/12 |
| B-0048 | Anderson, **γ 1.05**, 11 pbs | c-82ef 10/11, 126 (r-20261029-214114-4b5c) | 11/11, 98 (r-20261029-214456-f301) | 11/11 |
| B-0050 | conical R 3, **γ 3**, 10 pbs | c-82ef 9/10, 126 (r-20261029-215339-76e0) | 10/10, 94 (r-20261029-215720-2633) | 10/10 |

Every geometry type, every γ from 1.05 to 3, coarser and finer grids. Mean Newton steps 1.3–3.8 × van Leer's. No
crash or non-physical state on the candidates' side; the explicit solver mostly converges (often better than vL).
Partly hard: B-0043 (frozen crashes, vL near the step limit). Mild: B-0048, B-0050 (one back pressure each).

### 2. Newton (and explicit) stalls in low-Mach or weak-gradient nozzle flow, with or without a shock

| Case | Setup | Candidate (run id) | van Leer (run id) | Frozen |
|---|---|---|---|---|
| B-0040 | conical R 2, unchoked, pbs 0.945…0.995 | c-4ece 4/6, 192 (r-20261029-193932-099b) | 6/6, 56 (r-20261029-195250-b3d4) | 6/6 |
| B-0047 | parabolic R 4, unchoked, exit Mach ~0.03–0.1 | c-82ef 3/5, 241 (r-20261029-213125-55f3); c-60c5 **0/5** (r-20261029-221507-59df) | 5/5, 66 (r-20261029-213505-d3f8) | 5/5 |
| B-0049 | conical R 3, long low-Mach inlet (x_in −2), 11 pbs | c-82ef 5/11, 204 (r-20261029-214730-b186); c-60c5 **2/11**, 260 (r-20261029-233534-108c) | 10/11, 79 (r-20261029-215119-d122) | 11/11 |
| B-0051 | parabolic R 2.5, L 4 (gentle divergence), 11 pbs | c-82ef 7/11, 197, roughness_J 0.84 (r-20261029-220439-c44e) | 11/11, 122, roughness 0.0046 (r-20261029-220830-02fd) | 11/11 |
| B-0052 | conical, long low-Mach inlet, pb 0.01 (supersonic, **no shock**) | c-60c5 implicit 0/1, explicit ok (r-20261029-225629-c059) | both ok, 58 (r-20261029-230331-362d) | both ok |
| B-0056 | parabolic, long low-Mach inlet, pb 0.01 (no shock) | c-60c5 implicit 0/1, **explicit limit cycle at 7.88 orders** (r-20261030-001722-8a87) | both ok, 60, 12.0 orders (r-20261030-002508-c2fa) | both ok |

The worst failures: many cells at low Mach, weak gradients. B-0052/B-0056 show that a shock is not needed. Controls
with the same supersonic geometry but a short inlet converge (r-20261029-224829-f3dd, r-20261029-231446-2636). Partly
hard: B-0049 (vL misses one back pressure; frozen converges on all).

### 3. Slowly moving strong shocks: overshoot above van Leer (A7b regime), c-60c5ed6928 only

RF2-type Rankine–Hugoniot shocks moving at a fraction f = 0.2 of the maximum wave speed (~0.1 cells per step, inside
the quartic motion gate's transition band). Overshoot p90 of the single case; the Target A bound is 1.1 × van Leer.

| Case | Setup | c-60c5 (run id) | van Leer (run id) | thinc_bvd / weno5z |
|---|---|---|---|---|
| B-0053 | Mach 10, γ 1.4, f 0.2 | 0.01198 = 1.23 × (r-20261029-223331-c0b7) | 0.009757 (r-20261029-232206-3ca9) | 1.19 × / 2.46 × |
| B-0054 | Mach 10, **γ 5/3**, f 0.2 | 0.01708 = **5.96 ×** (r-20261029-235037-efff) | 0.002864 (r-20261029-235732-69ac) | 1.27 × / 2.89 × |
| B-0055 | Mach 5, γ 5/3, f 0.2 | 0.01559 = 2.14 × (r-20261030-000403-d396) | 0.007267 (r-20261030-001057-e99b) | 0.59 × / 4.08 × |

Frozen equals van Leer on all three. The thinc_bvd runs carry status "rejected" because of dev cases B-0016/B-0030
(known zoo issue); their values on the new case are reported. Near misses at lower f: 1.08 × (γ 5/3, Mach 10, f 0.1;
r-20261030-002709-8b15 vs r-20261030-003408-f548) and 1.00 × (γ 1.4, Mach 5, f 0.15; r-20261029-222440-2d89 vs
r-20261029-223137-04d0). On faster shocks (f ≈ 0.28) c-4ece6bb6f7 is cleaner than van Leer (r-20261029-205627-6a2b vs
r-20261029-210407-16c8). Partly hard: B-0053 (both reconstruction-slot zoo members also exceed 1.1 ×), B-0055 (weno5z).

## What the breakers add to the negative result

- **The A4 failure is broad, not a few unlucky instances.** All three candidates fail Newton across geometries, γ,
  grids and back-pressure regimes in which both stateful van Leer members converge; c-60c5ed6928 is the worst
  (0/5 on B-0047, 2/11 on B-0049). The signal was already on dev: every candidate fails N2 (Newton 0/1, 300 steps;
  dev r-20261029-102400-ed25, r-20261029-120946-85b2, r-20261029-113443-2bb6), where vL needs 58 steps.
- **Low-Mach, weak-gradient flow is the worst regime**, and a shock is not needed (B-0052, B-0056).
- **Suspected mechanism (code reading by all three agents, not measured):** the motion gate depends on the previous
  iterate, so the discrete operator changes between Newton steps; and the ungated entropy-field BVD/THINC weight
  with an absolute-looking `mono` threshold (REL·ρ)² switches on very small amplitudes. Neither is confirmed.
- **c-60c5ed6928's A7b failure has a specific trigger:** strong slowly moving shocks at γ 5/3, peaking where the
  motion gate is partly open.

## Zoo failures found along the way

`muscl_van_leer_frozen` gives a negative pressure in its explicit run on B-0043 (r-20261029-204151-7207) and on the
both-solver version of B-1801 (r-20261029-211820-3f69). Round 3 found the same member failing on a parabolic nozzle at
N 240 (r-20261023-225103-d50b). These cases were proposed for the candidates; the zoo crashes are noted, not proposed
separately.

## Not done

- No mechanism measurement (the judge reports only a share converged per case).
- thinc_bvd/weno5z were not run on the nozzle cases (stateless reconstruction-slot members).
- Unsteady cases were not run against the zoo where the candidate did not fail (B-1706, B-1903, B-1908).
