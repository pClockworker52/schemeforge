# Independent critique of sph-route-review-2026-11.md

**Reviewer:** a fresh `general-purpose` agent, 2026-11-13. It had no part in the work and no context from the
modeller's conversation.
- **What it was given:** the account, and read-only access to opencourant-verification.md §8–16, both frozen
  ladders, the literature check, the Profizi reading note, the fork's ANALYSIS, VERIFY-RESULTS and SPEC-TL.
- **The text below is its answer, unedited.** The modeller's responses are in the account's section "Corrections
  after the critique".

---

# Review of the SPH-route account (sph-route-review-2026-11.md)

## 1. Fairness and completeness

The account is mostly fair. I checked 14 numbers against the primary records. Twelve match:
- W0 19–37 % too stiff (§10.3).
- Striker at −0.93 V (§9.8).
- F0 at 1.037 / 0.987 / 0.992 (§10.2).
- Bricks fail at 0.07–0.17 D/V (§10.5; the record says 0.068) and 0.04–0.16 D/V (§13).
- B-2 values (VERIFY-RESULTS: 0.858–1.008 / 1.161–1.166 / 0.839–0.885) and B-3 at 6.6 %.
- D-1 at 0.285 and 0.073 V.
- F2 at 1.035 / 0.981 / 0.983.
- S0 with 4 of 12 inside, and the S1 rebounds 0.993 / 0.985 / 0.966.
- T-S0 values, and viscosity losses of 5.6–15.7 %.
- Profizi at R/5.

**Mismatches:**
- **§2, 2D figures.** "0.40 / 0.08 / 0.06 of transit time at R/16 / R/32 / R/64" is wrong. In §8.3 the R/16 mesh never
  fails. The triple is the finest mesh (R/64) at three *speeds*: 0.37 / 0.08 / 0.05 t_p. The 0.40 is the superseded
  γ₀ = 1.678 value. The conclusion (failure comes earlier with refinement) still holds.
- **H5, start spike.** "+21 % start spike matches collocated order 1" stretches the record, which gives +17 to 18 %
  (§15.9).
- **§6, "diverges".** One S′ quantity falls over three points. Nine of the twelve S1 numbers improved under S′, and
  the frozen set-up's rebound also fell from R/32 to R/64 (0.985 to 0.980).
