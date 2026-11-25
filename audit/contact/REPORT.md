# Arena 2 blind audit report (judge contact-v0.9.dev, eaf87f1; 2026-11-24)

*Written by the main session from the judge-auditor's final message, verbatim below the line. The auditor's hook
blocked it from writing this file itself. Its code and outputs are in this folder. Prompt:
docs/judge/contact_audit.md. Traced findings: docs/judge/contact_audit.md "Result".*

---

I ran the audit on 1000 random admissible instances. In short:

- **Exact solutions:** the judge's exact solutions agree with my independent ones to ≤3.5e-11.
- **Simple shear:** agrees to round-off.
- **Hertz:** fully reproduced from the judge's x and f.
- **Two real judge bugs:** `fe_leak_pre` is up to 9.2e4× off, and Newton convergence depends on the choice of units.
- **FE accuracy:** a small mesh-rounding effect puts FE about 1e-8 from exact.

**Setup.** Generator seed 20261124 (`numpy.random.default_rng`). 450 gap_closure (250 C0a, 200 C1 with distort 0.01–0.45), 450 simple_shear, 100 hertz inside the case file's held-out ranges. The judge ran in 8 batches of at most 150 cases.
- **Answered:** 926 (386 gap_closure: 213 C0a and 173 C1; 450 simple_shear; 90 hertz).
- **Judge errors:** 74, all `NewtonConvergenceError` (37 C0a, 27 C1, 10 C2).

## Maximum differences
"rel" is |judge − audit|/|audit|; "abs" is used where the reference is zero or noise level.

**gap_closure, judge exact vs audit exact**

| quantity | max diff |
|---|---|
| ideal_force | 1.2e-14 rel |
| exact_force | 3.5e-11 rel |
| exact_thickness | 3.3e-11 rel |
| exact_force_half | 6.1e-14 rel |
| exact_thickness_half | 3.2e-14 rel |
| exact_leak_pre | 5.7e-14 rel |
| exact_gap_res | 3.3e-11 rel |
| exact_force_err | 3.5e-11 abs (2e-4 rel only because the value itself is about 1e-7) |

**gap_closure, judge FE vs audit exact.** The last column is the same comparison after rounding the layer boundaries to 10 decimals (see cause 2).

| quantity | max diff | after rounding |
|---|---|---|
| fe_push | 2.2e-16 abs | |
| fe_force at full push | 1.0e-8 rel | 8.0e-10 |
| fe_force, every step with abs F ≥ 1e-6 | 2.5e-7 rel | 1.5e-7, but every row above 1e-9 has abs error ≤ 2.5e-13 |
| fe_force, every step with abs F &lt; 1e-6 | 2.4e-13 abs | |
| fe_thickness | 1.2e-8 rel | 1.5e-9 |
| fe_wall_pressure vs F/w, worst node | 2.5e-8 rel | 2.1e-8 |
| fe_leak_pre | **9.2e4 rel** | |
| fe_gap_res | 1.2e-8 rel | |
| fe_force_err | 1.3e-8 abs | |
| fe_pressure_spread (exact 0) | 4.2e-8 abs | |
| fe_min_J_medium vs s_m | 9.4e-9 rel | 1.5e-9 |

**gap_closure, classical vs ideal at every load step**
- Before contact: 3.9e-12 (abs, relative to the full-push ideal force).
- In contact: 1.1e-9 rel; the classical force is below ideal in all 1337 steps.

**simple_shear**

| quantity | max diff |
|---|---|
| mu, lmbda | 0 |
| P_xy | 4.1e-16 rel |
| P_yy | 5.6e-17 abs |
| shear_parasitic | 4.3e-16 rel (3.8e-16 against γ) |
| normal_parasitic | 1.6e-16 abs |

**hertz, recomputed from the judge's x and f.** The middle column uses load P = 2Σf; the last uses the judge's own `load`.

| quantity | P = 2Σf | judge's load |
|---|---|---|
| load vs 2Σf | 4.0e-10 rel (6.2e-13 abs) | — |
| p | 2.6e-15 abs, relative to max p | — |
| E_star | 0 | 0 |
| a_hertz, p0_hertz | 2.0e-10 rel | 0 |
| a_err | 4.0e-10 abs | 0 |
| p0_err | 2.0e-10 abs | 2.9e-11 rel |
| p_l2 | 9.8e-9 rel | 3.2e-14 |
| leak_out | 2e-21 abs | 0 |

