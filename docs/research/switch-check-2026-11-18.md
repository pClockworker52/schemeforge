# Switch-radius check, 2026-11-18 (calibration; spec and prediction fixed before any number is computed)

**Why.** Peter, chat 2026-11-18: one run could set up the next one. The idea is a contact map in which run 1 (no
bond) gives each surface point its contact history from the converged a(t). Run 2 bonds only where the edge was
subsonic when it passed, which leaves out the centre. This is the in-solver form of CS-20's switch radius, from a
fitted a(t) instead of rigid geometry; the brainstorm correction lists "a derivative of a fitted a(t)" as what
remains. It is a possible trigger for CS-22 part 2. Raw v_edge = da/dt does not converge (driver-check-2026-11-17
§6.1: 0 of 7 and 0 of 6). This check asks whether the switch radius taken from a *fitted* a(t) converges. It needs no
hunch and no engine time. If it fails, the contact-map idea is dropped before it uses a budget slot.

## 1. Quantity

For each speed V and mesh m:

1. **Time from first contact:** t′ = t − t₀, with t₀ = 0.001 R / V (the §8.3 deck's initial gap of 0.001 R; fixed by
   geometry, not fitted). That gives t₀ = 0.0167 ns at 600 m/s and 0.0200 ns at 500 m/s.
2. **Fit:** a(t′) = A t′^p by unweighted least squares on ln a vs ln t′, over the judged outputs (§2). A in µm·ns^−p.
3. **Fitted edge speed:** v(t′) = p A t′^(p−1). The switch is where v = C₀ = 5305.5 m/s (5.3055 µm/ns; P-HG-Al, §8.3):
   - t_c = (p A / C₀)^(1/(1−p)), defined for p < 1;
   - **a_c = A t_c^p**, the switch radius.
4. **Rigid reference, reported only:** a_c,rigid = R V / √(V² + C₀²). That is 1.124 µm at 600 m/s and 0.938 µm at
   500 m/s, with R = 10 µm.

a_c is an **extrapolation**. With the rigid estimate, t_c (about 0.10 ns at 600 m/s, about 0.09 ns at 500 m/s) lies
before the third output. The fit form is fixed here and is not changed after computing.

## 2. Data

`docs/research/opencourant/results/tl_cal6_p3_series.csv` (§25 quad runs; Al–Al 600 and 500 m/s; R/64, R/128,
R/256; fork binary `d0500106d`). Columns `V`, `frame`, `t_ns`, `a_R64_um`, `a_R128_um`, `a_R256_um`. Judged outputs:
the third onwards up to t*, as in driver-check §2 (frames 3–9 at 600 m/s, 3–8 at 500 m/s). No other column is used.

## 3. Rule

The §25 rule on a_c, per speed:

|a_c,256 − a_c,128| ≤ 3.5 % |a_c,256| and ( |a_c,256 − a_c,128| ≤ 0.8 |a_c,128 − a_c,64| or |a_c,128 − a_c,64| ≤ 3.5 % |a_c,128| ).

**Pass** if a_c converges at both speeds. **Fail** otherwise, and also if p ≥ 1 for any mesh (no switch defined).

**Reported only (not judged):**
- p, A and t_c per mesh;
- t_c relative to the time of output 3;
- a_c / a_c,rigid;
- the same quantities from a fit over outputs 3–6 only, as a sensitivity check of the fit window;
- whether the ratio a_c(600) / a_c(500) agrees with CS-20's predicted ratio. This is post hoc and not a CS-20 test,
  since these are simulations, not measurements.

**Outcome rule:**
- **Pass:** the contact map may be drafted as a candidate trigger for CS-22 part 2, but only if CS-22 part 1 passes.
  It needs a host that resolves a_c ≈ 1 µm with several particles. TLSPH spacing is 1.25 / 0.63 / 0.31 µm at
  R/8 / R/16 / R/32, so R/8 does not resolve it. Peter decides.
- **Fail:** the contact-map idea is dropped and recorded in multi-particle-tried.md.

## 4. Who computes what

Cloud, after this spec is committed: script `scripts/switch_check.py`, which reads only the file and columns of §2.
Results go in §6 of this file.

## 5. Prediction (modeller, judgment, before computing)

