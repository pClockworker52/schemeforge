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

## Draft thresholds (promo suite; numbers marked ⟨…⟩ come from the WSL promo runs, "Still needed" below)

| # | Metric (family, statistic) | Draft threshold | Why |
|---|---|---|---|
| D1 | GF gap_res, median | ≤ 0.1 × faltus2026 ⟨…⟩ | tight: a factor 10 beyond the robust member, of the order of the neo-Hookean media |
| D2 | HF converged, mean | = 1.00 | robust: every held-out Hertz instance converges |
| D3 | HF max_step, median; HX max_step | = 1; = 1 | robust: one load step, as faltus2026 at γ = 1e-6 (max_step on every HF instance since contact-v0.12) |
| D4 | HF a_err, median of abs | ≤ 0.02 | accurate: about 2× the dev-mesh floor of a (+0.9 %); mesh-stable (spec §mesh_sens) |
| D5 | HF p0_err, median of abs | ≤ 0.02 | about 4× the p0 floor (−0.5 %); mesh-stable |
| D6 | GF leak_pre, median | ≤ faltus2026 ⟨…⟩ | no worse than the robust member before contact |
| D7 | SF shear_parasitic, median | ≤ faltus2026 ⟨…⟩ | guard: no shear stiffness bought for tightness |
| D8 | SL converged, mean; SL shear_parasitic, median | = 1.00; ≤ faltus2026 ⟨…⟩ | C4 (contact-v0.11): it slides where the neo-Hookean media fail, and it resists no more than the robust member (dev C4-g6: faltus2026 6.2 %, wriggers2013 4.0 %, neo-Hookean fail) |

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
   D1–D8 together. The zoo references (⟨…⟩) are the plain zoo (factor 1). The sweep points are
   `scripts/contact_gamma_sweep.py`, registered as zoo-medium-<member>-g<factor>. On dev the mechanism reproduces
   the plain zoo to round-off (r-20261125-073846-e9f0: faltus2026 × 0.1 on C0a-g5 equals faltus2026 on C0a-g6).
2. **Robustness:** max_step on every HF instance (contact-v0.12, 735b69e).
3. **C4 built** (contact-v0.11, 9086db7). It adds D8.

## Still needed before the D commit

- **Peter's WSL promo runs:** the plain zoo plus the sweep (docs/judge/contact_promo_wsl.md). They fill ⟨…⟩ and
  check that no zoo point meets D1–D8.
- **Breakers on the zoo** before the tag (plan §4). They run in WSL, where the sforge MCP server connects.
- Then docs/targets/D.md in its own commit, with thresholds as here unless the promo numbers show that one sits
  inside the error floor or that a zoo point meets all of D1–D8. Either finding goes to Peter first.
