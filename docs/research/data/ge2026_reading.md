# Ge et al. 2026 (nonlocal mesh-sensitivity mitigation for cold spray): reading at F level

Read in the cloud on 2026-11-20 by the modeller (claude), from the PDF Peter supplied (open access, CC BY 4.0;
sha256 `dd1ffc0db2ef371a3c57b0e4743c88424d06342f4e7a3476721b5786275dc6a4`; not committed). This closes the Ge item
of WSL B task b9. All 17 pages read.

Labels: "**Reading:**" marks my own interpretation; everything else states what the source says, with its place.
Values read off a figure are marked "(fig.)".

**Blind screen:** none of B06 (Wu 2026), B07 (Liu 2025) or B16 (Kajihara 2024) is cited. The validation uses Cu
particle profiles from Tiamiyu 2020 and 2021 ([71, 72]), which are our B12 and B03; both are already exposed
(d67f72c). Ge prints no v_cr.

## Source

X. Ge, L. Zhou, S. Bagherifard, M. Guagliano, "High-Fidelity modeling of cold spray: Improved constitutive material
model and nonlocal mesh sensitivity mitigation", Int. J. Mech. Sci. 321 (2026) 111654,
doi:10.1016/j.ijmecsci.2026.111654 (Politecnico di Milano).

## 1. Method and set-up

- Abaqus/Explicit, **Eulerian** 3D quarter model (§3.1, Fig. 2), domain a 100 µm cube; EC3D8RT
  thermally coupled elements; default artificial viscosity (§3.3).
- Cu particle d = 10 µm on Cu, 25 °C; V = 590, 605, 768, 918, 990, 1058 m/s (from Tiamiyu [71, 72]); total time
  25 ns (§3.3).
- Meshes h = d/25, d/50, d/100 at the impact region (§4); d/50 is called "commonly adopted" (§1).
- Taylor–Quinney Q = 0.75 (Table 1).

## 2. Constitutive model (§2)

Eq. (1): σ_y = [(σ_y0 + A ε_pⁿ) + (α ε_pⁿ + β) ln(ε̇_p/ε̇_s) + B ln(ε̇_p/ε̇_u)] ·
(1 + e^((T_r − T_ref)η)) / (1 + e^((T − T_ref)η)), with the rate terms active above ε̇_s and ε̇_u respectively
(Eqs. 2–5). Cu values (Table 2): σ_y0 39 MPa, A 320 MPa, n 0.41, α 7.5 MPa, β 0.01 MPa, ε̇_s 10⁻³ s⁻¹,
B 110 MPa, ε̇_u 10⁴ s⁻¹, T_ref 350 °C, η 0.0043 °C⁻¹. A modification of the Ma–Wang model [28]. Appendix A: like JC
and MW it "lacks a strong physical basis"; accuracy may drop above 10⁷ s⁻¹, above 1100 m/s, near melting, and with
"cracking, particle fragmentation, or oxide layer spallation".

## 3. Diagnosis of mesh sensitivity (§4)

- **Kinematic issue** (§4.1, Fig. 6): interface elements cannot bend, so the deformation goes into the elements next
  to the interface; refinement halves the shear-band width and doubles strain and strain rate in it. Present even
  without thermal softening (Fig. 7).
- **Elliptic problem** (§4.2): thermal softening loses ellipticity. Adiabatic runs are the most mesh-sensitive
  (Fig. 8), with "unrealistic melting" at 918 and 1058 m/s on d/100 (Fig. 9). Heat diffusion helps at 590 m/s but
  does not remove excessive jetting at 918 and 1058 m/s (Fig. 10).
- **Reading:** the same two causes as ours: the jet-root folding (§8, §25 reading 1) and the missing length scale
  (§25 reading 2). Their kinematic issue is Eulerian/element-based; in TLSPH it would take a different form.

## 4. Nonlocal formulation (§5)

- Implicit gradient (Peerlings type), Eq. (15): f̄ − l²∇²f̄ = f. Over-nonlocal, Eq. (16): f̂ = m f̄ + (1 − m) f, m = 2.
- **What is nonlocal** (§5.2, Eq. 17): ε_p and ε̇_p standard nonlocal (ε̄_p, ε̄̇_p); temperature over-nonlocal
  (T̂ = 2T̄ − T, Eq. 23). Over-nonlocal is not used for ε_p "since the equivalent plastic strain and equivalent plastic
  strain rate must have maximum values at the central integration point to satisfy kinematic rules".
