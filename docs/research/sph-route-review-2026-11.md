# The SPH route for cold-spray interface modelling: what was tried and where it stopped (2026-11-03 to 2026-11-13)

**Purpose.** A self-contained account for a reader who has not followed the work. It is written by the modeller
who designed most of the route, so it is not independent.
- **Reviews:** an independent critique
  ([sph-route-review-2026-11-critique.md](sph-route-review-2026-11-critique.md)) and a meta-review
  ([sph-route-review-2026-11-meta.md](sph-route-review-2026-11-meta.md)) were applied to this text. Their corrections
  are edited in, and the change log at the end lists them.
- **Sources:** every number carries one. "§n" means `docs/research/opencourant-verification.md`; "fork" means the
  private repository `sph-hvi-contact`, a fork of the OpenCourant explicit solver (AGPL), with files named by their
  path and commit.
- **Labels:** statements marked *interpretation* are readings, not results.

## 1. The problem

**The physics.** In cold spray, a metal particle 15–25 µm across hits a substrate at 500–1100 m/s, below the melting
point. It bonds only where the native oxide (5–25 nm) breaks up and fresh metal meets fresh metal under pressure.
The candidate interface law is Bay-type cold welding: a point bonds when its surface expansion Y exceeds a threshold
Y′ while the normal pressure p_n exceeds an extrusion pressure.

**What the model must deliver** (project owner's requirement):
- particle and crater shape;
- rebound and critical velocity;
- the interface state at the contact edge: Y, p_n, temperature, bonded area.

It must be 3D, with the bond acting inside the solver during the impact.

**Amended 2026-11-13 and 2026-11-14:** the interface outputs are judged as averages over a stated length, 0.5 µm
(DECISIONS 2026-11-14), not as point values at the edge. Point values are reported only.

## 2. Why SPH, and how it was judged

**Lagrangian finite elements failed first.** At the jet root the contact-edge elements collapse, and they collapse
**earlier as the mesh is refined:**
- 2D axisymmetric quads (§8.3): the coarse mesh survives at every speed. The medium mesh fails at 0.20 and 0.10 of
  the penetration time at 750 and 1000 m/s. The fine mesh fails at 0.37, 0.08 and 0.05 at 500, 750 and 1000 m/s.
- 3D bricks under SPH: 0.07–0.17 D/V (§10.5).
- Brick on brick: 0.04–0.16 D/V (§13).

The edge plastic strain does not converge either. Heat conduction (k = 237 W/(m K)) does not change this at the
spacings reached, because its diffusion length (0.17–0.30 µm) is only 1–2 spacings at R/48 (§13.4, hunch CS-13c
refuted). SPH was chosen because it survives large distortion.

**How it was judged.** The steps were judged against exact references (1D wave solutions, Hertz contact).
- **Freezing:** most rungs had numeric thresholds frozen in a commit before any run. The solver's own SPH rungs (S0,
  S1) had none. The rule used for them under the stabilised settings (§15) was relative, and set beforehand by the
  project owner.
- **No tuning:** a failing rung meant stop and report.
- **Calibration:** the references and thresholds were not calibrated against a method known to work on the same
  decks before freezing. That gap matters in H5 and §5.

## 3. The hurdles, in order

**H1. SPH bodies in the solver are welded through the kernel** (§9.8, §10.3).
- The neighbour search and the force routine have no part filter, so two SPH bodies act as one continuum: no
  separation, no slip.
- In a striker/target column the striker is pulled back to −0.93 V, where the exact answer is 0.
- A sphere on an SPH block (W0) is 19–37 % too stiff, and its result depends on where the sphere starts.

**H2. SPH particle on brick substrate.**
- With the solver's own contact (TYPE7), elastic Hertz passes: peak 1.037, approach 0.987, rebound 0.992 at R/32
  (F0, §10.2).
- In an Al–Al impact the substrate bricks collapse at the contact edge (§10.5), as in §2. The contact never bonds.

**H3. A new separable SPH–SPH contact, written in the fork** (body filter plus penalty contact, surface expansion,
cohesive bond; fork `hvi/VERIFY-RESULTS.md`, §14). Frozen ladder: `sph-contact-ladder.md` @ 36c34bd.
- **The basic laws pass:** flat contact (B-1), no force without contact (A-2), surface expansion under stretch (C-1,
  within 0.27 %), cohesive separation (D-2: time 3.6 %, energy 1.000).
