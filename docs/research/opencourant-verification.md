# OpenCourant verification: feature check and rung 0 (elastic, elastic-plastic)

Session of 2026-11-03. Solver: OpenCourant `latest-20261011` (commit `cb760c2`), local install, 1 process,
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
| Adiabatic heating? | **LAW4 built-in temperature works** (T from internal energy, 293 → 880 K peak in the confined plate). **`/HEAT/MAT` does not give a usable temperature on axisymmetric quads**: T stays near 0 K (not even T₀), with or without engine `/THERMAL`. So no Taylor–Quinney fraction for now. |
| Rung 0 (elastic) against the exact solution? | **Agrees.** Contact time error +1.05/+0.36/−0.04/−0.31 % and rebound 0.965/0.978/0.986/0.991 V at 25/50/100/200 elements (variant A, closest to the JAX settings). JAX: +1.9/+0.9/+0.7/+0.4 %, 0.966/0.979/0.987/0.992 V (reproduced here). |
| Plateau force | **+0.66 % at every mesh**: a finite-strain effect, ≈ 0.42 × V/c_d, which vanishes as V → 0. Quads have no small-strain option (starter error 1223). JAX is linear and exact. |
| Rung 0p (elastic-plastic two-wave) | **Agrees with the closed form** with q ≈ 0: wall stress σ₂ to 0.9997 at 200 elements, plastic front speed 0.993 c_b, elastic front 0.997 c_d; ε_p behind the plastic wave 1.05 (q ≈ 0) and 0.986 (default q) of the closed form. |
| Pitfalls found | (1) The rigid-wall force output `FNZ` is ∫σ dr, not a force, in axisymmetric runs. (2) Default quadratic bulk viscosity + default time-step scale goes unstable (zero volume at cycle 0) on 50:1 quads. (3) Default bulk viscosity costs 5–7 % rebound velocity in the elastic case. |

## 1. Method

**Geometry and boundary conditions** (`ocdeck.write_plate_deck`).
- SI units (`/BEGIN` kg m s, deck version 2026). `/ANALY` N2D3D = 1. Quads in the YZ plane: Y = r, Z = axis.
- Plate 0 ≤ r ≤ R, 0 ≤ z ≤ L, uniform mesh, `/PROP/TYPE14` (Isolid 0 → default).
- Frictionless rigid plane `/RWALL/PLANE` (Slide = 0) at z = 0, normal +z, all nodes as secondary nodes.
- `/INIVEL` −V on all nodes, so the plate starts in contact.
- `/BCS` fixes u_r (and x) on the axis. For the confined cases it fixes u_r on all nodes. The starter then reports warning 312, "incompatible kinematic conditions", for the nodes that carry both `/BCS` and the wall; the elastic results below show no effect.

**Output.** Axisymmetric time-history quantities are **per radian**: `MASS` = ρL³/2 to machine precision, versus
ρπL³ for the full ring.
- The wall force is taken as F = 2π·d(ZMOM)/dt from the part time history, written every cycle (`/TFILE` below the time step). The wall is the only axial force, so this is exact up to the 7 printed digits.
- **Finding:** the `/TH/RWALL` column `FNZ` equals −∫σ_zz dr, measured as −1.0066·σR at R = L and 2L and n_r = 4 and 8. It is not a force per radian (which would be σR²/2). Do not use the rigid-wall time-history force in 2D axisymmetric runs without this conversion; it is only valid for uniform σ.

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

*Unconfined plate, 500 m/s, mirrored about the axis. Feature check only; the material values are nominal.*

## 3. Rung 0: elastic confined plate (comparison with the JAX code)

E = 70 GPa, ν = 0.35, ρ = 2700 kg/m³, L = R = 10 µm, n_r = 4, V = 100 m/s.
c_d = 6450.54 m/s, t_c = 2L/c_d = 3.1005 ns, F_exact = ρc_dVπL² = 0.54715 N.

JAX rows: `confined_plate_on_rigid_wall` rerun in this session (`uv run`, x64), identical to Peter's numbers.

