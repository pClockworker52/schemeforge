# Cold spray: blind test B06, results

Order of record:
- draft predictions: f82f197; **frozen**: c484494 (Peter approved);
- scoring script: 17e80eb (`coldspray_blind_b06_score.py`, tested on synthetic rows);
- outcomes (WSL B, step 3, task b12): da1900b, committed after all three;
- scores: this commit (`python -m schemeforge.research.coldspray_blind_b06_score`, `data/scores_b06.csv`).

Not a judge run. Rule B3: **Al is an in-sample material for Z6** (its fit used Al, Cu, Ni, Zn), so Z6's values test a
new condition of a known material. Every prediction is out of domain because B06 prints no particle diameter.

## Measured (as extracted; publisher version)

| Condition | What | v_cr (m/s) | Window used |
|---|---|---|---|
| B06-c1 | Al single crystal, native Al oxide 4.5 nm | 746 | bounds not printed; ±2 % (B6): 731.1–760.9 |
| B06-c2 | the same with 20 nm ZnO | 778 | bounds not printed; ±2 % (B6): 762.4–793.6 |

w_B06 = 30.5 m/s (rule B6).
- **Definition:** the velocity at which bonding and rebound are equally probable.
- **Spreads printed but not used as the window:** SD 3.8 / 4.5 m/s; 99 % CI ±6.9 / ±5.6 m/s.
- **Particle size:** none for the population. The two particles sectioned for TEM are 17.0 and 17.3 µm, inside Z6's
  8–16 µm domain only if the population matched them, which is not stated.

## Scores (rule S1: 0 inside the window, else distance to the nearest bound over the midpoint)

| Model | B06-c1 | B06-c2 | Domain |
|---|---|---|---|
| Z6_a015 (805.1) | 0.059 | 0.015 | out (d not reported) |
| Z6_a015_C0 (807.0) | 0.062 | 0.017 | out |
| baseline_LOMO (611.5) | 0.160 | 0.194 | out |
| DW_size, CS-10, Z18_static, Z18_Yd | no prediction | no prediction | — |

Z6 overpredicts both conditions, by 8 % and 3.5 %. The baseline underpredicts by 18–21 %.

## Hunch tests

- **CS-07 on B06: supported** by the frozen rule. Δ = v(c2) − v(c1) = **+32 m/s** against w = 30.5 m/s, a margin of
  1.5 m/s. **Caveat (stated before the outcome):** the oxide type changes with the thickness (native Al oxide against
  20 nm ZnO over it), so this support is not specific to thickness. Not exposed for the v_cr values.
- **CS-12 T4** (oxide type changes): reported, not predicted: +32 m/s.
- **CS-12 T1** (bonded-area pattern): **not refuted, exposed.** On the sectioned particles, bonding sits in a
  continuous middle region. The centre keeps oxide with gaps and no metallurgical bond, and the edge carries piled-up
  oxide. That is a bonded annulus with an unbonded centre, not "bonding concentrated at the centre with an unbonded
  rim". The authors state that one particle per condition is representative of SEM top views of several particles.
- **CS-12 T3** (thickness at one oxide type): not tested; B06 has no such series, and the T3 request was dropped.
- **CS-10, Z18:** no predictions by their rules (no d, no static strength).

## Against the modeller's expectation

Δ > 0 was expected with probability about 0.6: right. No expectation was stated for Z6 beyond the domain flag.

## What the authors say (as reported, not a verdict)

- The thicker ZnO resists the opening of oxide-free gaps, so more pressure is needed to extrude metal through them.
  This raises v_cr by a "modest" ~4 %.
- Below ~200 m/s the coated particles rebound more elastically, which the authors attribute to oxide strengthening.
- The authors' account is a thickness-and-extrusion reading close to CS-12's extrusion picture (p_E) with a thickness
  dependence. CS-12's minimal variant excludes such a dependence at fixed type. Because the type changed too, B06
  cannot decide between them, and no verdict is drawn.

**Exposure:** none for the v_cr values. Tang2024 (seen) informs the ring reading; ref. [31] was not opened.
