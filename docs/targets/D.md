# Target D — tight, robust and accurate third-medium contact (pre-registered)

Pre-registered 2026-11-27 at Gate 6 (PLAN §2 rule 5; docs/plans/2026-10-30-phase6.md step 6). Thresholds accepted by
Peter (DECISIONS 2026-11-25 "Target D thresholds accepted"). Rescaling rule and max_step on HF: DECISIONS 2026-11-25
"Gate 6 open items". No breaker case accepted (DECISIONS 2026-11-27 "Arena 2 breakers"). Arena `contact`, slot
`medium`. Draft and its history: docs/plans/2026-11-24-target-d-draft.md.

**Judge.** The references are promo runs on **contact-v0.12.dev** (735b69e; seed fingerprint d4f3b5e7dedec0f6). The
judge is tagged **contact-v1.0** in the next commit, which changes only `JUDGE_VERSION`. The judge tree is otherwise
identical, so the references stand for contact-v1.0.

## The gap

Over all four zoo media and all five stiffness scales, no front point is tight, robust and accurate at once
(docs/judge/contact_baseline.md; dev runs on contact-v0.8.dev: faltus2026 r-20261124-095229-3338, neo_hooke
r-20261124-095309-2957, neo_hooke_iv r-20261124-095346-da9d, wriggers2013 r-20261124-095425-7803):
- **Tight** points (C0a gap_res ≤ 1e-3) are the neo-Hookean media at γ ≤ 1e-5. They have max_step ≤ 0.5 and Hertz a_err
  from −3.9 % to +12 %, or they fail outright at γ = 1e-7.
- **Robust and accurate:** the only point with max_step = 1 and |a_err| ≤ 2 % is faltus2026 at γ = 1e-6. Its gap_res
  is 1.13e-2.
- Classical contact (no medium) is the ideal corner. The target is a medium closer to that corner than the zoo's front.

## Thresholds (all must hold on the promo suite)

| # | Metric (family, statistic) | Threshold | Why |
|---|---|---|---|
| D1 | GF gap_res, median | ≤ 0.1 × faltus2026 = **0.0034** (faltus2026 0.034) | tight: a factor 10 beyond the robust member, of the order of the neo-Hookean media |
| D2 | HF converged, mean | = 1.00 | robust: every held-out Hertz instance converges |
| D3 | HF max_step, median; HX max_step | = 1; = 1 | robust: one load step, as faltus2026 at γ = 1e-6 (max_step on every HF instance since contact-v0.12) |
| D4 | HF a_err, median of abs | ≤ 0.02 | accurate: about 2× the dev-mesh floor of a (+0.9 %), above the random-instance floor (≤ 1.33 %, blind audit); mesh-stable (spec §mesh_sens) |
| D5 | HF p0_err, median of abs | ≤ 0.02 | about 4× the p0 floor (−0.5 %); mesh-stable |
| D6 | GF leak_pre, median | ≤ faltus2026 = **5.59e-4** | no worse than the robust member before contact |
| D7 | SF shear_parasitic, median | ≤ faltus2026 = **3.84e-3** | guard: no shear stiffness bought for tightness |
| D8 | SL converged, mean; SL shear_parasitic, median | = 1.00; ≤ faltus2026 = **0.102** | C4 (contact-v0.11): it slides where the neo-Hookean media fail, and it resists no more than the robust member (dev C4-g6: faltus2026 6.2 %, wriggers2013 4.0 %, neo-Hookean fail) |

D4 and D5 sit above the judge's error floor: dev a +0.9 %, p0 −0.5 %; random instances a −1.25 … +1.33 %, p0
−0.57 … +0.19 % (blind audit, audit/contact/REPORT.md). p_l2 and leak_out are mesh-sensitive (contact_spec.md
§mesh_sens), so they are reported only.

**Guards:** hard constraints; every dev case converges; the dev suite stays within 60 s and 1 GB per candidate.

## Rescaling rule

A candidate counts only if no zoo member meets D1–D8 together with γ scaled by any of 10⁻², 10⁻¹, 1, 10 or 10². The
sweep points are `scripts/contact_gamma_sweep.py`, registered as zoo-medium-<member>-g<factor>. This guards against
a candidate that only rescales γ. On dev, the mechanism reproduces the plain zoo to round-off
(r-20261125-073846-e9f0).

## Promotion (bootstrap references)

As for Target A (PLAN §5.8): a paired bootstrap of log(candidate / reference) over the held-out instances, 10,000
resamples. The 95 % interval must lie entirely below 0.
- **B1:** GF gap_res against **faltus2026**, the robust member's weakness.
- **B2:** HF newton_iters against **neo_hooke**, the tight member's weakness, paired over the 6 HF instances. A
  bootstrap over 6 pairs is coarse, so D3 (max_step on every HF instance) carries the robustness threshold.

D1–D8 and the rescaling rule are checked as stated. The promotion check is not yet implemented in
`src/schemeforge/core/promotion.py` (TARGETS holds A and A-c); it is part of step 7 (search readiness).

## Zoo references and the sweep check (promo, contact-v0.12.dev)

Peter's WSL runs of 2026-11-25. The table was printed by `scripts/contact_target_d_table.py`; it holds aggregates
only. HF |a| and |p0| are medians of absolute values. `nan` means no instance converged for that metric. The D1..D8
column shows `+` where a threshold is met.

