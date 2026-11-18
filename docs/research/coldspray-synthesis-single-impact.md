# Cold spray: single-impact phase, synthesis (2026-11-18)

The deliverable of the single-impact phase's end point (DECISIONS 2026-11-07): what is known about single-particle
v_cr, scored; the negative results; and the open decisive experiment. The end point was reached on 2026-11-18: B03,
B05 and B12 closed without predictions, B07 and B16 report no v_cr, B06 scored, and the T3 measurement request
dropped (2026-11-17). Every number cites a results note. Nothing here is a new claim.

## 1. What holds

- **Sound speed carries most of the signal for pure metals.** Z6 (v_cr ≈ 0.15 √(B/ρ)) beat the property-free baseline
  on held-out rows: median S1 0.171 against 0.418 (CS-03 supported; results-v1). Blind, it falls within 1–6 % on six
  of eight pure-Al conditions of B14 (in-sample material) and 3.5–8 % high on B06 (out of domain, no size reported).
  The Hugoniot-C₀ variant does slightly better (in-domain median 0.053 against 0.080, results-v1); this is a lead,
  not a test.
- **Oxide raises v_cr within one metal.** CS-07 was supported twice: on B14 (+129.6 m/s for the hydroxide batch,
  exposed; results-b02-b14) and on B06 (+32 m/s for a 20 nm ZnO coat, w = 30.5; results-b06). Its direction also
  agreed on B10 (support undetermined). Each time the oxide type changed together with the thickness, so the
  support is for "more or different oxide", not for thickness alone.
- **Bonding starts in a ring.** Bonding in an annulus with an unbonded, oxide-covered centre is what B06's sections
  show, and CS-12's T1 is not refuted. It is exposed (the pattern was known from earlier papers, and Tang2024 shows
  it in bond strength).

## 2. What failed (negative results)

| Hunch or model | Data | Result | Note |
|---|---|---|---|
| CS-06: process FE values lie below single-impact windows | v1 | refuted | the gap is source by source, not a constant |
| CS-08: particle strength raises v_cr within one alloy | B10 | refuted | strength loss and oxide growth offset each other |
| CS-16: a harder substrate raises v_cr | B02 | refuted (Δ −75 against +102 predicted) | the cold-worked plate bonds earlier; the authors point to jetting and strain-hardening capacity |
| CS-02: sound speed alone ranks Al alloys | v1 | supported (that it cannot) | Z6 under-predicts age-hardenable Al by 8–16 % (B10 too) |
| Z6 on soft, heavy metals | v1 | d 0.17–0.44 | over-predicts Au, Ag, Sn |
| Hydroxide | B14 RH-95 / RH-95-D | Z6 −17 % / −11 % | oxide chemistry matters beyond thickness (T4 side) |
| Track B: a verified 3D interface-state solver | §14–§27 | route closed 2026-11-17 | not verifiable with the references available; integral bulk quantities are verified |

**Also refuted:** CS-13c (heat conduction as a regulariser of the contact edge; a rediscovery). **Inconclusive or
undetermined:** CS-01 (Z6 transfer to held-out pure metals), CS-05 (size law), CS-09 (sound speed alone within B10),
CS-11 (interface bracket).

## 3. What stays open

- **The decisive experiment: T3**, v_cr against oxide thickness at one oxide type, with particle strength unchanged.
  Four frozen models disagree by about one window each (Z18_Yd +127, Z18_static +92, CS-10 +37, CS-12 0 m/s for
  Al 6061 at 15 µm, 17 → 25 nm). No unseen series exists, and the request was dropped, so the question stays open.
  CS-10 and CS-12 remain open and untested; CS-17 needs an unseen substrate series.
- **The missing strength term.** Z6's misses (soft heavy metals high, Al alloys low) point to a strength-like term in
  opposite directions. Static strength did not order B10 (CS-08 refuted), and substrate hardness had the wrong sign
  on B02 (CS-16 refuted). What enters is not simply strength or hardness. The B02 reading (jetting, strain-hardening
  capacity) and the B06 reading (extrusion through oxide gaps) both point at the interface, which Track B could not
  verify.
- **Data gaps:** no impact-tested powder has a reported failure strain or work-hardening exponent; most papers print
  v_cr without window bounds (rule B6 then applies); particle size is sometimes withheld or not printed (B06).

## 4. Process lessons

- Pre-registration with frozen scorers worked: every verdict above came from rules and scripts committed before the
  outcomes were read.
- Registering ran ahead of testing (17 hunches in five days, 2026-11-07). The hunch budget fixed that; three hunches
  are open now.
- The modeller's predictions on the simulation track were repeatedly too optimistic; independent reviewers estimated
  about ten times lower odds (odds review 2026-11-16), and the data agreed.

## 5. Next (Peter)

The reduced-route plan is adopted (docs/research/reduced-route-plan.md). Which option leads — R1 closed-form v_cr law,
R2 particle-level build-up rule, R3 kinematic Bay estimate — is Peter's choice.
