# A physically chosen length for the contact edge (note, 2026-11-20)

Status: **note, not a hunch, not counted.** Written from a chat with Peter on 2026-11-20, while CS-22b runs on
WSL A. Labels: variant of nonlocal and strain-gradient plasticity; never "novel".

**Corrected 2026-11-20 (Peter): one fixed ℓ; no nm resolution.** The evolving ℓ and the "two-zone reading" of an
earlier version are set aside (§4, §4b).

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
- Here: a material length says below which scale JC is invalid; the JC solution is smeared at that scale, and the
  interface/bond law at the contact covers what lies below. This is **one model**: smeared JC plus the bond law we
  already have. The "inner zone" is only what the bond law stands in for, not a separate region in the simulation.

## 3. Candidate physical lengths

| Length | Source | Measurable? | Size (order) | Status |
|---|---|---|---|---|
| Feedstock grain size (JC validity limit) | EBSD on sectioned powder | yes, per powder | µm (not yet sourced for our powders) | open |
| Strain-gradient-plasticity length | indentation size effect (Nix–Gao), torsion (Fleck) | yes | µm for annealed metals (from memory; to check) | open; lead: Chakrabarty & Song 2020 |
| Thermal diffusion length | √(κt) | computed | ≈ 0.7 µm at 5 ns (Al) | too small (CS-13c) |
| Ge 2026 characteristic length | calibrated to morphology | no (fitted) | 4 µm = 0.4 d (Cu, 10 µm) | not physical (ge2026_reading.md §5) |

## 4. Peter's evolving ℓ (considered, set aside 2026-11-20)

Etched sections of cold-sprayed particles show smaller grains near the bond zone. So ℓ could start at the feedstock
grain size and shrink with deformation, as a state variable:
- refined grain size against flow stress (Derby relation) or against the Zener–Hollomon parameter: known relations
  with fitted constants;
- grain-size profiles against distance from the interface are a **second data type**, independent of v_cr, which is
  the project's scarcest input (lead: Tang et al. 2024, strength gradient in impact-induced bonding).

Risk: if ℓ shrinks to sub-µm at the bond zone during the impact, the resolution problem returns exactly where it
matters. Whether most refinement happens before or after bonding is decided is the first question for the
literature.

Set aside because §4b shows the grains collapse to tens of nm in the band during the impact, while every quantity we
judge is measured at µm scale; following the grains would buy precision no measurement can confirm.

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

**Reading (corrected):**
- Feedstock grains are µm (Cu powder 5–10 µm), so a **fixed** ℓ ≈ feedstock grain size of 2 µm or more is
  physically defensible for the particle.
- The band's nm grains need not be resolved. The model's resolution should match the measurements': Tang's bond
  strengths come from about 5 µm micro-tensile slabs; v_cr and rebound are whole-particle quantities.
- One model: JC with a fixed ℓ, plus the interface law at the contact. The nm physics (DRX grains, oxide break-up)
  enters only through the law's parameters, calibrated on µm-scale data such as Tang's strength against radius
  (data/tang2024_reading.md).
- Risk: smearing at ℓ = 2 µm widens the real band (about 0.5 µm in Al per Liu) about fourfold. That may change the
  jet, the contact pressure and the surface exposure that feed the bond law. The ℓ-plateau test (§5) decides. Ge's
  ℓ = 4 µm still matched Cu morphology, but that ℓ was tuned to it.

## 5. The test that would decide it (ℓ-plateau)

The y+ analogue of scale separation: converged outputs (rebound, bonded area, v_cr) stay the same over a range of ℓ
around the physical value (for example 1.5–4 µm). If they keep changing with ℓ, the smeared physics matters and the
sub-scale law must carry it. Scale separation is weak here (ℓ of 2–4 µm against R = 10 µm). If the plateau fails,
revisit an evolving ℓ (§4).

## 6. Link to the wall-function analogy (HANDOFF item 6, 2026-11-18)

| Reason it failed | With a physical ℓ |
|---|---|
| The first layer is the badly represented one (§22) | the first layer is only as thin as ℓ, resolvable at R/16–R/32 |
| No outer input converges (§27) | testable: the ℓ-averaged edge state at fixed ℓ |
| No overlap layer at a separating edge | becomes the ℓ-plateau test |
| No calibration data for the inner law | Tang et al. 2024: bond strength against radius at µm scale (Bay-type law); its surface-exposure input still comes from the non-converging skin Y on TLSPH |

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

## 9. After §33 (2026-11-21): which assumptions changed

The softening check (softening-check-2026-11-20.md, frozen 66636c8) read **informative** on the engine's own quad
temperature (§33): S = 1 − T*ᵐ is 0.91–0.94 at 0.25 a and 0.5 a already at the first judged frame, and the edge
exceeds T_m (1.03–1.08 T_m) at the last.
- **Retracted:** "the early Y − 1 failure is not thermal" (stated in chat on 2026-11-21 from the §32 reconstruction,
  which left out compression and q heating). Softening is 6–9 % at the first output.
- **Now justified:** "softening acts in the §25 window", the first unjustified step of the softening-off test.
- **Newly unjustified:** "the softening in this deck is physical". Part of the early heat is bulk-viscosity work
  (numerical) and reversible Grüneisen compression heating (§2.1); §33 does not separate them. A softening-off test
  switches off both kinds.
- **Newly false late in the window:** "JC is valid at the edge". At T ≥ T_m LAW4 sets the strength to zero and there
  is no latent heat. This is a second reason, besides the grain scale (§2), why JC is out of range at the edge.
- **Held:** the §32 reconstruction was a lower bound on the heating.
- **Unchanged:** step 0 ("the edge fails to converge because of a missing length") is still unjustified; §33
  removes one obstacle to testing it, it is not evidence for it.

Open before a softening-off test is drafted (its own first unjustified steps):
- with softening off the deck may run longer, so the judged windows of the twins differ;
- part of what is switched off is numerical (q) heating;
- the melt cut-off (strength zero at T ≥ T_m) goes with it.
