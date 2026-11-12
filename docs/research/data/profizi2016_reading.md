# Profizi, Combescure & Ogawa 2016 and Profizi's thesis: Total Lagrangian SPH with adhesion for cold spray

WSL A task 2026-11-12-a, item 1. Read on 2026-11-12 by the WSL A session. Evidence level **F** for the parts
listed under "What was read". Neither source is on the blind list.

## Sources

| | Paper | Thesis |
|---|---|---|
| Reference | P. Profizi, A. Combescure, K. Ogawa, "SPH modeling of adhesion in fast dynamics: Application to the Cold Spray process", C. R. Mécanique 344 (2016) 211–224, doi:10.1016/j.crme.2016.02.001 | P. Profizi, "Development of a numerical model of single particle impact with adhesion for simulation of the Cold Spray process", PhD thesis, INSA Lyon and Tohoku University, defended 2016-09-20, NNT 2016LYSEI088 |
| Fetched from | `comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2016.02.001.pdf` (open access, CC BY-NC-ND) | HAL, `theses.hal.science/tel-01715581/document`. The hosts `lamcos.insa-lyon.fr` and `theses.insa-lyon.fr` timed out from WSL |
| sha256 | `e406f809c9b7b8f6dd6a5872e29a1661d0f4f3e7d8122739faad50a5387e821d` | `fd85968b2bfcd17e16cc442bf68cbd3c51dca35e46a2acb8259cc22504261125` |
| Local copy | `~/oc_runs/lit/dl/profizi2016/profizi2016_crme.pdf` | `~/oc_runs/lit/dl/profizi2016/thesis.pdf` (177 PDF pages) |

**What was read.**
- Paper: all 14 pages.
- Thesis: §1.3 (numerical concepts), §1.4.3–1.5, ch. 2 (the model), §3.1–3.2, §3.4–3.6, §4.6, ch. 5, ch. 6, and
  appendix A (input file, pp. 145–148: an SPH particle of 1 mm on an FE substrate).
- **Not read:** thesis §1.1–1.2, §3.3 (shear-band tests; only the run times on p. 61 and the erosion remark on
  p. 62), §4.1–4.5 (experiments), appendix B.
- **Text only.** Both were read as extracted text. No figure was viewed, so values that exist only in a plot
  are missing here (in particular thesis Fig. 3.36, the mesh-convergence plot of the impact).

Page numbers: "p. 213" style = journal pages; "T p. 31" = printed thesis page.

**The paper is the smaller source.** Its §2.5.1 and §3–4.5 are reproduced nearly word for word in the thesis
(§1.4.4, §3.5.1–3.5.2); its §2.5.2–2.5.4 (the multiplier form of the adhesion) are in the paper only. The thesis adds the SPH settings, the activation and erosion criteria, the validation
runs and the limits.

## 1. SPH formulation

