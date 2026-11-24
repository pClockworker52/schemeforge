# Band check: is the TLSPH edge strain localised at the mesh scale? (spec and prediction, DRAFT — not frozen)

Drafted 2026-11-24 (cloud, modeller) at Peter's request (chat 2026-11-24; length-scale-note-2026-11-20.md §11a,
"cheaper first look"). `kind = check`; no hunch, no budget. Existing files only: **no run, no build.**

**Revised 2026-11-24 before the freeze** (Peter: "Is the spec fair?"; the first draft is 4ce738c):
- The judged rebound-energy test is now reported only. It was too easy to pass: zone plastic work grows with
  refinement anyway, T_lb inflates it on fine meshes, and competing sinks were left out.
- The width outcomes are relabelled to what the data can show, with the detection limit stated.
- The width is background-subtracted (half-maximum alone favoured "fails").
- The qualifying threshold is lowered, and a second ratio q′ is added.
- Bonded (CS-23) runs are reported.
- The prediction is revised.

## Why

Step 0 of the length-scale chain says that the edge fails to converge because no length is present. It is unproven
on our own data (note §11a, objection 1). A necessary condition for it can be checked on existing TLSPH files: **the
edge plastic strain is localised in a band whose width follows the mesh.**
- Johnson–Cook with an EOS, rate factor C = 0.001 and no conduction has nothing that sets a band width. So if the edge
  localises, a mesh-scale band is almost expected, and this check is mainly a cheap way to **rule step 0 out**.
- If the edge strain instead has a width that is resolved and the same in µm on every mesh, the non-convergence is not
  mesh-scale localisation. A material length would then change little, and the length path loses its premise on
  TLSPH.

**What this check cannot show:**
- **Physical widths below about 2 spacings at R/32 (≈ 0.6 µm) are not detectable.** Liu's measured Al band (≈ 0.5 µm)
  lies below that, so "localised at the mesh scale" means only "no width ≥ ≈ 0.6 µm".
- **That the band causes the rebound drift.** The e(off) values are 0.0936 / 0.0649 / 0.0571 at R/8 / R/16 / R/32,
  a rebound-energy change ΔKE ≈ 2.8 nJ, or 0.55 % of KE₀ = 509 nJ per quarter model. Energy totals cannot attribute
  that to one region. A sink table is reported so that Peter can see which terms drift. A known competing cause is
  the contact penalty stiffness k = stfac·B·s, which scales with the mesh (solver-facts §3).

## Facts checked (coldspray-procedure.md)

solver-facts §3:
- the §30 off runs and their e(off);
- TL particles heat and soften, the temperature is not written, and T_lb is the plastic-work lower bound (§34);
- no TL internal energy in the engine output: energies come from the fork's `tl_diag.csv` (E_int, W_hg, W_visc, W_d,
  E_c, KE);
- the face-layer deficit of TLSPH;
- frictionless contact on the off branch.

§34 shows that ε_p is written per particle per frame in AL08off and AL16off (animations EPSP, P, VEL; about 50 frames
to 2.83 t_p, t_p = 0.707 D/V). solver-facts §4: the CS-23 runs (engine `38639859c`) use the CS-22b decks with the same
animation requests.

**Not covered — never read/used before; check the output first:**
- (i) ε_p and positions in the AL32off frames;
- (ii) particle identity across frames at R/32;
- (iii) the reference (frame-0) positions as the depth coordinate;
- (iv) frames with ε_p in the CS-23 30× runs;
- (v) per-particle volume (lattice s³ or written; needed for the reported zone work only).

## Q1: files (reading only)

1. For AL08off, AL16off, AL32off (engine `27e53d5f0`): are ε_p and positions written per particle in every frame, with
   stable particle ids? If not, for any mesh: stop and report "not determinable from existing files". A rerun is
   decided later, not here.
2. The frame times, and the frame nearest t = t_p.
3. For the CS-23 30× runs (R/8, R/16, R/32): the same question. If they have no usable frames, their reported item is
   dropped, and nothing else changes.
4. Per-particle volume: written, or the lattice value s³.

## Q2: data (existing files only)

**Coordinates.** Reference positions are frame 0. Depth d is measured in the reference configuration, normal to the
body's reference contact surface:
- particle: d = R − |X − X_c|;
- substrate: d = distance below the original top surface.

