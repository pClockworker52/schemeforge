<!-- Reviewer 1, route review 2026-11-15 (D6). Fresh general-purpose agent, given review-packet.md (brief §§1–3), state-report-2026-11-15.md and inputs.md; brief §4 withheld. Saved verbatim below this line. -->

# Independent review: route review 2026-11-15, decisions D1–D4

## Overall judgment

The route as currently specified can't be reached. The first claim needs a 3D host with an in-solver bond, and it judges the interface state as 0.5 µm averages read from the volumetric particle layers. At R/32 the kernel reaches about 0.7 µm, so a 0.5 µm window sits inside the boundary error (§22.1; packet §1). The full block at R/64 already needs about 40 GB on a 15 GB machine (§22.1). That still leaves the flat lattice face's first-layer deficit (0.59 / 0.50 at R/32 / R/64, §22.2). The bulk mechanics with BCT off, on the other hand, are good: T-S1 rebound is 0.9988 and peak 1.060 against 1.062 (§20.5, §21.3), and T-B2 rebound is 0.999 (§21.2).

My judgment is that the project should stop asking the particle layers for surface quantities. The first claim should be narrowed to what this host can plausibly verify, and the host should get one bounded, pre-registered last attempt, with a trigger that cannot fire just because the reference is unconverged. The process discipline is sound. The weak point is that the requirements were fixed before anyone checked they were feasible, and the 2026-11-13 critique had already pointed at this.

## D1: bond in the solver or one-way

**Choice: (ii), one-way first, with a renamed output.** The first claim should report **v_onset**: the lowest impact velocity at which the Bay criterion is met at any point. This is a quantity of the model and is exact up to first bonding. It should not be labelled v_cr. The in-solver bond, using a continuous damage variable q as Input 1 suggests (a standard cohesive construction, critique 1), becomes stage 2.

**Reasons:**
- Requirement (b) adds rungs that have never been run on TLSPH: tension, cohesive, bonded and Bay activation (packet §1; §20.1).
- The only host that did run bonded rungs failed them by a wide margin: D-1 at 0.285 V against a limit of 0.05 V (§14.2).
- Keeping (b) stacks these unknown failure modes on top of a surface problem that is still open.
- I agree with critique 7 that the one-way result is exact only "until the first point bonds anywhere", not "until local unloading" as Input 2 says.
- I also agree with the modeller's point on Input 1: D1 does not fix the surface quantities. It removes failure modes, it does not remove the dependence on Y and p_n.

**Disagreement with the critique:** calling v_onset a "lower bound on v_cr" adds a modelling claim: that bonds formed during impact can only be lost afterwards, never gained. Naming the quantity for what it is avoids that claim.

**Main risk:** v_onset may not discriminate against the sound-speed law Z6 on Track A data. The claim could then be correct but scientifically weak.

**What would change my mind:** if the TLSPH tension and bonded rungs passed cheaply at R/32 with BCT off, keeping (b) would cost little.

## D2: averaging length against resolution

**Choice: (ii), plus a time-limited version of (iii). Reject (i). Reject (iv) as a host option.**

- **(i) is infeasible on this machine.** The full block at R/64 is already out of reach (§22.1).
- **(iv) cannot host the TLSPH resolution study.** SPH in OpenCourant is 3D only (opencourant-verification.md, summary table, line 24). 2D axisymmetric work can only improve the reference, through the JAX or quad codes.
- **(ii) removes the depth bands from the claim.** The Bay criterion needs Y and p_n (state report, "Goal"), not σ_zz in depth bands. Y would come from facet stretch on a measurement-only skin, and p_n from penalty forces per facet. The band σ_zz averages should become diagnostics only.
- **I partly disagree with the requirement in force.** "All 20 averages within 3.5 %" (§22.1) judged quantities that the claim does not use.
- **(iii), with a deadline.** WSL B should look for a physical length scale. Tang 2021 is a Waterloo MSc thesis on MPM. Its abstract credits its discretisation independence to "adhesion energy and regularization techniques", which is a regularised bond model, not evidence of converged interface states. If no physical length is found, keep 0.5 µm. Do not make the window coarser for convenience.

**Main risk:** Y from the skin is untested, and p_n from penalty forces was already 4.9–10.3 % high (§22.2). The skin fixes Y at best, not necessarily p_n.

**What would change my mind:** if a skin p_n with a converged reference still shows a fixed rim error that does not shrink from R/32 to R/64, the skin buys nothing, and the remaining options are (i) or a different host.

## D3: host

**Choice: (i), bounded by the D4 trigger:** TLSPH with BCT off on both bodies, a measurement-only skin (no force feedback, as in critique 8), and a flat block face with a fitted outer layer (critique 9). Track A continues regardless.

**Reasons:**
- This is the only host with clean elastic bulk numbers at reachable resolution (§20.5, §21.2).
- The conforming sphere side is much closer to the reference than the flat face: within 3.7 % at R/64, against band-1 errors of −8 / −9 % on the block (§22.2). So the flat-face construction is a cheap, specific hypothesis.
- (iii) is not available: there is no 2D remeshing for quads (log line 24).
- For (ii), only reading is justified now. Neither input gives evidence that CEL, ALE or MPM produce converged interface states (critique 11; Tang 2021 abstract).
- I don't treat (iv) as an alternative host. It is the fallback if the trigger fires.

**Main risk:** sunk cost. The skin and the fitted face are two new constructions, and a pass on elastic T-B2 still says nothing about plastic jetting.

