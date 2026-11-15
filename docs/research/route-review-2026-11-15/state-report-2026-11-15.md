# Cold-spray simulation: state report (copy)

Verbatim copy of the Claude Docs report "Cold-spray simulation: state report" (https://claude.ai/artifact/FVpVQWN2M7Uny4FwYzMxyS), doc revision 20, read 2026-11-15 for the route review; converted to Markdown, wording unchanged. The Claude Docs version is the live one.

2026-11-15 · Peter Scholz

## Summary

No solver configuration has yet passed its frozen verification ladder for elastic contact, so no cold-spray result can be claimed. The latest calibration (2026-11-15, §22) settled the open question against us: without the BCT correction, the first particle layer of a loaded TLSPH face carries only 0.5–0.6 of the true stress, under any contact, and 0.5 µm averages miss the 3.5 % rule (4 of 20 within it at R/32, 6 of 20 at R/64). By a rule fixed before the run, this is a failure: the next step is a review of the route, not another fix.

- **Track A** (experimental v_cr data) is waiting on step 1 of the last three blind papers.
- **Track B** (a 3D particle solver that computes the interface state) has had four configurations stopped by their ladders since 2026-11-08.
- **Common pattern:** every failure so far was a failure at a body surface, which is exactly where the interface state lives.

## Goal and requirements

The goal is a simulation of a single cold-spray particle impact that predicts whether and where the particle bonds, from material properties, without fitting to the outcome being predicted. The first claim must deliver, together (owner's decision of 2026-11-12, amended 2026-11-14):

1. particle shape and flattening, rebound and the critical velocity v_cr;
2. the interface state (contact pressure p_n, surface expansion Y, temperature, bonded area), judged as averages over 0.5 µm; point values at the contact edge are reported only;
3. in 3D, with the bond acting inside the solver during the impact (bonded areas carry tension and change the rebound), not evaluated afterwards.

The bonding law the solver is meant to host is a Bay-type cold-welding criterion: a point bonds when its surface expansion exceeds a threshold Y′ and the contact pressure exceeds an extrusion pressure (hunch CS-12). The requirement set was re-examined on 2026-11-14 and kept; a one-way bond (contact only, criterion evaluated afterwards) is the documented alternative.

## How we judge

A solver configuration counts only after it passes a frozen ladder of test cases with exact or converged reference solutions. Experimental agreement alone is not accepted. The rules:

- **Hunch:** a registered claim with mechanism, predicted effect and kill criterion, frozen before its tests. At most five may be open and untested at once; three are open now.
- **Ladder:** the ordered test cases (rungs) and their thresholds, frozen with the hunch. Thresholds are 1.25 × the error of a method known to work (quad finite elements or collocated SPH) on the same case, or that method's error + 3 points for surface and contact rungs.
- **Stop rule:** a failing core rung refutes the hunch, and the campaign stops. A fix is a new hunch, frozen before its runs. Nothing is tuned after a freeze; calibration before a freeze uses cases that are not rungs.
- **Predictions first:** each campaign's prediction is committed before its runs, and every result row names the committed solver binary.
- **Blind papers:** a closed list of experimental papers (B01–B16) was withheld from the modeller. An approved extractor passes on inputs only; predictions are frozen; then outcomes are read and scored.
- **Labels:** results are called rediscovery, variant of X, or plausibly new. Only an independent referee assigns the last; nothing is called novel.

| Term | Meaning |
|---|---|
| SPH | smoothed particle hydrodynamics: a mesh-free method in which particles carry mass and stress and interact through a smoothing kernel |
| collocated SPH | standard SPH with kernels evaluated in the current configuration (updated-Lagrangian in kind) |
| TLSPH | Total Lagrangian SPH: kernels and corrected gradients fixed in the reference configuration |
| UL SPH | updated-Lagrangian SPH, here with kernel-gradient correction as used by Dai et al. 2026 |
| BCT | boundary-consistent traction: our correction that spreads a contact or wall load over the first particle layers with boundary weights |
| R/16, R/32, R/64 | particle spacing as a fraction of the particle radius R |
| T-S0, T-S0p | elastic and elastic-plastic column striking a rigid wall (1D exact wave solutions, finite-strain corrected) |
| T-S1 | elastic sphere on a rigid wall at 20 m/s (Hertz impact; reference from an axisymmetric finite-element code) |
| T-B2 | elastic sphere on a deformable block (two-body Hertz) |
| rebound | exit over entry velocity; near 1 for an elastic impact |
| KE0 | kinetic energy at the start of a run |
| t_H, F_Hertz | Hertz contact time and peak force, the units of the T-S1 metrics |

## Track A: single-impact data

Track A tests closed-form v_cr models against single-particle impact measurements (mostly laser-induced projectile impact tests, LIPIT). Its three open hunches wait on blind data, and the last three blind papers reached step 1 on 2026-11-15.

- **Data:** an open v_cr table built from the literature (data/vcr_lipit.csv), each row with its source figure and uncertainty bracket. The reference law to beat is the one-parameter sound-speed law v_cr ≈ 0.15 c (zoo member Z6).
- **Record so far:** by 2026-11-07, 17 hunches had been registered; six met blind data: two refuted, two undetermined, one inconclusive, one supported but exposed. That rate led to the hunch budget.

| Hunch | Claim | Decisive test | Status |
|---|---|---|---|
| CS-10 | v_cr² = (0.15 c)² + β σ_p/ρ + γ (t_ox/d)/ρ: particle strength and oxide thickness both raise v_cr | same-powder series of three or more states, frozen after the fit | open; no blind paper reported particle strength |
| CS-12 | bonding is the local dissolution of the interface (oxide plus gap) by a Bay criterion; at a fixed oxide type, oxide thickness does not change v_cr | T3: v_cr against oxide thickness at one oxide type, unseen | open; T3 needs an unseen thickness series (possibly B06) |
| CS-17 | the substrate with less remaining strain-hardening capacity gives the lower v_cr, whatever its hardness | unseen pairs of substrate states of one metal | open; no unseen series known |

| Blind paper | State |
|---|---|
| B02, B10, B14 | scored earlier (B14 exposed) |
| B03, B05, B12 | closed without predictions (nothing discriminates); outcomes extracted and labelled exposed |
| B06 (oxide fracture), B07 (Ti bonding), B16 (velocity method) | PDFs filed 2026-11-15; step 1 is extractor task b10, inputs only |

The single-impact phase ends when all six papers are scored or declared unobtainable and the T3 measurement request is sent or dropped; then a synthesis is written.

## Track B: the solver host, step by step

Four particle-method configurations have been stopped by their ladders since 2026-11-08; finite elements and heat conduction were ruled out before that. The solver is a private fork of an open explicit impact code (OpenCourant) with our own SPH–SPH contact, cohesive bond and TLSPH bodies; licensed upstream files stay byte-identical.

| Date | Step | Result |
|---|---|---|
| 2026-11-15 | BCT off at the 0.5 µm scale (calibration, §22) | rule not met: 4 of 20 averages within 3.5 % at R/32, 6 of 20 at R/64; the face-layer deficit also appears against a deformable body. Counted as a failure: review session next |
| 2026-11-15 | BCT analysis and variant (calibration, §21) | BCT's wall scaling is exact only for a uniform load on a flat face; small or changing patches get rim loads 2–3× too high, on flat faces too. BCT also harms body-on-body contact. A variant fixed the energy but made the force noisy; not adopted. The T-S1 peak reference is 1.062, not 1.073 |
| 2026-11-14 | Diagnostics after the CS-18b verdict (§20.4–20.5) | T-S1 at R/64 with BCT passes its own limits (rebound 0.9788); at R/32 with BCT off the rebound is 0.9988 |
| 2026-11-14 | CS-18b: TLSPH + calibrated viscosity + BCT (§20) | **refuted at T-S1**: R/32 rebound 0.860 (limit ≥ 0.9796), contact time 5.3 % short; R/16 numerically unstable. T-S0 and T-S0p passed |
| 2026-11-13 | Calibration before CS-18b (§17–§19) | finite-strain references; thresholds from quads and collocated SPH; viscosity Q1 = 0.1, hourglass α = 5; BCT built; a survival probe at 800 m/s passed at R/16 and R/32 |
| 2026-11-13 | Independent route review, critique and meta-review | 12 of 14 numbers confirmed. Main advice: test first whether edge quantities converge at all, use band-averaged outputs, decouple the bond. The first and last conflict with the requirements and were set aside |
| 2026-11-13 | CS-18: TLSPH, uncalibrated (§16) | **refuted at T-S0**: rebound 0.942 at 100 particles (limit ≥ 0.95), contact time 1.1–1.5 % short |
| 2026-11-12 | Set-up S′: collocated SPH + kernel correction order 1 (§15) | host rungs failed the rule "not worse than before"; not adopted. Judged later against finite-strain references, its T-S0 would pass; its T-S1 rebound falls with refinement (0.993, 0.985, 0.966) |
| 2026-11-11 | Collocated SPH with contact and bond (§14) | A-0, A-2, B-1, C-1, D-2 pass; **B-2 fails** (two-body Hertz at R/32: rebound 0.885, approach 16 % long), B-3 and D-1 fail (bonded bar 0.285 V from exact, limit 0.05 V) |
| 2026-11-05 | CS-13c: heat conduction as a regulariser of the contact edge | refuted at reachable resolutions |
| 2026-11-04 | CS-11: solver-native contact or kernel welding as the interface (§10) | inconclusive: the weld has no interface from first touch, the contact can never bond; FE edge elements collapse at 0.07–0.17 D/V |
| 2026-11-04 | 2D axisymmetric finite elements, Johnson–Cook plus Grüneisen (§8) | the mesh fails at the jet root at 5–37 % of penetration time, earlier with refinement; edge quantities not converged; no Lagrangian remeshing for 2D quads |

## Current technical state

TLSPH bodies with the calibrated viscosity and hourglass control reproduce elastic contact closely when BCT is off; with BCT on they fail at the resolutions cold spray can afford. Without BCT, the first two loaded layers of a column carry only 0.62 and 0.86 of the true stress, against a rigid wall and a deformable body alike (§22).

**Elastic sphere on a rigid wall, 20 m/s (T-S1).** Reference: axisymmetric FE on the finest mesh (60 × 120). Metrics in units of t_H, F_Hertz and the Hertz approach; R/32 limits from the frozen CS-18b ladder.

| Configuration | Contact time | Peak force | Approach | Rebound | Viscous work / KE0 |
|---|---|---|---|---|---|
| Reference (FE 60 × 120) | 0.939 | 1.062 | 0.956 | 1.000 | — |
| Limit at R/32 | within 3.5 % | within 5.5 % | within 7.5 % | ≥ 0.9796 | — |
| TLSPH, BCT on, R/32 | 0.890 | 1.049 | 0.893 | **0.860** | 0.33 |
| TLSPH, BCT on, R/64 | 0.938 | 1.040 | 0.939 | 0.9788 | 0.020 |
| TLSPH, BCT off, R/32 | 0.927 | 1.060 | 0.928 | 0.9988 | 0.0016 |
| TLSPH, BCT variant "interior", R/32 | 0.925 | 1.402 raw (1.081 smoothed) | 0.926 | 0.999 | — |
| Collocated SPH, R/32 | 0.964 | 1.030 | 1.014 | 0.985 | — |
| S′ (collocated, kernel correction), R/64 | 0.955 | 1.019 | 0.958 | 0.966 | — |

**Elastic sphere on a deformable block (T-B2 geometry, R/32), TLSPH with penalty contact.** Reference: two-body Hertz; quad FE at R/128 gives peak 1.047, approach 0.976.

| BCT | Peak | Approach | Rebound | Contact segments |
|---|---|---|---|---|
| on | 1.080 | 0.901 | 0.984 | 2 |
| off | 1.054 | 0.952 | 0.999 | 1 |

- **Column end layers** (rigid wall, flat face): BCT on 0.9999 of the plateau stress in layers 1–4; BCT off 0.62 / 0.86 / 1.03 / 0.99.
- **Flat free surface under load** (T-surface b): within 0.8 % with BCT on and off.
- **High-velocity survival** (Al–Al, 800 m/s, to 1.0 D/V): passed at R/16 and R/32 with BCT on, as a calibration probe; not rerun with BCT off.
- **Not yet run under any TLSPH ladder:** tension, zero-energy modes, bonded and cohesive rungs, Bay activation.

**Interface averages, BCT off (§22).** Sphere on block (T-B2 geometry), body-on-body contact; averages over 0.5 µm discs on the axis and at half the contact radius, against the quad FE two-body run at R/128 on the same block. R/64 ran on a reduced block (the full block needs about 40 GB).

| Average (axis / 0.5 a) | R/32 | R/64 |
|---|---|---|
| contact pressure p_n, block side | +10.0 / +10.3 % | +7.8 / +4.9 % |
| normal stress, block, 0–0.5 µm below contact | −23.5 / −18.0 % | −8.1 / −8.8 % |
| normal stress, block, 0.5–1.0 µm | +5.9 / +7.9 % | +9.0 / +7.6 % |
| normal stress, sphere, 0–0.5 µm | −10.8 / +2.8 % | +1.0 / −3.3 % |
| normal stress, sphere, 0.5–1.0 µm | +1.7 / −5.1 % | +3.7 / +3.3 % |
| averages within 3.5 % | 4 of 20 | 6 of 20 |

The block's face layer itself stays at 0.59 (R/32) and 0.50 (R/64) of the reference, so the band average improves only by dilution. The fitted sphere surface is much closer than the flat cubic-lattice block face. The quad reference still rises 2–4 % from R/64 to R/128.

## What we understand and what we do not

The failures are understood case by case, but not the surface behaviour of the method as a whole.

**Understood (by analysis or a separating run):**

- **CS-18 T-S0:** the plateau offset came from finite strain, which the original linear reference ignored; the viscosity caused most of the rebound loss.
- **TLSPH end layers without BCT:** the corrected force sum expects a traction spread over the boundary layers, but a contact or wall load arrives on single particles. This gives the 0.62 / 0.86 layer stresses.
- **CS-18b T-S1:** BCT replaces the inverse of its spreading operator with the diagonal. That is exact only for a uniform load on a flat face; on a small or changing patch, rim loads come out 2–3× too high, the contact chatters and energy is exchanged. It fades with resolution because the patch holds more particles.
- **The T-S1 peak reference 1.073** came from one mesh (20 × 40) that sits above its neighbours; the converged value is 1.062.
- **The face-layer deficit is general** (§22): a column striking a deformable TL column gives the same 0.619 / 0.856 as against the rigid wall. It comes with any face loaded through single particles, and it stays fixed to the first one or two layers as resolution increases.

**Not understood:**

- **Energy accounting.** The viscous plus hourglass work reaches 0.49 KE0 in runs whose rebound is 0.998, so these terms are booked wrongly or something returns energy. TLSPH has no internal-energy output, so no run's energy balance can be closed.
- **Why S′'s rebound falls with refinement** (0.993 at R/16, 0.966 at R/64).
- **Whether interface quantities converge at all,** even as 0.5 µm averages. No host tried (FE in 2D and 3D, collocated SPH, TLSPH) has shown convergence of edge quantities. The published cold-spray simulations we read do not show it either; they validate on shapes, adhesion strength or v_cr.

**Pattern:** every failure since 2026-11-04 was at a body surface: the FE edge elements, the kernel weld, the SPH–SPH contact normals, the TLSPH end layers, BCT. The bonding criterion needs exactly the surface quantities Y and p_n.

## Next step: a review of the route

The rule fixed before calibration task 2026-11-15-a was not met, so by that rule the next step is a review session, before any further BCT variant or new hunch. Hunch CS-18c (TLSPH with BCT off) is therefore not defined.

Agenda of the review:

1. **The surface pattern:** every failure was at a body surface; §22 shows the TLSPH face-layer deficit is structural, not a wall artefact.
2. **Surface construction:** the fitted sphere surface is close (within 3.7 % at R/64), the flat lattice face is not. The substrate in cold spray is a flat face.
3. **A one-way bond for the first claim:** contact only, the Bay criterion evaluated afterwards. It still needs correct surface quantities.
4. **Energy accounting in TLSPH:** viscous plus hourglass work of up to 0.49 KE0 at a rebound of 0.998.
5. **A written dead-end trigger** for the particle-host route, scoped to this host and these resolutions.
6. **An external four-step proposal** (energy closure, one-way bond, consistent surface coupling or a surface skin, an Eulerian exit) and its critique: the skin is kept as a candidate if used for measurement only.

Rejected on 2026-11-15: BCT on flat wall faces only. It would pass the column rungs with a set-up the cold-spray runs would not use.

## Odds

The modeller's estimates are judgment, not judge results, and its last three host predictions were wrong; treat them as a rough prior.

| Milestone | 2026-11-12 | 2026-11-14 | 2026-11-15, before §22 | 2026-11-15, after §22 |
|---|---|---|---|---|
| calibration rule passes (0.5 µm averages within 3.5 %) | — | — | 30–40 % | failed |
| a TLSPH host passes its full ladder | — | 35–50 % | 20–30 % | 10–20 % |
| edge quantities converge as 0.5 µm averages in 3D | 25–35 % | 25–35 % | 20–30 % | 15–25 % |
| first claim with a one-way bond | — | 10–15 % | 8–12 % | 6–10 % |
| whole chain, bond in the solver | 5–10 % | 5–10 % | about 5 % | 3–5 % |

The owner chose on 2026-11-14 to continue at these odds, with a review after the next failure; that review is now due. Track A does not depend on any of them.

## Questions for reviewers

The most useful review would challenge the route, not the individual steps; the steps are checked by the ladders.

1. **Is a particle method the right host** for a quantity that lives at a surface? If not, which host gives converged surface expansion and contact pressure at a cold-spray contact edge in 3D, and where has that been shown?
2. **Does an interface state at the contact edge converge at all** without a physical length scale (oxide fragment size, a gradient-plasticity length)? Is 0.5 µm averaging a defensible substitute?
3. **Should the first claim use a one-way bond?** Up to the first bonding it is exact; v_cr then becomes a lower bound, because a bond may still break during rebound.
4. **Is there published work** that verifies cold-spray simulations against exact or converged references rather than experiments? Our sweeps have missed relevant work before (Dai et al. 2026).
5. **Energy accounting in TLSPH:** what explains viscous plus hourglass work of 0.49 KE0 at a rebound of 0.998?
6. **Surface construction:** why is the fitted sphere surface within 3.7 % at R/64 while the flat lattice face's first layer stays at 0.5–0.6? Can a flat substrate face be built the same way?

**Weaknesses of our process we already see:**

- The steps were rigorous, but the route was questioned too late. The 2026-11-13 critique's advice to test edge convergence first was set aside under the requirements.
- Several pre-run predictions by the modeller were wrong (CS-18, CS-18b, the S′ host rungs). Its judgment on this method family is poorly calibrated.
- The literature sample is small: about six papers read at full-text level, three more pending (Tang 2021, Ge et al. 2026, Dai et al. 2025).
- Some thresholds rest on one calibration method only, for example the tension limit of 0.095 V, which comes from a method with the tensile instability.

## Sources

All in the project repository, branch claude/exciting-fermi-qy077p, as of commit d106e5f. Section numbers (§) refer to the solver log.

| What | File |
|---|---|
| Solver log, §1–§21, with every judged number | docs/research/opencourant-verification.md |
| Result rows (each names its solver binary) | docs/research/opencourant/results/ |
| Decisions, dated | docs/DECISIONS.md |
| Hunch index and budget | docs/research/coldspray-hunches.md |
| Hunches CS-18, CS-18b with verdicts; CS-12 | docs/research/coldspray-hunch-cs18.md, -cs18b.md, -cs12.md |
| Frozen ladders | docs/research/sph-contact-ladder.md, sph-tlsph-ladder.md, sph-tlsph-b-ladder.md |
| Route review, critique, meta-review | docs/research/sph-route-review-2026-11.md, -critique.md, -meta.md |
| Literature on bonding methods | docs/research/data/bonding_methods_reading.md |
| Blind-paper rules and exposure log | docs/research/coldspray-blind-literature.md |
| Current tasks of the run sessions | docs/research/tasks/wsl-a.md, wsl-b.md |
| State and handoff | docs/STATUS.md, docs/HANDOFF.md |