Already seen: a(t) converges at every judged output (driver-check §6.1), and the mesh differences are 0.2–3.5 % of
the R/256 value. Raw da/dt does not converge.

- **Pass: 0.35.** For: a fit over 6–7 points smooths the noise that killed raw da/dt, and a converges pointwise.
  Against: the extrapolation amplifies errors. Near p ≈ 0.5, a_c depends on A roughly squared and is sensitive to p.
  A shift of 0.01 in p moves a_c by a few per cent, and the mesh-to-mesh differences in p could well be 0.01 or more.
  Close to the 3.5 % line is likely.
- **p within 0.45–0.60 on every mesh: 0.6.** The rigid small-angle value is 0.5.
- **a_c / a_c,rigid within 0.7–1.3: 0.6.**
- **The sensitivity fit (outputs 3–6) changes a_c by more than 10 %: 0.4.**

## 6. Results

Cloud, 2026-11-18. `python scripts/switch_check.py`; inputs are the §2 columns of `tl_cal6_p3_series.csv` only.
a_c,rigid comes out at 1.1237 / 0.9383 µm, matching §1. The largest fit residual over the judged frames is 2.3 %.

| V | mesh | A (µm ns^−p) | p | t_c (ns) | t_c / t(frame 3) | a_c (µm) | a_c / a_c,rigid | a_c, frames 3–6 |
|---|---|---|---|---|---|---|---|---|
| 600 | R/64 | 3.687 | 0.445 | 0.121 | 0.48 | 1.440 | 1.281 | −0.2 % |
| 600 | R/128 | 3.839 | 0.526 | 0.130 | 0.52 | 1.315 | 1.170 | −0.8 % |
| 600 | R/256 | 3.942 | 0.562 | 0.136 | 0.54 | 1.285 | 1.143 | −0.6 % |
| 500 | R/64 | 3.533 | 0.483 | 0.112 | 0.37 | 1.225 | 1.305 | +1.9 % |
| 500 | R/128 | 3.597 | 0.547 | 0.112 | 0.37 | 1.086 | 1.158 | +0.6 % |
| 500 | R/256 | 3.625 | 0.564 | 0.112 | 0.37 | 1.056 | 1.125 | +0.3 % |

**Rule on a_c (§3):**
- 600 m/s: |256 − 128| / 256 = 2.35 %, |128 − 64| / 128 = 9.48 %, so it converges.
- 500 m/s: 2.88 % and 12.73 %, so it converges.

**Verdict line: PASS.** a_c converges at both speeds.

**Limits (stated with the verdict):**
- **Thin margins:** 2.35 % and 2.88 % against the 3.5 % line.
- **p by itself would not pass at 600 m/s.** It drifts from 0.445 to 0.526 to 0.562, which is 6.5 % between R/128
  and R/256; at 500 m/s it is 3.0 %. a_c converges partly because the drifts in A and p offset each other
  (a_c ≈ p A² / C₀ near p = 0.5).
- **a_c is an extrapolation.** t_c is 0.37–0.54 of the time of the first judged output, so the switch itself was
  never observed.
- **Host:** 2D axisymmetric quads (the reference host), not TLSPH.
- **Reported, post hoc:** a_c(600) / a_c(500) at R/256 is 1.217, against CS-20's sin β_c ratio of 1.198 (+1.6 %).
  These are simulations, not measurements, so this is not a CS-20 test. The implied CS-20 k at the switch is
  1.13–1.14 at both speeds.

**Outcome rule applied:** the contact map may be drafted as a candidate trigger for CS-22 part 2, but only if CS-22
part 1 passes, and only on a host that resolves a_c ≈ 1.1–1.3 µm with several particles. TLSPH gives about 4
spacings at R/32 and fewer than one at R/8. Peter decides. Nothing is registered now.

**Against the prediction (§5):**
- Pass 0.35: it passed, the less likely side.
- "Close to the 3.5 % line is likely": right (2.35 % and 2.88 %).
- p within 0.45–0.60 on every mesh (0.6): miss. R/64 at 600 m/s has p = 0.445.
- a_c / a_c,rigid within 0.7–1.3 (0.6): miss, narrowly. R/64 at 500 m/s is 1.305; all other meshes are within.
- The frames 3–6 fit changes a_c by more than 10 % (0.4): no. The largest change is 1.9 %.
