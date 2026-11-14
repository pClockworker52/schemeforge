# TLSPH verification ladder for CS-18b: frozen

**Frozen 2026-11-14** (Peter approved; DECISIONS 2026-11-14), together with hunch CS-18b
([coldspray-hunch-cs18b.md](coldspray-hunch-cs18b.md)), in one commit, before any CS-18b rung run. After the freeze the rules of [sph-contact-ladder.md](sph-contact-ladder.md) apply:
- amendments are dated addenda;
- a failing core rung means stop and report;
- rows name the fork SHA of a committed binary;
- predictions are committed before their runs.

**Calibration came first** (DECISIONS 2026-11-13):
- references corrected for finite strain (§18.1);
- thresholds set as 1.25 × the error of methods known to work (§18.2), or, for surface and contact rungs, the quad
  error + 3 points (DECISIONS 2026-11-13);
- settings chosen on calibration cases that are not rungs (§18.3, §19.4).

No CS-18b rung deck was used to choose anything.

## Set-up (one set-up for all rungs)

| Item | Value |
|---|---|
| Formulation | as `sph-tlsph-ladder.md` set-up (SPEC-TL §1): cubic spline, h = 1.12 s fixed in the reference, first-order reference correction, Ganzenmüller force, F from positions, rate-form material, ρ = ρ₀/det F, dt scale 0.3 on h₀·λ_min, no reference update, slide planes with complete images |
| Viscosity | **LAMMPS SMD TLSPH pair form, Q1 = 0.1, Q2 = 0** (§18.3, §19.4) |
| Hourglass control | Ganzenmüller eq. 32, **α = 5**, with the plastic switch E → σ_y |
| Boundary-consistent traction | **on, guard 0.45** (§19.1–19.2; normal from −f/|f|; wall loads scaled so that the wall particle receives its stopping force) |
| Conditioning limits | `tl.cond_max` = 30, `tl.smin_min` = 0.025 |
| Contact and bond | hvi code unchanged: `surface.normal = colour`, dynamic surface flag, radial gap, `contact.stfac = 3` |
| Binary | fork `sph-hvi-contact` branch `tlsph`, solver source of 43791edbc, built from a clean tree |
| Off for TL bodies | ξ, kernel-correction order, conservative smoothing (fatal if set) |

**Metrics under BCT:** every wall force is read from the body's momentum rate (`plateau_dPdt`, `contact_dPdt`), not
from the engine's `/TH/RWALL` output, which reads 1.485 × the transmitted force under BCT (§19.2).

## References

Finite strain (§18.1):
- T-S0 (100 m/s): plateau 1.00659, contact time 0.99294, rebound 0.99654.
- T-S0p (50 m/s): σ₂ 1.00412, plastic front 1.00544 c_b, elastic front 1.00082 c_d.
- T-tension: the linear exact bar (finite strain changes it by at most 0.0033 V).
- Hertz rungs: as before.

## Core rungs, in this order

| Rung | Case | Pass |
|---|---|---|
| T-A0 | the fork with no TL body, on the A-0 decks | identical to the A-0 reference |
| T-S0 | confined column, 25 / 50 / 100 / 200 particles | at 100 and 200: plateau within 1.5 %, contact time within 2.0 %, rebound ≥ 0.9318 (100) and ≥ 0.9517 (200). Errors may not grow from 100 to 200 by more than the noise floors (plateau 0.1 %, contact time 0.2 %, rebound 0.2 %) |
| T-S0p | two-wave column, 200 particles | σ₂ within 1.5 %, plastic front within 3.5 %, elastic front within 1.5 % |
| T-S1 | Hertz sphere on a rigid wall, 20 m/s, R/16, R/32, R/64 | contact time at 10⁻² within 3.5 %; peak within 5.5 %; approach within 7.5 % at R/32 and 4.0 % at R/64; rebound ≥ 0.9796 (R/32) and ≥ 0.9746 (R/64); at R/64 no error more than its R/32 value + 0.01 |
| T-tension | single TL bar, tension wave (D-1 geometry, one body), 50 particles per L | maximum striker deviation from the exact bar over the whole run within **0.095 V** (see "Source of the tension limit") |
| T-zero-energy | free elastic block, smooth initial field (longest wavelengths, 1 % of c_d), 100 longest periods | share of kinetic energy in the shortest-wavelength band ≤ 1 % at all times; angular momentum drift ≤ 1e-10 relative |
| T-surface | (a) column end layers: steady stress of layers 1 and 2 over the momentum-rate plateau, at 100 and 200 particles; (b) the flat free surface under load (§18.4 deck, 16 wide, free x faces): σ_zz of the two outer columns over the middle, time-averaged over 0.25–0.55 contact times, at 100 and 200 | within **3.5 %** in (a) and (b) |
| T-B1 | two columns, contact | as sph-contact-ladder.md B-1 |
| T-B2 | Hertz sphere on a TL block, contact, R/16 and R/32 | at R/32: peak within **8.0 %**, approach within **5.5 %**, rebound > 0.9 |
| T-B3 | T-B2 started at s and at 2.4 s | ≤ 1 % |
| T-survival | Al–Al quarter model, 800 m/s, R/16 and R/32, contact only, t_end = 1.0 D/V | at both spacings: dt ≥ 0.1 of initial; detached mass ≤ 1 %; no cross-body pair closer than 0.5 s; no det F ≤ 0 or conditioning stop. Energy reported |
| T-C1 | equi-biaxial stretch | Y within 1 % |
| T-D1 | tied bar against the exact joined bar | maximum deviation over the run within the T-tension limit, **0.095 V** |
| T-D2 | cohesive separation | as sph-contact-ladder.md D-2 |
| T-D3 | Bay activation | as sph-contact-ladder.md D-3; once A3.5 exists |

## Reported rungs (not judged)

| Rung | What is reported |
|---|---|
| T-surface-sphere | conforming sphere under a Hertz-like load: layers 1–3 normal stress against the half-space value (static model and one engine run at R/32). Known: layer 2 is 26–30 % low (§19.1); a fix is a later step |
| T-large-strain-1 | column to plastic strain 0.5 against the exact two-wave solution |
| T-large-strain-2 | Taylor bar against a converged brick run, against 3 % |
| T-cost | T-B2 at R/32, idle machine |
| Energy closure | reported until the fork computes TL internal energy |
| BCT fallbacks | count and location of guard fallbacks, in every impact run |

## Interface outputs (for E-1 and later)

Y, p_n, temperature and bonded area are judged as averages over **0.5 µm** (DECISIONS 2026-11-14). Point values at
the edge are reported only. The E-1 gate draft is to be revised to this before its freeze.

## Source of the tension limit (T-tension, T-D1)

**0.095 V** comes from the §18.2 rule (1.25 × the calibration method's error) applied to one method only. That
method is the collocated SPH welded bar under the frozen collocated set-up: maximum deviation over the run 0.073 V
(opencourant-verification.md §14.3; window as in sph-contact-ladder.md Addendum 1 A2).
- **No quad-element tension calibration exists.**
- **The limit rests on a method known to have the tensile instability.** It is therefore loose by construction.
- **Peter chose to start with it** (2026-11-14). A quad tension calibration may replace it later, as an addendum
  labelled post hoc if it comes after any T-tension or T-D1 result has been seen.

## Addenda

None.
