# Band check: is the TLSPH edge band set by the mesh, and does it carry the rebound drift? (spec and prediction, DRAFT — not frozen)

Drafted 2026-11-24 (cloud, modeller) at Peter's request (chat 2026-11-24; length-scale-note-2026-11-20.md §11a,
"cheaper first look"). `kind = check`; no hunch, no budget. Existing files only: **no run, no build.**

## Why

Step 0 of the length-scale chain says that the edge fails to converge because no length is present. It is unproven
on our own data (note §11a, objection 1). Johnson–Cook plus an EOS has no length, so if the edge localises, step 0
makes two predictions that existing TLSPH files can check:

1. **Band:** the edge shear band stays a fixed number of particle spacings wide. Its width in µm therefore shrinks
   about fourfold from R/8 to R/32, while peak ε_p rises.
2. **Rebound energy:** if that band drives the rebound drift (e(off) 0.0936 / 0.0649 / 0.0571 at R/8 / R/16 / R/32,
   solver-facts §3), the extra plastic work dissipated near the interface on finer meshes is of the order of the
   rebound kinetic energy lost: ΔKE ≈ (0.0936² − 0.0571²) · KE₀ ≈ 2.8 nJ per quarter model, with KE₀ = 5.09·10⁻⁷ J.

A negative outcome on (1) is decisive: if the band width converges in µm, something already sets it, a material
length would change little, and the length path loses its premise on TLSPH.

A positive outcome makes step 0 plausible, but it is still a correlation; only a fixed-ℓ build tests it causally. A
known competing cause of the rebound drift is the contact penalty stiffness k = stfac·B·s, which scales with the mesh
(solver-facts §3).

## Facts checked (coldspray-procedure.md)

solver-facts §3:
- the §30 off runs and their e(off) values;
- TL particles heat and soften, the temperature is not written, and T_lb is the plastic-work lower bound (§34);
- costs;
- the face-layer deficit of TLSPH: end layers carry 0.655 / 0.845 of the stress;
- contact is frictionless (the off branch has no bond).

§34 shows that ε_p is written per particle per frame in AL08off and AL16off (animations EPSP, P, VEL; about 50 frames
to 2.83 t_p, t_p = 0.707 D/V).

**Not covered — never read/used before; check the output first:**
- (i) ε_p and positions in the **AL32off** frames;
- (ii) particle identity across frames at R/32;
- (iii) per-particle volume (lattice s³ or written);
- (iv) the reference (frame-0) positions as the depth coordinate.

Q1 settles them before any number is read.

## Q1: files (reading only)

For the §30 off runs AL08off, AL16off, AL32off (engine `27e53d5f0`):
1. Are ε_p and positions written per particle in every frame, with stable particle ids, on all three meshes?
2. Per-particle volume: written, or the lattice value s³ (state which, per body)?
3. The frame times, and the frame nearest t = t_p.

If (1) fails for any mesh: stop and report "not determinable from existing files". A rerun is decided later, not
here.

## Q2: data (existing files only)

**Coordinates.** Reference positions are frame 0. Depth d is measured in the reference configuration, normal to the
body's reference contact surface:
- particle: d = R − |X − X_c|;
- substrate: d = distance below the original top surface.

Widths are given in µm and in units of the mesh's own spacing s (1.25 / 0.625 / 0.3125 µm).

**Stations** (six, fixed now). Each is a line along the reference inward normal, in the meridian plane at azimuth
45° (the middle of the quarter model, away from both symmetry planes):
- particle: polar angle θ₀ = 30°, 50°, 70° from the impact pole;
- substrate: reference radius r₀ = 0.25 R, 0.50 R, 0.75 R.

A particle belongs to a station if its reference position lies within 0.75 s of the line.

**Profile and width at the judged frame** (the frame nearest t = t_p):
- ε_p(d) along the station, ordered by d;
- ε_peak = the maximum;
- **w_½** = the length of the set {d : ε_p(d) ≥ ½ ε_peak}, with linear interpolation between neighbouring particles.
  This covers a band at the surface (one-sided) and one inside the material.

**A station qualifies** if ε_peak ≥ 0.5 on all three meshes. Only qualifying stations are judged, because localisation
is expected only where the material is strongly strained.

