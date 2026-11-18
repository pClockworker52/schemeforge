# Multi-particle cold spray: brainstorm 2026-11-18

Ideas were generated from [multi-particle-spec.md](multi-particle-spec.md) alone. They were filtered afterwards
against [multi-particle-tried.md](multi-particle-tried.md). STATUS and the solver log were not read. Nothing here
was run, so there are no scores. "Untried" means untried in the project record. It does not mean new. The labels
follow iron rule 6. Each shortlisted item needs `sforge hunch add` before it is tested.

## Guiding observation

According to the tried list, contact radius r_c(t) is the only local-ish quantity that converges (§27). Bulk
integrals also converge. The most promising ideas therefore decide joining from r_c(t) and its derivatives, or
from integrals. Other ideas change what "converge" means (differences, distributions). None of them tries again
to converge the edge state.

Second observation: the tried list covers only the single-impact interface. Function 5 (hand-on to the next
impact) and the deposit level are untouched.

## Shortlist (untried, ranked)

| # | Idea | Mechanism | Predicted effect | Kill criterion | Label |
|---|---|---|---|---|---|
| 1 | **Kinematic jetting window, bond switched on in the solver from r_c(t)** | Edge speed v_e = dr_c/dt and collision angle β(r_c) come from contact-radius kinematics alone. Film is cleaned (and the bond activates as the edge passes) only where the edge is subsonic and β lies inside a window. Early on, v_e is supersonic, so there is no jet and the pole stays unjoined. That gives the ring without a local surface state. | Inner ring radius predicted from c and V without a fit. v_cr follows from the bonded ring surviving rebound under the existing cohesive law. | dr_c/dt not converged R/32→R/64 at the subsonic crossing; or predicted inner/outer ring radius outside ring-map scatter; or no ring at any V | variant of explosive-welding jetting criteria (Walsh 1953); **in the project record already: coldspray-kinematics.md (u = V cot β, switch radius a_c/R 0.09–0.27) and reduced-route option R3** (see correction below) |
| 2 | **Paired (differential) simulations** | Use the same discretisation and change one factor (film, cold-worked target, sprayed surface). The non-convergent edge error is mostly common-mode, so Δ may converge where absolute values do not. The experimental facts are relative anyway (+4…17 %, −12 %, +15 %). | Δv_cr signs and magnitudes for the three facts | Δ of the driver changes by more than half the experimental effect between R/32 and R/64; or wrong sign | untried; generic common-mode rejection |
| 3 | **Weak (statistical) convergence** | Run ensembles over lattice jitter or seeds. Require the *distribution* of edge quantities, or P(bond), to converge rather than pointwise values. This tests the working assumption directly and matches the statistical nature of v_cr. | Distribution moments stable under refinement even though samples are not | KS distance or mean shift R/32→R/64 not smaller than R/16→R/32 | untried |
| 4 | **Edge intensity factor (contour integral)** | Treat the moving joining edge like a crack tip. Local fields diverge, but the energy flux into the edge (dynamic J-type, path-independent) may converge. Join where G_edge ≥ film fracture + adhesion energy. | Convergent edge driver, distinct from annulus averages | Path dependence > 10 % across contours, or no convergence (risk: §27 annulus plastic work failed) | variant of dynamic fracture mechanics (J-integral) |
| 5 | **Checkpoint–rollback fixed point** | Run the impact, evaluate the aggregate trigger, rewind to the trigger time, re-run with the bond active, and iterate. The bond then acts in the solver (C3), which answers the reason the one-way bond was rejected. | Self-consistent bonded state; at most 2–3 iterations (contact time 10–40 ns) | Iteration does not converge, or oscillates between bond and no bond near v_cr | variant of the one-way bond (DECISIONS 2026-11-15) |
| 6 | **Multi-particle chain: cut-out window + impact surrogate + kinetic Monte Carlo deposit** | Impacts are separated in time (≫ 40 ns), so each is simulated in a deposit window of about 5D with absorbing boundaries. A surrogate maps (V, angle, local target state) → (P_stick, ring, shape, hardness, film, residual stress). The deposit grows by kinetic MC or level set, with a logistic P(V) from the ±2 % windows. | DE and porosity vs V; +15 % on sprayed surface; −12 % cold-worked | Window result depends on window size by more than 2 % in rebound; or DE curve outside data under blind rules | variant of thermal-spray stochastic build-up models |
| 7 | **Explicit physical roughness** | Seed measured roughness (polished vs sprayed, Ra) at a resolvable scale. Joining statistics then come from asperity events over an ensemble. | Sprayed-surface +15 % v_cr | Effect absent, or below the R/32→R/64 change | untried |
| 8 | **Bounds bracket** | Two limit bond laws (film always removed vs never) bracket v_cr. Check that the experiments fall inside. This is cheap verification without an interface reference (C6). | Bracket width < 20 % | Experiments outside the bracket | untried |
| 9 | **Forked bond response (synthesis of #2 and #5; added after the filter, 2026-11-18)** | Checkpoint at the trigger time t_b and fork into a bond-on and a bond-off branch. The branches are identical up to t_b, so all error accumulated before the decision is shared exactly, not just the mesh as in #2. The measured quantity is ΔR = rebound(on) − rebound(off), built from integrals only. #5's failure mode (oscillation near v_cr) is read as bistability: over a velocity band both branches are self-consistent (a bond that forms holds; a bond that never forms lets the particle rebound). Forks with a small change also give the derivative of the fixed-point map (stability, Newton steps). | Width of the bistable band in V, without a fit, compared with the ±2 % windows of the v_cr definition (joining and rebound equally probable); the band shifts with target state | (a) a zero-change fork does not stay bit-identical (non-deterministic solver); (b) ΔR not converged R/32→R/64; (c) the band is empty at every V or wider than about 10 % | variant of common-random-numbers / twin-run methods; bistability reading untried in the record |

**#9 status.** Registered and frozen 2026-11-18 as [CS-22](coldspray-hunch-cs22.md), simplified to one speed, one fork time and 7 runs. CS-12 was retired to free the slot, and Track B was reopened for this route only (DECISIONS 2026-11-18). WSL A task 2026-11-18-a.

Add-ons that need #1: stochastic hazard rate from the convergent kinematics (v_cr becomes the 50 % point by
construction), and the energy criterion (bond energy over the ring ≥ elastic rebound energy, both integral).