- **Implementation** (§5.3, Eqs. 18–22): the nonlocal plastic multiplier γ̄ is solved through the analogy with the
  transient heat equation, i.e. the Abaqus thermal degree of freedom carries γ̄ (k′ = 1; ρc′_p ∂T′/∂t → 0 via
  c_p = 0.001). The temperature is then updated inside the VUMAT (Eq. 23). **Reading:** physical heat conduction is
  therefore not modelled in the nonlocal runs; the over-nonlocal T̂ stands in for it.
- **Cost** (App. D, Table D.1): run times within 1 % of the local runs (918 m/s: 2.2 / 21.4 / 135.9 min at d/25 /
  d/50 / d/100).

## 5. The length ℓ (§5.4) — the key point for this project

Verbatim: "Since the characteristic length affects the numerical results, it can be treated as a material parameter
[83]. An iterative approach was employed to determine its value. When the characteristic length was set to 4 µm,
the simulated particle morphology demonstrated strong agreement with experimental observations. This finding
suggests that the characteristic length for Cu particles can be set to l = 2/5 d."

- ℓ = 4 µm = 0.4 d is **calibrated against particle morphology**, not derived from grain size, a strain-gradient
  length, or thermal diffusion.
- No ℓ-sensitivity study is shown. ℓ/h = 10, 20, 40 on the three meshes.
- **Reading:** ℓ fitted to the same morphology data used to show agreement, so the agreement is not independent.
  "l = 2/5 d" ties ℓ to the particle size, which a material length should not be.

## 6. What converges (§5.4, Fig. 12)

- Text: "nearly identical shear band widths", "almost identical local jetting across different mesh sizes"; the
  kinematic sensitivity "didn't fully eliminate … but … was significantly mitigated"; excessive jetting and
  unrealistic melting removed.
- Maximum ε_p from the colour-bar limits (fig.; these are the plot ranges, not a printed metric):

  | V (m/s) | d/25 | d/50 | d/100 | d/50 → d/100 |
  |---|---|---|---|---|
  | 590 | 1.3 | 1.5 | 1.6 | +7 % |
  | 918 | 1.8 | 2.3 | 2.5 | +9 % |
  | 1058 | 2.1 | 2.5 | 2.7 | +8 % |

  Without the nonlocal strategy (heat diffusion, Fig. 10): 1.7 / 2.0 / 2.5, 1.9 / 2.8 / 3.5, 2.3 / 3.2 / 5.0.
- No quantitative convergence measure (profile error vs mesh) is given for the nonlocal runs. No interface quantity
  (contact pressure, surface stretch, bonded area) and no bonding is modelled.
- **Reading:** the peak edge strain still rises with refinement, by less than half as much as before. By our rule
  (driver-check §3, 3.5 %) it would not count as converged.

## 7. Validation (§3.4)

Local model (no nonlocal), d/50, heat diffusion, against Tiamiyu Cu profiles: overlapping ratio 96.3 % at 590 m/s,
lowest 85.6 % at 990 m/s, 93.2 % at 1058 m/s (MW model 61.8 %) (Fig. 5a); flattening ratio within 5 % (Fig. 5b).
The nonlocal runs are compared with experiment only through the choice of ℓ.

## 8. Microstructure and evolving length

Not covered: no grain size, recrystallisation, or evolving ℓ. Leads cited:
- [29] Chakrabarty R, Song J. "A modified Johnson–Cook material model with strain gradient plasticity consideration
  for numerical simulation of cold spray process", Surf. Coat. Technol. 397 (2020) 125981 — a physical (strain-
  gradient) length in a cold-spray JC model.
- [77] Tang Q, Veysset D, Assadi H, Ichikawa Y, Hassani M. "Strength gradient in impact-induced metallic bonding",
  Nat. Commun. 15 (2024) 9630 — a measured gradient near the bond.

Both need a blind screen before reading (authors overlap with blind-list groups).

## 9. Stated limitations

Empirical model without strong physical basis (App. A); Cu only; validated range 590–1058 m/s; Eulerian Abaqus; the
kinematic issue mitigated, not removed.
