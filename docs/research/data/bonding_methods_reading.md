# Interface-bonding methods in cold spray: reading at F level (task 2026-11-13-b9)

WSL B task 2026-11-13-b9 (`docs/research/tasks/wsl-b.md`). Read on 2026-11-13 and 2026-11-15 by the WSL session.
**Status: done, except the closed source #5** (Dai et al. 2025, the task's "Wang 2025"; see "Not obtained").
Six sources are read: #1, #2, #3 (text and PDF), #3b, #4 and #6 (abstract). The comparison table covers these.

Labels: "**Reading:**" marks my own interpretation; everything else states what the source says, with its place.
Values read off a figure are marked "(fig., ±…)" with my reading error.

## Sources

| # | Reference | Obtained from | Version | sha256 | Read |
|---|---|---|---|---|---|
| 3 | B. Ren, J. Song, "Peridynamic Simulation of Particles Impact and Interfacial Bonding in Cold Spray Process", J. Therm. Spray Technol. 31 (2022) 1827–1843, doi:10.1007/s11666-022-01409-w (PMC9109757) | NCBI BioC API, `https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC9109757/unicode` (JSON full text, licence field "NO-CC CODE") | published text (PMC), **text only**: no page numbers, no equations, and most inline numbers and symbols are missing from the BioC text | `b2957c67d573a17b2f0646bfa8ba6f936b59adba813d92a0f9e84d035d007105` (the JSON) | all body text and captions; no figures |
| 1 | J. Tang, *Predictive model of impact-induced bonding in cold spray using the Material Point Method*, MASc thesis, Univ. of Waterloo, 2021, `http://hdl.handle.net/10012/17030` | UWSpace PDF, downloaded by Peter in a browser, filed as `coldspray-papers/notlisted_Tang_MASc-thesis_2021.pdf`, 110 pp. | accepted thesis | `4d5ff0e9c027279eb594f84d042185c48b4071c90845951d1b412b1e81a0109a` | all chapters (2026-11-15, for tasks b11 and b9) |
| 2 | X. Ge, L. Zhou, S. Bagherifard, M. Guagliano, "High-Fidelity modeling of cold spray: Improved constitutive material model and nonlocal mesh sensitivity mitigation", Int. J. Mech. Sci. 321 (2026) 111654, doi:10.1016/j.ijmecsci.2026.111654 | Polimi repository PDF (`re.public.polimi.it/bitstream/11311/1314673/1/1-s2.0-S0020740326005084-main.pdf`), downloaded by Peter in a browser, filed as `coldspray-papers/notlisted_Ge_IJMS2026_published.pdf`, 17 pp. | publisher version, CC BY | `dd1ffc0db2ef371a3c57b0e4743c88424d06342f4e7a3476721b5786275dc6a4` | all text; figures not viewed |
| 3 (PDF) | same paper as #3 | Springer PDF (`link.springer.com/content/pdf/10.1007/s11666-022-01409-w.pdf`), downloaded by Peter in a browser, filed as `coldspray-papers/notlisted_Ren-Song_JTST2022_published.pdf`, 17 pp. | publisher version | `12315209fb506a6f3d6fabd20254f0379d4454cd3e916ac467b7d74f374046ab` | equations and the numbers lost in the text version (2026-11-15); figures not re-read |
| 3b | B. Ren, J. Song, "Effect of particle oxidation, size and material on deformation, bonding and deposition during cold spray: a peridynamic investigation", arXiv:2403.01311v3 (2024-08-15) | `https://arxiv.org/pdf/2403.01311` | preprint v3 (no journal version found in OpenAlex) | `1ae87e5fa352564784ca5ed625373029ed6588103bc974cbf07e220f1be8f4aa` | all 29 pages, figures pp. 6 and 9 viewed |
| 4 | Z. Dai, F. Xu, J. Wang, J. Ye, W. Feng, "Investigation of interfacial adhesion and pore formation in cold spray using the updated Lagrangian SPH method", Comput. Mech. 78 (2026) 1587–1609, doi:10.1007/s00466-026-02813-7 | Peter's copy, `C:\Users\peter\coldspray-papers\art2Fs00466-026-02813-7.pdf` | published version | `759bd15a5ef47c85ae55dcb0d88fbcec55a5b2515078a80f2723337f84a84c74` | all pages; figures pp. 1594–1596, 1599 viewed |
| 6 | A. A. Khoei, M. R. Hirmand, H. Jahed, "A computational framework for predicting the adhesion strength of bonding in cold spray", ITSC 2023 (Québec), talk 2023-05-22 | `https://asm.confex.com/asm/itsc23/webprogram/Paper57341.html` | abstract only | (HTML, not hashed) | whole abstract |

Source #3b is not in the task table. It is named in DECISIONS 2026-11-13 ("peridynamic bonding … arXiv:2403.01311")
and is open, so it is read here.

**Page references.** #4: journal pages (p. 1590). #3b: arXiv page numbers (p. 12). #3: section name and
paragraph index of the BioC text (¶n); statements added from the PDF carry journal pages (p. 1832). #1: printed
thesis pages. #2: article pages 1–17.

### Not obtained