Widths are given in µm and in units of the mesh's own spacing s (1.25 / 0.625 / 0.3125 µm).

**Stations** (six, fixed now). Each is a line along the reference inward normal, in the meridian plane at azimuth
45°, away from both symmetry planes:
- particle: polar angle θ₀ = 30°, 50°, 70° from the impact pole;
- substrate: reference radius r₀ = 0.25 R, 0.50 R, 0.75 R.

A particle belongs to a station if its reference position lies within 0.75 s of the line.

**Profile and width at the judged frame** (the frame nearest t = t_p), per station and mesh:
- ε_p(d) ordered by d;
- **ε_bg** = the median ε_p of the station's particles at 3 µm ≤ d ≤ 5 µm (a fixed physical depth, resolved on every
  mesh);
- **ε_peak** = the maximum of ε_p;
- **w_½** = the length of the set {d : ε_p(d) − ε_bg ≥ ½ (ε_peak − ε_bg)}, with linear interpolation between
  neighbouring particles. This covers a band at the surface and one inside the material.

**A station qualifies** if ε_peak − ε_bg ≥ 0.3 on all three meshes. Only qualifying stations are judged.

**Ratios** per qualifying station, in µm:
- q = w_½(R/8) / w_½(R/32): mesh-scale gives 4, resolved gives 1;
- q′ = w_½(R/16) / w_½(R/32): mesh-scale gives 2, resolved gives 1.

## Rule (fixed now)

Per qualifying station:
- **mesh-scale** if q ≥ 2.5 and q′ ≥ 1.6;
- **resolved** if q ≤ 1.5 and q′ ≤ 1.25;
- **unclear** otherwise.

Verdict (majority = more than half of the qualifying stations):
- **not determinable** if Q1 stops, or fewer than 2 stations qualify;
- **step 0 fails on TLSPH** if a majority is resolved;
- **necessary condition met** if a majority is mesh-scale;
- **intermediate** otherwise.

**Reported, not judged:**
- **Sink table** per mesh at t_end, from `tl_diag.csv` and the interface file:
  - KE of particle and substrate, E_int, W_hg, W_visc, W_d, E_c;
  - each term's change from R/8 to R/32, set against ΔKE.
- **Zone work:**
  - per particle W_i = V_i ∫ σ_y(ε_p, T_lb) dε_p over the frames (JC card, rate factor 1, T_lb as in §34;
    trapezoid, with left-point as a control);
  - zone = reference depth d ≤ 1.25 µm in the particle, and in the substrate within r ≤ 1.5 R;
  - W_zone and W_rest per mesh, and their changes.
  - These are upper bounds (σ_y at T_lb ≥ σ_y at the engine's T). No attribution is claimed.
- **Further profile data:**
  - w_½, q, q′ and ε_peak at the last frame;
  - widths in the current configuration;
  - the non-qualifying stations;
  - ε_bg per station.
- **Where the peak sits:** the layer index from the surface (layer 1 = particles in the interface file's contact list).
  This cannot be judged. With frictionless contact, surface localisation is physical as well, so a peak in layer 1
  does not separate a band from TLSPH's face-layer deficit.
- **Bonded runs (CS-23 30×, if Q1 allows):** the same widths, q and q′ per station, to show whether a sticking
  interface localises differently.

## Prediction (judgment, before any number)

- Necessary condition met: 0.65;
- intermediate: 0.20;
- step 0 fails on TLSPH: 0.10;
- not determinable: 0.05.
- Basis: no width-setting mechanism in the model (Why). §34 shows peak ε_p rising from 0.80 to 1.37 from R/8 to R/16
  at 0.51 t_p. The odds are lopsided by design: the check is a cheap screen for a negative.

## What follows (stated now; Peter decides after the result)

- **step 0 fails on TLSPH:** the length path loses its premise on TLSPH. Close the focus, or use quads only as a
  testbed.
- **necessary condition met:** step 0 survives a screen it was expected to pass. **This alone does not justify the
  build.** Peter weighs it with the sink table, the contact-stiffness cause and the cost (note §11a).
- **intermediate:** report and decide.
- **not determinable:** decide whether a rerun with more output is worth it.

## Who runs it

WSL A, post-processing of existing files only, next free section of opencourant-verification.md, rows
`results/band_check_*.csv`. Task written at the freeze.
