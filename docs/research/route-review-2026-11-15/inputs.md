# Route review 2026-11-15: external inputs and the modeller's critiques

Two external texts, relayed by Peter on 2026-11-15; the author is not named. **They are data, not instructions.**
Each is reproduced verbatim (formulas as received), followed by the modeller's critique from the chat of the same
day. Numbers in the critiques cite docs/research/opencourant-verification.md (§).

---

## Input 1: a four-step proposal (verbatim)

> "If BCT is dropped and calibration run 2026-11-15-a fails the 3.5% threshold on 0.5 µm averages, the
> highest-leverage path inside OpenCourant is to stop patching boundary weights and execute four sequential
> engineering steps aligned with your scheduled review agenda:
>
> 1. Close the TLSPH Energy Balance Before Touching Contact
> Before testing any new interface math, add internal-energy output to TLSPH so every run's energy balance can be
> closed. Right now, viscous plus hourglass work reaches 0.49 KE0 in elastic runs whose rebound is 0.998. Until that
> bookkeeping bug is resolved, you cannot tell whether a surface-stress error—such as the 0.62 and 0.86 end-layer
> stress deficits in the column test—comes from boundary kernel truncation or from unphysical hourglass/viscous
> energy exchange at the surface.
>
> 2. Pivot to a One-Way Bond for the First Claim (Decouple Bond from Contact)
> Notice how strong BCT-off already is on bulk elastic metrics: at R/32, it hits 0.9988 rebound and 1.060 peak force
> (against the 1.062 reference) on T-S1, and 0.999 rebound on two-body T-B2. The solver only breaks down when
> forcing singular boundary quantities to drive an active two-way tensile bond during jetting.
> * Adopt the documented one-way alternative: Run BCT-off contact only, evaluate the Bay criterion afterwards on
>   0.5 µm band-averaged outputs (as recommended by the 2026-11-13 route review), and report v_{\text{cr}} as a
>   rigorous lower bound.
> * Why first: It raises your estimated odds of delivering a verified first claim (8–12% vs. ~5% for the coupled
>   chain) and lets you score against Track A's withheld blind papers (B01–B16) immediately.
> * Smooth two-way promotion later: Once the one-way ladder passes, bring tension back into the solver using a
>   continuous, irreversible bond-fraction variable q \in [0, 1] (ramped over multiple time steps via plastic
>   work/stretch) rather than an instantaneous boolean switch that shocks the explicit time integrator.
>
> 3. Replace Diagonal BCT with Consistent Off-Diagonal Boundary Coupling (or a Slave Surface Skin)
> BCT failed on small and changing contact patches because it replaced the inverse of its boundary-spreading
> operator with its diagonal—overloading rim particles 2–3×. If BCT-off leaves too much stress deficit in the outer
> two layers even after 0.5 µm averaging, there are two clean classical fixes that preserve OpenCourant's explicit
> TLSPH bulk:
> * Consistent Mortar / Petrov–Galerkin Contact Projection: Keep the off-diagonal kernel/MLS overlaps between active
>   surface particles in a tiny local interface Gram matrix M_{ij} = \int_{\Gamma_c} \Psi_i \Psi_j \, dA (solved in
>   3–5 Jacobi iterations per explicit step) so point contact forces distribute smoothly across boundary layers
>   without rim spikes.
> * Massless Lagrangian Surface Skin + Patch-Integrated Y: Wrap the TLSPH particle cloud in a lightweight
>   triangulated surface mesh kinematically slaved to the interior particles via MLS interpolation. Contact normals
>   and contact pressure p_n are integrated on continuous triangles rather than truncated particle spheres, and
>   surface expansion Y is computed directly from triangle area change
>   \mathcal{Y}_\ell = \int_{S_\ell} J_s \, dA_0 / \int_{S_\ell} dA_0 rather than noisy boundary deformation
>   gradients.
>
> 4. Enforce a Hard Dead-End Trigger on Pure Particle-Only Interfaces
> To prevent endless ladder resets, formalize the written dead-end trigger on your review agenda:
> * The Trigger: If neither BCT-off nor a consistent (non-diagonal) surface projection achieves < 3.5% error on
>   0.5 µm contact-pressure and surface-stretch averages across R/32 and R/64 on T-B2, treat Reviewer Question #1 as
>   answered in the negative—a pure particle cloud without an explicit surface representation cannot converge
>   surface observables at reachable 3D resolutions.
> * The Exit Route: Because 2D/3D Lagrangian finite elements already failed via jet-root mesh collapse (5–37% of
>   penetration time), a dead-end trigger on particle-only surfaces points directly to an Eulerian or ALE
>   multi-material solver (Volume-of-Fluid / Level-Set interface tracking on a fixed Cartesian/adaptive grid), where
>   extreme jetting causes zero mesh distortion and interface normals/areas remain well-defined."