**Ratio:** q = w_½(R/8) / w_½(R/32) in µm, per qualifying station. A purely mesh-set band gives q = 4, a physical
width q = 1.

**Rebound energy.**
- **Plastic work per particle:** W_i = V_i ∫ σ_y(ε_p, T_lb) dε_p over the frames from 0 to the last. σ_y is the JC
  card with rate factor 1 and T_lb as in §34. The thermal factor is zero for T_lb ≥ T_m.
  - Primary: trapezoid in ε_p between frames.
  - Control: left-point.
- **Zone:** particles with reference depth d ≤ 1.25 µm (one R/8 spacing; 2 and 4 layers on R/16 and R/32), in the
  particle, and in the substrate within r ≤ 1.5 R. **Rest:** every other particle.
- **Changes:** ΔW_zone = W_zone(R/32) − W_zone(R/8); ΔW_rest likewise.
- **ΔKE** = (e8² − e32²) · KE₀, from the §30 e(off) rows, recomputed by the script.
- **Bounds:** σ_y at T_lb overstates the yield stress where the engine's T > T_lb, so the absolute W are upper bounds.
  The rule uses mesh differences only, with the same approximation on every mesh.

## Rule (fixed now)

Width, over the qualifying stations (majority = more than half):
- **mesh-set** if q ≥ 2.5 at a majority;
- **physical width** if q ≤ 1.5 at a majority;
- **intermediate** otherwise.

Rebound energy:
- **holds** if ΔW_zone ≥ 0.5 ΔKE and ΔW_zone ≥ |ΔW_rest|;
- **fails** otherwise;
- **not determinable** if the trapezoid and left-point ΔW_zone differ by more than 0.5 |ΔW_zone|.

Verdict:
- **not determinable** if Q1 stops, or fewer than 2 stations qualify;
- **step 0 fails on TLSPH** if the width is physical;
- **step 0 plausible on TLSPH** if the band is mesh-set and the rebound-energy test holds;
- **mesh-set band, not the rebound driver** if the band is mesh-set and the rebound-energy test fails;
- **mesh-set band, rebound energy open** if the band is mesh-set and the rebound-energy test is not determinable;
- **intermediate** otherwise.

**Reported, not judged:**
- q and w_½ at R/16, and at the last frame;
- ε_peak per station and mesh;
- widths in the current configuration;
- the non-qualifying stations;
- W_zone and W_rest per mesh;
- **where the peak sits:** the layer index from the surface (layer 1 = particles in the interface file's contact list).
  This cannot be judged here. With frictionless contact, localisation at the surface is physical as well, so a peak in
  layer 1 does not separate a band from TLSPH's face-layer deficit. It is reported so that Peter can weigh it.

## Prediction (judgment, before any number)

- Verdict:
  - step 0 plausible: 0.22;
  - mesh-set band, not the rebound driver: 0.25;
  - mesh-set band, rebound energy open: 0.08;
  - intermediate: 0.25;
  - step 0 fails on TLSPH: 0.15;
  - not determinable: 0.05.
- Width alone: mesh-set 0.55; intermediate 0.25; physical 0.15.
- Basis: §34 shows peak ε_p rising from 0.80 to 1.37 from R/8 to R/16 at 0.51 t_p, which fits a mesh-set band. The
  rebound energy test is weakened by the competing contact-stiffness cause.

## What follows (stated now; Peter decides after the result)

- **step 0 fails on TLSPH:** the length path loses its premise on TLSPH. Close the focus, or use quads only as a
  testbed.
- **step 0 plausible:** grounds for the build. A design note for a Ge-type nonlocal ε_p and T (opencourant-verification
  §40 item 5), host chosen by the ℓ reading (note §11a).
- **mesh-set band, not the rebound driver:** a length would change the edge fields, not the rebound. Weigh the build
  against the contact-stiffness cause.
- **mesh-set band, rebound energy open** or **intermediate:** report and decide.
- **not determinable:** decide whether a rerun with more output is worth it.

## Who runs it

WSL A, post-processing of the §30 off-run files only, next free section of opencourant-verification.md, rows
`results/band_check_*.csv`. Task written at the freeze.