| Item | What the sources say | Where |
|---|---|---|
| Code | Europlexus ("a research FEM-SPH fast dynamic code"; named in the thesis only). Time integration: explicit Newmark, β = 0, γ = 0.5 (the paper prints α = 0.5) | T p. 19, p. 28; paper p. 212 |
| Formulation | **Total Lagrangian**, "to avoid tensile instability, with a search for neighbors only at the initial step" | T p. 31 |
| Kernel | Cubic spline (M4), with C = 1/(πh³) in 3D, support radius 2h | paper eq. (6), p. 213; T eq. (1.12), p. 21 |
| h and support | The "kernel radius" is twice the SPH particle radius R_SPH, and its influence extends to twice that. So h = 2 R_SPH = one particle spacing, support radius = 4 R_SPH = two spacings | T p. 44, p. 46 |
| Neighbour number | Limited to 50. Found by counting the nodes inside a sphere of 4 R_SPH in the lattice (average 50). The first Hopkinson run used a limit of 100 | T p. 31, p. 44, p. 48 |
| Lattice | Hexagonal close-packed. One R_SPH for all particles, fixed in time ("due to current software limitations") | T p. 31 |
| Gradient correction | "a normalization matrix from [BEL 00] is used to get first-order completeness". [BEL 00] = Belytschko, Guo, Liu & Xiao, IJNME 48 (2000) 1359–1400. **The equations are not printed** in either source; the reader is sent to Maurel, Combescure & Potapov 2006 and Liu & Liu 2010 | T p. 31; paper p. 213 |
| Hourglass / zero-energy control | **None.** Stress points are named as the known remedy and deliberately not used: "we chose the initial normalized 3D formulation (without stress points). This choice is justified by the existence of very large plastic strains which occur in the simulations, which dissipate enough energy to prevent hourglass modes from developing" | paper p. 213; T p. 22 |
| Artificial viscosity | Monaghan type ("basic artificial viscosity described in [MON 09]"), linear coefficient 0.8, quadratic coefficient 4 | T p. 31; appendix A p. 146 (`LINE 0.8 QUAD 4 … VOISIN 50`) |
| Other stabilisers | None mentioned (no artificial stress, no velocity smoothing) | – |
| Time step | Δt_max = 0.3 C_stab · 2 R_SPH / √(v + c²) as printed (probably v² + c²), C_stab = 0.5 in the text. The author notes that 0.05 "was found to be necessary for the material algorithm to get more than one step in the elastic regime". **The printed input file sets `CSTAB 0.05`.** The paper's runs use a fixed maximum step of 7·10⁻¹² s at R_SPH = 1.25 µm | T p. 31; appendix A p. 147; paper p. 217, p. 221 |
| Boundary conditions | Imposed on three particle layers | T p. 31, p. 49 |
| Absorbing boundary | A damping force on each boundary particle, opposite to its velocity, on the three outer layers of the substrate (all sides but the impacted one). Paper eq. (22) and thesis eq. (3.9): F = −V √(ρE) S_SPH. Thesis eq. (2.1): f = −√(ρ/E) π R_SPH² v·n. **The prints differ;** √(ρE) is the one with the units of an impedance. The author calls the area the weak point (voids in the lattice) | paper eq. (22), p. 220; T eq. (2.1), p. 31; T eq. (3.9), p. 81 |
| Material | Johnson–Cook with adiabatic heating (90 % of plastic work), radial return; a bisection solver replaced the code's own when thermal softening was on. Damage (shear criterion for Al, Johnson–Cook failure for Cu) softens yield stress and modulus; maximum damage 0.9 | T pp. 32–34 |

**My check of the time step** (not in the sources): with 2 R_SPH = 2.5 µm and c ≈ 5.1 km/s for aluminium, the
formula gives 7·10⁻¹¹ s at C_stab = 0.5. The 7·10⁻¹² s of the paper's runs therefore corresponds to C_stab = 0.05,
the value in the printed input file.

## 2. Reference update

**There is none.** Neighbours are searched once, at the initial step, and the correction matrix belongs to that
reference. No update rule, no trigger, no mixed scheme.

The thesis reports what follows from this:
- **No particle deletion.** "since the SPH algorithm is total Lagrangian, deleting elements proved to make the
  normalization matrix computation unstable." Erosion is therefore applied to finite elements only (T p. 33,
  p. 38).
  The shear-band tests with SPH erosion say the same: "a lot of numerical instabilities appeared because of
  the change in SPH neighborhood, especially for the normalizing matrix B" (T p. 62). There the erosion was done by cancelling a particle's
  interaction with its neighbours, not by deleting the node (T p. 61).
- **Fine meshes do not finish at high speed.** In the convergence study without adhesion (SPH particle on an FE
  substrate, R_SPH 1.25 / 1.00 / 0.75 / 0.5 µm), the results of the finer meshes exist only up to 900, 800 and
  600 m/s. The cause given is "the sudden drop in stable time increment due to the intense localization of SPH
  particles, 'fleeing' the contact zone" (T p. 70). I read the three speeds as belonging to the three finer
  meshes in order; the text does not say so explicitly. The text calls this case an Al particle on a Cu FE
  substrate (T p. 69); the captions of Figs. 3.37 and 3.38 say a Cu particle on an Al substrate.
