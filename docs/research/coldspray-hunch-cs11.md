# Cold spray: hunch CS-11 (interface bracket for simulated jetting onset), registration (frozen)

Drafted 2026-11-04 on Peter's decision to bracket the particle–substrate interface (route A + B, DECISIONS
2026-11-04 "SPH particle–substrate interface: bracket, bond decided afterwards"). **Status: frozen**
2026-11-04, approved by Peter as written. This commit comes before any Al–Al run of either setup; git order is the
proof. **This file is not edited after the first Al–Al run.** Rung S1 is accepted at 20 m/s (DECISIONS 2026-11-04
"Rung S1 accepted at 20 m/s"). Research track, not a ledger arena. Solver background: opencourant-verification.md §8 and §9.

## Why

In OpenCourant, two SPH bodies interact only through the kernel. Any SPH particle–substrate pair is therefore
welded: no separation and no slip within 2h (§9.8). A frictionless contact that separates exists only against
Lagrangian bricks (`/INTER/TYPE7`), and that brings back mesh distortion at the jet (§8). Neither interface is the
physical one. The real interface is oxide-covered, slides and can separate before bonding, and is welded only where
fresh metal meets. The two setups are the limiting cases:

| Setup | Name | Interface | Bound |
|---|---|---|---|
| **W** | welded | SPH particle on SPH substrate, kernel coupling as is | maximum adhesion: no-slip, carries tension |
| **F** | frictionless | SPH particle on a 3D Lagrangian brick substrate, `/INTER/TYPE7`, friction 0, SPH particles as secondary nodes | no adhesion: slides and separates freely |

If a simulated quantity is the same in W and F, the unknown interface law does not matter for it, and simulation can
inform it. If not, any simulated value depends on a contact law that nobody has measured, and it must be quoted with
both bounds or not at all.

## Hunch

```yaml
- id: CS-11
  registered: 2026-11-04 (approved by Peter as written; frozen before any Al-Al run)
  assumption_broken: >-
    The assumption of every published cold-spray impact simulation read so far that one chosen interface
    treatment (the solver's default contact or a coupling) is adequate for the jetting-onset question.
  statement: >-
    The simulated jetting-onset velocity v_on of a normal Al-Al impact (d = 15 um, room temperature) differs by
    no more than one measured Al-Al window width between the welded (W) and the frictionless (F) interface.
  mechanism: >-
    Jetting starts when the contact edge slows below the speed at which the compressed material can stay attached,
    so the shock detaches and material squirts out at the edge (Walsh-type jetting criteria from explosive welding;
    HG2018a for cold spray). That onset is set by the bulk compressive state behind the edge, which an interface
    law does not touch before onset. Tension and slip across the interface come into play only after material
    starts moving outward.
  counter_mechanism: >-
    A no-slip interface (W) suppresses the relative sliding that feeds the jet at the edge, so W jets later or
    weaker. Kernel tension (W) holds back the outward edge material, which also delays onset. Both would put
    v_on(W) above v_on(F).
  predicted_effect:
    - {metric: "Delta = |v_on(W) - v_on(F)| at the finest converged spacing", direction: same, size: "<= w"}
  kill_criterion: >-
    w = 45 m/s (Al-Al window H20-17, 790-835 m/s, Hassani2020). Refuted if Delta > w. Supported if Delta <= w/2 at
    J* = 1.5 and Delta <= w at both J* = 1.25 and J* = 2.0. Inconclusive otherwise, or if either setup fails the
    convergence or evaluability rules below.
  known_relatives:
    - HG2018a (hydrodynamic jetting at onset; Z6)
    - Walsh-type jet criteria (explosive welding lens; not read in this track)
    - Assadi2003 (ASI in Lagrangian FE; interface treatment not varied there as far as read)
    - published SPH/CEL cold-spray studies: not checked for an interface comparison; referee to search
  provenance: Raised by the kernel-weld finding (opencourant-verification.md §9.8), before any Al-Al run.
  label: none yet (referee)
  status: open
  author: claude (with Peter)
```

**Prediction of the author, stated for the record:** I expect CS-11 to be refuted with v_on(W) > v_on(F) (counter
mechanism). Either outcome is useful. A refutation means simulated jetting onset needs an interface model, and that
is a negative result for the ledger.

## Frozen protocol

### Common to W and F

- **Material:** Al, LAW4 Johnson–Cook + `/EOS/GRUNEISEN`, all values from P-HG-Al in properties.csv, as in the §8.3
  deck (γ₀ = 2.17, JC reference strain rate 1 s⁻¹). No erosion, no failure model, no element deletion.
