# Round 1 — euler1d / limiter, Target A (2026-10-21)

First hunch round (PLAN §10 task 8, Appendix D), small budget: 4 hunches, ≤ 8 proposer evaluations each, one
engine run with 2 islands × 3 generations × 8 children. Judge `euler1d-v1.1` throughout.

**How it was run.** The plan's subagents (hunch-generator, proposer, breaker) could not be started from the
desktop session (headless agent sessions are blocked there, and the session has no `sforge` MCP tools). The
orchestrator wrote and registered the hunches, implemented the proposals as parameter sweeps and evaluated them
with `sforge eval`; the engine islands used the `claude-cli` backend as designed. The held-out promo suite with
`sforge promote --target A` took the breaker's place (no cases were proposed to quarantine). All hunches were
registered (`sforge hunch add`) before any of their candidates was evaluated.

## Hunches and verdicts

| Hunch | Lens | Idea | Evals | Verdict | Evidence |
|---|---|---|---|---|---|
| H-0001 | approximation theory | superbee with log-sum-exp soft min/max (k = 2, 5, 10, 20) | 4 | **refuted** | k = 10, 20 still stall (N1 1.1 / 1.0 orders, Newton 300; r-20261021-043623-9008, r-20261021-043907-3df4). k = 2, 5 rejected on R3 (non-finite): the soft max adds ≈ log 2 / k at r = 0⁺, above the TVD bound 2r. |
| H-0002 | steady-convergence | MC with a soft min (k = 2, 5, 10, 20) | 4 | **refuted** | no k converges explicitly on N1 (1.7–2.9 orders; r-20261021-044247-9ac2, -044452-3bd2, -044136-6433, -044347-ed73). MC's stall is not only a kink effect. |
| H-0003 | contrarian | compressive below r = 1, flat above: soft min(2r, 1) (k = 5, 10, 20) | 3 | **inconclusive** | kill criterion not met — all k converge on N1 dev (12 orders, Newton 61–75) with contact 6.58–6.72 (van Albada 7.36) and N4 roughness 1.6–5.6e-4 (lowest of all, zoo minmod 1.4e-3); but the predicted contact ≤ 6.5 was missed. Best child, see below. |
| H-0004 | structure preservation | symmetric rational family between van Albada (g = 0) and van Leer (g = 2), g = 0.5, 1, 1.5 | 6 | **refuted** (narrowly) | every g converges on N1 dev; sharpest g = 1.5 has contact 6.438 > 6.4 (r-20261021-045245-da8a). First implementation failed in Newton (r-20261021-044806-2b08 …): a `1/r` branch inside `jnp.where` has an infinite derivative at r = 0. |

## Engine run

`sforge evolve` e-20261021-045407-c003, islands H-0003 and H-0004 seeded with lower_branch_k10 (c-10b8b55fd3) and
sym_rational_direct_g1p5 (c-029de5d726): 48 children, 48 ok on dev, 0 rejected, 0 LLM errors, 6 duplicates,
$2.70 list price (≈ $5.6 per 100). Many children collapsed onto the seed behaviour (contact 6.58 ± 0.01).

Top two by the dev proxies of Target A, then the held-out promo suite and `sforge promote --target A`:

| Candidate | What it is | Dev (run) | Promo (run) | Target A |
|---|---|---|---|---|
| c-44f8015f87 (H-0003, wild child of c-10b8b55fd3) | soft min(2r, 1 + 0.5 tanh(r − 1)), k = 10: 2r below 1, smooth cap rising to 1.5 | R1 shock 2.80, contact 5.46; N1 explicit + implicit, Newton 62; N4 roughness 0.0018 (r-20261021-045513-032a) | RF1 shock 2.99, contact 6.60 (median); NF1 explicit 0.60, implicit 1.00; NF3 roughness p90 0.0018 (r-20261021-050453-0b6a) | not promoted: A1, A2, A3, A7 fail; A4, A5, A6, B1, B2, B5 pass |
| c-5d9d00d656 (H-0004 island, crossover) | smooth symmetric-rational type | R1 3.07 / 6.22; N1 converges, Newton 53 (r-20261021-045744-7ebe) | RF1 3.39 / 7.87; NF1 explicit 0.95, implicit 1.00; NF3 p90 0.0018 (r-20261021-050743-741e) | not promoted: A1, A2, A7b fail; A3–A6, A7a, B1, B2, B5 pass |

Leaderboard delta against the zoo (promo medians, judge v1.0 zoo table in docs/targets/A.md): c-44f8015f87 is
sharper on contacts than van Leer (6.60 vs 7.12) at van Leer's explicit convergence (0.60) and with van Albada-like
roughness and Newton convergence everywhere — a point between van Leer and Koren on the front, not past it.
Label: variant of the superbee/MC family (smooth, capped). Nothing here is a novelty claim.

## Lessons for the next round

1. **Dev N1 is one instance; it overstates explicit convergence.** c-44f8015f87 converged on dev N1 but on only
   60 % of the held-out NF1 family. Before choosing island seeds, run promo on the top 2–3 candidates (≈ 3 min
   each) instead of trusting N1.
2. Soft-min/max smoothing has two traps: the soft max biases φ(0⁺) above 2r (TVD, R3 blows up), and any `1/r`
   branch inside `jnp.where` puts inf · 0 into the Newton Jacobian. Worth one line in the proposer prompt.
3. The islands mostly re-found their seeds; the one real improvement came from a `wild` (haiku) child.

## Open questions for Peter

- H-0003 is inconclusive: worth a second round with the tanh-cap family (cap height and k as parameters) judged on
  promo NF1 explicit convergence, or move to `limiter_stateful` (seed hunch 2), since explicit limit cycles look
  like the binding constraint?
- Should dev get a few more nozzle instances (an N1 sweep like N4) so that explicit convergence is not judged on
  one geometry? That is a judge change (v1.2).
