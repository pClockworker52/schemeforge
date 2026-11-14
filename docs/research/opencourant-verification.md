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
| CS-13c (task 2026-11-05-b) | **Refuted** by both clauses of the frozen rule. Brick particle on brick substrate, both bodies conductive (k = 237) against a k = 0 twin. Rungs B0 (frozen gap s/10, Stfac 1) and H0-k0 pass; check E passes in all 51 runs. t_f still falls 22–37 % from R/32 to R/48 and edge ε_p rises 35–66 %; the twins agree within 3.5 %. The particle side fails first in every run. A first campaign with `/HEAT/MAT` T1 = 0 (softening off) was discarded. §13 |
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
- **Correction (2026-11-05, §13.2):** the heat-card runs of this table had `/HEAT/MAT` T1 = 0, which OpenCourant reads as T_melt = 10²⁰ and which switches the Johnson–Cook thermal softening off. The brick comparison in the next point (737 K against 534 K) therefore also mixes in the lost softening. The particle overheating does not depend on it: it appears with any k and EFRAC, and from the first steps on.
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

## 13. Hunch CS-13c: brick particle on brick substrate with conduction; CS-13c refuted (task 2026-11-05-b)

Task: [tasks/wsl-a.md](tasks/wsl-a.md), task 2026-11-05-b. Protocol: [coldspray-hunch-cs13c.md](coldspray-hunch-cs13c.md),
frozen in `15fe42f`. Order followed: rung B0, rung H0-k0, the plastic-work output check, the 24 runs plus three runs
without `/HEAT/MAT`, then P1–P3 and the verdict rule. **Both rungs pass and check E passes in every run. The verdict
rule gives "refuted", by both of its clauses.** One full campaign had to be discarded because of a deck error of
mine (§13.2); the verdict comes from the corrected rerun.

### 13.1 Setup and prerequisite rungs

**Setup B** ([`brick_particle.py`](opencourant/scripts/brick_particle.py)):
- **Particle:** quarter O-grid sphere of 8-node bricks (`Isolid = 17`): a rounded cube core (half-size 0.5 R) and mapped shells, equiangular along the surface. At the contact pole the surface cells are s × s and the radial edge is about s. The mesh volume is within 0.06 % of the sphere's at R/16; there are no inverted elements, and the largest aspect ratio is 2.4.
- **Substrate:** the setup-F brick block (`sph_interface.brick_block`).
- **Contacts:** two `/INTER/TYPE7`, friction 0, `Istf = 1000`, `Igap = 1000`, no heat transfer. One has the particle nodes as secondary on the substrate top; the other has the substrate top nodes as secondary on the particle surface. The lowest particle node starts at the gap, so contact starts at t = 0.
- **Element counts:** at R/16, 18 522 particle and 31 581 substrate bricks; at R/48, 476 656 and 599 076.

**Rung B0 (elastic, 20 m/s, two-body Hertz; the brick analogue of F0)** ([`b0_rung.py`](opencourant/scripts/b0_rung.py),
[`results/cs13c_b0.csv`](opencourant/results/cs13c_b0.csv)). Rung-1 material and radius, as F0 (R = 10 µm,
E = 70 GPa, ν = 0.35):

| run | gap | Stfac | peak / F_H | approach / d_H | contact (1 %) / t_H | rebound / V | engine (8 threads) |
|---|---|---|---|---|---|---|---|
| R/16 | s/10 | 10 | 1.051 | 0.965 | 0.947 | 0.999 | 4 min |
| R/16 | s/10 | 1 | 1.040 | 0.985 | 0.964 | 0.999 | 4 min |
| **R/32** | **s/10** | **1** | **1.046** | **0.976** | 0.957 | **1.000** | 54 min |

**B0 passes** (frozen: at R/32 peak and approach within 5 %, rebound > 0.9 V). **Frozen: gap s/10, Stfac 1.** With two
contacts the penalty acts twice, so Stfac 1 already gives an approach within 2.4 %. Stfac 10 stiffens the peak.
The peak's 4.6 % excess at R/32 is close to the limit and did not decrease from R/16, so it is a mesh-level
offset, not converging toward Hertz. The "energy error" column of the listing dips to −99.9 % at peak compression
and returns to −0.1 %, because it leaves out the energy stored in the contact springs.

**Rung H0-k0** ([`h0_conduction.py`](opencourant/scripts/h0_conduction.py) with `K_W_MK=0`,
[`results/cs13c_h0_k0.csv`](opencourant/results/cs13c_h0_k0.csv)): the §11.2 brick slab with `/HEAT/MAT`, k = 0. The
largest temperature change over the run is **0.0 K** at all three spacings (limit 0.1 K): **passes**. The k = 237 control
reproduces §11.2 (0.017 % at 0.156 µm). (A first attempt showed changes of 12–44 K; the cause was a variable in the
deck writer shadowing the conductivity argument, so the deck carried k = 128. Fixed before the result above.)

**Per-element plastic work:** OpenCourant writes it for solids (`/ANIM/ELEM/WPLA`, engine `anim_dcod_key_0.F`; in the
VTK output as a per-element field). So **the second clause of check E is binding**, not only reported.

### 13.2 A discarded campaign: thermal softening was off (deck error)

The first full campaign (27 + 24 runs, 15:19–18:45) gave **bit-for-bit identical** t_f and P2 for the two twins at
every velocity and spacing, while their edge temperatures differed by up to 60 K. Cause: I left the `/HEAT/MAT`
field T1 at 0. With `/HEAT/MAT` the Johnson–Cook softening uses T* = (T − T_ref)/(T1 − T_ref) (engine `mmain.F90`;
LAW4's own T_melt is used only for the melt cut-off), and the starter reads T1 = 0 as T_melt = 10²⁰. So T* ≈ 0, and
the flow stress never saw the temperature. That run set would have met the "twins agree" refutation clause without
testing anything, so it is **discarded**, not counted (kept outside the repository). Fix: **T1 = T_melt = 933 K**
(P-HG-Al, the value LAW4 already has); the starter now echoes 933 K. Check at R/16, 800 m/s: the twins now differ
(t_f 0.1081 against 0.1085 D/V), and t_f moved from 0.113 to 0.108 D/V, close to the run without `/HEAT/MAT`
(0.106). The protocol does not name T1; setting it to the material's melting point is the input the frozen
material implies, so this is a deck fix, not a protocol change.

### 13.3 Runs and metrics

[`cs13c.py`](opencourant/scripts/cs13c.py), driver [`cs13c_all.sh`](opencourant/scripts/cs13c_all.sh), results
[`results/cs13c_pass1.csv`](opencourant/results/cs13c_pass1.csv) (to the stop: P1, stop element, check E) and
[`results/cs13c_pass2.csv`](opencourant/results/cs13c_pass2.csv) (rerun of the same deck to t_c: P2, P3). Implementation
of the frozen definitions:
- **dt₀** is the deck's own cycle-0 time step, from a one-cycle pre-run at each spacing. The run stops below dt₀/50.
- **Check E:** E1 is Σ m_node c_p (T − T₀) over both bodies (nodal mass ρV₀/8 per brick corner) against 1.05 × the particle's initial kinetic energy. E2 compares each element above 933 K with 1.10 × its plastic work.
- **P2:** a body's contact edge is its outermost surface node within 2 × gap of the other body's surface. P2 is that body's maximum ε_p over elements with centroid within 1.17 µm of that node.

Cost: R/48 runs took 6.8–31 min of engine time on 8 threads (largest: 500 m/s), so the 1 h budget stop did not trigger. Pass 1 took 2 h 20 min, pass 2 52 min.

**P1, failure time t_f / (D/V)** (every run stopped on the time-step collapse before t_e; the controlling element was
**a particle brick in all 27 runs**):

| V (m/s) | twin | R/16 | R/24 | R/32 | R/48 | R/32 → R/48 |
|---|---|---|---|---|---|---|
| 500 | k = 237 | 0.1599 | 0.1242 | 0.0963 | 0.0609 | −36.8 % |
| 500 | k = 0 | 0.1551 | 0.1214 | 0.0939 | 0.0630 | −32.8 % |
| 500 | no `/HEAT/MAT` (reported only) | 0.1483 | | | | |
| 800 | k = 237 | 0.1085 | 0.0807 | 0.0526 | 0.0378 | −28.1 % |
| 800 | k = 0 | 0.1081 | 0.0804 | 0.0526 | 0.0376 | −28.6 % |
| 800 | no `/HEAT/MAT` | 0.1058 | | | | |
| 1100 | k = 237 | 0.0877 | 0.0754 | 0.0549 | 0.0429 | −21.9 % |
| 1100 | k = 0 | 0.0871 | 0.0751 | 0.0546 | 0.0428 | −21.6 % |
| 1100 | no `/HEAT/MAT` | 0.0839 | | | | |

**P2, edge plastic strain at t_c** (t_c = 0.5 × the smallest t_f at that velocity: 0.913 / 0.352 / 0.292 ns; the edges
sit at 0.39 R, 0.29 R and 0.30 R in both bodies):

| V (m/s) | body | k = 237: R/16 / R/24 / R/32 / R/48 | R/32 → R/48 (k = 237 / k = 0) |
|---|---|---|---|
| 500 | particle | 0.395 / 0.606 / 0.806 / 1.115 | +38.3 % / +38.7 % |
| 500 | substrate | 0.187 / 0.280 / 0.381 / 0.542 | +42.3 % / +41.9 % |
| 800 | particle | 0.132 / 0.217 / 0.276 / 0.436 | +57.7 % / +57.7 % |
| 800 | substrate | 0.115 / 0.128 / 0.152 / 0.251 | +65.6 % / +65.6 % |
| 1100 | particle | 0.131 / 0.214 / 0.244 / 0.373 | +52.7 % / +52.7 % |
| 1100 | substrate | 0.115 / 0.134 / 0.165 / 0.223 | +35.1 % / +35.1 % |

The k = 0 twin's P2 differs from the conductive one by at most 0.55 % (500 m/s, R/48, particle).

**P3, conductive minus k = 0 (reported only):**

| V (m/s) | peak edge-band T, particle: R/16 / R/24 / R/32 / R/48 | substrate | Δ P2 (largest) |
|---|---|---|---|
| 500 | −2.3 / −7.0 / −15.1 / −29.6 K | −2.0 / −5.7 / −10.1 / −22.6 K | −0.006 (particle, R/48) |
| 800 | −0.4 / −1.4 / −2.8 / −7.5 K | −0.8 / −1.7 / −2.7 / −7.0 K | −0.0002 |
| 1100 | −0.6 / −1.3 / −3.1 / −6.0 K | −0.6 / −2.0 / −3.6 / −6.8 K | −0.0001 |

Conduction cools the edge band, and more so the finer the mesh, because the hot band is thinner and so loses heat faster. The peak temperature at
the stop falls by 14–100 K. But the plastic strain at t_c hardly changes, and t_f moves by at most 3.5 %.

**Check E:** passes in all 51 runs. The total heat is at most 20 % of the particle's initial kinetic energy (500 m/s,
R/16) and falls with refinement as the runs stop earlier. No element reaches 933 K (largest: 578 K).

![CS-13c: P1 and P2 against spacing](opencourant/figures/cs13c_verdict.png)

![CS-13c setup B, R/16, 800 m/s, conductive](opencourant/figures/cs13c_B16_800.gif)

*Setup B, conductive twin, R/16, 800 m/s, to the stop at 0.109 D/V (corrected deck). Section y = 0, mirrored. Left: plastic strain; right: temperature. A thin sheared and heated band forms on both sides of the
interface and is strongest at the two contact edges. The stopping element is a particle brick off this section. A
diagnostic visual from a separate run, with the campaign's settings.*

### 13.4 Verdict (frozen rule, applied as written)

