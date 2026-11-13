# The SPH route for cold-spray interface modelling: what was tried and where it stopped (2026-11-03 to 2026-11-13)

**Purpose.** A self-contained account for a reader who has not followed the work. It is written by the modeller
who designed most of the route, so it is not independent. An independent critique is in
[sph-route-review-2026-11-critique.md](sph-route-review-2026-11-critique.md).
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

## 2. Why SPH, and how it was judged

**Lagrangian finite elements failed first.** At the jet root, the contact-edge elements collapse:
- 2D axisymmetric quads at 0.40 / 0.08 / 0.06 of the transit time at R/16 / R/32 / R/64 (§8.3);
- 3D bricks under SPH at 0.07–0.17 D/V (§10.5);
- brick on brick at 0.04–0.16 D/V (§13).

They fail **earlier as the mesh is refined,** and the edge plastic strain does not converge. Heat conduction does
not regularise it (§13, hunch CS-13c refuted). SPH was chosen because it survives large distortion.

**How it was judged.** Every step was judged against exact references (1D wave solutions, Hertz contact), on rungs
whose thresholds were frozen in a commit before any run. A failing rung meant stop and report, with no tuning. This
is the project's general method.

## 3. The hurdles, in order

**H1. SPH bodies in the solver are welded through the kernel** (§9.8, §10.3).
- The neighbour search and the force routine have no part filter, so two SPH bodies act as one continuum: no
  separation, no slip.
- In a striker/target column the striker is pulled back to −0.93 V, where the exact answer is 0.
- A sphere on an SPH block (W0) is 19–37 % too stiff, and its result depends on where the sphere starts.

**H2. SPH particle on brick substrate.**
- With the solver's own contact (TYPE7), elastic Hertz passes: peak 1.037, approach 0.987, rebound 0.992 at R/32
  (F0, §10.2).
- In an Al–Al impact the substrate bricks collapse at the contact edge (H0 of §10.5), as in §2. The contact never
  bonds.

**H3. A new separable SPH–SPH contact, written in the fork** (body filter plus penalty contact, surface expansion,
cohesive bond; fork `hvi/VERIFY-RESULTS.md`, §14). Frozen ladder: `sph-contact-ladder.md` @ 36c34bd.
- **The laws pass what they were written to do:** flat contact (B-1), no force without contact (A-2), surface
  expansion under stretch (C-1, within 0.27 %), cohesive separation (D-2: time 3.6 %, energy 1.000).
- **Hertz fails.** B-2 at R/32: approach +16 %, peak 0.86–1.01, rebound 0.84–0.89 against limits of 5 % and > 0.9.
  B-3 (start-distance independence) misses by 6.6 % against 1 %.
- **Diagnosis, from runs with predictions recorded beforehand,** found two causes, both in the SPH bodies and not in
  the contact law:
  - (a) Separating the bodies cuts each body's kernel at the interface. The surface layer gets a wrong stress
    gradient, and the block's top layer buckles into a checkerboard.
  - (b) The tensile instability of SPH. A bonded bar under tension misses the exact solution by 0.285 V (D-1); a
    welded bar with none of the new code still misses by 0.073 V.

**H4. The solver's own repairs** (artificial stress ξ = 0.3 plus kernel-correction order 1).
- **What they fix:** B-2 at R/32 comes inside the limits: 1.035 / 0.981 / 0.983 (§14.3, diagnostic).
- **What they break:** the solver's own SPH rungs, by a rule fixed beforehand (§15):
  - the confined column (S0) gets 4 of 12 numbers inside;
  - the Hertz sphere on a rigid wall (S1) gets 11 of 12, and its rebound **falls with refinement**: 0.993, 0.985,
    0.966 at R/16, R/32, R/64, against an exact 0.9996.
- **Cause, from a split test:** order 1 alone. Part of it is an artefact of the symmetry planes; part is a real
  change of the bulk response, independent of width (+17 % force spike at first contact, contact time 2 % short).
  The settings were not adopted.

