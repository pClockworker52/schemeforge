# Cold spray: hunch CS-22 (forked bond response converges on TLSPH), registration (frozen)

Drafted 2026-11-18 by claude from brainstorm item #9
([multi-particle-brainstorm-2026-11-18.md](multi-particle-brainstorm-2026-11-18.md)), which combines #2 (paired runs)
and #5 (checkpoint and rollback). Peter's decisions (chat 2026-11-18):
- retire CS-12 to free a budget slot;
- reopen Track B for this route only;
- waive the "obtainable data" part of rule 1 for part 2.

Status:
- **Registered and frozen 2026-11-18** (Peter: "Freeze"), together with the DECISIONS entry, before any run.
- **Host:** TLSPH bodies with `cs12` in the fork, so this is in-solver, on Track B. The 2026-11-17 closure of the
  interface-state route stands for local drivers (skin Y, the §27 drivers, v_edge). CS-22 uses none of them.
- **Budget:** CS-12 retired, CS-22 registered, so the count stays 5 of 5.
- **Kept minimal on purpose:** one speed, one fork time, three meshes, 7 runs. A pass justifies widening it later.
  A fail ends the route cheaply.

```yaml
- id: CS-22
  registered: 2026-11-18, frozen 2026-11-18
  assumption_broken: >-
    That an in-solver bond needs a verifiable local trigger before its effect on the impact can be computed (the
    reason for the 2026-11-17 closure and for rejecting the one-way bond, DECISIONS 2026-11-15).
  statement: >-
    Run the same impact twice. The off branch never bonds. The on branch is identical except that, from
    t_b = 0.5 t_p on, every contacting pair bonds. The difference in rebound, dR = e(on) - e(off), converges under
    refinement, although the local edge state does not.
  mechanism: >-
    Up to t_b the two branches are the same computation, so every error made there cancels exactly in dR. After t_b
    they differ only by the cohesive tractions. These act on the rebound through whole-body sums (bonded area,
    separation work), which converge the way energy closure does (0.25 %, §23-§24). The edge state enters only
    through which pairs are in contact at t_b, which is set by a(t), and a(t) converges
    (driver-check-2026-11-17 §6.1).
  parameters: >-
    Fixed now, before any run.
    - Deck: the §26 survival deck (quarter model, CS-18b TL settings, BCT off, F2, stfac 3), with the material set to
      P-HG-Al (§8.3/§25). R = 10 um, V = 600 m/s, t_end = 2.0 D/V.
    - Fork time: t_b = 0.5 t_p, with t_p = 0.707 D/V from §25.
    - Bond: cs12 with p_E = 0 and Y' set so far below any skin Y that f_B = 1 within 1e-3 (value set in the fork
      design note before any run). Law `tie`, sigma_B = f_B sigma_flow,ij(t) frozen at damage onset (§26).
      delta_c = 31.25 nm on every mesh (the §26 survival value; a placeholder, not a physical value).
    - Rebound e: particle centre-of-mass z-velocity at t_end divided by V, positive away from the target.
    - Meshes: R/8, R/16, R/32.
  predicted_effect:
    - {metric: "(a) on branch with t_b = infinity vs off branch, written metrics, R/8", direction: same,
       size: "bit-identical"}
    - {metric: "(b) dR on R/8, R/16, R/32", direction: same, size: "converges by the driver-check §3 rule"}
  kill_criterion: >-
    (a) Refuted if any written metric differs.
    (b) Refuted unless |dR32 - dR16| <= 3.5 % |dR32| and (|dR32 - dR16| <= 0.8 |dR16 - dR8| or
        |dR16 - dR8| <= 3.5 % |dR16|). Also refuted if |dR32| < 0.01 (no signal).
    Supported if (a) and (b) both hold.
    Inconclusive if a run fails before t_end, or R/32 does not fit on WSL A. Exception: an on branch that fails after
    the particle has stuck (z-velocity within 0.01 V of the target's for the last 0.2 D/V) is judged on e at that
    time. Nothing is substituted after the runs.
    Part 2 (the bistable band in V) is registered only if part 1 is supported, with its trigger and kill rule, before
    any part-2 run. The "obtainable" part of rule 1 is waived for it (Peter, 2026-11-18). The +-2 % windows are seen
    data.
  known_relatives:
    - common random numbers / twin runs (Monte Carlo practice); here the twins share the whole history before t_b
    - CS-21 (paired twins on the §25 2D deck; they share the discretisation, not the history)
    - one-way bond (DECISIONS 2026-11-15)
    - cs12 illustration (§26; central debonding on spring-back with a tuned delta_c; a picture, no claim)
  label: none yet (referee); never "novel"
  status: open
  author: claude (from brainstorm #9), Peter (route and budget decisions)
```

## Fork change needed (WSL A, before any run)

**One key: the activation start time** (e.g. `cs12.t_on`), unless one exists. A short design note comes before the
code, then a T-A0 rerun (bit-identical). The bond-everywhere setting uses existing cs12 inputs (p_E = 0, low Y′). If
cs12 rejects such a Y′, WSL A stops and reports; it does not write a new mode.

## Runs

7 in total, all at 600 m/s:
- off and on at R/8, R/16 and R/32;
- one on branch with t_b = ∞ at R/8, for (a).

The cost is set by the two R/32 runs. Estimated from §26 (1.6 GB and 0.25 h at R/16, to 1 D/V), each R/32 run takes
about 13 GB and several hours.

## Author's prediction (judgment, recorded 2026-11-18, before any run)

- **(a) passes: 0.85.** Two runs of one binary were never compared directly. Threaded sums may not be ordered.
- **(b) supported, given (a): 0.35.** For: bonded area and separation work are sums over many pairs. Against: the
  bond changes spring-back, where the jetting rim is least resolved. R/8 is coarse.
- **Whether e(off) itself converges on TLSPH for a plastic impact is not known.** It will be reported, not judged.
