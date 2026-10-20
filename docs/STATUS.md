# STATUS
Phase: 1 — Arena 1 judge and zoo (in progress)      Judge version: — (not tagged yet)
Last session: 2026-10-20 — Gate 0 passed; Phase 1: exact solutions, both solvers, slot contracts, dev suite cases

## Done
- Phase 0, Gate 0 passed (see git history and DECISIONS.md).
- Exact Riemann solver (Toro ch. 4) and exact nozzle solution: Appendix H reproduced (Toro to the quoted digits,
  nozzle to 4–5 digits); Hypothesis property tests for Rankine–Hugoniot, rarefaction invariants, mirror symmetry,
  nozzle ṁ/h₀ constancy and entropy jump only at the shock.
- Unsteady solver (MUSCL + HLLC + SSP-RK3, JAX, jit): Sod converges; smooth-wave L1 orders 0.93 (first order),
  1.86 (minmod), 2.02 (van Leer), 2.00 (unlimited); exact conservation; HLLC keeps R5 to 1e-13.
- Steady nozzle solver: explicit LTS SSP-RK3 and implicit backward Euler with an exact coloured Jacobian
  (21 jvps instead of 360) and CFL backtracking.
- docs/judge: `euler1d_spec.md` (§1–5), `euler1d_slots.md`, `euler1d_cases.md`.
- Dev suite R1–R6, S1, N1–N4 in `cases.py` with YAML loading and admissibility checks.
- Metrics (§9.6, except cost and max_cfl, which need the evaluator / promo), hard constraints on limiter and
  flux slots plus run-level checks, metamorphic measurements (mirror, scaling, Galilean); spec §7–8.
  Sanity: on Sod, superbee < minmod < first order in contact and shock width; mirror error < 1e-12 for symmetric
  limiters and > 1e-6 for Koren; scaling exact to 1e-12.
- Zoo (§9.8, Phase 1 scope) as sandboxed candidate files: 7 limiters, 4 fluxes (Rusanov, HLL, HLLC, Roe),
  first order and WENO5-Z. All pass the sandbox and hard constraints; Roe fails R2 (see blockers).
  The judge's default HLLC is the zoo file.
- R7 Shu–Osher with a cached WENO5-Z reference at N = 12,800 (70 s to build; N = 6,400 differs by 4.3e-4 in L1 ρ
  on 400 cells, 36× below the best zoo error at N = 400).
- `sforge eval` (smoke, dev), `sforge zoo eval` (parallel) and `sforge judge version`: sandboxed worker with
  CPU pinning and CPU-time limit, core locks, wall-clock timeout, registry rows with judge version and hash,
  JSON reports in runs/reports/. Eval refuses uncommitted judge changes.
- Dev suite timing (van Leer, alone): 25.7 s in the worker including JIT, 37 s wall with CLI and worker start.
  With 13 zoo members in parallel each takes 24–68 s (shared memory bandwidth / SMT siblings).
- Judge bug found by the first zoo run and fixed: shocks near the nozzle exit escaped during the transient and
  the solver settled on a spurious supersonic-exit state (roughness_J ≈ 25 for every scheme). Fix: pressure
  outlet for p_b > p_crit2 and a subsonic-exit initial guess in the shock regime (spec §5.3).
- Tests: 184 passed, ruff clean.

## Next (ordered)
1. Held-out families (RF1, RF2, NF1–NF3) from the seed; `judge verify`; `judge exact` for the audit.
2. Blind audit with judge-auditor; problem-existence report `euler1d_baseline.md`; tag `euler1d-v1.0`.

## Blockers / questions for Peter
- Gate 1 decision (proposed in DECISIONS.md): keep Roe in the zoo as a documented known failure on R2 (NaN on
  the 123 problem, as in Einfeldt et al. 1991), instead of dropping it or weakening the positivity constraint.
- Venkatakrishnan with K > 0 does not fit the φ(r) slot (needs dx and absolute differences); the zoo has K = 0.
- Observations for the baseline report (see Numbers):
  - N2 (unchoked, exit Mach 0.085) is dominated by low-Mach dissipation: first-order HLLC underpredicts ṁ by
    75 % at N = 120 (converging slowly with N), MUSCL is within 1–8 %. It is a valid case but tests low-Mach
    behaviour as much as the limiter.
  - Dev budget: an implicit nozzle solve takes ~8 ms per Newton step (N = 120); N1–N4 implicit is 14 solves.
    Measure the full dev suite once `sforge eval` exists; if it exceeds 30 s, cut N4 to fewer points first.
- Appendix H, Toro test 5: our recomputed p* = 1691.65, u* = 8.68977 (v1.0 had this; my v1.1 edit was wrong and
  is reverted). Toro's table rounds the inputs.

## Numbers to remember (run ids, best candidates, costs)
- Machine: 16 physical cores / 32 threads, 15 GB RAM in WSL → evaluation lock default K = 15.
- JAX core pinning: `os.sched_setaffinity` before importing JAX gives CPU/wall 0.98; the XLA flag alone used ~23 cores.
- Unsteady Sod N = 200, van Leer: 4.3 ms per run after JIT (1 core).
- Zoo on the dev suite after the nozzle fix (judge euler1d-v0.dev, reports in runs/reports/):

  | member | R1 shock | R1 contact | S1 order | R7 l1_ref | N1 expl orders | N1 Newton | N4 roughness_J |
  |---|---|---|---|---|---|---|---|
  | superbee | 2.67 | 3.1 | 1.67 | 0.0049 | 1.2 | 300 (no conv.) | 9.67 |
  | MC | 2.74 | 5.42 | 1.91 | 0.0052 | 1.6 | 300 | 11.2 |
  | Koren | 2.77 | 6.1 | 1.84 | 0.0056 | 1.5 | 300 | 12.8 |
  | van Leer | 2.92 | 6.29 | 1.98 | 0.0058 | 2.5 | 60 | 0.0020 |
  | Venkatakrishnan | 2.97 | 6.73 | 1.98 | 0.0059 | 2.7 | 60 | 0.0020 |
  | van Albada | 3.67 | 7.36 | 2.00 | 0.0066 | 12 | 57 | 0.0015 |
  | minmod | 4.21 | 9.29 | 1.83 | 0.0072 | 8.3 | 59 | 0.0014 |
  | WENO5-Z | 2.56 | 3.9 | 3.33 | 0.0023 | 12 | 85 | 0.215 |
  | first order | 9.7 | 22.2 | 0.90 | 0.0126 | 12 | 50 | 0.0013 |

  Fluxes (MUSCL-van Leer): HLL, HLLC, Rusanov, Roe; Roe rejected on R2. First sign that Target A stands:
  sharp limiters stall and give roughness ~1e4× higher; smooth ones converge but smear contacts. To be
  confirmed on NF1/NF3 in the baseline report.
