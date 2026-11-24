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
- **Added after §34:** TLSPH particles heat and soften too, but without bulk-viscosity heating; the "numerical
  heating" caveat above applies to the quad deck, not to TLSPH (engine `27e53d5f0`).
- **Unchanged:** step 0 ("the edge fails to converge because of a missing length") is still unjustified; §33
  removes one obstacle to testing it, it is not evidence for it.

Open before a softening-off test is drafted (its own first unjustified steps):
- with softening off the deck may run longer, so the judged windows of the twins differ;
- part of what is switched off is numerical (q) heating;
- the melt cut-off (strength zero at T ≥ T_m) goes with it.

## 10. 2026-11-23: focus moves here (Peter); first step is solver reading

After CS-23 was refuted (§39), Peter moved the focus to the physical length scale and paused Track B (DECISIONS
2026-11-23).

**Found in an old copy of the fork** (`main` `e9432e6e`; to be confirmed on `cs12` by WSL A task 2026-11-23-c):
- The OpenRadioss base has `/NONLOCAL/MAT`, with an internal length LENGTH or a target element size LE_MAX.
- It is solved only in 3D solid and shell routines.
- It touches LAW2 (Johnson–Cook) among about 20 laws, but not LAW4 (our JC + Grüneisen card).
- In the base code it appears to serve damage regularisation, so it may not smooth the thermal softening that
  localises the edge.
- If so, it gives no zero-code ℓ test on our hosts: 2D quads for the §25 deck, TLSPH for the §30 deck.

