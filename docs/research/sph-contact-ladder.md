# SPH–SPH contact (sph-hvi-contact): verification ladder (frozen)

**Frozen 2026-11-08,** with the plan approved by Peter ([sph-hvi-contact-plan.md](sph-hvi-contact-plan.md),
DECISIONS 2026-11-08 "No-fork dropped"). This file is the judge for the fork `sph-hvi-contact`. It lives in
schemeforge, apart from the code it judges, in the same way that `arenas/**` is kept apart from candidates.

**Rules:**
- **Commit order.** This commit comes before any rung run. Every rung result names this file's commit and the fork
  SHA it was run on.
- **Amendments** are dated addenda below, never edits to the tables. A change of threshold after a result has been
  seen is labelled post hoc.
- **A failing rung** is recorded and reported. It is not tuned and rerun silently.

**Default set-up:** opencourant-verification.md §9.1 (cubic net, h = 2^(1/6) s, default q, ξ = 0, dt scale 0.3),
unless a rung says otherwise.

**Core and deferred rungs:**
- **Core** (run during milestone 1): A-0, A-2, B-1, B-2, B-3, C-1, D-2, D-3.
- **Deferred:** every other rung. They are run before any fork result is used for a claim.

**Performance runs E-1 and E-2** (plan A4b) are exploratory diagnostics. No v_cr is read from them.

## A: regression

| Rung | Case | Reference | Pass |
|---|---|---|---|
| A-0 | no sidecar: S0, S0p, S1, two-part column | baseline build of the base SHA | bit-identical output |
| A-1 | sidecar with 1 body: S0, S0p, S1 | baseline | ≤ 0.1 % in all rung metrics |
| A-2 | 2 bodies, 10 s apart, opposite velocities, no contact | free flight | velocities exact to 1e-12 relative, no cross force |

**Baseline condition (before A-0):** the source build must reproduce the shipped smoke deck's reference energies
exactly. It must also reproduce `opencourant/results/sph_s0.csv`, `sph_s0p.csv`, `sph_s1.csv`, `sph_twopart.csv`
and `cs11_f0w0.csv` to 4 digits. If it does not, nothing below is run.

## B: contact

| Rung | Case | Reference | Pass |
|---|---|---|---|
| B-1 | two-column striker/target (§9.8 deck, 50 particles/L) | exact 1D: striker at rest from 2L/c_d; target near end at rest to 4L/c_d, then V; target mean V/2 | striker \|v\|/V ≤ 0.05 for t ≥ 1.1·2L/c_d; target mean within 0.05 V of 0.5 V; interface tension never > 1 % of ρc_dV |
| B-2 | Hertz sphere on SPH block (W0 set-up), R/16, R/32 | two-body Hertz | at R/32 peak and approach within 5 %, rebound > 0.9 V |
| B-3 | B-2, started at s and at 2.4 s | itself | metrics differ ≤ 1 % |
| B-4 | two equal spheres, head-on | two-body Hertz | as B-2 |
| B-5 | block sliding on block under light normal load | frictionless: tangential momentum per body conserved | ≤ 1 % change |
| B-6 | B-2 quarter vs half model | itself | ≤ 0.5 % |
| B-7 | B-2 at 1 vs 8 threads | itself | ≤ 0.1 % |
| B-8 | energy in elastic B-2 | KE + contact + strain energy | total drift ≤ 2 % to end of rebound |

## C: surface expansion Y = (A − A₀)/A

| Rung | Case | Reference | Pass |
|---|---|---|---|
| C-1 | block under prescribed homogeneous equi-biaxial stretch λ | Y = 1 − 1/λ² on the free face | ≤ 1 % at λ = 1.5, 2 |
| C-2 | rigid rotation of a block, 90° | Y = 0 | \|Y\| ≤ 1e-3 |
| C-3 | sphere normals at t = 0 (colour gradient) | analytic radial normal | angle ≤ 5° at R/32 |

## D: bond

| Rung | Case | Reference | Pass |
|---|---|---|---|
| D-1 | B-1 with `tie`, σ_B above the tension amplitude | exact 1D joined bar (length 3L) | velocities within 0.05 V of exact |
| D-2 | B-1 with `tie`, σ_B below the tension amplitude | exact: separation when the interface stress reaches σ_B | separation time within 5 %; dissipated energy = G_c·A within 5 % |
| D-3 | two blocks pressed (p > p_E), stretched equi-biaxially to Y > Y' (prescribed), pulled apart | σ_B from the closed form on the exact Y(t), p(t) | pull-off traction within 2 % (cs12 and bay83) |
| D-4 | D-3 with Y < Y', and separately p < p_E | no bond (cs12); bay83 term-wise | zero bond strength / correct term |
| D-5 | D-3 at dt scale 0.3 and 0.15, s and s/2 | itself | ≤ 2 % |