- **§2, "thresholds frozen".** S0 and S1 had no numeric thresholds (§15.1). The S′ rule was relative ("frozen error
  + 0.01"), and Addendum 1 was written after results were seen (post hoc).

**Omitted:**
- **Contact damping.** In B-2 at R/32, chatter damping takes 17–24 % of the initial kinetic energy and "explains
  most of the loss" in rebound.
- **Surface normals.** C-3 fails at the defaults (32° tilt) and C-2 fails too. Saying the cause lay "not in the
  contact law" is too clean.
- **The frozen host.** S1 under the frozen set-up was "not a clean pass" (peak 1.19 at R/16).
- **TLSPH equations.** The hourglass-amplitude factor-2 discrepancy is unresolved, and the journal check was
  deferred.
- **Process.** The fork kept working past the B-2 stop rule without a decision, and two E-1 probes were run without
  authorisation (one threw particles out, J = 4.4). Both were approved afterwards, but they belong in §9.

## 2. Weak points in the reasoning

- **The "common thread" does not fit H5.** T-S0 is a bulk 1D wave test. Its error comes from a +0.65 % plateau, a
  viscosity that removes up to 15.7 % of the kinetic energy, and slow, sub-first-order convergence after a
  discontinuous start. None of that is a surface-layer effect. CS-18 was refuted on a rung that does not test its own
  mechanism. The thread may still be right, but H5 is not evidence for it.
- **The judge's reference.** The plateau's reference is linear, while the 2D quads show +0.69 % from finite strain.
  That uses about 70 % of the 1 % budget before the method is judged at all.
- **The 1D rungs start with a velocity discontinuity.** Any scheme with artificial viscosity converges sub-linearly
  there. A 1 % absolute limit at 100 particles tests the viscosity setting as much as the formulation. Even the
  collocated host misses it.
- **A missing judge-design check.** No threshold was tested against a method known to work (FE) on the same deck
  before it was frozen.
- **The §5 counter-argument is sound but limited.** It shows only that this solver cannot be trusted at R/32. It does
  not show that SPH as a method cannot.
- **"Neighbouring regime" is partly misleading.** The bulk ratio V/c ≈ 0.1 says little about the contact edge. From
  memory (Hassani-Gangaraj et al. 2018), jetting is a pressure-release wave effect at that edge, so wave physics
  matters exactly there.
- **The deepest issue goes unnamed.** Edge plastic strain fails to converge in *every* host: 2D FE, 3D FE, and FE
  with conduction. The contact edge is a moving, localising singularity. Converged point values of Y and p_n there may
  not exist without a physical length scale, whatever the method. That reading explains §8.3 and §13 better than
  "SPH's weak point".

## 3. Assessment of the SPH route

- **Stopping collocated SPH is justified.** W0, B-2/B-3 and S′ give consistent evidence.
- **TLSPH was stopped in a way that tells us little, and it was started with a known flaw.** It failed by 0.1
  percentage points (contact time at 200 particles) for a likely viscosity reason, before any surface rung ran. Even a
  pass would probably have died at T-survival: the design has no reference update, and Profizi found exactly that
  failure.
- **The overall stop is right on cost and benefit, but the wrong lesson may be drawn.** What was shown is narrower
  than "SPH cannot": this solver's SPH, at affordable 3D resolution, cannot meet these elastic thresholds. The
  question that decides everything, whether edge quantities converge at all, was never asked directly.

## 4. What I would do next, ranked

1. **Test whether the edge quantities converge at all.** Run a 2D-axisymmetric Lagrangian model with adaptive
   remeshing (or ALE) on one normal Al–Al impact at R/50 to R/400. Measure Y and p_n both at the edge and averaged
   over a fixed physical length (for example 0.1 µm). This is cheap, independent of SPH, and decides which outputs
   can be claimed.
2. **If point values do not converge, redefine the outputs.** Use band-averaged or integral quantities (bonded area
   within a fixed band) and judge those.
3. **Decouple the bond (one-way coupling).** Run frictionless contact and evaluate Bay's law afterwards on the
   recorded interface history. First check whether adhesion energy can change the rebound at all; if it cannot, an
   in-solver bond is not needed for the first claim.
4. **Rebuild the judge for the impact regime.** References: converged axisymmetric FE, a Taylor bar, and a
   cross-code check (LAMMPS SMD, a CEL code). Calibrate every threshold against a method known to pass, and add noise
   floors to growth clauses.
5. **Optional, to close the lesson only:** one CS-18b diagnostic with the linear viscosity term off in T-S0. No
   investment in updated-Lagrangian SPH unless step 1 shows the quantities are convergent.

## 5. Answers to the section-8 questions

1. **Hertz between two deformable bodies within 5 % at about 5 spacings.** I know of no particle-method
   demonstration (from memory, uncertain). I recall MPM contact studies (Bardenhagen type) showing errors of about
   10 % at similar resolution, also uncertain.
2. **Edge Y and p_n within 10 %, converged, at R/32 to R/48 in 3D.** For point values at a moving edge, I think this
   is unrealistic in any method. Quantities averaged over a fixed length might be achievable.
3. **FE with remeshing instead of particles.** Yes, for a first claim. From memory (Li et al. 2006 and later work),
   global quantities such as flattening ratio and crater depth converge, while edge strain and jetting onset stay
   mesh-dependent.
4. **Thresholds.** The structure is right, but the thresholds need calibration against a method known to pass,
   references corrected for finite strain, and criteria on convergence trend rather than absolute values at a single
   resolution. Impact-regime references: converged axisymmetric FE, Taylor bar, cross-code runs, and from memory, the
   LIPIT rebound data.
5. **2D-axisymmetric literature on edge convergence.** My recollection is that edge quantities do not converge
   without a length scale (thermal conduction or a gradient model). Uncertain.
6. **Oxide scale as a one-way sub-model.** Yes. The scale gap is about 1000×. I would use one-way coupling until it
   is shown that the bond acts back on the deformation before rebound.