**What would change my mind:** if the WSL B literature check finds a demonstrated converged contact-edge Y or p_n in some other host. Hillman's 2013 dissertation contains a "patch test for collocation method" section and should be read. I have not verified the "proves mathematically" claim in Input 2.

## D4: dead-end trigger (proposed; the thresholds are my judgment)

**Preconditions, all done before the frozen run:**
- TLSPH internal energy is implemented. The T-S1 and T-B2 energy budgets close within 1 % of KE0 (my proposal).
- The interface file lists the particles actually in contact (open item, §22.3).
- The quad reference is rerun at R/256. For each quantity q, U_ref,q = |quad R/128 − quad R/256|.
- If any U_ref,q > 1.75 % (half of 3.5 %), the reference is improved first (finer mesh or Richardson extrapolation) and the trigger is not evaluated. This prevents killing a host inside the reference's own noise.

**Host:** fork TLSPH, CS-18b viscosity and hourglass settings, BCT off, measurement-only skin, flat block with a fitted outer layer, frozen binary.

**Case:** T-B2 elastic, R = 10 µm, 20 m/s, quarter model (§22.1).

**Resolutions:** R/32 on the full block, R/64 on the reduced block. Each run is judged against the quad on the same block size (§22.1).

**Quantities:**
- p_n and Y from the skin, as 0.5 µm disc averages on the axis and at 0.5 a_max, block side and sphere side, at the force peak (8 values per resolution).
- Peak, approach and rebound against two-body Hertz.

**The trigger fires if any of these holds:**
1. At R/64, any skin average has |error| > 3.5 % + 2·U_ref,q.
2. For any skin average, |error at R/64| > 0.8 × |error at R/32| (no convergence).
3. Rebound falls below the CS-18b R/64 limit of 0.9746 (§20.4).
4. The energy budget does not close.

**If it fires:**
- The 3D particle-host route for the interface state is closed, scoped to this host, these resolutions and this machine (agreeing with critique on Input 1, step 4).
- No further BCT, skin or face variant, and no CS-18c.
- The negative result goes into the ledger.
- Track B shrinks to shape, flattening and rebound only, which needs no interface state. Track A becomes the main line.
- Any new host (MPM, Eulerian) needs its own review and its own trigger written before any run.

**A pass is not the full ladder.** It only licenses the plastic and tension rungs.

## D5: order of work (judgment)

1. The quad reference at R/256 and U_ref. This step is not in the packet's list, but it is cheap and gates the trigger.
2. TLSPH internal energy (WSL A), run in parallel with the WSL B literature check (VCI and collocation patch tests, Tang 2021).
3. The fitted flat face.
4. The measurement skin.
5. Freeze the D4 run and execute it.

## Claims checked and found wrong or unsupported

1. **State report summary:** the first layer "carries only 0.5–0.6 of the true stress, under any contact."
   - The column's first layer is 0.62 (§21.4, §22.2).
   - Every case that shows the deficit is a flat lattice face.
   - The conforming sphere side lies within 3.7 % at R/64 (§22.2), and no layer values are reported for it.
   - "Any contact" is therefore unsupported. What has been shown is "any point-loaded flat lattice face".
2. **Critique 5:** the reference drift "moves them further out." This holds for block band 1 only.
   - p_n (+4.9 to +10.3 %) and band 2 (+5.9 to +9.0 %) are too high (§22.2).
   - A rising reference would move those values inward. §22.2 says so itself for p_n at 0.5 a.
   - So Input 2's noise-floor point partly holds for p_n, which is the quantity the Bay criterion uses.
3. **Packet D2(iv):** 2D axisymmetric work for resolution studies. TLSPH/SPH in OpenCourant is 3D only (log line 24), so this option can serve the reference only, not the host.
4. **Input 1:** "8–12 % vs ~5 %." These are the pre-§22 odds. After §22 they are 6–10 % and 3–5 % (state report, "Odds"). Either way they are the modeller's judgment, not evidence.
5. **Input 2:** TLSPH "surviving" the 800 m/s probe as support for BCT-off bulk mechanics. The probe ran with BCT on only and was not rerun with BCT off (state report, "Current technical state").
6. **Input 2 / critique 4:** that the literature "proves mathematically" corrected particle methods fail traction patch tests. Unverified. The VCI papers I found (Chen, Hillman and Rüter 2013) address Galerkin integration. The collocation patch test sits in Hillman's 2013 dissertation, which I saw only as a table of contents.
7. **Packet D3(ii):** "Tang 2021 claims discretisation independence." Per its abstract, this is an MSc thesis, and the independence comes from adhesion energy and regularisation of the bond model, with bonded area converging under grid refinement. It is not verification of the interface state against exact references.
8. **0.49 KE0 at rebound 0.998** (packet, inputs): stated in §21.5, but the variant table there lists no work columns, so I could not check it against a row. The BCT-on R/32 values (0.33 + 0.15 at rebound 0.860, §20.2) do check.
9. **Minor:**
   - "p_n 5–10 % high": the lowest value is +4.9 % (§22.2).
   - Critique 1's "about R/100" means a window of about 2.2 kernel reaches (s ≈ 0.1 µm, h = 1.12 s, reach about 2h), not "several".

**Sources:**
- [Tang 2021, UWSpace](https://uwspace.uwaterloo.ca/handle/10012/17030)
- [Chen, Hillman, Rüter 2013, IJNME (via zendy.io)](https://zendy.io/title/10.1002/nme.4512)
- [Hillman 2013 dissertation, eScholarship](https://escholarship.org/content/qt2s8848b6/qt2s8848b6.pdf)