- **The surface normals fail at the defaults:** C-3 (sphere normals, maximum tilt 32° against 5°) and C-2 (Nanson
  area under rotation). A cone-and-fit normal passes C-3, but it is not the default.
- **Hertz fails.** B-2 at R/32: approach +16 %, peak 0.86–1.01, rebound 0.84–0.89 against limits of 5 % and > 0.9.
  B-3 (start-distance independence) misses by 6.6 % against 1 %.
  - Contact chatter damping took 17–24 % of the initial kinetic energy at R/32 and explains most of the rebound loss
    there.
- **Diagnosis, from runs with predictions recorded beforehand,** found two causes in the SPH bodies, on top of the
  contact's own normal and chatter problems:
  - (a) Separating the bodies cuts each body's kernel at the interface. The surface layer gets a wrong stress
    gradient, and the block's top layer buckles into a checkerboard.
  - (b) The tensile instability of SPH. A bonded bar under tension misses the exact solution by 0.285 V (D-1); a
    welded bar with none of the new code still misses by 0.073 V.

**H4. The solver's own repairs** (artificial stress ξ = 0.3 plus kernel-correction order 1).
- **What they fix:** B-2 at R/32 comes inside the limits: 1.035 / 0.981 / 0.983 (§14.3, diagnostic).
- **What they break:** the solver's own SPH rungs, by the owner's relative rule (§15):
  - the confined column (S0) gets 4 of 12 numbers inside;
  - the Hertz sphere on a rigid wall (S1) gets 11 of 12. The one miss is the rebound at R/64, which falls over three
    resolutions: 0.993, 0.985, 0.966 against an exact 0.9996. Nine of the twelve S1 numbers improve under the
    repairs, and the frozen set-up's rebound also falls from R/32 to R/64 (0.985 → 0.980). The frozen set-up's S1 was
    not a clean pass either (peak 1.19 at R/16).
- **Cause, from a split test:** order 1 alone. Part of it is an artefact of the symmetry planes; part is a real
  change of the bulk response, independent of width (+17 to +18 % force spike at first contact, contact time 2 %
  short). The settings were not adopted.

**H5. Total Lagrangian SPH, implemented in the fork** (reference kernels, first-order corrected gradients, hourglass
control, own pair viscosity, no reference update; fork `hvi/SPEC-TL.md`, branch `tlsph` eac1040b2; §16). Frozen
ladder: `sph-tlsph-ladder.md` @ 583912a.
- No-TL regression passes.
- **The first physics rung fails:** the elastic confined column, T-S0.
  - Contact time is 1.49 % short at 100 particles and 1.10 % at 200 (limit 1 %).
  - Rebound is 0.942 at 100 (limit ≥ 0.95).
  - The plateau settles at 1.0066.
- **No better than the collocated form in this bulk test:** at 200 particles the old collocated SPH is closer to
  exact on all three numbers.
- **The diagnosis afterwards** (§17; diagnostics, not verdicts) explains most of the failure:
  - **The plateau offset is finite strain.** It scales with velocity (0.65, 0.33 and 0.16 % at V, V/2 and V/4) with
    the same coefficient as the finite-element quads, and the frozen reference was linear. That is a flaw of the judge,
    not of the method.
  - **The contact-time error** is that offset plus about one particle spacing, to which the viscosity and the
    hourglass term both contribute.
  - **The viscosity** causes a little over half of the rebound loss. With it off, the rebound is 0.984 at 200
    particles.
  - **The start spike** (+20 to +21 %, against +17 to +18 % for collocated order 1) is a transient of the wall force,
    not a stress peak in any layer.
  - **The surface layer is wrong in the steady state.** The first two particle layers at the wall carry 0.655 and
    0.845 of the true stress, so the particle stress there is not the traction. Collocated order 1 shows a wider,
    alternating pattern over more than ten layers.
- **The hunch (CS-18) is refuted by its frozen rule.** The cold-spray survival rung was never reached.

**Literature** (`tlsph-literature-check.md`; `data/profizi2016_reading.md`, read in full):
- Profizi, Combescure & Ogawa (C. R. Mécanique 2016, and the 2016 thesis) used TLSPH with a first-order correction,
  pinball contact and a cohesive pair law for Al-on-Al cold spray. Their runs were at R/5 (about 5 particle spacings
  across the radius). Finer meshes failed at 600–900 m/s, and the author concludes that the total Lagrangian form
  lacks stability at high speed and recommends updated Lagrangian.
