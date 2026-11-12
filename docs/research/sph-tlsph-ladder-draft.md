# TLSPH verification ladder (for CS-18): DRAFT, awaiting Peter, not in force

Drafted 2026-11-12. Frozen together with hunch CS-18 ([coldspray-hunch-cs18.md](coldspray-hunch-cs18.md)) in one
commit, before the first TLSPH run in the fork (branch `tlsph`). After the freeze the rules of
[sph-contact-ladder.md](sph-contact-ladder.md) apply:
- amendments are dated addenda;
- a failing rung means stop and report;
- every row names the fork SHA of a committed binary;
- predictions are committed before their runs.

**What it judges:** the TLSPH body formulation in the fork, with the hvi contact and bond laws ported. It is a
separate ladder. The collocated-SPH ladder and its verdicts stay as recorded.

**Peter's answers shape it** (DECISIONS 2026-11-12): all three outputs are needed (so the surface layer must be
accurate), the bond acts in the solver (so tension in the bonded state is tested), and 3D is needed (so every rung is
3D).

## Set-up (fixed in the freeze commit; one set-up for all rungs)

To be filled in at the freeze, from the fork's SPEC-TL, after Profizi 2016 has been read:
- kernel and h;
- gradient correction;
- hourglass coefficient α;
- artificial viscosity;
- reference-update rule ("none", or a named rule with its trigger).

Nothing is varied per rung. Changing any of these after a run is an addendum labelled post hoc.

## Core rungs

| Rung | Case | Reference | Pass |
|---|---|---|---|
| T-S0 | confined column, elastic (§9.4 deck, TLSPH bodies), 25 / 50 / 100 / 200 particles | exact 1D | at 100 and 200: plateau within 1 %, contact time within 1 %, rebound ≥ 0.95; errors do not grow from 100 to 200 |
| T-S0p | two-wave elastic–plastic column (§9.5) | exact | σ₂ and both wave fronts within 1 % at 200 particles |
| T-S1 | Hertz sphere on a rigid wall, 20 m/s, quarter model, R/16, R/32, R/64 | Hertz (JAX reference of §9.6) | at R/32: peak and approach within 5 %, rebound ≥ 0.95; at R/64 each error ≤ its R/32 value + 0.01 |
| T-tension | single welded TLSPH bar, tension wave from a free-end release (D-1 geometry, one body) | exact 1D | maximum striker deviation ≤ 0.05 V over the whole run, at 50 particles per L |
| T-zero-energy | free elastic block, random initial velocity field of 1 % of c_d, 100 longest periods | energy content of the shortest lattice wavelength | the share of kinetic energy in the Nyquist-wavelength band stays ≤ 1 % of the total at the end; total energy drift ≤ 1 % |
| T-B1 | B-1 (two columns, contact) | exact 1D | as sph-contact-ladder.md B-1 |
| T-B2 | B-2 (Hertz sphere on a TLSPH block, contact), R/16, R/32 | two-body Hertz | at R/32 peak and approach within 5 %, rebound > 0.9 |
| T-B3 | T-B2 started at s and 2.4 s | itself | ≤ 1 % |
| T-C1 | C-1 (equi-biaxial stretch) | Y = 1 − 1/λ² | ≤ 1 % |
| T-D1 | D-1 (tied bar) | exact joined bar | ≤ 0.05 V, maximum over the whole run |
| T-D2 | D-2 | exact separation | as sph-contact-ladder.md D-2 |
| T-A0 | the fork without TLSPH parts = the collocated fork binary | itself | bit-identical on the A-0 decks |

## Reported rungs (judged once a reference is fixed; they do not stop the core)

| Rung | Case | Reference | Use |
|---|---|---|---|
| T-large-strain-1 | column driven to plastic strain 0.5 (strong elastic–plastic wave) | exact two-wave solution up to the reflection | reports whether the formulation without a reference update holds at large strain |
| T-large-strain-2 | Taylor bar (Al, 200 m/s) | converged Lagrangian-brick OpenCourant run of the same deck (verified element, Isolid 17), up to the time the bricks are still undistorted | final length and mushroom diameter within 3 %; decides whether a reference update is needed before E-1 |
| T-cost | T-B2 at R/32 | §9.3 collocated cost | µs per particle-cycle and cycles, idle machine |

**E-1 follows only** after all core rungs pass, T-large-strain-2 is within limits, and the E-1 gate (draft) is frozen.

## Open for Peter

1. Approve, change or reject the thresholds, in particular T-S0 (1 %), T-S1 (5 %, rebound 0.95), T-tension
   (0.05 V) and T-zero-energy (1 %).
2. Whether T-large-strain-2 (Taylor bar against bricks) is an acceptable reference, since it is not exact.
3. Whether the fork should fetch Profizi 2016 and the thesis first. This is recommended: the set-up section can only
   be filled once they are read. The route is either the two hosts being allowed in the environment, or WSL B.
