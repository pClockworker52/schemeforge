# Cold spray: CS-13b, protocol amendment of CS-13 (3D setup F instead of 2D quads), registration (frozen)

Drafted 2026-11-05. **Status: frozen** 2026-11-05, approved by Peter as written. This commit comes before any
conductive impact run. Hunch statement and mechanism: unchanged from [coldspray-hunch-cs13.md](coldspray-hunch-cs13.md)
(frozen 2026-11-05). This file replaces only the test protocol, for OpenCourant.

## Why an amendment

CS-13's prerequisite rung H0 failed for a structural reason: OpenCourant has no heat conduction on 2D quads, with any
formulation (opencourant-verification.md §11.2). On 3D bricks, the same H0 deck matches erfc to 0.03–0.3 % and
converges. The edge failure CS-13 is about also occurs in 3D: in setup F of CS-11, the substrate bricks at the contact
edge collapse at 0.07–0.17 D/V, earlier with refinement (§10.5). So the test moves to setup F. The 2D protocol of
CS-13 stays valid for the JAX route; if both are ever run, they are reported separately.

## Frozen protocol

### Setup

Setup F as frozen in CS-11 and §10.2, unchanged:
- SPH particle (surface-conforming, §9.1 settings) on 8-node bricks (`Isolid = 17`);
- `/INTER/TYPE7`, friction 0, gap s/2, Stfac 10;
- quarter symmetry, block 3R × 3R × 2R, bottom fixed;
- Al LAW4 Johnson–Cook + `/EOS/GRUNEISEN` (P-HG-Al, γ₀ = 2.17);
- R = 7.5 µm, no erosion, no failure model;
- run stop at the time-step collapse dt₀/50, as in §10.5.

**Conduction (the only change in the conductive runs):**
- `/HEAT/MAT` with k = 237 W/(m K) (P-HG-Al, `k_W_mK`), ρc_p from P-HG-Al, engine `/THERMAL`, in the bricks.
- In the particle too, if rung H0-SPH passes. If H0-SPH fails, the particle stays adiabatic; this is recorded, and
  the test goes ahead, because the failing elements are the substrate bricks.
- **The contact is adiabatic:** no heat crosses TYPE7. This keeps the interface out of the test. The edge band
  that fails sits in the substrate.

### Prerequisite rungs

- **H0-brick:** already passed (§11.2 control: 0.28 %, 0.068 %, 0.017 %). It is not repeated.
- **H0-SPH:** the H0 slab built from SPH particles (cubic net, §9.1 settings), against erfc at t = 10 ns. Pass:
  within 2 % at the finest spacing, with the temperature written out.

### Runs

- Velocities: 500, 800 and 1100 m/s, where adiabatic diagnostics already exist.
- Spacings: R/16, R/24, R/32 and **R/48**.
- Each case is run twice, adiabatic and conductive, with the same deck otherwise: 24 runs.
- The adiabatic runs are rerun, not taken from §10.5, because the §10.5 refinements were diagnostics outside a
  protocol. The §10.5 values are reported for comparison (P0, no verdict).

The thermal diffusion length √(κt) is about 0.44 µm at the observed failure times (about 2 ns at 800 m/s) and about
0.7 µm at 5 ns (κ = 9.79·10⁻⁵ m²/s). The spacings are 0.47, 0.31, 0.23 and 0.16 µm. CS-13's condition, spacing below
the thermal length, holds from R/24 on. R/48 is added so that two refinements lie inside that range.

### Metrics

- **P1, failure time t_f:** the run stop time. A run that reaches t_e = 0.25 D/V without collapse counts as not
  failed.
- **P2, edge plastic strain:** the maximum equivalent plastic strain in substrate bricks within a fixed physical
  distance of 1.17 µm (2.5 × R/16) of the contact edge, at t_c. The contact edge is the outermost substrate surface
  node in contact. t_c = 0.5 × the smallest t_f among all runs at that velocity, adiabatic and conductive. The same
  quantity for the particle body is reported, with no verdict.
- **P3, reported only:** conductive minus adiabatic peak edge temperature and plastic strain, at every spacing.

### Verdict rule (replaces CS-13's kill criterion for this route)

The refinement step R/32 → R/48 is a factor 1.5, not 2. CS-13's tolerance of 10 % per halving therefore becomes
**6 %** for this step (10 % × log 1.5 / log 2 ≈ 5.8 %, rounded).

- **Supported** if, at two or more of the three velocities, all three hold:
  - conductive t_f changes by at most 6 % from R/32 to R/48, or neither run fails;
  - conductive P2 changes by at most 6 % from R/32 to R/48;
  - the adiabatic twin fails at least one of the two above at that velocity. This control shows that conduction
    made the difference.
- **Refuted** if either holds:
  - at all three velocities, conductive t_f still falls by more than 6 % from R/32 to R/48 and P2 changes by more
    than 6 %;
  - conductive and adiabatic t_f and P2 agree within 6 % at every velocity and spacing, so conduction does not
    change the edge.
- **Inconclusive** otherwise, or if rung H0-SPH fails and the particle-side band turns out to control t_f (the
  controlling element is a particle, not a brick).

### Budget

From §10.5, the R/32 runs took 77–214 s. R/48 is estimated at about 5 times that per run, so the 24 runs are a few
hours. If one R/48 run takes more than 1 h, stop and report before the rest.

## Known limits

- **The thermal length at failure is only 1–3 spacings,** even at R/48. Regularisation may just begin to show, so
  "inconclusive" is a real outcome, not a failure of the protocol.
- **The adiabatic contact removes heat flow across the interface,** which is physical in reality. The test is about
  the bulk edge band, not the interface; CS-12 handles the interface.
- **One solver.** A supported result from OpenCourant alone does not carry CS-13. The JAX route (2D, CS-13's
  original protocol) is the independent check.