| # | Source | Why | What would get it |
|---|---|---|---|
| 5 | Z. Dai, J. Wang, F. Xu, W. Feng, "Physically based interaction model of cold spray particle bonding via smoothed particle hydrodynamics", Comput. Mech. 77(5) (2025) 1433–1454, doi:10.1007/s00466-025-02714-1 (pages from OpenAlex; #4 ref. 49 prints "77:1–22") | closed. **The task's "Wang, J. et al." is this paper; Dai is first author** (OpenAlex, and #4 ref. 49 and p. 1587) | Peter or Alex |
| — | Z. Dai, F. Xu, Q. Yang et al., "Adhesion strength prediction of cold spray particle via smoothed particle hydrodynamics", Int. J. Solids Struct. 330 (2026) 113875 (#4 ref. 60) | not in the task; #4 cites it for the adhesion-strength method (p. 1595). Not looked for | Peter or Alex, if wanted |
| — | A. A. Khoei, MASc thesis, Univ. of Waterloo, UWSpace handle 10012/20121, "A Computational Framework for Predicting the Adhesion Strength of Bonding in Cold Spray" (found by web search) | UWSpace bot challenge (as #1, which Peter downloaded in a browser) | browser download |
| — | R. Hirmand, J. Tang, H. Jahed, "A numerical modelling framework for impact-induced bonding of powder particles in cold spray" ("in submission" in #6) | no published version found in OpenAlex. Possibly published as Hirmand et al. 2024, J. Therm. Spray Technol., doi:10.1007/s11666-024-01803-6, which `coldspray-blind-literature.md` lists under "read only after the blind scoring" (not checked, not read) | after the blind scoring |
| — | B. Ren, J. Song, "Peridynamics simulation of microparticle impact: deformation, jetting, and the influence of surface oxide layer" (#3b ref. 52, "under review" in 2024) | not looked for further | — |
| — | H. Zhang, B. Ren, S. Yue, J. Song, "Numerical prediction of critical velocity and spray angle windows for particle adhesion in cold spray using peridynamics", ITSC 2025, doi:10.31399/asm.cp.itsc2025p0074 (OpenAlex: bronze) | found by the sweep, not in the task; not fetched | — |

### Blind screen (B06, B07, B16)

- **#1, #2, #3, #3b, #4:** none cites B06 (Wu 2026, Scripta), B07 (Liu 2025, Surf. Interfaces) or B16
  (Kajihara 2024, Acta). Checked by searching the reference lists for author, DOI and title.
- **#1 (Tang 2021):** cites no blind-list paper. Its experimental critical velocities come from its ref. [9],
  Hassani-Gangaraj et al. 2018 (HG2018b), which the blind file excludes as already exposed.
- **#2 (Ge 2026):** cites B03 and B12 (refs. [72], [71]), both closed and exposed since 2026-11-08, and B02 (Lucas &
  Schuh 2025, its ref. [21], p. 1, qualitative only; B02 scored on 2026-11-07).
- **Other hold-out papers cited (not in the task's screen, flagged for the leak scan):** #3b cites **B03** (Tiamiyu
  et al. 2021, its ref. 72) and **B14** (Lienhard et al. 2020, its ref. 16). The B03 citations (pp. 7, 11, 14, 20–21)
  are qualitative statements about oxide and jetting. On p. 7 an oxide thickness is attributed to refs. 71–72
  together; I leave that value out (B03 is closed and exposed since 2026-11-08, so this is conservative). No B14
  value is quoted (B14 scored on 2026-11-07).
- #3b p. 12 quotes a critical velocity of 470 m/s (10 µm Cu, 2.5 nm oxide) from its ref. 73 (Hassani-Gangaraj et
  al. 2019, Appl. Surf. Sci. 476; not on the blind list). Used in §3b item 7.
- #4 cites a different Tiamiyu paper (ref. 47, Mater. Today 72, 2024) for PTW; it is not B03 and no value is used.
- #6 is an abstract with no numbers.

---

## 3. Ren & Song 2022: peridynamics with adhesive contact (J. Therm. Spray Technol. 31)

**1. Method.**
- Non-ordinary state-based peridynamics (SB-PD) for the bulk, using the nonlocal deformation gradient (shape tensor
  K, influence function ω) and the first Piola–Kirchhoff stress to plug in a classical model ("State-Based
  Peridynamic Theory", ¶17–22).
- Meshfree discretisation after Silling & Askari (nodes with volumes) ("Numerical Implementation", ¶24).
- Horizon δ = 3 × the average node spacing (¶14).
- Plasticity: Johnson–Cook flow stress, radial return on the unrotated Cauchy stress, adiabatic heating with
  Taylor–Quinney 0.9 (¶59–63). Cu parameters in Table 1 (¶58; A = 90 MPa, B = 292 MPa, n = 0.31, C = 0.025,
  m = 1.09).
- Code: Peridigm (Sandia, open source) with an added in-house C++ module (¶53).
- **Stabilisation** against zero-energy modes of SB-PD: not mentioned (BioC text and PDF searched).

**2. Contact and interface.**
- Separate bodies; contact forces act between node pairs of different bodies within a "critical contact radius"
  in the current configuration (proximity search) (¶25–29, ¶32).
- No surface normals and no surface area are used: forces are along the pair direction (¶25–26). The authors name
  this as an advantage for irregular interfaces (¶12).
- Repulsion-only contact is used as the no-adhesion case (¶55).
- The wording of ¶48 speaks of "normal pressure", "contact surface area" and a "compression force in the normal
  direction"; the force itself is computed per node pair (¶25–26). **Reading:** "normal" there means the pair
  direction.
- The FE benchmark uses Abaqus surface-to-surface penalty contact (¶55).

**3. Bonding law.**
- **Contact model 1:** a Lennard-Jones type pair potential, exponents 12 and 6, between nodes of different bodies
  (¶35–43).
  - The equilibrium length "is set a little larger than the node spacing" (¶36).
  - Potential and force (PDF, Eqs. 15–17, pp. 1831–1832): φ = α[(r0/r)^12 − 2β(r0/r)^6], F_c = (12α/r0)[(r0/r)^13 −
    β(r0/r)^7] r̂; zero force at r_e = r0 β^(−1/6).
  - Cut-off radius: "the cut-off radius Rc is set to be 2.75r0" (p. 1832; ¶36).
  - Repulsion parameter: from the bulk modulus, through a linear-spring approximation of the potential at
    equilibrium (¶38–42): α ≈ 18 k r0² ΔV_x ΔV_y / (72 β^(7/3) π δ⁵) (Eqs. 18–22, p. 1832), with k the bulk modulus
    and δ the horizon.
  - Adhesion parameter β: **free**, "tuned to provide desired adhesion" (¶43). Fig. 7 gives CoR against β; CoR
    reaches 0 above a threshold β that depends on velocity (¶76): at 500 m/s it "drops to zero when β exceeds a
    threshold value of 4.5 × 10⁻³" (p. 1836). Fig. 7 covers 400, 500 and 600 m/s; the thresholds for 400 and
    600 m/s are not stated in the text ("differ", p. 1838).
- **Contact model 2:** an interface force–stretch law (linear rise, exponential softening, zero at full
  separation), fitted to the force–stretch curve of a **numerical** tensile fracture test of the bulk PD material
  (Fig. 1, ¶46–48). Compression uses the same law with negative stretch (¶48). Once fitted it has no free adhesion
  parameter (¶49). Equations (PDF, p. 1832–1833): tension f_c = c s_y exp(−m(s − s_y)) beyond the yield stretch s_y
  (Eq. 24), compression f_c = c|s| (Eq. 25), with the critical stretch tied to G_c = π c s_c² δ⁵/10 (Eq. 23). The
  fitted s_y and m are not given as numbers (Fig. 1 only).
- **Activation:** none. Bonds form whenever two nodes come within the contact radius (¶32). No oxide, no
  pressure or strain threshold (¶7: "native oxide films … are not considered").
- **Reading:** both laws make the bond independent of local deformation; whether the particle stays depends only on
  adhesion energy against rebound energy.

**4. Regularisation or length scale.**
- The PD horizon (3 spacings) and the contact radius are numerical lengths tied to the node spacing (¶14, ¶32: "an
  adjustable numerical parameter").
- No claim and no test of independence from the discretisation.

**5. Verification against exact references.** None. The bulk deformation is compared with an Abaqus/Explicit
axisymmetric model at the same element size: shapes at 400, 500 and 600 m/s, PEEQ and temperature at 400 m/s
(Figs. 3–5, ¶67–70). The agreement is stated as "compare fairly well"; no numbers.

**6. Convergence.** No resolution study. One resolution: FE elements d/50, PD node spacing "about the same" (¶54),
i.e. **about R/25** (25 spacings across the radius; my conversion). Edge quantities: the paper says FE shows
"unphysically large PEEQ" at the outermost periphery, and PD alleviates it "to some extent" but "not completely"
because of its total-Lagrangian nature (¶70).

**7. Validation against experiment.** None shown. ¶7 asserts the model "can also reproduce the adhesion strength …
that is consistent with experimental observations", and ¶93 that the bond strength "can be calibrated with
experimental measurements"; neither is demonstrated with data. The adhesion-strength calibration by a numerical pull-off
test is described as a "proof-of-concept type demo" (Fig. 11, ¶89).

**8. Impact conditions.** Cu (30 µm) on Cu, 400–600 m/s for the FE comparison (¶53, ¶67); the adhesion study at
500 m/s (¶73). The CoR study (Fig. 7, ¶75–76) uses 400, 500 and 600 m/s (Fig. 7 caption, p. 1838). Runs to 190–304 ns
are shown (¶73, ¶81).

**9. Dimension, scale, cost.** PD in full 3D; substrate radius and height 4 × the particle radius, "confirmed to
[be] sufficient" so that results do not change with a larger substrate (a domain-size check, not a resolution check)
(¶53, ¶67). Sides restrained laterally, bottom fixed (¶54). Single
particle. Multi-particle is stated as a possible extension, not done (¶93). Cost not stated.

**10. Stated limits.** Oxide not modelled (¶7); contact model 2 cannot vary adhesion after the fit (¶49); the
total-Lagrangian nature of PD does not fully remove unphysical edge strains (¶70); the pull-off calibration is a
proof of concept (¶89).

Numbers (text version, completed from the PDF): Table 2, maximum adhesion force for six β cases at 500 m/s: 0.93, 7.57,
17.33, 24.25, 30.44, 48.95 **mN** (unit from the PDF), for β = 2.5, 3.5, 4.0, 4.3, 4.5 and 5.0 × 10⁻³ (Table 2,
p. 1839; ¶83). Contact-force history example: −18.7 m/s at 270 ns with force 0.02 N,
then −0.98 m/s after 34 ns with 0.09 N (¶81).

## 3b. Ren & Song 2024: peridynamics with an oxide shell (arXiv:2403.01311v3)

**1. Method.**
- Peridigm (p. 4). Metal: non-ordinary state-based PD with Johnson–Cook (Table 1, p. 5; Cu as in #3, Fe added).
- Oxide shell: **ordinary** state-based PD with the critical-stretch bond-failure criterion; the critical stretch
  s0 comes from the energy release rate G0, the shear and bulk moduli and the horizon δ (eqs. 3–4, p. 6). Oxide
  properties (CuO/Cu₂O and Fe oxide: density, E, ν, fracture toughness) in Table 1 (p. 5).
- **2D plane strain**, with the z-freedom constrained (p. 5). Not axisymmetric.
- The implementation of these PD material models is referred to #3 (p. 5).

**2. Contact and interface.** Not described in this paper (no section on contact; p. 5 refers only the PD
material-model implementation to #3).
**Reading:** presumably the pair contact of #3; not confirmed by the text.

**3. Bonding law.** None in the solver. Bonding is inferred afterwards from surrogate events (pp. 11–12):
- oxide discontinuity (complete damage of the oxide at the contact) marks fresh metal contact (p. 14);
- substrate-only jetting = "limited metallurgical bonding"; jetting of both substrate and particle = "exceeding
  the critical velocity" (p. 11);
- the fraction of oxide points left at the interface, N = N_I/N_T, as a measure of cleaning (eq. 7, p. 19).

**4. Regularisation or length scale.** The horizon δ enters s0 (eq. 4). Normalisation N = N_I/N_T is introduced "to
address potential discrepancies arising from discretization variances … across the entire particle size range"
(p. 19). No discretisation-independence claim or test.

**5. Verification against exact references.** None.

**6. Convergence.** No resolution study. **Node spacing and horizon are not stated.** Fig. 1b (p. 6) shows the oxide
as one row of points round the particle. **Reading:** a 2.5–60 nm oxide resolved by one row of points on a 5–50 µm
particle means either a very fine spacing at the surface or an oxide whose thickness enters only through
properties; the paper does not say which.

**7. Validation against experiment.**
- Qualitative: thicker oxide restricts deformation, consistent with experiments (p. 7, refs. 71–72).
- The fitted size exponents of N (Table 2, p. 20: α = −0.199 and −0.192 for Fe at 550 and 600 m/s; −0.236 and
  −0.225 for Cu at 450 and 500 m/s) are compared with the measured exponents of the critical velocity of Schmidt
  et al. 2006 (−0.14 for 316L, −0.19 for Cu) (pp. 18, 20). **Reading:** the comparison identifies an oxide-fraction
  exponent with a v_cr exponent by assumption ("if oxide removal is considered the critical condition", p. 20).
- Semi-quantitative (p. 12): the substrate-jetting onset at 400–450 m/s for 2.5 nm oxide is called "reasonable"
  against a literature critical velocity for a 10 µm Cu particle (ref. 73, Hassani-Gangaraj et al. 2019, not
  blind; value under "Blind screen"); the drop of the jetting velocity from 5 to 2.5 nm oxide is said to
  "correspond well" with experiments over 20 → 2 nm (ref. 73).
- No quantitative validation of shapes.

**8. Impact conditions.** Cu-on-Cu and Fe-on-Fe; d = 5–50 µm; 100–750 m/s; oxide 2.5–60 nm (pp. 7, 11, 14, 18,
20). Nothing above 750 m/s.

**9. Dimension, scale, cost.** 2D plane strain, single particle, substrate ~5 d wide and deep (p. 6). Cost not
stated.

**10. Stated limits.** The 60 nm results "require further validation through experiments" (p. 12); the
size–critical-velocity relation is "a qualitative prediction" (p. 4).

## 4. Dai, Xu, Wang, Ye & Feng 2026: updated-Lagrangian SPH, dual and multi-particle (Comput. Mech. 78)

**1. Method.**
- **Updated-Lagrangian SPH** (ULSPH), neighbour list rebuilt each step (pp. 1588–1589). Mass, momentum and energy
  equations in standard SPH form with the Monaghan artificial viscosity Π_ij (eq. 14, p. 1591; ref. 51).
- Kernel: Wendland (p. 1591). Adaptive smoothing length, dh/dt = −h/(DIM ρ) dρ/dt (eq. 16, p. 1591). **The h/Δp
  ratio is not stated.**
- **Kernel gradient correction** (KGC, Shao et al. 2012): the kernel gradient multiplied by the inverse of the
  first-moment matrix (eq. 15, p. 1591). The paper uses it "to address the accuracy limitations arising from the
  inconsistency and tensile instability" (p. 1591). **No separate tensile-instability treatment** (no artificial
  stress) and **no zero-energy-mode or hourglass control** are mentioned.
- Stress: Mie–Grüneisen pressure, Jaumann rate for the deviator, radial return to von Mises; **Preston–Tonks–Wallace**
  flow stress (eqs. 2–10, pp. 1589–1590). PTW parameters only by reference (refs. 30, 46; p. 1590).
- Time integration: leapfrog, CFL Δt ≤ ζ h/(c0 + |v|), ζ ≈ 0.3 (eqs. 17–20, p. 1592).
- Code: in-house, CUDA + MPI, multi-GPU, domain decomposition with 2h halos (pp. 1592–1593).

**2. Contact and interface.**
- Separate bodies interact only through the "physically based interaction model" F_CS (eq. 14, p. 1591).
- Before bonding, contact model f1 (eq. 12, p. 1591): a repulsive pair force (B_ij/β) W_ij r_ij/|r_ij|² × 2m_j/(m_i+m_j)
  within 2h, with B_ij = K (C_ij + |v_max|)², K = 0.01 (contact stiffness), C_ij the mean sound speed, v_max the
  largest velocity in the calculation, and β the ratio of the two bodies' particle spacings (p. 1591). Details by
  reference to #5 (ref. 49).
- **No surface normals.** The force is along the pair vector (eqs. 12–13).
- Contact area S for the adhesion strength: "the area of the contact region … within a distance of 2h",
  S = π(L² + 4 D_S²)/4 from the measured diameter L and depth D_S of the
  contact region (p. 1596). It "can also be obtained through the area integral of surface SPH particles at the
  interface" (p. 1596); which one is used in the results is not said.

**3. Bonding law.**
- **Activation:** f1 switches to f2 for a pair when **both** points have equivalent plastic strain ε_p ≥ ε_th
  (eq. 11, p. 1591). ε_th = 1.4 for Cu. It "depends on the fracture strain and thickness of the oxide, as well as the
  onset strain of shear instability in the metal", with the derivation in #5 (p. 1591).
- **Bond law f2:** a 12-6 Lennard-Jones pair force, ω Δp² × (mass factor) × [(δ/|r|)¹² − (δ/|r|)⁶], within 2h
  (eq. 13, p. 1591). ω = 1.5392 × 10¹⁰ Pa for Cu; δ = 1.5 Δp (equilibrium distance); Δp = initial spacing.
  Parameter derivation by reference to #5 (p. 1591).
- No pressure condition, no separate oxide model; the oxide (5–30 nm) enters only through ε_th (pp. 1590–1591).
- Adhesion strength: F_adh / S, F_adh = sum of the absolute attractive forces along the impact direction
  (eq. 21, pp. 1595–1596).
- **Reading:** δ and the cut-off are fixed multiples of Δp and h, so the bond's range is a numerical length, and
  ω Δp² scales the pair force with the spacing. Whether F_adh/S is then independent of Δp is not shown in this paper
  (see item 6). The threshold acts on the point value of ε_p, which is exactly the edge quantity whose convergence is
  in doubt in our route.

**4. Regularisation or length scale.** None stated beyond the numerical bond range (δ = 1.5 Δp, cut-off 2h).
No claim of discretisation independence for the bond.

**5. Verification against exact references.** None. The two "benchmarks" are against experiments:
- Taylor bar, Cu, L = 70 mm, r = 10 mm, 165 m/s (p. 1593): shapes compared in Fig. 4b; no numbers. The condition
  number of the correction matrix stays lower with KGC than without (Fig. 5, pp. 1593–1594).
- Hypervelocity impact, Al sphere 10 mm on 4 mm Al plate at 6180 m/s, spacing 1 mm (p. 1594): hole diameter 26.5 mm
  against 27.5 mm measured, debris-cloud aspect ratio 1.34 against 1.39. Their own TLSPH run "terminated at
  0.43 µs" at first contact "due to excessive topological changes" (p. 1594, Fig. 6c).

**6. Convergence.**
- One resolution study, single particle, 605 m/s: fine spacing d/80, d/65, d/50, d/35 (text, p. 1594; the axis of
  Fig. 8c reads 1/80, 1/60, 1/50, 1/35), i.e. **about R/40, R/32, R/25, R/17.5**; the coarse substrate region has
  twice the spacing (p. 1594). The legend of Fig. 8b reads 1/65, the axis of Fig. 8c 1/60.
- Quantity shown: only the **flatness ratio** L/D_P. Fig. 8c (p. 1596; fig., ±0.03): 2.42 (1/80), 2.37 (1/60 or
  1/65), 2.21 (1/50), 2.10 (1/35), against ≈ 2.47 measured. The text calls this "good convergence performance" and
  adopts d/80 (≈ 0.2 µm) (p. 1595). **Reading:** the ratio still changes by 0.05 between the two finest levels and
  is approached monotonically from below; convergence is not established, and the finest level is the one chosen.
- **Not shown at any resolution:** adhesion strength, bonded area, ε_p, temperature or pressure at the contact edge,
  energy error.
- Energy: in the multi-particle runs the total energy **rises** by 4 % (uniform) and 5 % (random), ascribed to
  "round-off errors introduced by the interaction model" (p. 1600).

**7. Validation against experiment.**
- Single particle: deformed profile against an SEM section of Lemiale et al. 2014 (16.5 µm Cu, 605 m/s) (Fig. 8,
  p. 1596).
- Annular bonded region against an SEM of a peeled splat ("Xu et al. [61]"; ref. 61 in the list is Song et al.
  2018), described as similar in pattern, with different materials and conditions (p. 1596).
- Single-particle adhesion strength against velocity, against "experimental results for 15 µm Cu particles [62]"
  (ref. 62 = Assadi et al. 2011, J. Therm. Spray Technol. 20) (Fig. 9c, p. 1596; fig., ±5 MPa, ±10 m/s):

  | v (m/s) | ~470 | ~545 | ~575–580 | ~620 | ~635 | ~725 | ~815 |
  |---|---|---|---|---|---|---|---|
  | model (MPa) | 40 | 48 | 98 | 103 | 118 | 140 | 165 |
  | experiment (MPa) | 50 | 67 | 50 | 90, 120 | 130 | — | 195 |

  The paper says "agrees well … except for minor discrepancies caused by different deposition conditions"
  (p. 1596). **Reading:** differences up to ~50 MPa at ~575 m/s and 30 MPa at ~815 m/s; that the cited source holds
  measured single-particle adhesion strengths is not checked here.
- Multi-particle coating adhesion (Table 1, p. 1604): 128 MPa (uniform model), 154 MPa (random model) against
  151 MPa (Huang & Fukanuma 2012, Cu/Cu) and 170 MPa (Singh et al., Cu/steel).
- Porosity (Table 2, p. 1605): 5.20 % (uniform), 3.28 % (random) against 0.98 % (Cu/Cu) and 1.07 % (Cu/Al). The
  paper calls this a "tendency to overestimate" (p. 1605).
- Trends with velocity (605–768 m/s: 151.55 → 174.35 MPa, porosity 8.01 → 0.86 %) and particle density
  (99.07 → 154.58 MPa, porosity 12.75 → 2.28 %) are not compared with data (pp. 1605–1606); the size-distribution
  porosity trend is said to agree with Wong et al. (p. 1605).

**8. Impact conditions.** Cu on Cu throughout. Dual-particle adhesion of the first particle (Fig. 13, p. 1599):
90.7 MPa single → 101.1 (central), 110.5 (offset), 59.2 MPa (contactless second impact). Single particle 16.5 µm (text) at 605 m/s for the resolution study;
~470–815 m/s in Fig. 9c. Dual-particle: 12 µm, 605 m/s (p. 1597). Multi-particle: 290 particles of 12 µm or 212 of
8–20 µm, 648 m/s; velocity study 605–768 m/s (pp. 1600, 1605–1606). **Fine-resolution runs at 800–1100 m/s:** only
the ~815 m/s single-particle point of Fig. 9c, resolution not stated for it.

**9. Dimension, scale, cost.** 3D (Fig. 7, Fig. 14). Single-particle substrate 72 × 72 × 36 µm with a
non-reflecting "virtual particle boundary" on bottom and sides (p. 1594); the multi-particle substrate has three
resolution levels, the finest "matching the particles" (p. 1600). Single, dual (three geometries) and multi-particle (up to 290).
A fine model "typically contains more than ten million SPH particles" (p. 1592). Run times and GPU counts are not
given.

**10. Stated limits.** Energy gain 4–5 % from the interaction model (p. 1600); porosity overestimated, ascribed to
hundreds instead of thousands of particles (p. 1605). ULSPH "faces the dual challenges of tensile instability and
higher computational costs" (p. 1588).

**Internal inconsistencies noticed** (not errors of my reading):
- Fig. 7 (p. 1595) shows a 12 µm particle at 605 m/s; the text of §3.2 says 16.5 µm (p. 1594). d/80 ≈ 0.2 µm fits
  16.5 µm.
- Resolution 1/65 (text, p. 1594, and Fig. 8b legend) against 1/60 (Fig. 8c axis, p. 1596).
- Porosity of the uniform model: 5.3 % in the text (p. 1605) against 5.20 % in Table 2.
- Figure panels cite "[57]" and "[59]" where the captions cite [58] and [61] (p. 1596); "Xu et al. [61]" against
  ref. 61 = Song et al. 2018.

## 6. Khoei, Hirmand & Jahed, ITSC 2023 (abstract only)

What the abstract states (asm.confex.com, Paper57341):
- **Method:** material point method (MPM). The implementation "effectively eliminates spurious mesh dependence and
  captures complex phenomena such as jetting".
- **Bonding law:** a strain-like history variable, the "bonding parameter", from #1 and Hirmand, Tang & Jahed (in
  submission), "based on the commonly held view that bonding occurs due to large plastic strains occurring at
  extreme rates". **Two material constants:** a critical surface adhesion energy and a critical surface adhesion
  energy rate. Added: a "semi-empirical evolution law for adhesion strength on bonding boundaries", coupled to the
  bonding parameter.
- **Validation (claimed):** "desirable agreement with known experimental data such as critical bonding velocity,
  adhesion strength, and deformed particle/substrate shape". No numbers, no materials, no resolutions.
- Contact, regularisation, verification, convergence, conditions, dimension, cost, limits: not stated.

**Reading:** the "mesh dependence" claim is about the bonding model in MPM; what it is tested on cannot be judged
from the abstract. #1 and the Khoei thesis (UWSpace 10012/20121) are the sources for it.

## 1. Tang 2021: MPM with a bonding parameter (MASc thesis, Waterloo)

Read in full for task b11 (`docs/research/data/boundary_integration_reading.md` on the unmerged branch
`coldspray/boundary-integration-reading`, section G, which also covers item 6 in more detail).
Printed page numbers.

**1. Method.**
- In-house MPM (MUSL, multi-mesh contact) for single and multiple Al particles on Al (ch. 3; Fig. 4.1, p. 40).
- Material: PTW strength, SCG melt model, linear Mie–Grüneisen EOS, adiabatic heating (§3.5.1–3.5.3).
- Viscous damping boundaries represent the semi-infinite substrate (§3.5.5, pp. 35–36).
- Computed on the Niagara supercomputer, with a 24 h run limit (p. 48).

**2. Contact, normals, area.**
- Contact on the grid, between the bodies' multi-meshes. The contact normal is the substrate's, by the maximum
  volume (here mass) gradient; the particle's normal is set opposite, for collinearity (§3.5.4, pp. 34–35).
- Normals are "a known source of error in MPM" and are left to future work (pp. 34–35, 82–83).
- No contact area enters the bond. The bond acts at grid nodes.

**3. Bonding law.**
- **Variable:** a history variable D_bond per material point on the contact surface, mapped to grid nodes and
  averaged between the two bodies (eqs. 4.6–4.7, p. 39).
- **Bond force:** when the nodal D_bond(I_g) ≥ 1, the sticking contact force, which sets zero relative velocity, is
  applied in the separation phase (p. 39).
- **First model, strain-based (Hirmand et al., §4.1):** ΔD_bond = Δε_s^p / ε_bond, with ε_bond = ε_c (1 −
  ln(ε̇_s^p/ε̇_c)), driven by the shear plastic strain (eqs. 4.3–4.5, pp. 38–39). It is dropped as grid-sensitive
  (§4.1.3) and because it initiates bonds in the jetting rim (§4.1.4).
- **Final model, energy-based (§4.3):** D_bond = Σ ΔG_s / G_bond, with G_bond = G_c (1 − ln(ΔG_s/(Ġ_c Δt))) and
  ΔG_s = σ_vm Δε_p D_Cell (eqs. 4.16–4.17, pp. 51–52).
- **Activation:** D_bond reaching 1. No oxide, no pressure threshold (normal pressure is assumed sufficient for
  normal impacts, p. 38).
- **Parameters:**
  - Two constants, calibrated by logistic regression on the restitution ratio and on the percentage of bonded
    contact particles (PBCP), against experimental critical velocities for 14 µm and 30 µm Al. The velocities are
    from its ref. [9], Hassani-Gangaraj et al. 2018, not a blind paper.
  - Result: G_c = 1503.74 J/m² and Ġ_c = 2.271 "J/m²s" (pp. 66, 69). The conclusions print the rate unit as
    "J/m²µs" (p. 81). The unit is inconsistent in the source.
  - Bonded-particle threshold: about 5 % PBCP (pp. 69, 79–80). This is a classification tolerance of the
    calibration, not an independent prediction.
  - The classification tolerances "had to be adjusted" to get an intersection; some results "had to be
    incorrectly classified to achieve similar bonding boundaries" (Fig. 5.3, p. 57). With the expected tolerances
    the boundaries show "a clear difference between particle sizes and a lack of intersection" (Fig. 5.4, p. 58).

**4. Regularisation or length scale.** The grid length D_Cell in ΔG_s, after the crack-band regularisation of
fracture mechanics (eq. 4.16, p. 51), where the scaled fracture energy is "an 'algorithmic' value" (p. 51). So G_c
is a grid-scaled value, not a physical one. The author: "this insensitivity is more as a result of including D_Cell than
purely switching to an energy measure" (p. 52).

**5. Verification against exact references.** None.

**6. Convergence.**
- **Grids:** 1.5, 1.0 and 0.7 µm, three particle spacings each (Table 4.2, p. 52). Without a bond, the no-bond study
  also used 0.5 µm (Table 4.1, p. 47).
- **Converging, by the author's account:**
  - the bonding boundaries in the (G_c, Ġ_c) plane are "similar" across the nine configurations (Fig. 5.7,
    pp. 64–65);
  - the PBCP tolerance falls from about 8–9 % at 1.5 µm to about 5 % at 0.7 µm (Table 5.2, p. 60), "a clear
    convergence".
  - Both are obtained with classification tolerances chosen per grid (item 3).
- **Not converging:** the particle shape and the jetting change between 1.0 and 0.7 µm (Fig. 5.8, pp. 65–66), and
  the average plastic strain varies "drastically" with the grid without a bond (p. 48).
- **Not reported:** Y and p_n.
- **Reference:** a time-step reference only (pp. 66–67).
- **Reading:** a 14 µm particle at a 0.7 µm grid is about R/10 in grid cells (points 0.175 µm apart, about R/40).
- The ten-particle run uses the coarser 1.0/0.35 grid (p. 77; about R/7 in grid cells).

**7. Validation against experiment.**
- **Calibration:** the critical velocities of ref. [9] are calibration targets, so they are not independent
  validation.
- **Predictions:**
  - predicted critical velocities of 824, 809, 791, 776 and 761 m/s for 14, 18, 22, 26 and 30 µm (Table 5.4,
    p. 73), "decreases linearly" (p. 73); at the two calibration sizes that is 824 vs 810 and 761 vs 770 m/s. The
    14 µm value used adjusted tolerances (4.8 %, 0.9 m/s; p. 71), and linear interpolation between the two sizes is
    assumed in the analysis (p. 69);
  - a qualitative comparison of jetting with high-speed images of a 45 µm particle at 550 m/s (its ref. [12],
    Hassani-Gangaraj et al. 2019; Fig. 5.10, pp. 67–68);
  - a bonded fraction of about 5 %, set against a theoretical ~5 % for Cu (its ref. [60]) and a 15–95 % range (its
    ref. [90]) (pp. 79–80);
  - bond initiation shifted from the jetting rim towards the south pole, in line with Rahmati & Jodoin (p. 79).

**8. Impact conditions.**
- Al on Al, normal impact, room temperature.
- Particles 14–30 µm; substrate a cylinder 10 µm high and 30–50 µm across (Table 5.3, p. 69).
- Impact velocities 750–830 m/s in the prediction runs at the 0.7/0.175 grid (≈ R/10 in grid cells), PBCP read at
  80 ns (p. 69); also 45 µm at 550 m/s and 38 µm at 780 m/s (Fig. 5.10, p. 67). Overall 14–45 µm and 550–830 m/s.
- Only the no-bond convergence runs to 1000 ns were cut by the 24 h limit (p. 48).

**9. Dimension, particles, cost.**
- 3D. The figures of the particle show 3D point clouds (Fig. 5.17, p. 79); no symmetry reduction is stated.
- Single particles, plus two- and ten-particle impacts (§5.2.2–5.2.3, pp. 73–77).
- Cost: only the 24 h limit, which some runs reached (p. 48).

**10. Stated limits.** The model answers only "bonded or not" per material point and is "entirely incapable" of a
bond strength in MPa (p. 82). Also stated:
- Al/Al only.
- Oxide not modelled.
- Friction and normals left to future work (pp. 82–83).

## 2. Ge, Zhou, Bagherifard & Guagliano 2026: Eulerian FE with a nonlocal regularisation (Int. J. Mech. Sci. 321)

Journal pages of the article (1–17). It is CC BY.

**1. Method.**
- Abaqus/Explicit, Eulerian domain (App. D, p. 15), 8-node thermally coupled reduced-integration elements (EC3D8RT), with the
  default artificial viscosity (§3.1, §3.3, pp. 4–5).
- A new flow-stress model (eq. 1, p. 3) in a VUMAT: J2 radial return, Newton–Raphson with bisection (§3.2, p. 5).
- Cu parameters: Table 2 (p. 6), for example σ_y0 = 39 MPa, A = 320 MPa, n = 0.41, B = 110 MPa, T_ref = 350 °C.
- Heat diffusion included (§3.2).
- A quarter model, with a 100 µm cubic Eulerian domain (§3.1, p. 4).

**2. Contact, normals, area.** Abaqus Eulerian contact, "a default, non-modifiable setting" (§3.1, p. 4). No
normals or areas are handled by the authors.

**3. Bonding law.** **None.** The paper models deformation only. Bonding strength criteria are named as future
applications (§6, p. 13). The highest plastic strain sits in the jetting region, "also reported as the typical
location with the highest adhesion strength [77]" (p. 6).

**4. Regularisation or length scale.**
- **Hybrid nonlocal strategy (§5, pp. 9–12):** equivalent plastic strain and its rate are replaced by implicit-
  gradient nonlocal values, l²∇²γ̄ + γ − γ̄ = 0 (eqs. 15, 19). The temperature is replaced by an over-nonlocal
  value T̂ = 2T̄ − T (m = 2; eqs. 16, 23).
- **Implementation:** through Abaqus's heat equation as an analogue (eqs. 18–22).
- **Characteristic length:** l = 4 µm, "l = 2/5 d", found iteratively so that the simulated morphology matches
  experiment (p. 12). The paper: it "can be treated as a material parameter
  [83]". A second nonlocal parameter, c′_p = 0.001, makes the time term of eq. 20 vanish (p. 12). **Reading:** l
  is fitted, not a numerical length.

**5. Verification against exact references.** None.

**6. Convergence.**
- **Mesh sizes:** h = d/25, d/50 and d/100 (≈ R/12.5, R/25, R/50; my conversion) at three velocities (590, 918 and
  1058 m/s), under four settings: no thermal softening, adiabatic, heat diffusion, nonlocal (§4–5, pp. 6–12;
  Figs. 7, 8, 10, 12).
- **Without the strategy:**
  - finer meshes give narrower shear bands and higher peak plastic strain;
  - at d/100, "unrealistic melting" occurs at 918 and 1058 m/s with the adiabatic setting and at 1058 m/s with
    heat diffusion (Fig. 9, pp. 7–8); at 590 m/s the heat-diffusion runs are "almost identical" across meshes (p. 7).
- **With it:** "overall consistent particle deformation and almost identical local jetting across different mesh
  sizes"; the kinematic sensitivity "was significantly mitigated", although the strategy "didn't fully eliminate" it
  (p. 12). The maximum equivalent plastic strain matches "better" across meshes, with "nearly identical shear band
  widths" (p. 12); the maximum sits in the jetting region at the interface (p. 6).
- **Evidence:** visual (figures). No convergence numbers are given for shape, strain or temperature.
- **Not reported:** interface quantities (Y, p_n), because there is no bond.

**7. Validation against experiment.** Profiles of deposited Cu particles against the SEM profiles of Tiamiyu et
al. [71, 72], which are B12 and B03 (both closed and exposed since 2026-11-08), at six impact velocities from 590
to 1058 m/s (Figs. 3–5, pp. 5–8):
- overlap ratio 85.6–96.3 % with the new model; MW model down to 61.8 % at 1058 m/s;
- flattening ratio within 5 % of experiment, with the experimental values from [71] = B12 (p. 6).

All at d/50 and without the nonlocal strategy (§3.4).

**8. Impact conditions.** Cu 10 µm sphere on Cu, 25 °C, 590–1058 m/s (§3.3, p. 5). The d/100 runs at 918 and
1058 m/s finish (Table D.1). Without the nonlocal strategy they show unrealistic melting (Fig. 9); with it, none
(pp. 12–13).

**9. Dimension, particles, cost.**
- 3D quarter model.
- Single particle.
- Run times (Table D.1, p. 15): at 918 m/s, 2.2 / 21 / 135 min at d/25 / d/50 / d/100 without thermal softening,
  and within 1 % of these with the nonlocal strategy.

**10. Stated limits.** The flow-stress model is empirical. It may lose accuracy above 10⁷ s⁻¹ or above about
1100 m/s, near melting, with phase changes, and with damage, fragmentation or "oxide layer spallation" (Appendix A,
p. 14). The nonlocal strategy does not fully remove the kinematic mesh sensitivity (p. 12).

**Blind note.** Ge validates against B03 and B12 (refs. [72], [71]), both closed and exposed since 2026-11-08,
so no blinding applies to them. No B06, B07 or B16 material appears (searched). The six impact velocities are
in §3.3 (p. 5); the abstract gives the range 590–1058 m/s.

## 5. Dai et al. 2025: not read

Dai et al. 2025 (#5) is closed (see "Not obtained").

---

## Comparison (sources read so far)

Short form of items 1–9. "—" = not stated. R/n = spacings across the particle radius (my conversion).

| Source | 1. Method, code | 2. Contact; normals, area | 3. Bonding law; activation; parameters from | 4. Regularisation | 5. Exact-reference verification | 6. Convergence (resolutions; what converges) | 7. Validation (numbers) | 8. Conditions | 9. Dim.; particles; cost |
|---|---|---|---|---|---|---|---|---|---|
| #1 Tang 2021 | MPM (MUSL, multi-mesh contact), PTW, SCG melt, Mie–Grüneisen; in-house | grid-node contact; substrate normal (max. volume gradient), "a known source of error"; no area | history variable D_bond from ΔG_s = σ_vm Δε_p D_Cell against G_bond(G_c, Ġ_c); sticking contact when nodal D_bond ≥ 1; **no oxide, no pressure threshold**; G_c, Ġ_c calibrated to experimental v_cr (14, 30 µm Al) | grid length D_Cell in the energy increment (crack-band style) | none | grids 1.5, 1.0, 0.7 µm (≈ R/10 in grid cells at 0.7 µm for 14 µm); bonding boundaries "similar", PBCP tolerance ~8–9 % → ~5 % (tolerances chosen per grid); shape not converged; Y, p_n not reported | v_cr are calibration targets (810, 770 m/s); predicted 824 and 761 m/s at those sizes, linear in size; ~5 % bonded fraction is a calibration tolerance; jetting vs HG2019 images, qualitative | Al/Al 14–45 µm, 550–830 m/s | 3D; 1, 2, 10; Niagara, 24 h limit |
| #2 Ge et al. 2026 | Abaqus/Explicit Eulerian (EC3D8RT), new flow-stress model in VUMAT, heat diffusion | Abaqus default Eulerian contact | **no bonding law** | hybrid nonlocal: implicit-gradient ε_p, ε̇_p; over-nonlocal T (m = 2); l = 4 µm (2/5 d), fitted to morphology | none | d/25, d/50, d/100 (≈ R/12.5–R/50); with the strategy shapes and jetting "almost identical", peak PEEQ at the interface matches "better" (figures only) | profiles vs B03/B12 SEM (exposed): overlap 85.6–96.3 %, flattening within 5 % (d/50, no nonlocal) | Cu 10 µm, 590–1058 m/s | 3D quarter; single; 2–135 min |
| #3 Ren & Song 2022 | non-ordinary SB peridynamics + JC; horizon 3Δx; Peridigm + C++ | node-pair forces within a contact radius; no normals, no area | LJ 12-6 pair potential, cut-off 2.75 r0 (β free; CoR = 0 above β = 4.5 × 10⁻³ at 500 m/s) or force–stretch law fitted to a numerical bulk fracture test; **no activation criterion** | none (numerical horizon and contact radius) | none; shapes vs Abaqus axisym. FE, qualitative | one resolution, ≈ R/25; none shown | none (pull-off calibration as concept) | Cu 30 µm, 400–600 m/s | 3D; single; — |
| #3b Ren & Song 2024 | SB-PD metal + ordinary PD oxide with critical stretch (s0 from G0); Peridigm | not described (refers to #3) | **no bond in solver**; bonding inferred from oxide discontinuity, jetting onset, residual oxide fraction | horizon enters s0; normalised oxide fraction | none | spacing not stated; none | qualitative; fitted size exponents −0.19 to −0.24 set against v_cr exponents −0.14/−0.19 by assumption | Cu, Fe; 5–50 µm; 100–750 m/s; oxide 2.5–60 nm | 2D plane strain; single; — |
| #4 Dai et al. 2026 | ULSPH, Wendland, KGC, adaptive h, Monaghan viscosity, PTW; in-house multi-GPU | repulsive pair force f1 (K = 0.01) within 2h; no normals; area from L and D_S (or surface integral) | LJ 12-6 pair force f2 (ω = 1.54e10 Pa, δ = 1.5Δp, cut-off 2h) when **both** points have ε_p ≥ 1.4; ε_th from oxide and shear-instability argument in #5 | none beyond numerical bond range | none; Taylor bar and HVI against experiments (hole 26.5 vs 27.5 mm) | d/35–d/80 (≈ R/17.5–R/40) for flatness ratio only, 2.10 → 2.42 vs 2.47, still moving; adhesion, edge quantities not shown; energy +4–5 % | profile vs SEM; adhesion 40–165 MPa vs 50–195 MPa (fig.); coating adhesion 128/154 (uniform/random) vs 151/170 MPa; porosity 3.3–5.2 % vs ~1 % | Cu 8–20 µm; ~470–815 m/s single, 605–768 m/s multi | 3D; 1, 2, up to 290; > 10⁷ points, time — |
| #6 Khoei et al. 2023 (abstract) | MPM | — | history variable "bonding parameter", 2 constants (critical adhesion energy and its rate) + semi-empirical strength evolution | claims "effectively eliminates spurious mesh dependence" | — | — | claims agreement with v_cr, adhesion strength, shape; no numbers | — | — |
| **Our SPH route** (sph-route-review-2026-11.md) | collocated SPH in an OpenCourant fork; then TLSPH (corrected gradients, hourglass, own viscosity) | body filter + penalty contact; default normals fail C-3 and C-2 (Nanson area); cone-and-fit normal passes C-3 but is not the default | Bay-type: surface expansion Y > Y′ and p_n > extrusion pressure; cohesive separation (D-2 passes: time 3.6 %, energy 1.000) | none; heat conduction refuted as edge regulariser at reachable spacings | SPH particle on brick with the solver's TYPE7 contact passes Hertz (F0: peak 1.037, approach 0.987, rebound 0.992 at R/32); SPH–SPH Hertz B-2 at R/32 fails (approach +16 %, peak 0.86–1.01, rebound 0.84–0.89); peak 1.035, approach 0.981, rebound 0.983 with ξ + order 1 (not adopted); TLSPH T-S0 fails (contact −1.1 to −1.5 %, rebound 0.942) | R/16–R/64 on elastic rungs; edge quantities not converged in any host tried (FE 2D/3D, SPH) | none | two impact probes at R/16 only; FE edge elements collapse at 500–1000 m/s | 3D required; single; 11 days, 2 372 new engine lines |

No ranking and no recommendation (task instruction).

**Reading, for whoever compares (not a ranking):**
- None of the papers read tests its host against an exact elastic reference, and none shows convergence of a
  contact-edge quantity (Y, p_n or a bonded-area edge). Ge 2026 claims a better mesh match of the (nonlocal) peak
  PEEQ at the interface, from figures only. Our route's rungs ask for both. So the papers neither show that these rungs can be passed
  nor that they cannot.
- Dai 2026 runs ULSPH with first-order kernel correction, Monaghan viscosity and adaptive h, without artificial
  stress or hourglass control, in 3D up to 290 particles. Its multi-particle runs reach 605–768 m/s at the adopted
  d/80 (≈ R/30 for 12 µm particles at 0.2 µm); the ~815 m/s single-particle point has no stated resolution. Our runs
  did not reach such impacts.
- In #3 and #4, the bond range is tied to the particle spacing (pair potentials over δ ≈ 1–1.5 Δx, cut-off 2h or a
  contact radius), and no normals or surface areas enter the force. Our route's Bay law needs both.
- The claims of discretisation independence rest on regularisation, not on showing a resolution limit:
  - Tang 2021: the bond-energy increment is scaled by the grid length, so G_c is a grid-scaled ("algorithmic")
    value. Calibrated bonding boundaries agree between three grids (tolerances chosen per grid), but the particle
    shape still changes.
  - Ge 2026: a fixed nonlocal length of 4 µm fitted to morphology. Shapes look alike from d/25 to d/100, but no bond
    is modelled.
  - Khoei 2023: abstract only.

  None of them reports Y or p_n.

## Change log

- 2026-11-13: first version. Read #3 (text only), #3b, #4, #6. #1, #2 not fetched (bot challenges), #5 closed.
- 2026-11-13: review by an agent against the source texts and figures applied (paragraph references in #3, the
  quote and the p. 12 check in #3b, the f1 formula and missing details in #4, wording in the comparison and our row).
  No blind value found; Fig. 8c and 9c readings confirmed within the stated error.
- 2026-11-15: #1 Tang 2021 and #2 Ge 2026 read from Peter's browser downloads; #3 gaps filled from the PDF (equations,
  cut-off 2.75 r0, β threshold 4.5 × 10⁻³ at 500 m/s, Fig. 7 velocities, Table 2 in mN). Comparison rows added;
  #5 remains closed. Reviewed by a separate agent; its findings applied (α/β
  symbols in #3, Tang tolerances and Table 5.4, Ge melting cases and quotes, blind screen for #1/#2).
