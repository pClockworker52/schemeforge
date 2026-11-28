# Edge-energy check, 2026-11-28 (does an energy-per-area quantity at the interface converge on TLSPH?), draft

**Status: DRAFT, not frozen.** `kind = check`, not a hunch; the hunch budget is unaffected. Drafted 2026-11-28 (cloud,
modeller) on Peter's request ("Draft it."), under his priority "finding something that converges" (DECISIONS
2026-11-28). Post-processing of existing files only: no run, no build. Spec, rule and prediction are fixed before any
number is computed. No number was computed for this draft.

## 1. Question

Point values at the contact edge do not converge on any host: Y − 1, p_n beyond 0.25 a, the edge ε_p (§25–§27, §41).
problem-formalism §2(c) reads the edge as a crack tip, where point values are singular by construction. The lesson
of 2026-11-24 says criteria should be built from finite quantities, and in fracture mechanics the finite quantities
are energies.

**Question:** on the §30 TLSPH off runs (R/8, R/16, R/32), does the **plastic dissipation per unit contact area** in
an interface layer converge? Does its **interface excess** (the part concentrated at the interface, beyond the bulk
trend) converge?

If the excess converges, it is the first converged *interface* quantity in the track other than a(t). It would be in
J/m², the unit of a bond energy.

## 2. The case against (written before any number; read this first)

1. **No stress in the files.** The frames hold positions, `SPHELEM_Plastic_Strain`, `ELEMENT_ID` and `PART_ID` (§41
   Q1). They carry no stress tensor and no energy density, and the engine writes no TL internal energy (solver-facts
   §3). The fracture quantity that is finite at a tip is the energy **flux** J. It needs stresses, so it needs a rerun
   with stress output, which is not proposed here. This check uses dissipation **content**, from ε_p through
   Johnson–Cook.
2. **Large-scale yielding.** J is path-independent, and finite, only when the plastic zone is small against the
   geometry, or for proportional loading. In cold spray the whole particle yields, the edge passes ε_p 1, softening
   makes h_eff < 0 from ε_p ≈ 0.37 (§2(b)), and the edge unloads into the jet. A domain small enough to be local is
   not path-independent; one large enough to be path-independent is the whole body.
3. **A moving singular front leaves a singular wake.** Each point at depth d saw the edge pass at distance about d.
   With the stationary HRR exponents (ε ∼ r^−0.845, σε ∼ 1/r), the wake's plastic work density goes as 1/d, and its
   depth integral diverges logarithmically. At these meshes that is a drift of about ln 2 / ln(ρ/s), 0.25–0.35 per
   halving, which reads as "not converging". A growing front is less singular than a stationary one (Rice & Sorensen
   1978 and later work for hardening; from memory, not read), so the wake may be integrable. So **"not converging" here
   does not refute the crack-tip reading (§13 case B).**
4. **Precedent.** The annulus plastic work W_ann, an energy integral at the edge, did not converge: on quads at 0.00
   to 0.43 of judged points, and in the TLSPH survival probe with 4.5–30 % differences between R/16 and R/32
   (driver-check-2026-11-17.md). Even the whole-body plastic work on quads moved 2–12 % between R/128 and R/256.
5. **The outermost layer grows with refinement.** The band check (§41) found the ε_p peak in the outermost particle
   layer rising from 0.76–0.87 to 2.1 (R/8 to R/32) while its width in µm stayed at 0.6–0.9 µm. A peak that rises at
   fixed width makes the excess grow.
6. **Numerical dissipation is the largest drift.** |W_hg| fell from 29.7 to 11.9 nJ (substrate) and |W_visc| from 20.2
   to 9.1 nJ (particle), against a rebound energy of 2.7 nJ (§41 sinks). Energy that numerical dissipation stops
   taking must go somewhere, so the physical dissipation cannot converge until that does.

What this check can still decide: whether **any** interface-layer energy per area converges on TLSPH, and whether the
excess behaves like the observed outer-layer spike (§2 item 5). It cannot separate a singular but well-posed edge
(case B) from a TLSPH surface-layer error (case C).

## 3. Definitions (committed in the script before any profile is read)

- **Runs:** AL08off, AL16off, AL32off (engine `27e53d5f0`, §30), Al–Al, 600 m/s, P-HG-Al, R = 10 µm. Spacing s = 1.25
  / 0.625 / 0.3125 µm.
- **Judged frame:** A019, t = 24.0 ns = 1.02 t_p (as in the band check). Reported: the frame nearest 0.5 t_p.
- **Depth:** as in the band check, in the reference configuration (frame 0). Particle d = R − |X − X_c|; substrate d =
  depth below the original top surface.
- **Plastic work density (judged):** isothermal Johnson–Cook at T_r with CE = 1,
  w_p(ε) = A ε + B ε^(n+1)/(n+1), with A 148.4 MPa, B 345.5 MPa, n 0.183 (P-HG-Al) [J/m³]. This is an upper bound,
  because heating lowers σ_y. It is a monotone map of ε_p, so convergence of w_p is convergence of the ε_p field
  weighted by the work.
  - Reported: the plastic-heating-only adiabatic variant (T from ∫σ_y dε_p / ρc_p, the §34 lower-bound
    temperature).
