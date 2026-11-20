# Softening check: is thermal softening active in the §25 window? (spec and prediction, fixed before computing)

Written 2026-11-20 (cloud, modeller) at Peter's request, by applying "name the first unjustified step" to a proposed
test. `kind = check`; no hunch, no budget.

## Why

The proposed cheap test of "the edge fails to converge because the material has no length scale" (§25 reading 2) was:
rerun the §25 2D quad deck with thermal softening off and see whether Y − 1 converges. Its first unjustified step is
that thermal softening acts at all within the window §25 can judge:
- R/256 stops at about 0.8 ns (t/t_p ≤ 0.034, a ≤ 3.3 µm), as the surface starts to fold; whether a jet formed was
  not evaluated (§25).
- Y − 1 already fails the rule at the first output (t/t_p ≈ 0.004, about 0.1 ns), when little plastic work can have
  turned into heat.
- If softening is negligible in the window, switching it off changes nothing, and "still not converged" would be
  misread as "not a missing length". The test could only answer "no".
- The §25 rows (`results/tl_cal6_p3_*.csv`) hold no temperature.

## Quantity

The Johnson–Cook softening factor S = 1 − T*ᵐ with T* = (T − T_r)/(T_m − T_r), P-HG-Al: T_r = 293 K, T_m = 933 K,
m = 0.895 (§8.3). From the element temperature of the §25 R/256 runs (binary `d0500106d`, decks unchanged), at both
speeds (600 and 500 m/s), at every judged output (§25: 9 and 8 outputs up to t* = 0.81 / 0.85 ns):
- the area-averaged S over each §25 disc (0.25, 0.5, 0.75 a_256; particle and block side), as §25 averages p_n;
- the minimum S over the elements within 0.5 µm of the contact edge.
Also report the maximum temperature in the model at each output.

**Source:** the §25 field files, post-processing only. If they hold no temperature, rerun the two R/256 decks with
temperature added to the output and nothing else changed (§25: about 3 min each); the rerun must reproduce §25's stop
time and a_256(t) exactly, else stop and report.

## Rule (fixed now)

- **Uninformative:** S ≥ 0.95 for every judged disc and output, at both speeds and on both sides. Then the
  softening-off test cannot discriminate on this deck and is **not run**.
- **Informative:** otherwise. Then the softening-off test may be drafted (spec, rule and prediction committed first);
  this check does not fix its rule.
- The edge minimum is reported, not judged.

## Prediction (judgment, before any number)

- Uninformative: **0.6**. Against softening: the window ends before the jet is evaluated and the failure is present
  from about 0.1 ns. For it: the edge elements reach large strain early, and the R/256 stop is on a collapsing cell.
- Maximum temperature in the window: below 0.5 T_m, 0.7.

## Next unjustified step (recorded, not tested here)

That a result on the §25 2D quad deck carries over to the TLSPH skin, which is another host with another surface
measure.
