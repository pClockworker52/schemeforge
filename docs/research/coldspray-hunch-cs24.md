# Cold spray: hunch CS-24 (the substrate as a heat sink: a partner-aware thermal v_cr law), DRAFT

**Draft 2026-11-28 (cloud, modeller), not registered, not frozen. Ready for the freeze** (checklist below). Peter asked for it (chat 2026-11-28), after the
modeller's reasoning on partner-aware contact against problem-formalism.md. Zero-code in the solver sense: a closed-form
law evaluated on the single-impact table. No solver run.
- **Budget:** registration would make the count 3 of 5.
- **Rule 1's data clause: waived by Peter (chat 2026-11-28; DECISIONS 2026-11-28).** Every row it can be tested on is
  exposed (`data/vcr_lipit.csv`, read in this track since 2026-11-03). Any verdict is labelled **post hoc (exposed
  data)**.
- **Exposure disclosure (B4 spirit).**
  - This session read only the table's metadata: column names, the (source, particle, substrate) row counts and the
    particle sizes. No v_cr value was read.
  - It also read the zoo register (coldspray-data-and-zoo.md, Z1–Z17), which quotes Dowding 2020's measured size
    exponent (Z8: n = 0.19 Al, 0.21 Ti). The law's size exponent of −1/5 was derived in the modeller's working before
    that row was read, but no committed record predates the reading. **The size prediction therefore counts as
    exposed and is not judged as a discriminating test.**
  - Earlier sessions read Hassani 2020 (the mismatched pairs) in full. The modeller has no recollection of its pair
    values, but the exposure is real.
  - **2026-11-28, while adding item B:** the `notes` column of the CH rows and of H20-17 was read. It prints the
    authors' room-temperature comparison values: Al 810 m/s at 14.4 µm, Sn 330 m/s, Ti 765 m/s, and quotes of
    797–824 and 810 ± 16 m/s for Al–Al. These are item B's references. The heated values (`vcr_*` of CH) and every
    item-A value remain unread.

## Hunch

```yaml
- id: CS-24
  status: draft (not registered)
  lens: transfer / partner-aware (Peter's partner-aware contact idea, thermal reading)
  statement: >-
    Bonding needs the interface layer to reach a temperature rise set by the particle's melting margin, and that
    rise is limited by heat flowing into BOTH bodies during the contact. The substrate is a heat sink whose strength
    is its thermal effusivity e = sqrt(k rho c_p). So v_cr depends on the substrate's thermal effusivity, not only
    on its mechanical properties, and on particle size through the contact time. It acts in matched pairs too: the
    interface starts at the effusivity-weighted mean of the two temperatures, so for identical materials heating
    the substrate by dT counts half as much as heating the particle by dT. Particle-only thermal laws (Z1, Z2) give
    the substrate's temperature no weight.
  mechanism: >-
    problem-formalism.md §2(a): the only physical length below R is the thermal one, sqrt(kappa t), and it is a
    two-body length: heat made next to the interface drains into both bodies, partitioned by effusivity (contact of
    two half-spaces; Carslaw and Jaeger, textbook). §2(b): softening starts after a rise of only about 50 K, so the
    interface temperature history decides whether the layer softens in time. Model: the interface receives a heat
    flux q'' = c1 rho_p V^3 over the contact time t_c = d / V (both up to constant factors). The interface temperature
    rise of two half-spaces under a common flux is dT = (2 / sqrt(pi)) q'' sqrt(t_c) / (e_p + e_s), from the initial
    interface temperature T_i = (e_p T_p + e_s T_s) / (e_p + e_s). Bonding iff dT >= theta (T_m,p - T_i).
  law: >-
    v_cr = Lambda * [ (e_p + e_s) (T_m,p - T_i) / (rho_p sqrt(d)) ]^(2/5), with ONE fitted constant Lambda (it
    absorbs c1, theta and the geometric factors). Every ratio below is independent of Lambda.
  predicted_effect:
    - metric: v_cr(X on Y) / v_cr(X on X), same particle X, size-corrected with the law's d^(-1/5)
      direction: same sign as e_Y - e_X
      size: "((e_X + e_Y) / (2 e_X))^0.4 (table below)"
    - metric: d ln v_cr / d ln d at fixed materials (exposed, reported only)
      direction: down
      size: "-0.2 exactly"
    - metric: v_cr on a heated substrate / room-temperature substrate, matched pairs (item B, judged)
      direction: down (particle-only laws Z1, Z2 predict no change)
      size: "((T_m - T_i,hot) / (T_m - T_i,room))^0.4, T_i = (T_p + T_s) / 2 for matched pairs"
  kill_criterion: see "Rule" below (fixed before any v_cr value is read)
  known_relatives:
    - "Schmidt, Gärtner, Assadi, Kreye 2006 (zoo Z2): thermal diffusion explains the size effect; Z2 carries d. Size
      part: likely rediscovery (from memory and the zoo row; the paper's derivation not re-read here)."
    - "Dowding et al. 2020 (zoo Z8): measured v_cr ∝ d^(-n), n ≈ 0.2, explained by jet temperature and spall strength."
    - "Hassani-Gangaraj et al. 2020 (zoo Z9): an impact-mode map for mismatched pairs from both bodies' rho, C0 and
      dynamic yield. Partner-aware, but mechanical; no thermal property of the substrate."
    - "Assadi et al. 2003 (Z1): v_cr from particle rho, T_m, sigma_u and T_i. Particle-only."
    - "Contact temperature of two half-spaces (Carslaw and Jaeger; flash-temperature theory, Blok, Jaeger): textbook."
    - "Differs by: the substrate's effusivity enters v_cr. No zoo member has a substrate thermal property; the
      effusivity-weighted initial interface temperature T_i is also not in Z1/Z2. Label at most 'variant of
      Schmidt 2006 with the substrate as a heat sink'; never 'novel'."
  author: claude (modeller), from Peter's partner-aware idea
```