- **No test against exact references** was found in the SPH cold-spray work read.

## 4. The common thread (interpretation)

1. **The required interface quantities live where every SPH variant was least accurate.** Y, p_n and the bond are
   read off the one or two particle layers next to a surface. The evidence:
   - collocated bodies have truncated kernel sums there (H3a);
   - corrected bodies, both collocated order 1 and TLSPH, carry a stress there that differs from the traction (H5,
     §17: 0.655 and 0.845 at the wall);
   - the contact's normals fail at the defaults (H3).

   The T-S0 *failure* itself is a bulk test and is not evidence for this point. Its layer profile is.
2. **The elastic rungs demand sub-spacing accuracy.** At R/32 the Hertz approach is about 0.8 particle spacings,
   and the contact patch is about 5 spacings in radius.
3. **SPH's main strength is not needed here.** SPH earns its place where bodies fragment; cold spray does not
   fragment. The bulk ratio of impact speed to sound speed (about 0.1–0.2) says little about the contact edge, where
   jetting is a wave effect. The decisive physics sits in the surface layer.
4. **The edge may not converge in any method.** The contact edge did not converge in any host tried (2D FE, 3D FE, FE
   with conduction at reachable spacings, SPH). Point values of Y and p_n at a moving, localising edge may need a
   physical length scale to exist at all. If so, that limit belongs to the problem, not to SPH.

## 5. Where the judge was part of the problem

- **The reference of the 1D column was linear.** It ignored the finite-strain offset (0.42·V/c_d), which used about
  two thirds of T-S0's 1 % budget before the method was judged (§17).
- **The thresholds were not calibrated.** The 1 % and 5 % values came from finite-element expectations and were not
  checked against a method known to pass on the same decks. The collocated host itself would miss the TLSPH column
  rule at 100 particles (rebound 0.9485 against 0.95).
- **Settings were judged at uncalibrated defaults.** The rungs judged the viscosity and hourglass settings as much as
  the formulation. With a no-tuning rule in force, the gate could not separate calibration from method failure. This
  is plausibly connected to the work that continued past a stop rule (H3, §9), but that link is not shown.
- **One clause was badly designed.** "Errors must not grow from 100 to 200 particles" had no noise floor. It failed
  on a converged plateau. The verdict does not depend on it.
- **Counter-argument:** a host that cannot reproduce elastic Hertz contact within 5 % at R/32 gives no basis for
  trusting interface states, which are smaller, later and more local than a Hertz peak. It shows this for this
  solver at these resolutions, not for SPH as a method.
- **Consequence adopted for the follow-up (CS-18b):** a calibration phase before the freeze. It covers finite-strain
  references, thresholds checked against methods known to pass, and settings chosen on calibration cases that are not
  rungs.

## 6. What is not known

- **Convergence.** Whether any of the corrected forms converges in rebound and edge quantities. TLSPH stopped before
  its convergence rungs.
- **The surface-layer stress.** Why the corrected end layers carry the wrong stress. The leading reading (not tested)
  is that the correction makes the end-layer deformation gradient exact while the truncated pair-force sum is not
  corrected.
- **The plastic regime.** Whether surface-layer errors still matter once the flow is plastic over many spacings.
  There is no evidence at impact speed beyond two single probes at R/16.
- **The welded SPH bar.** Why it misses the exact tension wave by 0.07–0.09 V in every set-up.
- **A physical length scale.** Whether one regularises the edge at resolutions finer than those reached. Conduction
  was refuted only at reachable spacings (§2).

## 7. Options an outsider should weigh (no recommendation here)

| Option | Addresses | Known cost or risk |
|---|---|---|
| Updated-Lagrangian SPH with corrected gradients and stabilisation (e.g. Gil, Lee et al. 2022) | large strain; what Profizi recommends | tensile instability and zero-energy modes return; a second new formulation |
| FE with remeshing or ALE, plus a cohesive or Bay interface element (e.g. Kebriaei 2014 for roll bonding), in a commercial code | sharp interface, element-level surface area | licence; Eulerian or ALE smears the interface; the remeshing quality at the jet root is unknown. OpenCourant has no Lagrangian remeshing for 2D quads (§8.2) |
| Material point method | large deformation with a grid for gradients | multi-body contact on a grid; surface definition |
| Peridynamics (e.g. arXiv:2403.01311, cold spray with oxide) | fracture, oxide break-up | non-local surfaces, calibration; not examined |
| Reduced models: a particle-level contact rule for build-up, or approximate Y(r, t) and p(r, t) fields plus Bay's law | avoids resolving the interface | phenomenological; validity range limited |

