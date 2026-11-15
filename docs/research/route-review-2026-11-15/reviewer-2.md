<!-- Reviewer 2, route review 2026-11-15 (D6). Fresh general-purpose agent, given review-packet.md (brief §§1–3), state-report-2026-11-15.md and inputs.md; brief §4 withheld. Saved verbatim below this line. -->

# Independent review: route review 2026-11-15, decisions D1–D4

## Overall judgment

My judgment: as a programme for an in-solver bond in 3D, the route is close to exhausted. As a way to a narrower first claim it still has some life. The record shows a strong bulk and a weak surface. TLSPH with BCT off gets the elastic integrals right: on T-S1 at R/32 it gives rebound 0.9988 and peak 1.060 against 1.062 (§20.5, §21.3), and on T-B2 at R/32 rebound 0.999 (§21.2). But no host has delivered a verified surface quantity. Most of the §22 failure comes from the requirements themselves:
- The 0.5 µm length was chosen only so the window exceeds one spacing at R/32 (DECISIONS 2026-11-14, item 4). It was not chosen on physical grounds.
- 16 of the 20 judged averages are subsurface stress bands (§22.1). The Bay criterion takes p_n and Y, not σ_zz.
- The reference is itself unconverged by about the same amount as the 3.5 % threshold (§22.2).

So I would not read §22 as proof that the host can never deliver the interface state. I would read it as proof that the test was badly posed. One more bounded attempt is justified, provided the surface quantities are measured on a surface, the reference is tightened first, and a dead-end trigger with no escape clause is frozen before any run. Track A should carry the project if that attempt fails.

## D1. In-solver bond or one-way bond

**Choice: (ii) one-way first.** The in-solver bond becomes a second stage with its own ladder.

**Reasons.**
- **Fewer things can fail.** No tension, cohesive or bonded rung has ever run on TLSPH (§20.1). The one collocated-SPH bonded bar missed by 0.285 V against a 0.05 V limit (§14.2). Requirement (b) stacks an untested failure mode on top of an unsolved one.
- **The bound is one-sided, and that is useful.** The one-way result is exact until the first point bonds anywhere. I agree with the modeller's critique (item 7) that input 2's "identical up to local unloading" is wrong. The onset velocity it gives is a lower bound on v_cr *under the Bay criterion*. That makes a clean test in one direction: a measured v_cr below the predicted bound refutes the criterion plus the model. A measured v_cr above it decides nothing. This is a weaker claim, but an honest and falsifiable one.
- **The critique is right that (ii) does not fix the surface problem.** D1 does not replace D2 or D3.

**Main risk.** If bonds formed in compression usually break during rebound, the lower bound may sit far below v_cr and carry little information. (Judgment; I have no number for how often this happens.)

**What would change my mind.** A TLSPH tension and cohesive rung passing at R/32 at low cost before the surface work is done. Or evidence that onset-of-bonding bounds are uninformative in practice, for example blind-paper v_cr values well above any plausible onset velocity.

## D2. Averaging length against resolution

**Choice: (ii), with two changes to the judged quantities, plus (iv) for the reference only.**

1. **Judge only what the criterion uses.** Judge p_n and Y on a measurement-only skin, averaged over 0.5 µm discs *in the surface*. Report the depth-band σ_zz as a diagnostic and stop judging it. With a skin, the kernel-reach conflict concerns the in-plane disc, not a depth band:
   - At R/64 (s = 0.156 µm, §22.1) the kernel support is 2h = 2.24 s ≈ 0.35 µm. The smoothing-length rule h = 1.12 s is at verification-log line 523.
   - That support is smaller than the 0.5 µm disc radius. So most of the "kernel reach > window" problem goes away, without the roughly R/100 resolution option (i) would need.