**Before D-3:** the bay83 form is coded as printed in the primary source (Kebriaei 2014; Bay 1983 if Peter supplies
it), with page references in the fork's SPEC.md. The form quoted in the plan is from the external literature report
and has not been checked.

## Addenda

### Addendum 1 (2026-11-11, post hoc): stabilised set-up S′, D-1 window, B-2 resolution, E-1 before B-2/B-3

**Adopted by Peter on 2026-11-11, as written** (relayed in opencourant-verification.md §14.6; DECISIONS 2026-11-11).
It follows the referee's rulings (sph-contact-referee-2026-11-11.md).
- **Post hoc:** every item marked *post hoc* was written after rung results were seen (fork 6a8084b).
- **What stands:** the tables above are unchanged. Under the frozen set-up B-2, B-3 and D-1 FAIL (§14.2), and those
  FAILs stand.

### A1. Stabilised set-up S′ (post hoc)

**Motivation:** the fork's diagnostic runs F2 (B-2 at R/32, frozen contact law: peak 1.035, approach 0.981, rebound
0.983) and the D-1 columns with ξ = 0.3 + order 1. All of these were run outside the frozen set-up.

1. **S′ = §9.1 settings plus artificial stress ξ = 0.3 and kernel-correction order 1, on all particles.**
   - One set-up for the whole ladder. No per-rung choice, and no use only for rungs in tension.
   - Order 1 on interface particles only would be new solver code. That counts as a fix: a CHANGELOG entry with a
     literature check, then a full rerun under its own name. The global-S′ runs do not validate it.
2. **The FAILs under the frozen set-up stand** and stay recorded: B-2, B-3, D-1, and C-3 at its default normals. S′
   does not replace them. It opens a second, labelled track.
3. **Reruns under S′, all required before any S′ verdict:**
   - A-0 against a baseline built and run at S′;
   - A-2, B-1, B-2 at R/16 and R/32, B-3, C-1, D-2, D-3;
   - the host SPH rungs of opencourant-verification.md (S0, S1, F0) at S′, against the same references and
     thresholds as there. The host was verified only at ξ = 0 and order 0.
4. **Extra conditions, because S′ was chosen after seeing results:**
   - B-2 must also converge at R/48 or R/64, in the same direction and within the same limits as at R/32;
   - B-3 must pass within 1 % at R/32 for the stfac used;
   - the cost of S′ is reported against §9.1 (cycles and µs per particle-cycle, measured on an idle machine);
   - F2's 3.4 % overshoot of the Hertz peak is reported and either explained or flagged as open.
5. **Thresholds unchanged.** The B-2 peak metric (sensitive to chatter) is not changed; any change to it would be
   post hoc as well.

### A2. D-1 (tied bar)

1. **The reference stays the exact 1D joined bar.**
2. **The tie-versus-welded difference** at the same settings is reported as a labelled diagnostic ("the bond adds no
   error beyond the host"). It is not judged.
3. **Measurement window (clarification, not post hoc in substance):** D-1 is judged by the maximum deviation over
   the whole run, t ∈ [2L/c_d, end of run], not at a chosen instant.
4. **Optional refinement path (post hoc):**
   - D-1 passes if the maximum deviation from the exact bar falls below 0.05 V with refinement, at 50 → 100 → 200
     particles per L;
   - the deviation must decrease monotonically, and be below the limit at 200 particles per L.
5. **Design defect noted:** D-1's feasibility could have been checked at freeze time against §9.8. It was not.

### A3. B-2 resolution

R/32 stays required. Finer resolutions count only as convergence evidence (A1.4).

### A4. E-1 before B-2 and B-3 pass (conditional permission)

1. **Label on every row and figure:** "exploratory; B-2/B-3 FAIL under the frozen set-up (run ids …); no v_cr, no
   claim".
2. **The frozen set-up is the main case.** S′ may run alongside, labelled as S′.
3. **stfac:** Peter's choice (1 or 3, against the O11 default of 10).
4. **Records:** every run gets a CSV row with the fork SHA of a committed binary and the deck hash.
5. **No feedback:** nothing from E-1 feeds back into choosing the ladder's set-up, metrics or thresholds.
