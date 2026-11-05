# Cold spray: zoo member Z18 (Na2025 Eq. 6, Lienhard jet model), registration

Registered 2026-11-05 on Peter's decision ("register Eq. 6 as a zoo member"). This commit fixes the form, the input
rules and the fitting rule **before** the fit is run. The fit and its code come in a later commit (git order is the
proof). Source: [coldspray-reading-na2025.md](coldspray-reading-na2025.md). Not a judge. Like every zoo member, it is
scored on every blind paper frozen after this registration.

## Form (Na2025 Eq. 6, as printed)

V_cr = (2/k) · (C₀/B) · [σ₀ · t₀/t + σ_m · (t − t₀)/t]

| Symbol | Meaning | Value or source |
|---|---|---|
| C₀ | sound speed | Hugoniot C₀ of Table S1 (rule P1); Al 6061: 5350 m/s (Na print 5300) |
| B | bulk modulus | B = E / (3 (1 − 2ν)) from Table S1 (rule P1); Al 6061: 67.6 GPa (Na print 67.55) |
| σ₀ | oxide strength | **870 MPa**, fixed (Na2025, from Lienhard 2020 and Sun 2020; aluminium oxide) |
| t | jet thickness | **100 nm**, fixed (Na2025, from Lienhard 2020) |
| t₀ | oxide thickness of the powder | the paper's numeric value; not reported → no prediction |
| σ_m | metal strength in the jet | variant-specific, below |
| k | constant | variant-specific, below |

## Two variants

| Variant | σ_m | k | Note |
|---|---|---|---|
| **Z18_Yd** (as published) | the dynamic yield strength Y_d printed by the paper, **only if** fitted to rebounds below v_cr and passed by the extractor as a number, without any v_cr | **0.062** as published (fitted by Na on the as-received B10 powder) | Partly circular, like rule P2 in v1: Y_d comes from impacts of the same campaign. Reported separately. |
| **Z18_static** | the powder's static compression strength (rule BP1); else Tabor σ = 9.807 · HV / 3 MPa from powder microhardness, flagged | **fitted once on B10** (rule below) | Uses only inputs that blind papers provide before the freeze. |

## Fitting rule for Z18_static (frozen here, run once)

- **Calibration rows:** B-B10-c1 … c5 (printed v_cr). σ_m = static compression strength, t₀ = oxide FWHM thickness
  (blind_inputs.csv). C₀, B by rule P1 (Al 6061).
- **Fit:** one parameter, least squares on V_cr (unweighted), over all five rows. Closed form: 1/k = Σ(V·x)/Σ(x²),
  with x = (2 C₀/B) · σ_eff.
- **Reported, all in-sample:** k, the five residuals, leave-one-out residuals, the predicted B10 contrast Δ (S − W
  groups, as in the B10 rules).
- **Z18_Yd** is not refitted. Its B10 values are in-sample by construction (k was fitted on B10-c1) and are reported
  as a check that the implementation reproduces the paper (as received: 887 m/s measured).

## Domain claim (both variants)

- Rule D1: matched pair, room-temperature substrate, polished, 8 ≤ d ≤ 16 µm.
- **Al and Al alloys only,** because σ₀ = 870 MPa is sourced for aluminium oxide only. For other metals there is no
  prediction; nothing is filled.
- 1 ≤ t₀ ≤ 50 nm, and t₀ < t.

Outside the domain, the prediction is still made and scored as out of domain.

## Notes

- **Z18 has no particle-size term:** the oxide enters through the jet thickness, not d. This is the opposite of
  CS-10. A size series of an Al alloy with reported oxide thickness would separate them.
- **For CS-12's test T3** (Al 6061, 17 → 25 nm, same strength), Z18 predicts about +126 m/s, CS-10 about +37 m/s,
  CS-12 no change (coldspray-reading-na2025.md). Z18_static's value follows from its fitted k and is reported with
  the fit.
- **Label:** Na2025 / Lienhard2020 as published; Z18_static is a variant (a different strength input and a refitted
  k).