- **The author's conclusion:** the impact model was "found to lack consistency and stability at very high impact
  speeds mostly due to the total Lagrangian nature of the solid SPH method used. A switch to Updated Lagrangian is
  to be considered" (T p. 87). The thesis cites Vidal, Bonet & Huerta 2007 for the updated
  Lagrangian and the corrected total Lagrangian forms, in the context of fluids (T p. 22). The attribution to the
  total Lagrangian form is hedged elsewhere ("possibly due to", T p. 38).

## 3. Body-to-body contact

- **SPH on SPH: the pinball method** (Belytschko & Neal 1991). Each SPH node carries a sphere of radius R_SPH.
  Contact is detected when two spheres of different bodies interpenetrate. The contact normal is the line between
  the two centres (T p. 22, p. 23, p. 35; paper p. 214).
- **Force: Lagrange multipliers, no penalty.** The multipliers solve H λ = w with H = C M⁻¹ Cᵀ, each step. For
  unilateral contact the velocities at n + 3/2 are used, because the end-of-step form "leads to highly oscillating
  responses". A separate test detects rebound within a step (T pp. 23–24). The stated reason against penalty: the
  stiffness is a parameter and "some energy is consumed during the contact" (T p. 23, p. 28).
- **SPH on FE:** sliding surfaces, SPH nodes as slaves and element faces as masters, also with Lagrange multipliers.
  This is used whenever the harder body can be meshed with finite elements (T pp. 22–23, p. 31, p. 35).
- **Frictionless.** Friction "is now inexistent and could have a considerable influence" (T p. 35).
- **Not stated:** whether the kernel sums can connect particles of two SPH bodies that start close together. The
  printed input file is an SPH-on-FE case and does not show it.
- **Not shown:** any test of the contact against a reference (flat-on-flat wave, Hertz).

## 4. Adhesion law

It is a pair law between two pinballs, not a surface law (paper §2.5, pp. 214–215; T §2.2, pp. 35–38).

1. **Tie.** Once two points have been in contact and start to separate, the same Lagrange multiplier Λ that
   prevents penetration now prevents opening. Its magnitude is not bounded. The authors call this the Griffith
   variant and compare it to a "Dirac model of the JKR type" (both statements in the paper only, p. 215).
2. **Energy limit.** The work of the multiplier during opening is summed, ΔW = ½ (Λₙ + Λₙ₊₁) Δgap. The pair
   breaks when W reaches G_c · S_adh.
3. **Optional stress limit.** A maximum cohesive stress σ_c = Λ / S_adh gives a plateau (Dugdale–Barenblatt), with
   G_c = σ_c · gap_c.
4. **Adhesive area of a pair.** Paper: S_adh = (π/2)(R₁² + R₂²). Thesis: π R² with R the mean pinball radius. Both
   are the same for equal radii. The thesis calls this "for now mesh dependent", and the paper says it is
   "difficult to estimate accurately if the interfaces are highly distorted". On the same page the thesis calls the
   energy criterion "less mesh dependent and hence more robust" than a stress criterion (T p. 35).
5. **Activation criterion (thesis only).** Without it, every contact pair adheres as soon as it touches. With it,
   a pair adheres only after the local yield stress of the contacting elements has dropped by a set percentage
   from its maximum (30 % in the runs). This stands for a shear instability. The author's own judgement: "this
   criterion should be viewed with skepticism and should be improved or even changed" (T p. 134).
6. **Erosion criterion (thesis only).** A pair is broken when the damage of one of its two elements reaches
   D_adh,max (0.5 in the runs).

Values used: G_c = 0.02 J/m² in the elastic cases and 0.002–0.05 J/m² in the paper's table; σ_c 100–1600 MPa
(elastic) and 100–500 MPa (plastic), which gives a largest opening of 0.2 nm; G_c = 30 J/m² with no σ_c in thesis
§3.5.3. G_c is treated as unknown and chosen to reproduce a sticking window.

## 5. Verification shown, with numbers