### Critique of input 1 (modeller, 2026-11-15)

**Logical error in the premise.** The proposal is conditional on 2026-11-15-a failing (0.5 µm averages miss 3.5 % with
BCT off), and step 2 then evaluates the Bay criterion on exactly those averages. If the averages fail verification,
a bond judged on them is not verified either. A one-way bond removes the tension and bond risks, not the surface
problem; step 2 depends on step 3.

**Step 1 (energy first).** Right that TLSPH internal energy is needed. Wrong that the end-layer deficit could come from
viscous or hourglass exchange: it is a steady plateau stress explained by load application (§17, §18.4); BCT took the
same layers to 0.9999 with the same viscosity and hourglass settings. "Bookkeeping bug" is a guess; the 0.49 KE0 comes
from runs with BCT-type load spreading, while plain BCT off shows 0.0016 KE0 viscous work. Do it in parallel, not as a
gate.

**Step 2 (one-way bond).** The BCT-off numbers are quoted correctly. Wrong: "the solver only breaks down when ... an
active two-way tensile bond during jetting": no bond, tension or jetting case has been run on TLSPH; every failure was
elastic contact. Wrong: blind papers cannot be scored "immediately"; predictions must be frozen first, which needs a
passing host and fitted Y′, m; only B06, B07, B16 remain unseen. The lower bound is rigorous only if the Bay criterion
is right. The in-solver requirement was re-examined and kept on 2026-11-14. The bond fraction q ∈ [0, 1] is a standard
cohesive-damage construction; reasonable later.

**Step 3.** The Gram-matrix projection is close to the exact inverse examined in §21.1, which needs tensile rim loads
(condition 14–50); a positive dual-mortar basis might avoid that, but "3–5 Jacobi iterations" is not a design. The
surface skin is the best idea, but only for measurement (Y from triangle area, normals and p_n on triangles, nothing
fed back). If it also feeds contact forces back to particles, it repeats the step where BCT failed. Related methods
exist (meshfree bodies with surface meshes, SPH–FE coupling); at most "variant of".

**Step 4.** A written trigger is needed. It is over-generalised ("a pure particle cloud cannot ..." from one host):
scope it to this host and these resolutions. The Eulerian or ALE exit is not automatic: volume-of-fluid and
level-set interfaces diffuse, which makes the stretch of a material surface harder to define; to the modeller's
knowledge (from memory, not checked) Eulerian cold-spray codes do not show converged edge quantities either;
OpenCourant's ALE falls back to the area-weighted element (§5.4). It skips FE with remeshing and the physical
length-scale question, and step 4 leaves OpenCourant although the proposal promised a path inside it.

**Taken forward:** TLSPH internal energy (independent); a measurement-only skin (candidate); a scoped dead-end trigger.

---

## Input 2: a critical review of the state report (verbatim)