**Classical vs Hertz (the judge's error floor, not round-off), 90 instances:**
- a_err −1.25 % … +1.33 % (median +0.30 %)
- p0_err −0.57 % … +0.19 % (median −0.32 %)
- p_l2 1.1 % … 9.7 % (median 3.5 %)

The spec's dev figures are a +0.9 %, p0 −0.5 %, p_l2 1.6 %, so on random instances the floor is wider.

## Causes of every disagreement above 1e-10
1. **`fe_leak_pre` (judge bug; the spec doesn't say how F(g/2) is obtained).** It equals, to 1e-14, a linear interpolation of the FE force between the two load steps around g/2, not the force at g/2. g/2 fell between steps in all 386 instances. The dev cases hide this because g/2 is step 2 of 6 there; the held-out GF family will hit it. Fix: add g/2 as a load step.
2. **FE about 1e-8 from exact (minor judge bug).** This affects fe_force, fe_thickness, fe_gap_res, fe_min_J_medium and fe_force_err, and breaks the spec's "FE agrees to 1e-9 or better".
   - The error doesn't change with `steps` (identical 8.24e-9 for 2 to 40 steps) or when E is scaled by 1e-3 or 1e3. So it is not Newton, and float32 inputs were tested and ruled out.
   - Rounding the layer boundaries to 10 decimals brings it down to Newton level (≤8e-10 force, ≤1.5e-9 thickness). 10 decimals is the best fit in 124 of 131 cases.
   - The judge's mesh probably snaps coordinates to a 1e-10 grid, perhaps when the body and medium meshes are merged.
3. **Wall pressure and pressure spread up to 4e-8 (same rounding).** The judge's per-node pattern is reproduced to about 1e-9 by: reactions on rounded x coordinates, recovered with a mass matrix built on unrounded ones. This stays inside the self-check's 1e-7.
4. **What's left after rounding (Newton tolerance, as the spec states).** Full push ≤8e-10 relative; per-step rows above 1e-9 all have absolute force error ≤2.5e-13, at forces of 1–3e-6.
5. **Classical force up to 1.1e-9 (spec's "2e-10" claim is too optimistic).** It is always below ideal and does not change with E or steps, but depends on geometry. This is the leftover term of the Richardson extrapolation over k = 1e2, 1e3, 1e4 (of order 1e-9). One step (C1-0445, 1.10e-9) would just fail the self-check's 1e-9.
6. **Judge exact solution ≤3.5e-11 (informational, below 1e-10).** Its s_m carries an absolute error ≤6.6e-16, from cancellation when s_m is tiny. In some cases the judge's FE is closer to the truth than its own exact value.
7. **Newton convergence depends on units (judge robustness bug, matters for Gate 6).**
   - The problems are exactly invariant when E is scaled, yet the failure rate climbs with E: 3/125 below E = 0.1 versus 24/102 for E 10–100.
   - 10 of 12 failing gap cases converge with E × 1e-3.
   - All 10 Hertz failures (all with E ≥ 2.1) converge with E/10. C2-0054 gives identical metrics at E = 0.147 and 1.47 and fails at 4.42 and 14.7.
   - 5 of 25 gap cases inside GF-like ranges failed, and the case file's claim that every Hertz instance in its ranges converges does not hold.
   - The likely cause is the absolute 1e-10 Newton tolerance; a tolerance relative to the modulus or reaction size would fix it.
   - `judge exact` also returns an error for these cases instead of a result with converged = 0.
8. **Hertz `load` is not exactly 2Σf of the reported f (≤6.2e-13 abs; Newton equilibrium residual).** This flows into a_hertz, p0_hertz, a_err, p0_err and p_l2. With the judge's own load, every metric matches to ≤2.9e-11 or exactly.

## Where the spec is ambiguous or silent
- **p_l2:** the spec names no integration rule. The judge uses the trapezoidal rule on the nodes with x &lt; 1.5·a_hertz. A plain nodal sum or the exact integral of the quadratic interpolant gives noticeably different values (medians 2.2 % and 4.1 % vs 3.5 %).
- **Which a and P:** the windows use a_hertz; a_err uses the judge's `load`, whose source isn't stated.
- **leak_out:** the judge uses Σ|f|, not |Σf|.
- **p0_err:** max p and p(0) can't be told apart here (the peak is at x = 0 in every case).
- **F(g/2):** not defined when g/2 isn't a load step (cause 1).
- **Mesh:** coordinate rounding and the edge mass-matrix coordinates are not described (causes 2–3).
- **Newton tolerance:** its norm and units are not given (cause 7).
- **Accuracy claims:** "1e-9" and "2e-10" were measured only on dev cases.

## Files
- `model.py` — audit implementation
- `gen_cases.py` — instance generator
- `run_judge.sh` — runs the judge on the batches
- `compare.py` — the comparison
- `cases/`, `judge/` — the case batches and the judge's answers
- `probe/` — black-box tests for E scaling, step count and failures
- `results.json`, `compare_output.txt` — full comparison output
