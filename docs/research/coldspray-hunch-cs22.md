# Cold spray: hunch CS-22 (forked bond response converges on TLSPH), registration (DRAFT, not frozen)

Drafted 2026-11-18 by claude from brainstorm item #9
([multi-particle-brainstorm-2026-11-18.md](multi-particle-brainstorm-2026-11-18.md)), which combines #2 (paired runs)
and #5 (checkpoint and rollback). Peter's decisions (chat 2026-11-18):
- retire CS-12 to free a budget slot;
- reopen Track B for this route only;
- waive the "obtainable data" part of rule 1 for part 2.

Status:
- **DRAFT.** Not frozen. No run may start until this file says "frozen" and the DECISIONS entry is committed with it.
- **Host:** TLSPH bodies with `cs12` in the fork, so this is in-solver, on Track B. The 2026-11-17 closure of the
  interface-state route stands for local drivers (skin Y, the §27 drivers, v_edge). CS-22 uses none of them.
- **Budget:** CS-12 retired, CS-22 registered, so the count stays 5 of 5.

```yaml
- id: CS-22
  registered: 2026-11-18 (draft)
  assumption_broken: >-
    That an in-solver bond needs a verifiable local trigger before anything about bonding can be computed (the
    reason for the 2026-11-17 closure and for rejecting the one-way bond, DECISIONS 2026-11-15). CS-22 claims that
    the bond's effect on the impact can be computed and verified without one. Fork the run at a fixed time t_b into
    a bond-on and a bond-off branch. The difference in rebound converges under refinement, because both branches
    share every discretisation error made before t_b.
  statement: >-
    On TLSPH bodies in the fork, with cs12 in a contact mode (every pair with gap g < 0 and p_n > 0 activates at
    t >= t_b with constant bonded fraction f_B = 1; no skin Y, no p_E), the off branch never bonds. The on branch is
    the same run with activation allowed from t_b on. For Al on Al (P-HG-Al: LAW4 Johnson-Cook + Gruneisen, as in
    opencourant-verification.md §8.3/§25), R = 10 um, at 600 and 500 m/s:
    (a) an on branch with t_b = infinity gives written metrics bit-identical to the off branch (the §16.2 basis);
    (b) dR = e(on) - e(off) converges under refinement R/8 -> R/16 -> R/32 at t_b = 0.25, 0.5 and 0.75 t_p. Here e is
        the rebound coefficient: particle centre-of-mass z-velocity at t_end divided by V, positive away from the target.
  mechanism: >-
    Before t_b the two branches are the same computation, so every error made there is identical in both, not just
    similar as in CS-21. After t_b they differ by the cohesive tractions only. The rebound is a whole-body integral,
    and the bond acts on it through the bonded area and the work of separation W_b. Both are sums over many pairs, so
    their errors average out the way the energy closure does (0.25 %, §23-§24). The local edge state that does not
    converge (§25, §27) enters only through which pairs are in contact at t_b, which is a(t_b), and a(t) converges
    (driver-check-2026-11-17 §6.1).
  parameters: >-
    Fixed now, before any run.
    - Set-up as the §26 survival deck (quarter model, CS-18b TL settings, BCT off, F2, stfac 3), with the material
      changed to P-HG-Al and V = 600 or 500 m/s. Target size as §26, scaled with R.
    - t_end = 2.0 D/V.
    - t_p fixed from §25: 0.707 D/V at 600 m/s, 0.598 D/V at 500 m/s.
    - Cohesive law: cs12 `tie` law with sigma_B = f_B sigma_flow,ij(t), f_B = 1, frozen at damage onset (§26).
    - delta_c = 31.25 nm as a fixed physical length on every mesh (= 0.05 s at R/16, the §26 survival value). This
      is a placeholder, not a physical value. Part 1 tests convergence, not the value.
    - Particle and target spacing equal, as in §26.
  predicted_effect:
    - {metric: "part 1a: on(t_b = inf) vs off, written metrics", direction: same, size: "bit-identical"}
    - {metric: "part 1b: usable fraction of dR over the 2 speeds x 3 t_b", direction: up,
       size: "dR usable at >= 2 of 3 t_b at each speed"}
    - {metric: "part 2: width of the bistable band in V", direction: "any",
       size: "trigger and kill rule registered after part 1 passes; comparison with the +-2 % v_cr windows is post hoc"}
  kill_criterion: >-
    Part 1 (decisive, new runs).
    (a) Refuted if any written metric of the t_b = infinity on branch differs from the off branch at R/16, at either
        speed.
    (b) For each speed and t_b, apply the driver-check-2026-11-17 §3 rule to dR on the triple (R/8, R/16, R/32)
        in place of (R/64, R/128, R/256): |dR32 - dR16| <= 3.5 % |dR32| and (|dR32 - dR16| <= 0.8 |dR16 - dR8| or
        |dR16 - dR8| <= 3.5 % |dR16|). A point with |dR32| < 0.01 has no signal and counts as not converging.
        Refuted if dR is usable at fewer than 2 of 3 t_b at either speed. Supported if (a) holds and (b) is met at
        both speeds.
    Inconclusive if any run fails before t_end (TL stop, /DT stop, or out of memory). Exception: an on branch that
    fails after its particle has stuck (centre-of-mass z-velocity within 0.01 V of the target's for the last 0.2 D/V)
    is judged on e at that time. Also inconclusive if R/32 does not fit on WSL A. Nothing is substituted after the
    runs.
    Part 2 runs only if part 1 is supported. Its trigger (an aggregate evaluated after the fact on each branch, so
    that both branches can be self-consistent at one V) and its kill rule are registered then, before any part-2
    run. Peter waived rule 1's "obtainable" part for part 2 (2026-11-18). The +-2 % windows are seen data.
  known_relatives:
    - common random numbers / twin runs (Monte Carlo practice); the fork shares the whole history before t_b
    - CS-21 (paired twins on the §25 2D deck; shares discretisation, not history)
    - one-way bond (DECISIONS 2026-11-15; criterion afterwards, rejected because the bond must act in the solver)
    - cs12 illustration (§26; central debonding on spring-back with a tuned delta_c; a picture, no claim)
  label: none yet (referee); never "novel"
  status: open (draft)
  author: claude (from brainstorm #9), Peter (route and budget decisions)
```

