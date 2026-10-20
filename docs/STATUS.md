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
- Tests: 141 passed, ruff clean.

## Next (ordered)
1. Zoo (§9.8): limiters and fluxes as candidate-style files that pass the sandbox; WENO5-Z, then R7 with its
   cached reference.
2. `sforge eval` / `sforge zoo eval` with the sandbox subprocess, per-core pinning, registry rows; `judge version`.
3. Held-out families (RF1, RF2, NF1–NF3) from the seed; `judge verify`; `judge exact` for the audit.
4. Blind audit with judge-auditor; problem-existence report `euler1d_baseline.md`; tag `euler1d-v1.0`.

## Blockers / questions for Peter
- None blocking. Observations for the baseline report (see Numbers):
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
- First look at Target A (N1, N = 120, explicit, 50k iterations): first order converges (12 orders), minmod
  stalls at 8.3, van Leer at 3.7, superbee at 0.8 orders, all flagged as limit cycles. Implicit: first order,
  minmod, van Leer converge in 111–160 steps; superbee does not converge in 300.
