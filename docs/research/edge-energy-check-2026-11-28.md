# Edge-energy check, 2026-11-28 (does the energy delivered to the interface converge on TLSPH?), draft r1

**Status: DRAFT r1, not frozen.** `kind = check`, not a hunch; the hunch budget is unaffected. Drafted 2026-11-28
(cloud, modeller) on Peter's request ("Draft it."; r0 in eec71a6). Revised the same day after Peter's questions
("Let's check the edge energy." Why no stress? Why no J with large yielding? Don't overfit on the record; should the
missing TLSPH internal energy be fixed?). Spec, rule and prediction are fixed before any number is computed. No number
has been computed.

**What changed from r0:**
- r0 measured plastic-work *content* from ε_p only, because the frames carry no stress. That is a W_ann-type
  quantity (driver check), and it stays only as a reported comparator (Part C).
- The judged quantity is now the **energy flux into the interface layer**, by body. It is computed exactly from
  conservation, using two output-only additions to the fork: a per-particle internal energy and per-particle numerical
  work.
- A contour or domain J around the moving edge is computed from stresses and reported with its path dependence.
- This needs a fork output change and reruns of the §30 off decks (Stage 0, Stage A).

## 1. Question

Point values at the contact edge do not converge (Y − 1, p_n beyond 0.25 a, edge ε_p; §25–§27, §41). The edge behaves
like a crack tip (problem-formalism §2(c)). The lesson of 2026-11-24 says criteria should be built from finite
quantities, and energy flow to a moving front is the fracture-mechanics candidate.

**Question:** on Al–Al 600 m/s TLSPH off runs at R/8, R/16 and R/32, does the energy that each body delivers to its
interface layer, per unit contact area, converge? Does its **interface excess**, the part concentrated at the
interface beyond the bulk trend, converge? Each body is evaluated separately: particle and substrate are the two
partners that feed the interface.

## 2. Background, sorted by what it applies to

### 2a. Facts about the instrument (apply to every quantity on this host, whatever the concept)

- **Numerical dissipation is the largest mesh drift** (§41 sinks): |W_hg| 29.7 → 11.9 nJ (substrate), |W_visc| 20.2 →
  9.1 nJ (particle), R/8 → R/32, against a rebound energy of 2.7 nJ. Today it is known only as a global total.
  - Stage 0 adds it per particle, so this check can see where it sits and remove it from the physical flux.
  - The hourglass accumulator is biased under ringing (§17), so its per-particle values are reported with that caveat.
- The **ε_p peak sits in the outermost particle layer** and rises 0.76–0.87 → 2.1 at a nearly fixed width of
  0.6–0.9 µm (§41). This may be physics (a singular edge) or a TLSPH surface-layer error; §41 could not tell which.
- The **face-layer deficit** of TLSPH (end layers carry 0.655 / 0.845 of the stress; §17, §22).
- e(off) drifts 0.094 / 0.065 / 0.057 (§30), and energy closes to 0.25 % with BCT off (§20.5).

### 2b. Concept precedents (apply only where this check measures the same thing)

- **W_ann** (driver check 2026-11-17): plastic work in an annulus at the edge did not converge (quads; TLSPH probe
  4.5–30 %). It applies to Part C, which measures the same kind of quantity. **It does not apply to the judged flux:**
  that is total energy (internal plus kinetic), delivered across the layer's boundary, separated by body and with
  numerical work removed. Nothing like it has been measured in the track.
- Pointwise thresholds (CS-12 skin Y, §26) and outer drivers (§27) are different concepts; not used here.

### 2c. Why J is not ruled out by large-scale yielding

- **The energy flux into a region around a moving front is defined for any material.** It is the work of the outside
  material through the boundary, plus the energy the moving boundary sweeps in (Freund's dynamic energy-flux integral;
  from memory).
- What large-scale yielding breaks is **path independence**: material between two contours dissipates, so F(ρ) depends
  on the contour size ρ. That dependence is information, not a defect: F(ρ₁) − F(ρ₂) is the dissipation and storage
  rate between the two contours. The tip limit ρ → 0 is the energy reaching the front itself. For ideal plasticity
  that limit is zero, and with hardening and rate it may be finite.
- Formulations built for this case: Atluri's T* for incremental plasticity, and configurational forces, J_tip = J_far −
  C_p, with C_p the plastic configurational force (Simha, Fischer, Kolednik and co-authors; from memory, not read). A
  frictionless contact edge is not a crack, but configurational forces apply to any moving front.
