# Cold spray: hunch CS-25 (the contact as an object with a model of its partners: co-exposure by per-face compression), registration (frozen)

**Registered and frozen 2026-11-28, approved by Peter ("Freeze"), as drafted in a5a82be, with the tolerance 0.15
unchanged, before any v_cr value of the judged rows (H20-04, H20-05, H20-07) or of their denominators was read.**
Drafted 2026-11-28 (cloud, modeller) from the brief
[interface-as-object-2026-11-28.md](interface-as-object-2026-11-28.md), on Peter's request ("Write it as a hunch. This
will need a bit of reasoning and a fresh session."). Zero-code in the solver sense: an a(t)-driven interface model
whose v_cr consequence is a closed form, evaluated on the single-impact table. No solver run.
- **Budget:** this registration makes the count 3 of 5.
- **Rule 1's data clause: waived by Peter (chat 2026-11-28: "I waive the data clause. Finding something that
  converges has priority now."; DECISIONS 2026-11-28).** Every row it can be tested on is exposed
  (`data/vcr_lipit.csv`). The judged item below uses three H20 rows whose v_cr values are not quoted anywhere in the
  record, and fixes the predictions before they are read. That is weaker than unseen data, and any verdict is labelled
  **post hoc (exposed data)**. The real test (unseen pairs, residue maps, ring maps) has no source.
- Predictions: `scripts/cs25_predict.py` (reads `properties.csv` only; no v_cr value). Output quoted below.

## Exposure disclosure (B4 spirit)

- **Read in this session:**
  - the brief, the CS-24 result section (the six mismatched-pair ratios and the CH ratios), the zoo register
    (Z1–Z18), including its prose line on LIPIT matched values (Al 797–824, Ni 650–660, Zn 518–523 m/s);
  - metadata of `vcr_lipit.csv`: ids, particle, substrate, substrate temperature, the first characters of
    `oxide_state`, and, for the nine H20 mismatched rows, `regime`, `vcr_definition` and `d_um`.
- **Not read:** any `vcr_*` value of H20-04 (Cu on W), H20-05 (Sn on Cu) and H20-07 (W on Cu), nor of the H20 matched
  rows Cu on Cu and Sn on Sn. A grep of the repository finds H20-04/05/07 only in `vcr_lipit.csv` and in the Z9 regime
  rows of `predictions_v1.csv` / `scores_v1.csv`, which carry no velocity. The matched denominators are scored by Z6 in
  `scores_v1.csv`; that file was not opened.
- **Earlier exposure:** earlier sessions read Hassani 2020 in full. The modeller has no recollection of its pair
  values, but the exposure is real.
- **The form was chosen with the six context ratios in view.** Two simpler forms were discarded during drafting
  because they contradict the resolved signs of those six pairs (section 4). So the six pairs decide nothing; they are
  calibration context.

## 1. What CS-25 says, in one paragraph

The contact is an object of its own. Each interface element is born when the contact edge passes its radius, and it
holds one film state per face. A face is cleaned only if the edge is subsonic for that face *and* that face is
compressed enough to jet. Both partners feel the same traction, but they are compressed by different amounts
(μ_i = p / B_i). A contact that knows only its traction, like eq. 10 of problem-formalism.md, cannot tell whether each
face has jetted. One that holds a model of both partners (their bulk modulus B and impedance Z) and the edge kinematics
can. Bonding needs fresh metal on **both** faces at the same place (co-exposure), so the stiffer partner, the last to
be compressed enough, sets v_cr. For matched pairs this is exactly Z6 (v_cr = α c) and CS-20's ring. All new content is
in mismatched pairs.

## 2. The model

Particle p on substrate s, normal impact at speed V, particle radius R. SI units.

