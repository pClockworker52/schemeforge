# Cold spray: blind test B02 and B14, results

Order of record:
- frozen predictions and rules: 27e7eea;
- CS-16 addendum: 542f810;
- scoring script: f8fb8f5;
- task wording fix: b8ed1eb;
- outcomes (WSL B, step 3): add80b8, a descendant of all four, committed after them;
- scores: this commit (`python -m schemeforge.research.coldspray_blind2_score`, `data/scores_b02_b14.csv`).

Not a judge run. Rule B3: **Al and Cu are in-sample materials for Z6** (its fit used Al, Cu, Ni, Zn), so Z6's
values below test new conditions of known materials, not new materials. B14 is exposed throughout; B02 partly.

## Measured (as extracted; thesis sources)

| Condition | What | v_cr (m/s) | Window |
|---|---|---|---|
| B14-c1 | As-Recd, ~5–6 nm amorphous | 846 | 824–868 |
| B14-c2 | HT-Base (argon) | 814 | 801–827 |
| B14-c3 | HT-30 (30 min dry air) | 843.5 | 839–848 |
| B14-c4 | HT-60 | 815 | 787–843 |
| B14-c5 | HT-240 | 859 | 837–881 |
| B14-c6 | RH-50, ~5–6 nm, onset of hydration | 828.5 | 815–842 |
| B14-c7 | RH-95, ~8 nm, crystalline (oxy)hydroxide | 970.5 | 940–1001 |
| B14-c8 | RH-95-D, dried, < 1 nm thinner than c7, amorphous, OH gone | 902 | 864–940 |
| B02-c1 | Cu on soft Cu (63 HV) | 641 | bounds not printed; ±2 % (B6) |
| B02-c2 | Cu on hard Cu (105 HV) | 566 | bounds not printed; ±2 % (B6) |

w_B14 = 44.0 m/s, w_B02 = 24.1 m/s (from B6).

## Verdicts (frozen rules)

| Test | Frozen rule | Measured | Verdict |
|---|---|---|---|
| **CS-16** (harder substrate raises v_cr; Δ_pred = +102.2) | refuted if Δ ≤ 0 | Δ = v(hard) − v(soft) = **−75.0** | **Refuted** |
| CS-07 on B14 (oxide raises v_cr; Δ_H = v(c7) − mean v(D)) | refuted if Δ_H ≤ 0, supported if Δ_H > w | Δ_H = +129.6 (w = 44.0) | **Supported (exposed)**; oxide type and thickness changed together |

## Reported without a verdict

- **Dry series** (c1, c3, c4, c5): spread 44.0 m/s = 1.0 w. Different thermal histories, same stated oxide: one
  v_cr within a window, as Z6, the baseline and CS-12(c) expect.
- **RH-95-D against RH-95: v(c8) − v(c7) = −68.5 m/s (1.6 w)**, at nearly the same thickness (< 1 nm apart). Removing
  the hydroxide and the crystallinity lowered v_cr by more than a window. Thickness-only models (the forms of CS-10
  and Z18) expect a few m/s; CS-12 allows a type effect but predicted no direction (its T4). This is **evidence that
  oxide chemistry or structure matters beyond thickness** (post hoc, exposed paper, no verdict).
- **S1 and relative errors** (`data/scores_b02_b14.csv`):

| Model | B14 dry and RH-50 (c1–c6) | B14-c7 / c8 | B02-c1 / c2 (out of domain) |
|---|---|---|---|
| Z6_a015 | −1 to −6 %; S1 0–0.04 | −17 % / −11 % | −10 % / +2 % |
| Z6_a015_C0 | −1 to −6 % | −17 % / −11 % | −9 % / +4 % |
| DW_size | +11 to +17 % | −2 % (inside the window) / +5 % | — |
| baseline_LOMO | −25 to −29 % | −37 % / −32 % | +9 % / +23 % |
| CS-16 | — | — | −25 % / +3 % |

## What this says