- r0 said J could not be formulated here. That was wrong: what fails is path independence, not the definition.

### 2d. What a singular front implies (reasoning, not tested)

- If the edge field were stationary-HRR-like (σε ∼ 1/r), the energy density around the current edge is integrable in
  2D, so the flux into a small torus around the edge is finite.
- The *wake* (material the edge has passed, at depth d) would carry w ∼ 1/d, which has a log-divergent depth integral.
- A growing front is less singular than a stationary one (from memory), so the wake may be integrable.
- Model check M4 shows how a log-divergent wake would score. "Not converging" therefore does not by itself refute the
  crack-tip reading.

## 3. Stage 0: fork outputs and their rung (WSL A)

**Build (output only; must be bitwise neutral on written metrics, T-A0):** a per-particle record at each animation
frame, quarter model:
- w_i [J]: accumulated stress work V⁰_i ∫ P:Ḟ dt (the per-particle terms of `tl_diag`'s E_int);
- h_i, q_i [J]: accumulated hourglass and pair-viscosity work on particle i (the per-particle terms of W_hg and
  W_visc);
- the Cauchy stress σ_i (6 components) and J_i = det F_i;
- velocity and position (already written).

**Rung (all must pass before Stage A):**
- **S0-1 sums:** Σ w_i, Σ h_i and Σ q_i per body equal `tl_diag.csv`'s E_int, W_hg and W_visc to ≤ 0.1 % of KE₀ at
  every frame. Run: AL08off rerun (about 100 s).
- **S0-2 neutrality:** the rerun reproduces the §30 AL08off written metrics (e, `tl_diag.csv`, interface file) bit for
  bit, headers masked.
- **S0-3 stress:** −tr σ_i / 3 matches the written pressure P_i to ≤ 10⁻⁶ relative.
- **S0-4 elastic reversibility (known answer):** the elastic body-on-body T-B2 deck (conforming sphere R = 10 µm on
  a block, 20 m/s, §22.1), at R/16. An elastic interface keeps no energy. After separation, the interface-layer energy ε_b(ρ) of section 4 must
  return to ≤ 5 % of its in-contact peak, and the per-particle numerical work must stay ≤ 1 % of KE₀.

If S0 fails: stop and report; no Stage A.

## 4. Stage A: judged quantities (reruns AL08off, AL16off, AL32off with the Stage 0 outputs)

Engine as §30 (`27e53d5f0`) plus the output change; decks unchanged. Cost: about 100 s, 0.5 h and 11–12 h. The R/32
memory stays near §30's 12.7–14.2 GiB plus the new arrays.

**Definitions** (committed in the script before any profile is read):
- **Depth** in the reference configuration: particle d = R − |X − X_c|; substrate d = depth below the original top
  surface. ρ ∈ {1.25, 2.5, 3.75, 5} µm. Layer set S_b(ρ) = particles of body b with d ≤ ρ.
- **Contact area:** A_c(t) = π a(t)² / 4 (quarter), with a the largest current radial position of a particle with
  nonzero contact force in the interface file.
- **Energy delivered to the layer per contact area**, by conservation:
  ε_b(ρ, t) = Σ_{i ∈ S_b(ρ)} [ (w_i + k_i + h_i + q_i)(t) − (w_i + k_i + h_i + q_i)(0) ] / A_c(t) [J/m²],
  with k_i = ½ m_i |v_i|².
  - Adding h_i and q_i books the numerical work done in the layer as received energy. The physical flux is then the
    energy the layer received from its surroundings and through the contact, whichever sink took it.
  - Reported: the same without h_i and q_i, and h_i + q_i alone.
- **Interface excess:** ε_ex,b = 2 ε_b(2.5) − ε_b(5) [J/m²], the intercept of the bulk trend at zero thickness.
- **Partner share** (reported): ε_ex,p / (ε_ex,p + ε_ex,s).
- **Judged frame:** A019 (1.02 t_p). Reported: the frame nearest 0.5 t_p, and the time series.
- **Mesh differences:** Δ_ab = |q_b − q_a| / |q_b| (a coarser, b finer). Classes:
  - **converged:** Δ_16,32 ≤ 0.05 and Δ_16,32 ≤ 0.6 Δ_8,16;
  - **converging:** Δ_16,32 ≤ 0.15 and Δ_16,32 ≤ 0.6 Δ_8,16;
  - **not converging:** otherwise.

**Model checks** (on the real frame-0 lattices, run before any real profile; manufactured w fields, k = h = q = 0):

| Check | Field (energy density per reference volume, in units of w₀; bulk 0.2 for r_ref ≤ 8 µm) | Required class of ε_ex |
|---|---|---|
| M1 converged band | 0.2 + exp(−d / 1 µm) | converged |
| M2 integrable singular front | 0.2 + 0.5 (d / 1 µm)^−0.5 | converging or converged |
| M3 rising surface spike | 0.2 + P exp(−d / 0.75 µm), P = 0.8 / 1.3 / 2.1 at R/8 / R/16 / R/32 | not converging |
| M4 log-divergent wake (reported) | 0.2 + 0.5 (d / 1 µm)^−1 | expected not converging |

If M1 or M2 fails its class, or M3 comes out converging or converged, the estimator fails its rung: **not
determinable**.

## 5. Outcomes (judged at A019)

- **Finite interface energy:** ε_ex,b converged or converging for both bodies, and |ε_ex,b| ≥ 0.2 |ε_b(2.5)| on R/32
  for both (a real share).
- **Bulk only:** ε_b(5) converged or converging for both bodies, ε_ex not.
- **Nothing converges:** neither.
- **Not determinable:** Stage 0 fails, Q1 fails (a(A019) differs by > 5 % across meshes), or a model check fails.

**Reported, not judged:**
- **Part B, domain J around the moving edge.** Weight q = 1 for ℓ ≤ ρ/2, falling linearly to 0 at ℓ = ρ, with ℓ the
  r–z distance to the current edge point.
  - F_b(ρ) = −Σ_{i ∈ b} V_i ∇q_i · [σ_i · v_i − e_i (v_i − u_e)], with V_i = J_i V⁰_i, e_i = (w_i + k_i)/V_i and u_e
    the edge velocity from central differences of a(t).
  - Per unit edge length, for each ρ: the profile F_b(ρ) (path dependence) and its trend toward small ρ.
  - Not judged, because u_e from differences of a(t) does not converge (driver check).
- **Part C, comparator (W_ann-type):** the plastic-work content γ_b(ρ) from ε_p through isothermal Johnson–Cook (r0's
  quantity), with its excess. Whether total-energy flux and plastic content behave differently is the direct test of
  whether the flux is a different concept in practice.
- **Where numerical work sits:** h + q per layer and its share of ε_b(ρ), by mesh.
- **The CS-23 30× bonded runs:** the same quantities, if a rerun is approved later (not part of this check).

## 6. Prediction (judgment, before any number)

- Stage 0 passes: 0.70 (S0-1 depends on the accumulators being per particle in the source; S0-4 on the hourglass bias
  under ringing).
- Given Stage 0 passes: finite interface energy 0.20, bulk only 0.35, nothing converges 0.30, not determinable 0.15.
- Why these odds:
  - The instrument facts (2a) act on any quantity: the outer-layer spike and the drift of numerical dissipation can
    put a mesh-dependent amount of energy into the outermost layer.
  - The concept itself is untested, and booking numerical work as received energy removes the most obvious cause of
    drift. That is why the odds are higher than r0's 0.10 for the plastic content.
  - M2 versus M4 (section 2d) limits what "not converging" means.

## 7. What follows (stated now)

- **Finite interface energy:** the first converged interface quantity besides a(t), split by partner. Next would be a
  hunch on whether bonding needs ε_ex to exceed an interface energy (cohesive G_c), with the partner split as the
  contact's model of its partners. Peter decides.
- **Bulk only:** the excess is the non-converging part. Compare it with Part C and with the per-particle numerical
  work: if the drift sits in h + q, the next task is the dissipation itself.
- **Nothing converges:** the instrument does not converge even in energy. A dissipation sweep (hourglass coefficient,
  pair viscosity) on R/8 and R/16 comes next.
- **Not determinable:** recorded; Peter decides.

## 8. Facts check (coldspray-procedure.md)

- Covered: positions, ε_p, ids and frame times (§41); `tl_diag.csv` E_int, W_hg, W_visc per body (§41 sinks); TLSPH
  stress fields can be written (T-B2 runs, §22.1); the §30 decks request only EPSP, P and VEL animations (§34).
- **Not covered: never read/used before; check the output first:**
  - (i) per-particle w, h, q (new output, Stage 0);
  - (ii) σ and J per particle in an impact run;
  - (iii) a(t) from the interface file of the §30 off runs;
  - (iv) the T-B2 deck at R/16 for S0-4 (run before at R/32 and R/64 only).
