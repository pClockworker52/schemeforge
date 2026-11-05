# OpenCourant verification: feature check and rung 0 (elastic, elastic-plastic)

Sessions of 2026-11-03 and 2026-11-04 (rung 1, element formulation, temperature checks). Solver: OpenCourant `latest-20261011` (commit `cb760c2`), local install, 1 process,
1 thread ([openradioss-setup.md](openradioss-setup.md)). Decision context: DECISIONS 2026-11-03 "Main impact
solver: OpenCourant instead of OpenRadioss". Peter's order: option 1 (JC + Grüneisen in 2D axisymmetric), then
option 2 (rung 0 against the exact solution and the JAX code), then the elastic-plastic 1D case in OpenCourant
only. Option 4 (Taylor validation) is on hold.

All decks are our own, written by [`opencourant/scripts/ocdeck.py`](opencourant/scripts/ocdeck.py) from the card
formats in the shipped keyword configuration (`hm_cfg_files`) and the Radioss 2022 Reference Guide (RG). No QA deck
is used or copied.

## Summary

| Question | Answer |
|---|---|
| JC + Mie–Grüneisen on axisymmetric quads? | **Yes.** `/MAT/LAW4` + `/EOS/GRUNEISEN` on `/QUAD` with N2D3D = 1 is accepted and runs; confined and unconfined plates at 500 m/s; pressure peak −4 % of the Hugoniot estimate. |
| Adiabatic heating? | **LAW4's built-in temperature is exactly plastic-work heating** (ΔT = ∫σ_y dε_p/ρc_p, checked to 0.4 % with a constant yield stress, §2.1), **plus** bulk-viscosity work when q is on, **plus** reversible compression heating when `/EOS/GRUNEISEN` is used. **`/HEAT/MAT`** gives T ≈ 0 on axisymmetric quads (unusable in 2D). On 3D bricks it works but **ignores EFRAC** for LAW4 (0.9 and 0.5 give the same T), so a Taylor–Quinney fraction β needs ρc_p/β instead. |
| Rung 0 (elastic) against the exact solution? | **Agrees.** Contact time error +1.05/+0.36/−0.04/−0.31 % and rebound 0.965/0.978/0.986/0.991 V at 25/50/100/200 elements (`Isolid = 17`) (variant A, closest to the JAX settings). JAX: +1.9/+0.9/+0.7/+0.4 %, 0.966/0.979/0.987/0.992 V (reproduced here). |
| Plateau force | **+0.69 % at every mesh**: a finite-strain effect, ≈ 0.42 × V/c_d, which vanishes as V → 0. Quads have no small-strain option (starter error 1223). JAX is linear and exact. |
| Rung 0p (elastic-plastic two-wave) | **Agrees with the closed form** with q ≈ 0: wall stress σ₂ to 0.9997 at 200 elements, plastic front speed 0.993 c_b, elastic front 0.997 c_d; ε_p behind the plastic wave 1.05 (q ≈ 0) and 0.986 (default q) of the closed form. |
| **Axisymmetric element** | **Use `Isolid = 17`** (4-point quad). The default 2D solid is area-weighted. It fails the Hertz sphere (about 5 × too stiff, mesh-independent) and loses axial momentum in free flight; it passes only the 1D cases. With `Isolid = 17` OpenCourant agrees with the JAX code on the unconfined disc (to 0.004 V) and on the Hertz sphere (to about 1 %). **Lagrangian only**: with ALE the starter falls back to the area-weighted element (§5.4). §5 |
| Rung 1 (Hertz sphere) | **Agrees with the JAX code** (contact, peak, approach and rebound within about 1 % at 10 × 20, 15 × 30, 20 × 40). Both are 4–5 % short of quasi-static Hertz at 20 m/s and approach it at lower speed (dynamic effect). |
| Jet distortion (open item 8) | **SPH is 3D-only** (source: no N2D use, 3D kernel only). **No Lagrangian remeshing for `/QUAD`** (`/ADMESH` is shells only). **Option 1 (Lagrangian, `Isolid = 17`, Al–Al, 500–1000 m/s):** the mesh fails at the jet root at 5–37 % of the penetration time on the finest mesh, earlier with refinement; edge quantities are not converged (rerun with sourced γ₀ = 2.17: same conclusion). A bonding criterion cannot be evaluated before failure. §8 |
| 3D SPH ladder (Peter, 2026-11-04) | **S0 and S0p pass** (h = 1.12 s, the starter default; default artificial viscosity). **Hertz S1 is not a clean pass:** it needs surface-conforming particles; at 20 m/s it converges toward JAX (within 2–3 % at R/64, peak 4 % low), at 2 m/s it is still 7–10 % off at R/64. Quarter symmetry = half model. Cost 4.6 µs/particle-cycle (1 thread), 0.9 µs at 8 workers. **Two SPH parts are kernel-welded** (tension and shear across the interface), so the Al–Al interaction is a decision for Peter. §9 |
| CS-11 interface bracket (Peter, 2026-11-04) | **F0 passes** (SPH sphere on `Isolid = 17` bricks, TYPE7, gap s/2, Stfac 10: R/32 peak 1.037, approach 0.987, rebound 0.99). **W0 fails** (SPH on SPH: R/32 peak 1.19, approach 0.68; depends on the start position). Al–Al F sweep (R/16, 400–1200 m/s): every run stops on contact-edge brick collapse at 0.115–0.17 D/V; J ≤ 1.06, no crossing of 1.5. At R/32 F is unevaluable (collapse before 0.1 D/V). **CS-11 inconclusive.** Failed SPH particles leave the kernel interaction (source). §10 |
| CS-13 rung H0 (Peter, 2026-11-05) | **Fails.** OpenCourant has **no heat conduction on 2D quads** (`Isolid = 17` or 0): an initial 100 K step does not change at all (RG `/THERMAL`: solid, shell and SPH only; no quad conduction routine in the source). The same deck on 3D bricks matches erfc to 0.017 % at h = 0.156 µm. k = 237 W/(m K) sourced (HG2018a). No impact run made; fallback (JAX) is Peter's decision. §11 |
| CS-13b (task 2026-11-05-a) | **Blocked, no verdict.** Rung H0-SPH fails narrowly (2.5 % at s = 0.156 µm against 2 %; first order). The prescribed fallback, conductive bricks with an adiabatic SPH particle, cannot run: without a particle `/HEAT/MAT` the engine exhausts memory (WSL OOM); with one, the particle overheats to 9·10⁴ K whatever k and EFRAC are (energy allows ≤ 357 K at 800 m/s). None of the 24 runs made; options for Peter. §12 |
| Pitfalls found | (1) The rigid-wall force output `FNZ` is ∫σ dr, not a force, in axisymmetric runs. (2) Default quadratic bulk viscosity + default time-step scale goes unstable (zero volume at cycle 0) on 50:1 quads. (3) Default bulk viscosity costs 5–7 % rebound velocity in the elastic case. (4) Axisymmetric time-history internal energy (and the ERR % energy-balance column) reads zero: energy balance cannot be checked from it. (5) With `Isolid = 17` the temperature is computed but not written out. |

## 1. Method

**Geometry and boundary conditions** (`ocdeck.write_plate_deck`).
- SI units (`/BEGIN` kg m s, deck version 2026). `/ANALY` N2D3D = 1. Quads in the YZ plane: Y = r, Z = axis.
- Plate 0 ≤ r ≤ R, 0 ≤ z ≤ L, uniform mesh, `/PROP/TYPE14` with `Isolid = 17` (4-point quad; the default element fails rung 1, §5).
- Frictionless rigid plane `/RWALL/PLANE` (Slide = 0) at z = 0, normal +z, all nodes as secondary nodes.
- `/INIVEL` −V on all nodes, so the plate starts in contact.
- `/BCS` fixes u_r (and x) on the axis. For the confined cases it fixes u_r on all nodes. The starter then reports warning 312, "incompatible kinematic conditions", for the nodes that carry both `/BCS` and the wall; the elastic results below show no effect.

**Output.** Axisymmetric time-history quantities are **per radian**: `MASS` = ρL³/2 to machine precision, versus
ρπL³ for the full ring.
- The wall force is taken as F = 2π·d(ZMOM)/dt from the part time history, written every cycle (`/TFILE` below the time step). The wall is the only axial force, so this is exact up to the 7 printed digits.
- **Finding:** the `/TH/RWALL` column `FNZ` equals −∫σ_zz dr, measured as −1.0066·σR at R = L and 2L and n_r = 4 and 8 (`Isolid = 0`; −1.0069·σR with `Isolid = 17`). It is not a force per radian (which would be σR²/2). Do not use the rigid-wall time-history force in 2D axisymmetric runs without this conversion; it is only valid for uniform σ.

**Metrics (rung 0)**, identical to `tests/test_impact_axisym.py`:
- **plateau:** mean force over 0.2–0.8 t_c divided by ρc_dVπL²;
- **contact:** last time with F > 10⁻⁹ F_exact, divided by t_c = 2L/c_d;
- **rebound:** centre-of-mass velocity at t = 3L/c_d, divided by V.

**Variants** (`rung0.py`):

| Variant | Bulk viscosity q_a, q_b | Time-step scale (`/DT`) | Comment |
|---|---|---|---|
| A | 10⁻³⁰ (≈ 0) | 0.4 | closest to the JAX code (no viscosity, CFL 0.4) |
| B | ≈ 0 | 0.9 (default) | |
| C | defaults 1.10, 0.05 (RG p.1703–1704) | 0.9 | OpenCourant out of the box |

Reproduce: `python rung0.py <work_dir> <out.csv>`, `python rung0p.py <work_dir> <out.csv> <traces.npy>`, then
`plot_rung0.py` and `plot_rung0p.py`. All need numpy (plus matplotlib and pillow for plots) and the local install
path in `ocdeck.OC_ROOT`. Raw runs stay in the session scratchpad; result tables are in
[`opencourant/results/`](opencourant/results/).

## 2. Option 1: Johnson–Cook + Mie–Grüneisen + heating on axisymmetric quads

**Material:** nominal copper-like values, typed from memory and **not verified**. That is fine for a feature
check and they must not be used for results:
- E = 124 GPa, ν = 0.34, ρ = 8930 kg/m³;
- JC: A = 90 MPa, B = 292 MPa, n = 0.31, C = 0.025, ε̇₀ = 1 s⁻¹, m = 1.09, T_melt = 1356 K;
- ρc_p = 3.44 MJ/(m³K);
- Grüneisen: c₀ = 3940 m/s, S₁ = 1.49, γ₀ = 1.99.

Plate L = R = 10 µm, V = 500 m/s, default bulk viscosity.

| Run | Setup | Starter / engine | Result |
|---|---|---|---|
| J1 | LAW4 + GRUNEISEN, confined, 50 × 4 | accepted (only warning 312); normal termination, 627 cycles | Listing echoes "JOHNSON COOK LAW" and "MIE-GRUNEISEN EOS". Peak cell pressure 19.8 GPa vs ρ₀(c₀ + S₁V)V − ⅔σ_y ≈ 20.6 GPa (−4 %, frames every 0.25 ns). ε_p max 0.30. **T: 293 K → 880 K peak** (during compression), 705 K at 15 ns. |
| J2 | as J1 + `/HEAT/MAT` (EFRAC 0.9) | accepted; listing echoes T0 = 293, ρc_p, "FRACTION OF STRAIN ENERGY CONVERTED INTO HEAT = 0.9"; normal | **T ≈ 10⁻⁸ K everywhere** |
| J3 | as J2, unconfined, 50 × 10 | normal, 2290 cycles | ε_p max 1.92; T ≈ 10⁻⁹ K |
| J4, J5 | J2, J3 + engine `/THERMAL` | normal; engine prints "FINITE ELEMENT THERMAL ANALYSIS … TEMPERATURE (SOLID ONLY)" | T starts at 0 (T₀ not applied), max ≈ 10⁻⁸ K |
| J6 | J4 with conductivity AS = 400 W/(m K) | normal | unchanged, T ≈ 10⁻⁸ K |
| J7 | LAW4 + GRUNEISEN, no `/HEAT/MAT`, unconfined, 50 × 50 | normal, 1.0 s engine time | GIF below: ε_p max 1.89, T max 693 K at 12.5 ns |

`/HEAT/MAT` notes:
- The 2022+ card format has no `Iform` field. RG p.1223–1224 says `Iform = 0` (finite volume) is for ALE solids and `Iform = 1` for Lagrangian solids and shells.
- The engine's "(SOLID ONLY)" message suggests 2D quads are not covered.
- Not resolved. Next test: the same card on 3D bricks.
- Until then, the only working temperature path in 2D is LAW4's built-in adiabatic update. That takes T from the element internal energy, including reversible compression energy (hence the 880 K peak and drop to 705 K on release), and offers no Taylor–Quinney fraction.

![JC + Grüneisen plate, plastic strain and temperature](opencourant/figures/opt1_jc_gruneisen.gif)

*Unconfined plate, 500 m/s, mirrored about the axis, default element (`Isolid = 0`). With the verified element
(`Isolid = 17`) the deformation is nearly the same (§2.2), but its temperature is not written out (§5.3). Feature
check only; the material values are nominal.*

### 2.1 What the LAW4 temperature contains (exact check)

The source sets the update (`engine/source/materials/mat/mat004/m4law.F`, lines 223–239, commit `cb760c2`):
- **without thermal analysis:** `TEMPEL = TEMPEL + SIGY*DPLA/RHOCP`, i.e. plastic work with factor 1;
- **with thermal analysis on a Lagrangian mesh:** `FHEAT = FHEAT + SIGY*DPLA*VOL` as the heat source, with no EFRAC factor in that line.