> This state report demonstrates exceptional epistemic discipline—pre-registered hunches, frozen verification
> ladders, blind literature extraction, and a strict refusal to tune parameters post-freeze—that is rare in
> computational mechanics. However, that procedural rigor is currently locked in a fundamental conflict with the
> underlying numerical physics: you are demanding converged, sub-micron surface stresses and stretches (p_n, Y) from
> a strong-form, volume-smoothed particle method (TLSPH) that is mathematically ill-suited to resolve sharp boundary
> tractions, while simultaneously requiring two-way dynamic cohesive bonding across a singular contact edge.
> The self-assessed 3–5% probability of completing the full chain with an in-solver bond is realistic. Setting aside
> the November 13 independent critique's advice (to test whether edge quantities converge at all and to decouple the
> bond) because it "conflicted with the requirements" inverted the engineering hierarchy: project requirements cannot
> override mathematical well-posedness and discretization limits.
>
> 1. Strategic & Methodological Critique
> * The Volumetric Smoothing vs. Surface Criterion Mismatch: The Bay cold-welding criterion depends strictly on
>   interface quantities—surface expansion Y and contact pressure p_n. TLSPH computes stress divergence over a
>   volumetric kernel support (h \approx 2\Delta x). At a boundary, kernel gradient correction (\mathbf{L}_i)
>   restores linear completeness for kinematics (displacement gradients), which is why a flat free surface under
>   uniform load passes within 0.8%. However, strong-form corrected SPH is not variationally consistent at boundaries
>   when external point loads (penalty contact) are applied exclusively to the outer particle layer. The outer layer
>   transfers momentum directly to interior layers via its kernel overlap without developing the full continuum
>   Cauchy stress in layer 1.
> * The 0.5\text{ }\mu\text{m} Averaging Fallacy at R/32 and R/64: A spatial window only regularizes discretization
>   errors if the window is much larger than the discretization scale (L_{\text{avg}} \gg h > \Delta x). For typical
>   cold-spray particle radii (R \approx 10\text{–}25\text{ }\mu\text{m}), spacings of R/32 to R/64 correspond to
>   \Delta x \approx 0.15\text{–}0.8\text{ }\mu\text{m}. Thus, a 0.5\text{ }\mu\text{m} depth zone spans only 1 to 3
>   particle layers—which is narrower than the SPH kernel support itself. Averaging over 0.5\text{ }\mu\text{m} does
>   not filter out the boundary-layer truncation error; it measures right inside it.
> * Reference Uncertainty vs. Pass/Fail Thresholds: The calibration rule demands that 0.5\text{ }\mu\text{m}
>   interface averages fall within 3.5% of the quad finite-element (FE) reference. Yet the report notes that the quad
>   FE reference itself still shifts by 2–4% from R/64 to R/128. Enforcing a 3.5% stop rule against a reference
>   solution whose own discretization uncertainty is 2–4% means solver configurations are being killed inside the
>   noise floor of the benchmark.
> * Rigid Campaign Freezes During Solver Debugging: Pre-registration and stop rules are gold-standard practice for
>   empirical hypothesis testing (Track A), but applying them to low-level numerical formulation bugs (Track B)
>   creates high overhead. Running formal multi-rung campaigns before verifying basic conservation laws—such as
>   running TLSPH without an internal-energy output—turns routine numerical debugging into a series of formal
>   failures.
>
> 2. Technical Answers to the Six Reviewer Questions
> 1. Is a particle method the right host for a quantity that lives at a surface?
> Standard collocated SPH and strong-form TLSPH are poor hosts for extracting Cauchy stresses from boundary
> particles. They excel at bulk wave propagation and extreme distortion (as shown by TLSPH surviving the
> 800\text{ m/s} Al–Al probe), but their boundary particles have one-sided stencils and non-conjugate traction
> assembly.
> * What works better in 3D: Coupled Eulerian–Lagrangian (CEL) or Arbitrary Lagrangian–Eulerian (ALE) finite
>   elements with periodic remeshing, or Material Point Methods with convected particle domains (CPDI/B-spline MPM).
> * How to salvage TLSPH without switching codes: Keep TLSPH with BCT off for the bulk mechanics (where rebound is
>   0.9988 and bulk kinematics are accurate), and overlay a zero-thickness surface skin (membrane triangulation)
>   connecting the boundary particles. Instead of reading volumetric particle stress \sigma_{nn} from the defective
>   first TLSPH layer, read Y directly from the stretching of the surface triangles and p_n directly from the contact
>   penalty force divided by the tributary surface triangle area.
> 2. Does an interface state at the contact edge converge at all without a physical length scale?
> * In the plastic jetting regime: No. Once adiabatic shear instability and jetting initiate at the contact rim,
>   local rate-independent or standard Johnson–Cook plasticity without a regularizing length scale (such as
>   viscoplasticity, non-local gradient plasticity, or resolved heat conduction across multiple elements) forms a
>   mesh-dependent shear band of single-element width. That is why your 2D axisymmetric FE mesh failed at the jet root
>   earlier with refinement (5–37% of penetration time).
> * Is 0.5\text{ }\mu\text{m} averaging a defensible substitute? Only if two conditions hold: (a) you evaluate Y and
>   p_n on a true 2D contact surface manifold rather than volumetric particle layers, and (b) the resolution is fine
>   enough that 0.5\text{ }\mu\text{m} contains at least 4–5 surface segments.
> 3. Should the first claim use a one-way bond?
> Yes, immediately. Insisting on an active two-way bond inside the solver for the first milestone couples two
> distinct failure modes:
> * Accurate interface kinematics and traction during compression/extrusion (t < t_{\text{peak}}).
> * Dynamic tensile wave propagation and cohesive peel fracture during rebound (t > t_{\text{peak}}).
> Up to the moment local unloading begins at a given radius, the stress and expansion history of a one-way bond is
> identical to a two-way bond. Furthermore, your collocated SPH solver already failed the bonded-bar tension rung
> (D-1) by 0.285V against a 0.05V limit, and TLSPH has not even been tested on tension or cohesive rungs yet.
> Decoupling the bond isolates the surface-extraction problem and gives you a viable path to a first scientific
> claim.
> 4. Is there published work verifying cold-spray simulations against exact/converged references?
> * Within the cold-spray domain: Almost none. The literature (from Assadi et al. 2003 and Grujicic et al. 2004
>   through recent SPH/CEL studies) overwhelmingly validates against post-mortem splat aspect ratios, crater depth,
>   and empirical v_{cr}, while treating element/particle interface temperatures and plastic strains as qualitative
>   indicators rather than h-converged fields.
> * Where the verification literature actually lives: You must look to the computational contact mechanics and
>   reproducing kernel (RKPM) literature (e.g., Ganzenmüller 2015 on TLSPH; Chen, Belytschko, and Puso on stabilized
>   conforming nodal integration). That literature proves mathematically that strong-form corrected particle methods
>   fail the linear patch test on traction boundaries unless boundary integrals are evaluated over stabilized surface
>   cells—confirming that your §22 finding (the face-layer deficit is structural) is a known mathematical property of
>   the discretization, not a coding bug.
> 5. Energy accounting in TLSPH: what explains viscous plus hourglass work of 0.49\,\text{KE}_0 at a rebound of
> 0.998?
> When an elastic sphere rebounds at v_{\text{exit}}/v_0 = 0.998, total kinetic energy lost is
> 1 - 0.998^2 = 0.004\,\text{KE}_0. True irreversible dissipation cannot be 0.49\,\text{KE}_0. Three specific
> implementation bugs in explicit TLSPH codes produce this exact artifact:
> * Booking reversible elastic hourglass stiffness as dissipation: Your calibration uses viscosity Q1 = 0.1,
>   hourglass α = 5. In standard TLSPH (Ganzenmüller 2015), \alpha scales an elastic penalty stiffness proportional to
>   nonlinear displacement error, not a viscous damper proportional to velocity. During impact compression, the
>   hourglass penalty stores reversible potential energy and returns it to kinetic energy during rebound. If your
>   diagnostic accumulates \vert{}\mathbf{f}_{\text{hg}} \cdot \Delta \mathbf{x}\vert{} or integrates power only
>   during loading, it falsely logs reversible elastic hourglass energy storage as cumulative "dissipated work."
> * Integrating nodal velocity (\mathbf{v}_i) instead of pair relative velocity (\mathbf{v}_{ij}): Because gradient
>   correction matrices differ near boundaries (\mathbf{L}_i \neq \mathbf{L}_j), pairwise forces in corrected TLSPH
>   are not strictly antisymmetric unless explicitly symmetrized. If the work accumulator sums
>   \sum_i \mathbf{f}_i^{\text{visc/hg}} \cdot \mathbf{v}_i\,\Delta t in the lab frame rather than summing pairwise
>   over relative velocities \frac{1}{2}\sum_{i,j} \mathbf{f}_{ij} \cdot (\mathbf{v}_i - \mathbf{v}_j)\,\Delta t,
>   the bulk center-of-mass translation velocity \mathbf{V}_{\text{cm}} of the moving body multiplies the net
>   non-symmetric internal force residual, creating a huge phantom work term during flight/contact.
> * Missing internal strain-energy output: Because your TLSPH implementation lacks an internal strain-energy
>   accumulator (\Delta E_{\text{int}} = \sum_i V_{0,i} \mathbf{P}_i : \Delta \mathbf{F}_i), this accounting error
>   went unflagged until compared against rebound KE.
> 6. Why is the fitted sphere surface within 3.7% at R/64 while the flat lattice face's first layer stays at 0.5–0.6?
> Can a flat substrate face be built the same way?
> * Why the flat cubic lattice fails: On a flat cubic lattice face, 100% of the top particles lie on an exact
>   coplanar sheet (z = 0). Penalty contact applies force exclusively to Layer 1, while Layer 2 (at z = -\Delta x)
>   receives zero direct contact force. Because the kernel radius spans across Layers 1, 2, and 3, Layer 1 transfers
>   roughly 40–50% of its applied contact load directly to Layers 2 and 3 via kernel gradients without needing Layer
>   1's own constitutive stress \sigma_{zz} to rise above 0.5\text{–}0.6\,p_n.
> * Why the fitted sphere succeeds: On the curved sphere surface, particles entering the contact zone are
>   geometrically staggered in depth (z) relative to the contact plane, and a 0\text{–}0.5\text{ }\mu\text{m} band
>   slices across shells with varied radial/hoop stencil orientations. Consequently, contact penalty forces and
>   internal kernel reactions are distributed across multiple staggered particle depths rather than quantized into a
>   single coplanar sheet.
> * Can a flat substrate be built the same way? You could break the coplanar layer artifact by using an isotropic
>   glass-like or centroidal Voronoi tessellation (CVT) packing for the substrate, which staggers particle depths.
>   However, you should not do this for cold spray: a staggered/rough particle surface introduces artificial
>   geometric roughness at the scale of \Delta x, causing contact pressure spikes and artificial tangential
>   interlocking that will corrupt surface expansion Y.
>
> 3. Recommended Decisions for the Route Review Session
> * Adopt the "Surface Measurement Skin" + BCT Off: Permanently drop BCT (which fails on curved/small patches by
>   over-amplifying rim loads 2–3×). Keep TLSPH with BCT off for the bulk body mechanics, and define a triangulated
>   surface skin over the boundary particles. Compute surface stretch Y directly from the kinematics of the surface
>   triangles and p_n directly from the contact penalty forces mapped to the surface facets—never from the volumetric
>   stress tensor \boldsymbol{\sigma}_i of Layer 1 particles.
> * Switch to a One-Way Bond for Milestone 1: Amend the 2026-11-14 requirement. Evaluate the Bay criterion
>   (Y > Y' and p_n > p_{\text{ext}}) as a one-way state variable on the surface skin during impact. Defer two-way
>   cohesive tension/rebound coupling to Milestone 2.
> * Close the Energy Balance Before Any New Ladder: Add explicit internal strain-energy integration (E_{\text{int}}),
>   elastic hourglass potential energy (E_{\text{hg}}), viscous dissipation (E_{\text{visc}}, integrated strictly on
>   pairwise relative velocities), and contact penalty energy (E_{\text{contact}}) to OpenCourant. Require total
>   energy conservation within <1\% on T-S1 before freezing another hunch.
> * Set a Concrete Dead-End Trigger for Track B: If TLSPH (with BCT off + surface skin measurement + one-way bond)
>   cannot match the reference interface traction p_n and surface stretch Y on T-B2 and an elastic-plastic sphere
>   impact at R/32 and R/64, terminate the 3D particle solver route and pivot to an Eulerian or remeshed 2D
>   axisymmetric ALE finite-element host.

### Critique of input 2 (modeller, 2026-11-15)

**Right, and new:**
1. **The averaging window lies inside the kernel reach.** At R/32, s = 0.31 µm and h = 1.12 s, so the kernel reaches
   about 0.7 µm; the 0.5 µm band measures inside the boundary error. The 0.5 µm decision (2026-11-14) only checked
   that the window exceeds one spacing. If the window must be several kernel reaches, 0.5 µm needs s ≈ 0.1 µm, about
   R/100 for a 10 µm particle; R/64 on the full block already needs about 40 GB (§22). **The conflict between the
   physical averaging length and this host's reachable resolution is the main finding**, which the review does not
   state.
2. **The edge-convergence test was skipped** under the requirements: fair.
3. **CS-18b was frozen without internal energy** (a listed known limit): fair. Correction: §17–§19, §21, §22 were
   calibration, not frozen campaigns.
4. **Literature pointer:** variationally consistent / stabilised conforming nodal integration (Chen, Belytschko,
   Puso). If it shows corrected particle methods fail the patch test at loaded boundaries, the face-layer deficit is a
   known property (rediscovery). "Proves mathematically" is unverified; worth a WSL B reading task.

**Wrong or overstated:**
5. **"Killed inside the noise floor":** not in §22. Band-1 errors were 8–24 %, against a reference drift of 2–4 % that
   moves them further out. The principle (threshold above reference uncertainty) is sound for future rules.
6. **Energy:** the arithmetic and the reversible-hourglass hypothesis are reasonable. Missed: the 0.49 KE0 occurs only
   with BCT-type spreading (BCT on 0.33 + 0.15; variant up to 0.49); BCT off gives 0.0016 + 0.0001 KE0. The
   lab-frame mechanism needs non-antisymmetric pair forces; the TL force is pairwise and momentum-rate checks agree.
   "Exact artifact" is overconfident. Internal energy is still needed before plastic runs.
7. **One-way bond "identical up to local unloading":** wrong. It is exact only until the first point bonds anywhere.
   Bonding starts at the rim while compression continues, and a bonded rim stops slip and changes jetting nearby, so
   the two diverge mid-compression.
8. **p_n from penalty forces over skin facets:** in §22, p_n already came from the penalty forces and was 5–10 % high,
   so facet areas alone do not fix it. Y from triangle stretch is the real gain, untested. A skin used for measurement
   only is sound; one that feeds forces back repeats BCT's failure step.
9. **Flat face against sphere:** the coplanar-sheet explanation is a plausible hypothesis. For the sphere it describes
   the wrong construction: our conforming sphere has a fitted outer shell over the lattice, not random staggering. The
   obvious cheap test is a flat face with a fitted outer layer (adjusted mass), not considered. The roughness warning
   is reasonable but untested here.
10. **Jet-root failure as shear banding:** the §8 failure was element collapse (Lagrangian distortion); localisation
    may contribute. Heat conduction as a regulariser was refuted at reachable resolutions (CS-13c).
11. **Exit route:** CEL, ALE and MPM are named without evidence of converged interface states. The fallback
    "remeshed 2D axisymmetric ALE FE" conflicts with the 3D requirement, and OpenCourant has no remeshing for 2D
    elements.
12. **The opening praise** is not evidence.

**Taken forward:** the averaging-window conflict (first agenda item); the literature check; the fitted flat face test;
the one-way bond with its validity stated correctly (until first bonding); internal energy before any plastic run.
