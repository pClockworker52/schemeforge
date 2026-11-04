# Cold spray: CS-10 fit on B10 (in-sample, post hoc by construction)

Registration and frozen fitting rule: [coldspray-hunch-cs10.md](coldspray-hunch-cs10.md), commit 3f181ed, made
before this fit. Code: `src/schemeforge/research/coldspray_cs10.py`. Output: `data/cs10_fit.csv`. Not a judge run;
every number below is in-sample on B10, whose outcomes were seen.

## Frozen constants (for all later blind papers)

| Constant | Value | Bound hit? |
|---|---|---|
| α | 0.15 (fixed, Z6_a015) | – |
| β | **0.3774** | no |
| γ | **3.190 × 10¹¹ Pa** | no |

Neither coefficient sits at its bound, so **CS-10 is not dead on arrival** under its own rule. These constants
are frozen. Predictions for the next blind papers use them unchanged.

## Fit quality (in-sample; m/s)

| Condition | Measured | Fit | Leave-one-out | LOO β | LOO γ (Pa) |
|---|---|---|---|---|---|
| c1 | 887 | 863.2 | 846.3 | **0** | 3.68e11 |
| c2 | 820 | 859.8 | 878.7 | 0.990 | 2.36e11 |
| c3 | 880 | 862.1 | 858.2 | 0.429 | 2.96e11 |
| c4 | 875 | 886.2 | 893.6 | 0.214 | 3.65e11 |
| c5 | 897 | 889.7 | 884.1 | 0.499 | 2.85e11 |

| Model | In-sample RMS | Leave-one-out RMS |
|---|---|---|
| CS-10 (2 constants) | 23.0 | 34.9 |
| Constant (mean of the others) | 26.9 | 33.7 |

Predicted Δ (S − W, B10 groups): −17.8 m/s, measured −30.5 m/s.

## What this says (post hoc)

1. **B10 does not determine CS-10.** Out of sample within B10, CS-10 is no better than a constant (34.9 against
   33.7 m/s, both about two times the stated ±2 % velocity uncertainty of ≈ ±17 m/s). Two constants on five points
   with a 77 m/s spread cannot be pinned down. This is the expected weakness the registration named, now
   quantified.
2. **The strength term is fragile.** Leaving out c1 drives β to 0; across the folds β ranges 0–0.99. γ is
   steadier (2.4–3.7 × 10¹¹ Pa). The fit attributes most of the excess over Z6 to the oxide term (c1: oxide
   1.32 × 10⁵ m²/s² against strength 0.49 × 10⁵, on top of (α c)² = 5.64 × 10⁵).
3. **β is far below Schmidt's 4 F₁ = 4.8.** If plastic work mattered at Schmidt's scale, B10's strength drop
   would have lowered v_cr by about 100 m/s (Z2's predicted Δ was +103). The data allow a much weaker strength
   term only.
4. **γ is large.** For a sphere, γ = 6 k σ_ox, where k is the share of shell fracture work that has to be paid
   from kinetic energy. γ = 3.2 × 10¹¹ Pa would need σ_ox k ≈ 53 GPa, more than any oxide's fracture stress. Read
   physically, the t/d term is not shell-fracture work alone. It also carries whatever else grows with heat
   treatment time (oxide structure, Mg enrichment, H4). This is a reason to expect K1 on other oxides to fail.

## Consequences for the blind set

- The frozen β, γ go into the next freeze unchanged. The K1–K3 kill rules in the registration decide; this note
  adds none.
- The clearest test is an oxide series on another metal or powder (B14 Al: exposed, reported separately; B06,
  B05 if they carry thickness values). CS-10 predicts a large oxide effect: with the frozen γ, +1 nm on a 15 µm Al
  6061 particle adds about 4.6 m/s near 860 m/s (≈ 37 m/s from 17 to 25 nm).