- **Geometry:** particle d = 15 µm (R = 7.5 µm), surface-conforming SPH sphere (§9.1), normal impact, quarter
  symmetry. Substrate block 3R × 3R × 2R (quarter), bottom fixed.
- **SPH settings:** the §9.1 table (h = 1.12 s, default artificial viscosity, ξ = 0, time-step scale 0.3).
- **Spacing:** the particle and the SPH substrate (W) use the same spacing s. The F bricks have edge length s within
  1.5R of the impact axis, graded outside.
- **F only:** `/INTER/TYPE7`, friction 0. Element and gap are chosen by the prerequisite rung F0 below and frozen
  with it.

### Jetting metric

- **J(V)** = the maximum over time t ≤ t_e and over all particle-body SPH particles of u_r / V, where u_r is the
  outward radial velocity.
- **t_e = 0.25 D/V.**
- **v_on** = the lowest V at which J crosses **J\* = 1.5**, found by linear interpolation between the sweep
  velocities. J\* = 1.25 and 2.0 are sensitivity values.
- Reported, without a verdict: the same metric for the substrate body (J_s); edge equivalent plastic strain at t_e,
  as in §8.3; the full J(V) curves.
- **Bracket width against measured oxide effects** (reported, no verdict). Δ is compared, as Δ and as Δ / 812 m/s,
  with the measured oxide effects known now:
  - Lienhard2020: about +14 % v_cr for Al at +2–3 nm (exposed, second-hand via Veysset2021);
  - B10: the 77 m/s spread across five heat treatments, and the group contrast of −30.5 m/s.

  The reading is fixed now:
  - Δ well above these effects: the unknown interface law swamps everything the oxide does, so a simulation says
    nothing about oxide effects unless it carries an explicit interface law.
  - Δ at or below them: the simulated onset is not arbitrary, but oxide effects still need an explicit law to be
    seen.

### Sweep and convergence

1. **Coarse sweep:** s = R/16, V = 400 to 1200 m/s in steps of 50, both setups.
2. **Refinement:** s = R/24 and R/32 at four velocities per setup. These are the two R/16 sweep velocities around
   that setup's crossing, plus one on each side.
3. **Converged:** v_on(R/24) and v_on(R/32) agree within 25 m/s, for each setup separately. Δ is taken at R/32.
4. **Budget:** first measure the cost of one F run at R/16. If the projected total exceeds 48 h of machine time,
   stop and report before the R/32 runs.

### Evaluability

- An F run whose brick mesh fails (time-step collapse, as in §8) before t_e is evaluated only up to the failure
  time.
- If the failure comes before 0.1 D/V, the run is unevaluable.
- If any of the velocities needed for a crossing is unevaluable, that setup's v_on is undetermined, and CS-11 is
  inconclusive. This is recorded as a result about F, not worked around.
- No crossing within 400–1200 m/s in either setup: inconclusive, recorded.

### Prerequisite rungs (before the sweep; pass thresholds frozen here)

- **F0 (TYPE7 Hertz):** elastic SPH sphere on an elastic brick block of the same material, 20 m/s, R/16 and R/32,
  against two-body Hertz (E* = E / (2 (1 − ν²))). Pass: at R/32, peak force and maximum approach within 5 % of
  Hertz, and the sphere separates (rebound > 0.9 V). Element formulation and gap are chosen here and frozen.
- **W0 (welded Hertz, loading phase only):** the same with an SPH block. Only the loading phase up to the peak
  force is meaningful. Pass: at R/32, peak force and maximum approach within 5 % of two-body Hertz. Rebound is
  reported but has no pass threshold, because the weld holds the sphere.
- A failed rung stops the sweep for that setup and goes to Peter.

## Where CS-11 sits in the plan

The long-term target is the **interface law** (oxide fracture, fresh-metal contact, bond or separation), not the
onset velocity (coldspray-go-nogo.md, local-first order revision 2). CS-11 measures only **how much the unknown law
matters** between its two bounds; it does not say what the law is. The first explicit candidate law is an oxide
interphase of SPH particles (option C of opencourant-verification.md §9.8). It will be registered as its own hunch
after the SPH material-failure check, and judged on oxide series it has not seen.

## What CS-11 cannot show

- v_on is a simulated quantity, **not v_cr**. Its distance from the measured Al window (790–835 m/s) is reported
  and labelled; no verdict depends on it.
- Supported means only that onset does not depend on the interface between these two bounds. The bond itself is
  decided afterwards (route B), by a criterion on the F fields. That criterion is a separate hunch, registered before
  it is evaluated.
- One material, one size and one interface pair: transfer to other metals is not tested.
