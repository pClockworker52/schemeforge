# Target A — sharp and smooth steady shock capturing (pre-registered)

Pre-registered 2026-10-20 at Gate 1 (PLAN §2 rule 5, §11.1), from the zoo baseline in
docs/judge/euler1d_baseline.md; thresholds accepted by Peter. Judge: `euler1d-v1.0`. Slot: `limiter` first;
`limiter_stateful` and `reconstruction` candidates are measured against the same thresholds.

## The gap

The zoo has no member that is both as sharp as superbee/MC/Koren and as convergent and smooth as van Albada:
sharp limiters stall (Newton never converges on held-out nozzles) and give objectives 10³–10⁵ times rougher;
smooth limiters converge but pay 0.5–1.4 cells of shock width and 2–6 cells of contact width.

## Thresholds (all must hold on the promo suite)

| # | Metric (family, statistic) | Threshold | Zoo reference (judge v1.0 promo) |
|---|---|---|---|
| A1 | RF1 shock_width, median | ≤ 2.6 cells | superbee 2.49, Koren 2.53, MC 2.54; van Leer 2.94, van Albada 3.42 |
| A2 | RF1 contact_width, median | ≤ 6.5 cells | superbee 4.58, MC 6.12, Koren 6.37; van Leer 7.12, van Albada 8.42 |
| A3 | NF1 converged_expl, mean (share of instances) | ≥ 0.95 | van Albada 0.95, minmod 0.90, van Leer 0.60, Koren 0.55, MC 0.45, superbee 0.05 |
| A4 | NF1 converged_impl, mean (share of instances) | = 1.00 | minmod, van Albada, van Leer, Venkatakrishnan 1.00; MC 0.35, Koren 0.30, superbee 0 |
| A5 | NF3 roughness_J, p90 | ≤ 0.002 | minmod 0.0009, van Albada 0.0015, van Leer 0.0018; superbee 21 |
| A6 | S1 order_smooth (dev) | ≥ 1.9 | van Albada 2.00, van Leer 1.98 |
| A7 | RF1 overshoot p90 and RF2 overshoot p90 | ≤ 1.1 × van Leer's | van Leer RF1 0.0219, RF2 0.0233 |

No zoo member meets A1–A5 together: the sharp limiters fail A3–A5, the convergent ones fail A1–A2.

Guard metrics (may not regress by more than 10 % against van Leer, median): RF1 l1_smooth, NF1 shock_pos_err,
NF2 mdot_var, NF2 converged_impl. Hard constraints and all dev cases must pass.

## Promotion

Per PLAN §5.8: paired bootstrap (10,000 resamples) of log(candidate / best qualifying zoo member) on the
held-out instances for A1, A2 and A5; the 95 % interval must lie entirely on the good side. A3, A4 and A7 are
checked as stated. The statistics come from `sforge eval --suite promo` aggregates; the bootstrap needs the
per-instance values, which the promotion tool reads from ~/.schemeforge/heldout_runs/ (to be built in Phase 2
or 3; agents never see them).

## Kill criterion

4 rounds or about 2,000 evaluated candidates without a promotion (PLAN §11.4) → write
docs/results/arena1-negative.md.
