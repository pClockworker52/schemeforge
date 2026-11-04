# Cold spray: hunch CS-10 (combined strength + oxide energy balance), registration

Registered 2026-11-04, **before** its two constants are fitted and before any further blind paper is frozen. The
commit of this file is the timestamp; the fit and its code come in a later commit (git order is the proof).
Research track, not a ledger arena. Assumption numbers refer to [coldspray-go-nogo.md](coldspray-go-nogo.md).

## Why

B10 (Na2025, [coldspray-results-b10.md](coldspray-results-b10.md)) refuted strength alone (CS-08: Δ = −30.5 m/s)
and left oxide alone not refuted (CS-07). Across the five heat treatments, strength fell (351 → 219 MPa) while the
oxide grew (16.8 → 24.7 nm), and v_cr stayed within 77 m/s. One reading: both mechanisms act and offset each other.
CS-10 makes that reading quantitative so that later blind papers can kill it.

## Exposure (rule B4)

- The modeller has seen all B10 inputs and outcomes, and the authors' qualitative conclusion (strength loss and
  oxide growth offset; a combined model with one fitted constant fits best). **B10 is calibration data for CS-10;
  any B10 number for CS-10 is in-sample.**
- The form of Na2025 Eq. 6 (described in the handoff as a Lienhard rule of mixtures) has **not** been read in this
  session. CS-10's form below comes from the energy-balance argument, not from Eq. 6; the referee must compare the
  two before any label beyond "variant of" is considered.
- B14 (Lienhard2020, Al oxide/hydroxide): the relative effect (+14 % v_cr at 95 % RH, +2–3 nm) is known via
  Veysset2021. A K1 result on B14 is reported separately as exposed.

## Form

Kinetic energy per unit particle volume at the critical velocity covers three costs, added in v² as in the
energy balance of Schmidt2006 Eq. 8:

```
v_cr^2 = (alpha * c)^2  +  beta * sigma_p / rho  +  gamma * (t_ox / d) / rho
```