| n_z | JAX plateau | JAX contact | JAX rebound | OC A plateau | OC A contact | OC A rebound | OC B contact | OC B rebound | OC C contact | OC C rebound |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 1.0000 | 1.0190 | 0.9656 | 1.0066 | 1.0105 | 0.9645 | 1.0156 | 0.9680 | 1.0001 | 0.9334 |
| 50 | 1.0000 | 1.0088 | 0.9790 | 1.0066 | 1.0036 | 0.9779 | 1.0046 | 0.9804 | 0.9976 | 0.9454 |
| 100 | 1.0000 | 1.0072 | 0.9871 | 1.0066 | 0.9996 | 0.9858 | 1.0000 | 0.9873 | 0.9942 | 0.9545 |
| 200 | 1.0000 | 1.0038 | 0.9920 | 1.0066 | 0.9969 | 0.9905 | 0.9970 | 0.9915 | **stopped** | **stopped** |

The full table, with KE ratio, `FNZ` and cycle counts, is in
[`results/rung0_opencourant.csv`](opencourant/results/rung0_opencourant.csv). Engine time ≤ 0.2 s per run.

![Rung 0 comparison](opencourant/figures/rung0_compare.png)

**Findings**
- **Rebound velocity:** OpenCourant without viscosity (A, B) and JAX converge alike: deficit 3.5 → 2.2 → 1.4 → 0.9 % (JAX 3.4 → 2.1 → 1.3 → 0.8 %), a factor of about 1.6 per mesh doubling (order ≈ 0.7) in both. The two codes differ by ≤ 0.004 V at every mesh.
- **Contact time:** OpenCourant converges from above and crosses 2L/c_d at about 100 elements, ending at −0.3 % at 200. That fits the finite-strain stiffening below (the wave runs about 0.3 % faster at this strain); JAX stays above.
- **Plateau +0.66 %, the same at every mesh, time step and viscosity.**

  | V (m/s) | strain V/c_d | plateau − 1 | ratio (plateau − 1) / strain |
  |---|---|---|---|
  | 1 | 1.6e-4 | +0.00006 | 0.40 |
  | 10 | 1.6e-3 | +0.00065 | 0.42 |
  | 100 | 1.6e-2 | +0.00659 | 0.43 |
  | 1000 | 0.155 | +0.0696 | 0.45 |

  (A settings, 100 elements.) The excess scales with the strain and vanishes as V → 0, so it is the
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

## 5. Rules for our own decks (from the above)

1. Take wall forces from momentum (2π d(ZMOM)/dt per part) or from element stresses, not from `/TH/RWALL` FNZ.
2. Remember that axisymmetric time-history output is per radian (×2π for the ring).
3. Use time-step scale 0.4 (`/DT`) or keep the element aspect ratio ≤ about 10 if default bulk viscosity is on.
4. Verification against linear solutions: q ≈ 0 and V ≤ 10 m/s (finite-strain excess ≤ 0.07 %).
5. Temperature in 2D: LAW4 built-in only, until `/HEAT/MAT` is understood. Report that it includes compression energy.
6. Velocity sweeps: plain text decks, starter + engine via `subprocess`, one directory per case (`ocdeck.run`); about 0.1–4 s per run at these sizes.

## 6. Open items

1. `/HEAT/MAT` on axisymmetric quads (T ≈ 0): test on 3D bricks; look for a 2D thermal option. This blocks a Taylor–Quinney fraction.
2. JC + Grüneisen against a closed form: a confined plate with an EOS has a Hugoniot solution (elastic precursor + shock). That would be rung 0p with LAW4 instead of LAW2, and the JAX code would need an EOS.
3. Warning 312 (`/BCS` + rigid wall on the same nodes): harmless here; check again with friction or sliding.
4. The tension behind the front in the QA copper rod ([openradioss-setup.md](openradioss-setup.md) §3.3): rung 0p shows clean fronts with q ≈ 0 and with q default on our meshes, so the cause there is more likely the coarse QA mesh or the `/BCS`-held face than the solver. Not re-run.
5. Rung 1 (Hertz sphere, JAX has it): needs a sphere mesh in `ocdeck`; next in the ladder.
