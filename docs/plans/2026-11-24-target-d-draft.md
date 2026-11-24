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

## Draft thresholds (promo suite; numbers marked ⟨…⟩ come from the promo zoo run in item 3)

| # | Metric (family, statistic) | Draft threshold | Why |
|---|---|---|---|
| D1 | GF gap_res, median | ≤ 0.1 × faltus2026 ⟨…⟩ | tight: a factor 10 beyond the robust member, of the order of the neo-Hookean media |
| D2 | HF converged, mean | = 1.00 | robust: every held-out Hertz instance converges |
| D3 | HX max_step | = 1 | robust: one load step, as faltus2026 at γ = 1e-6 |
| D4 | HF a_err, median of abs | ≤ 0.02 | accurate: about 2× the dev-mesh floor of a (+0.9 %); mesh-stable (spec §mesh_sens) |
| D5 | HF p0_err, median of abs | ≤ 0.02 | about 4× the p0 floor (−0.5 %); mesh-stable |
| D6 | GF leak_pre, median | ≤ faltus2026 ⟨…⟩ | no worse than the robust member before contact |
| D7 | SF shear_parasitic, median | ≤ faltus2026 ⟨…⟩ | guard: no shear stiffness bought for tightness |

D4 and D5 sit above the error floor. p_l2 and leak_out are mesh-sensitive (spec §mesh_sens), so they are reported
only, not thresholds. Guards: hard constraints, all dev cases converge, and the dev suite stays within 60 s and 1 GB.

**Promotion (bootstrap references), as for Target A:** a paired bootstrap of log(candidate / reference) on the
held-out instances, with 10,000 resamples, where the 95 % interval must lie below 0:
- **B1:** GF gap_res against faltus2026 (the robust member's weakness);
- **B2:** HF newton_iters against neo_hooke (the tight member's weakness). There are only 6 instances; see item 2.

**Kill criterion (draft):** 4 rounds or about 2,000 evaluated candidates without a promotion. Then write
docs/results/arena2-negative.md, as for Arena 1.

## Decisions for Peter before the D commit

1. **Rescaling (the cheater lens).** A candidate may rescale γ internally (ψ = c γ ψ_nh passes every constraint,
   unit scaling included). That moves it along a zoo member's own front. Against the zoo at the same γ, a
   rescaled zoo member could look like progress. Draft rule: a candidate counts only if no zoo member with γ scaled
   by any of 10⁻², 10⁻¹, 1, 10, 10² meets D1–D7 together. The zoo references then come from a promo sweep over
   these scale factors (4 media × 5 factors), not from the plain zoo. *Alternative:* fixed thresholds only (as
   above) and rely on D1 + D3 jointly. Modeller's judgment: the sweep is the safer choice, and it is also the check
   that "no zoo member meets D" (as Target A states for its zoo).
2. **Robustness is measured on 7 instances (HF 6, HX 1).** D3 rests on one held-out instance. *Option:* measure
   max_step on all HF instances in promo. This is a judge change, and the cost is about 1–7 min per candidate
   promo (robust media need one trial). *Or:* raise HX from 1 to 6 instances. Either is its own judge commit with
   a zoo check.
3. **The promo zoo run needs the held-out seed, which lives only on Peter's machine** (WSL).
   - Steps: `sforge zoo eval --arena contact --suite promo`, plus the γ-sweep from item 1 if chosen.
   - The run fills the ⟨…⟩ references and checks that no zoo member (or sweep point) meets D1–D7.
   - Only then: commit docs/targets/D.md and tag `contact-v1.0`.