2. **Keep the skin measurement-only.** I agree with the modeller's critique of input 1, step 3: feeding skin forces back to the particles repeats the step where BCT failed.
3. **Use 2D axisymmetric runs only to generate references.** The quad reference drifts 2.3–4.0 % from R/64 to R/128 (`results/tl_cal4_compare.csv`, column `quad_R64_to_R128`). That is cheap to tighten in 2D: the R/128 quad took about 1806 s of engine time (`tl_cal4_quad.csv`). I would not use 2D as the host, because it relaxes (c) without need.

**On (iii).** I disagree with the packet's framing. It treats 0.5 µm as the physical baseline and any coarser length as suspect, but 0.5 µm was itself a numerical choice. The physical candidate, 0.2 µm (the thermal diffusion length, DECISIONS 2026-11-13), was dropped because it lay below one spacing. Either justify a length physically or state it as a resolution limit of the claim. Do not present it as physics.

**Main risk.** Y taken from facet stretch may be accurate while p_n stays 5–10 % high, as it already does from penalty forces (§22.2). The skin fixes the geometry of the measurement, not the force distribution.

**What would change my mind.** The skin reproduces the band-1 error pattern instead of the surface value. Or the corrected-particle literature (WSL B) shows surface tractions cannot be recovered even with surface integration.

## D3. Host

**Choice: (i) as one bounded attempt under D4, with (iv) running in parallel as the default fallback.**

**Reasons for (i).**
- It is the only host with clean elastic integrals on both T-S1 and T-B2 (§20.5, §21.2).
- Its kinematics near a free surface are good: the flat free surface under load is within 0.8 % (§21.4), and Y is a kinematic quantity.

**Why not (ii) or (iii) now.**
- MPM has no evidence on this question. Tang 2021 turns out to be a University of Waterloo master's thesis. Per its record, it reaches discretisation-independent *bonded area* through an adhesion-energy regularisation, not converged edge p_n or Y. I saw only the thesis record and a search summary, not the full text.
- Input 2's CEL/ALE suggestion and input 1's Eulerian exit cite no evidence of converged interface states.
- (iii) is not available in OpenCourant for 2D elements.

**Main risk: large distortion, not the surface.** The survival probe at 800 m/s passed only with BCT on (§19.5) and was never rerun with BCT off. No plastic impact has run with BCT off (§20.1). A TL formulation could fail at jetting even if the surface problem is solved. (Judgment; not tested here.)

**What would change my mind.** The BCT-off survival probe fails. Or the fitted flat face shows the same layer-2 deficit as the conforming sphere (see factual note 5 below).

## D4. Dead-end trigger, frozen before any further result

**Host.**
- TLSPH in the fork, CS-18b set-up (Q1 = 0.1, α = 5), BCT off on both bodies.
- Measurement-only skin.
- Flat substrate face built with a fitted outer layer, one construction frozen in advance, no variants afterwards.
- Binary and decks committed before the runs.

**Cases and resolutions.**
- **(1) T-B2 elastic deck.** R/32 on the full block; R/64 on the reduced block (§22.1).
- **(2) Survival probe.** The BCT-off rerun of the §19.5 probe at 800 m/s, R/16 and R/32, to 1.0 D/V, with its survival checks. TLSPH internal energy must exist first.
- **(3) Elastic-plastic sphere on block** at a velocity below the 2D FE jet-root collapse, compared only up to the time the FE reference is valid (§8: collapse at 5–37 % of penetration). The velocity and end time are frozen with the trigger.

**Quantities.** On the block side and the sphere side (once the interface file lists the particles actually in contact, §22.3), at the axis and at 0.5 a_max:
- p_n: penalty force over facet area.
- Y: facet area stretch.

Each is taken at the force peak and as the 0.4–0.6 t_H window mean, all averaged over 0.5 µm discs.

**Reference and its uncertainty.**
- Run the quad axisymmetric reference at R/64, R/128 and R/256.
- Define U_ref as the R/128-to-R/256 change, or the Richardson error estimate if the observed order is stable.
- Require U_ref ≤ 1.75 % (half the threshold) before the trigger is evaluated. If that cannot be reached, the trigger is evaluated at 3.5 % + U_ref and the loosening is recorded.
- Cross-check p_n on the axis against Hertz.

