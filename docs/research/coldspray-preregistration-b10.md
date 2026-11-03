# Cold spray: pre-registration for blind paper B10 (Na et al. 2025, Al 6061 heat-treatment series)

Frozen 2026-11-03, committed with `data/predictions_b10.csv` **before** B10's outcomes are extracted (rule B2,
step 2). Inputs: `data/blind_inputs.csv` rows B10-c1 to B10-c5 (leak-scanned before reading). Code:
`src/schemeforge/research/coldspray_blind.py`.

**Exposure note.** The modeller knows the retrospective Al 6061 window of Hassani2020 (900–950 m/s, 13 ± 3 µm,
different powder) from the v1 tables. No B10 outcome has been seen.

## Conditions (inputs only)

LIPIT, Al 6061 powder on polished Al 6061-T6, d = 15 ± 1 µm, temperatures not stated (room assumed).

| Condition | Treatment | Static compression strength (MPa, ~35 µm particles, 50 % strain) | Oxide shell (nm, TEM/EDS FWHM) |
|---|---|---|---|
| c1 | as received | 351.3 ± 62.7 | 16.8 |
| c2 | 230 °C, 75 min | 298.1 ± 36.1 | 17.0 |
| c3 | 530 °C, 75 min | 218.8 ± 46.0 | 18.9 |
| c4 | 530 °C, 240 min | 233.0 ± 76.7 | 24.0 |
| c5 | 530 °C + 170 °C, 8 h | 237.8 ± 44.5 | 24.7 |

Groups used below: **S** = {c1, c2} (high strength, thin oxide), **W** = {c3, c4, c5} (low strength, thick
oxide). Strength and oxide thickness are anti-correlated across the groups, so a strength mechanism and an oxide
mechanism predict opposite group differences.

## Rules for this paper

- **BP1 (Peter, 2026-11-03):** strength-dependent models use the paper's static compression strength in place of
  σ_u / σ_TS. The impact-fitted Y_d is unavailable for blind papers (it is fitted to rebound data, an outcome).
- **BP2:** Al 6061 has no sourced T_m or c_p in `properties.csv`; Z1 and Z2 use the pure-Al values (P-HG-Al:
  933 K, 896.9 J/kg K), flagged.
- **BP3:** temperatures not stated, so room temperature is assumed (T_i = 20 °C).
- **BP4:** Z1 and Z2 are declared out of domain (calibrated on process critical velocities; Z2 on 25 µm). Z6 and
  the baseline are in domain (rule D1: matched, room temperature, polished, 8–16 µm).
- **Scoring:** rule S1 per condition (distance outside the measured window / midpoint), plus the group contrasts
  below. Δ = mean v_cr(S) − mean v_cr(W) from the measured window midpoints; w = median measured window width.

## Frozen predictions (m/s; `data/predictions_b10.csv`)

| Model | c1 | c2 | c3 | c4 | c5 | Domain |
|---|---|---|---|---|---|---|
| Z6_a015 | 750.8 | 750.8 | 750.8 | 750.8 | 750.8 | in |
| Z6_a015_C0 | 802.5 | 802.5 | 802.5 | 802.5 | 802.5 | in |
| baseline_LOMO | 611.5 | 611.5 | 611.5 | 611.5 | 611.5 | in |
| Z1_Assadi_static | 709.1 | 703.8 | 695.9 | 697.3 | 697.8 | out |
| Z2_Schmidt_static | 892.5 | 837.9 | 749.0 | 765.7 | 771.2 | out |

## Hunches tested on B10

```yaml
- id: CS-08
  registered: 2026-11-03
  assumption_broken: Z6 (strength is swamped by impact pressure; HG2018a)
  statement: Particle strength raises v_cr within one alloy, at fixed density and sound speed.
  mechanism: >-
    Jetting needs the interface to flow hydrodynamically; a stronger particle resists the outward flow at the
    contact edge longer, so a higher impact pressure, hence velocity, is needed before jetting sets in (spall /
    strength terms of HG2019 and Lucas2025; strength terms of Z1, Z2).
  predicted_effect: [{metric: Delta, direction: up, size: "> w (S above W by more than a typical window)"}]
  kill_criterion: Refuted if Delta <= 0. Supported if Delta > w. Inconclusive if 0 < Delta <= w.
  known_relatives: [Assadi2003 (Z1), Schmidt2006 (Z2), HG2019 response, Lucas2025, Hassani2020 Al-alloy rows]
  label: variant of the strength terms in Z1/Z2 (referee to confirm)
  author: claude (with Peter)
- id: CS-07 on B10
  statement: Same-metal oxide effect (registered as CS-07); here oxide thickness rises from S to W.
  predicted_effect: [{metric: Delta, direction: down, size: "< -w (W above S by more than a typical window)"}]
  kill_criterion: >-
    For B10, refuted if Delta >= 0. Supported (for the same-metal part of CS-07) if Delta < -w. Inconclusive if
    -w <= Delta < 0. Caveat: strength and oxide co-vary with the heat treatment, so B10 can support at most one of
    CS-07 and CS-08, and support for one is not proof of its mechanism.
- id: CS-09
  registered: 2026-11-03
  statement: Sound speed alone (Z6) holds within an alloy series. All five B10 windows are mutually consistent
    with a single v_cr.
  predicted_effect: [{metric: "max - min of the five measured midpoints", direction: same, size: "<= w"}]
  kill_criterion: Refuted if max - min > 2 w. Supported if <= w. Inconclusive otherwise.
  known_relatives: [HG2018a]
  author: claude (with Peter)
```

Reported in addition (not hunches): S1 distances for every model and condition, and whether Z2's predicted
ordering (S above W) matches the measured one.

## Step 3

B10's measured windows are extracted after this commit, into `data/vcr_lipit.csv` with prefix `B-`, together with
the window definition the paper uses, then scored by a script committed separately.