**First step (Peter's choice):** WSL A reads the source:
- what `/NONLOCAL/MAT` regularises;
- whether it feeds σ_y and T;
- what a Ge-type nonlocal ε_p and T would cost on quads and on TLSPH.

The literature steps of §8 wait: the grain sizes in the originals, an Al feedstock grain size, and Chakrabarty &
Song 2020 (Peter's download).

**Still unjustified:** step 0 ("the edge fails to converge because of a missing length"). A test of it at fixed ℓ needs
a host that carries ℓ; the reading decides whether one exists without new code.

## 11. After §40 (2026-11-24): no host carries ℓ; which length is physical

**§40 (reading, `cs12` `38639859c`).**
- `/NONLOCAL/MAT` is a damage regulariser. For LAW2 and LAW4 the smoothed plastic strain reaches only `/FAIL` models,
  never σ_y or T.
- It is solved on 3D solids and shells only, and is silently ignored on quads, SPH and TLSPH.
- **There is no zero-code ℓ test.** A Ge-type model (ε̄_p standard, T̂ = 2T̄ − T, both in LAW4's σ_y; keys from the
  sidecar, no protected file touched) costs about 4–5 task sessions on 2D quads, and about 3 more on TLSPH.
- LAW2 is no shortcut: it has no melt branch and no length.

**New point: the band a gradient model produces is several ℓ wide.** In the 1D softening bar of §40,
w = 2ℓ√(m − 1)(π − arctan(1/√(m − 1))), so w = 1.5πℓ ≈ 4.7ℓ at m = 2 (re-derived in the cloud).
- The Ge form, with hardening in ε̄_p and thermal softening through T̂, has its own factor (§40 item 5, still to be
  worked out and source-checked), presumably of the same order. Only the bar above is closed.
- So "ℓ = grain size" (§4b) and "band width = grain size" are different models:

| Reading | ℓ for Al (feedstock grains ≈ 2 µm; Liu band ≈ 0.5 µm) | Band (≈ 4.7ℓ) | Mesh h ≤ ℓ/4 | Host |
|---|---|---|---|---|
| ℓ = grain size (JC validity limit, §2) | ≈ 2 µm | ≈ 9 µm, about the particle radius R = 10 µm | 0.5 µm (R/20) | quads or TLSPH |
| band width = grain size | ≈ 0.4 µm | ≈ 2 µm | 0.1 µm (R/100) | quads (§25 ran R/256); TLSPH cannot (R/32 has s = 0.31 µm) |
| band width = measured band (Liu, Al) | ≈ 0.1 µm | ≈ 0.5 µm | 0.025 µm (R/400) | beyond R/256 even on quads |

- Ge's ℓ = 4 µm on 10 µm Cu sits in the first row: its band is the size of the particle. That may be why morphology
  matched after calibration.
- The y+ reading of §2 ("JC is invalid below a representative volume of several grains") fits the second row better:
  the smeared band should be about one representative volume wide, not several.
- This is a modelling choice that has to be fixed before any hunch. It decides the host (quads) and the mesh the build
  must reach.

**Evidence on step 0 since §9:**
- Ge's nonlocal runs still show the peak edge strain rising 7–9 % from d/50 to d/100 (ge2026_reading.md §6). That is
  better than local (+25–56 %), but not converged by our 3.5 % rule.
- Ge also names a second, kinematic cause, present without thermal softening: interface elements cannot bend, so the
  deformation goes into the next element row (§3, Fig. 7).
- So a length is at most part of the cause. Step 0 stays unjustified, and the evidence leans "necessary, not
  sufficient".

**Chain now** (first unjustified step in bold):

| Step | Status |
|---|---|
| **0. The edge fails to converge because a length is missing** | **unjustified**; Ge: a length helps but leaves 7–9 % drift and a kinematic cause |
| 1. A physical length exists for the particle (grain size or band width) | second-hand numbers (§4b); which reading (table above) not chosen |
| 2. A host carries ℓ in σ_y and T | false today (§40); a build of about 4–5 sessions on quads |
| 3. At fixed ℓ the edge quantities converge under refinement | untested |
| 4. Outputs plateau over ℓ around the physical value (§5) | untested |

**Options for Peter** (no hunch drafted):
- (i) **Build on quads:** the §40 5(a) design note first, then module, 1D band check, neutrality. Then a frozen step-0
  test on the §25 deck: at fixed ℓ, do the edge quantities converge? This tests steps 2–3 directly, and step 0 with
  them.
- (ii) **Literature first:** choose the reading in the table above, and source the numbers:
  - Liu et al. band and grain sizes in the original;
  - an Al feedstock grain size;
  - Chakrabarty & Song 2020 (Peter's download);
  - a primary source for the band-width factor (Peerlings et al. 1996 or similar).
- (iii) **The softening-off test** (§9, on hold). It is zero-code but probes only the thermal half of step 0, and Ge
  Fig. 7 already shows edge drift without softening.

Modeller's recommendation: (ii) together with the design note of (i). The design note can be written for a general ℓ,
and the ℓ reading decides the mesh the build has to reach.

### 11a. Correction, 2026-11-24 (after Peter's questions; two statements of §11 were too strong)

**Host: no preference yet (withdraws "it points to quads as the host").**
- The quad argument was resolution only. It holds only under "band width = grain size" (ℓ ≈ 0.4 µm, h ≤ 0.1 µm).
- §11 left out three things about quads:
  - the mesh fails at the jet root: R/256 stops at about 0.8 ns ≈ 0.034 t_p (solver-facts §1, §25);
  - quads carry no bond law;
  - quads have no conduction.
- So quads can only be a **testbed for step 0**, not the host the model has to work on.
- TLSPH is that host: it runs to 2 D/V and carries cs12. Its limits:
  - under "ℓ = grain size" (2 µm), ℓ/s = 1.6, 3.2 and 6.4 at R/8, R/16 and R/32, so only two meshes resolve ℓ (R/64
    is out of reach);
  - §40's cheap TLSPH form smooths over reference neighbours. That is a material (convected) length, arguably right
    for a grain size, but a modelling choice;
  - TLSPH's documented non-convergence (skin Y, e(off)) has not been tied to shear localisation.
- The ℓ reading decides the host: grain size points to TLSPH, band width to a quad testbed.

**Ge: weak evidence for our hosts (withdraws "the evidence leans necessary, not sufficient").**
- Ge is finite elements. Its residual 7–9 % drift with the nonlocal model has two candidate causes: the formulation
  itself, or the element-kinematic effect Ge names (interface elements cannot bend). The second does not exist in
  SPH, which has errors of its own (surface kernel truncation, hourglass modes).
- The figure comes from colour-bar limits.
- What remains of it: in one FE code a length more than halved the drift but did not remove it.

**Objections, ranked:**
1. Step 0 is unproven on our own data. On quads the readings never separated localisation from jet-root mesh failure.
   On TLSPH the non-convergence is skin reconstruction and rebound drift, with causes not separated.
2. Scale separation is weak. The band is ≈ 4.7ℓ, so a large ℓ smears the jet and the pressure that feed the bond law,
   and a small ℓ brings back the resolution problem. The ℓ-plateau test decides this, but it can fail for structural
   reasons.
3. Cost: about 4–5 sessions (quads) or 7–8 (TLSPH) before step 0 can be tested.

**For continuing:**
- edge non-convergence has stopped every host;
- a bond law cannot converge on inputs that do not;
- a fixed-ℓ step-0 test is a clean, freezable yes/no.

**Cheaper first look at objection 1 (option, not yet a spec):**
- From existing §30 off-run files (R/8, R/16, R/32), measure the edge shear band's width in particle spacings, and
  check whether the drifting quantities sit in it.
- If the band is always 1–2 spacings and narrows with refinement, that is direct evidence for step 0 on TLSPH. If not,
  the path loses its premise.
- Before any spec: check against solver-facts that ε_p is in the written output.