| # | Quantity | Form | Source |
|---|---|---|---|
| 1 | Partner model | B_i [Pa] from E, ν (rule P1); ρ_i; c_i = √(B_i/ρ_i); Z_i = √(B_i ρ_i) = ρ_i c_i | properties.csv, P-H20 rows |
| 2 | Edge kinematics | a(t) = √(2RVt − V²t²); edge speed u(r) = V √(R² − r²)/r | coldspray-kinematics.md (rigid; the only converged interface quantity is a(t)) |
| 3 | Birth | element at r born at t(r) = a⁻¹(r), with u(r) | from 2 |
| 4 | Shared pressure | p = V Z_p Z_s / (Z_p + Z_s) (planar acoustic contact, water-hammer) | textbook |
| 5 | Face compression | μ_i = p / B_i = Δu_i / c_i, Δu_i = p / Z_i | from 4 |
| 6 | Face state | φ_i(r) ∈ {0, 1}, 1 = film intact. φ_i(r) = 0 iff u(r) ≤ c_i **and** μ_i ≥ μ* | hunch |
| 7 | Bond state | b(r) = (1 − φ_p(r)) (1 − φ_s(r)) (co-exposure) | hunch |
| 8 | Particle bonds | iff b(r) = 1 on a non-empty annulus | hunch |
| 9 | Threshold | μ* = α/2 with α = 0.15 from Z6 (HG2018a), **not fitted here** | zoo Z6 |

Consequences (closed form):
- **v_cr(p on s) = (α/2) · max(B_p, B_s) · (1/Z_p + 1/Z_s).** Symmetric under swapping particle and substrate.
- **Matched pair:** p = VZ/2, μ = V/(2c), so v_cr = α c, which is Z6. In the kinematic reading of Z6
  (coldspray-kinematics.md, reading 2) this is the fixed switch angle atan(α) = 8.5°.
- **Each face's cleaning speed:** v_i = (α/2) B_i (1/Z_p + 1/Z_s). The face with the smaller B is cleaned first.
- **Inner radius of the bonded ring** at V ≥ v_cr: r_in/R = V / √(V² + min(c_p, c_s)²). For matched pairs this is
  CS-20's strong form (k = 1). At v_cr it is 0.148 for every matched pair.

**Reading of μ*:** each face must be compressed by 7.5 % (linear acoustics) before its jet can clear the film. At that
compression the Hugoniot correction to the shock speed is about 10 % (S ≈ 1.3–1.5); it is not included.

**What the form leaves out** (stated, not tested):
- strength, hardening and temperature: substrate heating changes only B and ρ, so CS-25 predicts almost no CH shift.
  The exposed CH drops (Al −11 %, Sn −18 %) are not explained. For matched pairs CS-25 adds nothing to Z6;
- size: the form has no length, so no size effect. Size corrections use Z8's measured exponent (below);
- the interface's own length (oxide thickness, process zone) and a graded, fed-and-drained film state φ(r, t): both add
  parameters that one v_cr per pair cannot fix (problem-formalism §2(e)); they are not part of this hunch;
- geometry: a sphere on a half-space is not a planar contact. This is the likeliest reason for the largest context
  miss (Cu on Al, penetration regime; section 4);
- oxide type, rate effects, melting (Z10; relevant for Sn).

## 3. The five questions of the brief

1. **How it differs from R3, CS-20 and the other tried routes.**
   - CS-20 and R3 put one threshold on one kinematic switch, with the sound speed of a matched pair. CS-25 has a
     switch per face (from each partner's c), a compression condition per face (from each partner's B), and a
     co-exposure rule. For matched pairs it reduces to CS-20 (strong form) plus Z6, so it says nothing new there.
   - CS-12 (Bay stretch) and the pressure–slip driver read solver interface fields, which do not converge (§26, §27).
     CS-25 reads none: only a(t) and material constants. It does not regularise any solver field and does not need to.
   - CS-24 was thermal. CS-25 has no thermal term.
2. **Parameters, and what fixes each.**
   - α = 0.15: fixed by Z6 (HG2018a, matched pairs, Al, Cu, Ni, Zn). Not refitted. μ* = α/2 follows.
   - The pressure partition (eq. 4): none (textbook).
   - The co-exposure rule (AND of both faces): a structural choice with no constant. It was chosen with the six
     context ratios in view (section 4).
   - The scoring tolerance 0.15 (section 6): a scoring choice, fixed now.
   - The graded form (supply rates, expulsion) would add at least two constants. Only ring maps could fix them; none
     unseen exists. Not registered.
