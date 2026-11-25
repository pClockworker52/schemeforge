# Target D: draft for Peter (2026-11-24; NOT pre-registered)

Plan step 6 requires that Target D is pre-registered from the zoo front, outside the judge's error floor, with
held-out checks and bootstrap references, in its own commit. This file is the draft. It becomes `docs/targets/D.md`
only after Peter accepts it and the promo zoo references (item 3 below) are filled in.

## The gap (from the front)

Source: docs/judge/contact_baseline.md and docs/judge/baseline/contact_front.json. These are measurements by the
judge functions on the dev mesh, not registered runs. Registered dev runs of the zoo on contact-v0.8.dev:
faltus2026 r-20261124-095229-3338, neo_hooke r-20261124-095309-2957, neo_hooke_iv r-20261124-095346-da9d,
wriggers2013 r-20261124-095425-7803.

Over all four media and all five stiffness scales, the front contains no point that is tight, robust and accurate at
once:
- **Tight.** Every point with C0a `gap_res` ≤ 1e-3 belongs to the neo-Hookean media at γ ≤ 1e-5. All of them have
  `max_step` ≤ 0.5 and Hertz `a_err` of −3.9 % to +12 %, or they fail outright at γ = 1e-7.
- **Robust and accurate.** The only point with `max_step` = 1 and |`a_err`| ≤ 2 % is faltus2026 at γ = 1e-6, and its
  `gap_res` is 1.13e-2.
- Classical contact is the ideal corner (no medium). The target is a medium that comes closer to that corner than
  the zoo's front.

## Draft thresholds (promo suite; references from the WSL promo runs of 2026-11-25, judge contact-v0.12.dev)

| # | Metric (family, statistic) | Draft threshold | Why |
|---|---|---|---|
| D1 | GF gap_res, median | ≤ 0.1 × faltus2026 = **0.0034** (faltus2026 0.034) | tight: a factor 10 beyond the robust member, of the order of the neo-Hookean media |
| D2 | HF converged, mean | = 1.00 | robust: every held-out Hertz instance converges |
| D3 | HF max_step, median; HX max_step | = 1; = 1 | robust: one load step, as faltus2026 at γ = 1e-6 (max_step on every HF instance since contact-v0.12) |
| D4 | HF a_err, median of abs | ≤ 0.02 | accurate: about 2× the dev-mesh floor of a (+0.9 %), above the random-instance floor (≤ 1.33 %, blind audit); mesh-stable (spec §mesh_sens) |
| D5 | HF p0_err, median of abs | ≤ 0.02 | about 4× the p0 floor (−0.5 %); mesh-stable |
| D6 | GF leak_pre, median | ≤ faltus2026 = **5.59e-4** | no worse than the robust member before contact |
| D7 | SF shear_parasitic, median | ≤ faltus2026 = **3.84e-3** | guard: no shear stiffness bought for tightness |
| D8 | SL converged, mean; SL shear_parasitic, median | = 1.00; ≤ faltus2026 = **0.102** | C4 (contact-v0.11): it slides where the neo-Hookean media fail, and it resists no more than the robust member (dev C4-g6: faltus2026 6.2 %, wriggers2013 4.0 %, neo-Hookean fail) |

D4 and D5 sit above the error floor. p_l2 and leak_out are mesh-sensitive (spec §mesh_sens), so they are reported
only, not thresholds. Guards: hard constraints, all dev cases converge, and the dev suite stays within 60 s and 1 GB.

**Promotion (bootstrap references), as for Target A:** a paired bootstrap of log(candidate / reference) on the
held-out instances, with 10,000 resamples, where the 95 % interval must lie below 0:
- **B1:** GF gap_res against faltus2026 (the robust member's weakness);
- **B2:** HF newton_iters against neo_hooke (the tight member's weakness), paired over the 6 HF instances. A
  bootstrap over 6 pairs is coarse; D3 (max_step on every HF instance) carries the robustness threshold.

**Kill criterion (draft):** 4 rounds or about 2,000 evaluated candidates without a promotion. Then write
docs/results/arena2-negative.md, as for Arena 1.

## Decided (DECISIONS 2026-11-25, Peter)

1. **Rescaling:** a candidate counts only if no zoo member with γ scaled by any of 10⁻², 10⁻¹, 1, 10, 10² meets
   D1–D8 together. The zoo references are the plain zoo (factor 1). The sweep points are
   `scripts/contact_gamma_sweep.py`, registered as zoo-medium-<member>-g<factor>. On dev the mechanism reproduces
   the plain zoo to round-off (r-20261125-073846-e9f0: faltus2026 × 0.1 on C0a-g5 equals faltus2026 on C0a-g6).
2. **Robustness:** max_step on every HF instance (contact-v0.12, 735b69e).
3. **C4 built** (contact-v0.11, 9086db7). It adds D8.

## Promo references and the sweep check (2026-11-25, Peter's WSL runs)

Judge contact-v0.12.dev; seed fingerprint d4f3b5e7dedec0f6. The table was printed by
`scripts/contact_target_d_table.py` on Peter's machine (aggregates only). HF |a| and |p0| are medians of absolute
values; `nan` means no instance converged for that metric. Plain-zoo runs: faltus2026 r-20261125-180442-ceee,
neo_hooke r-20261125-180441-78df, neo_hooke_iv r-20261125-180441-89cc, wriggers2013 r-20261125-180442-8e1d. Sweep
runs: as listed.

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

**Check passed:** no zoo point at any scale meets D1–D8 together.

**Reading (modeller):**
- **Closest points:** faltus2026 ×0.1 and wriggers2013 ×0.01 pass 6 of 8. Both miss D1 by a factor 4–5
  (gap_res 0.0133 and 0.0167) and D3 (HF max_step 0.5).
- **Tight points are fragile.** Every point that meets D1 has HF max_step ≤ 0.5 and fails D8.
- **The tightest fully robust point** (HF and HX max_step 1) is neo_hooke ×10, at gap_res 0.0075. It misses D4 by
  far (|a| 0.25).
- **D4 is the narrowest threshold.** Only two points meet it, and it sits above the random-instance floor (≤ 1.33 %)
  by a modest margin.
- **The dev front was optimistic about the robust media.** faltus2026 meets |a| 1.0 % at dev γ = 1e-6, but has a
  median of 7.6 % on HF, where γ is 1e-6–1e-5.

## Still needed before the D commit

- ~~Peter's WSL promo runs~~: done (table above). No zoo point meets D1–D8, and no threshold sits inside the error
  floor.
- **Breakers on the zoo** (plan §4; WSL, sforge MCP). If a breaker case is accepted into the judge, the judge version
  changes and the promo references above must be rerun. So docs/targets/D.md is committed after the breaker review,
  on the judge version it will be tagged with.
- **Peter accepts the thresholds**, then docs/targets/D.md goes in its own commit.
