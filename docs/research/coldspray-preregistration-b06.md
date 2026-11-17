# Cold spray: pre-registration for blind paper B06 — Frozen 2026-11-17 (Peter approved)

Frozen with `data/predictions_b06.csv` (generated in f82f197, unchanged), **before** any outcome of B06 is extracted (rule B2, step 2). Inputs:
`data/blind_inputs.csv`, rows B06-c1 and B06-c2, as merged in 5f7bf7d (WSL B task b10; leak scan clean: inputs only,
diameters withheld, no outcomes). Code: `src/schemeforge/research/coldspray_blind_b06.py`; the frozen
`coldspray_blind2.py` (B02/B14) is untouched.

**Paper.** B06: Wu et al. 2026, "Mechanisms of oxide layer fracture during microparticle impact bonding", Scripta
Mater. 283, 117444, doi:10.1016/j.scriptamat.2026.117444; publisher version supplied by Peter (sha256 188dadc3…b2b).

## Inputs (as extracted)

| Condition | Particle | Oxide | Substrate |
|---|---|---|---|
| B06-c1 | Al single-crystal particles (vacuum-annealed THP-A20S powder) | native Al oxide, 4.5 ± 0.9 nm (TEM) | Al plate, 99 %, polished to 0.05 µm, air-exposed |
| B06-c2 | the same, then ZnO-coated by barrel sputtering | ZnO 20 ± 1 nm on the particle; native Al oxide 4.5 nm on the substrate | the same |

- **Particle diameters are withheld** (mixed with outcome); no nominal powder size is given.
- Velocity uncertainty about 2 %. Temperatures and impact angle are not stated.
- Strength data are **cited, not measured**: a SC Al dynamic yield strength of about 50 MPa (B06's ref. [36]);
  quasi-static compression of SC Al–ZnO particles (flow-stress factor about 1.75, ZnO fracture strain about 12–15 %,
  first-fracture stress about 60 MPa) from ref. [31] (Tang, Ichikawa, Hassani, Scripta Mater. 244, 2024, 116008); ZnO
  and Al₂O₃ differ by about 8 % in fracture strength and about 50 % in hardness (refs. [21, 22]).
- The two conditions differ in **oxide type and thickness together**. They are not a series of one oxide type over
  several thicknesses, so B06 is **not a T3 test**.

## Exposure (rule B4)

- The modeller has not opened B06 or its ref. [31].
- **Tang2024** (Nat. Commun. 15, 9630; same group; seen at S level, coldspray-data-and-zoo.md) shows a weak centre and
  a rise toward the edge in a site-specific bond-strength map of Al–Al splats. It is a different paper, but it
  informs any bonded-area reading.
- The **bonded-ring pattern** (unbonded centre) is exposed in general (blind-literature log, 2026-11-05), so any CS-12
  T1 verdict on B06 is reported as exposed.
- **B06 v_cr values:** not seen.

## Rules

- **Input rules of each frozen model, unchanged:**
  - Z6 and the baseline by the v1 rules;
  - DW_size for Al and Ti, and it needs d;
  - CS-10 needs d, a static particle strength (static compression, else powder hardness by Tabor) and a numeric oxide
    thickness;
  - Z18_static needs a static strength;
  - Z18_Yd needs a Y_d fitted by the paper itself to rebounds below v_cr. σ0 is sourced for aluminium oxide only.
- **Temperatures:** room (rule BP3). **Substrate:** polished. **d:** not reported, so every model with a size domain
  is out of domain.
- **Score:** rule S1 per condition. Windows as printed, else rule B6 (v_cr ± the stated ~2 %).
- **w** = the median window width of the paper.

## Frozen predictions (m/s; `data/predictions_b06.csv`)

| Model | B06-c1 | B06-c2 | Domain |
|---|---|---|---|
| Z6_a015 | 805.1 | 805.1 | out (d not reported) |
| Z6_a015_C0 | 807.0 | 807.0 | out |
| baseline_LOMO | 611.5 | 611.5 | out |
| DW_size | no prediction (needs d) | no prediction | — |
| CS-10 | no prediction (no d; no static particle strength) | no prediction | — |
| Z18_static | no prediction (no static strength) | no prediction | — |
| Z18_Yd | no prediction (Y_d only cited, not fitted by B06) | no prediction (also: ZnO outside σ0) | — |

Every model with a prediction gives one value for both conditions: none has a term for oxide type, and none can use
the thickness without d or a strength.

## Hunch tests on B06

```yaml
- id: CS-07 on B06 (tested hunch, applied again)
  statement: Oxide raises v_cr within one metal (registered as CS-07).
  metric: Delta = v(B06-c2) - v(B06-c1)
  kill_criterion: >-
    Refuted if Delta <= 0. Supported if Delta > w. Inconclusive otherwise. Caveat: oxide type changes with thickness
    (native Al oxide against 20 nm ZnO on top of it), so support is not specific to thickness, and a refutation could
    come from the weaker, softer ZnO. Not exposed for the v_cr values.
- id: CS-12 on B06
  statement: >-
    T4 (oxide type changes): not predicted, reported. T1 (bonded-area pattern): if B06 prints bonded-area or
    oxide-residue maps at or just above v_cr, refuted if bonding is concentrated at the centre with an unbonded rim;
    reported as exposed (the ring pattern is known).
  note: T3, CS-12's decisive test, needs a thickness series of one oxide type; B06 has none.
- id: CS-10 on B06
  statement: no prediction by its frozen rule (no d, no static particle strength). Nothing is scored.
```

## What B06 can and cannot decide (plain statement)

B06 hardly discriminates between the open hunches.
- **It can score:** Z6 and the baseline in absolute terms (out of domain); the sign of the oxide effect under CS-07,
  with a type confound; and, if maps are printed, CS-12 T1 (exposed).
- **It cannot test:** CS-10 (no inputs), CS-12's decisive T3 (no thickness series), or CS-17 (one substrate).
- The decision on the T3 measurement request does not depend on B06.

## Modeller's expectation (judgment, before any outcome)

Δ > 0 is more likely than not (probability about 0.6). The coating is four times thicker, and ref. [31] reports a
stiffer, harder-to-deform coated particle. Against that, ZnO is the weaker and softer oxide. Z6 at 805 m/s: no
expectation beyond the out-of-domain flag, because the size is unknown.