- **Layer dissipation per contact area:** γ(ρ) = Σ_{d_i ≤ ρ} V⁰_i w_p(ε_p,i) / A_c [J/m²], for each body separately.
  The sum runs over the whole layer, jet included. V⁰_i = s³ (lattice volume). A_c = π a² / 4 for the quarter model,
  with a = a(t) at the frame: the largest current radial position of a particle with nonzero contact force in the
  interface file.
  - ρ ∈ {1.25, 2.5, 3.75, 5} µm, which is at least one spacing on every mesh.
- **Interface excess:** the intercept of γ(ρ) at zero thickness, extrapolating the bulk slope between 2.5 and 5 µm:
  γ_ex = 2 γ(2.5) − γ(5) [J/m²]. This is the Gibbs-type surface excess of dissipation.
- **Mesh differences:** for a quantity q, Δ_ab = |q_b − q_a| / |q_b| between meshes a (coarser) and b (finer).
- **Class per quantity and body:**
  - **converged:** Δ_16,32 ≤ 0.05 and Δ_16,32 ≤ 0.6 Δ_8,16;
  - **converging:** Δ_16,32 ≤ 0.15 and Δ_16,32 ≤ 0.6 Δ_8,16;
  - **not converging:** otherwise.

## 4. Q1: files (reading only; stop if it fails)

1. Frames A000 and A019 (and the 0.5 t_p frame) of all three off runs, with positions, ε_p and ids. These were read in
   §41; the run files were kept (task 2026-11-24-b deleted only the derived arrays).
2. a(t) at those frames from the interface file (contact-force list). **Never read for these runs.** Check that
   a(A019) on the three meshes differs by less than 5 %. a(t) converges elsewhere (driver check; TLSPH probe median
   2.8 %). If it does not, stop and report it.
3. Particle volume s³: check against the deck's lattice.

## 5. Model checks (on the real lattices, before any real profile is used)

Manufactured ε_p fields placed on the frame-0 positions of each mesh. Bulk ε_b = 0.2 for r_ref ≤ 8 µm in both
bodies, 0 outside.

| Check | Field | Required class of γ_ex (both bodies) |
|---|---|---|
| M1 converged band | ε_b + 1.0 exp(−d / 1 µm) | converged |
| M2 integrable singular front | ε_b + 0.5 (d / 1 µm)^−0.5 | converging or converged |
| M3 observed spike | ε_b + P exp(−d / 0.75 µm), P = 0.8 / 1.3 / 2.1 at R/8 / R/16 / R/32 | not converging |
| M4 stationary HRR wake (reported only) | ε_b + 0.5 (d / 1 µm)^−0.845 | expected not converging (§2 item 3) |

If M1 or M2 fails its class, or M3 comes out converging or converged, the metric fails its rung (standing rigor
rule, coldspray-procedure.md): stop and report **not determinable**.

## 6. Outcomes (judged at A019)

- **Finite interface dissipation (on TLSPH):** γ_ex is converged or converging on both bodies, and γ_ex ≥ 0.2 γ(2.5)
  on R/32 for both bodies (the excess is a real share, not round-off around zero).
- **Bulk only:** γ(5) is converged or converging on both bodies, but γ_ex is not (or is below the 0.2 share).
- **Nothing converges:** neither holds.
- **Not determinable:** Q1 stops, or a model check fails.

**Reported, not judged:**
- γ(ρ) for every ρ, body and mesh, with Δ and class;
- the adiabatic variant;
- the 0.5 t_p frame;
- the sinks from `tl_diag.csv` at A019 (W_hg, W_visc, W_d, E_c) beside Σ γ·A_c, to show whether γ's drift tracks the
  numerical-dissipation drift;
- the CS-23 30× bonded runs (§39), if their frames allow, the same quantities.

## 7. Prediction (judgment, before any number)

- Finite interface dissipation 0.10; bulk only 0.30; nothing converges 0.45; not determinable 0.15.
- Why so low: §2 items 4–6 are measured, and each one alone predicts a drifting excess. Item 3 says that even a
  well-posed singular edge may drift at these meshes.
- Not determinable 0.15: Q1 item 2 (a(t) from the interface file) is unread, and M2 may not reach "converging" at R/32.

## 8. What follows (stated now)

- **Finite interface dissipation:** a converged interface quantity in J/m² exists on TLSPH. Next would be a hunch
  comparing γ_ex with a bond-energy scale, and a stress-output rerun for a domain J (Stage B), both after Peter's
  review.
- **Bulk only:** the interface excess is the non-converging part, like every point value. A criterion built from
  finite quantities then needs the interface's own length (cohesive zone), or a different host.
- **Nothing converges:** even bulk dissipation drifts. The first thing to make converge is the numerical dissipation
  (§2 item 6); the next check would be a dissipation sweep (hourglass coefficient, pair viscosity) on R/8 and R/16.
- **Not determinable:** recorded; no rerun is decided here.

## 9. Cost and facts check

- One WSL A post-processing session, as for the band check. Frame conversion needs a few GB of scratch, deleted after.
- **Facts checked** (solver-facts §3, §41).
  - Covered: frame fields and ids, frame times, the judged frame A019, `tl_diag.csv` sinks.
  - **Not covered: never read/used before; check the output first:** (i) a(t) from the §30 off runs' interface file
    (Q1 item 2); (ii) V⁰ = s³ as the particle volume (Q1 item 3).