**H5. Total Lagrangian SPH, implemented in the fork** (reference kernels, first-order corrected gradients, hourglass
control, own pair viscosity, no reference update; fork `hvi/SPEC-TL.md`, branch `tlsph` eac1040b2; §16). Frozen
ladder: `sph-tlsph-ladder.md` @ 583912a.
- No-TL regression passes.
- **The first physics rung fails:** the elastic confined column, T-S0.
  - Contact time is 1.49 % short at 100 particles and 1.10 % at 200 (limit 1 %).
  - Rebound is 0.942 at 100 (limit ≥ 0.95).
  - The plateau settles at 1.0066.
- **No better than the collocated form:** at 200 particles the old collocated SPH is closer to exact on all three
  numbers.
- **Readings, not verdicts:**
  - the viscosity removes 5.6–15.7 % of the kinetic energy;
  - the plateau and a +21 % start spike match the collocated order-1 runs.
- The hunch (CS-18) is refuted by its frozen rule. The cold-spray survival rung was never reached.

**Literature** (`tlsph-literature-check.md`; `data/profizi2016_reading.md`, read in full):
- Profizi, Combescure & Ogawa (C. R. Mécanique 2016, and the 2016 thesis) used TLSPH with a first-order correction,
  pinball contact and a cohesive pair law for Al-on-Al cold spray. Their runs were at R/5 (about 5 particle spacings
  across the radius). Finer meshes failed at 600–900 m/s, and the author concludes that the total Lagrangian form
  lacks stability at high speed and recommends updated Lagrangian.
- **No test against exact references** was found in the SPH cold-spray work read.

## 4. The common thread (interpretation)

1. **The required interface quantities live where SPH is weakest.** Y, p_n and the bond are read off the one or two
   particle layers next to a surface. Every variant tried was least accurate there:
   - truncated kernel sums;
   - instability in tension;
   - correction terms that change the end layers (H4, H5).
2. **The elastic rungs demand sub-spacing accuracy.** At R/32 the Hertz approach is about 0.8 particle spacings,
   and the contact patch is about 5 spacings in radius.
3. **The tool comes from a neighbouring regime.** SPH earns its place in hypervelocity impact, where bodies
   fragment. Cold spray does not fragment (impact speed / sound speed ≈ 0.1–0.2). Its decisive physics sits in the
   surface layer, SPH's weak point.

## 5. Where the judge may be part of the problem

- **The thresholds are FE-grade.** The 1 % and 5 % values came from finite-element expectations. The collocated
  host itself would miss the TLSPH column rule at 100 particles (rebound 0.9485 against 0.95).
- **One clause was badly designed.** "Errors must not grow from 100 to 200 particles" had no noise floor. It failed
  on a converged plateau that moved by 0.006 points. The verdict does not depend on it.
- **Counter-argument:** a host that cannot reproduce elastic Hertz contact within 5 % at R/32 gives no basis for
  trusting the interface states the law needs. Those states are smaller, later and more local than a Hertz peak.

## 6. What is not known

- **Convergence.** Whether any of the stabilised forms converges: the S1 rebound under H4 diverges, and TLSPH was
  stopped before its convergence rungs.
- **The plateau offset.** Whether it is finite strain (finite-element quads show +0.69 %) or a discretisation
  effect. A diagnosis with deck switches only is running (WSL A task 2026-11-13-a).
- **The plastic regime.** Whether surface-layer errors still matter once the flow is plastic over many spacings.
  There is no evidence at impact speed beyond two single probes at R/16.
- **The welded SPH bar.** Why it misses the exact tension wave by 0.07–0.09 V in every set-up.

## 7. Options an outsider should weigh (no recommendation here)

