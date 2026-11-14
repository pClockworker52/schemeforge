# Tasks for WSL A (OpenCourant simulations)

Procedure: [../coldspray-procedure.md](../coldspray-procedure.md). Pull `claude/exciting-fermi-qy077p`, do the
newest open task, push results to `coldspray/opencourant-sph`. Write only your own section of
opencourant-verification.md and your own scripts and results. Do not edit STATUS, HANDOFF, DECISIONS, the hunch
files or this file. Blind-list papers stay closed.

## Task 2026-11-14-c: BCT under non-uniform and curved loads (open; calibration before any freeze)

**Basis:** §20.4–20.5 and DECISIONS 2026-11-14 "CS-18c: TL with a corrected BCT, not a switch to UL SPH". With BCT
off, T-S1 at R/32 gives a rebound of 0.9988; with BCT on it gives 0.860, and at R/64 0.9788. The TL bodies with the
CS-18b viscosity and α handle curved contact. The defect is BCT's coupling to the load on a curved patch with few
particles. BCT cannot be dropped: without it the end layers carry 0.65 / 0.84 of the stress (§17, §19.2).
**Status of the cases:** this is calibration for a hunch not yet drafted (CS-18c). T-S1 is now a known case, and it
will be a non-blind rung of the CS-18c ladder. Rows `kind = calibration`. Commit a prediction before each group of
runs. Stop and report at the end.

**Leading hypothesis (cloud, untested):** the rigid wall is kinematic (the wall particle is stopped, force = m Δa).
BCT spreads that force over the end layers, and the §19.2 amendment then scales the load so that the wall particle
still receives its full stopping force. This is exact only for a uniform load on a flat face. On a curved patch, and
when particles enter and leave contact, the two disagree, which shows up as the 1.485 × wall-output mismatch, the
chatter and the energy exchange. Under the hvi penalty contact (body on body, what cold spray uses) there is no
kinematic constraint to fight, so BCT may already behave there.

1. **Static and code analysis.** Where exactly does the wall scaling misload a curved patch, or one that changes
   from step to step? Compare it with BCT spreading a penalty force. One page in the fork's SPEC-TL-b.
2. **Body-on-body probe first** (the most decisive and the cheapest): the T-B2 geometry (Hertz sphere on a TL
   block, hvi contact, `contact.stfac = 3`), R/32, BCT on and off, the CS-18b set-up otherwise. Report peak,
   approach, rebound, chatter (contact segments), viscous and hourglass work. This is a calibration run of a T-B2
   deck: name it as such in the rows.
3. **A BCT variant**, chosen from 1 and 2 (WSL A proposes; examples: a penalty wall for TL bodies in place of the
   kinematic wall; per-particle wall loads without the global stopping-force scaling; BCT only on patches above a
   stated particle count, with a stated rule). One variant, fixed and committed before its runs:
   - T-S1 at R/16, R/32 and R/64;
   - the §19.2 column check (layers 1–4 within 1 % of the momentum-rate plateau);
   - the flat free surface under load (§18.4 deck, T-surface b);
   - the conforming-sphere layer-2 check of §19.1 (static model): does the variant change the 26–30 % deficit?
   - T-A0 (no TL body: identical).
4. **Also, for the CS-18c ladder:** the T-S1 peak reference (1.073, JAX §9.6). All hosts tend to 1.02–1.05 at R/64
   (collocated 1.027, S′ 1.019, TL 1.040), and the quad two-body peak is 1.047. Check the reference's resolution
   and, if needed, give a converged value. This is a reference check, not a change to any verdict.
5. **Results:** fork `hvi/results/tl_cal3_*.csv`, SPEC-TL-b updated; schemeforge §21 on `coldspray/opencourant-sph`.
   Then stop.

## Task 2026-11-14-b: T-S1 at R/64 and one BCT-off diagnostic (closed: done, §20.4–20.5, merged c329481)

