# Cold spray: hunch CS-14 (simulate the blanket alone in a small cell), registration (frozen)

Drafted 2026-11-05. Idea and content: Peter. **Status: frozen** 2026-11-05, approved by Peter with review notes 1, 2,
4 and 5 folded in. This commit comes before any run. Research track, not a ledger arena. Background: CS-12 (coldspray-hunch-cs12.md), Zhang & Bay
1997 (coldspray-reading-zhangbay1997.md), Na2025 / Z18 (coldspray-zoo-z18.md).

## Hunch (Peter's text, with review notes 1, 2, 4, 5 folded in)

```yaml
- id: CS-14
  registered: 2026-11-05, frozen 2026-11-05 (approved by Peter)
  assumption_broken: >-
    That the interface law has to be fitted to v_cr. Here it is derived from the oxide mechanics.
  statement: >-
    Don't simulate the impact; simulate the blanket alone in a small cell. A patch about 1 um wide of native oxide,
    resolved at nanometre scale as bonded DEM grains on a metal substrate, is loaded with prescribed histories of
    surface stretch Y and normal pressure p (from the bulk simulation or from analytic estimates). Outputs: the
    fragment geometry (t/w), the threshold stretch Y' and the extrusion pressure p_E, each as a function of oxide
    thickness.
  length_scales: >-
    (note 1) With t and w as the only lengths, w ∝ t follows from dimensional analysis, so a constant t/w would be
    trivial. The cell therefore contains these additional lengths, each a fixed value across the 5-25 nm sweep:
    the DEM grain size d_g (nanometre scale), the cohesive length of the oxide-metal interface, the plastic length
    of the metal substrate (from its flow stress and modulus), and the cell width (about 1 um). Their values are
    set and recorded in the rung commit, before the thickness sweep, and are not changed afterwards.
  mechanism_split: >-
    (note 5) In Zhang & Bay 1997, Y' belongs to the thin-film mechanism (threshold, no extrusion pressure) and
    t/w and p_E to the cover-layer mechanism (no threshold, extrusion through cracks). The outputs are read
    accordingly: t/w and p_E decide the cover-layer reading; Y' decides the film reading. Each is reported
    separately against the prediction.
  mechanism: >-
    A brittle film on a stretched substrate cracks into fragments, and fresh metal extrudes through the gaps
    (Zhang & Bay 1997). If the crack spacing scales with film thickness, t/w stays constant and thickness drops out.
  predicted_effect:
    - {metric: "t/w, Y' and p_E over oxide thickness 5-25 nm at fixed oxide type", direction: same,
       size: "within +-10 %"}
  consequence: >-
    (note 2) Supports the mechanism of CS-12(c). T3, a v_cr measurement, remains the decisive test between CS-12,
    CS-10 and Z18.
  kill_criterion: >-
    Refuted if t/w or p_E changes by more than 25 % over 5-25 nm. Inconclusive if the rung fails.
  rung_first: >-
    Fragmentation of a brittle film on a stretched substrate, compared with shear-lag theory or published
    experiments (crack spacing against film thickness). This also covers the metric rule.
  open:
    - Grain-bond strength of the oxide at about 1e9 /s; only Lienhard's 870 MPa is available (via Na2025).
    - A thin amorphous oxide may be ductile rather than brittle.
    - (note 4) The oxide-metal interface strength: shear-lag fragmentation assumes the film stays bonded; if it
      delaminates instead, the fragment pattern changes. No sourced value.
  known_relatives:
    - bonded-particle models (Potyondy & Cundall)
    - shear-lag film fragmentation
    - Zhang & Bay 1997
    - Rahmati 2021
  label: none yet (referee)
  status: open
  author: Peter
```

## Review notes (claude; notes 1, 2, 4, 5 accepted and folded in above; 3, 6, 7, 8 not adopted, kept for the record)

1. **The prediction is almost guaranteed unless the cell has a second length scale.** If the only lengths in the
   problem are the oxide thickness t and the fragment width w, dimensional analysis forces w ∝ t, so t/w is constant
   by construction. The classic shear-lag result (crack spacing ∝ t · σ_f / τ_i) has the same property. A
   deviation can only come from an additional length:
   - the DEM grain size (physical for a crystalline oxide; a numerical choice for an amorphous one);
   - the plastic zone of the metal beneath;
   - the cohesive length of the oxide–metal interface;
   - the 1 µm cell width.

   **Suggestion:** the frozen version names which of these lengths the cell contains, with values. Otherwise a
   supported result tests the discretisation, not the oxide. At 5 nm thickness and nanometre grains, the film is only
   about five grains thick, so discreteness effects are likely at the thin end.
2. **Y' may depend on thickness through strength, not geometry.** In shear-lag theory the onset of cracking is set by
   the film's fracture strain, which is thickness-independent in the simple theory. Measured fracture strength of
   thin films often rises as thickness falls, though. If the grain-bond strength is held fixed across 5–25 nm, the
   cell cannot show that effect. Holding it fixed is a choice worth stating.
3. **A missing parameter: the oxide–metal interface strength.** Shear-lag fragmentation assumes the film stays bonded
   to the substrate. If it delaminates instead (Tiamiyu 2022 reports delamination below v_cr, as far as that leak
   tells), the fragment pattern changes. The cell needs an interface strength, and there is no sourced value. That
   belongs in "open" next to the grain-bond strength.
4. **Which of Zhang & Bay's mechanisms the cell represents.** p_E belongs to the cover-layer mechanism; Y' belongs
   to the film mechanism, which has no extrusion pressure (Eqs. 10, 11). The cell can output both, but the
   prediction treats them together. Stating which output decides which mechanism avoids a mixed reading later.
5. **Evidence level of a supported result.** A supported CS-14 supports the *mechanism* behind CS-12(c). It does not
   decide T3, which is a v_cr measurement. CS-10, Z18 and CS-12 are judged there. Suggested wording for the
   consequence: "supports the mechanism of CS-12(c); T3 remains the decisive test".
6. **Loading histories.** The bulk simulations fail at the contact edge (§8, §10), which is exactly where the
   stretch history matters. Analytic estimates are the practical source. Their form, and the rate (about 10⁹/s),
   should be fixed in the frozen protocol.
7. **Tool and priority.** OpenCourant has no DEM. This would be our own code (JAX), a new build with its own rungs.
   It fits plan revision 2, step 2 (interface-law hunches), but it is simulation work while the priority decision of
   2026-11-05 puts the data side first. Your call whether it starts now or waits for B14, B06, B05.
8. **The rung is good, with one caveat.** Published crack-spacing data for oxide films on metals are mostly
   quasi-static. A pass at low rate does not cover 10⁹/s, so the rung verifies the cell, not the rate dependence.