Check: Johnson–Cook with B = C = 0 gives a constant yield stress A = 300 MPa, so each element must heat by exactly
A·ε_p/ρc_p. Confined plate (2D, 20 × 2) and confined brick column (3D, 20 bricks) at 500 m/s, time-step scale
0.4 ([`tcheck.py`](opencourant/scripts/tcheck.py), [`results/temperature_check.csv`](opencourant/results/temperature_check.csv)):

| Case | EOS | bulk viscosity | `/HEAT/MAT` | ΔT median (K) | A·ε_p/ρc_p (K) | ratio |
|---|---|---|---|---|---|---|
| 2D | none (LAW4 default) | ≈ 0 | – | 13.09 | 13.14 | **0.996** |
| 2D | none | default | – | 43.99 | 7.37 | 5.97 |
| 2D | Grüneisen | ≈ 0 | – | 91.50 | 14.69 | 6.31 |
| 2D | Grüneisen | default | – | 129.65 | 6.74 | 19.2 |
| 3D | none | ≈ 0 | – | 12.97 | 13.02 | **0.996** |
| 3D | Grüneisen | ≈ 0 | – | 91.83 | 14.15 | 6.51 |
| 3D | none | ≈ 0 | EFRAC 0.9 (+ `/THERMAL`) | 12.90 | 13.01 | **0.998** |
| 3D | none | ≈ 0 | EFRAC 0.5 (+ `/THERMAL`) | 12.90 | 13.01 | **0.998** |

- **Plastic-work heating is exact** (to 0.4 %) when nothing else adds energy.
- **Bulk viscosity adds its dissipated work** to the temperature: 6× here. In a shock that is the irreversible jump the q term represents, but its size is set by q_a and q_b, not by the material.
- **The Grüneisen EOS adds compression heating:** +78 K at about 10 % compression with γ₀ = 1.99, of the order of T·γ·ΔV/V ≈ 60 K. It is reversible and falls on release (J1: 880 K peak, 705 K later).
- **EFRAC has no effect** with LAW4, consistent with the source line. In adiabatic runs, β·W/ρc_p can be obtained by entering ρc_p/β.
- **q ≈ 0 doubles ε_p** in this coarse shock (14.7 K vs 6.7 K of plastic heating), as in rung 0p: ringing behind the jump causes extra yielding.

For cold spray, the interface temperature is meant to come from plastic work. The other two parts should
therefore be either kept small (q small, at a fine mesh) or reported separately (EOS compression heating).

### 2.2 Why the centre lifts off the wall (run J7)

J7 is a squat disc (R = L = 10 µm) on a frictionless, non-adhesive rigid wall, with no failure model (Pmin =
−10³⁰). Underside gap and bottom-layer pressure, read by node ID from the 0.25 ns frames:

| t (ns) | gap at r₀ = 0 / 0.5R / 0.74R (nm) | bottom-layer p at r₀ = 0 / 0.24R / 0.5R / 0.74R (GPa) | outer radius (µm) |
|---|---|---|---|
| 0.5 | 0 / 0 / 0 | 19.7 / 19.7 / 19.7 / 19.4 | 10.4 |
| 1.5 | 0 / 0 / 0 | 19.7 / 19.5 / 10.4 / 4.4 | 11.4 |
| 2.5 | 0 / 0 / 0 | 0.2 / 2.9 / 2.0 / 1.3 | 12.4 |
| 3.0 | 99 / 0 / 0 | −0.4 / −0.5 / −0.2 / 0.6 | 12.9 |
| 4.5 | 846 / 186 / 39 | −1.5 / −1.5 / −1.0 / −0.3 | 14.2 |
| 5.0 | 1502 / 418 / 96 | 1.9 / 1.3 / 0.0 / −0.2 | 14.6 |
| 12.5 | 1249 / 3 / 0 | 0.0 / −0.5 / 1.5 / 0.9 | 19.5 |

1. **Impact shock (0–2 ns).** The face is loaded to about 19.7 GPa (Hugoniot estimate 20.6 GPa). The shock runs up the disc at U ≈ c₀ + S₁V ≈ 4.7 km/s. Behind it the material is at rest axially and compressed by about V/U ≈ 10 %.
2. **Lateral release from the free side face.** The cylinder's side is free, so a release fan runs inward from the edge. The bottom-layer pressure drops at 0.74R by 1 ns, at 0.5R by 1.5 ns, at 0.24R by 2 ns and on the axis by 2.5 ns (about 4 km/s inward). Behind it the material flows **outward along the wall** (arrows in the GIF): the rim pancakes and slides, so the outer radius grows from 10 to 19.5 µm. This ring stays on the wall because its motion is mostly radial.
3. **Focusing on the axis (≈ 2.5–3 ns).** The inward release meets itself on the axis and the pressure there goes negative. The highly compressed central column springs back (stored EOS compression and elastic energy) and pushes the underside up. **The centre leaves the wall at about 2.7 ns**, before the 1D picture would predict it: there, the release from the top face is back at the wall only at 2L/U ≈ 4.3 ns.
4. **Top-face release (≈ 4.3–4.5 ns).** It arrives and adds tension (−1.5 GPa in the bottom layer). The centre underside briefly moves up at about 1.2 km/s, and the gap reaches 1.5 µm at 5 ns.
5. **Afterwards** the thinned centre rings like a free plate: the gap swings between 1.1 and 1.8 µm with a period of about 3.5 ns. The rim (r₀ ≥ 0.74R) stays in or near contact and keeps sliding outward.

**Is it physical?** The mechanisms are: shock, release from the free edge, cylindrical focusing on the axis, and
springback of the compressed core. These are ordinary wave mechanics, and the axis is where the release waves from
all around the edge meet. For this idealised problem, then, a central gap with the rim still sliding is the
expected answer, not a solver artefact.

What is idealised or not converged:
- **No adhesion.** Any tension at the interface separates it. Real bonding would hold where bonded, which is exactly the cold-spray question.
- **Frictionless wall.**
- **No spall model.** The disc carries −1.5 GPa of tension; a failure model could open a spall plane instead.
- **Coarse mesh and default bulk viscosity.** 50 × 50 cells; the ringing amplitude and the 1.2 km/s spike are not mesh-converged.
- **Nominal material values.**
- **Geometry.** A real particle is a sphere, so contact grows from a point and the release comes from the moving contact edge, not from a fixed side face.

For orientation only (general knowledge, not checked in this session): single-particle cold-spray impacts are
often described with an unbonded centre and bonding in an outer ring. The same release-wave picture is the usual
explanation.

**Re-checked with `Isolid = 17` (§5).** The tables above come from the default element. Re-run with the 4-point
quad, the lift-off is essentially the same:
- the gap on the axis is 88 nm at 3 ns (99 before), 436 nm at 4 ns (492), 1360 nm at 5 ns (1502);
- the same pressure sequence;
- the outer radius is 18.6 µm at 12 ns (19.3).

The explanation stands. The GIF below is from the `Isolid = 17` run.

![Pressure, velocity and underside gap](opencourant/figures/opt1_liftoff.gif)

*Left: pressure (red compression, blue tension; scale −3 to 20 GPa), velocity arrows, mirrored. Right: underside
gap at three initial radii; the dotted line marks 2L/U, when the top-face release returns to the wall in 1D.*

## 3. Rung 0: elastic confined plate (comparison with the JAX code)

E = 70 GPa, ν = 0.35, ρ = 2700 kg/m³, L = R = 10 µm, n_r = 4, V = 100 m/s.
c_d = 6450.54 m/s, t_c = 2L/c_d = 3.1005 ns, F_exact = ρc_dVπL² = 0.54715 N.

JAX rows: `confined_plate_on_rigid_wall` rerun in this session (`uv run`, x64), identical to Peter's numbers.

| n_z | JAX plateau | JAX contact | JAX rebound | OC A plateau | OC A contact | OC A rebound | OC B contact | OC B rebound | OC C contact | OC C rebound |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 1.0000 | 1.0190 | 0.9656 | 1.0069 | 1.0105 | 0.9650 | 1.0156 | 0.9689 | 1.0001 | 0.9336 |
| 50 | 1.0000 | 1.0088 | 0.9790 | 1.0069 | 1.0036 | 0.9784 | 1.0046 | 0.9813 | 0.9976 | 0.9455 |
| 100 | 1.0000 | 1.0072 | 0.9871 | 1.0069 | 0.9996 | 0.9863 | 1.0000 | 0.9884 | 0.9942 | 0.9546 |
| 200 | 1.0000 | 1.0038 | 0.9920 | 1.0069 | 0.9969 | 0.9911 | 0.9969 | 0.9926 | **stopped** | **stopped** |

All OpenCourant columns use `Isolid = 17` (§5). The full table, with KE ratio, `FNZ` and cycle counts, is in
[`results/rung0_opencourant.csv`](opencourant/results/rung0_opencourant.csv). Engine time ≤ 0.2 s per run.
The first runs with the default element (`Isolid = 0`) are kept in `rung0_opencourant_isolid0.csv`. In this
confined case they differ by at most 0.0006 (plateau 1.0066, rebound 0.9905 at 200 elements), because without
radial motion the two formulations nearly coincide.

![Rung 0 comparison](opencourant/figures/rung0_compare.png)

**Findings**
- **Rebound velocity:** OpenCourant without viscosity (A, B) and JAX converge alike: deficit 3.5 → 2.2 → 1.4 → 0.9 % (JAX 3.4 → 2.1 → 1.3 → 0.8 %), a factor of about 1.6 per mesh doubling (order ≈ 0.7) in both. The two codes differ by ≤ 0.004 V at every mesh.
- **Contact time:** OpenCourant converges from above and crosses 2L/c_d at about 100 elements, ending at −0.3 % at 200. That fits the finite-strain stiffening below (the wave runs about 0.3 % faster at this strain); JAX stays above.
- **Plateau +0.69 % (+0.66 % with `Isolid = 0`), the same at every mesh, time step and viscosity.**

  | V (m/s) | strain V/c_d | plateau − 1 | ratio (plateau − 1) / strain |
  |---|---|---|---|
  | 1 | 1.6e-4 | +0.00006 | 0.40 |
  | 10 | 1.6e-3 | +0.00065 | 0.42 |
  | 100 | 1.6e-2 | +0.00659 | 0.43 |
  | 1000 | 0.155 | +0.0696 | 0.45 |

  (A settings, 100 elements, `Isolid = 0`.) The excess scales with the strain and vanishes as V → 0, so it is the
  finite-strain formulation, not an error. The exact solution and the JAX code are small-strain linear. At
  1000 m/s the contact time drops to 0.937 t_c for the same reason. Switching it off is not possible: `Ismstr`
  = 1, 10 or 11 on quads stops the starter with error 1223, "QUAD ELEMENT IS NOT COMPATIBLE WITH SMALL STRAIN
  OPTIONS". For cold spray (strains of order 1) this is the physics we want; for verification against linear
  solutions it sets a floor of about 0.4 ε.
- **Default bulk viscosity (C)** absorbs energy: the rebound deficit is 6.7 → 5.5 → 4.6 % at 25/50/100 elements, falling much more slowly than without viscosity. **At 200 elements (aspect ratio 50) it stops at cycle 0** with "ZERO OR NEGATIVE VOLUME FOR 2D-ELEMENT". Each of these avoids it: q_a ≈ 0, time-step scale 0.4, or n_r = 8 or 16 (aspect ≤ 25). The quadratic term is the trigger; q_a = 1.1 alone fails, q_b = 0.05 alone runs.

## 4. Rung 0p: elastic–perfectly-plastic confined plate (OpenCourant only)

Same plate, `/MAT/LAW2` with Y = 100 MPa, no hardening (b = 0), no rate or temperature terms. Uniaxial strain,
small-strain closed form (`rung0p.py`):
- σ_HEL = Y(1 − ν)/(1 − 2ν) = 216.7 MPa, carried by an elastic precursor at c_d = 6450.5 m/s; u_HEL = σ_HEL/(ρc_d) = 12.44 m/s.
- The plastic wave runs at c_b = √(K/ρ) = 5367.2 m/s; σ₂ = σ_HEL + ρc_b(V − u_HEL) = 761.0 MPa at V = 50 m/s.
- The wall stress is σ₂ from t = 0 until the release from the back face returns at 2L/c_d.
- ε_p behind the plastic wave = ⅔(V − u_HEL)/c_b = 0.00467 (uniaxial strain: dε_p = ⅔ dε_zz after yield).

The stress profile |σ_zz| = p + ⅔σ_vM is taken per element layer, against the initial position z₀, at
t = 0.75 L/c_d. That is before the precursor reaches the back face. Front positions are the mid-level crossings.
Time-step scale 0.4 throughout.

