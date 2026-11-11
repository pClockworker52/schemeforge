# Referee report on the sph-contact ladder questions (2026-11-11)

**Referee:** independent agent (`referee`, agent id ad58af87a76f8cea5), run 2026-11-11 from the cloud session.
**It saw:**
- the frozen ladder (sph-contact-ladder.md @ 36c34bd);
- opencourant-verification.md §9.1 and §9.8;
- the plan and DECISIONS 2026-11-08;
- the fork's `hvi/` files at commit 6a8084b (sparse checkout).

**It did not see** the modeller's own recommendations. The modeller's recommendation on Q2 (judge D-1 against the
welded SPH bar) is overruled below. The report is reproduced verbatim. Peter's decisions on it are recorded
elsewhere (addendum draft: sph-contact-ladder-addendum-1-draft.md).

---

## What I checked
- **Confirmed:**
  - The ladder was frozen at 36c34bd and the plan was committed in the same commit, before any rung run.
  - The B-2 and B-3 peak and approach values match `results/hvi_b.csv` (for example 0.8575 / 1.1662, and the B-3
    peak 0.9416 against 1.0080, a 6.6 % gap).
  - The welded-bar miss at the frozen set-up (striker −0.925 V against −0.998 at 3.0 T_C) agrees with schemeforge's
    own §9.8 data (−0.93 V at 3.0), so it is plausible.
- **Not verifiable:**
  - `hvi_b.csv` holds only the A3.2 rows (fork 4e0646744, last row B-2d at R/16). There are no rows for C-1 or D-2
    (both core rungs reported PASS), C-2, C-3, D-1, B-2d R/32, the stabiliser matrix, the welded bars, or F1/F2.
    They exist only in `~/oc_runs`.
  - The fork history has a single commit (6a8084b, 2026-11-11 14:36). F1/F2 ended at 10:28 that day. So
    "predictions recorded before the runs" rests only on the CHANGELOG's word; git cannot confirm it.
  - Several runs (D-1, D-2, C-3, the A3.4 binary) used uncommitted binaries. That breaks the ladder rule that every
    result names its fork SHA.

  **Modeller's note:** "single commit" is the shallow sparse checkout the referee read. GitHub shows five commits
  with dates (8eb530f 11-09, 057e41a 11-09, 937ff00 11-10, e606c13 11-11 04:37, 6a8084b 11-11 13:36). The runs and
  predictions after 937ff00 still fall between commits, so the referee's point stands for them.

## Q1: ξ = 0.3 and/or kernel-correction order 1. Allowed with conditions, as a post-hoc set-up amendment, not a clarification
- **Not a clarification.** §9.1 marks ξ = 0 as untested in tension and says order 1 was never varied. That is a fair
  reason to revisit the set-up. But the pair was picked after seeing which options made B-2 pass, from a matrix of
  options and two contact laws.
- **Conditions:**
  - A dated addendum, labelled post hoc, that cites the F2 and D runs as its motivation.
  - Every frozen-set-up FAIL stays on record: B-2, B-3, D-1, and C-3 at its defaults.
  - **One set-up for the whole ladder,** with order 1 on all particles exactly as tested. Choosing settings rung by
    rung, or only for rungs in tension, is not allowed.
  - Order 1 on interface particles only would be new solver code. That makes it a fix: it needs a CHANGELOG entry
    with a literature check, and it gets its own full rerun. The global order-1 runs do not validate it.
  - Rerun every core rung under the new set-up (A-0 against a baseline built at the same settings, A-2, B-1, B-2 at
    R/16 and R/32, B-3, C-1, D-2, D-3). Also rerun the host's own SPH rungs from opencourant-verification.md (S0,
    S1, F0), since the host was only ever verified at ξ = 0 and order 0.
  - Because the choice was post hoc, B-2 must also pass where nothing was tuned: a finer resolution (R/48 or R/64)
    showing convergence, and B-3 within 1 %.
- **What is weaker, and whether it is acceptable:**
  - The settings were selected for passing.
  - F2's 3.4 % peak overshoot sits near the 5 % limit and is still unexplained.
  - ξ and order 1 have not been separated on the full deck.
  - This is acceptable only with the confirmation runs above and the cost (+70 % for ξ, per §9.1) reported.

## Q2: Measuring D-1 against the welded SPH bar. Not allowed as a replacement; allowed as an extra metric
- The ladder says "exact 1D joined bar" in the text and the table. Swapping in the welded bar weakens the test, it
  does not clarify it:
  - the reference would become a numerical solution with a known defect (tensile instability);
  - absolute accuracy would no longer be checked;
  - it breaks the project rule of judging against exact solutions.
- The tie-versus-welded difference (0.090 against 0.091 V) may be reported as a labelled diagnostic: "the bond adds
  no error beyond the host". D-1 stays FAIL against the exact bar.
- Legitimate ways forward:
  - (a) A post-hoc addendum that keeps the exact reference and requires the deviation to go below 0.05 V with
    refinement (for example 100 and 200 particles per L).
  - (b) Fix the host's behaviour in tension.
- The ladder never says over what time window D-1 is measured. Fixing that before the next run is a legitimate
  clarification, provided it uses the maximum over the whole run, not a favourable instant.
- Feasibility could have been checked at freeze time using §9.8. Missing that is a design defect of the ladder, and
  it still has to be fixed by a dated addendum.

## Q3: A finer resolution instead of R/32 for B-2. Not allowed as a replacement
- R/32 is named explicitly, and it is the production resolution for the E runs.
- The "only 5 spacings" argument is weakened by F0: the same SPH sphere at R/32 passes Hertz against a flat surface
  (0.987 / 1.037 / 0.99). So R/32 is achievable.
- F2 already passes at R/32 under the amended set-up, so the question is largely moot. Finer runs belong in the
  record as convergence evidence, which Q1 requires anyway.

## Q4: Running E-1 now. Allowed with conditions
- The plan says only "after B-3", and B-3 has been run. E-1 is exploratory, and the 80/20 effort weighting favours
  it.
- Conditions:
  - Label: "exploratory; B-2/B-3 FAIL under the frozen set-up (run ids); no v_cr, no claim".
  - Run the frozen set-up as the primary case. The amended pair may run alongside, labelled as such.
  - Peter decides stfac (1 or 3 against the O11 default of 10).
  - Every run gets a CSV row with fork SHA and deck hash.
  - E-1 results must not feed back into choosing the set-up or thresholds for the ladder.

## Process problems
1. Missing result rows for C-1, D-2 (core PASS claims), C-2, C-3, D-1 and all the diagnostics. The C-1 and D-2 PASS
   claims are not admissible as verdicts until they are recorded.
2. Runs on uncommitted binaries, and a single-commit history, so the timing of predictions cannot be audited.
3. The plan's stop rule ("Any failing rung: stop, record it, report") was not followed after B-2 failed. Work went on
   through A3.3 and A3.4 and into deferred rungs. Peter should confirm or reject that after the fact.
4. An E-1 probe (R/16, 800 m/s) was already run, prompted by an external LLM review, with no schemeforge or Peter
   decision.
5. The deferred rungs run early (C-2, C-3, D-1) are allowed, but their FAILs stand.
6. The base is `d791761` instead of the plan's `cb760c2` tag. It is documented and the A-0 baseline is
   bit-identical, but Peter should accept it explicitly.
7. Multiple comparisons: four options and two laws were tried before F2. B-3 at R/32 was run only at stfac 10.
8. Any change to the chatter-sensitive B-2 peak metric would also be post hoc.