## 7a. Requirements conflict

The critique's first three steps would each change the owner's requirements:
- a 2D axisymmetric test of whether edge quantities converge (the requirement is 3D);
- band-averaged outputs (the requirement is the edge state);
- a one-way coupled bond (the requirement is an in-solver bond).

**The owner kept the requirements** (CS-18b, 2026-11-13). The 2D edge-convergence test is the one result that could
justify revisiting them. Running it is a decision for the owner, not a technical default.

## 8. Questions for an independent expert

1. Has any particle method been shown to reproduce elastic Hertz contact between two deformable bodies within about
   5 % at a contact radius of about 5 spacings? If so, with what formulation?
2. Is it realistic to read surface expansion and contact pressure at a moving contact edge to within 10 %, with
   convergence, from SPH, updated-Lagrangian SPH or MPM at 3D resolutions of R/32 to R/48?
3. For cold spray, would you host a Bay-type interface law in FE with adaptive remeshing instead of a particle
   method? What is known about convergence of edge quantities there?
4. Are the thresholds (1 % on 1D wave quantities, 5 % on Hertz) appropriate for judging a host for interface laws,
   or should the judge use impact-regime references instead? If the latter, which references?
5. What does the 2D-axisymmetric literature show for edge-quantity convergence, if a single normal impact were
   accepted for a first claim?
6. Is the oxide-scale interface (5–25 nm against 15 µm) better handled as a pure sub-model fed by a coarser bulk
   simulation, one-way coupled, despite the owner's wish for an in-solver bond?

The critique answers these partly from recall. Those answers are checked in
[sph-route-expert-answers-check.md](sph-route-expert-answers-check.md).

## 9. Cost so far, and what the process caught

**Cost:** eleven days (2026-11-03 to 2026-11-13):
- a fork with six new engine files (2 372 lines: contact, surface, bond and output, then TLSPH), plus hooks in
  existing routines;
- 140 result rows in the `hvi_*` and `tl_*` CSVs of `opencourant/results/` (by 2026-11-13), besides the earlier
  OpenCourant verification campaigns;
- three frozen ladders and five hunches on the method side: CS-11 (inconclusive), CS-13 / 13b / 13c (13c refuted),
  CS-18 (refuted).

**What the process caught:**
- The stop rules ended three tracks early: the thermal path, S′, and TLSPH at T-S0.
- Predictions committed before runs exposed several wrong expectations, the modeller's included: "the elastic host
  rungs likely pass" (CS-18) and "S0 at S′ will pass".
- An independent referee overruled one of the modeller's proposals: judging D-1 against the welded bar.

**Process faults:**
- some results were first kept only locally, on uncommitted binaries, and recovered later (§14);
- the fork worked past the B-2 stop rule without a decision, and two impact probes (E-1) ran without one; one threw
  particles out. Both were approved afterwards;
- the judges were frozen without calibration (§5), and a growth rule had no noise floor;
- the TLSPH hourglass-amplitude question (a factor 2 between sources) and the journal check of its equations are
  still open.

## Change log

- **2026-11-13, b339744:** first version.
- **2026-11-13, after the critique:** four number corrections and five accepted omissions, first appended as a
  closing section.
- **2026-11-13, after the meta-review** (this version): all corrections edited into §§2–6.
  - §2: the 2D failure figures corrected (they were mis-assigned to meshes); freezing and calibration stated as they
    were; conduction refuted only at reachable spacings.
  - §3: normals, chatter and S1 caveats added in H3 and H4; "diverges" removed; the start spike given as +20/21 against
    +17/18 %; the §17 diagnosis added to H5.
  - §4: the T-S0 failure no longer cited as surface-layer evidence; the §17 layer profile cited instead; the
    edge-convergence point added.
  - §5: rewritten (finite-strain reference, calibration).
  - §6: updated.
  - §7a: added (requirements conflict).
- **2026-11-13, requirement amended** (DECISIONS 2026-11-13): §1 states that the edge state is averaged over a stated
  length.
- **2026-11-14:** the averaging length was fixed at 0.5 µm (the first proposal, 0.2 µm, was below one spacing at R/32).
