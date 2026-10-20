# Arena 1 (euler1d) blind judge audit

Audit per docs/PLAN.md §9.10 and docs/judge/euler1d_audit.md. Performed by the judge-auditor subagent on
2026-10-20. The audit implementation was written from docs/judge/euler1d_spec.md §1–4 and textbook formulas only;
`src/schemeforge/arenas/` and `~/.schemeforge/` were never accessed. Judge answers were obtained exclusively via
`uv run sforge judge exact --arena euler1d --case <file> --json`.

(The subagent was not permitted to write this file; it was written by the main session from the subagent's final
report, with the user's approval.)

## Summary

- 1002 random admissible cases (600 Riemann, 402 nozzle): judge and audit agree everywhere; the largest
  relative difference is 6.5e-13. No disagreement above 1e-10.
- 22 targeted edge cases: one **judge bug** (crash for p_b a few ulp above p_crit2), one audit bug (fixed),
  one 1-ulp rounding difference.

## Instance generator

- Seed: **20261020** (`numpy.random.default_rng`), script `gen_cases.py`.
- **Riemann (600):** gamma in {1.4, 5/3, 1.405, 1.2}; rho log-uniform in 10^-1..10^1; p log-uniform in
  10^-3..10^3; |u| <= a; vacuum check; x0 in [0.3, 0.7]; n = 50; t_end = 0.3–0.95 × the time the fastest wave
  needs to reach a boundary.
  Wave patterns: rarefaction–rarefaction 34, rarefaction–shock 240, shock–rarefaction 210, shock–shock 116.
- **Nozzle (402):** 44–45 cases for each of the 9 geometry (anderson, parabolic, conical) × regime (subsonic,
  shock, supersonic exit) pairs; n = 40; area ratio 2–10, length 2–4, inlet ratio 1.5–3. Half of the parabolic and
  conical cases use x_in in [-0.5, 0.5]. p_b is kept at least 1–2 % of the regime interval away from the critical
  pressures.

## Method

`exact.py`, from spec §1–4 plus Toro ch. 4 and Anderson ch. 7, float64:

- **Riemann:** p* by Newton with bisection fallback, iterated until the value stops changing; then u*, the star
  densities, wave speeds and fan sampling per spec §2.7.
- **Nozzle:** Mach from area ratio by bisection on log(A/A*) followed by a Newton polish; p_crit1–3 per spec §3.
  In the shock regime, M1 is found by bisection on p_exit(M1) − p_b and x_s from the closed-form inverse of A(x).
  Profiles are built region by region, with M = 1 exactly at x = x_t.

**Comparison** (`compare.py`): relative difference |a − b| / max(|a|, |b|, floor). The floor is 0, except for
Riemann velocities (u*, wave speeds, sampled u), where it is max(|u_K| + a_K) of the case, so that u* ≈ 0 does not
inflate the figure. The unfloored value is listed as well.

**Sanity check:** `exact.py` reproduces the PLAN Appendix H reference values (Toro tests 1–5 star states; Anderson
p_crit1–3, x_s = 2.09933, M1 = 2.07001, p02/p01 = 0.68817).

## Maximum relative differences (1002 random cases)

| Quantity | max rel | unfloored |
|---|---|---|
| p_star | 8.5e-16 | |
| u_star | 4.7e-16 | 6.3e-14 |
| rho_star_L / rho_star_R | 7.4e-16 / 7.7e-16 | |
| wave kinds | identical | |
| wave speeds | 6.4e-16 | 1.0e-13 |
| sampled rho / u / p | 1.8e-15 / 1.0e-15 / 2.5e-15 | u: 1.9e-13 |
| regime | identical, 402/402 | |
| x_shock | 2.8e-15 | |
| M1 | 4.3e-15 | |
| p0_ratio | 2.5e-15 | |
| A_star_1 / A_star_2 | 0 / 2.5e-15 | |
| mass_flow | 7.6e-16 | |
| p_crit1 / p_crit2 / p_crit3 | 8.2e-16 / 2.3e-15 / 2.7e-15 | |
| profile M / rho / u / p | 6.0e-13 / 5.5e-13 / 5.5e-13 / 6.5e-13 | |

The largest difference (about 6e-13, case A-N0058) is in a cell 8.4e-4 from the throat (M = 0.99935), where
Mach-from-area is ill-conditioned. A 50-digit mpmath reference gives an audit error of 4.7e-13 and a judge error of
1.3e-13, so the difference comes from the audit's rounding.

## Disagreements above 1e-10 (22 targeted edge cases, `edge_cases.py`, `probe_crit.py`)

1. **Judge bug: crash just above p_crit2.**
   - For p_b in (p_crit2, p_crit2 + a few ulp], `sforge judge exact` exits with code 2 and
     `sforge: f(a) and f(b) must have different signs`, instead of returning a shock at x_s ≈ x_exit.
   - A batch containing such a case aborts and returns no output for any case in it.
   - Observed band: 1–4 ulp on anderson (gamma 1.4), 1–4 ulp on parabolic (R 4, L 3, gamma 1.2), 1–8 ulp on
     conical (R 6, L 2.5, gamma 5/3). From +5 ulp (anderson) and +9 ulp (conical) the judge works and matches the
     audit; on parabolic, +16 ulp was the next value probed.
   - Probable cause (inferred from behaviour only): the root finder evaluates p_exit − p_b at the x_exit end of
     its bracket, and rounding gives it the same sign as the interior.
   - Random families essentially cannot hit this (the band is about 1e-15 wide), but a submitted case could.
   - Suggested fix: return x_s = x_exit when p_exit(x_exit) >= p_b, or classify the regime with a tolerance.
2. **Audit bug, fixed: p_b exactly equal to p_crit1.**
   - The judge returns x_s = x_t and M1 = 1 exactly. The first audit version returned M1 − 1 ≈ 5e-6, giving
     differences of about 2–6e-6 in x_shock and M1 (cases E-B01, E-B11, E-B21).
   - Cause: near p_crit1, p_exit − p_b behaves like (M1 − 1)^3, so a root finder only resolves M1 to about
     eps^(1/3) ≈ 6e-6. The audit now treats p_b == p_crit1 as M1 = 1.
   - One or two ulp below p_crit1 the two codes still differ by up to about 1e-5 in x_s and M1. Neither is more
     correct; this is ill-conditioning of the problem, not a bug.
3. **Rounding:** p_crit2 differs by 1 ulp on the conical gamma 5/3 probe. Its only effect is to feed into item 1.

Edge cases that agree:

- a stationary contact exactly on a cell centre (both give the correct star state);
- identical left and right states;
- a rarefaction head on a cell centre;
- the throat exactly on a cell centre (M = 1, all three regimes);
- p_b = 0.9999999;
- p_b exactly equal to p_crit2 or p_crit3 (both give supersonic exit).

## Spec ambiguities

- **Spec §3, p_b = p_crit1:** the spec puts this pressure in the shock regime but states x_s ∈ (x_t, x_exit), an
  open interval. The judge returns x_s = x_t; the spec should say so.
- **Spec §3, p_b within rounding of p_crit2:** behaviour is unspecified, and the judge crashes there (item 1).
- **Spec §2.7, "wave boundary takes the inner side":** this only matters for shocks; at rarefaction heads and tails
  the two sides coincide.
- **docs/judge/euler1d_cases.md:**
  - The default x_in is not stated (observed: 0).
  - The YAML comment lists only anderson and parabolic geometries, though conical is accepted.
  - `id` is described as optional, but `sforge judge exact` requires it
    (`NozzleCase.__init__() missing 1 required positional argument: 'id'`).

## Files

All in `audit/euler1d/`:

- `exact.py`: independent exact solvers
- `gen_cases.py`: random instance generator
- `compare.py`: comparison, output in `compare_out.txt`
- `edge_cases.py`: targeted edge cases, output in `edge_out.txt`
- `probe_crit.py`: ulp probing around p_crit2
- `cases/` (riemann_00–02.yaml, nozzle_00–02.yaml) and `judge_out/` (matching judge JSON)
- `cases_edge/` (edge.yaml, single/, probe/) and `judge_out_edge/edge.json`

## Reproduce

```
uv run python audit/euler1d/gen_cases.py 20261020
# for each cases/<name>.yaml:
uv run sforge judge exact --arena euler1d --case audit/euler1d/cases/<name>.yaml --json > audit/euler1d/judge_out/<name>.json
uv run python audit/euler1d/compare.py
```