| Option | Addresses | Known cost or risk |
|---|---|---|
| Updated-Lagrangian SPH with corrected gradients and stabilisation (e.g. Gil, Lee et al. 2022) | large strain; what Profizi recommends | tensile instability and zero-energy modes return; a second new formulation |
| FE with remeshing or ALE, plus a cohesive or Bay interface element (e.g. Kebriaei 2014 for roll bonding), in a commercial code | sharp interface, element-level surface area | licence; Eulerian or ALE smears the interface; the remeshing quality at the jet root is unknown |
| Material point method | large deformation with a grid for gradients | multi-body contact on a grid; surface definition |
| Peridynamics (e.g. arXiv:2403.01311, cold spray with oxide) | fracture, oxide break-up | non-local surfaces, calibration; not examined |
| Reduced models: a particle-level contact rule for build-up, or approximate Y(r, t) and p(r, t) fields plus Bay's law | avoids resolving the interface | phenomenological; validity range limited |

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

## 9. Cost so far, and what the process caught

**Cost:** eleven days (2026-11-03 to 2026-11-13):
- a fork with six new engine files (2 372 lines: contact, surface, bond and output, then TLSPH), plus hooks in
  existing routines;
- 140 result rows in the `hvi_*` and `tl_*` CSVs of `opencourant/results/`, besides the earlier OpenCourant
  verification campaigns;
- three frozen ladders and five hunches on the method side: CS-11 (inconclusive), CS-13 / 13b / 13c (13c refuted),
  CS-18 (refuted).

**What the process caught:**
- The stop rules ended three tracks early: the thermal path, S′, and TLSPH at T-S0.
- Predictions committed before runs exposed several wrong expectations, the modeller's included: "the elastic host
  rungs likely pass" (CS-18) and "S0 at S′ will pass".
- An independent referee overruled one of the modeller's proposals: judging D-1 against the welded bar.
- **Process faults:** some results were first kept only locally, on uncommitted binaries, and recovered later (§14);
  and a growth rule had no noise floor.

## Corrections after the critique (2026-11-13, modeller)

The independent critique ([sph-route-review-2026-11-critique.md](sph-route-review-2026-11-critique.md)) checked 14
numbers and found four mismatches. They are corrected here rather than in the text above:
1. **§2, the 2D figures.** "0.40 / 0.08 / 0.06 at R/16 / R/32 / R/64" is wrong. In §8.3 the R/16 mesh never failed.
   The finest mesh, R/64, failed at 0.37 / 0.08 / 0.05 t_p for 500 / 750 / 1000 m/s, and failure comes earlier with
   refinement. The conclusion stands.
2. **H5, the start spike.** TLSPH gives +20 to +21 %, collocated order 1 gives +17 to +18 % (§15.9). They are
   similar, not equal.
3. **§6, "diverges".** One quantity under S′ (the S1 rebound) falls over three resolutions. Nine of twelve S1 numbers
   improved under S′, and the frozen rebound also fell from R/32 to R/64 (0.985 → 0.980).
4. **§2, "thresholds frozen before every run".** S0 and S1 had no numeric thresholds under the collocated ladder.
   The S′ rule was relative and set beforehand by Peter, and Addendum 1 was post hoc.

**Omissions the critique names, accepted:**
- contact chatter damping took 17–24 % of the kinetic energy in B-2 at R/32;
- C-2 and C-3 failed at the defaults (normals), so "not in the contact law" is too clean;
- S1 under the frozen set-up was not a clean pass;
- the TLSPH hourglass-amplitude factor-2 question is open;
- the fork worked past the B-2 stop rule, and two E-1 probes ran without a decision (both approved afterwards).

**Two weak points I accept** (the critique's §2):
- **H5 is not evidence for the "common thread."** T-S0 is a bulk 1D test, and its failure is not a surface-layer
  effect.
- **The edge may be unconvergent in any method.** The contact edge did not converge in any host tried (2D FE, 3D FE,
  FE with conduction, SPH). Point values of Y and p_n there may need a physical length scale to exist at all. If so,
  that limit belongs to the problem, not to SPH, and it should be tested directly before another host is built.