| point | run | GF gap_res | GF leak_pre | SF shear | HF conv | HF max_step | HX max_step | HF \|a\| | HF \|p0\| | SL conv | SL shear | D1..D8 | all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| faltus2026 | r-20261125-180442-ceee | 0.034 | 0.000559 | 0.00384 | 1 | 1 | 1 | 0.0764 | 0.0346 | 1 | 0.102 | -++--+++ | no |
| faltus2026 ×0.01 | r-20261125-181302-40b2 | 0.00505 | 5.61e-06 | 3.84e-05 | 1 | 0.5 | 0.167 | 0.0325 | 0.00511 | 1 | 0.0369 | -+--++++ | no |
| faltus2026 ×0.1 | r-20261125-181302-4d4e | 0.0133 | 5.6e-05 | 0.000384 | 1 | 0.5 | 1 | 0.0161 | 0.00864 | 1 | 0.055 | -+-+++++ | no |
| faltus2026 ×10 | r-20261125-181302-3ef3 | 0.0832 | 0.00544 | 0.0384 | 1 | 1 | 1 | 0.247 | 0.0957 | 1 | 0.196 | -++----- | no |
| faltus2026 ×100 | r-20261125-181302-4f65 | 0.188 | 0.0455 | 0.384 | 1 | 1 | 1 | 1.04 | 0.213 | 1 | 0.312 | -++----- | no |
| neo_hooke | r-20261125-180441-78df | 0.00104 | 0.000285 | 0.000247 | 1 | 0.375 | 0.25 | 0.0474 | 0.0076 | 0 | nan | ++--+++- | no |
| neo_hooke ×0.01 | r-20261125-181302-de6e | 1.93e-05 | 3.28e-06 | 2.47e-06 | 0 | 0 | nan | nan | nan | 0 | nan | +----++- | no |
| neo_hooke ×0.1 | r-20261125-181302-e412 | 0.000134 | 2.85e-05 | 2.47e-05 | 0.5 | 0.0417 | nan | 0.0417 | 0.00852 | 0 | nan | +---+++- | no |
| neo_hooke ×10 | r-20261125-181302-d6e0 | 0.00745 | 0.00284 | 0.00247 | 1 | 1 | 1 | 0.253 | 0.0168 | 0.75 | 0.018 | -++-+-+- | no |
| neo_hooke ×100 | r-20261125-181302-bb9d | 0.0456 | 0.027 | 0.0247 | 1 | 1 | 1 | 1.75 | 0.113 | 1 | 0.0478 | -++----+ | no |
| neo_hooke_iv | r-20261125-180441-89cc | 0.00279 | 0.00022 | 0.000247 | 1 | 0.5 | 0.5 | 0.0488 | 0.00591 | 0.5 | 0.0273 | ++--+++- | no |
| neo_hooke_iv ×0.01 | r-20261125-181303-3662 | 0.000177 | 2.2e-06 | 2.47e-06 | 0.333 | 0 | nan | 0.0498 | 0.00981 | 0 | nan | +---+++- | no |
| neo_hooke_iv ×0.1 | r-20261125-181302-b747 | 0.000703 | 2.2e-05 | 2.47e-05 | 1 | 0.146 | 0.25 | 0.0351 | 0.00801 | 0 | nan | ++--+++- | no |
| neo_hooke_iv ×10 | r-20261125-181303-cca0 | 0.0109 | 0.0022 | 0.00247 | 1 | 1 | 1 | 0.245 | 0.013 | 1 | 0.0423 | -++-+-++ | no |
| neo_hooke_iv ×100 | r-20261125-181406-1edd | 0.0414 | 0.0214 | 0.0247 | 1 | 1 | 1 | 1.7 | 0.0621 | 1 | 0.102 | -++----+ | no |
| wriggers2013 | r-20261125-180442-8e1d | 0.0413 | 0.00102 | 0.000992 | 1 | 1 | 1 | 0.17 | 0.0258 | 1 | 0.0508 | -++---++ | no |
| wriggers2013 ×0.01 | r-20261125-181455-19ef | 0.0167 | 1.02e-05 | 9.92e-06 | 1 | 0.5 | 0.5 | 0.0192 | 0.0042 | 1 | 0.0355 | -+-+++++ | no |
| wriggers2013 ×0.1 | r-20261125-181504-5c8b | 0.0263 | 0.000102 | 9.92e-05 | 1 | 0.5 | 0.5 | 0.0265 | 0.0117 | 1 | 0.0413 | -+--++++ | no |
| wriggers2013 ×10 | r-20261125-181508-d650 | 0.0652 | 0.0101 | 0.00992 | 1 | 1 | 1 | 0.916 | 0.0499 | 1 | 0.0727 | -++----+ | no |
| wriggers2013 ×100 | r-20261125-181513-a882 | 0.11 | 0.0915 | 0.0992 | 1 | 1 | 1 | 3.57 | 0.151 | 1 | 0.131 | -++----- | no |

**No zoo point at any scale meets D1–D8 together.**
- The closest points are faltus2026 ×0.1 and wriggers2013 ×0.01, which meet 6 of 8. Both miss D1 by a factor 4–5 and
  miss D3.
- D4 is the narrowest threshold: only 2 of the 20 points meet it.

## Known limits of the judge (Gate 6 report)

- ν outside 0.15–0.45, simple shear s > 3, slides beyond C4's 0.05–0.2 a, and indentations below one column are
  outside the declared scope (breakers 2026-11-27, docs/rounds/2026-11-27-contact-breakers.md).
- At ν = 0.45, inside the HF range, every zoo member misses |a_err| 2 % (8–21 %). This is part of the references above.
- 65 of 450 audit gap closures outside the GF ranges do not converge. C4 was not part of the blind audit.

## Kill criterion

4 rounds or about 2,000 evaluated candidates without a promotion, as for Arena 1 (PLAN §11.4; the draft's
criterion). Then write docs/results/arena2-negative.md.
