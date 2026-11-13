# Meta-review of the SPH route review and its critique

**Provenance:** provided by Peter on 2026-11-13, in the cloud session, as his answer to a design question. The
author was not stated; the text is Peter's submission. It reviews
[sph-route-review-2026-11.md](sph-route-review-2026-11.md) (as of b339744, before the in-place rewrite) and
[sph-route-review-2026-11-critique.md](sph-route-review-2026-11-critique.md). The text is reproduced verbatim,
followed by the modeller's response.

---

Setting aside the numerical mismatches, omissions, judge-reference flaws, and edge-singularity arguments already covered in sph-route-review-2026-11-critique.md, five structural and methodological issues remain across the two documents:
 * The "Append-Only" Editing Anti-Pattern: The modeller’s account is intended as a "self-contained account for a reader who has not followed the work," yet it leaves falsified figures and disproven diagnoses inside §§2–6 and appends corrections at the very end "rather than in the text above". A new reader absorbs a false progression in §2 and a disproven claim in §3 (that Hertz failed purely in the SPH bodies and "not in the contact law") before discovering on the final page that both statements are untrue. The corrections need to be edited directly into §§2–6.
 * The Epistemological Flaw in the "No-Tuning" Rule: The project’s core method—freezing thresholds in advance and treating any miss as an immediate "stop and report, with no tuning"—conflates implementation bugs and uncalibrated numerical damping with fundamental mathematical failure of a continuum method. Freezing a judge is only valid after a solver’s baseline damping, normal definitions, and code equations are verified. Making the gates punitive on uncalibrated defaults directly incentivized the team to bypass their own stop rules to test impact physics.
 * The Critique’s Self-Contradiction on Thermal Conduction: In §5 (Answer 5), the reviewing agent suggests from memory that edge quantities require a physical length scale such as "thermal conduction or a gradient model" to converge. However, in §2 of the exact same critique, the reviewer notes that edge plastic strain failed to converge in "FE with conduction", and §2 of the modeller's report explicitly states that "Heat conduction does not regularise it (§13, hunch CS-13c refuted)". Thermal conduction is already a refuted path in this project.
 * The Unaddressed Governance Impasse: The critique’s ranked action plan in §4 recommends pivoting to 2D-axisymmetric ALE/remeshing (Step 1), redefining outputs to band-averaged integrals (Step 2), and decoupling the bond into a one-way post-processor (Step 3). While technically sound, every one of those steps violates the project owner's explicit mandate in §1: the model "must be 3D, with the bond acting inside the solver during the impact" and deliver the interface state at the contact edge. Neither document acknowledges that the technical roadmap cannot proceed without first using Step 1 to formally renegotiate the owner's requirements.
 * Unverified Literature Benchmarks in §5: Because the reviewing agent operated without external literature access, four of its six answers to the expert questions in §5 rely on hedged recall explicitly flagged as "(from memory, uncertain)" or "Uncertain". The modeller’s §8 questions still require a dedicated literature verification pass before being used for project decisions.

---

## Modeller's response (2026-11-13)

1. **Corrections appended, not edited in: accepted.** The no-edit rule covers frozen pre-registrations and hunch
   files, not a review document. The account has been rewritten in place, and a closing change log keeps the
   critique's quotes traceable.
2. **The no-tuning rule: accepted, with a limit.** The rule prevents tuning until a run passes. Freezing on
   uncalibrated defaults, however, conflates judge bugs (the linear reference, §17), calibration (damping) and method
   failure; T-S0 shows this.
   - **Change:** CS-18b gets a calibration phase before its freeze. It covers finite-strain references, thresholds
     checked against methods known to pass on the same decks, and settings chosen on calibration cases that are not
     rungs (DECISIONS 2026-11-13, WSL A task 2026-11-13-b).
   - The link to the bypassed stop rules is plausible but not shown.
3. **Conduction: accepted in part.** CS-13c refuted conduction as a regulariser in OpenCourant at reachable spacings:
   the diffusion length was 0.17–0.30 µm, 1–2 spacings at R/48 (§13.4). A physical length scale at R/100 or finer was
   not tested. The critique should have said its suggestion goes beyond the tested range; it is not refuted in
   principle.
4. **Requirements conflict: accepted.** The critique's steps 1–3 would change the owner's requirements (3D,
   in-solver bond, edge state). Peter kept the requirements by choosing CS-18b. Step 1 is the test that could justify
   revisiting them; this is now stated in the account (§7a).
5. **Unverified literature: accepted.** A literature pass on the critique's expert answers is in
   [sph-route-expert-answers-check.md](sph-route-expert-answers-check.md).
