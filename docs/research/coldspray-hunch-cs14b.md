# Cold spray: CS-14b, method amendment and clarification of CS-14 (registration, frozen)

Registered 2026-11-05 on Peter's instruction ("register a method amendment and clarification of CS-14"). **Status:
frozen** 2026-11-05. The hunch (statement, mechanism, prediction, kill criterion, consequence, mechanism split, open
items) stays as frozen in [coldspray-hunch-cs14.md](coldspray-hunch-cs14.md). This file changes the **method** and
**clarifies the scope**. The new rung protocol is frozen separately, before any run of the new method.

## 1. Clarification: CS-14 is a submodel

CS-14 is an **interface cell at nanometre scale**. It derives the interface law (fragment geometry t/w, threshold
stretch Y', extrusion pressure p_E as functions of oxide thickness) from the mechanics of the oxide alone, under
prescribed histories of surface stretch and pressure. It is **not** a simulation of the whole particle.

Peter's original intent was a **whole-particle model**: SPH for the particle and substrate, with the oxide as DEM.
That is not registered. The reason it needs CS-14 first is scale:
- the oxide is 5–25 nm thick, the particle about 15 µm across, a ratio of about 1000;
- resolving the oxide with nanometre grains over the surface of one particle (about 700 µm²) takes on the order
  of 10⁹ grains;
- at affordable SPH spacings (about 0.2 µm), a resolved shell would be 10–40 times too thick, and its properties
  would have to be scaled, which loses the thickness dependence (the same problem as the oxide-interphase option C
  of opencourant-verification.md §9.8).

So a whole-particle model can carry the oxide only as an **effective interface law**, and CS-14 is where that law
comes from. A whole-particle hunch can be registered later (as CS-15), with CS-14's law as its input.

## 2. Method change: continuum film with cohesive cracks instead of DEM

| | CS-14 as frozen | CS-14b |
|---|---|---|
| Oxide film | bonded DEM grains at nanometre scale | **2D plane-strain continuum**, linear elastic (small strain), meshed with quadrilateral elements |
| Fracture | brittle grain bonds | **cohesive zones** on candidate crack planes (every vertical element boundary in the film), linear-softening traction–separation law with strength σ_c and fracture energy G_c |
| Oxide–metal interface | tie to the substrate | unchanged in the first rung (elastic–perfectly plastic in shear, yield stress τ_i, no delamination); a cohesive delamination law is added in a later rung, registered first |
| Substrate | prescribed stretch | unchanged in the first rung; a resolved plastic metal substrate (for p_E) in a later rung, registered first |

**Why** (from the DEM rung, coldspray-cs14-rung.md):
- **No invented bond law.** The cohesive parameters σ_c and G_c are continuum properties of the oxide. They are
  still unknown (open item), but they are the quantities a measurement or an atomistic calculation would provide,
  not grain-level stand-ins.
- **No lattice artefacts.** The square lattice bridged its own cracks; the triangular lattice prefers 60° cracks
  and arrested at the grips. A continuum film has no preferred lattice directions. The restriction of cracks to
  vertical element boundaries is a stated limit, appropriate for the through-thickness opening cracks of
  fragmentation.
- **Exact verification.** Shear-lag theory applies to a continuum film directly.

## 3. Length scales (replaces the DEM grain size in CS-14's length_scales field)

The cell contains, besides t and w:
- **the cohesive length ℓ_cz = E G_c / σ_c²,** the film's own physical length. This replaces the DEM grain size as
  the "second length" CS-14 requires (review note 1);
- **the mesh size h,** numerical only: results must converge as h is refined, at least three elements across the
  cohesive process zone and at least four through the thickness;
- unchanged: the cohesive length of the oxide–metal interface (later rung), the plastic length of the metal (later
  rung), and the cell width.

**Consequence for the prediction:** t/w can depend on thickness only through t/ℓ_cz (and the other lengths). That is
now a physical statement, with ℓ_cz as the number to source.

## 4. What happens to the DEM work

- `src/schemeforge/research/blanket_dem.py`, its tests, the DEM rung protocol with amendment 1, its R0 results and
  figures stay in the repository as a record. They are not developed further.
- R1 of the DEM rung is not run. The amendment-2 question raised by the DEM R0 is closed by this change.

## 5. Not registered here (noted for later)

- **Molecular dynamics** is the method for the open oxide properties: whether a thin amorphous oxide is brittle or
  ductile, and σ_c and G_c at about 10⁹/s. It needs reactive interatomic potentials and a GPU cluster; it is not
  available locally.
- **CS-15, the whole-particle model** (section 1).