| Test | Reference | Result | Where |
|---|---|---|---|
| Two rigid masses with a cohesive force, second mass on a spring (not an SPH run) | closed form / numerical root | M = 1, m = 2, V₀ = −1, G_c = 0.2: separation velocity 0.0898 for every F_c when k = 0; with k = 0.5 it is 0.000 / 0.086 / 0.091 for F_c = 0.05 / 0.5 / 5 | paper Table 1; T Table 3.5 |
| Elastic SPH cylinder (R 12.5 µm, height 16.67 µm) on a built-in cylinder (R 25 µm), 20 m/s, 618 + 2526 particles, R_SPH 1.25 µm, same case scaled ×10 and ×100 | none (size effect shown qualitatively) | without adhesion: rebound 12 m/s at every size. With G_c = 0.02 J/m²: the two smaller sizes stick (5.5 % and 55 % of the adhesion energy used after 20 000 steps), the largest rebounds at 1.64 m/s | paper pp. 217–218; T pp. 75–76 |
| Elastic SPH sphere (R 12.5 µm, 737 particles) on an SPH block (15 776 particles), 20 m/s, σ_c varied | none | rebound falls with σ_c to a plateau at 30 % of the impact velocity; lower with absorbing boundaries | paper pp. 219–220 |
| Hopkinson bar, SPH specimen (5 mm, R_SPH 125 µm, 8880 particles) | FE run of the same case | "only a few percents in maximum load difference", SPH "a little softer"; overall "less than 10 %" | T pp. 44–48 |
| Traction test, Al cylinder 40 × 120 mm, 200 s⁻¹ (p. 50 says 250 s⁻¹) | FE (Europlexus; itself within 1–2 % of Abaqus, compared at 20 s⁻¹) | SPH maximum force **below** FE by 11 %, 8 %, 5 % and 3.6 % at R_SPH = 2, 1.5, 1 and 0.5 mm (3009, 7314, 25 593, 207 288 particles) | T pp. 49–50 |
| Impact without adhesion, SPH particle (R 12.5 µm) on FE substrate, R_SPH 1.25 → 0.5 µm, 100–1000 m/s | itself (mesh convergence) | numbers only in Fig. 3.36 (not read). Text: "very consistent" in deformation, and in rebound speed below 700 m/s; finer meshes fail above 600–900 m/s | T pp. 69–70 |
| 1 mm Cu on Cu (SPITS experiment), SPH particle on FE substrate, R_SPH 30 µm | one cross-section each | 230 m/s: height −23.5 % (experiment −30 %), penetration 15.2 % (7.5 %), diameter +16 % (+10 %). 457 m/s (R_SPH 40 µm "due to stability issues"): height −31.5 % (about −40 %), penetration 33.5 % (about 36 %), diameter +38 % (+20 %). Yield stress fitted to the measured hardness | T pp. 125–129 |
| Al on Al, both SPH, 100–1000 m/s, G_c varied, no criteria | experimental sticking window "typically 400 to 700 m/s" | G_c = 0.02: share of particle nodes still stuck 0 % up to 300 m/s, 12 % / 6 % / 24 % at 400 / 500 / 600, 0 % at 700, 9 % / 22 % / 31 % at 800 / 900 / 1000. Sticking is declared above 1 % ("completely arbitrary"). Maximum plastic strain about 1.5 in the window, above 5 at the highest speeds | paper Table 3, pp. 221–222 |
| Same with G_c = 30 J/m², activation at 30 % yield drop, erosion at D = 0.5 | – | activation gives a lower limit of 500 m/s; erosion gives an upper limit near 1700 m/s | T pp. 85–86 |

**What is not there.** No test against an exact reference for the SPH bodies or the contact: no wave in a bar, no
Hertz contact, no tension wave, no zero-energy test, no convergence order. Every SPH check is a comparison with
finite elements or with one experiment, at the 4–11 % level. None of the rungs of our ladders has a counterpart.

## 6. Resolution and cost

- **Cold-spray runs:** particle radius 12.5 µm with R_SPH = 1.25 µm. The particle spacing is 2 R_SPH = 2.5 µm,
  that is **R/5** in our notation, 737 particles in the sphere. The SPH substrate (75 × 75 × 33.4 µm) has 15 776
  particles. The thesis calls this "a very coarse mesh … for quick computations" (T p. 85), the paper "relatively
  coarse" (p. 222).