([`cs13c_verdict.py`](opencourant/scripts/cs13c_verdict.py))
- **Supported:** at none of the three velocities. Conductive t_f changes by −22 to −37 % from R/32 to R/48 (limit 6 %), and P2 by +35 to +66 % in both bodies.
- **Refuted, clause (a):** holds. At all three velocities conductive t_f falls by more than 6 % (−36.8, −28.1, −21.9 %), and P2 changes by more than 6 % in both bodies.
- **Refuted, clause (b):** holds too. The twins agree within 6 % in t_f and P2 at every velocity and spacing (largest difference 3.5 %, in t_f at 500 m/s).
- No rung failed, and every run passed check E, so the inconclusive conditions do not apply.

**CS-13c: refuted.** In OpenCourant, heat conduction at k = 237 W/(m K) does not regularise the contact edge of an
Al–Al brick-on-brick impact. The failure time keeps falling with refinement down to R/48, and the edge plastic strain
keeps rising, with or without conduction.

**What it shows and what it does not (no further verdict):**
- **Conduction acts too slowly to matter before the edge fails.** At t_c the thermal diffusion length √(κ t_c) is 0.30 / 0.19 / 0.17 µm (500 / 800 / 1100 m/s), 1–2 spacings at R/48. The edge band cools by up to 30 K, but the flow stress drop that drives the localisation is not changed measurably.
- **The failing side is the particle,** in every run, and its collapse time falls steadily as the spacing is refined (by a factor 2.0–2.9 from R/16 to R/48). This is the mesh-scale edge failure of §8.3 and §10.5, now in a fully Lagrangian 3D model.
- **One solver, as the protocol says.** A refutation in OpenCourant does not carry over to CS-13's mechanism in general. The JAX route is the independent check.
- **DECISIONS 2026-11-05 applies:** CS-13c was the last OpenCourant protocol for the thermal question, so there is no CS-13d.

## 14. sph-hvi-contact, milestone 1: recorded rows, verdicts and diagnostics (tasks 2026-11-08-a and 2026-11-11-a)

Task: [tasks/wsl-a.md](tasks/wsl-a.md), task 2026-11-11-a (record and commit), which pauses task 2026-11-08-a.
Judge: [sph-contact-ladder.md](sph-contact-ladder.md), frozen in `36c34bd`. Referee:
[sph-contact-referee-2026-11-11.md](sph-contact-referee-2026-11-11.md). Fork: `sph-hvi-contact`, rows recorded at
fork commit `b95ef45c6`; the solver source last changed in `e606c1386`. Details of every run: the fork's
`hvi/CHANGELOG.md` and `hvi/VERIFY-RESULTS.md`.

**This section adds no new physics.** It records every run the fork reported, says on which binary each ran, and
separates verdicts from diagnostics. No run was made under ξ = 0.3 + order 1 (set-up S′) and no E-1 run was made
for this task.

### 14.1 What was done for task 2026-11-11-a

1. **Rows.** Every run reported in the fork's VERIFY-RESULTS.md after A3.2 is now a CSV row, written by the fork's
   `hvi/scripts/collect_runs.py` from the run folders in `~/oc_runs`:

   | file | content | rows |
   |---|---|---|
   | [`results/hvi_a.csv`](opencourant/results/hvi_a.csv) | A-0 and A-2 | 20 |
   | [`results/hvi_b.csv`](opencourant/results/hvi_b.csv) | B-1, B-2, B-3 and B-2d at R/16 (A3.2, fork `4e0646744`; unchanged) | 21 |
   | [`results/hvi_c.csv`](opencourant/results/hvi_c.csv) | C-1, C-2, C-3 | 8 |
   | [`results/hvi_d.csv`](opencourant/results/hvi_d.csv) | D-1, D-2 and the D-1 column diagnostics (tie and welded bars) | 17 |
   | [`results/hvi_diag.csv`](opencourant/results/hvi_diag.csv) | every other B-type run: B-2d at R/32, tangent-plane gap, surface-only normals, fast deck, cone + fit, stabiliser matrix (a), F1, F2, B-1 regressions | 33 |
   | [`results/hvi_e.csv`](opencourant/results/hvi_e.csv) | the two E-1 probes (R/16, 800 m/s), labelled `unauthorised probe, diagnostic` | 2 |

   Every row carries the ladder commit, the deck hash, the settings (ξ, kernel-correction order, α_cs, stfac, normal,
   gap, surface detection), the binary it ran on, and `binary_state`.
2. **`binary_state`** has three values:
   - `committed`: the binary was built from a clean tree at the named fork SHA;
   - `source committed before run`: the solver source was committed (`e606c1386`) before the run, and the binary
     had been built from the same files one day earlier. This holds for the runs of 2026-11-11 (cone + fit full run,
     stabiliser matrix, F1, F2). The deck scripts carried uncommitted switches (`HVI_STAB`) during these runs; the
     deck hash in the row fixes the deck;
   - `binary uncommitted`: built from a dirty tree. This holds for every run between A3.2 (`4e0646744`) and
     `e606c1386`, that is C-1, C-2, C-3, D-1, D-2, the tangent-plane-gap runs, the surface-only test, the fast-deck
     acceptance runs and the second E-1 probe. For these rows the column `fork_sha` is the last source commit at run
     time, not the source of the binary.
3. **Rebuild.** The fork was rebuilt from a clean tree at `6a8084b11` (source = `e606c1386`). The new binary differs
   from the A3.4 binary of 2026-11-10 in 27 bytes (link stamp); no solver source file is newer than that binary.
4. **Reruns on the rebuilt binary, frozen set-up, clean tree:**

   | rung | result | against the earlier, inadmissible row |
   |---|---|---|
   | C-1 (core) | top-face Y within 0.27 % (λ = 1.5) and 0.23 % (λ = 2) of 1 − 1/λ²; limit 1 % | every recorded digit equal, same deck hash |
   | D-2 (core) | separation at 2.074 T_C against 2.001 (3.6 %, limit 5 %); dissipated energy 1.0000 × G_c·A (limit 5 %) | every recorded digit equal, same deck hash |
   | B-1 (stfac 1, colour; regression) | striker 0.0087 V, target 0.0043 V, tension 0 | every recorded digit equal to the A3.2 row |
   | A-0 (no sidecar) | PASS: 55 rows bit-identical to the baseline (S0 22, S0p 8, S1 16, two-part 9) | |

### 14.2 Verdicts under the frozen ladder (`36c34bd`), frozen set-up (ξ = 0, order 0)

Only rows with `binary_state = committed` carry a verdict.

| rung | verdict | fork SHA | row |
|---|---|---|---|
| A-0 | PASS (55 rows bit-identical) | `e606c1386` (rebuilt at `6a8084b11`) | `hvi_a.csv` |
| A-2 | PASS (float64 momenta, max \|Δv\|/V = 0) | `4e0646744` | `hvi_a.csv` |
| B-1 | PASS | `4e0646744`; regression row at `e606c1386` | `hvi_b.csv`, `hvi_diag.csv` |
| B-2 | **FAIL** (R/32: no stfac in {1, 3, 10} passes; stfac 1: peak 0.858, approach 1.166, rebound 0.885) | `4e0646744` | `hvi_b.csv` |
| B-3 | **FAIL** (R/32, stfac 10: 6.6 %, limit 1 %) | `4e0646744` | `hvi_b.csv` |
| C-1 | PASS | `e606c1386` | `hvi_c.csv`, row `kind = verdict` |
| D-2 | PASS | `e606c1386` | `hvi_d.csv`, row `kind = verdict` |
| D-3 | not run | | |

Deferred rungs that were run early. Their rows are diagnostics until they are rerun on a committed binary; the FAILs
stand:
- **C-2: FAIL** at the default `surface.area` (Nanson: side faces 6.0e-3, limit 1e-3); the rate form gives 3.9e-4.
- **C-3: FAIL** at the defaults (colour gradient: max tilt 32.3°, limit 5°). With `surface.detect = cone` and
  `surface.normal = fit` the max tilt is 0.91°; that is a candidate fix, not the default.
- **D-1: FAIL** (0.285 V from the exact joined bar, limit 0.05 V).

**One thing the C-1 row does not show by itself:** the first C-1 run failed (`hvi_c.csv`, first row). The cause was a
thread race in the new A3.3 hook (a missing barrier; fork CHANGELOG 2026-11-09), a code error and not a threshold
question. It was fixed before the passing run. Both rows are recorded.

### 14.3 Diagnostics (no verdict, whatever the numbers)

All rows of `hvi_diag.csv` and `hvi_e.csv`, the `D-1 diag` rows of `hvi_d.csv`, and the rows above with
`binary_state` other than `committed`.

- **Set-up S′ (ξ = 0.3 + order 1; outside the frozen set-up, chosen after seeing results).** At R/32, stfac 1:

  | run | peak | approach | rebound |
  |---|---|---|---|
  | F2: frozen contact law | 1.035 | 0.981 | 0.983 |
  | F1: cone + fit, tangent-plane gap | 1.034 | 0.975 | 0.977 |

  Both overshoot the Hertz peak by 3.4 %. The host's own F0 run at R/32 under the frozen set-up (§10: SPH sphere on
  a brick block, no hvi code) has peak 1.037, approach 0.987, rebound 0.992, so the overshoot is probably the SPH
  sphere's own at this resolution. That is a reading of existing rows, not a tested statement; the R/48 run the
  addendum asks for would test it.

  The predictions for these runs are in the fork's CHANGELOG, but the CHANGELOG was committed after the runs
  (`6a8084b11`), so git does not date them. The referee's conditions for S′ are in the addendum draft; none of them
  has been run.
- **D-1 column, maximum deviation of the striker from the exact joined bar over the whole run** (the window the
  addendum draft proposes; the fork's VERIFY-RESULTS quotes the value at 3.0 T_C, which is lower for the runs with
  ξ):

  | set-up | tie | welded SPH bar (no hvi) |
  |---|---|---|
  | frozen | 0.285 V | 0.073 V |
  | ξ = 0.3 | 0.156 V (0.123 at 3.0 T_C) | 0.126 V (0.111) |
  | α_cs = 0.1 | 0.089 V (0.086) | 0.081 V (0.080) |
  | order 1 | 0.447 V | 0.297 V |
  | S′ | 0.092 V (0.090) | 0.094 V (0.091) |

  The tie-against-welded difference is a labelled diagnostic only (referee, Q2). D-1 is judged against the exact
  bar and fails in every set-up.
- **E-1 probes (R/16, 800 m/s).** Two runs, made without a decision by Peter or schemeforge. Frozen law, stfac 3:
  J = 1.04. Tangent-plane gap, stfac 1: particles are thrown out (J = 4.4). No v_cr, no claim.

### 14.4 What cannot be repaired after the fact

- **Timing of predictions.** The predictions for the runs between `937ff009c` and `6a8084b11` (fast deck, C-3,
  cone + fit, stabiliser matrix, F1/F2) were written into the CHANGELOG before each run, but committed afterwards.
  File times are the only evidence. From now on each recorded prediction gets its own commit before its runs.
- **Binaries between A3.2 and `e606c1386`.** Five intermediate binaries (kept in `~/oc_runs/ocroot_*`) were built
  from uncommitted source and cannot be tied to a commit. The C-1 and D-2 results from them are reproduced digit
  for digit on the committed binary; the other rows stay `binary uncommitted`.
- **The stop rule.** B-2 failed at fork `4e0646744`; the fork went on through A3.3, A3.4 and deferred rungs without
  Peter's decision. That is for Peter to confirm or reject (addendum draft, open point 2).

### 14.5 Rules from now on (task item 3)

- The source is committed before every run campaign, and no run is made on a dirty tree. This covers deck scripts,
  since they define the deck.
- Each recorded prediction is committed in its own commit before its runs.
- Every run gets its CSV row in `hvi/results/` when it ends, with the fork SHA of a committed binary.

**Stopped here,** as the task says: no run under S′ and no E-1 until Peter decides on
[sph-contact-ladder-addendum-1-draft.md](sph-contact-ladder-addendum-1-draft.md).

### 14.6 Peter's decisions on the addendum draft (given in the WSL A session, 2026-11-11)

Peter decided the four open points of
[sph-contact-ladder-addendum-1-draft.md](sph-contact-ladder-addendum-1-draft.md) in the WSL A session. WSL A does
not edit DECISIONS or the ladder, so they are reported here for the cloud session to record:

