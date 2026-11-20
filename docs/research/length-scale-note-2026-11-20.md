# A physically chosen length for the contact edge (note, 2026-11-20)

Status: **note, not a hunch, not counted.** Written from a chat with Peter on 2026-11-20, while CS-22b runs on
WSL A. Labels: variant of nonlocal and strain-gradient plasticity; never "novel".

## 1. The problem in one paragraph

Johnson–Cook plus an EOS has no length. At the contact edge thermal softening localises the shear into the thinnest
band the discretisation allows, so the mesh sets the band width; local edge quantities (Y − 1, edge strain) rise with
refinement (§25), while integrals (a(t), energy) converge. Heat conduction gives a physical length (√(κt) ≈ 0.7 µm at
5 ns, CS-13), but it is 1–3 spacings even at R/48 (CS-13c refuted). A resolvable length that is chosen freely just
moves the dependence from the mesh to ℓ.

## 2. Peter's reframing: "y+ the other way round"

JC is fitted to polycrystal specimens; it describes averages over a representative volume of several grains and has
no meaning below it. Resolving the edge below that scale asks the model a question outside its validity. So ℓ need
not be a regularisation knob: it can be the model's own validity limit, made explicit.
- Wall function: y+ = y u_τ/ν says where the universal inner law holds; the first cell sits outside it and the law
  covers the inside.
- Here: a material length says below which scale JC is invalid; the solution is smeared at that scale, and a sub-scale
  law (the interface/bond law) covers what lies below.

## 3. Candidate physical lengths

| Length | Source | Measurable? | Size (order) | Status |
|---|---|---|---|---|
| Feedstock grain size (JC validity limit) | EBSD on sectioned powder | yes, per powder | µm (not yet sourced for our powders) | open |
| Strain-gradient-plasticity length | indentation size effect (Nix–Gao), torsion (Fleck) | yes | µm for annealed metals (from memory; to check) | open; lead: Chakrabarty & Song 2020 |
| Thermal diffusion length | √(κt) | computed | ≈ 0.7 µm at 5 ns (Al) | too small (CS-13c) |
| Ge 2026 characteristic length | calibrated to morphology | no (fitted) | 4 µm = 0.4 d (Cu, 10 µm) | not physical (ge2026_reading.md §5) |

## 4. Peter's evolving ℓ

Etched sections of cold-sprayed particles show smaller grains near the bond zone. So ℓ could start at the feedstock
grain size and shrink with deformation, as a state variable:
- refined grain size against flow stress (Derby relation) or against the Zener–Hollomon parameter: known relations
  with fitted constants;
- grain-size profiles against distance from the interface are a **second data type**, independent of v_cr, which is
  the project's scarcest input (lead: Tang et al. 2024, strength gradient in impact-induced bonding).

Risk: if ℓ shrinks to sub-µm at the bond zone during the impact, the resolution problem returns exactly where it
matters. Whether most refinement happens before or after bonding is decided is the first question for the
literature.

## 4b. Grain-size evidence (added later on 2026-11-20)

Source: an AI literature summary Peter pasted in chat (not checked against the primary papers; every number below is
second-hand until read in the original):
- Panova & Schuh (Cu on Cu, LIPIT, 17–21 µm, 552–875 m/s; released by Peter 2026-11-08): powder grains about
  5–10 µm, substrate 15–20 µm; metadynamic recrystallisation (mDRX) grains of 1.3–3.0 µm at the interface,
  formed right after the impact by residual heat; sub-100 nm DRX bands from peak shear cited, not resolved.
- Liu et al. 2019/2020 (Scripta Mater., pure Al, two bonded particles, TEM): nanograins 10–30 nm at the
  particle–particle interface (about 30 % below 10 nm), a continuous gradient to about 500 nm toward the centre.
- Zou et al. 2009 (Ni, EBSD): 100–200 nm grains at the bond interface, elongated parent grains in the core.
- Tiamiyu et al. 2022 (Nature Mater.; a blind-list-2 candidate): starting grain sizes 0.24, 3, 13 and 34 µm in a
  DRX study. Only grain sizes were seen, no v_cr; not on the frozen list, so no B4 entry.

**Reading:**
- The starting grain size is in the range Peter wants (Cu powder 5–10 µm), so an initial ℓ of 2 µm or more is
  physically defensible for the bulk of the particle.
- In the shear band the grains fall to tens of nm **during** the impact (DRX), not only afterwards. An evolving ℓ
  that follows the grains would therefore collapse to tens of nm exactly at the bond zone, far below any reachable
  resolution.
- That suggests a two-zone reading instead of one evolving ℓ: JC with ℓ ≈ feedstock grain size outside the band,
  and the band itself (nanocrystalline, a different material) treated as a sub-scale zone covered by the interface
  law. That is the wall-function structure (§2), with the band as the "viscous sublayer". The band thickness, from
  the grain gradient (about 0.5 µm in Al per Liu), would set where the outer model stops.
- Tang et al. 2024 (data/tang2024_reading.md) measured bond strength against radius with a Bay-type law: a
  candidate inner law **and** calibration data for it.

## 5. The test that would decide it (ℓ-plateau)

The y+ analogue of scale separation: converged outputs (rebound, bonded area, v_cr) stay the same over a range of ℓ
around the physical value (for example 1.5–4 µm). If they keep changing with ℓ, the smeared physics matters and the
sub-scale law must carry it. Scale separation is weak here (ℓ of 2–4 µm against R = 10 µm).

## 6. Link to the wall-function analogy (HANDOFF item 6, 2026-11-18)

| Reason it failed | With a physical ℓ |
|---|---|
| The first layer is the badly represented one (§22) | the first layer is only as thin as ℓ, resolvable at R/16–R/32 |
| No outer input converges (§27) | testable: the ℓ-averaged edge state at fixed ℓ |
| No overlap layer at a separating edge | becomes the ℓ-plateau test |
| No calibration data for the inner law | still open (v_cr only; grain-size profiles may help) |

## 7. What Ge 2026 adds (ge2026_reading.md)

- For: a nonlocal ε_p, ε̇_p plus over-nonlocal T with ℓ = 4 µm makes particle shape and jetting nearly mesh-
  independent on Cu at no extra cost.
- Against: ℓ is fitted to morphology, no ℓ-sensitivity is shown, and the peak edge strain still rises 7–9 % from
  d/50 to d/100 (fig.). No interface quantities.

## 8. Next, if Peter wants to pursue it (after CS-22b)

1. Chakrabarty & Song 2020 (strain-gradient JC for cold spray): no open copy; Peter downloads it. Tang et al.
   2024: read (main text; SI not read). Check the grain-size numbers of §4b in Panova & Schuh and Liu et al.
2. Find a measured grain size or gradient length for an Al powder like P-HG-Al.
3. Only then: draft a hunch built on the ℓ-plateau test (budget 4 of 5).
