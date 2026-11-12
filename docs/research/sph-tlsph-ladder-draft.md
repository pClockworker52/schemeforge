# TLSPH verification ladder (for CS-18): DRAFT, awaiting Peter, not in force

Drafted 2026-11-12, revised the same day after the Profizi reading and SPEC-TL. It is frozen together with hunch
CS-18 ([coldspray-hunch-cs18.md](coldspray-hunch-cs18.md)) in one commit, before the first TLSPH run in the fork
(branch `tlsph`). After the freeze the rules of [sph-contact-ladder.md](sph-contact-ladder.md) apply:
- amendments are dated addenda;
- a failing rung means stop and report;
- every row names the fork SHA of a committed binary;
- predictions are committed before their runs.

**What it judges:** the TLSPH body formulation in the fork, with the hvi contact and bond laws ported unchanged. It
is a separate ladder; the collocated ladder and its verdicts stay as recorded.

**Peter's answers shape it** (DECISIONS 2026-11-12): all three outputs are needed, the bond acts in the solver, and
every rung is 3D. It includes an early survival rung at impact conditions (Peter, 2026-11-12, after the Profizi
reading).

## Freeze preconditions (all three needed)

1. Peter approves the numeric thresholds below.
2. Journal check of SPEC-TL's equations (Ganzenmüller eqs. 15, 17, 24, 32; CMAME 286 (2015) 87–106), against the
   preprint used and one independent source (WSL A task 2026-11-12-b).
3. A value for `tl.cond_max`, with its reason (same task).

## Set-up (adopted by Peter 2026-11-12, from SPEC-TL §1 at fork `tlsph` 1ae689c; one set-up for all rungs)

| Item | Value |
|---|---|
| Particles | cubic net at cell centres, surface-conforming spheres (opencourant-verification.md §9.1) |
| Kernel | cubic spline, support 2h, evaluated on reference positions |
| h | 2^(1/6) s ≈ 1.12 s, fixed in the reference |
| Gradient correction | first-order reference correction matrix per particle, computed once at t = 0, including symmetry images |
| Force | antisymmetric corrected form (Ganzenmüller eq. 24), P = J σ F⁻ᵀ |
| Kinematics | F from positions each cycle (eq. 17); L at mid-step into the solver's material routines (rate form, unchanged) |
| Hourglass control | Ganzenmüller eq. 32, **α = 10**; E replaced by the current yield stress once a particle is plastic |
| Viscosity | Monaghan pair form on reference pairs (SPEC-TL §3.7): q_a = 2, q_b = 1, solver's shear switch, compression only |
| Density | ρ = ρ₀ / det F |
| Time step | solver's SPH step, scale 0.3, on the length h₀·λ_min(F) |
| Reference update | **none** |
| Symmetry | slide planes only, mutually orthogonal, with complete single, double and triple images |
| Contact and bond | hvi code unchanged: `surface.normal = colour`, dynamic surface flag, radial gap, `contact.stfac = 3` |
| `tl.cond_max` | to be fixed before the freeze |
| Off for TL bodies | ξ, kernel-correction order, conservative smoothing (fatal if set) |

Changing any item after the freeze is an addendum labelled post hoc.

## Core rungs, in this order

| Rung | Case | Reference | Pass |
|---|---|---|---|
| T-A0 | the fork with no TL body, on the A-0 decks | the collocated fork binary | bit-identical |
| T-S0 | confined column, elastic (§9.4 deck, TL body), 25 / 50 / 100 / 200 particles | exact 1D | at 100 and 200: plateau within 1 %, contact time within 1 %, rebound ≥ 0.95; errors do not grow from 100 to 200 |
| T-S0p | two-wave elastic–plastic column (§9.5) | exact | σ₂ and both wave fronts within 1 % at 200 particles. The front width is also reported next to the collocated run |
| T-S1 | Hertz sphere on a rigid wall, 20 m/s, quarter model, R/16, R/32, R/64 | Hertz (JAX reference, §9.6) | at R/32: peak and approach within 5 %, rebound ≥ 0.95; at R/64 each error ≤ its R/32 value + 0.01 |
| T-tension | single TL bar, tension wave (D-1 geometry, one body) | exact 1D | maximum striker deviation ≤ 0.05 V over the whole run, 50 particles per L |
| T-zero-energy | free elastic block; initial velocity field of the longest wavelengths only, amplitude 1 % of c_d; 100 longest periods | spectral split of the kinetic energy | the share in the shortest-wavelength band never exceeds 1 % of the total. **Bug check:** total angular momentum of the free body drifts ≤ 1e-10 relative |
| T-B1 | two columns, contact (B-1) | exact 1D | as sph-contact-ladder.md B-1 |
| T-B2 | Hertz sphere on a TL block, contact, R/16 and R/32 | two-body Hertz | at R/32: peak and approach within 5 %, rebound > 0.9 |
| T-B3 | T-B2 started at s and at 2.4 s | itself | ≤ 1 % |
| **T-survival** | Al–Al quarter model, 800 m/s, R/16 and R/32, contact only, t_end = 1.0 D/V | survival checks (E-1 gate draft §3) | at both spacings: dt ≥ 0.1 of initial; detached mass ≤ 1 %; no cross-body pair closer than 0.5 s; no det F ≤ 0 or ill-conditioned-matrix stop. Energy reported, not judged. **FAIL stops TLSPH without a reference update**; an update rule is a new design with its own addendum |
| T-C1 | equi-biaxial stretch (C-1) | Y = 1 − 1/λ² | ≤ 1 % |
| T-D1 | tied bar (D-1) | exact joined bar | ≤ 0.05 V, maximum over the whole run |
| T-D2 | cohesive separation (D-2) | exact | as sph-contact-ladder.md D-2 |
| T-D3 | Bay activation (D-3) | closed form on prescribed Y(t), p(t) | as sph-contact-ladder.md D-3; once A3.5 exists |

## Reported rungs (do not stop the core)

| Rung | Case | Reference | Use |
|---|---|---|---|
| T-large-strain-1 | column driven to plastic strain 0.5 | exact two-wave solution up to the reflection | whether the form holds at large strain in 1D |
| T-large-strain-2 | Taylor bar, Al, 200 m/s | converged Lagrangian-brick run (Isolid 17) of the same deck, while the bricks are undistorted | final length and mushroom diameter, reported against 3 %. Reported only (Peter): the reference is numerical |
| T-cost | T-B2 at R/32 | §9.3 collocated cost | µs per particle-cycle and cycles, on an idle machine |

## Resources

TL storage is about 2.1 GB per million particles (SPEC-TL §3.8). T-S1 at R/64 is a sphere alone and fits. No impact
rung is run at R/64.

**E-1 follows only** after all core rungs pass and the E-1 gate (draft) is frozen.

## Open for Peter (before the freeze)

1. Approve, change or reject the thresholds:
   - T-S0 at 1 %;
   - T-S1 at 5 %, with rebound ≥ 0.95;
   - T-tension at 0.05 V;
   - T-zero-energy at 1 %, plus the 1e-10 angular-momentum check;
   - T-survival's checks.
2. Approve the order: T-survival before the bond rungs.