**Threshold.** Each judged average must satisfy |e| ≤ 3.5 % + U_ref at R/64 on case (1), and at the finest reachable resolution on case (3).

**The trigger fires if any one of these holds:**
- (a) any judged p_n or Y average misses that threshold;
- (b) case (2) fails a survival check at R/32;
- (c) energy cannot be closed within a tolerance frozen with the trigger once internal energy exists.

There is no "one more variant" clause.

**If it fires.**
- The in-solver interface-state route on particle hosts in OpenCourant ends: no BCT variants, no CS-18c, no CS-19 runs.
- Track B shrinks to WSL B literature work, with no runs until Peter reopens it on new external evidence.
- The first claim moves to track A (D3 iv), with an optional, explicitly reduced 2D axisymmetric one-way study up to jet-root collapse, labelled as such.

## D5. Order of work (optional)

1. **In parallel:** TLSPH internal energy (WSL A) and the boundary-integration literature check (WSL B).
2. **Before any further result:** freeze D4 and refine the 2D reference.
3. The BCT-off survival probe. It is cheap and can kill the route early.
4. The skin and the fitted flat face, judged on T-B2 under D4.
5. The elastic-plastic case.

## Factual claims checked

1. **Input 2, "h ≈ 2Δx": wrong.** h = 1.12 s and the kernel support is 2h = 2.24 s (verification log line 523, §10.3). Its conclusion still holds: 0.5 µm is 1.6 s at R/32 (§22.1), inside the 0.7 µm reach.
2. **The modeller's critique of input 2, item 5 ("wrong ... not in §22"): overstated.** The quad R/128 value is above R/64 for every judged average (`tl_cal4_compare.csv`), so reference drift moves negative errors outward and positive errors inward. Two of the seven R/64 peak-frame misses (p_n at 0.5a, +4.9 %, drift 4.0 %; sphere band 2 on the axis, +3.7 %, drift 3.2 %) lie within the drift. §22.2 itself says p_n at 0.5a could come inside. Band 1 is a real failure, as the critique says.
3. **Input 1, "8–12 % vs ~5 %": outdated.** These are the pre-§22 odds; after §22 they are 6–10 % and 3–5 % (state report, Odds table).
4. **The 0.5 µm choice only checked one spacing (critique item 1): confirmed** by DECISIONS 2026-11-14, item 4.
5. **State report, "the fitted sphere surface is much closer": true only for band averages.** The point values on the sphere side are −16 % (layer 1) and −28 % (layer 2) at R/64 (`tl_cal4_compare.csv`), consistent with the 26–30 % layer-2 deficit in DECISIONS 2026-11-14. The fitted construction also has a layer deficit, which weakens the hope placed in a fitted flat face.
6. **D-1 at 0.285 V against a 0.05 V limit: confirmed** (§14.2).
7. **Input 2, that the literature "proves" corrected particle methods fail the patch test at traction boundaries: unsupported as stated.** Chen, Wu, Yoon and You 2001 (IJNME 50:435–466) set out an integration constraint for linear exactness in *Galerkin* meshfree methods. Its transfer to strong-form TLSPH is not shown by anything I could reach. I read only the abstract and secondary summaries.
8. **Tang 2021 is a master's thesis, not a refereed paper.** Its "discretisation independence" refers to bonded area under an adhesion-energy regularisation (from the thesis record, not read in full).

Sources: [Tang 2021 thesis, UWSpace](https://uwspace.uwaterloo.ca/items/3e65f986-62f4-413c-8570-36a3a1e206e8); [UWSpace record 10012/17030](https://uwspace.uwaterloo.ca/handle/10012/17030); [Chen et al. 2001, SCNI (copy on Scribd)](https://www.scribd.com/document/524084467/chen2000); [SCNI follow-up, core.ac.uk](https://core.ac.uk/download/71316876.pdf).