1. **A1–A4 adopted as written.**
2. **Approved after the fact:** the fork's work past the plan's stop rule (A3.3, A3.4, the deferred rungs run early)
   and the E-1 probe.
3. **Fork base `d791761` accepted** instead of `cb760c2`.
4. **stfac 3 for E-1.**

No S′ run and no E-1 run is started on this basis alone: the ladder's commit order asks for the addendum to be
frozen in its own commit first.

## 15. sph-hvi-contact under set-up S′: host rungs S0 and S1 fail, reruns stopped (task 2026-11-11-b)

Task: [tasks/wsl-a.md](tasks/wsl-a.md), task 2026-11-11-b. Judge: [sph-contact-ladder.md](sph-contact-ladder.md),
frozen in `36c34bd`, Addendum 1 frozen in `140b84a`. Set-up S′ = the frozen settings plus ξ = 0.3 and
kernel-correction order 1 on all SPH particles (`SPH_STAB=0.3,0,1`, `sphdeck.py` `cb257fd`). Fork binary: source
`e606c1386`, built from a clean tree; runs started from the clean fork tree `de0906894`; results recorded in fork
`d56b565ba`. Details: the fork's `hvi/CHANGELOG.md`, "Set-up S': host rungs S0, S1, F0 and A-0".

**Result: step 1 of the task fails. S′ is not a valid host set-up under the rule fixed before the runs, and the
task stopped there.** No hvi rung (A-2, B-1, B-2, B-3, C-1, D-2, D-3, optional rungs) was run at S′. The verdicts
under the frozen set-up (§14.2) stand unchanged.

### 15.1 Rule, prediction and verdicts

- **Pass rule.** §9.4 and §9.6 give no numeric thresholds for S0 and S1. Peter fixed the rule in the WSL A session
  on 2026-11-11, before the runs: **not worse than before.** For S0 (h = 1.12 s; 25, 50, 100, 200 particles;
  plateau, contact time, rebound against 1) and S1 (conforming sphere, rigid wall, quarter model, 20 m/s; R/16,
  R/32, R/64; contact time at 10⁻² F_Hertz, peak, approach, rebound against the JAX reference of §9.6) the error
  |value / reference − 1| at S′ may exceed the error under the frozen set-up by at most 0.01. F0 keeps the limits
  of §10.2. Code: the fork's `hvi/scripts/sp_host_eval.py`.
- **Commit order.** Rule and prediction were committed in the fork (`2d60ce057`, `de0906894`) before the campaign
  started (2026-11-11 19:47).
- **Rows.** [`results/hvi_host.csv`](opencourant/results/hvi_host.csv) (one row per judged number, frozen value
  next to the S′ value), [`results/sp_host/`](opencourant/results/sp_host/) (raw CSVs with a `setup` column; the
  column `xi_stab` of `sph_s1.csv` is the deck script's own argument and reads 0, the property card of every deck
  has ξ = 0.3 and order 1), [`results/hvi_a.csv`](opencourant/results/hvi_a.csv) (A-0 at S′). All rows:
  `binary_state = committed`, ladder `36c34bd+140b84a`.

| rung | verdict at S' | numbers inside the rule | predicted |
|---|---|---|---|
| S0 | **FAIL** | 4 of 12 | PASS (wrong) |
| S1 | **FAIL** | 11 of 12 | FAIL through R/16 (wrong cause: R/16 passes, R/64 fails) |
| F0 | PASS | 3 of 3: peak 1.049, approach 0.958, rebound 0.986 | borderline, peak 1.04–1.06 (right) |
| A-0 at S' | PASS | fork without sidecar = base `d791761`: 55 runs, 627 metrics, max difference 0 | PASS (right) |

### 15.2 S0

Value at S' / frozen value; reference 1; a number fails when its error exceeds the frozen error + 0.01:

| particles | plateau | contact time | rebound |
|---|---|---|---|
| 25 | **1.0169** / 0.9948 | **0.9666** / 1.0112 | **0.8638** / 0.8881 |
| 50 | **1.0166** / 0.9955 | **0.9797** / 1.0075 | **0.9112** / 0.9251 |
| 100 | **1.0167** / 0.9956 | 0.9871 / 1.0065 | 0.9408 / 0.9485 |
| 200 | **1.0168** / 0.9957 | 0.9902 / 1.0050 | 0.9598 / 0.9640 |

Bold = outside the rule. The plateau stress is 1.7 % high at every spacing (frozen: 0.4–0.5 % low) and does not
move with refinement; it misses the limit (frozen error + 0.01 ≈ 1.5 %) by 0.15–0.25 percentage points at all four
spacings. The contact time is short instead of long and converges to 1 from below; the rebound is lower at every
spacing and the gap to the frozen value closes with refinement (0.024, 0.014, 0.008, 0.004).

### 15.3 S1

20 m/s, conforming, rigid wall, quarter; S' / frozen; references 0.940, 1.073, 0.957, 0.9996:

| spacing | contact at 10⁻² | peak | approach | rebound |
|---|---|---|---|---|
| R/16 | 0.921 / 0.964 | 1.079 / 1.193 | 0.925 / 1.122 | 0.993 / 0.925 |
| R/32 | 0.935 / 0.964 | 1.055 / 1.030 | 0.941 / 1.014 | 0.985 / 0.985 |
| R/64 | 0.955 / 0.964 | 1.019 / 1.027 | 0.958 / 0.986 | **0.966** / 0.980 |

Eleven numbers are inside the rule and nine of them are closer to the reference than under the frozen set-up. The
one failure is the rebound at R/64: error 3.33 % against a limit of 2.99 % (frozen error 1.99 % + 1). The R/16
force tail that ξ alone produced (contact time 1.089) is not there with order 1.

### 15.4 Reported, not judged

S1 at 2 m/s moves toward the reference at R/32 and R/64 (R/64: 0.956 / 1.026 / 0.962 /
0.972 against frozen 1.037 / 0.957 / 1.069 / 0.992). The mirror-wall rows stay bad (R/16 rebound 0.086 against
0.625 frozen). One lattice-sphere run with the mirror wall at R/32 blew up (peak 5·10⁵); the same case was already
unusable under the frozen set-up (rebound 0.52), and lattice spheres are not a recommended set-up (§9.6). S0p at
h = 1.12 s: wall plateau 1.014 against 0.994 frozen, the same +2 % shift as in S0.

### 15.5 Against the prediction

S0: wrong. I expected the plateau within 0.5 % of the frozen value with high
confidence; order 1 shifts it by +2.1 %. S1: I named the wrong failure (R/16 contact time); the rebound at R/64,
which I expected within 0.01 of the frozen value, is 0.013 lower. F0 and A-0 as predicted.


### 15.6 Per required rung: S′ next to the frozen verdict

| rung | frozen set-up (§14.2) | S′ |
|---|---|---|
| S0 (host) | pass (§9.4) | **FAIL** |
| S1 (host) | not a clean pass (§9.6) | **FAIL** (rebound at R/64) |
| F0 (host) | pass (§10.2) | PASS |
| A-0 | PASS | PASS (bit-identical to the base build at S′) |
| A-2 | PASS | not run (stopped) |
| B-1 | PASS | not run |
| B-2 | **FAIL** | not run; the diagnostic F2 of §14.3 (stfac 1) is not a verdict |
| B-3 | **FAIL** | not run |
| C-1 | PASS | not run |
| D-2 | PASS | not run |
| D-3 | not run | not run (A3.5 not implemented) |

### 15.7 For Peter and the cloud session to decide

WSL A changed nothing and proposes no fix here. The facts that bear on a decision:

- The S0 failure is a constant offset: order 1 puts the plateau stress 1.7 % above the exact value at every
  spacing. It misses the limit by 0.15–0.25 percentage points, but it does not converge, which the frozen set-up
  does not show (0.4–0.5 % low at every spacing).
- The S1 failure is one number of twelve (rebound at R/64, 0.34 percentage points over the limit); nine of the
  twelve are closer to the reference than under the frozen set-up.
- Which of ξ and order 1 causes the S0 offset is not measured: no host run with order 1 alone exists.
- The cost comparison (step 6), R/48 (step 4) and D-3 (step 7) are untouched.

### 15.8 Which part shifts S0 (diagnostic; Peter, 2026-11-12)

Peter asked for the cause before deciding. Two S0 runs (h = 1.12 s; 25 to 200 particles) on the same fork binary:
order 1 alone and ξ = 0.3 alone. No verdict, no rule change. The prediction (order 1 alone = S′, ξ alone = frozen)
was committed in the fork before the runs.

**Results (2026-11-12, clean tree, rows [`results/sp_host/s0_order1.csv`](opencourant/results/sp_host/s0_order1.csv) and [`s0_xi.csv`](opencourant/results/sp_host/s0_xi.csv), diagnostics).**
Both predictions hold, and exactly: order 1 alone gives the S' numbers digit for digit, ξ alone gives the frozen
numbers digit for digit (same cycle counts). **The S0 shift is caused by order 1 alone; ξ does nothing in S0.**

What order 1 changes in S0 (200 particles; frozen value in brackets):

| quantity | order 1 | frozen |
|---|---|---|
| wall force, plateau / ρ c_d V A | 1.0168 | 0.9957 |
| rate of change of the column's momentum, plateau | 1.0063 | 0.9957 |
| wall force, peak | 1.177 | 0.998 |
| impulse of the wall force / initial momentum | 1.975 | 1.959 |
| momentum change of the column / initial momentum | 1.960 | 1.964 |

Under the frozen set-up the wall force and the momentum rate agree to five digits. With order 1 the wall force is
1.0 % above the momentum rate during the plateau, and over the whole run the wall delivers 1.5 % more impulse than
the column receives (frozen: 0.5 % less, the size of the integration error of this check). ~~So with order 1 the
forces between the particles do not sum to zero: the corrected kernel sums do not conserve momentum exactly.~~
(Wrong, corrected in §15.9: the gap comes from the lateral symmetry planes of the deck.) The
wall force also has a start spike of +18 %. This is a reading of the two runs, not a code analysis; where in the
order-1 sums the momentum goes was not traced.

### 15.9 Correction of §15.8 and a width test (diagnostic, 2026-11-12)

**Correction.** In the solver source (`engine/source/elements/sph/spforcp.F`) the force between two real particles
is exactly equal and opposite with or without order 1. The gap between wall force and momentum rate in §15.8
therefore cannot come from real particle pairs. Test, with the prediction committed in the fork before the runs
(fork script `hvi/scripts/s0_width.py`): S0 at 50 particles per L with cross-sections 4, 8 and 16 particles wide,
frozen and order 1 alone.

**Results (2026-11-12, clean fork tree; rows [`results/sp_host/s0_width.csv`](opencourant/results/sp_host/s0_width.csv)).**
S0, h = 1.12 s, 50 particles per L:

| width (particles) | set-up | wall-force plateau | momentum-rate plateau | wall impulse − momentum change, / p0 (frozen offset removed) | contact time | rebound | wall-force peak |
|---|---|---|---|---|---|---|---|
| 4 | frozen | 0.9955 | 0.9955 | 0 | 1.0075 | 0.9251 | 0.998 |
| 8 | frozen | 0.9960 | 0.9960 | 0 | 1.0075 | 0.9250 | 0.999 |
| 16 | frozen | 0.9961 | 0.9961 | 0 | 1.0075 | 0.9250 | 0.999 |
| 4 | order 1 | 1.0166 | 1.0063 | +0.0195 | 0.9797 | 0.9111 | 1.180 |
| 8 | order 1 | 1.0089 | 1.0063 | +0.0049 | 0.9797 | 0.9111 | 1.170 |
| 16 | order 1 | 1.0070 | 1.0063 | +0.0012 | 0.9797 | 0.9111 | 1.167 |

(The frozen runs show a constant offset of −1/n_z = −0.0200 between the sampled wall impulse and the momentum
change: the bottom layer starts in contact and is stopped in the first step. It is subtracted in the fifth column.)

