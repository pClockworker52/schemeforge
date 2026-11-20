# Tang et al. 2024 (strength gradient in impact-induced bonding): reading of the main text

Read in the cloud on 2026-11-20 (modeller, via a fetch agent) from the PMC copy
(https://pmc.ncbi.nlm.nih.gov/articles/PMC11544021, CC BY-NC-ND). Main text, figure captions and Methods only;
the Supplementary Information (SI §1–3, Eqs. S15–S20, the FE model) was **not** read. Values only plotted are not
available. Labels: "**Reading:**" marks my interpretation.

**Blind screen:** not on the blind list. No critical velocity is stated anywhere in the main text (impact velocities
only). Al on Al, so B07 (Ti) and B16 are not touched.

## Source

Q. Tang, D. Veysset, H. Assadi, Y. Ichikawa, M. Hassani, "Strength gradient in impact-induced metallic bonding",
Nat. Commun. 15 (2024) 9630, doi:10.1038/s41467-024-53990-z.

## 1. Set-up

- Al particles (Valimet, nominal 20 and 45 µm) on Al substrates polished to 0.04 µm. LIPIT, impact velocities
  100–1200 m/s (Methods).
- Main case: 23 ± 2 µm at 1100 ± 41 m/s (Fig. 1g, 2a). Also 42 ± 3 µm at 860 ± 20 m/s (Fig. 2b), 20 µm at 862 m/s
  (Fig. 2c).
- Site-specific in situ micro-tensile tests on FIB slabs (5 µm) with the interface at the gauge centre, five per
  particle from centre to periphery; normal and shear stress combined by Tsai–Hill. TEM/EDS of the interface.
- FE simulations in SI §2 only (not read).

## 2. Measured bond-strength profile

- Weakest at the centre, up to a normalised interfacial arc length of about 0.16; "a sudden twofold increase" to
  about 0.32; then a plateau over "more than 60%" of the arc, with a slight decline toward the edge.
- Peaks 220–233 MPa (42 µm and 20 µm cases); bulk Al yield about 115 MPa (Suppl. Fig. 8), so the peak is about
  1.9–2.0× bulk yield (my arithmetic). Gradient about 50 MPa µm⁻¹.
- 862 → 1100 m/s: about 25 % stronger in the weak central region; doubling particle size at fixed velocity does not
  change the distribution significantly.
- Early surface opening about 3 µm from the centre at 1 ns, peak contact pressure about 5 GPa there (Fig. 2d).

## 3. Oxide form decides the level

TEM: nm-thick oxide layers, about 10–16 nm oxide particles, and debris of a few nm. Strengths 94, 201 and 212 MPa at
0.04, 0.24 and 0.43 ζ_max, respectively for layers, particles and debris (Fig. 3). Near the centre, bonding is
"extremely localized" between µm-long unfractured oxide layers; beyond about 0.2 a continuously bonded interface; the
oxide acts as a barrier beyond about 0.92 (Fig. 4).

## 4. Predictive framework (Eq. 1)

σ_B = (σ_fd / σ_fb) · P_eff · Y_eff, local strength = the peak of σ_B over time, capped by the instantaneous flow
stress σ_fb. P_eff = impact pressure minus a critical pressure for extruding metal through oxide gaps (depends on
flow stress and local surface exposure, Eq. S20, not read). Y_eff = exposed / total surface area. No fitted
parameters are given in the main text.

**Reading:** this is a Bay-type law (pressure × surface exposure, capped by flow stress), the same family as `cs12`
and `bay83` in the fork. The measured strength-against-radius profile is **calibration and test data for an
interface law**, the data type the project has lacked (HANDOFF item 6, "no calibration data"). It needs the local
surface exposure, which on TLSPH comes from the skin Y that does not converge (§25, §26).

## 5. Microstructure and length scale

No grain size or microstructure numbers; prior work on dislocation density, grain refinement and dynamic
recrystallisation toward the edge is cited (refs. 46–52). No intrinsic length scale is discussed.

## 6. Not covered

Plotted strength values, centre strength, µm positions (only normalised arc length), SI equations and FE model.
Companion paper (not read): "Microparticle impact–induced bond strength in metals peaks with velocity", PNAS (2025),
doi:10.1073/pnas.2424355122; its abstract gives a value for Al on Al that was seen in a search snippet (logged here as
seen: Al v_cr about 800 m/s; not a blind-list paper).