## Fork changes needed (WSL A, before any run)

1. **cs12 contact mode.** Activation on g < 0 and p_n > 0 only, with f_B = 1. It needs a design note before any code
   (as `hvi/CS12-DESIGN.md`) and a T-A0 rerun (bit-identical).
2. **Activation start key** (e.g. `cs12.t_on`), unless one exists. With t_on = ∞ the build must be neutral, which is
   kill (a).
3. Optional: a restart-continued run checked bit-identical to an uninterrupted one. If it passes, on branches may
   restart from the off branch at t_b to save engine time. If it fails, or is not tried, they run from t = 0.

## Author's prediction (judgment, recorded 2026-11-18, before any run)

- **(a) passes: 0.85.** The engine reproduced written metrics in §16.2, but two runs of one binary were never compared
  directly there (3 of 47 time histories differed in near-zero columns), and threaded sums may not be ordered.
- **(b) supported, given (a): 0.35.** For: W_b and the bonded area are sums over many pairs. Against: at R/8 the
  contact patch at 0.25 t_p is only a few particles wide, so the bonded area there is coarse. The bond also changes
  spring-back, where the jetting rim is least resolved.
- **Whether e(off) itself converges on TLSPH for a plastic impact is not known.** No TLSPH row has a plastic rebound
  judged under refinement. It will be reported, not judged.
- **Cost (estimate from §26: 1.6 GB and 0.25 h at R/16 quarter, 1584 m/s, to 1 D/V; about 8× memory and 16× time per
  halving):**
  - R/32 about 13 GB and several hours per run, which is the tight point on a 15 GB machine;
  - 24 runs (2 V × 3 meshes × off plus 3 t_b);
  - item 3 of the fork changes cuts the on-branch cost to the part after t_b.
