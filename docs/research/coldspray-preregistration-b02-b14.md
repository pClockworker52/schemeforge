# Cold spray: pre-registration for blind papers B02 and B14 (and B04, B13 without v_cr)

Frozen 2026-11-07, committed with `data/predictions_b02_b14.csv` **before** any outcome of these papers is extracted
(rule B2, step 2). Inputs: `data/blind_inputs.csv`, rows B02, B04, B13, B14, as merged in 7a9e0b5. Leak-scanned
before reading: the only velocity-related hits were a Hugoniot sound speed (B04), a saw speed and a sound-speed
table reference (B02), a spray-gun traverse speed (B13), and "TEM/STEM" read as "m/s" (B14); no outcome. Code:
`src/schemeforge/research/coldspray_blind2.py` (first general version; B10's code stays frozen as it was).

**Sources.** WSL B extracted B04 and B14 from Lienhard's PhD thesis (MIT 2022) and B02 from Lucas's PhD thesis (MIT
2025). The theses state that the chapters follow the published articles (B02: by title match only). Scoring uses
the same source at step 3.

## Papers without a prediction

- **B04** (Sn and Zn above the critical velocity) and **B13** (Fe-based metallic glass, single-pass cold-spray splats,
  not LIPIT) report no v_cr for their conditions (`measures_vcr = no`). Nothing is predicted or scored.

## Exposure (rule B4)

- **B14 (Lienhard 2020):**
  - the relative effect (+14 % v_cr at 95 % RH, +2–3 nm) is known via Veysset2021;
  - the model form, jet thickness (100 nm) and oxide strength (870 MPa) are known via Na2025 (logged 2026-11-05);
  - the statement that thicker oxides raise v_cr "even with changes as small as a few nanometers" is known via
    Na2025.

  **All B14 verdicts are reported as exposed.**
- **B02 (Lucas 2025):** Panova2026b quotes "half-hard Cu v_cr 539–588" from B02, B03 and HG2018b together (logged in
  the blind list). B02's substrates are soft (O temper) and full-hard (H04), not half-hard. The modeller has also
  seen PA-01 (Panova2026b: 19 µm Cu powder on a polished plate of 98 HV, 567 m/s). **B02 is reported as partly
  exposed.**

## Rules

- **Input rules** of each frozen model, unchanged:
  - Z6 and the baseline by the v1 rules;
  - DW_size for Al and Ti;
  - CS-10 needs a particle strength (static compression, else powder hardness) and a numeric oxide thickness;
  - Z18 needs Al and a particle strength (Z18_static) or a sub-critical Y_d of an Al powder (Z18_Yd).
- **Neither paper reports a particle strength for the impacted powder,** so CS-10 and both Z18 variants give **no
  prediction** (recorded in the CSV with the reason). B02's dynamic yield strength of 383 MPa comes from
  Cu-on-sapphire impacts, and Cu is outside Z18's domain.
- **Temperatures:** room (B14 states it; B02 does not, rule BP3).
- **Score:** rule S1 per condition. Windows as printed, else rule B6 (v_cr ± the stated velocity uncertainty; if
  none is stated, only sign and rank verdicts).
- **w** = median window width of the paper.
- **Oxide thickness** as parsed by `oxide_thickness_nm`: B14-c1, c3–c6 5.5 nm (~5–6 nm); c7 8 nm; c2 and c8 no numeric
  value ("not separately reported"; "thinner than RH-95 by less than 1 nm").

## Frozen predictions (m/s; `data/predictions_b02_b14.csv`)

| Model | B14, all eight conditions (Al, 11 µm) | Domain | B02, both conditions (Cu, 19 µm) | Domain |
|---|---|---|---|---|
| Z6_a015 | 805.1 | in | 578.6 | out (d > 16 µm) |
| Z6_a015_C0 | 807.0 | in | 586.5 | out |
| baseline_LOMO | 611.5 | in | 696.5 | out |
| DW_size | 951.1 | in | — (Al and Ti only) | — |
| CS-10, Z18_static, Z18_Yd | no prediction (no particle strength) | — | no prediction | — |

Every model with a prediction gives one value per paper, because none has a term for what varies within a paper
(oxide treatment in B14, substrate temper in B02).

## Hunch tests on B14 (all exposed)

Groups: **D** = {c1, c3, c4, c5}, the dry series with a stated ~5–6 nm amorphous layer. **H** = {c7}, RH-95, ~8 nm
with crystalline (oxy)hydroxide pockets.

```yaml
- id: CS-07 on B14
  statement: Oxide raises v_cr within one metal (registered as CS-07).
  metric: Delta_H = v(c7) - mean v(D)
  kill_criterion: >-
    Refuted if Delta_H <= 0. Supported if Delta_H > w. Inconclusive otherwise. Caveat: thickness and oxide type
    change together (hydroxide), so support is not specific to thickness. Exposed: the relative effect is known.
- id: dry-series consistency (reported, no hunch verdict)
  metric: max - min of v(c1), v(c3), v(c4), v(c5)
  reading: >-
    Same powder, same stated oxide thickness and type, different thermal histories (300 C in argon and dry air).
    Z6, the baseline, and CS-12(c) all expect one v_cr within a window. Reported against w and 2w, as for CS-09.
- id: RH-95-D against RH-95 (reported, no hunch verdict)
  metric: v(c8) - v(c7)
  reading: >-
    Nearly the same thickness (less than 1 nm apart), the oxide type changed back (no crystallinity, OH bands gone).
    Thickness-only models (CS-10, Z18 in form) expect a difference of a few m/s at most. CS-12 lets Y' change with
    type but predicts no direction (its T4). Reported against w.
```

CS-12's decisive test T3 does not apply: the thickness span at one oxide type is under 5 nm.

## B02

Only out-of-domain Z6 and baseline values exist; both are identical for the two substrates. A hunch on substrate
hardness may be registered as an addendum to this file. Any addendum must be committed **before** the step-3
extraction of B02's outcomes. No other change is allowed after this commit.

## Step 3

The outcomes of B02 and B14 are extracted after this commit, with the step-3 prompt, into `data/vcr_lipit.csv`
with prefixes `B-B02-` and `B-B14-`, then scored by a script committed separately before the outcomes are read.

## Addendum 1 (2026-11-07, before step 3): hunch CS-16 on B02

Registered on Peter's instruction, as the B02 addendum allowed above, before any outcome of B02 is extracted. Code:
`cs16_predict` in `coldspray_blind2.py`. Predictions: `data/predictions_b02_cs16.csv`. The frozen
`predictions_b02_b14.csv` is unchanged.

```yaml
- id: CS-16
  registered: 2026-11-07 (frozen in this addendum)
  assumption_broken: >-
    H2 in part (the substrate's state does not matter) and the substrate-free form of every zoo member: Z6, the
    baseline, CS-10 and Z18 use particle properties only.
  statement: >-
    For matched Cu, a harder substrate raises v_cr, as v_cr ~ HV_substrate^n with n fitted on two seen rows of the
    same 19 um Cu powder (Panova2026b PA-01, 98 HV, 567 m/s; PA-02, 142 HV, 653 m/s): n = 0.3808.
  mechanism: >-
    A harder substrate deforms less and forms a smaller crater, so less of the jetting and interface stretch comes
    from the substrate side; the particle must arrive faster to reach the same interface state.
  predictions: {B02-c1 (soft, 63.4 HV): 480.4, B02-c2 (hard, 105.2 HV): 582.6, Delta_pred = c2 - c1: +102.2}
  kill_criterion: >-
    w = B02's median window width (rule B6 where not printed). Refuted if Delta_meas <= 0, or if
    |Delta_meas - Delta_pred| > w + 0.5 Delta_pred. Supported if |Delta_meas - Delta_pred| <= w and
    Delta_pred > w. Inconclusive otherwise. The absolute values are scored by rule S1, with no verdict.
  caveats:
    - PA-02's substrate is a polished cold-sprayed Cu layer, so microstructure changes with hardness.
    - Panova's v_cr is the mean of the last two rebounds and the first two bonds, not an equal-count window.
    - Fitted on two points; B02-c1 (63 HV) lies below the fitted range (98-142 HV), an extrapolation.
    - Partly exposed: a "half-hard Cu 539-588" quote attributed to B02, B03 and HG2018b together is known.
  known_relatives: [Panova2026b (substrate hardness and growth surface), Hassani2020 (impact ratio, Z9), Lucas 2025
    (B02 itself, unread)]
  label: none yet (referee)
  status: open
  author: claude (with Peter)
```
