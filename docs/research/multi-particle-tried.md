# Multi-particle cold spray: what was tried (filter list; read only after generating ideas)

Companion to [multi-particle-spec.md](multi-particle-spec.md). Use it in a second pass, to mark each new idea as
"tried", "variant of a tried one" or "untried". Details: opencourant-verification.md (§), DECISIONS.

| Approach | Result | Where |
|---|---|---|
| 2D axisymmetric Lagrangian FE (Johnson–Cook, Grüneisen) | mesh collapses at the jet root at 5–37 % of penetration, earlier when refined; edge quantities not converged | §8 |
| Heat conduction as a regulariser of the contact edge | refuted at reachable resolution (a rediscovery) | CS-13c, §13 |
| Solver-native contact or kernel welding as the interface | inconclusive: the weld has no interface, the contact can never bond | CS-11, §10 |
| Collocated SPH with separable contact and a cohesive bond | two-body Hertz and bonded bar fail | §14 |
| Collocated SPH with kernel correction (S′) | rebound falls with refinement | §15 |
| Total Lagrangian SPH, uncalibrated, then calibrated with boundary-consistent traction (BCT) | refuted at T-S0, then at T-S1; BCT overloads rims of small or changing patches and puts energy in | §16–§21 |
| TLSPH with BCT off, 0.5 µm depth averages | face layer deficit (0.5–0.6); averages miss 3.5 % | §22 |
| Variationally consistent integration (VCI), momentum-restoring VCI, fitted flat face | VCI fails its momentum gate; the momentum-restoring variant passes but worsens skin pressure; the fitted face helps flat columns only | §23–§24 |
| Measurement-only surface skin | p_n within 3.6 %, surface stretch 13 % low at R/64 | §23 |
| Bay-type activation (stretch and pressure thresholds) on the skin | stretch peaks at the particle pole, so the centre bonds first; no ring for any thresholds | §26 |
| Outer or non-local activation drivers (annulus plastic work, pressure–slip history, ring-averaged stretch) | none converges; only contact radius does | §27 |
| One-way bond (criterion evaluated afterwards) | proposed, not adopted (the bond must act in the solver) | DECISIONS 2026-11-15 |
| Closed-form v_cr laws (sound speed, strength plus oxide, oxide jet model, substrate hardness) | sound speed works for pure metals; strength and hardness terms refuted; oxide-thickness test (T3) open | synthesis 2026-11-18 |
| Eulerian / ALE, MPM, peridynamics, updated-Lagrangian SPH (Dai) | read, not run; none shows converged interface states | bonding_methods_reading.md, route review |
| Paired differences (twins sharing the mesh, block hardened) of the outer drivers on 2D quads (CS-21) | refuted: no difference usable (0–0.33 of points); pairing does not cancel the edge error | §28 |
| Forked bond response: twin TLSPH runs, every contacting pair bonds from 0.5 t_p, rebound difference dR (CS-22) | refuted: dR below 10⁻³ on R/8–R/32 (sign changes); every bond fails on rebound with δ_c 31.25 nm, σ_B = σ_flow; e(off) itself moves 44 % then 14 % | §30 |