| V | n_z | q | wall plateau / σ₂ | profile σ₂ | profile σ_HEL | plastic front / c_b | elastic front / c_d | ε_p behind wave / closed form | rebound / V |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 25 | ≈ 0 | 0.9881 | 0.9851 | – | 0.9659 | 1.0193 | 1.146 | 0.808 |
| 50 | 50 | ≈ 0 | 0.9935 | 0.9896 | 1.070 | 0.9774 | 1.0037 | 1.105 | 0.819 |
| 50 | 100 | ≈ 0 | 0.9972 | 0.9940 | 1.060 | 0.9872 | 0.9983 | 1.074 | 0.824 |
| 50 | 200 | ≈ 0 | **0.9997** | 0.9972 | 1.048 | **0.9933** | **0.9971** | 1.051 | 0.826 |
| 50 | 25 | default | 1.0038 | 1.0030 | – | 0.9763 | 1.0637 | 1.013 | 0.792 |
| 50 | 50 | default | 1.0043 | 1.0017 | 1.084 | 0.9886 | 1.0452 | 0.997 | 0.802 |
| 50 | 100 | default | 1.0042 | 0.9976 | 1.102 | 0.9942 | 1.0338 | 0.991 | 0.807 |
| 50 | 200 | default | 1.0041 | 0.9939 | 1.093 | 0.9975 | 1.0251 | 0.986 | 0.812 |
| 25 | 100 | default | 1.0020 | 0.9972 | 0.982 | 0.9828 | 1.0193 | 0.991 | 0.824 |
| 100 | 100 | default | 1.0087 | 0.9989 | 1.315 | 1.0037 | 1.0485 | 0.989 | 0.868 |
| 200 | 100 | default | 1.0179 | 1.0078 | 1.906 | 1.0163 | 1.0657 | 0.989 | 0.904 |

The table is in [`results/rung0p_opencourant.csv`](opencourant/results/rung0p_opencourant.csv). The rebound has
no closed form here; it is listed for later comparison with the JAX code once that has plasticity.

![Rung 0p summary](opencourant/figures/rung0p_summary.png)

![Rung 0p stress profiles](opencourant/figures/rung0p_profiles.gif)

*Stress profile through the thickness, 200 elements, q ≈ 0, V = 50 m/s. Closed form drawn while it applies
(t ≤ L/c_d).*

**Findings**
- **Two-wave structure reproduced.** Wall stress, plastic wave speed and elastic front speed converge to the closed form with q ≈ 0 (to 0.03 %, 0.7 % and 0.3 % at 200 elements). The plastic strain behind the wave converges from above (+5 % at 200) because the ringing behind the jump causes a little extra yielding.
- **Default viscosity** smears the fronts: the elastic mid-level crossing runs 2.5–6 % ahead, the plateau sits at +0.4 %, and ε_p is within 1.5 %.
- **The σ_HEL shelf** measures 5–10 % high. At t = 0.75 L/c_d the shelf is only 0.126 L wide (12 elements at n = 100), and the ±3-element margins leave too few cells next to an overshooting front. This is a limit of the measurement, not a solver error: the GIF shows the shelf at the right level. At V ≥ 100 m/s the plastic front itself sits in the window, so the column means nothing there.
- **Velocity dependence** of the wall plateau (+0.2/+0.4/+0.9/+1.8 % at 25/50/100/200 m/s) and of the plastic front speed: finite strain again. The pressure-dependent bulk stiffness at finite strain is not in the small-strain closed form.

## 5. Rung 1: Hertz sphere, and the axisymmetric element formulation

### 5.1 What went wrong with the default element

The first rung-1 runs used the default 2D solid (`Isolid = 0`). The sphere came out far too stiff, independent
of the mesh:

| Isolid 0, 15 × 30 | approach / d_Hertz | time of max approach / t_Hertz | peak force / F_Hertz |
|---|---|---|---|
| from momentum (time history) | 0.518 | 0.272 | 1.73 |
| from node positions (animation) | 0.51 | ≈ 0.27 | – |
| 30 × 60 (time history) | 0.516 | 0.271 | 1.74 |

The hourglass coefficient changed nothing (h = 0, default and 0.1 give identical results). Two cross-checks
located the problem:
- **Slender elastic rod** (R = 5 µm, L = 100 µm, uniaxial stress, so radial and hoop terms matter): the plateau stress is ρc₀V to 0.2 %. So the element is right for smooth, nearly uniform fields.
- **Unconfined elastic disc** (R = L = 10 µm, 20 × 20, V = 20 m/s) against the JAX code on the identical mesh: the velocity and force histories agree for about one transit time. After that the default element **loses axial momentum in free flight**, from 0.55 V to 0.42 V, with no node in contact and no axial external force. The wall force read from momentum goes negative.

The source explains it. The default quad (`engine/source/elements/solid_2d/quad/`) is **area-weighted** in
axisymmetric runs:
- nodal mass `MASS = RHO*AREA*OFF*FOURTH`, with no radius factor (`qmass2.F`);
- plane-like area-gradient forces plus 1/r terms `AX1 = (σ_θθ − σ_rr)·A²/(4V)` and `AX2 = σ_rz·A²/(4V)` (`qfint2.F`, `qcumu2.F`);
- the time history reports real per-radian quantities from separate routines, which is why mass and momentum looked consistent at t = 0.

An area-weighted scheme does not conserve axial momentum, and it gets concentrated loads near the axis
wrong. Hertz contact at the pole is exactly that case. The confined plate (no radial motion) and the slender rod
(uniform fields) do not show it.

The force dispatcher (`engine/source/elements/forint.F`, line 1266) calls the 4-point quad `q4forc2` when
`JHBE == 17`, or `N2D == 1 .AND. JHBE == 22`, i.e. `Isolid = 17` in `/PROP/TYPE14`. In our decks `Isolid = 22` gave
the default element again. With **`Isolid = 17`**:

| Unconfined disc, t / (L/c_d) | 1.0 | 2.0 | 3.0 | 4.0 | 5.9 |
|---|---|---|---|---|---|
| v/V JAX | −0.1395 | 0.4938 | 0.5443 | 0.5592 | 0.5592 |
| v/V OpenCourant, `Isolid = 0` | −0.1122 | 0.5642 | 0.4891 | 0.4196 | 0.5125 |
| v/V OpenCourant, `Isolid = 17` | −0.1392 | 0.4973 | 0.5459 | 0.5611 | 0.5605 |

`Isolid = 17` agrees with JAX to 0.004 V and **conserves momentum in free flight** (0.560 ± 0.001 V).
**`ocdeck` now writes `Isolid = 17` by default.** Rungs 0 and 0p were re-run with it (§3, §4).

### 5.2 Rung 1 results

Elastic sphere, E = 70 GPa, ν = 0.35, ρ = 2700 kg/m³, R = 10 µm, V = 20 m/s, touching the frictionless rigid wall
at t = 0. It uses the JAX code's graded square-to-disk mesh (`ocdeck.sphere_mesh` is a copy of
`impact_axisym.sphere_mesh`, shifted up by R), run to 1.6 t_Hertz. Hertz:
- t_Hertz = 28.71 ns, F_Hertz = 0.02898 N, d_Hertz = 0.1951 µm (`rung1.hertz`, identical to `impact_axisym.hertz_reference`);
- t_Hertz ≈ 9.3 × 2R/c_d, so Hertz's quasi-static assumption is only approximately met.

Metrics are identical for both codes:
- **contact:** end of the main pulse, i.e. the first time after the force peak with F < 10⁻³ F_Hertz;
- **peak:** maximum force;
- **approach:** maximum centre-of-mass approach;
- **rebound:** final centre-of-mass velocity / V.

OpenCourant uses `Isolid = 17`, q ≈ 0, time-step scale 0.4 ([`rung1.py`](opencourant/scripts/rung1.py),
[`results/rung1_opencourant.csv`](opencourant/results/rung1_opencourant.csv)).

| Mesh n_u × n_v | Code | contact / t_Hertz | peak / F_Hertz | approach / d_Hertz | rebound / V |
|---|---|---|---|---|---|
| 10 × 20 | JAX | 0.950 | 1.060 | 0.954 | 0.9994 |
| 10 × 20 | OpenCourant | 0.962 | 1.058 | 0.963 | 0.9988 |
| 15 × 30 | JAX | 0.956 | 1.058 | 0.958 | 0.9992 |
| 15 × 30 | OpenCourant | 0.967 | 1.062 | 0.961 | 0.9993 |
| 20 × 40 | JAX | 0.953 | 1.073 | 0.957 | 0.9996 |
| 20 × 40 | OpenCourant | 0.956 | 1.075 | 0.958 | 0.9996 |
| 15 × 30 | OpenCourant, `Isolid = 0` | 0.506 | 1.728 | 0.518 | 0.994 |

Engine time 7 s, 43 s and 150 s (OpenCourant, 1 core); JAX 3 s, 7 s and 24 s.

![Rung 1: Hertz sphere](opencourant/figures/rung1_hertz.png)

![Rung 1: contact zone and force](opencourant/figures/rung1_contact.gif)

*Left: pressure near the pole (mirrored), OpenCourant `Isolid = 17`, 15 × 30; the blue ticks mark the Hertz
contact radius at maximum approach. Right: wall force against JAX and Hertz.*

**Lower impact velocity** (15 × 30, same metrics). t_Hertz / (2R/c_d) grows as V^(−1/5):

| V (m/s) | t_Hertz / (2R/c_d) | JAX contact / peak / approach | OpenCourant contact / peak / approach |
|---|---|---|---|
| 20 | 9.3 | 0.956 / 1.058 / 0.958 | 0.967 / 1.062 / 0.961 |
| 2 | 14.7 | 0.972 / 1.045 / 0.983 | 0.975 / 1.043 / 0.994 |
| 0.2 | 23.3 | 1.016 / 0.914 / 1.000 | **fails**: rebound 2.09 V |

- **Approach** moves to Hertz as the impact becomes more quasi-static (0.958 → 0.983 → 1.000 in JAX). This supports the dynamic explanation of the offset at 20 m/s.
- At 0.2 m/s the contact patch is only about 0.44 µm wide, a few cells, so peak force and contact time are limited by contact resolution there.
- **OpenCourant at 0.2 m/s:** after the main pulse the wall keeps pushing, and the sphere leaves at 2.09 V. The approach is 0.02 µm, and the rigid wall's handling of tiny penetrations evidently injects energy. That is irrelevant at cold-spray speeds (10³–10⁴ × higher), but it shows the wall is not exactly energy-conserving.

- **OpenCourant (`Isolid = 17`) and the JAX code agree to about 1 %** on all four metrics at every mesh. That is the code-to-code verification this rung was meant to give.
- **Both sit 4–5 % short of Hertz in contact time and approach, and 6–7 % above in peak force.** This does not improve between 10 × 20 and 20 × 40 in either code. Two independent codes giving the same offset points to the model rather than either implementation: Hertz is quasi-static, while here t_c ≈ 9 wave transits, and the elastic waves carry part of the load. This is not proven here. A run at lower V (longer t_c relative to the transit time) should move both codes towards Hertz if this is right.
- Rebound 0.999 in both: almost no energy is left in vibrations.
- 30 × 60 is out of reach for OpenCourant on one core: the graded pole cells force a time step of 2.2·10⁻¹⁴ s, about 2.1 million cycles and 2 h per run. JAX needed about 1 h at 30 × 60 and was stopped too.

### 5.3 Temperature output with `Isolid = 17`

With the 4-point quad, the LAW4 temperature is **computed and used**. A thermal-softening test (T_melt = 400 K,
constant yield 300 MPa) gives von Mises 262.0 MPa with `Isolid = 17` and 262.2 MPa with `Isolid = 0`, against
264.7 MPa expected for the 12.6 K rise. But it is **not written out**: animation `TEMP` and `/TH/QUAD TEMP` both
stay at T₀ = 293 K. The plastic strain is written normally. Until this is fixed (to be reported to OpenCourant),
temperature fields in 2D need `Isolid = 0` for output only. Its deformation is close for the plate cases (§2.2),
but it is not verified for contact problems.

### 5.4 `Isolid = 17` and ALE

A local copy of the QA copper rod (`ALE2D/bar2_v41`, axisymmetric ALE) with `Isolid = 17` runs. The starter
replaces the element: warning 1222, "QUAD FORMULATION 17, IS NOT AVAILABLE WITH ALE OR EULERIAN FORMULATION, IS
SET TO 2". **In 2D axisymmetric runs the verified 4-point element is Lagrangian only. ALE and Euler parts use the
area-weighted element**, the one that fails rung 1. That matters for the jet, where ALE was one of the options for
extreme distortion. In 2D axisymmetric, ALE would need its own verification (a Hertz-type or disc case run as ALE)
before use. SPH is the alternative (3D dropped, open item 8).

## 6. Rules for our own decks (from the above)

1. Take wall forces from momentum (2π d(ZMOM)/dt per part) or from element stresses, not from `/TH/RWALL` FNZ.
2. Remember that axisymmetric time-history output is per radian (×2π for the ring).
3. Use time-step scale 0.4 (`/DT`) or keep the element aspect ratio ≤ about 10 if default bulk viscosity is on.
4. Verification against linear solutions: q ≈ 0 and V ≤ 10 m/s (finite-strain excess ≤ 0.07 %).
5. Temperature: LAW4 built-in (2D and 3D). Enter ρc_p/β for a Taylor–Quinney fraction β, because EFRAC is ignored. Keep bulk viscosity small, because its work heats the material. Report the EOS compression heating separately.
6. **`/PROP/TYPE14` `Isolid = 17`** for every axisymmetric part (ocdeck default). For temperature fields only, `Isolid = 0` output is a stopgap until §5.3 is fixed.
7. Do not use the time-history internal energy or the ERR column in 2D axisymmetric runs. Check energy from kinetic energy and the work done, or from element fields.
8. Velocity sweeps: plain text decks, starter + engine via `subprocess`, one directory per case (`ocdeck.run`); about 0.1–4 s per run at these sizes.

## 7. Open items

