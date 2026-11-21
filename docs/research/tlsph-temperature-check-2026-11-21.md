# TLSPH temperature check: do TL particles heat, soften with it, and write it? (spec and prediction, fixed before reading)

Written 2026-11-21 (cloud, modeller) at Peter's request. `kind = check`; no hunch, no budget.

## Why

- The record never checked that TL particles heat. §26 states that cs12's σ_flow is "SIGY of the material call
  (LAW4: rate and adiabatic temperature included)". The D-3 check (σ_flow/σ_y 1.0000) ran at small strain, where
  heating is negligible.
- TLSPH has its own stress path in the fork (SPEC-TL). If it skips LAW4's adiabatic update or passes a fixed
  temperature, every TLSPH impact so far ran **without thermal softening**: CS-18b survival (§19, §23), §26, §30
  (CS-22) and CS-22b.
- On 2D quads the temperature was computed and used but not written (§32), and softening is active from the first
  frame with the edge above T_m (§33). Whether TLSPH matches is unknown.

## Q1: source (no run)

With file and line references in the fork (`sph-hvi-contact`, engine `27e53d5f0`):
1. For a TL particle, is LAW4 called so that its adiabatic temperature is updated each cycle (σ_y dε_p/ρc_p, plus
   any q or EOS part) and the updated temperature is used in that particle's σ_y in the following cycles?
2. Which buffer do the SPH/TL animation, H3D and time-history outputs write as temperature?
3. Which temperature does cs12's σ_flow,ij use?

## Q2: data (no new run)

From the existing §30 runs AL08off and AL16off (Al–Al 600 m/s, P-HG-Al, engine `27e53d5f0`), at the last written
frame and at one frame near 0.5 t_p:
- the written particle temperature, if any;
- a plastic-work lower bound per particle, T_lb = T_r + ∫σ_y dε_p/(ρ c_p), integrated over the written frames from the
  particle's written ε_p (as §32, with rate factor 1; P-HG-Al: ρ 2700, c_p 896.9, T_r 293 K, T_m 933 K, JC A 148.4,
  B 345.5 MPa, n 0.183, m 0.895);
- T_max / T_m, and the share of particles with ε_p > 0.5.
If no temperature is written for SPH, Q2 reports "not written" and Q1 decides.

## Rule (fixed now)

- **(a) heats and writes:** Q1 shows the update is used in σ_y, and the written T ≥ T_lb − 1 K for at least 95 % of
  particles with ε_p > 0.5, on both meshes.
- **(b) heats, not written:** Q1 shows the update is used in σ_y, but the written temperature is T₀ (or absent).
- **(c) does not heat:** Q1 shows no temperature update is used in σ_y (TLSPH runs are thermally unsoftened).
- **(d) other:** anything else (e.g. written T below T_lb, or Q1 unclear): stop and report.

## Prediction (judgment, before any reading)

(a) 0.35, (b) 0.35, (c) 0.25, (d) 0.05.

## Facts checked (procedure)

solver-facts.md §1 (quad temperature, LAW4 heating), §3, §4. Not covered: TLSPH heating and its temperature output,
which is the subject of this check.

## Consequences (decided after the result, not now)

- (c): every TLSPH impact result is re-read as "no thermal softening". CS-22b's verdict is unaffected (its rule does
  not use T), but its physical reading is.
- (b): an output change as in §33.