1. **CS-16 is refuted, cleanly and in direction.** The cold-rolled, harder Cu substrate bonds the same Cu powder at a
   **lower** velocity (566 against 641 m/s, −12 %). The prediction came from two Panova rows where the harder
   surface was a cold-sprayed coating. Hardness was the wrong variable to carry over: the substrate's state matters,
   but not through its hardness. The authors' own analysis (recorded by WSL B, read only now) attributes it to the
   cold-worked plate's low strain-hardening capacity: at equal velocity the particle jets around almost the whole rim
   on the hard plate and bonds earlier. Hassani's impact-ratio scaling predicts the opposite as well.
2. **This matters for the interface view.** On B02, bonding followed the amount of **jetting and rim stretch**, not
   the hardness. That is the kind of interface state CS-12's blanket uses, read here post hoc, not a test.
3. **Oxide chemistry, not only thickness.** B14's RH-95-D result is the clearest sign so far that a thickness-only
   oxide term (CS-10, Z18) is incomplete. It is the T4 side of CS-12 (oxide type), which CS-12 did not quantify.
4. **Z6 holds for pure Al** within about 1–6 % on six of eight B14 conditions (an in-sample material), and misses
   the hydroxide batch by 17 %.

## Consequences (proposals for Peter, nothing decided here)

- The decisive thickness test T3 is still open. B14 gives a type change, not a thickness series. The campaign
  trigger waits for B06 and B05.
- A substrate-side hunch with strain-hardening capacity instead of hardness would be a new registration. It would be
  inspired by B02, so it could not be tested on B02.
- Lucas's Table 2 (Y_d, C₀, B, failure strain ε_c per material) makes the spall-type law Z7 runnable for Cu, post hoc.

## Addendum (2026-11-07): Z7 spall law on B02, post hoc

**Post hoc.** Z7 was not frozen for B02; its inputs (Lucas ch. 4 Table 2) were withheld in step 1. Script:
`scripts/z7_cu_posthoc.py`. Z7 is v_cr = (2/k) (2 Y_d ε_c / B)^(1/2) C₀. Its constant k is unknown, so only the
ratio v_cr(soft) / v_cr(hard) is testable. C₀ and B are equal for the two plates and cancel.

| Variant | Ratio soft / hard | Against measured 1.133 ± 0.032 |
|---|---|---|
| Substrate properties only (Lucas's own evaluation): soft Y_d 351 MPa, ε_c 0.29; hard 562 MPa, 0.16 | 1.064 (hard would be 602 m/s, given soft = 641) | Right direction; contrast about half the measured one, 0.069 short (about 2 × the combined error) |
| Arithmetic-mean mixing of particle and substrate (Panova2026b form); particle Y_d 383 ± 65 MPa, particle ε_c not reported | 1.187 at ε_p = 0; 1.079 at 0.10; 1.001 at 0.29 | Matches only for ε_p = 0.04 (0.01–0.09 over the Y_p and v_cr errors). Soft above hard only if ε_p < 0.25–0.33 |

What this says:
- **Unlike hardness (CS-16, refuted on B02), Z7 gets the sign right**, because its failure-strain term
  (ε_c ≈ n, Considère) falls faster from soft to hard than its strength term rises.
- **The size is short.** Substrate-only Z7 explains about half the contrast. The mixing rule reaches the measured
  ratio only with a particle failure strain (0.01–0.09) below the full-hard plate's 0.16. Meanwhile the powder's
  Y_d (383 MPa) lies between the two plates. No measurement of ε_p exists, so this is a requirement, not a
  contradiction.
- **Bearing on CS-17** (frozen; strain-hardening capacity, directional): the ε_c term of Z7 carries CS-17's
  direction. B02 cannot test CS-17 (it inspired it); this addendum adds no evidence for or against it. CS-17's label
  "variant of Lucas 2025" stands.
- **No new hunch.** The particle failure strain is the missing input; measuring it (or the powder's n) would turn
  the mixing rule into a test.