| Symbol | Meaning | Unit | Source |
|---|---|---|---|
| c | sqrt(B/ρ), B = E / (3(1 − 2ν)) | m/s | properties.csv, rule P1 |
| alpha | 0.15, fixed (Z6_a015, HG2018a) | – | not refitted |
| sigma_p | particle strength (input rule below) | Pa | the paper |
| rho | particle density | kg/m³ | rule P1 |
| t_ox | native oxide (or hydroxide) thickness of the powder | m | the paper |
| d | particle diameter | m | the paper |
| beta | plastic-work coefficient, ≥ 0 (Schmidt's 4 F₁ = 4.8 is a relative) | – | **fitted once** |
| gamma | effective oxide work stress, ≥ 0: fracture and expulsion work per unit shell volume, times the shell-volume fraction factor (6 t/d for a sphere) | Pa | **fitted once** |

Mechanism of the terms:
1. **Jetting onset** (α c): the shock-release condition of Z6; it absorbs whatever average oxide and strength
   penalty the Z6 fit metals had.
2. **Plastic work** (β σ/ρ): a stronger particle dissipates more energy in the crater and the jet before fresh
   metal meets; this is the strength mechanism of CS-08.
3. **Oxide work** (γ t/(ρ d)): the oxide shell must be fractured and swept out of the contact (CS-07). Its volume
   fraction scales as t/d, so the term predicts **a size effect through the oxide**: at fixed t, thinner shells
   relative to d cost less, so larger particles bond at lower velocity.

Assumptions kept: H1 (one threshold), H2 (fresh polished substrate), H4 (oxide enters as a thickness only:
hydroxide chemistry and oxide structure are ignored, γ is one constant for all oxides), H5 for c and ρ, H6, H7.
Assumptions broken: Z6's "strength is swamped by impact pressure" and the clean-surface reading of Z6.

## Fitting rule (frozen here, run once)

- **Calibration rows:** B-B10-c1 … c5 (printed v_cr, midpoints), the only seen rows with both strength and oxide
  thickness reported. Inputs from `data/blind_inputs.csv` (static compression strength, oxide FWHM thickness,
  d = 15 µm) and properties.csv (Al 6061, P-H20-Al6061: ρ, E, ν).
- **Fit:** non-negative least squares of y = v_mid² − (α c)² on x₁ = σ_p/ρ and x₂ = (t_ox/d)/ρ, unweighted, no
  intercept.
- **Dead on arrival:** if either fitted coefficient sits at its bound (0), CS-10 does not exist as a combined
  model. That is recorded as a negative result and **no other form is tried on the same data**.
- Reported with the fit, all labelled in-sample or post hoc: the five residuals, leave-one-out residuals, and the
  predicted Δ for B10 (Δ as in the B10 rules).

## Prediction rule for blind papers frozen after the fit

- **Strength σ_p**, in this order: powder static compression strength (as BP1); else powder microhardness by
  Tabor, σ_p = 9.807 · HV / 3 MPa (flagged "Tabor"); else no prediction. Substrate strength is not an input.
- **Oxide t_ox:** the powder's reported native oxide or hydroxide thickness, numeric. Not reported → no
  prediction (nothing is filled).
- **d:** the reported mean or median diameter. ρ, E, ν by rule P1; missing → no prediction.
- **Domain claim:** rule D1 (matched pair, room-temperature substrate, polished, 8 ≤ d ≤ 16 µm) and
  1 ≤ t_ox ≤ 50 nm and 50 ≤ σ_p ≤ 1000 MPa. Outside it the prediction is still made and scored separately as
  out of domain.
- Windows: as printed, else rule B6. Score S1 as in the frozen v1 rules.

## Hunch

```yaml
- id: CS-10
  registered: 2026-11-04
  assumption_broken: Z6 (strength swamped by impact pressure; clean surface); keeps H4 (thickness only)
  statement: >-
    v_cr^2 = (0.15 c)^2 + beta sigma_p / rho + gamma (t_ox / d) / rho with beta, gamma > 0 fitted once on B10.
    Strength and oxide both raise v_cr and can offset each other within one alloy, and the oxide term makes
    v_cr fall with particle size at fixed oxide thickness.
  mechanism: >-
    Energy balance at the contact: the impact energy per unit volume must cover jetting onset (Z6), plastic
    work that grows with particle strength, and the work to fracture and expel an oxide shell whose volume
    fraction scales with t_ox / d.
  predicted_effect:
    - {metric: "K1: Delta v between thickest and thinnest oxide state of one powder", direction: up,
       size: "as computed by CS-10 with the frozen beta, gamma"}
    - {metric: "K2: median S1 over in-domain blind conditions where CS-10 runs", direction: down,
       size: "below Z6_a015's median S1 on the same conditions, and <= 0.05"}
    - {metric: "K3: Delta v between strongest and weakest state of one powder at oxide within +-2 nm",
       direction: up, size: "as computed by CS-10"}
  kill_criterion: >-
    w = median measured window width of the series (rule B6 where not printed). K1 and K3, each on a same-powder
    series of at least three states frozen after the fit: refuted if |Delta_meas - Delta_pred| > w + 0.5
    |Delta_pred|; supported if |Delta_meas - Delta_pred| <= w and |Delta_pred| > w; inconclusive otherwise.
    K2: refuted if median S1(CS-10) >= median S1(Z6_a015); supported if lower and <= 0.05; inconclusive with
    fewer than three conditions. CS-10 is refuted if any of K1, K2, K3 is refuted on unexposed data; it is
    supported only if K2 and at least one of K1, K3 are supported. Dead on arrival as stated in the fitting rule.
  known_relatives:
    - Schmidt2006 Eq. 8 (additive energy terms in v^2; Z2)
    - Assadi2003 (strength term; Z1)
    - HG2018a (Z6, the jetting term)
    - Na2025 Eq. 6 (combined strength + oxide fit on B10; form not read in this session)
    - Lienhard2020, HG2019b, Ren2024 (oxide raises v_cr), CS-07, CS-08
    - Dowding2020 (size effect; attributed there to other mechanisms)
  provenance: Inspired by B10 (outcomes seen) and the authors' conclusion. Calibrated on B10 only.
  label: variant of Schmidt2006 with an oxide term (referee to confirm, against Na2025 Eq. 6 in particular)
  status: open
  author: claude (with Peter)
```

## What CS-10 cannot show

- Calibration uses one alloy, one size and a 16.8–24.7 nm oxide range. Two constants on five points, with
  ±2 % velocity uncertainty and a 77 m/s spread, will be poorly determined; the fit commit reports how poorly.
- γ is one constant for all oxides (H4). A same-metal oxide series tests the t/d term only for that oxide.
- The size prediction is testable only on a size series with reported oxide thickness; DW (Al, Ti) has none.
