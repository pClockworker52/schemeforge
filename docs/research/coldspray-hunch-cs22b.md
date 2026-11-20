# Cold spray: hunch CS-22b (forked bond response with a δ_c ladder), DRAFT — not frozen

Drafted 2026-11-20 by claude at Peter's request (chat 2026-11-19), after CS-22 part 1 was refuted for its registered
setting only (opencourant-verification.md §30; DECISIONS 2026-11-19 with its scope note). In CS-22 the placeholder
δ_c = 31.25 nm gave a bond of a few J/m²; every bond tore on rebound and dR stayed below 10⁻³, so the claim that dR
converges was never tested above the signal floor.

Status:
- **Draft, not frozen.** Not counted in the budget until Peter freezes it (then 4 of 5). No WSL task before the freeze.
- **Post hoc by construction.** The δ_c values are chosen after §30 was seen. They are fixed here, by the rule below,
  before any CS-22b run; nothing is chosen after a CS-22b run is seen.
- **Host:** as CS-22 (TLSPH with `cs12` in the fork, Track B, forked bond-response route only).
- **Changed from CS-22:** only the δ_c ladder, the reuse of the §30 off runs, the lost-bond validity check and the
  stage gate. Everything else is CS-22 with A1.

```yaml
- id: CS-22b
  registered: draft 2026-11-20 (not frozen)
  assumption_broken: >-
    As CS-22: that an in-solver bond needs a verifiable local trigger before its effect on the impact can be computed.
  statement: >-
    Run the same impact as CS-22 with three on branches that differ only in delta_c. For at least one delta_c in the
    ladder, the rebound difference dR = e(on) - e(off) converges under refinement and |dR32| >= 0.01.
  mechanism: >-
    As CS-22: up to t_b the branches are one computation, so all error made there cancels in dR; after t_b they
    differ only by the cohesive tractions, which act on the rebound through whole-body sums. CS-22 could not test this
    because its bond was too brittle to act. With partial bonding (some pairs hold, some tear), e(on) and e(off) may
    share most of their mesh error, so dR may converge although e(off) does not (14 % from R/16 to R/32, §30).
  parameters: >-
    Fixed now, before any CS-22b run.
    - As CS-22 with A1: the §26 survival deck (quarter model, CS-18b TL settings, BCT off, F2, stfac 3) with P-HG-Al,
      R = 10 um, V = 600 m/s, t_end = 2.0 D/V; cs12 with Y' = -1e6, p_E = 0, off-skin contacting particles bond,
      bond.t_on = 11.78 ns (0.5 t_p); law tie, sigma_B = f_B sigma_flow,ij frozen at damage onset; fork engine
      27e53d5f0; meshes R/8, R/16, R/32; e as in CS-22.
    - delta_c ladder, the same physical length on every mesh: 3x, 10x and 30x the CS-22 value, i.e.
      0.09375, 0.3125 and 0.9375 um (delta_c / s = 0.075, 0.25, 0.75 at R/8 and 0.3, 1, 3 at R/32).
    - Off branch: the three §30 off runs (AL08off, AL16off, AL32off; same engine and deck). No new off runs.
    - Kill (a) is not repeated: same engine; delta_c acts only after t_on; §30 kill (a) passed under A2.
    - Lost-bond check (post-processing of the interface file, no code): a bond is lost if a skin facet's bond state
      goes from bonded to not bonded between two interface records while its damage D < 1. Any lost bond makes that
      (delta_c, mesh) run invalid.
    - Stage gate: for each delta_c, on runs at R/8 and R/16 first. R/32 is run for that delta_c only if both runs are
      valid, reach t_end (or the CS-22 stuck exception applies) and |dR16| >= 0.01. At most 3 R/32 runs; memory is
      checked before each.
  predicted_effect:
    - {metric: "dR on R/8, R/16, R/32, for at least one delta_c", direction: same,
       size: "converges by the driver-check §3 rule, |dR32| >= 0.01"}
  kill_criterion: >-
    Per delta_c: refuted if it fails the stage gate on |dR16| or on reaching t_end, or |dR32| < 0.01, or not
    (|dR32 - dR16| <= 3.5 % |dR32| and (|dR32 - dR16| <= 0.8 |dR16 - dR8| or |dR16 - dR8| <= 3.5 % |dR16|)).
    Inconclusive for that delta_c if a run is invalid by the lost-bond check, or fails before t_end without the stuck
    exception, or R/32 does not fit.
    CS-22b supported if at least one delta_c passes. Refuted if every delta_c is refuted. Otherwise inconclusive.
    Nothing is substituted after the runs.
    Stated in advance: a delta_c at which the particle sticks on every mesh gives dR = -e(off), which fails the rule
    by construction (§30: |e32 - e16| = 0.0078 > 3.5 % of 0.057). Three delta_c values give three chances to pass;
    noted, not corrected for.
  known_relatives:
    - CS-22 (same route; its placeholder bond was too brittle to act)
    - §26 illustration delta_c sweep (Ti-6Al-4V, 1584 m/s, R/12; seen data on another material)
    - brainstorm #9 (forked bond response); common random numbers / twin runs
  label: none yet (referee); never "novel"
  status: draft
  author: claude (draft), Peter (route and request)
```

## Why these δ_c values (post hoc, labelled)

- σ_flow for P-HG-Al from its Johnson–Cook values (A 148.4, B 345.5 MPa, n 0.183) is about 450–540 MPa at
  ε_p 0.5–2 without thermal softening, and roughly half that near the interface temperatures (modeller's estimate,
  not a solver output). Take 200–550 MPa.
- With the bilinear law, G_c = ½ σ_B δ_c. The CS-22 placeholder gives about 3–9 J/m². The ladder gives about 9–26,
  31–86 and 94–258 J/m².
- A rough threshold proxy from the §30 rows (seen data): rebound kinetic energy of the off branch divided by the
  maximum bonded area of the on branch, assuming both per quarter model: 71, 37, 29 J/m² at R/8, R/16, R/32. The
  ladder brackets it from below, near and above.
- The §26 illustration sweep (another material and speed) kept 0.06–0.11, 0.63–0.65 and 1.00 of the ever-bonded
  facets at δ_c/s = 0.3, 1 and 3. It informed the range only.

## Lost bonds and the pair list

§26 saw facets that were debonded show state 0 or 1 later, probably a pair leaving the pair list or re-pairing (not
checked). With δ_c of up to 3 s at R/32, a bonded pair may open beyond the cross-body candidate range before its
damage reaches 1, and the bond would vanish without tearing. Before any run, WSL A reports from the fork the opening
at which a cross-body pair leaves the candidate list. This sets expectations only; the rule above decides.

## Runs

- Stage 1: 3 δ_c × R/8 and R/16 on runs = 6 runs (§30: R/8 about 100 s, R/16 about 0.5 h each).
- Stage 2: at most 3 R/32 on runs, only for δ_c values that pass the gate (§30: about 11 h and 14 GiB each on the
  23.5 GiB VM; more bonds held may raise memory).
- Rows `results/tl_cs22b_*.csv`, written up as §31 of opencourant-verification.md.

## Author's prediction (judgment, recorded 2026-11-20 with the draft)

- **CS-22b supported: 0.15.** Against: a strong bond pulls dR towards −e(off), whose mesh drift fails the rule by
  construction; R/8 is coarse.
- **If one passes, most likely 10×** (partial bonding, where e(on) and e(off) can share their mesh error).
- **30× sticks on at least one mesh: 0.6.**
- **At least one lost bond at 30× and R/32: 0.4.**
