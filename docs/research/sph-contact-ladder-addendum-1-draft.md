# sph-contact ladder, addendum 1: DRAFT, awaiting Peter, not in force

**Status:** draft of 2026-11-11, by the modeller. It follows the referee's rulings
([sph-contact-referee-2026-11-11.md](sph-contact-referee-2026-11-11.md)).
- **Not in force.** The frozen ladder ([sph-contact-ladder.md](sph-contact-ladder.md) @ 36c34bd) applies unchanged
  until Peter approves.
- **On approval:** this text is appended to the ladder's "Addenda" section as "Addendum 1 (2026-11-xx, post hoc)" in
  its own commit, and this draft file is deleted.
- **Label:** every item marked *post hoc* was written after rung results had been seen (fork 6a8084b,
  VERIFY-RESULTS.md).

## A1. Stabilised set-up S′ (post hoc)

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

## A2. D-1 (tied bar)

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

## A3. B-2 resolution

R/32 stays required. Finer resolutions count only as convergence evidence (A1.4).

## A4. E-1 before B-2 and B-3 pass (conditional permission)

1. **Label on every row and figure:** "exploratory; B-2/B-3 FAIL under the frozen set-up (run ids …); no v_cr, no
   claim".
2. **The frozen set-up is the main case.** S′ may run alongside, labelled as S′.
3. **stfac:** Peter's choice (1 or 3, against the O11 default of 10).
4. **Records:** every run gets a CSV row with the fork SHA of a committed binary and the deck hash.
5. **No feedback:** nothing from E-1 feeds back into choosing the ladder's set-up, metrics or thresholds.

## Open for Peter (decide before this draft can be frozen)

1. Adopt A1–A4 as written, change them, or reject them.
2. **After the fact:** approve or reject the fork's work past the plan's stop rule (A3.3 and A3.4 after B-2 failed,
   and the deferred rungs run early), and the E-1 probe (R/16, 800 m/s) made without a decision.
3. Accept the fork base `d791761` instead of `cb760c2`. It is documented, and A-0 is bit-identical.
4. stfac for E-1.