- **Finest impact mesh:** R_SPH = 0.5 µm (R/12.5), 11 534 particles in the sphere, with an FE substrate of
  72 000 elements (T p. 69).
- **Simulated time:** 0.35 µs (paper p. 222), 0.2 µs and 0.177 µs (T p. 69, p. 85). The paper also says the runs
  "always stopped after … typically 5000 time steps" (also T p. 82); at 7·10⁻¹² s that is 0.035 µs, which does not
  match 0.35 µs. 50 000 steps would match. Not resolved.
- **Cost:** no figure for the impact runs. The only run times are for the shear-band cylinder: 3676 particles
  0.9 h, 29 357 particles 30.5 h (T p. 61; machine and step count not stated). FE is called "a lot lower" in cost
  than SPH, which is why the substrate is FE whenever possible (T p. 31).

## 7. Stated limits

1. **Total Lagrangian at high speed:** instability and loss of consistency, time-step collapse on finer meshes,
   no particle deletion; "a switch to Updated Lagrangian is to be considered" (§2 above).
2. **No hourglass control;** relies on plastic dissipation (§1).
3. **Adhesive area** is mesh dependent and wrong at large interface distortion (paper p. 215, p. 224).
4. **Unphysical second sticking range** above about 900 m/s without the erosion criterion (paper p. 222, p. 224).
5. **The sticking decision is arbitrary:** 1 % of nodes in the paper, one remaining pair in the thesis; "the
   notion of a minimal final adhesive surface … should later be investigated" (T p. 87; pp. 132–133).
6. **The activation criterion is not validated** (T p. 134); the damage parameters are "maybe the most sensitive
   ones" (T p. 135).
7. **No friction** (T p. 35).
8. **Localisation is mesh dependent,** and full convergence is not claimed: "The goal is not anyway to get a
   complete clear convergence" (T p. 70).
9. **SPH is softer than FE** at equal spacing; about half the spacing is needed for 5 % (T p. 50).
10. **Substrate penetration** against the experiment is "not considered satisfactory" (T p. 127).

## 8. What this means for CS-18 and the TLSPH ladder (my reading, not in the sources)

1. **The pairing is theirs.** TLSPH with a first-order correction, a separate pair contact between bodies, and an
   energy-limited cohesive pair law with an activation criterion: all four are in the thesis. "Variant of Profizi
   et al. 2016" is the right expectation for the referee's label. What differs in CS-18: hourglass control, a
   penalty contact with surface normals in place of pinballs with multipliers, a different activation law, and
   judging against exact references.
2. **Their set-up, for comparison with SPEC-TL:** cubic spline, h = one spacing (support two spacings, about 50
   neighbours on a close-packed lattice), correction matrix of Belytschko et al. 2000, Monaghan viscosity
   0.8 / 4, no hourglass control, no reference update.
3. **The main risk of CS-18 is confirmed from experience.** Without a reference update their finer meshes fail at
   high speed (600 m/s at R/12.5), while the coarse R/5 runs finish up to 1900 m/s (T p. 85). The thesis attributes
   this "mostly" to the total Lagrangian form. Our E-1 conditions (R/16 and finer, up to 800 m/s
   and above) lie beyond what their formulation finished at comparable resolution. Rung T-large-strain is therefore the decisive one, and
   it should be run at more than one resolution.
4. **Their evidence says nothing about the surface layer.** No rung-like test exists, and R/5 is far coarser than
   any of our rungs. The claim of CS-18 (accurate surface layer at the ladder's thresholds) is not anticipated by
   their results in either direction.
5. **Their case for no hourglass control is plastic dissipation.** Their elastic runs (cylinder and sphere at
   20 m/s) also ran without it, but were not compared with a reference. Our core rungs are elastic (T-S0, T-S1,
   T-B2, T-tension), where their justification does not apply.
6. **Particle deletion** destabilised their correction matrix. In the fork, failure (`KXSP(2) = 0`) removes a
   particle from the sums; SPEC-TL has to say what happens to the reference sums of its neighbours.
7. **"Pontabry et al. 2016"** (our external literature report) is not cited in either source. Whether it is the
   same group stays unverified.