**What the law leaves out** (stated, not tested):
- substrate deformation and hardness;
- oxide removal and the jetting kinematics (CS-20 / R3);
- rate effects;
- the heated layer's thickness. The surface-flux form assumes it is ≪ R.

Mechanical partner effects (Z9) and thermal ones can both be present. This hunch only claims that the thermal one is
visible in the sign of v_cr changes between substrates.

## Predictions (sourced properties, 2026-11-28)

Effusivity e = √(k ρ c_p) [J m⁻² K⁻¹ s⁻½]: Al 23 957, Cu 37 173, Ni 18 965, Ti 7 187, Sn 10 528.
- ρ from the P-H20 rows.
- k and c_p from the P-WP rows (`properties.csv`, Wikipedia element infoboxes, added 2026-11-28; c_p = molar heat
  capacity / standard atomic weight). They agree with P-HG for Al, Cu and Ni c_p to the printed digit.
- The values computed from memory before the sourcing differed by under 0.3 %; no prediction changed beyond the third
  digit (Ti on Cu 1.571 → 1.569).

**Item A, judged (the mismatched pairs of H20; v_cr(X on Y) / v_cr(X on X)):**

| Particle on substrate | Predicted ratio | Predicted sign of the change |
|---|---|---|
| Al on Cu | 1.10 | + |
| Al on Ni | 0.96 | − |
| Al on Ti | 0.84 | − |
| Cu on Al | 0.93 | − |
| Cu on Ti | 0.81 | − |
| Ti on Cu | **1.57** | + |

Ordering for Al particles: Ti < Ni < Al < Cu substrate. This is not the order of substrate hardness, and it puts the
soft, conductive Cu above the hard, insulating Ti.

**Item B, judged (matched pairs on a heated substrate, CH rows against the authors' quoted room-temperature
values):**

| Pair | Particle / substrate temperature | Predicted v_cr change against room temperature |
|---|---|---|
| Al on Al | 292 / 364 K | −2.3 % |
| Sn on Sn | 292 / 364 K | −7.1 % |
| Ti on Ti | 292 / 348 K | −0.7 % |

Z1 and Z2 predict 0 for all three, since the particle temperature is unchanged.

**Reported only (exposed or confounded):**
- Size (DW rows): v_cr(39.4 µm) / v_cr(10.3 µm) = 0.765 for Al; v_cr(24.9 µm) / v_cr(6.9 µm) = 0.774 for Ti.
- The absolute values of the 11 matched materials with Λ fitted on one row, against zoo Z6.

## Rule (fixed now; applied once, after the freeze)

### Item A (the H20 mismatched pairs)

1. **Unit.** For each of the six pairs, the observed ratio r_obs = v_cr,mid(X on Y) / v_cr,mid(X on X), with both rows
   from H20. Correct for size with the law's own (d_XY / d_XX)^(1/5), using the `d_um` column.
