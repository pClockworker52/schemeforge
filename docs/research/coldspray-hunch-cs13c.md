# Cold spray: CS-13c, protocol amendment of CS-13 (3D brick particle on brick substrate, k = 0 twin), registration (frozen)

Drafted 2026-11-05. **Status: frozen** 2026-11-05, approved by Peter (with the check-E fallback below). This commit
comes before any run of this protocol. Hunch statement and mechanism: unchanged from [coldspray-hunch-cs13.md](coldspray-hunch-cs13.md).
This file replaces the test protocol of [CS-13b](coldspray-hunch-cs13b.md). CS-13b was blocked before its runs and
has no verdict (opencourant-verification.md §12). CS-13's original 2D protocol stays for the JAX route.

## Why this protocol

- **Conduction does not work on the SPH particle.** H0-SPH fails at 2.5 %. A conductive brick substrate under an
  adiabatic SPH particle either exhausts memory or heats the particle to about 9·10⁴ K by artefact (§12.2).
- **Conduction works on bricks** (§11.2 control: 0.28 % → 0.017 %).
- **A brick particle on a brick substrate** gives both bodies the same heat path. It is the 3D counterpart of
  CS-13's original 2D case: Lagrangian on both sides, with edge collapse on both sides. CS-13's claim covers both
  edges.
- **The twin is k = 0 with `/HEAT/MAT`,** not a run without `/HEAT/MAT`. With `/HEAT/MAT` the brick temperature
  comes from a different heat source (nodal, from strain energy) than without it (element internal energy), and the
  peak changes from 737 to 534 K before any conduction acts (§12.2). With both twins on the same heat path, **the
  only difference between them is k**.

## Frozen protocol

### Setup

- **Particle:** Al sphere, R = 7.5 µm, quarter symmetry, 8-node bricks `Isolid = 17` (the formulation frozen in
  §10.2). O-grid mesh (cube core plus mapped shells), regular along the lower surface, element edge s near the
  contact.
- **Substrate:** brick block 3R × 3R × 2R (quarter), bottom fixed. Edge s for x, y ≤ 1.5R and z ≥ −1.5R, graded
  outside (ratio 1.2), as in setup F.
- **Material, both bodies:** LAW4 Johnson–Cook + `/EOS/GRUNEISEN` from P-HG-Al (γ₀ = 2.17). No erosion, no failure
  model.
- **Contact:** two `/INTER/TYPE7`, each body's nodes as secondary on the other's surface, friction 0. Gap and Stfac
  are chosen in rung B0 and frozen with it. **No heat transfer across the contact,** as in CS-13b.
- **Thermal, both twins:** `/THERMAL`, and `/HEAT/MAT` on both bodies with ρc_p from P-HG-Al.
  - **conductive twin:** k = 237 W/(m K) (P-HG-Al);
  - **k = 0 twin:** k = 0, everything else identical.
- **Run stop** at the time-step collapse dt₀/50 or at t_e = 0.25 D/V. Engine runs under the memory and time caps of
  `sphdeck.run` (§12).

### Prerequisite rungs

- **B0, brick-on-brick contact:** elastic brick sphere on an elastic brick block, 20 m/s, R/16 and R/32, against
  two-body Hertz (E* = E / (2 (1 − ν²))). Pass at R/32: peak force and maximum approach within 5 %, rebound > 0.9 V.
  Gap and Stfac are chosen here and frozen. This is the brick analogue of F0.
- **H0-k0:** the §11.2 brick H0 slab with k = 0 and `/HEAT/MAT`. Pass: the temperature changes by no more than
  0.1 K over the run. This checks that the twin really does not conduct. H0 with k = 237 on bricks has already
  passed (§11.2) and is not repeated.
- **E, energy check in every run (new, from §12):**
  - the total heat Σ m c_p (T − T₀) over both bodies must not exceed the initial kinetic energy of the particle by
    more than 5 %;
  - no element's temperature may exceed T_melt = 933 K (P-HG-Al) unless its own plastic work accounts for it.
    The engine's local plastic-work energy is the reference, with a 10 % tolerance.

  If OpenCourant gives no per-element plastic-work output, the second clause is reported only, and the
  total-energy bound stays binding.

  A run that fails E is invalid. If any run needed for a verdict is invalid, CS-13c is inconclusive.

### Runs

500, 800 and 1100 m/s × R/16, R/24, R/32, R/48 × the two twins: **24 runs**. Also, reported only, one run per
velocity at R/16 without `/HEAT/MAT` (the adiabatic heat path of §8.3), to show the size of the heat-source change.

### Metrics

- **P1, failure time t_f:** the run stop time. A run that reaches t_e without collapse counts as not failed. The
  body containing the controlling element is recorded.
- **P2, edge plastic strain:** for **each body**, the maximum equivalent plastic strain within a fixed physical
  distance of 1.17 µm of its contact edge, at t_c. The contact edge is that body's outermost surface node in contact.
  t_c = 0.5 × the smallest t_f among all runs at that velocity, both twins.
- **P3, reported only:** conductive minus k = 0 peak edge temperature and plastic strain, at every spacing.

### Verdict rule

Tolerance **6 %** for the step R/32 → R/48, as in CS-13b.

- **Supported** if, at two or more of the three velocities, all three hold:
  - conductive t_f changes by at most 6 % from R/32 to R/48, or neither run fails;
  - conductive P2 changes by at most 6 % from R/32 to R/48 **in both bodies**;
  - the k = 0 twin fails at least one of the two above at that velocity.
- **Refuted** if either holds:
  - at all three velocities, conductive t_f falls by more than 6 % from R/32 to R/48 and P2 changes by more than 6 %
    in either body;
  - conductive and k = 0 twins agree within 6 % in t_f and P2 at every velocity and spacing.
- **Inconclusive** otherwise, or if a rung fails, or if a run needed for the verdict fails check E.

### Budget

Estimated from §10.5 and the element counts (about 0.8 million bricks at R/48), each R/48 run takes several
minutes to about half an hour. Stop rule as in CS-13b: if one R/48 run takes more than 1 h, stop and report before
the rest.

## Known limits

- **The thermal length at failure is only 1–3 spacings,** as in CS-13b. "Inconclusive" is a real outcome.
- **The particle side can collapse first.** That is allowed: the claim covers both edges, and P2 is judged in both.
- **One solver.** A supported result from OpenCourant alone does not carry CS-13; the JAX route is the independent
  check.
- **Check E is a new metric.** Its first use is a sanity bound, not a verdict, so the metric-rung rule is met by its
  definition: it is an energy balance with an exact upper bound.
