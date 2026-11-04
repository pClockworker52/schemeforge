# Cold spray: blind test B10 (Na et al. 2025, Al 6061 heat-treatment series), results

Order of record:
- frozen predictions and rules: commit 060fff8 (2026-11-03 21:44 UTC);
- outcomes extracted by a separate session: 94fd173 (2026-11-04), a descendant of the freeze;
- scoring script committed before reading the outcomes: f770a8b;
- adaptation for missing window bounds: this commit.

The first literature-blind result of the track. Not a judge run.

## Measured (Na2025, Sec. 4; printed v_cr, the midpoint of an equal-count window)

| Condition | Treatment | Static strength (MPa) | Oxide (nm) | Measured v_cr (m/s) |
|---|---|---|---|---|
| c1 | as received | 351 | 16.8 | 887 |
| c2 | 230 °C, 75 min | 298 | 17.0 | 820 |
| c3 | 530 °C, 75 min | 219 | 18.9 | 880 |
| c4 | 530 °C, 240 min | 233 | 24.0 | 875 |
| c5 | 530 °C + aged | 238 | 24.7 | 897 |

**The window bounds are not printed**, and the extractor could not digitize them (bonded points overlap at
CoR = 0). Velocity uncertainty is stated as ±2 %. So the per-condition score S1 and the typical window width w
used by the frozen verdict rules are **unavailable**.

## Verdicts (frozen rules; branches that need w are undetermined, none is filled in after the fact)

Δ = mean v_cr(S = c1, c2) − mean v_cr(W = c3, c4, c5) = 853.5 − 884.0 = **−30.5 m/s**.
Spread of the five values: 77 m/s.

| Hunch | Frozen rule | Verdict |
|---|---|---|
| CS-08: particle strength raises v_cr within one alloy | refuted if Δ ≤ 0 | **Refuted.** The stronger, thin-oxide group is not above the weaker, thick-oxide group |
| CS-07 on B10: oxide raises v_cr within one metal | refuted if Δ ≥ 0; supported if Δ < −w | **Not refuted;** support undetermined (w unavailable). The direction agrees |
| CS-09: sound speed alone; all five consistent with one v_cr | needs w | **Undetermined** |

Context, explicitly post hoc and not verdicts: with the stated ±2 % velocity uncertainty (≈ ±17 m/s per value),
Δ is about one combined uncertainty. Hassani2020's Al 6061 window was 50 m/s wide; if w were 50 m/s, CS-07 and
CS-09 would both be inconclusive.

## Predictions against the printed v_cr (post hoc metric: relative error, because S1 is unavailable)

| Model | c1 | c2 | c3 | c4 | c5 | Predicted Δ |
|---|---|---|---|---|---|---|
| Z6_a015 (0.15 sqrt(B/ρ)) | −15 % | −8 % | −15 % | −14 % | −16 % | 0 |
| Z6_a015_C0 (0.15 C₀) | −10 % | −2 % | −9 % | −8 % | −11 % | 0 |
| baseline_LOMO | −31 % | −25 % | −31 % | −30 % | −32 % | 0 |
| Z1_Assadi_static (out of domain) | −20 % | −14 % | −21 % | −20 % | −22 % | +8 |
| Z2_Schmidt_static (out of domain) | +1 % | +2 % | −15 % | −13 % | −14 % | **+103** (measured −30.5) |

## What this says

1. **Strength alone does not order this series.** Strength-dependent laws fed with the static strength (Z2
   strongly, Z1 weakly) predict the as-received powder highest by a wide margin. The measured values do not
   show that.
2. **The sound-speed law under-predicts this Al 6061 powder by 8–16 %** (the C₀ variant by 2–11 %), the same
   direction as the Al alloys in the retrospective test (CS-02). A sound-speed-only law misses something that
   matters for age-hardenable Al, and it is not simply strength (point 1).
3. **The authors reach a compatible conclusion by another route.** Their own analysis, read only now, says strength
   loss and oxide growth from the heat treatments offset each other. Neither alone explains the trend, and a
   combined strength-plus-oxide model, with one constant fitted on the as-received powder, fits best. That
   model is a relative of CS-07 + CS-08 combined; it was not in our frozen zoo.
4. **c2 (230 °C degassing) is the odd one,** lowest at 820 m/s with thin oxide and intermediate strength. The
   paper calls it "marginally lower". One value cannot carry a mechanism.

## Protocol lesson

The B10 pre-registration did not say what to do when a paper prints only v_cr without bounds. The verdicts
above therefore stop where w is needed. **Proposed rule B6** (for Peter's approval; would apply only to papers
whose predictions are frozen after the rule is adopted): if window bounds are not printed and cannot be
digitized, the window is v_cr ± the paper's stated velocity uncertainty. If no uncertainty is stated, only
sign- and rank-based verdicts are scored.