1. **Temperature output with `Isolid = 17`** (§5.3): computed but written as T₀ in animation and `/TH/QUAD`. Report to OpenCourant, with a minimal deck (`tcheck.py` case, `isolid=17`). Until then, temperature fields need a workaround.
2. `/HEAT/MAT` on axisymmetric quads (T ≈ 0): works on bricks (§2.1), so this is a 2D limitation. **Explained 2026-11-05 (§11.2):** 2D quads have no conduction routine; the nodal temperature is never updated. In 2D use the LAW4 built-in update with ρc_p/β for a Taylor–Quinney fraction β.
3. JC + Grüneisen against a closed form: a confined plate with an EOS has a Hugoniot solution (elastic precursor + shock). That would be rung 0p with LAW4 instead of LAW2, and the JAX code would need an EOS.
4. Rung 1 at 30 × 60 and finer: about 2 h per OpenCourant run on one core (pole cells force dt ≈ 2·10⁻¹⁴ s). A mesh with less grading at the pole, or MPI, would make it affordable.
5. Rigid wall at very small impact speeds injects energy (§5.2, V = 0.2 m/s). Not relevant for cold spray; note before using the wall for slow contact.
6. Warning 312 (`/BCS` + rigid wall on the same nodes): harmless here; check again with friction or sliding.
7. The QA copper rod ([openradioss-setup.md](openradioss-setup.md) §3.3) is ALE, so it can only use the area-weighted element (§5.4). Its tension behind the front is unexplained; an ALE verification case would cover it.
8. **Jet distortion (Peter, 2026-11-04: 3D dropped).** A third dimension does not reduce mesh distortion at the jet, and a normal impact is axisymmetric. Remaining options: Lagrangian with `Isolid = 17` plus erosion or remeshing (first, cheapest); 2D ALE after its own verification; SPH after its own verification.
9. **3D question is back (Peter):** SPH is 3D-only (§8.1), there is no 2D Lagrangian remeshing (§8.2), and 2D Lagrangian fails at the jet root before a converged edge criterion is available (§8.3). Options after jetting onset: 3D SPH (ladder in §8.4), or 2D ALE after its own verification.
10. **3D SPH (§9), open for Peter:**
    - ~~the particle–substrate interaction method (§9.8)~~ decided: bracket W/F, CS-11 (DECISIONS 2026-11-04); outcome inconclusive, both setups not evaluable (§10.6);
    - ~~whether S1 passes~~ decided: accepted at 20 m/s with stated limits; 2 m/s recorded as not passed;
    - the time-step scale (0.9 is as accurate as 0.3 in S0; check on an impact rung before using it);
    - ξ in tension.
11. **CS-11 (§10):** ~~accept "inconclusive"~~ decided by Peter 2026-11-05 (inconclusive, no further runs). Still not traced: the `Isolid = 24`/`1` nodal time-step collapse with TYPE7 + SPH (§10.2).
12. **CS-13 (§11), open for Peter:** H0 fails (no conduction on 2D quads); JAX fallback or a 3D protocol change.

## 8. Jet distortion: facts and the option-1 diagnostic (Peter's guidance, 2026-11-04)

### 8.1 Fact (a): SPH is 3D-only

- **Starter and engine accept it without warning.** A minimal SPH deck (`/SPHCEL` particles in the YZ plane, `/PROP/TYPE34`, `/ANALY` N2D3D = 1) runs to normal termination; the only warning is an optional-card notice.
- **The SPH code never uses the 2D flag.** In the 67 SPH source files (`engine/source/elements/sph/*` and the starter SPH routines, commit `cb760c2`), `N2D` appears once, in `spstres.F` line 278, where it is only passed on to the material driver. It enters no kinematics, no kernel and no force.
- **The only kernel is the 3D cubic spline:** `W = (1 − 1.5 q² + 0.75 q³) · INVPI/(H*H*H)` (`engine/source/elements/sph/weight.F`, lines 54 and 99–101). There is no 2D normalisation (10/(7πh²)) and no axisymmetric (r-weighted) variant anywhere in the SPH sources.
- **The Reference Guide says so directly** (2022, p.42, "Smooth Particle Hydrodynamics (SPH)"): "The SPH formulation is only available in 3D analysis." (Found 2026-11-04 while setting up §9; the first pass of §8.1 missed this sentence.) `/PROP/TYPE34` also offers only a "3D expansion of h" (p.1753).

**SPH in OpenCourant is 3D-only.** With `/ANALY` N2D3D = 1 it runs silently but computes a 3D particle slab
without axisymmetric terms, which is wrong for our problem and not flagged. Per Peter's guidance this brings back
the 3D question for the stages after jetting onset (§8.4).

### 8.2 Fact (b): no Lagrangian remeshing or rezoning for `/QUAD`

- **`/ADMESH` (adaptive meshing) is for shells only.** It is described as "used in metal forming" (RG p.2508), with state cards only for shells (`/ADMESH/STATE/SHELL`, `/SH3N`) and IDs limited for "node ID and shell ID". The starter builder `starter/source/model/remesh/build_admesh.F` and the engine splitter `engine/source/model/remesh/admdiv.F` use the shell arrays `IXC`/`IXTG` 85 and 41 times, and the quad array `IXQ` and the solid array `IXS` never.
- **The only rezoning is ALE:** `engine/source/ale/arezon.F90` (`subroutine arezon(n2d, numelq, …)`) rezones ALE variables in 2D and 3D. There is no Lagrangian rezoning.

**So there is no 2D Lagrangian remeshing or rezoning for `/QUAD`.** Rezoning exists only inside ALE, which in 2D
uses the area-weighted element (§5.4).

### 8.3 Option 1 diagnostic: Lagrangian `Isolid = 17`, no erosion

**Rerun with the sourced γ₀ = 2.17 (2026-11-04): the conclusion does not change.** Failure still comes earlier
with refinement at every speed and the edge strain is still not converged. Details below.

**Set-up** ([`option1_alal.py`](opencourant/scripts/option1_alal.py)):
- **Particle:** Al sphere, R = 10 µm, O-grid mesh (square core plus mapped layers, regular quads along the whole lower surface).
- **Substrate:** Al block 5R × 5R. Cell size h is matched to the particle within 1.5R of the contact, then graded; bottom fixed.
- **Contact:** two `/INTER/TYPE5` (particle nodes on the substrate surface, substrate nodes on the particle surface; 2D `/SURF/SEG` two-node segments, RG `/SURF/SEG` "format for 2D and axisymmetrical analysis"). Gap 0.001 R at t = 0.
- **Element and models:** `Isolid = 17`, default bulk viscosity, no erosion, no failure model (P_min = −10³⁰).

**Material:** LAW4 + `/EOS/GRUNEISEN` from `docs/research/data/properties.csv`.
- **P-HG-Al** (HG2018a preprint, Extended Data Table 1): ρ = 2700, T_m = 933 K, c_p = 896.9 J/(kg K), ν = 0.35, C₀ = 5305.5 m/s (√(B/ρ), as the preprint uses it), s = 1.339, **γ₀ = 2.17**, JC A = 148.4 MPa, B = 345.5 MPa, n = 0.183, C = 0.001, m = 0.895, reference strain rate 1 s⁻¹, T_ref = 293 K.
- **P-H20-Al** (Hassani2020 Table S1): E = 70 GPa.
- **γ₀ history:** the first sweep (commit `01a1f6b`) used a placeholder γ₀ = 2s − 1 = 1.678 because no sourced value was in the table. Peter added the preprint values on 2026-11-04 (γ₀ = 2.17; the reference strain rate 1 s⁻¹ and T_ref = 293 K were already the values used). All nine runs were repeated with γ₀ = 2.17; the table below is that rerun. The placeholder results are kept in [`results/option1_alal_gamma1678.csv`](opencourant/results/option1_alal_gamma1678.csv) and [`results/option1_alal_eval_gamma1678.csv`](opencourant/results/option1_alal_eval_gamma1678.csv).

**Runs:**
- V = 500, 750, 1000 m/s × h = 0.625, 0.3125, 0.156 µm (R/16, R/32, R/64).
- Window 2 D/V, or until the run stops on the `/DT` minimum time step, set to about dt₀/30 with flag "stop run".
- **OpenCourant prints NORMAL TERMINATION also for that stop.** The stop is therefore judged from the time reached, not from the listing text.
- **Reference contact time t_p:** the end of penetration, when the particle's axial velocity crosses zero. It is taken from the coarse run, which reaches it at all speeds; it is mesh-insensitive (500 m/s: 0.590 coarse, 0.598 medium).
- **Edge quantities:** maximum equivalent plastic strain within 2.5 h of the contact edge (the outermost particle rim node on the substrate surface), at t_eval = min(t_stop, t_p).

| V (m/s) | mesh (h) | outcome | t_stop / t_p | t_eval / (D/V) | contact radius a/R | ε_p edge, particle | ε_p edge, substrate | engine (s) | γ₀ = 1.678: t_stop / t_p |
|---|---|---|---|---|---|---|---|---|---|
| 500 | coarse (0.625 µm) | reached 2 D/V | – | 0.59 | 1.22 | 1.13 | 1.33 | 5.9 | – |
| 500 | medium (0.312 µm) | reached 2 D/V | – | 0.59 | 1.19 | 2.06 | 1.73 | 59 | – |
| 500 | fine (0.156 µm) | **dt collapse** | **0.37** | 0.21 | 0.96 | 2.14 | 3.68 | 65 | 0.40 |
| 750 | coarse (0.625 µm) | reached 2 D/V | – | 0.91 | 1.40 | 1.64 | 4.92 | 9.9 | – |
| 750 | medium (0.312 µm) | **dt collapse** | **0.20** | 0.18 | 0.91 | 1.56 | 6.00 | 3.8 | 0.49 |
| 750 | fine (0.156 µm) | **dt collapse** | **0.08** | 0.06 | 0.56 | 2.16 | 2.01 | 7.0 | 0.08 |
| 1000 | coarse (0.625 µm) | reached 2 D/V | – | 1.33 | 1.51 | 2.35 | 17.3 | 14 | – |
| 1000 | medium (0.312 µm) | **dt collapse** | **0.10** | 0.13 | 0.82 | 2.97 | 1.57 | 1.5 | 0.10 |
| 1000 | fine (0.156 µm) | **dt collapse** | **0.05** | 0.06 | 0.55 | 1.47 | 1.72 | 5.6 | 0.06 |

t_p / (D/V) = 0.593, 0.920, 1.333 at 500, 750, 1000 m/s (γ₀ = 1.678: 0.590, 0.918, 1.325). Tables:
[`results/option1_alal.csv`](opencourant/results/option1_alal.csv) (per run) and
[`results/option1_alal_eval.csv`](opencourant/results/option1_alal_eval.csv) (evaluation).

![Edge plastic strain until failure](opencourant/figures/option1_edge_strain.png)

![Al on Al, 500 m/s, medium mesh, to 2 D/V](opencourant/figures/option1_al500_medium.gif)

*500 m/s, medium mesh, mirrored, to 2 D/V (this run survives). The substrate edge cells at r ≈ R are sheared
flat; a coarse-mesh run that survives is not a converged one (see below).*

**Where the runs fail** ([`option1_failure.py`](opencourant/scripts/option1_failure.py)):
- Every collapse that could be located is controlled by a **substrate surface cell at the contact edge** (centroid z ≈ 0, 0.09–0.15 R from the edge), with a smallest interior angle of 0.3–0.5° (aspect 7–17), i.e. a collapsed cell. (γ₀ = 1.678: 0.10–0.23 R, 0.1–0.5°.)
- The surviving runs end with controlling substrate cells at 1.8–4.7° and dt ≈ 0.17–0.36 dt₀ (500 m/s coarse: a particle cell at 26°, 0.57 dt₀).
- **It is element distortion at the root of the jet, not contact stiffness.**
- Medium 1000 m/s stopped before the first 500-cycle printout, so its controlling cell is not in the listing.
- The threshold dt₀/30 is a choice. The controlling cells were already near zero angle, so a lower threshold would gain little time (not tested).

**Convergence:**
- **The failure time does not converge; it gets earlier with refinement at every speed.** At 500 m/s: none, none, 0.37 t_p. At 750: none, 0.20, 0.08 t_p. At 1000: none, 0.10, 0.05 t_p.
- Finer cells at the edge are crushed sooner, as expected at a moving shear singularity.
- The edge plastic strain is not mesh-converged either. At 500 m/s at t_p: 1.13 (coarse) and 2.06 (medium); fine fails at 0.37 t_p with 2.14. The substrate edge strain varies by up to 10× between meshes at the same speed.
- **Effect of γ₀ (1.678 → 2.17):** eight of nine runs change by at most 0.03 t_p in failure time, and most edge strains by under 10 %. The edge values of failing runs move more (1000 m/s medium, particle: 1.94 → 2.97), as expected for values read off a collapsing cell. The exception is medium 750 m/s, which now fails at 0.20 t_p instead of 0.49 t_p. A failure time that moves by a factor 2.5 under a 30 % change of an EOS parameter that barely affects the other runs is itself a sign that it is set by a collapsing cell, not by the physics.
- **Temperature:** not available. `Isolid = 17` does not write it out (§5.3). The values would come only from LAW4's built-in update (plastic work plus q work plus EOS heating, §2.1).

**Answer to Peter's question (no critical velocity is claimed):**
- **No.** In 2D Lagrangian with the verified element, a jetting or shear-instability criterion at the contact edge cannot be evaluated mesh-converged before the mesh fails.
- On the finest mesh the run fails at 5–37 % of the penetration time, in most cases before a jet has formed (contact radius 0.6–1.0 R).
- With γ₀ = 1.678 the medium 750 m/s run showed a thin substrate jet before failing at 0.49 t_p. With γ₀ = 2.17 it fails at 0.20 t_p, before a jet, so that observation did not even survive a change of γ₀, let alone refinement.
- Coarse meshes survive to t_p, but their edge values are not converged and so cannot carry a criterion.