2. **Resolved.** A pair is resolved if |ln r_obs| exceeds the combined half-width of the two windows,
   ln(v_high / v_low) / 2 summed over both rows. Otherwise it is unresolved and not counted.
3. **Score.** For each resolved pair, agree if sign(ln r_obs) = sign(e_Y − e_X); otherwise disagree.
4. **Verdict A:**
   - **supported (post hoc):** at least 4 resolved pairs, and agreements ≥ 2 × disagreements;
   - **refuted:** disagreements ≥ agreements among the resolved pairs;
   - **undetermined:** otherwise, including fewer than 4 resolved pairs.

### Item B (CH heated substrates, matched)

1. **Unit:** r_obs = v_cr(CH row) / v_cr(room temperature, as quoted in the row's notes). For Al, correct for size
   with (15.5 / 14.4)^(1/5). Sn and Ti quote no size, so they are not corrected.
2. **Resolved** if |ln r_obs| exceeds the CH row's printed relative uncertainty plus 0.02. The 0.02 is H20's stated
   velocity uncertainty, standing in for the quoted room-temperature value, which has no window.
3. **Agree** if r_obs < 1.
4. **Verdict B:**
   - **supported (post hoc):** at least 2 resolved, all agree;
   - **refuted:** at least 1 resolved and disagreements ≥ agreements;
   - **undetermined:** otherwise.

### Overall

Items A and B are reported separately; neither is pooled into the other.
- **Supported:** A supported and B not refuted.
- **Refuted:** A refuted.
- Otherwise the result is mixed or undetermined, stated as it is.
5. **Reported with the verdict, not judged:**
   - ln r_obs against the predicted ln ratio for every pair;
   - the same sign test with the substrate's dynamic yield strength in place of effusivity (`Yd_micro_MPa` of the
     P-H20 rows), as a mechanical comparator;
   - the size and heated-substrate items above.

Before the freeze, the effusivity values are sourced and the predicted table recomputed. If a predicted sign flips
(possible only for Al on Ni, which lies 4 % from 1), the frozen table is the recomputed one.

## Author's prediction (judgment, before any v_cr value is read)

- Item A: supported 0.25, refuted 0.40, undetermined 0.35.
- Item B: supported 0.20, refuted 0.15, undetermined 0.65. The predicted shifts are small against the windows; Sn
  (−7 %) is the only one likely to be resolved.
- Why not higher: mechanical mismatch (Z9) probably dominates the pair differences. Al on Ni lies close to 1. Hassani
  2020 framed its results mechanically. A thermal sink that matters for the size effect may still be too weak to
  show between substrates within LIPIT's ±2 % windows.
- Ti on Cu (+57 % predicted) carries most of the weight. If it goes the other way, the hunch is close to refuted on
  its own.

## What follows (stated now)

- **Supported (post hoc):** the substrate-effusivity effect becomes a measurement item for a new data request: the same
  particle on substrates of equal hardness but different effusivity. A solver form (a sub-grid pair conduction term
  in the TLSPH contact) is only drafted after that, with Peter.
- **Refuted:** recorded as a negative result. The thermal reading of partner awareness is closed at the R1 level; the
  size effect stays with Z2/Z8.
- **Undetermined:** parked with CS-20, waiting for an unseen substrate series.

## Before the freeze (checklist)

1. ~~Source k and c_p; recompute.~~ Done 2026-11-28 (above).
2. ~~Peter: rule 1 waiver.~~ Waived 2026-11-28 (DECISIONS).
3. **Moved to after the freeze:** the literature step. It means reading Schmidt et al. 2006's derivation and searching
   for any substrate-thermal-property effect on v_cr. A search on that topic would likely surface Hassani 2020's pair
   results, which are item A's data. The step sets only the label, not the prediction, so it runs after the freeze
   and before the verdict is labelled.
4. Facts check (coldspray-procedure.md): no solver output is read. The inputs are `vcr_lipit.csv` columns
   (`vcr_low_mps`, `vcr_high_mps`, `vcr_mid_mps`, `d_um`, `particle`, `substrate`, `T_substrate_K`) and
   `properties.csv` columns. Not covered: the k and c_p entries, which are newly sourced (2026-11-28) and never read/used before in a judged item.