- **The gap between wall force and momentum is a deck artefact of the lateral planes.** It falls by a factor of 4
  per doubling of the width (0.0195, 0.0049, 0.0012), that is with 1/width². A share that scales like 1/width² is
  the share of the four corner columns, where two planes meet; that the corners are the place is an inference
  from this scaling, not traced in the code.
- **Order 1 has a width-independent effect as well,** and this is its real effect on the column: momentum-rate
  plateau 1.0063 (frozen 0.9955; exact 1), contact time 0.980 (1.0075), rebound 0.911 (0.925), start spike of
  the wall force +17 to 18 %. The wall-force plateau tends to 1.006 for a wide column.
- **Against the prediction.** Frozen: right (0.9955–0.9961). Order 1 at width 8: +0.0129 over frozen, at the upper
  end of the predicted +0.008 to +0.013. At width 16: +0.0108, outside the predicted +0.003 to +0.007, because I
  did not expect the width-independent part (+0.0108 → 0.51 of the excess at width 4, so "below half" just fails).
  The gap itself falls faster than predicted (1/width² and not 1/width).
- **What it changes for the S0 verdict at S':** nothing. The rule was fixed for the 4-wide deck. On an infinitely
  wide column the plateau would be inside the rule (error 0.6 % against a limit of 1.5 %), but contact time and
  rebound do not depend on the width and stay outside the rule at 25 and 50 particles. S1 is not affected (R/32
  half against quarter model at S': peak 1.059 against 1.055).

### 15.10 Peter's decision (WSL A session, 2026-11-12) and the analysis

**Peter accepted the stop.** S′ is not adopted; the verdicts under the frozen set-up stand (§14.2: B-2 and B-3
FAIL). Steps 3–8 of task 2026-11-11-b are not run. WSL A does not edit DECISIONS; this is reported here for the
cloud session to record.

At Peter's request WSL A wrote an analysis (what was learned, what is not understood, outlook on other approaches
and on simplifying assumptions for cold spray): fork `sph-hvi-contact`, `hvi/ANALYSIS-2026-11-12.md`. Its outlook
is from general knowledge, with no paper opened, and is marked as such.

## 16. TLSPH in the fork: T-A0 passes, T-S0 fails, task stopped (task 2026-11-12-c)

Task: `tasks/wsl-a.md`, task 2026-11-12-c. Judge: `sph-tlsph-ladder.md` and hunch `coldspray-hunch-cs18.md`,
frozen in `583912a`. These three files are on branch `claude/exciting-fermi-qy077p` and not yet on this branch. Design: the fork's `hvi/SPEC-TL.md`
(set-up of the ladder; differences between code and text in its section 3.12). Fork `sph-hvi-contact`, branch
`tlsph`: engine source `eac1040b2`, binary built from the clean tree; results recorded in `a51d44ca3`. Details: the
fork's `hvi/CHANGELOG.md`, "TLSPH implementation, SPEC-TL 6 steps 1 to 5" and "TLSPH ladder, core rungs".

**Result: the implementation (SPEC-TL section 6, steps 1 to 5) is in the fork and reviewed. T-A0 passes. T-S0, the
second core rung, fails, and the task stopped there** (task rule: a failing core rung means stop and report to
Peter, with no tuning). No later rung was run: T-S0p, T-S1, T-tension, T-zero-energy, T-B1, T-B2, T-B3,
T-survival, T-C1, T-D1, T-D2 have no verdict. The CS-18 kill clause (T-survival) was not reached.

### 16.1 Verdicts

| rung | verdict | numbers | predicted |
|---|---|---|---|
| T-A0 | PASS | 55 of 55 runs without a TL body identical to the A-0 run on `6a8084b` in the written metrics (§16.2) | none recorded (deviation from the task rule) |
| T-S0 | **FAIL** | see §16.3 | FAIL at 100 particles (not blind; see §16.4) |

Rows: [`results/tl_a0.csv`](opencourant/results/tl_a0.csv), [`results/tl_host.csv`](opencourant/results/tl_host.csv).
Every row: `binary_state = committed`, fork SHA `eac1040b2` (last commit that changed solver source), ladder
`583912a`, deck hash.

### 16.2 T-A0

The A-0 deck set (S0, S0p, S1, two-particle test; no sidecar) on the TLSPH binary, compared with the A-0 run of
the binary before TLSPH (`6a8084b`, §14). A run counts as identical if every column of its csv row except the
timing columns and the thread count is the same string (fork `hvi/scripts/tl_a0.py`).

| file | runs identical | fields compared |
|---|---|---|
| sph_s0.csv | 22 of 22 | 286 |
| sph_s0p.csv | 8 of 8 | 104 |
| sph_s1.csv (five files `s1_*.csv`) | 16 of 16 | 304 |
| sph_twopart.csv | 9 of 9 | 27 |

The ladder asks for "bit-identical". The comparison is on the written metrics (double precision in the csv), not
on the engine's binary output files; this is the same basis as rung A-0 in §14. The run was made twice: on the
first TLSPH commit (`07c549519`) and again on `eac1040b2` after the review added two fatal checks; both give 55
of 55. The second run carries the verdict.

Time histories: 47 of the runs write a time-history csv. 44 are byte-identical to the reference, 3 are not
(`Hrhc20112032`, `Hrhl20112016`, `Hrfl20112016`: the half and the full sphere models). They differ only in the
sphere's momentum in the directions without a symmetry plane, where the exact value is zero and the written values
are below 5·10⁻²⁷. The same three files also differ between the two T-A0 runs, so it is noise in a zero sum
between runs; whether two runs of one binary differ in the same way was not tested. No metric uses these columns.
Strictly, "bit-identical" holds for the written metrics of all 55 runs and for 44 of 47 time-history files.

### 16.3 T-S0

Confined elastic column of §9.4 (h = 1.12 s), the whole column one TL body; 4 threads. Rule (frozen): at 100 and
200 particles plateau and contact time within 1 %, rebound ≥ 0.95; the three errors do not grow from 100 to 200.
Reference 1 for all three numbers.

| particles | plateau | contact time | rebound | point criteria |
|---|---|---|---|---|
| 25 (reported) | 1.0057 | 0.9603 | 0.8694 | not judged |
| 50 (reported) | 1.0063 | 0.9773 | 0.9136 | not judged |
| 100 | 1.0065 | **0.9851** | **0.9420** | fail |
| 200 | 1.0065 | **0.9890** | 0.9604 | fail |

Bold = outside the limit. Errors from 100 to 200: plateau 0.648 → 0.654 % (grows), contact time 1.49 → 1.10 %,
rebound 5.80 → 3.96 %.

**T-S0 FAIL** on each part of the rule: contact time and rebound at 100, contact time at 200 (0.10 percentage
points over the limit), and the growth criterion through the plateau (by 0.005 percentage points).

### 16.4 Against the prediction

The prediction (fork `2c0523579`, committed before the run) was not blind: development runs had already shown
the TL column at 25, 50 and 100 particles. It said FAIL at 100, and that is what happened. Its two real
predictions, for the 200-particle run, are both wrong: contact-time error expected at 0.8 to 1.0 % (found 1.10 %),
and "errors do not grow" expected to hold (the plateau error grows). A third expectation is also wrong: contact
time and rebound "converge at roughly first order" (§16.5: they do not). The rebound at 200 (0.960) is inside the
predicted range of 0.955 to 0.965.

### 16.5 Diagnostics (no verdict)

- **Plateau.** 1.00565, 1.00631, 1.00648, 1.00654 at 25, 50, 100, 200 particles: the sequence looks converged to
  about 1.0066, not to 1. The 2D quads gave +0.69 % (+0.66 % with `Isolid = 0`) on the rung-0 column, a finite-strain effect
  (§3); collocated SPH with kernel-correction order 1 gave 1.0063 at 50 particles in the momentum-rate plateau (§15.9; its wall-force plateau was 1.0166 at this column width; for TL both measures give 1.0063). The TL value is close to both. That
  fits a finite-strain offset of the linear reference, but it is not shown for TLSPH: no TL run at a lower
  velocity was made. Against it: the collocated column under the frozen set-up sits at −0.43 % at the same
  velocity, and the 1.1 % gap between it and the quads is unexplained (§9.4); an offset of the reference alone
  would shift all formulations the same way. If it is finite strain, the growth criterion fails on a number that converges to a value
  other than the reference.
- **Contact time and rebound.** Contact-time error 3.97, 2.27, 1.49, 1.10 %; its ratio per halving of the spacing
  falls (1.74, 1.53, 1.36). Rebound error 13.1, 8.6, 5.8, 4.0 %, ratio about 1.5 per halving. Neither converges
  at first order.
- **Dissipation.** Work removed by the artificial viscosity until the end of the run, as a share of the initial
  kinetic energy: 15.7, 11.1, 7.8, 5.6 %. By the hourglass force: 0.25, 0.12, 0.06, 0.03 %. Start spike of the
  wall force: 1.21, 1.21, 1.21, 1.20 of the exact plateau force.
- **Self-checks of the TL module.** Condition number of the correction matrix 1.62 (limit 30), completeness sums
  1.2·10⁻¹⁵, smallest det F 0.9835, largest stretch 1.008, no plastic strain.
- **The collocated host under the same rule.** The collocated frozen set-up (§9.4 rows, A-0 reference) gives
  0.9956 / 1.0065 / 0.9485 at 100 and 0.9957 / 1.0050 / 0.9640 at 200. Measured with the T-S0 rule it would miss
  at 100 on the rebound (0.9485 against 0.95) and meet the point criteria at 200. At 200 the collocated host is closer to
  the reference in all three numbers: plateau error 0.43 against 0.65 %, contact-time error 0.50 against 1.10 %,
  rebound 0.9640 against 0.9604.

### 16.6 Not done, and what is open

- Not run: every rung after T-S0. Not written: the T-zero-energy deck. The T-B and later rungs would use the
  existing deck scripts with the TL switch.
- Not tested: the cause of the plateau offset; which of viscosity (Monaghan 2 / 1 with the shear switch), kernel
  stencil or hourglass term sets the contact-time error and the rebound.
- Deferred by Peter before the freeze and still open: the journal version of Ganzenmüller 2015 against the
  preprint (hourglass amplitude, SPEC-TL 3.10).
- For Peter and the cloud session: T-S0 failed under the frozen rule, so the TLSPH ladder is stopped at its second
  rung. Any change to the set-up or the rule is an addendum, labelled post hoc.

## 17. T-S0 diagnosis: what sets the errors of the TL column (task 2026-11-13-a; diagnostics only, no verdicts)

Task: `tasks/wsl-a.md`, task 2026-11-13-a (on branch `claude/exciting-fermi-qy077p`). Fork `sph-hvi-contact`,
branch `tlsph`: engine source `eac1040b2` (unchanged; deck and sidecar switches only), script
`hvi/decks/tl_diag_s0.py`, results recorded in `cd1efb6a3`. Each case changes one thing against the frozen T-S0
set-up of §16. The six predictions were committed in the fork, one commit each (`ecc79946c` to `316b0eda6`),
before the first diagnostic run. Rows: [`results/tl_diag_s0.csv`](opencourant/results/tl_diag_s0.csv), all with
`kind = diagnostic`, `binary_state = committed`, fork SHA and deck hash, and no verdict.

**Short answer.** The plateau offset is finite strain. The contact-time error is that offset plus about one
spacing, to which viscosity and hourglass force both contribute. A little more than half of the rebound error is the
viscosity; the rest is not explained. The start spike is a transient of the end layers at the wall.

### 17.1 Cases

