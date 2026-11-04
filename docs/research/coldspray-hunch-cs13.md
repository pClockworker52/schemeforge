# Cold spray: hunch CS-13 (heat conduction gives the contact edge its length scale), registration draft

Drafted 2026-11-04 (perspective A after CS-11). **Status: draft.** It is frozen when Peter approves it, and that
commit comes before any run with conduction. Research track, not a ledger arena. Background:
opencourant-verification.md §8.3 (2D Lagrangian), §10.5 (3D, setup F).

## Observation behind it

Every Lagrangian impact run so far fails at the contact edge, and **fails earlier as the spacing is refined**:
- 2D `Isolid = 17`, Al–Al, 500–1000 m/s, R/16 to R/64 (§8.3, also with γ₀ = 2.17);
- 3D bricks under the SPH particle, 500–1100 m/s, R/16 to R/32 (§10.5).

The edge plastic strain does not converge either. This is the classic signature of **localisation in a problem
without an intrinsic length scale**, as for adiabatic shear bands. All runs are adiabatic. Temperature comes only
from plastic work, softens the material through Johnson–Cook, and cannot diffuse. Rate sensitivity is weak
(JC C = 0.001). Nothing in the model sets a width for the edge band except the mesh.

The physical length that acts at this scale is the thermal diffusion length ℓ_th = √(κ t), with κ = k/(ρ c_p). As an
order of magnitude only (k ≈ 237 W/(m K) from memory; ρ, c_p from P-HG-Al), ℓ_th ≈ 0.7 µm at t = 5 ns. That is
comparable to the spacings used (0.47 µm at R/16 for R = 7.5 µm) and to the jet thickness. HG2018a attributes the
LIPIT size effect to thermal diffusion, which fits.

## Hunch

```yaml
- id: CS-13
  registered: draft 2026-11-04 (frozen on Peter's approval)
  assumption_broken: >-
    The adiabatic assumption of the impact simulations (and of most published cold-spray impact models at
    micrometre scale), which proposed H8 depends on: the edge problem is well posed without heat conduction.
  statement: >-
    With physical heat conduction, the Lagrangian edge fields of a normal Al-Al impact converge in mesh spacing,
    and the mesh failure no longer comes earlier with refinement, once the spacing is below the thermal diffusion
    length over the edge time scale.
  mechanism: >-
    Adiabatic thermal softening drives the edge shear band to the smallest width the mesh allows, so the band,
    the element distortion and the failure time are set by the mesh. Conduction removes heat from a band narrower
    than about l_th faster than it is generated, which sets a minimum band width; below that width refinement
    changes nothing.
  counter_mechanism: >-
    The failure is geometric (the jet root folds the mesh whatever the band width), or the regularising scale is
    mechanical (rate sensitivity, inertia), in which case conduction changes the edge little and the trend stays.
  predicted_effect:
    - {metric: "P1: time of mesh failure t_f, per velocity, over R/16, R/32, R/64", direction: "converges",
       size: "|t_f(R/64) - t_f(R/32)| / t_f(R/32) <= 0.10"}
    - {metric: "P2: edge equivalent plastic strain at a common time t_c, per velocity", direction: "converges",
       size: "change between R/32 and R/64 <= 10 %"}
    - {metric: "P3 (reported, no verdict): adiabatic minus conductive edge fields at the same spacing",
       direction: "conduction lowers peak edge temperature and strain", size: "not predicted"}
  kill_criterion: >-
    Test: the §8.3 2D Lagrangian diagnostic (Isolid = 17, Al-Al, R = 10 um, 500 / 750 / 1000 m/s, R/16, R/32,
    R/64, no erosion), unchanged except that heat conduction is switched on with sourced Al conductivity. t_c =
    0.5 x the smallest t_f among the runs at that velocity, adiabatic runs of §8.3 included. A conductive run that
    reaches the end time of §8.3 without failing counts as converged for P1. Refuted if, at all three
    velocities, t_f still falls with refinement by more than 10 % from R/32 to R/64 and P2 fails. Supported if P1
    and P2 both hold at two or more of the three velocities. Inconclusive otherwise, or if the prerequisite rung
    fails.
  prerequisite_rung: >-
    H0: conduction alone, 1D slab with a step in temperature (or a constant surface flux), on the element used,
    against the erfc solution: temperature profile within 2 % at the finest spacing, and temperature written out.
    Two open items from §5 and §8 must be solved here first: /HEAT/MAT gave T ~ 0 on quads, and T is computed but
    not written out with Isolid = 17. If OpenCourant cannot pass H0 with Isolid = 17, CS-13 goes to Peter before any
    impact run (the 2D-axisymmetric JAX code is the fallback, as DECISIONS 2026-11-04 allows).
  inputs_needed: >-
    Thermal conductivity of Al (and of the alloys later), sourced into properties.csv before the freeze; nothing
    filled from memory. The 237 W/(m K) above is an order-of-magnitude remark and enters no rule.
  known_relatives:
    - thermal and viscous regularisation of adiabatic shear bands (classic numerics and shear-band literature;
      not read in this track)
    - HG2018a (thermal diffusion as the origin of the LIPIT size effect)
    - Assadi2003 and later FE studies of cold spray (whether they include conduction and test convergence: to check)
  provenance: Perspective A after CS-11 (2026-11-04), from the "fails earlier with refinement" pattern of §8.3 and
    §10.5.
  label: none yet (referee); expected "rediscovery" for the numerics, possibly "variant of" for its use here
  status: draft
  author: claude (with Peter)
```

## Why it is next to CS-12

CS-12's simulation part (T2, and the conditional-independence test) needs interface-state histories up to the end
of contact. Today no bulk solver survives the contact edge that long. If CS-13 holds, the 2D Lagrangian route with
conduction may survive long enough. The particle–substrate interface would then still need its blanket law (CS-12),
but the bulk would no longer be the bottleneck.

**If CS-13 is refuted,** the edge failure is geometric or mechanical. The bulk problem then needs a different
answer (ALE, remeshing in our own code) before CS-12 can be simulated, and that is a result for the ledger.

## What CS-13 cannot show

- Convergence with conduction says the edge problem is well posed. It does not say the fields are right; that
  needs measured data (CS-12 T1/T2).
- One material, one size. The size effect is reported (P3 and later runs at other R) but not judged here.
- Convergence of t_f is a weak metric. P2 (edge strain at a common time) is the stronger one, and both are needed
  for support.