**Basis:** CS-18b refuted at T-S1 (DECISIONS 2026-11-14). Peter is moving towards an updated-Lagrangian SPH hunch
(CS-19, drafted by the cloud session). This task only answers whether BCT is carried into that draft. **It is not a
rescue of CS-18b, and not a diagnostic campaign:** two runs, one table, no further runs without a new task.
**Binary:** the same as task a (clean tree `8188ca5ec`), deck switch `HVI_TL_SET=cs18b`; wall forces from the
momentum rate.

1. **T-S1 at R/64:** let the running case finish and add its row and numbers to §20.4, labelled "reported, after the
   verdict" (it cannot change the CS-18b verdict).
2. **One diagnostic run:** T-S1 at R/32 with `tl.bct = off`, everything else as task a.
   - Rows `kind = diagnostic`, no verdict; `binary_state = committed`, fork SHA, deck hash.
   - Commit a one-line prediction in its own commit before the run.
   - Report the same quantities as the §20.2 table: contact at 10⁻² (first drop and last time above), peak,
     approach, rebound, largest and final KE / KE0, smallest det F, number of contact segments, viscous and
     hourglass work.
3. **Reading rule, fixed now (before the run):**
   - rebound ≥ 0.9796 with BCT off: the wall–BCT coupling is the main cause, so BCT is **not** carried unchanged
     into CS-19 for curved contact;
   - rebound < 0.9796 with BCT off: the TL bodies (or the viscosity/hourglass set-up) fail curved contact on their
     own, so BCT is not shown to be the cause; CS-19 may carry BCT, and must test it at T-S1;
   - either way the row is a diagnostic, and nothing is tuned on it.
4. **Results:** fork `hvi/results/tlb_diag.csv`; §20.4 and a short §20.5 on `coldspray/opencourant-sph`. Then stop.

## Task 2026-11-14-a: CS-18b core rungs (closed: T-S1 FAIL, CS-18b refuted, §20, merged 7984e1c)