| case | particles | plateau | contact time (first sample / interpolated) | rebound | viscous work | hourglass work | wall-force peak | undershoot after it | settled within 2 % after (s / c_d) |
|---|---|---|---|---|---|---|---|---|---|
| frozen (T-S0 rerun with stress output) | 50 | 1.0063 | 0.9773 / 0.9761 | 0.9136 | 11.1 % | 0.12 % | 1.211 | 0.908 | 8.2 |
| frozen (T-S0 rerun with stress output) | 100 | 1.0065 | 0.9851 / 0.9846 | 0.9420 | 7.8 % | 0.06 % | 1.210 | 0.911 | 8.0 |
| frozen (T-S0 row, no new run) | 200 | 1.0065 | 0.9890 / 0.9887 | 0.9604 | 5.6 % | 0.03 % | 1.196 | 0.916 | 8.0 |
| D-visc-off | 100 | 1.0058 | 0.9893 / 0.9892 | 0.9732 | 0 | (26 %, see note) | 1.327 | 0.769 | never (ripple 6.3 %) |
| D-visc-off | 200 | 1.0067 | 0.9932 / 0.9926 | 0.9836 | 0 | (26 %, see note) | 1.327 | 0.769 | never (ripple 6.0 %) |
| D-visc-P (q_a 4, q_b 0.8) | 100 | 1.0065 | 0.9851 / 0.9848 | 0.9467 | 7.1 % | 0.09 % | 1.220 | 0.897 | 8.3 |
| D-visc-P (q_a 4, q_b 0.8) | 200 | 1.0065 | 0.9900 / 0.9893 | 0.9638 | 5.0 % | 0.04 % | 1.212 | 0.903 | 8.4 |
| D-hg, alpha 0 | 100 | 1.0064 | 0.9870 / 0.9864 | 0.9411 | 8.0 % | 0 | 1.249 | 0.796 | 16.7 |
| D-hg, alpha 0 | 200 | 1.0065 | 0.9900 / 0.9897 | 0.9600 | 5.6 % | 0 | 1.243 | 0.807 | 16.8 |
| D-hg, alpha 20 | 100 | 1.0065 | 0.9833 / 0.9828 | 0.9426 | 7.7 % | 0.10 % | 1.184 | 0.969 | 3.8 |
| D-hg, alpha 20 | 200 | 1.0065 | 0.9882 / 0.9877 | 0.9606 | 5.5 % | 0.05 % | 1.176 | 0.972 | 3.7 |
| D-vel, V / 2 | 200 | 1.0033 | 0.9923 / 0.9920 | 0.9609 | 5.5 % | 0.03 % | 1.193 | 0.918 | 8.0 |
| D-vel, V / 4 | 200 | 1.0016 | 0.9941 / 0.9935 | 0.9611 | 5.5 % | 0.03 % | 1.192 | 0.916 | 8.0 |
| D-width, 16 x 16 | 100 | 1.0065 | 0.9851 / 0.9846 | 0.9420 | 7.8 % | 0.06 % | 1.210 | 0.911 | 8.0 |
| collocated, order 1 (no TL body) | 50 | 1.0166 (momentum rate 1.0063) | 0.9797 / 0.9793 | 0.9111 | not written | none | 1.180 | 0.838 | 16.3 |
| collocated, order 1 (no TL body) | 100 | 1.0167 (momentum rate 1.0063) | 0.9871 / 0.9866 | 0.9408 | not written | none | 1.178 | 0.840 | 16.3 |

Columns: every number is normalised with the case's own velocity. Works are shares of the initial kinetic
energy at the end of the run. Wall-force peak and undershoot: the largest wall force of the run, and the smallest
one after it before 0.1 contact times; the peak is over the exact plateau force, the undershoot over the measured
plateau. The contact time has two values because the 5 % crossing is read from samples 0.0007 to 0.0017 contact
times apart; the second value is interpolated between two samples.

Note on the hourglass work without viscosity: the diagnostic `w_hourglass` reaches -26 % of the initial kinetic
energy, growing linearly in time, while the kinetic energy returns to 97.7 % after the rebound. So this energy was
not removed. The diagnostic sums force times half-step velocity, which is biased for an oscillation that is
resolved by few time steps; with ringing it is not a measure of dissipation. [inference from the kinetic energy
alone: the listing has no internal energy for a TL body, and the accumulator itself was not tested] In the cases
with viscosity there is no ringing (ripple below 0.02 %); there the end kinetic energy plus the two works is
0.981, 0.991 and 0.995 of the initial energy at 50, 100 and 200 particles. That gap is larger than the hourglass
share, so the balance cannot confirm the hourglass share either.

The task named the widths and coefficients; the mapping of Profizi's "linear 0.8 / quadratic 4" onto the solver's
pair viscosity 2 (q_a μ² − q_b c μ) / (ρ_i + ρ_j) is q_b = 0.8, q_a = 4. Whether Profizi's own expression has the
same normalisation was not checked. Changing q also changes the time step (cycle counts at 100 particles: 2175
frozen, 1877 Profizi, 903 without viscosity). The wall-force columns of the frozen 200-particle row are
recomputed from the T-S0 run's trace and are in no csv.

### 17.2 D-layer: stress per layer

Axial stress per layer over ρ c_d V, layer 1 on the wall; the steady values of the 50-particle profiles agree with these to 0.001 (the maxima and the collocated bulk mean, 1.0034, do not):

| layer from the wall | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | bulk mean (11 to 0.6 n) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TL, 100 particles, at 0.4 contact times | 0.655 | 0.845 | 1.018 | 1.006 | 1.006 | 1.006 | 1.006 | 1.006 | 1.006 | 1.006 | 1.0064 |
| TL, largest value up to 0.45 contact times | 0.813 | 0.890 | 1.076 | 1.055 | 1.044 | 1.040 | | | | | 1.021 (any layer from 11 on) |
| collocated order 1, 100 particles, at 0.4 | 0.550 | 0.941 | 1.045 | 0.978 | 1.028 | 0.990 | 1.019 | 0.997 | 1.014 | 1.001 | 1.0066 |
| collocated order 1, largest value | 0.801 | 0.941 | 1.186 | 1.024 | 1.095 | 1.038 | | | | | 1.052 (any layer from 11 on) |

### 17.3 Reading

**1. What sets the contact-time error.** No single item; three parts, here with the interpolated values:

| part | size | evidence |
|---|---|---|
| finite strain (the reference is linear) | 0.65 % at V, 0.33 % at V / 2, 0.16 % at V / 4; at V the same at 50, 100 and 200 particles | D-vel: the plateau offset is proportional to V, and a front with a high plateau is fast by the same factor (jump condition) |
| a term of about one spacing | 0.9 to 1.0 spacings: error minus offset = 0.88 / n, 0.89 / n, 0.95 / n at 50, 100, 200 (V); 0.95 / n at V / 2; 0.98 / n at V / 4 | T-S0 rows and D-vel |
| the viscosity | without it the error is 1.08 % instead of 1.54 % at 100 and 0.74 % instead of 1.13 % at 200: a difference of 0.45 % and 0.39 % of the contact time, so about constant and not proportional to 1 / n (0.45 and 0.78 spacings). Two caveats: the run without viscosity has 6 % ripple on the force, which blurs a 5 % crossing, and its time step is 2.4 times larger | D-visc-off |
| the hourglass force | 0.18 spacings per 10 units of alpha at 100 (alpha 0 / 10 / 20: 1.36 / 1.54 / 1.72 %), 0.2 at 200 (1.03 / 1.13 / 1.23 %) | D-hg |

The width changes nothing. Profizi's coefficients change the interpolated contact time by 0.02 % at 100 and
0.06 % at 200. The error of the frozen set-up minus the finite-strain offset is 0.89 % at 100 and 0.48 % at 200;
this is a difference of two measured numbers and says nothing about a rung.

**2. What sets the rebound error.** The viscosity carries a little more than half of it. Without viscosity the
rebound is 0.973 at 100 and 0.984 at 200 (error 2.7 and 1.6 % instead of 5.8 and 4.0 %). What is left is not
explained by ringing alone: the kinetic energy that is not centre-of-mass motion at the end is 3.0 % (100) and
1.9 % (200) of the initial energy without viscosity, and 2.4 % and 1.7 % in the frozen runs, which do not ring.
So a similar amount of energy stays in internal motion of the column after the rebound in both cases; what
motion that is was not looked at. Profizi's coefficients remove 9 % less energy than
the frozen ones and raise the rebound by 0.005 (100) and 0.003 (200). The hourglass coefficient and the velocity
do not change the rebound (within 0.001).

**3. Is the plateau offset finite strain?** Yes. The offset is 0.654 %, 0.326 %, 0.163 % at V, V / 2, V / 4:
proportional to V within 0.5 % of its value, coefficient 0.42 x V / c_d, the same as for the quad elements. It
does not depend on the viscosity coefficients (with viscosity on), the hourglass coefficient or the width. The
growth of the plateau error from 100 to 200 particles in T-S0 (0.648 to 0.654 %) then reads as convergence to
this offset. [inference]

**4. Where the start spike sits.** It is a transient of the end layers at the wall during the first spacings of
wave travel. No layer reaches a stress 21 % above the plateau:
- The wall force peaks at 1.2 to 1.6 s / c_d (the sample step is 0.14 s / c_d at 50 and 100 particles and
  0.41 at 200, so the 200-particle peak of 1.196 is undersampled), undershoots to 0.91 of the plateau, and stays
  within 2 % from 8 s / c_d on. In units of s / c_d this is the same at 50, 100 and 200 particles and at all three
  velocities, so in physical time it shrinks with the spacing.
- In absolute terms no layer carries a stress peak of that size: layer 1 never exceeds 0.81 of the reference
  stress, layer 3 reaches 1.08, the layers from 11 on at most 1.02. Relative to its own steady value layer 1 does
  overshoot, by 24 % (0.813 against 0.655) at the time of the wall-force peak, and the overshoot travels into the
  column and decays: layers 3 to 6 exceed their steady values by 5.7, 4.9, 3.8 and 3.3 %, layer 11 by 1.5 %.
- In the steady state the first two layers carry less stress than the wall transmits: 0.655 and 0.845 (layer 3:
  1.018; from layer 4 on the bulk value). The pattern is the same at 50 and 100 particles and does not change in
  time. The wall force (1.0065) is nevertheless the bulk stress, so the momentum balance holds; the particle
  stress of the two end layers is not the traction there.
- The hourglass force damps the transient: alpha 0 / 10 / 20 gives peak 1.25 / 1.21 / 1.18, undershoot 0.80 /
  0.91 / 0.97 and settling after 16.7 / 8.0 / 3.8 s / c_d. Without viscosity the peak is 1.33.
- Collocated SPH with kernel-correction order 1 shows a transient of the same kind (peak 1.18, undershoot 0.84,
  settled after 16 s / c_d; taken at width 4, where its wall force carries the width artefact of §15.9 of the
  schemeforge document) and a wider steady pattern: 0.550, 0.941, 1.045, 0.978, 1.028, 0.990, ... alternating over
  more than ten layers. The collocated frozen set-up without correction has no start spike (peak 0.998, T-A0
  reference rows); its layer profile was not taken.

Does the spike come from the end-layer correction? The evidence fits: both set-ups with a corrected gradient have
it and the uncorrected one does not; its steady pattern sits in the first three layers and it scales with the spacing. It is not
isolated, because the correction of a TL body cannot be switched off from the deck. My reading: the correction
matrix makes the deformation gradient of the one-sided end layer exact for linear fields, but the pair force sum
at a truncated neighbourhood is not corrected, so the end layers find an equilibrium with a stress that differs
from the traction, and they oscillate into it. [inference, not tested]

### 17.4 Against the predictions

| case | prediction | found |
|---|---|---|
| D-vel | plateau 1.0033 and 1.0016; contact time 0.9925 and 0.9942; rebound unchanged | 1.0033 and 1.0016; 0.9923 and 0.9941; 0.9609 and 0.9611. Right |
| D-visc-off | stable; peak 1.25 to 1.5; plateau within 0.002; contact time unchanged within 0.003; rebound 0.95 to 0.98 and 0.96 to 0.99 | stable, peak 1.33, plateau 1.0058 and 1.0067, rebound 0.973 and 0.984: right. Contact time +0.004 at both spacings: outside the predicted range, so the viscosity (or the larger time step and the ripple that come with switching it off) does move the contact time |
| D-visc-P | plateau and contact time unchanged; rebound +0.002 to +0.01; viscous work 0.8 to 0.95 of the frozen one; peak 1.21 to 1.25 | unchanged; +0.005 and +0.003; 0.91; 1.22 and 1.21. Right |
| D-hg | both stable and within 0.002 in plateau and contact time; alpha 20: spike within 0.01; alpha 0: spike changes by a few 0.01 | stable; contact time -0.002 and +0.002 at 100 (at the edge of the range); alpha 0 spike +0.04: right. Hourglass work at alpha 20: 1.75 times, predicted "about doubles". Alpha 20 spike -0.026: wrong, the hourglass force acts on the start transient in both directions |
| D-width | identical within 1e-4 | plateau, contact time, rebound and peak agree to 5e-8 or better. Right |
| D-layer | wall-force peak within 5 s / c_d, settled within 20, same at 50 and 100; bulk overshoot below 5 %; first one to three layers deviate steadily; layer 1 stress 15 to 30 % above the plateau | timing, bulk and the steady three-layer pattern: right. Layer 1 stress: wrong, it is 35 % below the plateau and never above 0.81; the spike is in the wall force only. Collocated order 1: spike in the first layers right, but the steady pattern runs over more than ten layers and the bulk overshoot is 5.2 % over the reference stress (4.5 % over its own bulk value) |