### 8.4 What the SPH result means for the plan

Per Peter's guidance, a 3D-only SPH stops the SPH route in 2D. It brings back the 3D question for everything
after jetting onset (bonded area, erosion, second impacts). That question is Peter's. Facts for it:
- **What 3D would be for.** A third dimension does not cure Lagrangian distortion (Peter, §7 item 8). In 3D the point would be SPH (mesh-free, so no distortion failure) or 3D ALE with the 8-node brick, which is not the area-weighted 2D element. Neither is verified here.
- **Cost:** superseded by the measured numbers in §9.3. Original estimate: Quarter symmetry with particle spacing R/16 gives about 4.3 × 10³ particles in the particle and about 5.8 × 10⁴ in a 3R × 2R substrate region. With a stable step of about 3·10⁻¹¹ s, 2 D/V at 750 m/s is about 1.8 × 10³ cycles, minutes per run on one machine. Halving the spacing costs about 16×. The SPH cost per particle and cycle in OpenCourant has not been measured.
- **Verification ladder if 3D SPH is chosen:** the same rungs in 3D (confined column against the exact 1D solution, the two-wave case, Hertz against JAX and `Isolid = 17`), and convergence in particle spacing.

ALE in 2D stays last (§5.4).

## 9. 3D SPH verification ladder (Peter's decision, 2026-11-04)

DECISIONS 2026-11-04, "Post-onset simulation route: 3D SPH, no OpenCourant fork": everything after jetting onset
goes to 3D SPH in OpenCourant, with quarter symmetry for normal impacts, after its own verification ladder. Branch
`coldspray/opencourant-sph`. Decks are written by [`sphdeck.py`](opencourant/scripts/sphdeck.py); the rungs are
[`sph_rung0.py`](opencourant/scripts/sph_rung0.py) (S0), [`sph_rung0p.py`](opencourant/scripts/sph_rung0p.py)
(S0p) and [`sph_rung1.py`](opencourant/scripts/sph_rung1.py) (S1). Run times are engine wall-clock on Peter's
laptop (Intel i9-14900HX: 8 performance + 16 efficiency cores, 32 threads, WSL2).

**Status:**
- **S0 (confined column, elastic) passes.**
- **S0p (two-wave, elastic–perfectly-plastic) passes.**
- **S1 (Hertz, quarter symmetry): accepted at 20 m/s by Peter** (DECISIONS 2026-11-04, "Rung S1 accepted at 20 m/s; CS-11 approved"), with stated limits: the peak force is about 4 % low, rebound is reduced by the artificial viscosity, and contacts much smaller than the particle spacing are not resolved. It needs a surface-conforming sphere; a plain lattice sphere fails. At 20 m/s it converges toward JAX and `Isolid = 17` (within 2–3 % at R/64, peak 4 % low). **The 2 m/s case is recorded as not passed** (still 7–10 % off at R/64) and is not pursued (§9.6).
- **Quarter symmetry is exact to plotting accuracy** against a half model (§9.7).
- **Al–Al not started here: stop for Peter.** SPH–SPH particle–substrate interaction in OpenCourant is a kernel coupling that welds the two bodies, so it carries tension and shear across the interface (§9.8). For a jetting and bonding diagnostic that has no defensible default. Peter's decision: bracket the interface (route A + B, hunch CS-11); continued in §10.

### 9.1 SPH settings (candidates for the frozen setup)