**Judge, frozen:** [../sph-tlsph-b-ladder.md](../sph-tlsph-b-ladder.md) and hunch
[../coldspray-hunch-cs18b.md](../coldspray-hunch-cs18b.md), frozen in 6f0786a. Cite it in every row.
**Binary:** fork `tlsph`, solver source of 43791edbc (as in the ladder's set-up), built from a clean tree.

1. **Core rungs, in the frozen order:** T-A0, T-S0, T-S0p, T-S1, T-tension, T-zero-energy, T-surface, T-B1, T-B2,
   T-B3, T-survival, T-C1, T-D1, T-D2. T-D3 waits for A3.5.
2. **Metrics under BCT:** every wall force is read from the body's momentum rate (ladder, "Metrics under BCT").
   Rung scripts that read `/TH/RWALL` must be switched before the runs; the switch is a script commit that comes
   before the predictions.
3. **Reported rungs,** labelled, whenever convenient:
   - T-surface-sphere;
   - T-large-strain-1 and -2;
   - T-cost;
   - energy closure;
   - BCT guard fallbacks (count and location) in every impact run.
4. **Rules:**
   - commit the source and decks before each campaign;
   - commit each prediction in its own commit before its runs;
   - every row records `binary_state = committed`, the fork SHA, ladder 6f0786a and the deck hash;
   - a failing core rung means stop and report to Peter, with no tuning;
   - if T-survival fails, stop TLSPH without a reference update (CS-18b kill clause).
5. **Results:** fork `hvi/results/tlb_*.csv`; schemeforge §20 on `coldspray/opencourant-sph`, with a verdict table per
   rung and the reported rungs kept apart.

## Task 2026-11-13-c: CS-18b calibration part 2 and BCT implementation (closed: done, §19, merged b5a4424)

**Basis:** DECISIONS 2026-11-13 "CS-18b calibration decisions" and §18.
**Rules (as task b):**
- this is still before the freeze; no TLSPH rung deck is used to choose anything;
- predictions and criteria are committed before their runs;
- rows `kind = calibration`, with fork SHA (committed binary) and deck hash.

1. **BCT on the conforming sphere** (static model, no engine run).
   - The BCT weights of §18.4 on the conforming sphere at R/16, R/32 and R/64, for contact patches of 3 to 10
     spacings in radius.
   - Report:
     - the sign and conditioning of Σ φ (B·n), with a proposed guard threshold;
     - the uniformity of the layer stresses under a Hertz-like pressure;
     - the torque error per pair and in total.
   - **If no robust guard exists, stop here and report.**
2. **BCT implementation** in the fork: a TL-only step after the hvi contact and wall forces; the hvi code is
   unchanged. Then:
   - T-A0 again (no TL body: identical);
   - a non-rung check: a confined TL column of length 2L at V/2 with BCT. The steady stresses of layers 1 to 3 should
     be within 1 % of the plateau.
3. **Quad two-body Hertz** (Isolid 17, axisymmetric, the B-2 geometry):
   - a deformable sphere on a deformable block, elastic, 20 m/s, at the finest affordable meshes, with convergence
     shown;
   - peak, approach and rebound against two-body Hertz. These are the quad errors for the T-B2 limits (quad error +
     3.0 points, rounded up to the next 0.5 %).
4. **α recalibration** with the LAMMPS viscosity (Q1 = 0.05, Q2 = 0), on non-rung cases: the free bar of §18.3, and
   a free block with a smooth initial field at a size other than T-zero-energy's.
   - Criterion, stated before the runs:
     - no resolved wave faster than exact (the SPEC-TL §3.5 rule);
     - the share of shortest-wavelength energy ≤ 1 %;
     - then the least dissipation.
   - Report α, and whether Q1 should change (re-run §18.3's criterion if it does).

5. **Survival probe** (added 2026-11-13, DECISIONS "CS-18b hold lifted"; a calibration-phase diagnostic, no
   verdict). Run it after item 2 (BCT implemented).
   - **Set-up:** TLSPH with the §18 set-up (LAMMPS viscosity Q1 = 0.05, α as recalibrated in item 4 or 10 if item 4 is
     not done yet, BCT).
   - **Case:** Al–Al quarter model, 800 m/s, R/16 and R/32, contact only (`bond.model = none`), t_end = 1.0 D/V.
   - **Judged by** the survival checks of the E-1 gate draft §3:
     - dt ≥ 0.1 of its initial value;
     - detached mass ≤ 1 %;
     - no cross-body pair closer than 0.5 s;
     - no det F ≤ 0 and no ill-conditioned-matrix stop;
     - energy reported, not judged.
   - **Also report:** how far beyond the kinematic switch (0.002–0.019 D/V) the run gets, the smallest det F, the
     largest stretch, and the time step history.
   - **The prediction** is committed in its own commit before the runs. Rows `kind = calibration, diagnostic`.

**Output:** fork `hvi/SPEC-TL-b.md` updated and `hvi/results/tl_cal2_*.csv`; schemeforge §19 on
`coldspray/opencourant-sph`. Then stop.

## Task 2026-11-13-b: CS-18b calibration and design (closed: done, §18, merged 3a89b1c)

**Basis:** DECISIONS 2026-11-13 "CS-18b with a calibration phase before its freeze". The T-S0 diagnosis is in §17.
This is the phase **before** the CS-18b freeze: tuning on the calibration cases below is allowed and recorded. The
TLSPH rungs themselves (the decks of `sph-tlsph-ladder.md`) are not used to choose anything.

**Rules:**
- source committed before each campaign;
- rows `kind = calibration`, with fork SHA (committed binary) and deck hash;
- no verdicts.

**(a) Finite-strain references.** For T-S0, T-S0p and T-tension, derive the exact 1D solution including finite
strain:
- the plateau stress and front speed for the solver's hypoelastic material at the deck's velocity (the offset
  0.42·V/c_d found in §17 is a check, not the definition);
- check it against the quad elements (Isolid 17) and against TL runs at V/2 and V/4 (from §17).

Write the reference formulas into the fork's `hvi/SPEC-TL-b.md`.

**(b) Threshold calibration.** Run the quad elements (Isolid 17, 2D) and collocated SPH (frozen §9.1 set-up) on the
T-S0, T-S0p and T-S1 decks at the ladder's resolutions, measured against the references of (a).
- Propose each CS-18b threshold as a stated margin over what these methods achieve.
- Every growth clause gets a noise floor.
- For B-2 and T-surface, propose a threshold with its reason.

**(c) Viscosity.** Take one viscosity form from the literature, for example the LAMMPS SMD TLSPH viscosity
(Ganzenmüller) or Monaghan with a switch, read from the source and cited. Choose its coefficients on calibration
cases that are **not** ladder rungs:
- a confined column at a different length (2×) and velocity (V/2);
- a free elastic bar ringing in its first mode, judged by damping per period.

The criterion is stated before the runs: stable without ringing, and the least dissipation.

**(d) End-layer stress design note.** In the steady state the TL end layers carry 0.655 and 0.845 of the true stress
(§17.2).
- From the literature, find why a corrected-gradient formulation does this at a truncated neighbourhood, and what
  corrects it. Candidates: corrected pair-force sums, boundary integral terms, ghost or mirror layers at free
  surfaces.
- Propose a fix (new code, described, not implemented) or argue for none.
- Define a rung **T-surface:** the steady stress of the first two layers against the traction, in the T-S0 column
  and at a free surface under load, with its threshold from (b).

**Output:** fork `hvi/SPEC-TL-b.md` and `hvi/results/tl_cal_*.csv`; schemeforge §18 on `coldspray/opencourant-sph`.
Then stop. The cloud session drafts CS-18b and its ladder from this output, and Peter approves the freeze.

## Task 2026-11-13-a: T-S0 diagnosis (closed: done, §17, merged 7638d1a)

**Why:** CS-18 is refuted at T-S0 (§16; DECISIONS 2026-11-13). Before Peter decides on a CS-18b, find out which
part of the set-up sets the contact-time and rebound errors, and whether the plateau offset is finite strain.

**Rules:**
- no solver code changes; deck and sidecar switches only;
- each case changes one thing against the frozen set-up;
- each prediction is committed in its own commit before its runs;
- rows are marked `diagnostic`, carry the fork SHA (committed binary) and the deck hash, and never a verdict.

**Deck:** the T-S0 column (h = 1.12 s, 4 wide), at 100 and 200 particles unless stated otherwise.

| Case | Change |
|---|---|
| D-visc-off | viscosity off (q_a = q_b = 1e-30); report if unstable |
| D-visc-P | Profizi's linear 0.8 / quadratic 4 |
| D-hg | α = 0, and α = 20 |
| D-vel | V/2 and V/4, at 200 particles (a finite-strain offset should scale with V) |
| D-width | width 16, at 100 particles (no effect expected with complete images) |
| D-layer | post-processing only: plateau stress per layer; where the +21 % start spike sits (first layers or bulk); the same for the collocated order-1 run of §15.9 |

**Report per case:** plateau, contact time, rebound, viscous and hourglass work as shares of the initial kinetic
energy, and the start spike. Then a short reading:
- which item sets the contact-time and rebound errors;
- whether the plateau offset is finite strain;
- whether the start spike comes from the end-layer correction.

**Results:** fork `hvi/results/tl_diag_s0.csv`; schemeforge §17 on `coldspray/opencourant-sph`. Then stop.

## Task 2026-11-12-c: TLSPH implementation and core rungs (closed: stopped at T-S0, §16; CS-18 refuted)

**Basis:**
- **Judge, frozen:** [../sph-tlsph-ladder.md](../sph-tlsph-ladder.md) and hunch
  [../coldspray-hunch-cs18.md](../coldspray-hunch-cs18.md), frozen in 583912a. Cite it in every row.
- **Design:** fork `sph-hvi-contact`, branch `tlsph`, `hvi/SPEC-TL.md` at 3e9aa6b. A change to the ladder's set-up
  after the freeze is an addendum labelled post hoc, and goes to Peter first.

1. **Implementation, in SPEC-TL §6 order.** Report each step's check in the fork CHANGELOG.
   1. Sidecar keys (`tl.*`) and fatal checks → T-A0 (no TL body: bit-identical).
   2. Reference lists with complete images; the correction matrix; the first-cycle self-check (completeness sums,
      image counts, the `tl.cond_max` and `tl.smin_min` stops).
   3. Kinematics and force without hourglass and viscosity; the one-cycle uniform-stretch check.
   4. Hourglass force, viscosity, energies and diagnostics (smallest det F, principal stretches, plastic strain,
      hourglass energy).
   5. hvi attachment (SPEC-TL §5, hvi code unchanged).
2. **Core rungs, in the frozen order:** T-A0, T-S0, T-S0p, T-S1, T-tension, T-zero-energy, T-B1, T-B2, T-B3,
   **T-survival**, T-C1, T-D1, T-D2. T-D3 waits for A3.5. The reported rungs (T-large-strain-1 and -2, T-cost)
   whenever convenient, labelled.
3. **Rules:**
   - commit the source and decks before each campaign;
   - commit each prediction in its own commit before its runs;
   - every row records `binary_state = committed`, the fork SHA, the ladder commit 583912a and the deck hash;
   - a failing core rung means stop and report to Peter, with no tuning;
   - **if T-survival fails, stop TLSPH without a reference update** (CS-18 kill clause).
4. **Results:**
   - fork `hvi/results/tl_*.csv`;
   - schemeforge `coldspray/opencourant-sph`, with a new **§16** in opencourant-verification.md (a verdict table per
     rung, diagnostics kept apart).

## Task 2026-11-12-b: freeze preconditions for the TLSPH ladder (closed: tl.cond_max 30, tl.smin_min 0.025 at fork 3e9aa6b; journal check deferred by Peter)

**Basis:** DECISIONS 2026-11-12 "TLSPH set-up from SPEC-TL adopted"; ladder draft
[../sph-tlsph-ladder.md](../sph-tlsph-ladder.md), "Freeze preconditions".

1. **Journal check of SPEC-TL's equations:** eqs. 15 (correction matrix), 17 (F), 24 (force) and 32 (hourglass) of
   Ganzenmüller, CMAME 286 (2015) 87–106.
   - Compare the journal version with the preprint arXiv:1410.7221 that SPEC-TL used. If the journal version is
     paywalled, ask Peter for the PDF.
   - Compare with one independent source, for example Bonet & Lok 1999 or Vidal, Bonet & Huerta 2007 for the
     correction and force, or another TLSPH paper for the hourglass term.
   - Record every difference in SPEC-TL, with page references.
2. **`tl.cond_max`:** compute the condition numbers of the reference correction matrices at t = 0 with a script,
   with no engine run. Cover:
   - the bulk cubic net;
   - free faces, edges and corners;
   - symmetry-plane neighbourhoods with images;
   - the surface-conforming sphere at R/16, R/32 and R/64 (including the merged particles).

   Propose a limit with its reason (for example 10× the largest value found in these sets-ups), and write it into
   SPEC-TL §5.3.
3. **Push** the fork branch `tlsph`, and stop. No solver code until the freeze commit in schemeforge exists.

## Task 2026-11-12-a: TLSPH in the fork, preparation only (closed: done; reading note merged bc3376b, SPEC-TL at fork tlsph 1ae689c)

**Basis:**
- DECISIONS 2026-11-12: TLSPH directly in the solver, 3D, bond in the solver.
- Hunch draft [../coldspray-hunch-cs18.md](../coldspray-hunch-cs18.md) and ladder draft
  [../sph-tlsph-ladder.md](../sph-tlsph-ladder.md).
- Literature: [../tlsph-literature-check.md](../tlsph-literature-check.md).

**Allowed now (no runs):**
1. **Read Profizi, Combescure & Ogawa 2016** (C. R. Mécanique 344, 211–224, doi:10.1016/j.crme.2016.02.001) and
   **Profizi's PhD thesis** (INSA Lyon 2016), at F level. Fetch them yourself under the standing fetch rule (the
   journal page and the lamcos.insa-lyon.fr thesis PDF are open; the cloud session cannot reach those hosts).
   Write `docs/research/data/profizi2016_reading.md` covering:
   - the SPH formulation (kernel, correction, stabilisation, viscosity);
   - the reference update, if any, and its trigger;
   - the body-to-body contact;
   - the adhesion law;
   - the verification shown, with numbers;
   - resolution and cost;
   - the stated limits.

   These papers are not on the blind list.
2. **In the fork, on a new branch `tlsph` from `main`,** write two documents:
   - `hvi/SPEC-TL.md`: a design proposing the set-up section of the ladder (kernel, h, correction, hourglass α,
     viscosity, reference-update rule) with reasons. It also covers where the hvi contact and bond laws attach.
   - A **CODEMAP addendum:** where a new SPH formulation plugs into the engine, whether the SPH arrays can hold
     reference neighbours, reference gradients and F, how symmetry planes would work with fixed reference
     neighbourhoods, and how SPMD/OpenMP split the loops.

   Commit both. **No solver code and no runs** until CS-18 and the TLSPH ladder are frozen in schemeforge.
3. **Push** the reading note to schemeforge on a branch `coldspray/profizi2016-reading`, and the fork branch
   `tlsph`. Then stop.

## Task 2026-11-11-b: ladder reruns under set-up S′ (closed: stopped at step 1, §15; Peter 2026-11-12)

**Basis:** [../sph-contact-ladder.md](../sph-contact-ladder.md), **Addendum 1** (frozen in 140b84a, post hoc; adopted by
Peter 2026-11-11). Cite 36c34bd + 140b84a in every row.
- **S′** = the §9.1 settings plus ξ = 0.3 and kernel-correction order 1 on **all** particles. It is one set-up for
  every rung below.
- **stfac 3** for all S′ rungs (Peter's choice for E-1; one value throughout). B-3 must pass for it.
- The FAILs under the frozen set-up stand (§14.2); S′ is a second, labelled track.

**Rules:**
- Commit the source and decks before each campaign.
- Commit each recorded prediction in its own commit before its runs.
- Every run gets a row with `binary_state = committed`.
- A failing **required** rung means stop, record it and report to Peter, with no tuning. Optional items do not stop
  the task.

**Order:**
1. **Host rungs at S′:** S0, S1 and F0 of opencourant-verification.md, on the fork binary without a sidecar. Same
   references and thresholds as in §9.4, §9.6 and §10.2. If one fails, stop: S′ is then not a valid host set-up.
2. **A-0 at S′:**
   - build the base `d791761` unmodified;
   - run S0, S0p, S1 and the two-part column at S′ on it and on the fork without a sidecar;
   - the two must be bit-identical.
3. **A-2, B-1, B-2** (R/16 and R/32), **B-3** (R/32, start at s against 2.4 s, within 1 %).
4. **B-2 convergence:** B-2 at R/48 (R/64 if R/48 is affordable and inconclusive). It must be in the same direction
   and within the same limits as at R/32. Report whether the 3.4 % peak overshoot of F2 is the SPH sphere's own: the
   F0 rerun at S′ from step 1 is the comparison.
5. **C-1, D-2** at S′.
6. **Cost:** cycles and µs per particle-cycle for S′ against §9.1, measured on an idle machine. Use B-2 R/32 and one
   column run.
7. **D-3** needs A3.5 (cs12 and bay83 activation) first:
   - A4.0: code the bay83 form as printed in the primary source (Kebriaei 2014, and Bay 1983 if Peter supplies it),
     with page references in SPEC;
   - implement, check A-0 again, then run D-3 at S′.
8. **Optional, not stopping:** the D-1 refinement path of Addendum 1 A2.4 at S′ (50 → 100 → 200 particles per L;
   maximum deviation over the whole run). Then C-2 and C-3 at S′ with `surface.area = rate` and `cone + fit` named
   as settings, as diagnostics. Changing a default is a fix with its own CHANGELOG entry.

**Results:** `hvi_*.csv` rows with a `setup` column (`frozen` or `S'`), plus a new §15 in opencourant-verification.md
on `coldspray/opencourant-sph`. §15 lists, per required rung, the verdict under S′ next to the frozen-set-up verdict.

**Not in this task:** E-1. It waits for the E-1 gate
([../sph-contact-e1-gate-draft.md](../sph-contact-e1-gate-draft.md)) to be approved and frozen. E-1 itself runs under
Addendum 1 A4: frozen set-up as the main case, S′ alongside, stfac 3.

## Task 2026-11-11-a: record and commit before anything else (closed: done, §14, merged 5a251fc)

**Why:** the referee ([../sph-contact-referee-2026-11-11.md](../sph-contact-referee-2026-11-11.md)) found that most
results in the fork's VERIFY-RESULTS.md exist only in `~/oc_runs`. Several were made on binaries that were never
committed, and the predictions after 937ff00 cannot be dated by git. Until this is fixed, the C-1 and D-2 PASS claims
are **not admissible as verdicts**.

1. **Commit every run reported in VERIFY-RESULTS.md as a CSV row in `hvi/results/`.** Each row carries:
   - the fork SHA of the binary it ran on;
   - the ladder commit 36c34bd;
   - the deck hash;
   - the settings (ξ, kernel-correction order, α_cs, stfac, normal, gap).

   This covers:
   - C-1, C-2, C-3;
   - D-1, D-2;
   - B-2d at R/32;
   - the cone + fit full run and the fast-deck acceptance runs;
   - the stabiliser matrix (cases a and c);
   - the welded bars;
   - F1 and F2;
   - the E-1 probe (R/16, 800 m/s), labelled `unauthorised probe, diagnostic`.
2. **Uncommitted binaries.** Rows from a binary that was never committed are marked `binary uncommitted`.
   - Commit the current source, rebuild, and rerun the core rungs C-1 and D-2 on that committed binary. Only those
     rows can carry a verdict.
   - Also rerun A-0 on it (no sidecar, bit-identical).
3. **From now on:**
   - commit the source before every run campaign;
   - commit each recorded prediction (CHANGELOG) in its own commit before its runs;
   - never run on a dirty tree.
4. **Push to schemeforge,** as task 2026-11-08-a item 3 says: the `hvi_*.csv` files and a new **§14** in
   opencourant-verification.md, on `coldspray/opencourant-sph`. §14 states which rows are verdicts and which are
   diagnostics.
5. **Stop after this.** Make no new runs under ξ = 0.3 + order 1 (set-up S′) and no E-1 until Peter decides
   the addendum draft (since adopted as Addendum 1 of the ladder, 140b84a). Reruns of C-1, D-2 and
   A-0 under the frozen set-up (item 2) are allowed.

## Task 2026-11-08-a: sph-hvi-contact, milestone 1 (open; the S′ reruns are task 2026-11-11-b)

**Status 2026-11-11:**
- B-2, B-3 and D-1 FAIL under the frozen ladder (referee-confirmed for B-2 and B-3 from `hvi_b.csv`).
- The plan's stop rule applies from here on. A failing rung means stop, record and report; continuing needs Peter's
  decision.
- 2026-11-12: milestone 1 is blocked under the frozen set-up (S′ not adopted, DECISIONS 2026-11-12). The work
  continues as TLSPH (hunch CS-18, draft).
- E-1 waits for the frozen E-1 gate ([../sph-contact-e1-gate-draft.md](../sph-contact-e1-gate-draft.md), draft until
  Peter approves).

**Plan:** [../sph-hvi-contact-plan.md](../sph-hvi-contact-plan.md) (approved by Peter, DECISIONS 2026-11-08 "No-fork
dropped"). **Judge, frozen:** [../sph-contact-ladder.md](../sph-contact-ladder.md), commit 36c34bd. Cite its commit in every result.

1. **Repo.** Create the private repo `sph-hvi-contact` at `~/sph-hvi-contact`, in the WSL filesystem, not under
   `/mnt/c`. Start it from the OpenCourant source at the commit behind `latest-20261011`, and copy the plan there
   as `hvi/PLAN.md`.
2. **Part A, in order:** A0 (baseline; stop if it fails), A1 (CODEMAP), A2 (SPEC committed before code), then A3
   with the core rungs. E-1 comes after B-3, and E-2 after D-3.
3. **Results here:** push to `coldspray/opencourant-sph`:
   - one CSV per rung group under `docs/research/opencourant/results/` (`hvi_*.csv`), with the fork SHA and the
     ladder commit in every row;
   - a new section **§14** in opencourant-verification.md.
4. **Stops:** a failing core rung goes to Peter. Never run `check_untouched.sh` red. E runs are diagnostics only:
   no v_cr.

## Task 2026-11-05-b: CS-13c (closed: refuted, §13)

Protocol: [../coldspray-hunch-cs13c.md](../coldspray-hunch-cs13c.md), frozen in commit 15fe42f. Follow it exactly and
in this order:

1. **Rung B0:** elastic brick sphere on an elastic brick block, two TYPE7 contacts, 20 m/s, R/16 and R/32, against
   two-body Hertz. Choose and report the gap and Stfac; they are then frozen.
2. **Rung H0-k0:** the §11.2 brick slab with `/HEAT/MAT` and k = 0. The temperature may change by at most 0.1 K.
3. **Check whether OpenCourant writes per-element plastic work.** If it does not, the second clause of check E is
   reported only, as the protocol says.
4. **The 24 runs** (500 / 800 / 1100 m/s × R/16, R/24, R/32, R/48 × twins k = 237 and k = 0), plus one run per
   velocity at R/16 without `/HEAT/MAT`, reported only.
   - Check E in every run.
   - Keep the memory and time caps.
   - Budget stop: one R/48 run over 1 h, stop and report.
5. **Metrics P1–P3,** with the controlling element's body recorded, and P2 for both bodies. Then apply the frozen
   verdict rule exactly as written.

Results go in opencourant-verification.md **§13**. A failed rung or an impossible step goes to Peter.

## Task 2026-11-05-a: CS-13b (closed: blocked, §12)

Protocol: [../coldspray-hunch-cs13b.md](../coldspray-hunch-cs13b.md), frozen in commit 9a36aae. Follow it exactly and
in this order:

1. **Rung H0-SPH.** The H0 slab of §11.2 built from SPH particles (cubic net, §9.1 settings), with conduction,
   against erfc at t = 10 ns. Pass: within 2 % at the finest spacing, with the temperature written out. If it fails,
   the particle stays adiabatic, as the protocol says, and you continue.
2. **The 24 runs.**
   - Setup F as frozen in §10.2; 500, 800 and 1100 m/s; R/16, R/24, R/32 and R/48.
   - Each case adiabatic and conductive. Conduction in the bricks, and in the particle only if H0-SPH passed.
   - Contact adiabatic: no heat across TYPE7.
   - Budget stop: if one R/48 run takes more than 1 h, stop and report before the rest.
3. **Metrics, as defined in the protocol:**
   - P1: t_f;
   - P2: maximum substrate edge plastic strain within 1.17 µm of the contact edge, at t_c = 0.5 × the smallest t_f
     at that velocity;
   - P3: conductive minus adiabatic, reported only;
   - P0: comparison with the §10.5 values, reported only;
   - also report which element controls each run's stop (a brick or a particle).
4. **Apply the frozen verdict rule exactly as written,** including the adiabatic-twin control and the 6 % tolerance
   for R/32 → R/48.

Results go in opencourant-verification.md **§12**. A failed rung or an impossible step goes to Peter, as before.