### 17.5 Not done

- A TL run without the correction matrix, which would isolate the cause of the start spike: it needs solver code.
- The layer profile of the collocated frozen set-up.
- A check of the `w_hourglass` accumulator.
- Nothing here is a verdict or changes one: T-S0 stays FAIL under the frozen rule (§16).

## 18. CS-18b calibration and design (task 2026-11-13-b; calibration and design only, no verdicts)

Task: `tasks/wsl-a.md`, task 2026-11-13-b (DECISIONS 2026-11-13, "CS-18b with a calibration phase before its
freeze"). Fork `sph-hvi-contact`, branch `tlsph`, records at `999ace118`: the full write-up is the fork's
`hvi/SPEC-TL-b.md`; rows `hvi/results/tl_cal_*.csv` (copied to [`results/`](opencourant/results/)), all
`kind = calibration`, with fork SHA, deck hash and `binary_state = committed`. No TLSPH rung deck was used to choose
anything. Binaries: `eac1040b2` (quad and collocated rows) and `84e87958d` (adds an optional viscosity form; on the
frozen T-S0 column its default path reproduces `eac1040b2` byte for byte, and the A-0 decks without a TL body
other than the S1 spheres give 39 of 39 runs identical to the A-0 reference).

### 18.1 (a) Finite-strain references

LAW1 and LAW2 take the pressure from the density (p = K(ρ/ρ0 − 1)) and the deviator in rate form, so in uniaxial
strain the compressive stress is S(λ) = K(1/λ − 1) − (4G/3) ln λ. Rankine–Hugoniot in the reference configuration
gives the plateau U/c_d = 1 + 0.423 V/c_d + … (ν = 0.35), the 0.42·V/c_d of §17 derived. Contact time and rebound
come from a 1D Lagrangian solver of the same law (finite-strain run minus linear run on the same mesh, 16000 cells),
read with the rung definitions (`fs1d.py`).

| rung | metric | small-strain reference (frozen) | finite-strain reference |
|---|---|---|---|
| T-S0 (100 m/s) | plateau | 1 | **1.00659** |
| T-S0 | contact time | 1 | **0.99294** |
| T-S0 | rebound | 1 | **0.99654** |
| T-S0p (50 m/s) | σ₂ | 1 | **1.00412** |
| T-S0p | plastic front | c_b | **1.00544** c_b |
| T-S0p | elastic front | c_d | **1.00082** c_d |
| T-tension | striker velocity | exact linear bar | differs by at most 0.0033 V: keep the linear reference |

Checks: TL plateaus at V, V/2, V/4 (§17) are within 0.006 % of the reference; quads Isolid 17 within 0.03 %; the
collocated column is 1.08 % low (the unexplained §9.4 gap; not finite strain).

### 18.2 (b) Threshold calibration

Quads (Isolid 17, viscosity off, dt scale 0.4; S1 meshes are R/12.5 to R/25.2, the finest is compared at R/32 and
R/64) and collocated SPH (frozen §9.1 set-up, the T-A0 rows of the same binary and decks), with the SPH ladder's
metric definitions (except the quads' T-S0 contact time, interpolated between samples; the sampled values give
0.87 % and 0.50 % and change no threshold). Proposed rule, committed after the quad and collocated numbers existed
and using no TL number: **threshold = 1.25 × the larger error of the two methods, rounded up to the next 0.5 %, at
least 0.5 %**.

| rung | metric | resolution | quads error | collocated error | proposed | frozen |
|---|---|---|---|---|---|---|
| T-S0 | plateau | 100 / 200 | 0.03 % / 0.03 % | 1.09 % / 1.08 % | within 1.5 % | 1 % of 1 |
| T-S0 | contact time | 100 / 200 | 0.74 % / 0.44 % | 1.37 % / 1.21 % | within 2.0 % | 1 % of 1 |
| T-S0 | rebound | 100 / 200 | 1.02 % / 0.55 % | 4.82 % / 3.27 % | ≥ 0.9318 / ≥ 0.9517 | ≥ 0.95 |
| T-S0p | σ₂ | 200 | 0.69 % | 0.95 % | within 1.5 % | 1 % |
| T-S0p | plastic front | 200 | 1.21 % | 2.64 % | within 3.5 % | 1 % |
| T-S0p | elastic front | 200 | 0.37 % | 1.05 % | within 1.5 % | 1 % |
| T-S1 | contact at 10⁻² | R/32 / R/64 | 0.11 % | 2.57 % / 2.56 % | within 3.5 % | not judged |
| T-S1 | peak | R/32 / R/64 | 0.22 % | 4.01 % / 4.28 % | within 5.5 % | 5 %; R/64 ≤ R/32 + 0.01 |
| T-S1 | approach | R/32 / R/64 | 0.11 % | 5.93 % / 3.02 % | within 7.5 % / 4.0 % | 5 %; R/64 ≤ R/32 + 0.01 |
| T-S1 | rebound | R/32 / R/64 | 0.00 % | 1.43 % / 1.99 % | ≥ 0.9796 / ≥ 0.9746 | ≥ 0.95 |

- Against the finite-strain references, the calibration methods fail several frozen limits: collocated SPH the
  T-S0 plateau and contact time, the T-S0 rebound at 100 (0.9485), the T-S0p fronts and the T-S1 approach at R/32;
  the quads the T-S0p plastic front.
- Noise floors for the growth clauses: T-S0 from 100 to 200, plateau 0.1 %, contact time 0.2 % (one time-history
  sample either way), rebound 0.2 %; T-S1 keeps + 0.01.
- **T-B2** (sphere on a TL block, R/32): proposed peak within 5.5 %, approach within 7.5 % (the one-body limits; two
  bodies in series give a weighted mean of their errors [inference]), rebound > 0.9 kept. Not calibrated by a run; a quad
  two-body run should calibrate it before the freeze.

### 18.3 (c) Viscosity

Form: the LAMMPS SMD TLSPH pair viscosity, read from the source (`pair_smd_tlsph.cpp`, Ganzenmüller 2014): acts in
compression and expansion, no switch, reference sound speed and density, relative normal velocity capped at
0.01 c0, Π = (−Q1 c0 μ + Q2 μ²)/ρ0. Ported as sidecar option `tl.visc = lammps` (fork `84e87958d`). Q2 = 0 (with the
cap it is at most 0.02 Q2 of a linear term, and anti-dissipative in expansion). Calibration cases, not rungs: a
confined TL column of length 2L at V/2, and a free TL bar ringing in its first mode. The column is, in dimensionless
form, the T-S0 column at V/2 (its rows equal §17's V/2 run): not a rung, but not a new geometry; the bar is the
independent case. Criterion committed before the
runs (fork `4a6412f6b`): stable; wall-force ripple ≤ 0.5 % on the column at both spacings; then the least first-mode
damping per period of the bar.

| setting | column ripple (L/50, L/100) | column rebound (L/100) | bar damping per period (L/100) | column start spike |
|---|---|---|---|---|
| frozen Monaghan q 2/1 | 0.00 %, 0.00 % | 0.961 | 3.59 % | 1.19 |
| Q1 = 0.01 | 2.59 %, 1.09 % | 0.983 | 0.10 % | 1.29 |
| Q1 = 0.02 | 1.32 %, 0.32 % | 0.983 | 0.21 % | 1.29 |
| **Q1 = 0.05** | 0.23 %, 0.01 % | **0.980** | **0.51 %** | 1.28 |
| Q1 = 0.1 | 0.02 %, 0.00 % | 0.976 | 1.02 % | 1.27 |
| Q1 = 1 | 0.00 %, 0.00 % | 0.938 | 9.75 % | 1.18 |

**Proposed: LAMMPS form, Q1 = 0.05, Q2 = 0** (Q1 = 0.01 and 0.02 ring). The start spike of the wall force grows
(1.19 → 1.28); the hourglass α, which also damps it (§17), was not recalibrated.

### 18.4 (d) End-layer stress

- **Cause, reproduced:** a static model of the TL column (`tl_endlayer.py`: corrected reference gradient, Ganzenmüller
  force, lateral images, linear elasticity, linearised hourglass force) gives 0.6515 / 0.8397 / 1.0107 for layers
  1 to 3 under a wall force on layer 1; the TL runs measured 0.6504 / 0.8400 / 1.0117 (over their plateau). No fitted
  parameter. For a uniform stress the corrected force sum leaves a boundary force spread over two layers with
  opposite signs (+1.485, −0.471 per unit area on layers 1 and 2). The wall and the hvi contact apply the whole load
  to layer 1, so the end layers deform until they balance it. Loading the layers in proportion to that boundary
  force makes the stress uniform exactly. A flat, lattice-aligned free face under uniform in-plane load with
  σ · n = 0 is an exact discrete equilibrium (curved faces and non-uniform stress are not covered by the argument):
  the error is where a normal traction acts, at walls and contacts, so at the particle–substrate interface.
- **Literature:**
  - Röthlin, Klippel & Wegener (arXiv:1807.01117, §4.2) state that a corrected scheme must impose σ · n
    explicitly. They list stress rotation (Randles & Libersky 2000), ghost particles (Hieber & Koumoutsakos 2008),
    a −σ · n body force (Hieber et al. 2004) and the weak form; the four originals were not read.
  - Vignjevic et al. 2021 state that boundary conditions spread over a boundary layer of the support size.
  - No source deriving the consistent traction for corrected TLSPH was found.
- **Proposed fix (not implemented): boundary-consistent traction.**
  - Store the reference boundary vector B_k = Σ_j V_k V_j (K_k + K_j) ∇W_kj per TL particle.
  - Distribute each contact or wall force f_i over the TL particles k of the same body near i with weights
    φ_ik (B_k · n_i) / Σ_m φ_im (B_m · n_i), φ_ik = W_ik / Σ_{i' loaded} W_i'k (Shepard-normalised over the loaded
    particles). With plain kernel weights the load split comes out wrong (1.106 / −0.106 instead of 1.485 / −0.471;
    layer stresses 0.728 / 0.873 in the static model). With φ the static model gives 0.9999 on every layer.
  - The weights sum to 1, so momentum is conserved. The torque error is of order |f| s per pair. The denominator
    mixes positive and negative layer terms and needs a guard on curved surfaces; this should be checked on the
    conform sphere before coding.
  - It is a TL-only step after the hvi contact force; the hvi law stays unchanged.
  - Reason to fix: the interface stress drives the plastic flow and the edge state [inference; no TL impact run
    has looked at it].
- **Proposed rung T-surface**, limits by the rule of 18.2:
  1. Layers 1 and 2 of the T-S0 column over the wall-force plateau, at 100 and 200 particles: quads 0.11 %,
     collocated 11.4 % (its own alternating end pattern), **within 14.5 %**; with quads alone 0.5 %. TL today:
     35 % and 16 %; BCT with Shepard weights 10⁻⁴ in the static model (not implemented).
  2. Free surface under load (the T-S0 column 16 particles wide with free x faces, `tl_cal_surface.py`):
     σ_zz of the two outer columns over the middle, time-averaged over 0.25–0.55 contact times. Collocated
     1.010 / 1.007 at 100 particles and 0.999 / 1.001 at 200, giving **within 1.5 %** at 100 and 0.5 % at 200.
     The time average was introduced after the first single-frame runs had been seen (they scattered with the
     breathing mode across the width: 0.908 / 0.961 at 50, 1.026 / 1.008 at 100).
     There is no quad calibration (the axisymmetric quads cannot represent this deck), and TL was not run on it.

### 18.5 Not done

- A quad two-body run to calibrate T-B2.
- A second bar amplitude for the viscosity (the 0.01 c0 cap matters only at impact velocities).
- A recalibration of the hourglass α together with the new viscosity.
- The S1 part of A-0 on `84e87958d` (the rest gives 39 of 39 identical runs).
- The rebound and contact-time references at V/2 and V/4 (not converged at 16000 cells).
- The CS-18b draft itself is the cloud session's, and Peter approves the freeze.

## 19. CS-18b calibration part 2 and BCT (task 2026-11-13-c; calibration only, no verdicts)

Task: `tasks/wsl-a.md`, task 2026-11-13-c, items 1 to 5 (item 5 added 2026-11-13); DECISIONS 2026-11-13 "CS-18b
calibration decisions" and "CS-18b hold lifted". Fork `sph-hvi-contact`, branch `tlsph`, records at `72740e89b`: the
full write-up is `hvi/SPEC-TL-b.md` section 5; rows `hvi/results/tl_cal2_*.csv` (copied to
[`results/`](opencourant/results/)), `kind = calibration` (item 5: `calibration, diagnostic`). Engine rows carry the
fork SHA, deck hash and `binary_state = committed`; the static-model rows carry the script commit; the dispersion
rows have no deck. Criteria and predictions were committed before their runs (each named below). No TLSPH rung deck
was used to choose anything. Four runs have no row, because their directories were overwritten or stopped (listed
in SPEC-TL-b section 5): the first BCT check, the quad R/16 run with bulk viscosity off, the first α block run, and
the first BCT-off column rows.

Binaries: `43791edbc` (BCT, final; T-A0 on it 55 of 55 runs identical), `84e87958d` (quad two-body runs; quad code
identical in all fork binaries), the superseded first BCT commit `d88157a23` (one check run, see 19.2).

### 19.1 Item 1: BCT on the conforming sphere (static model, no engine run)

`tl_bct_sphere.py`: quarter conforming sphere at R/16, R/32, R/64, TL operators of `tl_mod.F90`, Shepard-normalised
BCT weights, contact patches of 3 to 10 spacings, exact and colour normals. Criterion committed in fork `d6b229f3c`.

- **A robust guard exists** (calibrated with exact and colour normals; the engine uses −f/|f|, not tested). No loaded particle has a non-positive guard value; the smallest is 0.911 (R/64, exact
  normal); merged particles 1.11–1.27; values up to 10.9 only at the patch edge (small weights). **Proposed
  `tl.bct_guard` = 0.45.** The stop rule did not trigger.
- **Torque error** per pair 1.06–1.36 |f| s at most, 0.18–0.63 on average; zero in total for the axisymmetric patch
  by symmetry.
- **Layer stresses under a Hertz pressure** (normal stress near the axis over the half-space Hertz value):

  | body | patch | point load: layer 1 / 2 | BCT: layer 1 / 2 / 3 |
  |---|---|---|---|
  | flat lattice-aligned block | 10 spacings | 0.732 / 0.806 | 1.075 / 0.960 / 0.986 |
  | sphere R/16 | 10 spacings | 0.761 / 0.619 | 1.043 / 0.721 / 0.850 |
  | sphere R/32 | 10 spacings | 0.824 / 0.652 | 1.094 / 0.738 / 0.856 |

  On a flat face BCT works under a non-uniform pressure too (first-order consistent; the layer-1 overshoot shrinks
  with the patch size). **On the conforming sphere layer 2 stays 26–30 % low with BCT** at R/16 and R/32 alike. The
  flat block does not show it, so it comes with the sphere's surface construction (the moved outer layer over the
  lattice) [inference for the cause]. BCT corrects the load application, not this. (The flat block was added after
  the criterion commit, as a comparison. The stress solve was not run at R/64.)
- Against the prediction: the guard part right; the stress part wrong (the point-load deficit is 13–27 %, not
  30–40 %; BCT does not bring the sphere's layers within 5 %).

### 19.2 Item 2: BCT in the fork, and its check

Sidecar `tl.bct = on` (default off), `tl.bct_guard`. b_k computed once at t = 0; one serial routine spreads
per-particle loads with the weights of 19.1, the outward normal taken as −f/|f| (no hvi normal needed), point load
kept where the guard value is below the threshold. Hooks, TL-only, hvi code unchanged: after `HVI_CONTACT_FORCES`
(contact force per particle) and around `RGWAL0` (rigid-wall force = m Δa). Prediction committed in `d88157a23`.

- **First version not kept:** spreading the kinematic wall force as it was left the wall particle short; the wall
  over-corrected each cycle (wall-force ripple 30 %, layers 0.91 / 0.95 / 1.00). Amended before any further run
  (`43791edbc`, recorded in SPEC-TL-b 5.2): each wall load is scaled so that the wall particle still receives its
  stopping force (exact for a uniform load on a flat face).
- **Check (column 2L at V/2, LAMMPS Q1 = 0.05, α = 10):** with BCT, layers 1 to 4 carry **0.9999** of the plateau
  measured from the momentum rate, at 100 and 200 particles (without: 0.65 / 0.84 / 1.01). **The task's criterion
  (within 1 %) is met.** Plateau unchanged; contact time +0.003 / +0.0016, rebound +0.003 / +0.0015. The predicted
  change below 0.002 failed at 100 particles.
- **Measurement changed after data:** the check script first divided by the `/TH/RWALL` plateau. Over that plateau
  the BCT layers are 0.673, and the check would fail. It was switched to the momentum rate after the first runs had
  been seen; the reason is the caveat below.
- **Output caveat:** with BCT the engine's `/TH/RWALL` force is the wall's kinematic stopping force, **1.485 times**
  the force transmitted to the body; the momentum rate is right. The wall's force sums and external work in the
  engine output are off by the same factor. Rungs with a rigid wall and BCT must read the wall
  force from the body momentum (`sph_rung0.py`'s `plateau_dPdt`, `contact_dPdt`; the frozen T-S0 metric reads
  `/TH/RWALL`).
- **T-A0 on `43791edbc`: 55 of 55 runs identical.**

### 19.3 Item 3: quad two-body Hertz for T-B2

Axisymmetric O-grid quad sphere on a quad cylinder (radius 3R, depth 2R, bottom fixed), Isolid 17, TYPE5 both ways,
elastic, 20 m/s, against two-body Hertz (`sph_f0w0.hertz2`). Prediction committed in `b36e0aa4f`. With the bulk
viscosity off (as the one-body quad references) the R/16 run became unstable after the rebound; all runs use the
default bulk viscosity, time-step scale 0.4.

| mesh | peak | approach | rebound |
|---|---|---|---|
| R/16 | 1.0054 | 1.0953 | 0.9988 |
| R/32 | 1.0205 | 1.0209 | 0.9995 |
| R/64 | 1.0408 | 0.9909 | 0.9996 |
| R/128 | **1.0470** | **0.9763** | 0.9997 |

In the last doubling the peak changes by +0.6 % and the approach by −1.5 %; the approach has not converged to 1 %.
Geometric extrapolation (an estimate, not a run) gives peak about 1.050 and approach about 0.9625.
- **T-B2 limits by the DECISIONS formula on the finest mesh: peak within 8.0 % (4.70 + 3.0), approach within 5.5 %
  (2.37 + 3.0)**; rebound > 0.9 kept.
- On the extrapolated errors (4.97 % and 3.75 %) the formula gives 8.0 % and **7.0 %**. Which one applies to the
  approach is for Peter.
- At R/32 the quads alone would give 5.5 % for both.
- Against the prediction: the peak and approach ranges and the limits are right. The rebound (0.9997) is outside the
  predicted 0.95–0.99, and the approach changed by more than the predicted 1 % between the finest meshes.

### 19.4 Item 4: α with the LAMMPS viscosity

Criterion committed in `b36e0aa4f`: (1) no resolved wave faster than exact (lattice dispersion, ν = 0.35);
(2) shortest-wavelength kinetic energy ≤ 1 % in a free 12³ block with a smooth initial field over 100 periods;
(3) least first-mode damping of the free bar; if two candidates are within 0.05 percentage points, the smaller
viscous + hourglass work of the block.

| α | (1) largest phase-speed ratio | (2) band share max | bar damping / period (100) | block work / KE0 |
|---|---|---|---|---|
| 0 | 0.9930 | 40.9 % | 0.5134 % | 0.992 |
| 1 | 0.9934 | 3.54 % | 0.5134 % | 1.004 |
| 3 | 0.9944 | 1.43 % | 0.5133 % | 1.026 |
| **5** | 0.9955 | 0.63 % | 0.5129 % | **1.041** |
| 10 | 0.9981 | 0.34 % | 0.5123 % | 1.071 |
| 15 | 1.0501 | — | — | — |

- As committed: **α = 5** (the bar damping of 5 and 10 differs by 0.0007 points, so the tie-break decides).
  The tie-break uses the hourglass-work diagnostic, which §17 found unreliable (both sums exceed KE0).
- α changed, so the Q1 criterion of §18.3 was rerun with α = 5: Q1 = 0.05 now rings (ripple 2.23 % at 100
  particles); **Q1 = 0.1** is selected (bar damping 1.02 % per period).
- **Recommendation (post hoc, not part of any committed criterion):** α = 10 with Q1 = 0.05 (the set-up before
  this task) also meets every criterion and damps the bar half as much (0.51 % against 1.02 % per period; column
  rebound 0.980 against 0.975). It is the worse of the two under the block-work diagnostic of the tie-break (1.071
  against 1.041). The sequential procedure does not search the pairs jointly. My recommendation for the freeze is
  **α = 10, Q1 = 0.05**; the decision is Peter's.

### 19.5 Item 5: survival probe (calibration-phase diagnostic, no verdict)

Al–Al quarter model, 800 m/s, contact only, both bodies TL with the committed outcome of this task (LAMMPS
Q1 = 0.1, α = 5, BCT on, guard 0.45), contact.stfac = 3, colour normals, t_end = 1.0 D/V. Prediction committed in its own commit `e6d7abce0`.
Reported against the E-1 gate draft §3 survival checks:

| | R/16 | R/32 |
|---|---|---|
| time reached | 0.995 D/V (t_end) | 0.995 D/V (t_end) |
| smallest dt / initial dt (≥ 0.1) | 0.204 | 0.157, at 0.996 D/V, still falling |
| dt / dt0 at 0.1, 0.25, 0.5, 0.75 D/V | 0.58, 0.43, 0.35, 0.27 | 0.46, 0.38, 0.30, 0.26 |
| detached mass (≤ 1 %) | 0 | 0 |
| closest cross-body pair (≥ 0.5 s) | 0.88 s, at 0.10 D/V | 0.89 s, at 0.02 D/V |
| det F > 0, no matrix stop | yes; smallest det F 0.885 (particle) / 0.852 (substrate) | yes; 0.856 / 0.833 |
| largest / smallest principal stretch | 2.11 / 0.21 (particle) | 2.20 / 0.21 (particle), 2.19 / 0.24 (substrate) |
| largest plastic strain | 2.2 (particle), 1.7 (substrate) | 2.9 (particle), 5.6 (substrate) |
| largest speed | 1.38 V | 1.92 V |
| kinetic energy at the end / KE0 | 0.009 | 0.010 |
| viscous / hourglass work at the end / KE0 | 0.072 / 0.104 | 0.047 / 0.065 |
| BCT guard fallbacks (particle-cycles) | 231, all after 0.975 D/V | 182 526, all after 0.815 D/V |
| engine time | 21 min (4 threads, beside T-A0) | 2 h 46 min (8 threads, alone); peak memory 5.6 GB |

Both runs pass every survival check of the E-1 gate draft §3, reported here only. They pass the kinematic switch
(0.002–0.019 D/V) by a factor of 50 and more. The energy cannot be closed: the engine gives no TL internal energy,
and the hourglass-work diagnostic is unreliable (§17).

Against the prediction (fork `e6d7abce0`): passing the kinematic switch, reaching 0.2 D/V, det F staying positive
and 0.6–0.9, and no matrix stop are right. The main prediction is wrong at both resolutions: the time step does not
fall below 0.1 dt0. It falls steadily, to 0.16 at R/32 by the end, so it would cross 0.1 later than 1.0 D/V if the
trend went on [inference]. Also wrong: detached mass stays 0 (not above 1 %), the closest pair is 0.88–0.89 s (not
0.5–0.8 s), and the largest stretch is 2.2 (not above 3). The guard fallbacks late in both runs, many at R/32, show
where BCT turns itself off; where they occur was not examined.

### 19.6 Not done

- The sphere's layer-2 deficit under BCT (19.1): its cause is inferred, not shown, and no fix is proposed here.
- The ladder's wall metrics with BCT (19.2): the rung scripts would have to read the momentum rate.
- BCT under a non-uniform rigid-wall load (the T-S1 sphere on the wall), where the wall scaling is not exact;
  contact forces with a tensile part.
- A joint (α, Q1) search; the survival probe with α = 10, Q1 = 0.05.
- CS-18b and its ladder are the cloud session's draft; Peter approves the freeze.

## 20. CS-18b core rungs: T-A0, T-S0, T-S0p pass; T-S1 fails; campaign stopped (task 2026-11-14-a)

Task: `tasks/wsl-a.md`, task 2026-11-14-a. Judge: [sph-tlsph-b-ladder.md](sph-tlsph-b-ladder.md) and hunch
[coldspray-hunch-cs18b.md](coldspray-hunch-cs18b.md), frozen in `6f0786a`. Fork `sph-hvi-contact`, branch `tlsph`,
records at `62116031a`; details in the fork's `hvi/CHANGELOG.md`, "CS-18b core rungs".

**Binary.** Built from the clean tree at `8188ca5ec`. Its solver source equals `43791edbc` byte for byte: `8188ca5ec`
undoes a comment-only change made after task 2026-11-13-c. The engine binary differs from the old `ocroot_43791edbc`
at byte 929 of the file header; I take that to be build metadata [not checked further].

**Set-up.** The ladder's set-up through the deck switch `HVI_TL_SET=cs18b`: LAMMPS viscosity Q1 = 0.1, Q2 = 0;
α = 5; BCT on with guard 0.45. Every wall force is read from the body's momentum rate (the ladder's "Metrics under
BCT"); the script switch was committed before the predictions.

**Rows.** [`results/tlb_a0.csv`](opencourant/results/tlb_a0.csv) and [`results/tlb_host.csv`](opencourant/results/tlb_host.csv).
Every row has `binary_state = committed`, fork `8188ca5ec`, ladder `6f0786a` and the deck hash. Each prediction was
committed in its own commit before its runs.

### 20.1 Verdicts

| rung | verdict | numbers | limits | prediction |
|---|---|---|---|---|
| T-A0 | PASS | 55 of 55 runs identical to the A-0 reference | identical | right |
| T-S0 | PASS | 100 / 200: plateau 1.0065 / 1.0066, contact time 0.9936 / 0.9941, rebound 0.964 / 0.976; no error grows beyond its floor | plateau 1.5 % of 1.00659, contact time 2.0 % of 0.99294, rebound ≥ 0.9318 / ≥ 0.9517 | right (not blind: the calibration column is this column at V/2) |
| T-S0p | PASS | 200: σ₂ 0.9984, plastic front 0.9883 c_b, elastic front 1.0034 c_d (errors 0.57 / 1.71 / 0.26 %) | 1.5 / 3.5 / 1.5 % of 1.00412 / 1.00544 / 1.00082 | right |
| **T-S1** | **FAIL** | R/32: contact at 10⁻² 0.890 (**5.3 %**), peak 1.049 (2.3 %), approach 0.893 (6.7 %), rebound **0.860**. R/16: numerically unstable | contact 3.5 %, peak 5.5 %, approach 7.5 %, rebound ≥ 0.9796 (R/32) | "FAIL more likely than not": right on the verdict, but the R/16 instability was not predicted |

**The campaign stops at T-S1** (task rule: a failing core rung means stop and report to Peter, no tuning).
T-tension, T-zero-energy, T-surface, T-B1–T-B3, T-survival, T-C1, T-D1 and T-D2 are not run. The T-tension
prediction had already been committed (`c49849d18`). The T-S1 run at R/64 was still running when this was written.
It cannot change the verdict, because R/32 misses its point criteria; it is added in 20.4.

### 20.2 T-S1

| | R/16 | R/32 | collocated SPH at R/32 (§18.2) |
|---|---|---|---|
| contact at 10⁻² / peak / approach / rebound | 0.36 / 11.9 / 0.66 / 1.23 | 0.890 / 1.049 / 0.893 / 0.860 | 0.964 / 1.030 / 1.014 / 0.985 |
| largest kinetic energy over the run / KE0 | **9.0** | 1.000 | — |
| kinetic energy at the end / KE0 | 1.56 | 0.74 | — |
| BCT guard fallbacks (particle-cycles) | 88 (first reported at 1.47·10⁻¹⁰ s) | 36 | — |
| smallest det F | 0.81 | 0.87 | — |

- **R/16 is a numerical instability:** energy is created (up to 9× KE0) and the force reaches 11.9 F_Hertz at
  0.36 t_Hertz.
- **R/32 is stable but soft, and the wall contact chatters.**
  - The force averages 0.89–0.99 F_Hertz from 0.30 to 0.55 t_Hertz and peaks at 1.049.
  - The contact time 0.890 is the first time after the peak that the force falls below 10⁻², the rule used for the
    references. The force comes back afterwards, up to 0.48 F_Hertz, and stays above 10⁻² until 0.968; the trace has
    20 separate contact segments (R/16: 83).
  - Under a "last time above 10⁻²" reading R/32 would pass the contact criterion (2.9 %). It fails on the rebound
    under either reading.
  - 26 % of the kinetic energy is lost in an elastic impact at 20 m/s. Where it goes is not known: the viscous plus
    hourglass work (0.33 + 0.15 KE0) exceeds the loss, and there is no TL internal energy to close the balance.
  - R/16's contact time 0.36 is an artefact of the same rule (the force stays above 10⁻² until 0.753).
- **Ladder reading:** the frozen text attaches resolutions to the approach and rebound limits but not to contact
  time and peak. The driver applies those two at R/32 and R/64, not at R/16 (which would fail them too). The
  verdict does not depend on the reading.
- **Reading [inference, not tested]:** this is the first engine case of BCT under a non-uniform rigid-wall load,
  which §19.2 named as untested. The wall scaling is exact only for a uniform load on a flat face. On the curved
  patch the wall particles do not receive exactly their stopping force, and the wall–BCT exchange can feed energy
  (R/16) or soak it up (R/32). The conforming sphere's layer-2 deficit (§19.1) may add to the softness. No run
  separates the two (for example T-S1 with BCT off), because that would be tuning after a failure.

### 20.3 Reported (not judged)

- **BCT guard fallbacks** in every run, in particle-cycles: 32 in each T-S0 and T-S0p run; T-S1 as in 20.2.
  Locations were not examined.
- **Energy closure:** not available (no TL internal energy in the fork).
- **T-S0p rerun:** the first T-S0p run wrote its rows as "dirty tree", a false positive (the tracked result csv
  the run writes counted as a modified file). After the fix the run was repeated, with the same values; the first
  run has no committed row.
- **Data loss during a disk clean-up on 2026-11-14** (my error, not part of a run): an over-broad deletion removed
  the VTK frames and restart files of this campaign's run directories and of those of task 2026-11-13-c. All rows
  and saved analysis arrays are intact; the raw frames could only be regenerated by rerunning.

### 20.4 T-S1 at R/64

**Reported, after the verdict** (added 2026-11-14; it cannot change the CS-18b verdict). R/64 meets all its own
criteria:

| | R/16 | R/32 | R/64 | R/64 limit |
|---|---|---|---|---|
| contact at 10⁻² | 0.36 | 0.890 | 0.938 (0.2 %) | 3.5 % |
| peak | 11.9 | 1.049 | 1.040 (3.1 %) | 5.5 % |
| approach | 0.66 | 0.893 | 0.939 (1.9 %) | 4.0 % |
| rebound | 1.23 | 0.860 | 0.9788 | ≥ 0.9746 |
| contact segments above 10⁻² | 83 | 20 | 9 | — |
| kinetic energy at the end / KE0 | 1.56 | 0.74 | 0.96 | — |
| viscous / hourglass work / KE0 | — | 0.33 / 0.15 | 0.020 / 0.007 | — |
| BCT guard fallbacks | 88 | 36 | 16 | — |

No R/64 error exceeds its R/32 value + 0.01. **The T-S1 verdict stays FAIL**, because R/32 fails its point
criteria. The failure is strongly resolution-dependent. My reading, untested: the wall–BCT exchange on a curved
patch that holds few particles goes wrong, and the effect fades with resolution. The chatter is still there at R/64
but no longer harms the metrics. Run time 1 h 26 min for all three resolutions (8 threads); peak memory 10.0 GB
(R/64).

### 20.5 Diagnostic: T-S1 at R/32 with BCT off (task 2026-11-14-b)

One run, no verdict. Same binary (`8188ca5ec`) and decks as task a, with `tl.bct = off` (fork deck switch
`HVI_TL_BCT=off`, which also drops `tl.bct_guard`). Row `results/tlb_diag.csv` (`kind = diagnostic`, fork deck
commit `3e3c2ae22`, deck hash `884329d1b58fcdc0`, `binary_state = committed`). The prediction was committed before
the run (fork `50e37b5d5`). The first start stopped at the engine's input check (the guard key is refused with
BCT off) before any time step; it was rerun after the deck fix, and has no row. Trace quantities come from the fork
script `hvi/scripts/tlb_s1_trace.py`, which reproduces the 20.2 and 20.4 values.

| | R/32 BCT on (20.2) | **R/32 BCT off** | R/64 BCT on (20.4) |
|---|---|---|---|
| contact at 10⁻²: first drop / last time above | 0.890 / 0.968 | 0.927 / 0.926 | 0.938 / 0.942 |
| peak / approach / rebound | 1.049 / 0.893 / 0.860 | 1.060 / 0.928 / **0.9988** | 1.040 / 0.939 / 0.9788 |
| largest / final kinetic energy / KE0 | 1.000 / 0.74 | 1.000 / 0.998 | 1.000 / 0.96 |
| smallest det F | 0.87 | 0.92 | 0.88 |
| contact segments above 10⁻² | 20 | 4 | 9 |
| viscous / hourglass work / KE0 | 0.33 / 0.15 | 0.0016 / 0.0001 | 0.020 / 0.007 |

"First drop" is the first sample below 10⁻² after the peak, so it can lie one sample after "last time above".

- With BCT off, three of the four segments are blips below 0.015 F_Hertz in the first 1 % of t_Hertz; then the
  contact is one clean segment. With BCT on, 11 segments of 0.2–0.65 F_Hertz come before the main contact (from
  0.096 t_Hertz) and 8 of up to 0.48 F_Hertz follow it.
- **Reading, by the rule fixed in the task before the run:** rebound 0.9988 ≥ 0.9796. The wall–BCT coupling is the
  main cause of the R/32 failure, so **BCT is not carried unchanged into CS-19 for curved contact.**
- Reported, not judged: with BCT off the other R/32 errors (contact 1.4 %, peak 1.2 %, approach 3.0 %) also lie
  inside the R/32 limits. This is not a rescue of CS-18b, and nothing is tuned on it.
- What it does not show: BCT was built for the plane-wall end layer (§19, T-S0); this run does not test BCT off on
  flat faces.
- My prediction was wrong: I expected the rebound to stay below 0.9796 (0.92–0.96). The chatter and the viscous
  work dropped as predicted, but much further (viscous work 200× smaller).
