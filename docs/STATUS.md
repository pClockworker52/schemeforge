# STATUS
Phase: 1 — Arena 1 judge and zoo (at Gate 1, waiting for Peter)      Judge version: euler1d-v0.dev (untagged)
Last session: 2026-10-20 — Phase 1 complete except the blind audit; baseline report written

## Gate 1 (PLAN §9.11)
- [x] Appendix H reproduced: Toro star states to the quoted digits, nozzle values to 4–5 digits
      (`sforge judge verify`, 51/51 checks; tests). Toro test 5 uses the recomputed 1691.65 / 8.68977.
- [ ] **Blind audit agrees on ≥ 1,000 instances** — Peter runs it in a WSL session: docs/judge/euler1d_audit.md.
- [x] Zoo sanity: superbee narrowest and minmod widest Sod contact among the limiters; HLLC and Roe keep the
      stationary contact R5 exactly, HLL and Rusanov smear it (`judge verify`).
- [x] Hard constraints and metamorphic tests pass for every zoo member — **except Roe on R2** (positivity; NaN
      on the 123 problem, as in Einfeldt et al. 1991). Decision needed (below).
- [x] Dev suite ≤ 30 s per candidate on one core, JIT included: 25.7 s (van Leer, alone).
- [x] `docs/judge/euler1d_baseline.md` written; Target A/B recommendation inside — **decision needed** (below).
- [ ] Judge tagged `euler1d-v1.0` — after the audit and Peter's decisions (bump JUDGE_VERSION, tag, rerun zoo).

## Decisions for Peter at Gate 1
1. **Roe**: keep it in the zoo as a documented known failure on R2 / some RF1 instances (proposed), or drop it.
2. **Target A thresholds** (baseline §5, proposed): RF1 shock width median ≤ 2.6 cells and contact ≤ 6.5;
   NF1 explicit converged in ≥ 95 % and implicit in 100 % of instances; NF3 roughness_J p90 ≤ 0.002;
   S1 order ≥ 1.9; RF1/RF2 overshoot p90 no worse than van Leer. Confirm or change → docs/targets/A.md.
3. **Target B**: proposed to build the `operator` slot and its well-balanced baseline at the start of Phase 3
   and set thresholds then.
4. **Venkatakrishnan K > 0**: not in the φ(r) slot (needs dx); fine to defer to the reconstruction slot?
5. **Billing**: WSL Claude Code showed "API Usage Billing" earlier; you said you would switch to the subscription.

## Done (Phase 1)
- Exact Riemann (Toro ch. 4) and exact nozzle solutions with Hypothesis property tests; spec §1–4.
- Unsteady solver (MUSCL + HLLC + SSP-RK3, JAX) and steady nozzle solver (explicit LTS RK3, implicit Newton with
  exact coloured Jacobian, pressure outlet, regime-dependent initial guess); spec §5.
- Metrics, hard constraints, metamorphic measurements; spec §7–8. Unresolved jumps are not measured.
- Zoo as sandboxed candidate files: 7 limiters, 4 fluxes, first order, WENO5-Z; R7 Shu–Osher reference.
- Dev suite R1–R7, S1, N1–N4; held-out families RF1 20, RF2 10, NF1 20, NF2 10, NF3 5 from the secret seed.
- `sforge eval` (smoke/dev/promo), `zoo eval`, `judge version|verify|exact` (batch), `reveal` (TTY only):
  sandboxed worker, core locks, registry, promo aggregates only; instance details in ~/.schemeforge/heldout_runs/.
- Four judge artifacts found by the zoo runs and fixed (see baseline §6 and git log).
- Tests: 202 passed, ruff clean.

## Next (ordered)
1. Peter: blind audit (docs/judge/euler1d_audit.md); then tell the main session to review audit/euler1d/REPORT.md.
2. Peter: Gate 1 decisions above.
3. Then: fix anything the audit finds, set JUDGE_VERSION = "euler1d-v1.0", commit, tag, `sforge zoo eval` dev and
   promo, write docs/targets/A.md, and start Phase 2 (§10).

## Notes
- Run everything in WSL; the venv lives at ~/.venvs/schemeforge behind the `.venv` symlink (DECISIONS.md).
- Promo per candidate: 2–5.5 min with 13 in parallel; zoo dev ~70 s, zoo promo ~6 min wall.
- Use `set -o pipefail` when chaining tests with `| tail` before a commit.

## Numbers to remember (run ids, best candidates, costs)
- Machine: 16 physical cores / 32 threads, 15 GB RAM in WSL → evaluation lock default K = 15.
- JAX core pinning: `os.sched_setaffinity` before importing JAX (CPU/wall 0.98); the XLA flag alone used ~23 cores.
- Unsteady Sod N = 200, van Leer: 4.3 ms per run after JIT; dev cost metric ~40 ns per cell update.
- Zoo results: docs/judge/euler1d_baseline.md (dev + held-out aggregates, 41-point sweep, front plot).