| Setting | Chosen | Why | Tested alternatives |
|---|---|---|---|
| Particle arrangement | Cubic net, spacing s, particles at cell centres | Symmetry planes at cell boundaries (s/2 from the nearest particles) then mirror the lattice exactly (§9.2 item 3). | – (the manual's close-packed net would put particles on the symmetry planes) |
| Free curved surfaces | **Surface-conforming:** lattice interior; particles within s of the surface moved radially onto the sphere of radius R − s/2; pairs closer than s/2 merged (0.5 % of particles); particle mass = body mass / N | A plain lattice sphere has a stepped pole (steps of s), and Hertz then fails, worse with refinement (§9.6) | plain lattice |
| Smoothing length h | **h = (√2 m/ρ)^(1/3) = 2^(1/6) s ≈ 1.12 s**, the starter's own default | Flat S0 plateau at every spacing, contact time and rebound converge, cheapest (about 54 neighbours) | 1.25 s (S0 worse), 1.5 s (manual's cubic-net advice: unstable at 200 particles in S0, plateau drifts +1.3 %) |
| Artificial viscosity | **Defaults, q_a (β) = 2, q_b (α) = 1** (Monaghan) | Without it S0 goes unstable at 100 and 200 particles (plateau 0.94, contact +10 %) | off (1e-30) |
| Tensile-instability correction ξ | **0 (default, off)** | Changes nothing in S0 (no tension), costs +70 %. Its effect in tension (rebound, jets) is untested; see §9.8 | 0.3 (Monaghan 2000; the manual's recommended value is an equation lost in the text extraction) |
| Kernel correction order | 0 (default) | – | not varied |
| Conservative smoothing α_cs | 0 (default) | – | not varied |
| Time-step scale | /DT 0.3 (manual: "0.3 is recommended", Theory Manual p.446) | Scale 0.9 gives the same S0 results to four digits at a third of the cost; not yet checked on impact rungs | 0.9 |
| Wall contact | `/RWALL/PLANE`, frictionless, all particle nodes secondary | The particle centre stops at the wall | `/SPHBCS` mirror plane: too stiff and sticky (§9.6) |
| Symmetry | `/SPHBCS/SLIDE` planes on fixed frames, at cell boundaries | Quarter = half model (§9.7) | – |
| Particle–substrate interaction (Al–Al) | **open: Peter** | §9.8 | – |

### 9.2 Pitfalls found

1. **A particle mass on `/SPHCEL` silently overrides h.** With a mass on the `/SPHCEL` line, the starter sets the particle type to "mass input" and replaces the property's h by (√2 m/ρ)^(1/3) (`starter/source/elements/sph/spinih.F`, lines 88–93). The listing still prints the property's h. Give the mass only in `/PROP/TYPE34`.
2. **q = 0 means default.** As for solids, `/PROP/TYPE34` replaces q_a = 0 by 2 and q_b = 0 by 1 (`hm_read_prop34.F`); "off" needs 10⁻³⁰.
3. **Symmetry ghosts are single reflections.** One ghost per particle per plane, none across two planes, so there are no corner ghosts on the quarter model's z axis (`spsym.F`). A particle lying on a plane meets its own ghost at zero distance. Planes therefore go at cell boundaries.
4. **Two SPH parts interact through the kernel like one body.** There is no part filter in the neighbour search or in the force routine `spforcp.F`; the only interaction between SPH parts is the kernel (RG p.42: FE–SPH interaction goes through `/INTER/TYPE7`). Shown in §9.8.
5. **No internal energy for SPH** (RG: "Internal energy (IE) is not available for SPH"). The listing's energy-error column is therefore meaningless; it reads −14 % to −86 % in the elastic Hertz runs.
6. **SPH is 3D-only:** RG p.42 states it explicitly (added to §8.1).
7. Our own: `ocdeck.convert_anim` re-read old `.vtk` files when a run was repeated in the same directory; fixed.

### 9.3 Cost, measured (replaces the §8.4 estimate)

Single thread, µs per particle and cycle (engine wall-clock / (particles × cycles)):

| Case | h | µs |
|---|---|---|
| Quarter sphere, 34 332 particles, 2 symmetry planes | 1.12 s | 4.6 |
| Column, 4 symmetry planes (many ghosts) | 1.12 s | 5.4–6.1 |
| Column | 1.25 s | 7.5–8.6 |
| Column | 1.5 s | 10–11.5 |
| Column, ξ = 0.3 | 1.12 s | 10.3 (with other runs on the machine) |

Parallel, quarter sphere at s = R/32 (34 332 particles), wall-clock µs per particle and cycle:

| Workers | 1 | 4 | 8 | 16 |
|---|---|---|---|---|
| OpenMP threads (`-nt`) | 4.59 | 1.46 | 0.91 | 0.75 |
| MPI ranks | – | 1.41 | 0.89 | 0.79 |

Beyond 8 workers the gain is small: the CPU has 8 performance cores. Stable time step, elastic Al, h = 1.12 s,
scale 0.3: dt ≈ 2.15·10⁻⁵ s/m × s (2.15·10⁻¹² s at s = 0.1 µm).

**Updated estimate for the Al–Al diagnostic** (not run):
- **Model:** quarter symmetry; substrate block 3R × 3R × 2R (quarter), particle and substrate at the same spacing.
- **Particle counts:** R/16 about 7.8·10⁴ particles, R/24 about 2.6·10⁵, R/32 about 6.2·10⁵.
- **Cycles:** 2 D/V at 750 m/s is 53 ns. With dt at 0.6× the elastic value (compression stiffens and h shrinks; an assumption) that is about 6.6·10³, 9.9·10³ and 1.3·10⁴ cycles.
- **Wall-clock at 8 workers:** about 8 min, 40 min and 2 h. With scale 0.9 (if the impact rungs confirm it) a third of that.

The earlier §8.4 estimate ("about 1.8·10³ cycles, minutes per run" at R/16) used dt ≈ 3·10⁻¹¹ s. The measured
step at R/16 is 1.3·10⁻¹¹ s at scale 0.3 (4·10⁻¹¹ s at 0.9).

### 9.4 Rung S0: confined column (elastic) against the exact 1D solution

Rung-0 parameters: E = 70 GPa, ν = 0.35, ρ = 2700 kg/m³, L = 10 µm, V = 100 m/s.
- **Column:** n_z particles along z, 4 × 4 in the cross-section. Lateral motion is blocked on every particle (`/BCS`), and four `/SPHBCS/SLIDE` planes close the lateral faces, so the kernel sees an infinite slab.
- **Wall:** `/RWALL/PLANE` through the bottom particle layer; the column starts in contact.
- **Force:** the `/TH/RWALL` FNZ column is a force in 3D. It equals d(momentum)/dt to 4 digits (in 2D it was not, §5).
- **Exact:** plateau ρ c_d V, contact time 2L/c_d, rebound V.

| Particles along L | h | plateau / ρc_dV | contact / (2L/c_d) | rebound / V | cycles | engine (s, 1 thread) |
|---|---|---|---|---|---|---|
| 25 | 1.12 s | 0.9948 | 1.0112 | 0.888 | 541 | 1.3 |
| 50 | 1.12 s | 0.9955 | 1.0075 | 0.925 | 1081 | 5.2 |
| 100 | 1.12 s | 0.9956 | 1.0065 | 0.949 | 2160 | 21 |
| 200 | 1.12 s | 0.9957 | 1.0050 | 0.964 | 4319 | 75 |
| 200 | 1.25 s | 0.9919 | 1.0112 | 0.963 | 3879 | 93 |
| 200 | 1.5 s | 1.0103 | 0.9983 | **0.906** | 3313 | 108 |
| 100 | 1.5 s, q off | 0.944 | 1.107 | 0.896 | 674 | 13 |

All variants: [`results/sph_s0.csv`](opencourant/results/sph_s0.csv) (also the 0.9 time-step scale, the 8 × 8
cross-section and ξ = 0.3).

- **Plateau:** −0.43 % at every spacing, against the small-strain exact value. The 2D quads gave +0.69 % (finite strain, §3). Both are within 0.7 % of the exact value, but on opposite sides. The 1.1 % gap between them does not change with spacing, so it comes from how each formulation treats finite strain, not from resolution. It is not explained further here.
- **Contact time:** converges to the exact value from above: +1.1 % → +0.5 %.
- **Rebound:** 0.888 → 0.964, still rising (about first order; errors 11, 7.5, 5.2, 3.6 %). The quads with q ≈ 0 reach 0.991. SPH needs its artificial viscosity, which costs rebound in this purely elastic problem.
- 8 × 8 instead of 4 × 4 particles in the cross-section: identical to 3–4 digits, so the lateral planes are clean.

### 9.5 Rung S0p: elastic–perfectly-plastic two-wave case

Same column, LAW2 with Y = 100 MPa and no hardening, V = 50 m/s; closed form as rung 0p (§4). Profile of −σ_zz per
particle layer at t = 0.75 L/c_d.

| Particles | h | wall plateau / σ₂ | profile σ₂ | profile σ_HEL | plastic front / c_b | elastic front / c_d | ε_p behind wave / exact |
|---|---|---|---|---|---|---|---|
| 25 | 1.12 s | 0.991 | 0.983 | – | 0.902 | 1.100 | 0.987 |
| 50 | 1.12 s | 0.994 | 0.992 | 1.190 | 0.942 | 1.057 | 0.988 |
| 100 | 1.12 s | 0.994 | 0.993 | 1.127 | 0.965 | 1.029 | 0.986 |
| 200 | 1.12 s | 0.994 | 0.995 | 1.121 | 0.979 | 1.011 | 0.988 |
| 200 | quad, `Isolid = 17`, default q (§4) | 1.004 | 0.994 | 1.093 | 0.998 | 1.025 | 0.986 |

[`results/sph_s0p.csv`](opencourant/results/sph_s0p.csv) (also h = 1.5 s, which converges more slowly).

- **Plateau and plastic strain agree with the closed form to about 0.5–1.5 % at every spacing.** At 200 particles they match the quads with default viscosity: σ₂ 0.995 vs 0.994, ε_p 0.988 vs 0.986, rebound 0.812 vs 0.812.
- **The fronts converge to the right speeds:** plastic 0.90 → 0.98 c_b, elastic 1.10 → 1.01 c_d.
- **The elastic precursor overshoots by 12 %** (quads: 9 %), and the overshoot shrinks with spacing. It is the usual ringing at a sharp front with artificial viscosity.

![SPH S0 and S0p](opencourant/figures/sph_s0.png)

### 9.6 Rung S1: Hertz sphere, quarter symmetry

Same physics and metrics as rung 1 (§5): R = 10 µm, E = 70 GPa, ν = 0.35, ρ = 2700 kg/m³, V = 20 m/s and 2 m/s,
touching the wall at t = 0, run to 1.6 t_Hertz. Metrics: contact (end of the main pulse, F < 10⁻³ F_Hertz), peak,
max approach, rebound.
- **Contact at 10⁻² F_Hertz added:** SPH force tails (a few edge particles leaving the wall late, under 1 % of F_Hertz) move the 10⁻³ end of contact by up to 15 %.
- **Model:** quarter sphere, h = 1.12 s, default viscosity, time-step scale 0.3, frictionless `/RWALL/PLANE` on the particle nodes; force from d(momentum)/dt × 4.
- **References** (rung 1): JAX 20 × 40 at 20 m/s, 0.953 / 1.073 / 0.957 / 0.9996 (contact / peak / approach / rebound; contact at 10⁻²: 0.940); `Isolid = 17` 20 × 40, 0.956 / 1.075 / 0.958 / 0.9996. At 2 m/s (15 × 30): JAX 0.972 / 1.045 / 0.983, `Isolid = 17` 0.975 / 1.043 / 0.994.

**A plain lattice sphere fails, and gets worse with refinement.** With a cubic net the bottom of the sphere is a set
of flat terraces one spacing high. The Hertz approach at 20 m/s is 0.195 µm, which is 0.3 s at R/16 and 0.6 s at
R/32, so the load goes through the few particles on the lowest terrace (4 per full sphere by construction).

| Surface | Wall | s | contact | peak | approach | rebound |
|---|---|---|---|---|---|---|
| lattice | rigid wall | R/16 | 1.469 | 0.515 | 1.322 | 0.979 |
| lattice | rigid wall | R/32 | no end (force tail) | 0.982 | **1.888** | 0.904 |
| lattice | mirror plane | R/16 | 1.341 | 0.661 | 1.284 | 0.967 |
| lattice | mirror plane | R/32 | 1.140 | 1.095 | 1.481 | **0.521** |

The full lattice model at R/16 gives the same numbers as the half model (1.459 / 0.528 / 1.324), so the missing
corner ghosts of the quarter model are not the cause.

**With the surface particles moved onto the sphere** (§9.1), particle heights near the pole follow r²/2R, and the
contact grows continuously as Hertz assumes. Quarter sphere, rigid wall:

| V | s | particles | a_Hertz / s | d_Hertz / s | contact | contact (10⁻²) | peak | approach | rebound | engine (threads) |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 | R/16 | 4 269 | 2.2 | 0.31 | 1.107 | 0.964 | 1.193 | 1.122 | 0.925 | 29 s (4) |
| 20 | R/32 | 34 239 | 4.5 | 0.62 | 1.019 | 0.964 | 1.030 | 1.014 | 0.985 | 7 min (4) |
| 20 | R/64 | 274 126 | 8.9 | 1.25 | **0.975** | **0.964** | **1.027** | **0.986** | **0.980** | 94 min (8) |
| 2 | R/16 | 4 269 | 0.9 | 0.05 | 1.335 | 1.328 | 0.812 | 1.322 | 0.975 | 41 s (4) |
| 2 | R/32 | 34 239 | 1.8 | 0.10 | 1.133 | 1.116 | 0.928 | 1.151 | 0.985 | 16 min (4) |
| 2 | R/64 | 274 126 | 3.6 | 0.20 | 1.066 | 1.037 | 0.957 | 1.069 | 0.992 | 122 min (8) |

Run times were measured with other runs sharing the CPU (the R/64 runs overlapped each other), so they are upper
bounds. The second-finest spacing (R/32) takes 7–16 min, well under the 2 h limit. Table:
[`results/sph_s1.csv`](opencourant/results/sph_s1.csv) (all variants).

![SPH S1 Hertz](opencourant/figures/sph_s1.png)

![SPH S1 contact zone](opencourant/figures/sph_s1_contact.gif)

*Left: particle centres in the slice 0 < y < s (mirrored), pressure, s = R/32, 20 m/s; the blue ticks mark the
Hertz contact radius at maximum approach. Right: wall force against Hertz and JAX.*

At 20 m/s:
- **Contact time and approach converge toward JAX and `Isolid = 17`.** The gap to JAX halves per refinement: contact +16 %, +7 %, +2.3 %; approach +17 %, +6 %, +3.0 %.
- **The main pulse has converged:** the contact time at 10⁻² F_Hertz is 0.964 at all three spacings, 2.5 % above JAX (0.940).
- **The peak force stalls about 4 % below JAX** (1.030, 1.027 vs 1.073), close to Hertz (1.0).
- **Rebound 0.98–0.985** against 0.9996 in JAX, the cost of the artificial viscosity, as in S0.
- **The mirror-plane wall fails:** it is too stiff (contact 0.67–0.75) and sticky (rebound 0.63), because the kernel couples the sphere to its mirror image within 2h, in tension too. It is rejected as a wall. It is a preview of §9.8.
- ξ = 0.3 at R/16: peak −2.7 %, the other metrics within 0.4 %, a longer force tail.

At 2 m/s:
- **Every metric converges toward JAX and `Isolid = 17`, but slowly.** At R/64 they are still 7–10 % off: contact 1.335 → 1.133 → 1.066 (JAX 0.972), peak 0.81 → 0.93 → 0.96 (1.045), approach 1.32 → 1.15 → 1.07 (0.983).
- **The cause is resolution.** The Hertz contact radius is only 0.9, 1.8 and 3.6 spacings, and the approach 0.05–0.2 s.
- **The next spacing is out of reach.** R/128 would be about 2.2·10⁶ particles and about 16 × the R/64 cost, roughly 30 h on this machine.

**Verdict on S1: not a clean pass. Peter decides.**
- **20 m/s:** contact time and approach converge to within 2–3 % of JAX and `Isolid = 17` at R/64, and the main pulse (contact at 10⁻²) is converged at +2.5 %. The peak force stalls 4 % below JAX.
- **2 m/s:** still 7–10 % off at the finest affordable spacing.
- **What this means for cold spray:** a Hertz contact (approach ≪ spacing) is the hardest case for particle methods. In a cold-spray impact the approach is of order R, i.e. tens of spacings, so this rung is more demanding than the application. It still means SPH cannot resolve the early, elastic contact stage at affordable spacing. Hence the failure is reported here rather than worked around.

### 9.7 Quarter symmetry against a half model

Same case at R/32, 20 m/s, surface-conforming, rigid wall: quarter model (planes x = 0 and y = 0) against a half model
(plane x = 0 only, 68 478 particles).

| Model | contact | contact (10⁻²) | peak | approach | rebound |
|---|---|---|---|---|---|
| quarter | 1.019 | 0.964 | 1.030 | 1.014 | 0.985 |
| half | 0.993 | 0.971 | 1.031 | 1.012 | 0.986 |

- **The force histories lie on top of each other.** Peak, approach and rebound agree to 0.15 %.
- **The contact-time differences come from the tail only:** 2.5 % at 10⁻³ F_Hertz, 0.7 % at 10⁻².
- The quarter model has no corner ghosts on its z axis (§9.2 item 3), which is exactly where the contact is. At R/16 on the plain lattice the quarter model differs from the half and full models by 0.6 % in contact and 2.5 % in peak; the half and full models agree to 0.1 %.

**Quarter symmetry is exact for this normal impact to within about 1 % on every metric**, and to 0.15 % on peak,
approach and rebound at R/32. It halves the cost.

### 9.8 Particle–substrate interaction: why Al–Al is not started

**Test** ([`sph_twopart.py`](opencourant/scripts/sph_twopart.py),
[`results/sph_twopart.csv`](opencourant/results/sph_twopart.csv)):
- A striker column of length L (part 1, −V) hits a target column of length 2L (part 2, at rest). Same material, lateral confinement and h = 1.12 s as S0; 50 particles per L.
- **Exact 1D:** the striker stops at t = 2L/c_d and stays at rest. Between 2L/c_d and 2·(2L/c_d) the target's near end is also at rest, with zero stress at the interface. After that the near end moves away at V. The target's mean velocity is V/2 from 2L/c_d on.

| t / (2L/c_d) | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 | 3.5 | 4.0 |
|---|---|---|---|---|---|---|---|
| striker v / V, exact | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| striker v / V, SPH | −0.02 | −0.00 | −0.02 | **−0.48** | **−0.93** | −0.53 | −0.07 |
| target mean v / V, SPH (exact −0.5) | −0.49 | −0.50 | −0.49 | −0.26 | −0.04 | −0.24 | −0.47 |

**The two parts are welded.** When the target's near end starts to move away, it pulls the striker along through the
kernel; momentum goes back and forth between the parts. There is no part filter in the neighbour search or the force
routine (§9.2 item 4), so particles of different parts within 2h ≈ 2.2 s of each other act like one continuum:
- **Tension across the interface:** no separation within the kernel range.
- **Shear across the interface:** the velocity gradient is taken across both parts, so the interface is no-slip.
- **No setting changes this.** The only SPH–SPH interaction is the kernel; `/INTER/TYPE7` needs a main surface of segments, which SPH parts do not have (RG p.42: FE–SPH interaction goes through TYPE7).

**Why this stops the Al–Al diagnostic.** Jetting starts at the contact edge, from the shear and the material squeezed
out between particle and substrate. A welded, no-slip interface changes exactly that. It also builds adhesion into
every contact, which would prejudge the bonding question the diagnostic is meant to inform. This is a setting with
no defensible default, so per Peter's guidance I stop here.

**Options for Peter** (none tested beyond the above):
1. **SPH particle and SPH substrate, kernel interface as is.** It is the only all-SPH route. Results would read as "welded-interface" jetting, and only quantities before any separation would be interpretable. The weld would have to be stated with every result.
2. **SPH particle on a Lagrangian 3D brick substrate, `/INTER/TYPE7`** (SPH particles as secondary nodes). The contact separates and slides, but the substrate jet is again a Lagrangian mesh, with the distortion failure of §8 now in 3D. It would need its own rung (Hertz with TYPE7 instead of the rigid wall).
3. **`Sol2SPH` substrate:** bricks that convert to SPH particles when they distort (RG `/SPHGLO` Isol2sph, `/PROP/SOLID`). The contact is TYPE7 until conversion and a kernel weld afterwards, so it combines the problems of 1 and 2. Unverified.
4. A code change for a separable SPH–SPH contact is excluded by the no-fork decision.

## 10. Hunch CS-11: interface bracket, rungs F0 and W0, sweep (Peter's decision, 2026-11-04)

DECISIONS 2026-11-04, "SPH particle–substrate interface: bracket, bond decided afterwards" (route A + B) and "Rung S1
accepted at 20 m/s; CS-11 approved". The protocol is frozen in
[coldspray-hunch-cs11.md](coldspray-hunch-cs11.md) (commit `f08456a`, before any Al–Al run) and is followed here in
its order: F0, W0, the SPH failure check, the cost of one F run at R/16 and the 48 h rule, then the sweep. Branch
`coldspray/opencourant-sph`.

### 10.1 Setups and scripts

- [`sph_interface.py`](opencourant/scripts/sph_interface.py) writes both setups, quarter symmetry, block 3R × 3R × 2R (quarter), bottom fixed:
  - **W:** SPH sphere on an SPH block (cubic net, same spacing s, same §9.1 settings). The lowest sphere particle starts one spacing above the top block layer (the two lattices "touch").
  - **F:** SPH sphere on 8-node bricks, `/INTER/TYPE7` with the sphere's particles as secondary nodes and the block's top face as main surface, friction 0. Bricks of edge s for x, y ≤ 1.5R and z ≥ −1.5R, graded (ratio 1.2) outside. The lowest sphere particle starts at the gap height, so contact starts at t = 0.
- [`sph_f0w0.py`](opencourant/scripts/sph_f0w0.py): rungs F0 and W0 (rung-1 material and radius: E = 70 GPa, ν = 0.35, ρ = 2700 kg/m³, R = 10 µm, 20 m/s). Reference: two-body Hertz, E* = E / (2 (1 − ν²)), t_Hertz = 37.8 ns, d_Hertz = 0.257 µm (0.41 s at R/16, 0.82 s at R/32), contact radius a = 1.60 µm. Force = −d(ZMOM)/dt of the sphere × 4; approach from the integrated centre-of-mass velocity.
- [`cs11_sweep.py`](opencourant/scripts/cs11_sweep.py): the Al–Al sweep (§10.5).
- Results: [`results/cs11_f0w0.csv`](opencourant/results/cs11_f0w0.csv).

### 10.2 Rung F0 (SPH sphere on TYPE7 bricks): passes; element, gap and stiffness frozen

| run | element | gap | Stfac | peak / F_H | approach / d_H | contact (1 %) / t_H | rebound / V | engine |
|---|---|---|---|---|---|---|---|---|
| R/16 | `Isolid = 17` | s/2 | 1 | 0.981 | 1.081 | 1.074 | 0.942 | 3.5 min, 3 threads |
| R/16 | `Isolid = 17` | s/2 | 10 | 1.039 | 1.025 | 1.017 | 0.940 | 3.9 min, 3 threads |
| R/16 | `Isolid = 17` | s/10 | 10 | 1.038 | 1.024 | 1.015 | 0.939 | 3.1 min, 3 threads |
| **R/32** | `Isolid = 17` | **s/2** | **10** | **1.037** | **0.987** | 0.956 | **0.992** | 24 min, 8 threads |

**Pass** (frozen thresholds: at R/32 peak and approach within 5 % of Hertz, rebound > 0.9 V). R/32: 34 239
particles, 198 000 bricks, 10 052 cycles.

**Frozen for setup F:**
- **Element `Isolid = 17`** (H8C, 2 × 2 × 2 Gauss points, constant-pressure default `Icpre = 1`), the formulation verified in 2D (§5), default bulk viscosity (1.10, 0.05), `Ismstr` default. `Isolid = 24` (HEPH) and `Isolid = 1` (Belytschko) were started at R/16 and stopped: with either, the engine runs at a nodal time step of 4.3·10⁻¹³ s set by the brick node on the impact axis, 30× below the SPH time step and independent of the contact stiffness. With `Isolid = 17` the step stays at the SPH value (1.3·10⁻¹¹ s at R/16). The cause was not traced.
- **Gap s/2** (constant, `Igap = 1000`): the particle's surface is s/2 outside its centre, so first contact is where the SPH surface meets the brick face. s/10 gives the same metrics to 0.1 % (approach is measured from first contact), so the choice does not matter for the rung. The starter warns that s/2 exceeds half the smallest main edge; that warning is about self-contact and does not apply.
- **Stiffness `Istf = 1000`, Stfac = 10** (penalty stiffness 10 × B A²/V of the main brick, i.e. 10 B s per particle). With Stfac = 1 the penalty compliance adds 8 % to the approach at R/16 (estimate: penetration ≈ p₀ s / B ≈ 0.05 s against d_H = 0.41 s), at Stfac = 10 it adds under 1 %. The time step drops by 15 % at R/32 (contact nodal step 5.9·10⁻¹² s against 6.7·10⁻¹² s SPH).
- Other TYPE7 fields at their defaults (no friction, `Inacti` none, `VIS_S` = 0.05 critical damping of the penalty).

### 10.3 Rung W0 (SPH sphere on SPH block, welded): fails

| run | start distance (lowest particle to top layer) | peak / F_H | t_peak / t_H | approach / d_H | rebound / V at 0.8 t_H | engine |
|---|---|---|---|---|---|---|
| R/16 | s (lattices touch) | 1.372 | 0.30 | 0.575 | 0.66 | 7.2 min, 4 threads |
| **R/32** | s (lattices touch) | **1.191** | 0.38 | **0.678** | 0.90 | 71 min, 8 threads |
| R/16, diagnostic | 2.4 s (outside the kernel support 2h = 2.24 s) | 0.94 | — | stops 0.45 d_H short of lattice contact | 0.92 | 24 min, 4 threads |

**Fail** (frozen threshold: at R/32 peak and approach within 5 % of two-body Hertz). The sphere meets a contact that
is too stiff and too wide: the force rises from t = 0 and peaks early, 37 % (R/16) and 19 % (R/32) above Hertz, and
the approach reaches only 0.58 and 0.68 of d_H. Both move toward Hertz with refinement, but slowly: the peak excess
falls from 0.37 to 0.19 (about ∝ s), the approach deficit only from 0.43 to 0.32 (about ∝ s^0.4). Extrapolated, the
peak would enter the 5 % band near R/130 and the approach only near R/3000. Neither is reachable: R/32 already has
624 000 particles and takes 71 min for the loading phase alone, and the particle count grows as n_r³.

**Why, and why it is not just a slow rung:**
- Particles of the two bodies interact as soon as they are within the kernel support 2h ≈ 2.24 s, and with continuity density any approach inside that range builds pressure. At t = 0 every sphere particle whose height above the top layer is under about 1.2 s is already inside the support, so the initial contact is a disc of radius about √(2.5 R s) (0.39 R at R/16, 0.28 R at R/32), wider than the Hertz contact radius at peak (0.16 R).
- **The result depends on where the sphere starts.** Started outside the kernel support (diagnostic row), the sphere is stopped through the kernel tails before the two lattices ever reach their touching distance, and bounces off at 0.92 V; the peak force falls from 1.37 to 0.94. A welded SPH–SPH contact therefore has no defined first-contact geometry at these spacings: its stiffness is set by the particle arrangement within 2h, not by the contact mechanics.
- After the peak the force turns negative (tension; panel a), as expected from the weld (§9.8).

![CS-11 rungs F0 and W0](opencourant/figures/cs11_f0w0.png)

**Per the protocol, setup W stops here and goes to Peter.** No W Al–Al run was made.

### 10.4 SPH material failure: are failed particles deleted? (for the oxide-interphase option)

- **Reference Guide:** the only statement is in the failure-model compatibility table, `/FAIL` comment 4 (RG p.1303): "Failure models can be used for SPH simulation for all materials compatible with SPH formulation." The RG does not say what happens to a failed particle. The only explicit SPH deletion in the RG is the time-step option `/DT/SPHCEL/DEL` (p.3036): "The SPH cell which is controlling the time step is removed".
- **Source (OpenCourant engine, `elements/sph/spmall3.F`, `sphprep.F`):** when the failure model sets a particle's `OFF` flag to 0, `spmall3.F` sets `KXSP(2,I) = 0` and requests a new neighbour search (`ISPHBUC = 1`) and a contact update (`IDEL7NOK = 1`). `sphprep.F` puts only particles with `KXSP(2,N) ≠ 0` into the neighbour sort. **A failed particle is therefore taken out of the kernel interaction**: it neither gives nor receives SPH forces. Its node is not removed (no code path deletes the node or its mass was found), so it keeps its mass and moves freely; whether it stays a TYPE7 secondary node was not traced.
- **For option C (oxide interphase):** a layer of interphase particles with a failure model would, on failure, drop out of the kernel coupling, so the weld between particle and substrate opens where the interphase has failed. That is the behaviour the option needs. It is not yet verified by a run, and the free nodes of failed particles carry mass and momentum through the gap.

### 10.5 Cost of one F impact at R/16, budget, and the sweep

**Run** ([`cs11_sweep.py`](opencourant/scripts/cs11_sweep.py), results
[`results/cs11_sweep.csv`](opencourant/results/cs11_sweep.csv)): Al LAW4 Johnson–Cook + `/EOS/GRUNEISEN`
(P-HG-Al, γ₀ = 2.17, as in §8.3), no failure, no erosion; R = 7.5 µm; to t_e = 0.25 D/V. The time-step collapse
limit is dt_min = dt₀/50 (dt₀ = 2.15·10⁻⁵ s/m × s, §9.3), as in §8.3; OpenCourant then stops the run. J and J_s come
from `/TH/NODE` (X, Y, VX, VY) of every particle node and of the substrate nodes with z ≥ −R/2 and r ≤ 2R, sampled
every t_e/100.

**Cost and the 48 h rule.** The first F run (R/16, 400 m/s, 4 269 particles and 31 581 bricks) took **35 s of engine
time on 8 threads** for 1 416 cycles (5.5 µs × threads per particle-or-brick cycle). It stopped at 0.17 D/V; run to
t_e it would take about 52 s. Projected protocol total, with every run reaching t_e: F at R/16 about 15 min, W at
R/16 about 35 min, R/24 about 1 h for both setups, R/32 about 1 h (F) and 4 h (W). That is **about 6.5 h, well
under 48 h**, so the sweep goes ahead.

**F coarse sweep, R/16, 400–1200 m/s in steps of 50** (17 runs, all evaluable):

| V (m/s) | 400 | 500 | 600 | 700 | 800 | 900 | 1000 | 1100 | 1200 |
|---|---|---|---|---|---|---|---|---|---|
| J (particle) | 0.80 | 0.84 | 0.86 | 0.95 | 1.02 | 1.06 | 1.06 | 1.01 | 0.96 |
| J_s (substrate, no verdict) | 1.43 | 1.71 | 1.76 | 1.87 | 2.00 | 2.14 | 2.23 | 2.28 | 2.28 |
| run stop / (D/V) | 0.170 | 0.145 | 0.128 | 0.123 | 0.115 | 0.115 | 0.118 | 0.120 | 0.123 |

(Every 50 m/s step is in the CSV; the steps between the columns lie between their neighbours, J ≤ 1.06 throughout.)

- **Every F run stops before t_e** on the time-step collapse, at 0.115–0.17 D/V. The controlling bricks are in the top layer at the contact edge (at 400 m/s: bricks 4118 and 8758, centroids at r = 0.66 R, z = −s/2), so this is the §8.3 failure in 3D. All 17 runs pass 0.1 D/V, so they are evaluated up to the stop.
- **J never reaches J\* = 1.5**; its largest value is 1.06 (900–1000 m/s). It also stays below the sensitivity values 1.25 and 2.0. The maximum comes at 0.28–0.37 t_e (0.07–0.09 D/V), before the stop, and J falls afterwards (GIF below), so the truncation did not cut a rising J at R/16.
- **The substrate metric J_s passes 1.5 at about 425 m/s** and 2.0 at about 750 m/s (linear interpolation). It is reported without a verdict.

**Refinement: no velocities defined, and F cannot be refined.** The frozen protocol refines around the R/16
crossing, and F has none. To see whether F could be refined at all, three velocities (500, 800, 1100 m/s) were run
at R/24 and R/32. **This is a diagnostic outside the protocol**, labelled so in the CSV, and it carries no verdict:

| s | V (m/s) | run stop / (D/V) | evaluable | J | J_s |
|---|---|---|---|---|---|
| R/16 | 500 / 800 / 1100 | 0.145 / 0.115 / 0.120 | yes / yes / yes | 0.84 / 1.02 / 1.01 | 1.71 / 2.00 / 2.28 |
| R/24 | 500 / 800 / 1100 | 0.113 / 0.085 / 0.093 | yes / **no** / **no** | 0.96 / 1.24 / 1.48 | 1.94 / 2.34 / 2.54 |
| R/32 | 500 / 800 / 1100 | 0.090 / 0.068 / 0.070 | **no / no / no** | 1.02 / 1.48 / 1.68 | 2.15 / 2.43 / 2.26 |

- **The brick substrate fails earlier as the spacing is refined**, as in 2D (§8.3). At R/32 every run stops before 0.1 D/V, so **setup F is unevaluable at the spacing where CS-11 takes Δ**.
- J grows with refinement at every speed (at 800 m/s: 1.02, 1.24, 1.48). It is read off a mesh that is collapsing at the contact edge, so it is not converged, and at R/24 and R/32 it is also cut off earlier.
- Run times: R/24 30–83 s and R/32 77–214 s of engine time on 8 threads (all stopped early).

![CS-11 setup F: J(V) and run stop](opencourant/figures/cs11_sweep_F.png)

![Setup F, R/16, 800 m/s](opencourant/figures/cs11_F16_800.gif)

*Setup F, s = R/16, 800 m/s, to the run stop at 0.115 D/V. Left: particle centres in the slice 0 ≤ y < s (mirrored),
coloured by u_r/V, over the deformed brick grid in the plane y = 0. Right: J(t) and J_s(t). The particle's
outward speed peaks at about 0.09 D/V and falls; the substrate's keeps rising until the edge bricks collapse.*

### 10.6 Outcome for CS-11 and what goes to Peter

**CS-11 is inconclusive under its frozen rules.** Each of these is enough on its own:
1. **W:** the prerequisite rung W0 fails (§10.3), so the W sweep is not run and v_on(W) is undetermined.
2. **F:** J does not cross J\* = 1.5 anywhere in 400–1200 m/s at R/16 (nor 1.25 or 2.0), so v_on(F) is undetermined ("no crossing: inconclusive, recorded"). F also cannot be refined: at R/32 every run is unevaluable (brick collapse before 0.1 D/V, §10.5), so the convergence rule could not be met even with a crossing.

Δ = |v_on(W) − v_on(F)| is therefore not determined, and the bracket width cannot be compared with the measured oxide
effects. The author's prediction (refuted, with v_on(W) > v_on(F)) is untested. The hunch file stays as frozen; the
result is recorded here.

**What the rungs and runs show (facts, no verdict):**
- **Neither bound of the bracket can be simulated to convergence with OpenCourant's existing interface options.** The welded bound (SPH on SPH) has no defined contact at reachable spacings: its stiffness comes from the particle arrangement within the kernel support (§10.3). The frictionless bound (SPH on TYPE7 bricks) passes its elastic rung, but in the Al–Al impact the contact-edge bricks collapse at 0.07–0.17 D/V, earlier as the spacing is refined: the §8.3 result, now in 3D.
- In F at R/16, the particle's outward speed peaks at about 0.09 D/V and then falls, while the substrate's keeps rising until the run stops (J_s up to 2.3). This is mesh-dependent (R/24, R/32 diagnostic) and carries no verdict.
- SPH material failure removes a failed particle from the kernel interaction (§10.4), so the oxide-interphase option C can open a weld. But it would sit inside the welded SPH–SPH contact that W0 just failed, so it would need its own contact rung first.

**Decisions for Peter:**
1. Accept CS-11 as inconclusive (both setups not evaluable), recorded here.
2. Whether any OpenCourant interface route is left without a fork. The candidates seen so far all carry a known problem: brick erosion at the contact edge (excluded by CS-11's "no erosion"); `Sol2SPH`, where bricks convert to SPH particles and the interface becomes the kernel weld again; and option C, which inherits W0's contact problem. Or the interface question moves to a route outside OpenCourant.

## 11. Hunch CS-13: heat conduction at the contact edge; rung H0 fails (Peter's decision, 2026-11-05)

DECISIONS 2026-11-05: CS-11 closed as inconclusive; CS-12 and CS-13 approved and frozen. Protocol:
[coldspray-hunch-cs13.md](coldspray-hunch-cs13.md). Order followed: source k, add it to the deck, rung H0, then
(only if H0 passes) the §8.3 diagnostic with conduction. **H0 fails, so no impact run was made.** This goes to
Peter; the JAX fallback is his decision.

### 11.1 Thermal conductivity, sourced

- **Pure Al: k = 237 W/(m K)**, `properties.csv` row P-HG-Al, new column `k_W_mK`. Source: HG2018a preprint (arXiv 1612.08081), Extended Data Table 1, row "Conductivity (W/m K)", printed, a simulation input of that paper (the table cites its refs 31–34). **Condition:** no temperature is printed with it. The same table gives the ρ, c_p and Johnson–Cook values already used (P-HG-Al), so κ = k/(ρ c_p) = 9.79·10⁻⁵ m²/s is internally consistent with the §8.3 deck.
- **Al 6061: not sourced.** HG2018a covers pure Al only; nothing was filled from memory (noted under "Still missing" in the data README).
- **In the deck:** `/HEAT/MAT` with ρc_p = 2700 × 896.9 J/(m³ K) and AS = 237 W/(m K), BS = 0, engine `/THERMAL` ([`h0_conduction.py`](opencourant/scripts/h0_conduction.py)). The impact deck (`option1_alal.py`) is unchanged, because H0 failed.

### 11.2 Rung H0: conduction alone against erfc

**Case** ([`h0_conduction.py`](opencourant/scripts/h0_conduction.py), [`results/cs13_h0.csv`](opencourant/results/cs13_h0.csv)):
- Bar 0 ≤ z ≤ 20 µm, one element across, all nodes fixed.
- Initial nodal temperature 393 K for z < L/2 and 293 K for z > L/2 (`/INITEMP`); the node at L/2 gets the mean.
- Al LAW4 + Grüneisen + `/HEAT/MAT` as above, run to 10 ns, where √(κt) = 0.97 µm, far from the ends.
- Exact: T = T0 + (T1 − T0)/2 · erfc((z − L/2) / (2√(κt))).
- Output: `/TH/NODE TEMP` along one edge, plus `/ANIM/NODA/TEMP` and `/ANIM/ELEM/TEMP`.
- Metric: max |T − T_exact| / (T1 − T0) over the nodes.

| element | h = 0.625 µm | h = 0.3125 µm | h = 0.156 µm (finest) | temperature written out | max change of T over the run |
|---|---|---|---|---|---|
| **axisymmetric `/QUAD`, `Isolid = 17`** (the CS-13 element) | 0.323 | 0.409 | **0.454** | yes (nodal TEMP) | **0.0 K** |
| axisymmetric `/QUAD`, `Isolid = 0` (diagnostic) | 0.323 | — | — | yes | 0.0 K |
| 3D `/BRICK`, `Isolid = 17` (control) | 0.0028 | 0.00068 | 0.00017 | yes | 45 K |

**H0 fails** (frozen threshold: within 2 % at the finest spacing). On axisymmetric quads the temperature is now
written out: the nodal temperature from `/INITEMP` comes through `/TH/NODE TEMP`, so that part of the old open item
is solved, but only because the field is nodal. **It never changes:** no heat is conducted, with either quad
formulation. The error grows with refinement only because a sharp step deviates more from a resolved erfc. The
same deck on 3D bricks matches erfc to 0.28 % at the coarsest spacing and converges at second order. So the deck,
the card and the sourced k are right, and the gap is the 2D element.

![CS-13 rung H0](opencourant/figures/cs13_h0.png)

**Why (documentation and source):**
- RG `/THERMAL` (engine), comment 2: "Works for thermal analysis with solid, shell and sph elements." 2D quads are not listed. The engine prints "FINITE ELEMENT THERMAL ANALYSIS" and, in the earlier J4/J5 runs, "TEMPERATURE (SOLID ONLY)".
- Source: the brick force routine `elements/solid/solide/sforc3.F` calls the finite-element conduction routine `STHERM` when thermal analysis is on (`JTHE < 0`). The quad force routines `qforc2.F` (`Isolid = 0`) and `q4forc2.F` (`Isolid = 17`) call no conduction routine, and the source tree has conduction routines for solids (8-, 4-, 10-, 20-node), thick shells, shells and SPH, but none for quads. The only 2D heat path is the ALE finite-volume one (`ale/atherm.F`, RG `/HEAT/MAT` Iform = 0), and with ALE the starter replaces `Isolid = 17` by the area-weighted quad that fails the Hertz rung (§5.4).
- This also explains the 2026-11-03 result "`/HEAT/MAT` gives T ≈ 0 on quads" (§2, runs J2–J6): with `/HEAT/MAT` the temperature becomes a nodal field that nothing in 2D updates (T₀ from `/HEAT/MAT` was not applied either; `/INITEMP` is). The other old item, LAW4's element temperature not written out with `Isolid = 17` (§5.3), is not fixed by this. It does not matter for conduction, which in 2D is absent anyway.

### 11.3 What goes to Peter

- **CS-13 cannot be tested with OpenCourant in 2D.** The prerequisite rung fails because 2D quads have no heat conduction at all, not because of an accuracy problem. By the protocol this goes to Peter before any impact run.
- **Options** (for Peter; none run here):
  1. **The JAX 2D-axisymmetric code**, the fallback named in CS-13 and DECISIONS 2026-11-04. It would need conduction added and its own H0.
  2. **OpenCourant 3D bricks**, where conduction works (H0 control above). The CS-13 test is specified as the §8.3 2D runs, so this would be a protocol change. A 3D quarter model at R/64 is far more expensive: §10.5 shows the 3D brick edge failing in the same way.
- The sourced k and the H0 deck are ready for either route.

## 12. Hunch CS-13b: 3D setup F with conduction; rung H0-SPH fails, and the conductive runs are blocked (task 2026-11-05-a)

Task: [tasks/wsl-a.md](tasks/wsl-a.md), task 2026-11-05-a. Protocol:
[coldspray-hunch-cs13b.md](coldspray-hunch-cs13b.md), frozen in `9a36aae`. Order followed: rung H0-SPH, then the
24 runs. **H0-SPH fails narrowly (2.5 % against 2 %), so the particle has to stay adiabatic. OpenCourant cannot run
that mix: setup F with conduction in the bricks and an adiabatic SPH particle either exhausts memory or overheats
the particle far beyond what the impact's energy allows. None of the 24 runs was made.** This is an impossible step
under the frozen protocol, so it goes to Peter.

### 12.1 Rung H0-SPH: conduction in SPH particles against erfc

**Case** ([`h0_sph.py`](opencourant/scripts/h0_sph.py), [`results/cs13b_h0_sph.csv`](opencourant/results/cs13b_h0_sph.csv)):
- The H0 slab of §11.2 (L = 20 µm, 393 K | 293 K step at L/2, k = 237 W/(m K), to 10 ns) as SPH particles: a cubic net of spacing s in a column 12 s × 12 s, §9.1 settings (h = 2^(1/6) s, dt scale 0.3), every particle fixed, no symmetry planes.
- Measured on the particle column nearest the axis, 6 s from the free sides. Output: `/TH/NODE TEMP`, `/ANIM/NODA/TEMP`, `/ANIM/ELEM/TEMP`.
- **The step is set as two SPH parts with different `/HEAT/MAT` T0.** With thermal analysis on, the starter sets every SPH particle's temperature to its `/HEAT/MAT` T0 and ignores `/INITEMP` (starter `spinit3.F`, "INITIALISATION OF THERMAL BEHAVIOR"; a first run with `/INITEMP` stayed at 293 K everywhere). Both parts are the same material, and the SPH conduction loop (engine `sptemp.F`) has no part filter, so they conduct as one body.

| s | 0.625 µm | 0.3125 µm | 0.156 µm (finest) |
|---|---|---|---|
| max \|T − T_exact\| / ΔT | 0.129 | 0.052 | **0.025** |
| κ fitted to the profile / κ | 0.83 | 0.95 | 0.97 |
| engine (8 threads) | 4 s | 17 s | 68 s |

**H0-SPH fails** (frozen threshold: within 2 % at the finest spacing; the temperature is written out). The error
converges at first order and comes from too low an effective diffusivity, which approaches κ with refinement. Neighbouring particles pair up in
temperature (e.g. 352.2 / 352.8, 333.2 / 333.8 K at 0.31 µm), the mark of the wide two-pass Laplacian (`sptemp.F`
computes a gradient first, then its divergence). By the protocol, the particle stays adiabatic and the test goes ahead.

### 12.2 Setup F with conductive bricks and an adiabatic particle: not runnable

Probe at R/16, 800 m/s ([`cs13b_probe.py`](opencourant/scripts/cs13b_probe.py),
[`results/cs13b_probe.csv`](opencourant/results/cs13b_probe.csv)). It sits outside the 24 runs and is a
**diagnostic**:

| variant | particle `/HEAT/MAT` | stop / (D/V) | stop element | particle T max | particle T median / 99 % | particles > T_melt (933 K) | particle ε_p max | brick T max | brick ε_p max |
|---|---|---|---|---|---|---|---|---|---|
| adiabatic (no `/THERMAL`) | — | 0.1150 | brick (3161, 8729) | 392 K | 295 / 364 K | 0 of 4269 | 0.52 | 737 K | 1.34 |
| bricks k = 237, particle k = 0 | T0 293 K, k 0, EFRAC 1 | 0.1132 | brick (3161, 8729) | **89 909 K** | 406 / 48 897 K | **1161** | 0.13 | 534 K | 1.31 |
| as above, particle EFRAC = 0 | T0 293 K, k 0, EFRAC 0 | 0.1132 | brick (3161, 8729) | 89 909 K | identical | 1161 | 0.13 | 534 K | 1.31 |
| bricks k = 237, **no** particle `/HEAT/MAT` (the protocol as written) | — | — | — | engine passes 15 GB within seconds; the kernel OOM-kills it and the WSL VM goes down (three times, 10:15–10:19 CET; bisected under a memory cap in a separate session) | | | | | |

- **The protocol as written cannot run.** With `/THERMAL`, `/HEAT/MAT` on the bricks and none on the SPH material, the engine's memory runs away. Adding `/HEAT/MAT` to the particle, or removing it from the bricks, makes it run (≈ 400 MB).
- **With a particle `/HEAT/MAT`, the particle's temperature is non-physical.** The whole kinetic energy at 800 m/s, 320 kJ/kg, heats Al by at most 357 K. The particle instead reaches 9·10⁴ K, and a quarter of its particles pass the melting point by 2.1 ns, starting at the impact axis. k = 0 does not help (no conduction), and neither does EFRAC = 0 (the result is bit-identical, so the SPH heat source ignores EFRAC). Above T_melt the Johnson–Cook flow stress vanishes, so the particle's mechanics change: its peak ε_p drops from 0.52 to 0.13.
- **The heating path also changes in the bricks.** Adiabatic LAW4 takes T from the element internal energy (RG LAW2/LAW4 comment 11). With `/HEAT/MAT`, T is nodal and heated by the strain energy, and the brick peak falls from 737 K to 534 K in the conductive run. A conductive-minus-adiabatic difference would therefore mix conduction with a change of heat source. A brick k = 0 twin would separate the two, but it is not run here because the particle problem comes first.
- **The stop element is a brick in every variant** (the same two elements, 3161 and 8729), and the stop time moves by only 1.6 %. So the particle artifact does not reach the stop at R/16, but it changes the particle that loads the edge.

### 12.3 Outcome and what goes to Peter

**Status of CS-13b: blocked before its runs; no verdict.** Rung H0-SPH fails (2.5 %), and the setup the protocol then
prescribes (conductive bricks, adiabatic particle) either crashes or corrupts the particle. The frozen verdict rule
needs the 24 runs, so it was not applied.

**Options** (for Peter; none run here):
1. **Particle with `/HEAT/MAT` (k = 0), as is.** This runs, but the particle melts by an artifact, so the adiabatic twin is no longer the same particle, and the twin control in the verdict rule stops meaning "conduction made the difference". Not recommended.
2. **Rigid or elastic particle.** Any particle material whose mechanics do not depend on T (e.g. LAW1 elastic with `/HEAT/MAT`, k = 0) would remove the artifact from the loading side. This is a protocol change, because the edge failure would then come from a different impactor.
3. **Brick particle instead of SPH.** Conduction works on bricks (§11.2 control), and with TYPE7 between two brick bodies both sides use one consistent heat path. This is also a protocol change, and it reintroduces the particle-side brick collapse that SPH was chosen to avoid (§8.3).
4. **JAX route** (CS-13's original 2D protocol, with conduction added and its own H0), as already named in CS-13.

**Safety change in the scripts:** every engine and starter run through `sphdeck.run` now runs under a
virtual-memory cap, with core dumps off and a hard time limit, so a runaway run is killed instead of the WSL VM.