## Correction (2026-11-18, after the filter)

The filter used only multi-particle-tried.md. A later check of the record (while drafting hunches) found three
things that list does not mention:
- **#1 is mostly in the record already.** coldspray-kinematics.md has the Walsh/Hassani-Gangaraj subsonic-edge
  switch on rigid geometry, and reduced-route option R3 is the kinematic estimate of where bonding starts. Only two
  parts of #1 are new to the record: reading the switch radius a_c as the inner radius of the ring, and an in-solver
  bond. The in-solver bond needs the Track B route, which was closed on 2026-11-17.
- **v_edge = da/dt from the solver does not converge** (driver-check-2026-11-17.md §6.1: 0 of 7 and 0 of 6 points),
  although a(t) does. #1's first kill test is therefore already failed for raw differences. Only a derivative of a
  fitted a(t), or the rigid-geometry formula, remains.
- **#2's motivating facts are seen data.** The +4–17 %, −12 % and +15 % effects, and the ring maps exposed for CS-12
  T1, cannot test it. Under the hunch budget, registration needs a named unseen source.

**Registered 2026-11-18:** #1, narrowed to the R3 ring-radius form, as
[CS-20](coldspray-hunch-cs20.md); #2, cold-worked target only, as [CS-21](coldspray-hunch-cs21.md) (DECISIONS
2026-11-18).

## Dropped after filtering

| Idea | Reason |
|---|---|
| Non-local averaging over a physical length; Grady–Kipp oxide fragment size as that length; phase-field bond variable | variant of §27 (non-local drivers, none converges); a physical length does not fix a non-converging driver |
| Sub-grid 1D film strip driven by surface stretch | variant of §26 (stretch peaks at the pole, centre bonds first) |
| Very fine 2D axisymmetric runs for the edge | tried, §8 (jet-root collapse) |
| Eulerian/ALE/MPM/hybrid FE skin; steady comoving-frame 2D edge solve | read, none shows converged interface states; useful only for #4 (amplitude, not local values) |
| Jet peel depth (jet mass flux / swept area vs film thickness) | variant of oxide jet model; needs the jet root, which collapses (§8) |
| Adiabatic shear instability criterion | mesh-dependent in the literature (rediscovery); heat-conduction regulariser refuted (CS-13c) |
| Sound-speed backbone plus simulated corrections | variant of closed-form laws; survives only inside #2 |
| MD film-rupture table | needs local inputs that do not converge |
| Goal-oriented adjoint refinement | targets aggregates that already converge |
| Cross-prediction protocol | already exists (pre-registration, blind scoring) |

## Suggested first step

Run #1 and #2 first. Both reuse existing resources (convergent r_c(t), the in-solver cohesive bond, and the
experimental judges), and each has a cheap kill test at R/32 vs R/64. #1's kill test is whether dr_c/dt converges
at the subsonic crossing. #2's kill test is whether Δ converges. #6 is the only route that addresses the
multi-particle goal itself, and it can start in parallel because it does not depend on the interface question.