3. **Which zoo members it must beat, and on what.** On mismatched pairs:
   - **Z6, particle only** (the particle's v_cr unchanged by the substrate; ratio 1);
   - **Z6 with Z7's mismatched-pair rule** (arithmetic means of B and ρ of both bodies). Z7 itself is not runnable
     here (no tensile failure strains for these materials); this comparator stands in for its mean rule.
   - Z9 gives regimes, not v_cr. Whether CS-25's limiting face matches Z9's regime label is reported, not judged.
   - On matched pairs CS-25 is Z6: nothing to beat, nothing claimed.
4. **A kill criterion that is not post hoc.** None exists on available data. The judged item (section 6) is post hoc
   in the exposure sense but uses rows outside the reasoning record, with the form and the predictions fixed first.
   A waiver of rule 1's data clause is needed, as for CS-24.
5. **Closest relatives** (from memory; the literature step runs after the freeze, see the checklist):
   - water-hammer pressure of two impedances (textbook);
   - HG2018a (Z6): v_cr ≈ 0.15 √(B/ρ) from shock and release at the edge. CS-25's per-face condition is Z6's criterion
     applied to each face;
   - Hassani 2020 (Z9): the same acoustic partition of material velocities, turned into a damage-number ratio with
     dynamic yield to give regimes. CS-25 drops the strength and turns the partition into a v_cr via co-exposure;
   - Z7's arithmetic-mean rule for dissimilar pairs (via Panova 2026b);
   - Bay's cold-welding picture: both surfaces' cover layers must break for fresh metal to meet (from memory, not read
     in this track);
   - the third body (Godet 1984; Berthier): the interface as a body fed by both partners. Framing only; no third-body
     rheology is used;
   - Walsh et al. 1953 and HG2018 (subsonic-edge jetting); CS-20.
   - **Label: at most "variant of Z6 extended to dissimilar pairs with Z9's partition and a co-exposure rule"; never
     "novel".**

## 4. How the form was chosen (calibration context: exposed, decides nothing)

With the six CS-24 pairs in view (the brief lists their ratios), three forms of the per-face condition were tried:
- **sound speed only** (face i jets strongly iff V/c_i ≥ α; bond iff both): v_cr = α max(c_p, c_s). It predicts
  ratio 1.00 for Al on Ni and Al on Ti, both resolved at +34 % and +26 %. Discarded;
- **either face suffices** (OR instead of AND): it predicts Al on Cu 0.71 and Al on Ni 0.68 of Al on Al, the wrong
  sign for every Al-particle pair. Discarded;
- **compression per face, both faces (AND):** kept.

The kept form against the six ratios (`scripts/cs25_predict.py`; observed ratios copied from the CS-24 result table,
size-corrected there):

| Pair | r_obs | resolved | CS-25 ratio | \|ln error\| CS-25 | Z6 particle only | Z6 mean |
|---|---|---|---|---|---|---|
| Al on Cu | 1.082 | no | 1.217 | 0.117 | 0.079 | 0.311 |
| Al on Ni | 1.344 | yes | 1.541 | 0.137 | 0.296 | 0.435 |
| Al on Ti | 1.260 | yes | 1.145 | 0.095 | 0.231 | 0.288 |
| Cu on Al | 1.120 | yes | 1.693 | **0.413** | 0.113 | 0.015 |
| Cu on Ti | 1.400 | yes | 1.286 | 0.085 | 0.336 | 0.245 |
| Ti on Cu | 0.825 | no | 1.016 | 0.208 | 0.192 | 0.049 |

- On the four resolved pairs CS-25 has the right sign every time and the smallest error on three. It misses Cu on Al
  (Z9: penetration, a dense particle into a soft substrate) by a factor 1.5.
- Because the law is symmetric, the Cu on Al miss is the same statement as: Al on Cu and Cu on Al should need the same
  v_cr, and they very likely do not.
- No constant was fitted to these rows, but the AND rule was picked against them. That is why they are context only.

## Hunch

```yaml
- id: CS-25
  status: open (registered and frozen 2026-11-28)
  lens: partner-aware contact, Peter's reframing (the contact's model of its partners)
  statement: >-
    The contact is an object with a model of both partners. An interface element born at radius r when the edge
    passes holds one film state per face. A face is cleaned only if the edge is subsonic for that face and that face
    is compressed by at least mu* = alpha/2 under the shared contact pressure. The particle bonds only where both
    faces are clean (co-exposure). Since the two faces share the traction but not the compression, the partner with
    the larger bulk modulus sets v_cr. For dissimilar pairs, v_cr(p on s) = (alpha/2) max(B_p, B_s)(1/Z_p + 1/Z_s),
    with alpha = 0.15 from Z6 and no constant fitted. For matched pairs it is Z6.
  mechanism: >-
    Jetting clears the film from a face once that face is shocked hard enough (Z6's criterion, read per face) and the
    edge is subsonic for it (Walsh, HG2018). Fresh metal must meet fresh metal (Bay; co-exposure), so a face that is
    not compressed enough keeps its film and blocks bonding, whatever the other face does. In a planar acoustic
    contact the pressure is shared, p = V Z_p Z_s/(Z_p + Z_s), so face i is compressed by p/B_i: the stiffer face
    lags. Matched pairs are compressed equally, so both faces arrive together; in dissimilar pairs the stiff face
    comes late or the soft face takes most of the velocity, depending on B and Z.
  law: "v_cr = (alpha/2) max(B_p, B_s)(1/Z_p + 1/Z_s); alpha = 0.15 (Z6), B from E and nu, Z = sqrt(B rho)"
  predicted_effect:
    - metric: v_cr(Cu on W) / v_cr(Cu on Cu), size-corrected
      direction: up
      size: 1.689
    - metric: v_cr(Sn on Cu) / v_cr(Sn on Sn), size-corrected
      direction: up
      size: 1.794
    - metric: v_cr(W on Cu) / v_cr(Cu on Cu), size-corrected
      direction: up
      size: 1.689
    - metric: v_cr(W on Cu) / v_cr(Cu on W), size-corrected (reported only)
      direction: same
      size: 1.000
  kill_criterion: see "Rule" (section 6), fixed before any of the judged rows is read
  known_relatives: see section 3, question 5
  label: at most "variant of Z6 extended to dissimilar pairs with Z9's partition and a co-exposure rule"
  author: claude (modeller), from Peter's reframing
```

## 5. Predictions (`uv run python scripts/cs25_predict.py`, 2026-11-28)

Partner models (rule P1, P-H20 rows): Al B 77.8 GPa, c 5367 m/s, Z 14.49 MRayl; Cu 133.3, 3858, 34.56; Ni 175.4, 4438,
39.53; Ti 107.4, 4882, 22.00; Sn 59.5, 2862, 20.80; W 311.4, 4022, 77.42. Matched v_cr = α c: Al 805, Cu 579, Ni 666,
Ti 732, Sn 429, W 603 m/s.

**Judged item (H20 rows not quoted in the record):**

| Pair | CS-25 v_cr [m/s] | limiting face | ratio against | CS-25 ratio | Z6 particle only | Z6 mean | r_in/R at v_cr | face cleaned from, p / s [m/s] |
|---|---|---|---|---|---|---|---|---|
| Cu on W | 977 | substrate | Cu on Cu | 1.689 | 1.000 | 1.029 | 0.246 | 418 / 977 |
| Sn on Cu | 770 | substrate | Sn on Sn | 1.794 | 1.000 | 1.204 | 0.260 | 344 / 770 |
| W on Cu | 977 | particle | Cu on Cu | 1.689 | 1.043 | 1.029 | 0.246 | 977 / 418 |

Cu on W and W on Cu share the denominator row and get the same CS-25 value; they are not independent.

**Unseen predictions (no H20 row; no source known):**

| Pair | CS-25 v_cr [m/s] | ratio to the particle's matched pair | Z6 mean ratio | face cleaned from, p / s [m/s] |
|---|---|---|---|---|
| Ni on Al | 1241 | 1.864 | 1.052 | 1241 / 550 |
| Ti on Al | 922 | 1.259 | 1.038 | 922 / 668 |
| Cu on Ni | 714 | 1.233 | 1.078 | 542 / 714 |
| Ni on Cu | 714 | 1.072 | 0.937 | 714 / 542 |
| Al on Sn | 683 | **0.848** | 0.692 | 683 / 523 |
| Sn on Al | 683 | 1.591 | 1.297 | 523 / 683 |
| Al on W | 1913 | 2.376 | 0.784 | 478 / 1913 |

- **Not every mismatch costs.** Al on Sn is predicted to bond 15 % below Al on Al (a soft, low-B substrate takes most
  of the velocity, and Al is then the stiffer face). Sn's low melting point (Z10) may interfere.
- **Reversal symmetry:** v_cr(X on Y) = v_cr(Y on X) for every pair. The context miss (Cu on Al) already suggests it
  fails for Al/Cu.
- **Residue below v_cr:** between the two faces' cleaning speeds, the face with the smaller B is cleaned outside r_in
  and the stiffer face keeps its film. Example: an Al particle rebounding from Ni between 550 and 1241 m/s shows fresh
  metal on the particle side only. This is the prediction closest to the brief's "interface as object", and it needs
  surface analysis of rebound pairs, which no source has.
- **Ring:** at v_cr the unbonded centre of a dissimilar pair is larger than that of a matched pair (r_in/R 0.18–0.27
  against 0.148 for the nine H20 pairs), with its edge set by the partner with the lower sound speed.

## 6. Rule (fixed at the freeze; applied once, after it)

**Judged item J** (H20-04 Cu on W, H20-05 Sn on Cu, H20-07 W on Cu):
1. **Unit.** r_obs = v_cr,mid(numerator) / v_cr,mid(denominator) as in the table above, both rows from H20. Correct for
   size with Z8's measured exponent: multiply by (d_num / d_den)^0.2, using `d_um`. The law itself has no size term.
2. **Tolerance.** hw = the summed half-widths ln(v_high / v_low)/2 of the two rows. tol = hw + 0.15.
3. **Score per pair.** Agree if |ln r_obs − ln r_CS25| ≤ tol, else disagree. Closer if |ln r_obs − ln r_CS25| is smaller
   than the error of both comparators (Z6 particle only, Z6 mean).
4. **Verdict J:**
   - **supported (post hoc):** at least 2 of 3 agree, and CS-25 is closer than both comparators on at least 2 of 3;
   - **refuted:** at least 2 of 3 disagree;
   - **undetermined:** otherwise.
5. **Reported with the verdict, not judged:**
   - the reversal ratios v_cr(Y on X)/v_cr(X on Y) for all three H20 reversal pairs (Al/Cu, Cu/Ti, Cu/W), against
     CS-25's 1.00;
   - the S1 distance of CS-25's absolute v_cr for all nine H20 mismatched rows;
   - CS-25's limiting face against Z9's regime label (by construction both lean on B: Z9's ratio uses ρC₀²Y_d);
   - the result without the size correction.

The 0.15 was chosen with the context errors in view (0.085–0.137 on the three good pairs, 0.413 on Cu on Al). Peter
may change it before the freeze, not after.

## Author's prediction (judgment, before any judged row is read)

- J: supported 0.30, refuted 0.35, undetermined 0.35.
- Why: Cu on W and Sn on Cu are splatting pairs (soft particle, stiff substrate), where the context errors were small.
  W on Cu is a penetration pair like Cu on Al, where CS-25 overshot by a factor 1.5; it will likely disagree. The
  predicted ratios (+69 %, +79 %) are large, so even the splatting pairs can miss outside the tolerance.
- If W on Cu disagrees as expected, the verdict hangs on the two splatting pairs.

## What follows (stated now)

- **Supported (post hoc):** two measurement items for a data request. (1) Surface analysis of a rebound pair between
  the two cleaning speeds (e.g. Al on Ni or Al on Ti): fresh metal on the soft-B face only. (2) v_cr of a reversal pair
  (Ni on Al against Al on Ni) and of Al on Sn. No solver form is drafted before that.
- **Refuted:** negative result. The acoustic co-exposure reading of the contact's partner model is closed at the R1
  level. A geometric (sphere on half-space) partition would be a new hunch, not a rescue.
- **Undetermined:** parked with CS-20 until an unseen dissimilar-pair source appears.
- **Either way:** CS-25 does not address Peter's point that partner awareness should matter for matched pairs
  (DECISIONS 2026-11-28). The CH observation (substrate heating acts far beyond thermal partition) stays with CS-17 /
  substrate state.

## Before the freeze (checklist)

1. ~~Peter: rule 1 waiver.~~ Waived 2026-11-28 (DECISIONS).
2. ~~Peter: the tolerance and the verdict thresholds.~~ Frozen as drafted (Peter asked why 0.15; answered in chat,
   see DECISIONS 2026-11-28).
3. **Literature step after the freeze** (as for CS-24): any search for dissimilar-pair v_cr laws would likely surface
   Hassani 2020's pair values, which are item J's data. The step sets only the label, not the prediction.
4. **Scoring script** `scripts/cs25_score.py`, committed after the freeze and before it is run.
5. **Facts check** (coldspray-procedure.md): no solver output is read. Inputs: `properties.csv` (`E_GPa`, `nu`,
   `rho_kg_m3` of the P-H20 rows; used under rule P1 since the retrospective test) and `vcr_lipit.csv` (`id`,
   `particle`, `substrate`, `vcr_low_mps`, `vcr_high_mps`, `vcr_mid_mps`, `d_um`; used by CS-24). The `regime` column
   is read for a report-only line. Not covered: none.

## Result (2026-11-28, after the freeze; post hoc, exposed data)

`uv run python scripts/cs25_score.py` (committed in 35f803c before it was run). The first run crashed on blank fields
before printing any number. The fix (a13ae83, rule unchanged) reports rows without a numeric window as not scorable.

**Verdict J: UNDETERMINED: not scorable.** H20-04 (Cu on W), H20-05 (Sn on Cu) and H20-07 (W on Cu) carry no v_cr
window. Hassani 2020 Table 1 prints NA ("no post-impact indentations found; no window satisfying the definition",
"no window; competition with melting", "no window satisfying the definition"). So 0 agree and 0 disagree, which is
"undetermined" by the frozen rule.
- **This is a drafting error.** Before the freeze the modeller checked these rows' metadata (`regime`, `d_um`) and
  that no file quoted them, but not that their v_cr fields were filled. The blanks are why no file quoted them. The
  facts check of the checklist covers columns, not the presence of values in the judged rows.

**Reported, not judged:**

| Item | Value | CS-25 |
|---|---|---|
| Reversal Cu on Al / Al on Cu (size-corrected) | 0.711 (ln −0.341, hw 0.137) | 1.000 |
| Reversal Ti on Cu / Cu on Ti | 0.764 (ln −0.270, hw 0.183) | 1.000 |
| Reversal W on Cu / Cu on W | not scorable | 1.000 |

| Row | CS-25 v_cr [m/s] | window [m/s] | S1 | limiting face | Z9 regime |
|---|---|---|---|---|---|
| H20-01 Al on Ni | 1241 | 1080–1210 | 0.027 | substrate | splatting |
| H20-02 Al on Ti | 922 | 1000–1110 | 0.074 | substrate | splatting |
| H20-03 Al on Cu | 979 | 855–990 | 0.000 | substrate | splatting |
| H20-06 Cu on Al | 979 | 625–710 | 0.404 | particle | penetration |
| H20-08 Ti on Cu | 744 | 525–685 | 0.097 | substrate | co-deformation |
| H20-09 Cu on Ti | 744 | 765–845 | 0.026 | particle | co-deformation |

H20-04, -05 and -07 are not scorable (Z9: splatting, splatting, penetration). No-size-correction ratios: not printed
for J (nothing scorable).

**Reading (post hoc; not a verdict):**
- **The law's structural prediction fails on exposed data.** CS-25 is symmetric under swapping particle and
  substrate. Both scorable reversal pairs break that symmetry beyond their windows: the reversed pair needs 24–29 %
  less. A symmetric planar partition cannot represent this. The asymmetry has to come from what the frozen form left
  out (the geometry of a sphere on a half-space, and strength).
- **Absolute values:** the splatting and co-deformation rows lie within 10 % of their windows (S1 ≤ 0.097) with no
  constant fitted. The penetration row (Cu on Al) misses by 40 %. These are the context pairs the form was chosen on,
  so this is not evidence.
- **The NA notes** (no indentation of W under Cu, melting competition for Sn) are qualitative. They carry no weight
  for or against CS-25.
- **Against the prediction:** undetermined 0.35, as it happened, but for a reason the author did not foresee.
- **Literature step:** not run. The verdict does not depend on it, and the label stays at most "variant of Z6
  extended to dissimilar pairs with Z9's partition and a co-exposure rule".

**Consequences, as fixed in "What follows" (undetermined):** parked with CS-20 until an unseen dissimilar-pair source
appears; hunch count back to 2 of 5. The reversal failure means that a later test, if one comes, tests a form already
known to miss a symmetry property on exposed data.
