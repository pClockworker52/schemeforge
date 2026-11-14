# Cold spray: hunch CS-18b (calibrated TLSPH bodies with boundary-consistent traction), registration (frozen)

Drafted 2026-11-14 by the modeller, from the calibration in opencourant-verification.md §18 and §19 and Peter's
decisions (DECISIONS 2026-11-13 and 2026-11-14).
- **Registered and frozen 2026-11-14** together with its ladder ([sph-tlsph-b-ladder.md](sph-tlsph-b-ladder.md)), in
  one commit, before any CS-18b rung run. Peter approved; the T-tension limit of 0.095 V has its source noted in the
  ladder.
- **A new hunch, not an amendment of CS-18.** CS-18 stays refuted at T-S0
  ([coldspray-hunch-cs18.md](coldspray-hunch-cs18.md)).
- **Budget:** it makes the count 4 of 5.

```yaml
- id: CS-18b
  registered: 2026-11-14, frozen 2026-11-14 with its ladder
  assumption_broken: >-
    H8 at the level of the body formulation, as CS-18: collocated SPH bodies with Eulerian kernels cannot carry an
    accurate surface layer. CS-18 showed that a corrected TLSPH form alone also loads its end layers wrongly
    (0.655 / 0.845 of the true stress, §17) and that its first ladder judged an uncalibrated viscosity against a
    linear reference (§17, §18).
  statement: >-
    TLSPH bodies as in CS-18 (reference kernels, first-order corrected gradients, Ganzenmueller force form, no
    reference update), with three changes fixed by calibration on non-rung cases:
    - the LAMMPS SMD TLSPH pair viscosity, Q1 = 0.1, Q2 = 0 (§18.3, §19.4);
    - the hourglass coefficient alpha = 5, with the plastic switch (§19.4);
    - boundary-consistent traction (BCT), which spreads contact and wall loads over the end layers with the reference
      boundary weights, guard 0.45 (§18.4, §19.1, §19.2).
    Carrying the unchanged hvi contact and bond, these bodies pass the CS-18b ladder at its stated spacings, against
    finite-strain references and thresholds calibrated on methods known to work (quad elements, collocated SPH).
  mechanism: >-
    The corrected reference gradients make the bulk first-order consistent. BCT applies normal tractions the way the
    corrected force sum expects, so the end layers carry the traction. Reference kernels avoid the tensile
    instability of Eulerian kernels. The calibrated viscosity removes the excess damping that set most of the CS-18
    rebound error.
  predicted_effect:
    - {metric: "T-host (T-S0, T-S0p, T-S1)", direction: pass, size: "calibrated thresholds of the CS-18b ladder"}
    - {metric: "T-surface (column end layers, flat free surface)", direction: pass, size: "within 3.5 %"}
    - {metric: "T-B2", direction: pass, size: "peak 8.0 %, approach 5.5 %, rebound > 0.9"}
    - {metric: "T-survival (Al-Al, 800 m/s, R/16 and R/32)", direction: pass, size: "survival checks"}
  kill_criterion: >-
    Refuted if any of T-S0, T-S0p, T-S1, T-tension, T-zero-energy or T-surface fails at its frozen threshold.
    Refuted for cold-spray use (without a reference update) if T-survival fails. A failing contact rung (T-B1, T-B2,
    T-B3, T-D1, T-D2) with all body rungs passing is recorded as "the body formulation was not the only cause", and
    is not tuned. Inconclusive if a core rung cannot be run.
  parameters: >-
    All set-up items are fixed in the freeze commit (ladder, section "Set-up"). None are varied per rung.
  known_relatives:
    - CS-18 (same formulation without BCT and with an uncalibrated viscosity; refuted at T-S0)
    - Profizi, Combescure & Ogawa 2016 (TLSPH plus adhesion for cold spray; data/profizi2016_reading.md)
    - Dai et al. 2026 (updated-Lagrangian SPH for cold spray with a bonding pair force; data/bonding_methods_reading.md)
    - Ganzenmueller 2015 and LAMMPS SMD/MACHDYN (hourglass control; the viscosity form)
    - corrected SPH boundary-condition treatments listed by Roethlin, Klippel & Wegener (arXiv:1807.01117, section 4.2;
      the originals not read)
  label: none yet (referee); BCT's weighting is a candidate for review; never "novel"
  status: open
  author: Peter (direction), WSL A (calibration and BCT design), claude (formulation)
```

## Author's prediction (judgment, recorded 2026-11-14, before any CS-18b rung run)

- **Host rungs: likely pass.** The thresholds are 1.25 × the calibration methods' errors, and TL tracked the
  finite-strain references closely in §17 and §18. The weakest point is the T-S0 rebound at 100 particles, which
  depends on the viscosity.
- **T-surface: likely pass on the column and the flat free surface** (static model and column check at 0.9999).
  The conforming sphere is not judged (reported rung, §19.1).
- **T-B2: uncertain.** The sphere's layer-2 deficit under BCT and the colour normals may move the approach.
- **T-survival: likely pass.** The calibration probe passed at both spacings (§19.5), though the time step was still
  falling at R/32.
- **For the record:** the author's CS-18 prediction ("elastic rungs likely pass") was wrong, and the T-survival
  prediction ("leaning fail") was wrong in the calibration probe.

## Known limits, named before the freeze

1. **Conforming-sphere surface:** with BCT, layer 2 stays 26–30 % low (static model, §19.1). It is reported, and a fix
   is a later step (Peter, 2026-11-14). Interface outputs on the particle side carry this caveat.
2. **Engine wall-force output under BCT** is 1.485 × the transmitted force. Rungs read the momentum rate (§19.2).
3. **No TL internal energy:** energy closure is reported only.
4. **BCT guard fallbacks** late in the R/32 survival probe (182 526 particle-cycles after 0.815 D/V), location
   unexamined.
5. **Journal check of the four Ganzenmüller equations** is still deferred; it is required before the first claim.

## Verdict (2026-11-14): refuted at T-S1

Under the frozen kill rule ("refuted if any of T-S0, T-S0p, T-S1, T-tension, T-zero-energy or T-surface fails at its
frozen threshold"), **CS-18b is refuted.** The third core rung, T-S1 (Hertz sphere on a rigid wall, 20 m/s), failed
(opencourant-verification.md §20; fork `tlsph`, binary from clean tree `8188ca5ec`, ladder `6f0786a`; rows
`opencourant/results/tlb_host.csv`, all `binary_state = committed`):

| spacing | contact at 10⁻² | peak | approach | rebound | limits (R/32) |
|---|---|---|---|---|---|
| R/32 | 0.890 (**5.3 %**) | 1.049 (2.3 %) | 0.893 (6.7 %) | **0.860** | contact 3.5 %, peak 5.5 %, approach 7.5 %, rebound ≥ 0.9796 |
| R/16 | numerically unstable: kinetic energy up to 9.0 KE0, force up to 11.9 F_Hertz | | | | |

- **The verdict does not depend on readings of the rule.** Under a "last time above 10⁻²" reading of contact time
  R/32 would meet that criterion (2.9 %), but it fails the rebound under either reading. Whether contact time and peak
  apply at R/16 (the frozen text names resolutions only for approach and rebound) does not matter either.
- **R/64** was still running when §20 was written (interim at 0.86 t_Hertz: KE 0.93 KE0). It cannot change the
  verdict, because R/32 misses point criteria. Its numbers are reported in §20.4 when they arrive.
- **Passed before the failure:** T-A0 (55 of 55 identical), T-S0 (plateau 1.0066, contact time 0.9941, rebound 0.976
  at 200 particles) and T-S0p (errors 0.57 / 1.71 / 0.26 %). T-tension, T-zero-energy, T-surface, the contact rungs
  and T-survival were not run (stop rule).

**Against the author's prediction:** "host rungs: likely pass" was wrong for T-S1. WSL A's own prediction ("FAIL more
likely than not") was right on the verdict, but did not foresee the R/16 instability. This is the second TLSPH host
prediction by the author that was wrong (CS-18: "elastic rungs likely pass").

**Readings, not verdicts** (§20.2; none tested, because a separating run would be tuning after a failure):
- this is the first engine case of BCT under a non-uniform rigid-wall load, which §19.2 named untested; the wall
  scaling is exact only for a uniform load on a flat face;
- the conforming sphere's layer-2 deficit (known limit 1) may add to the softness;
- 26 % of the kinetic energy is lost in an elastic impact; viscous plus hourglass work (0.33 + 0.15 KE0) exceeds the
  loss, so without TL internal energy (known limit 3) the balance cannot be closed;
- the wall contact chatters (20 contact segments at R/32, 83 at R/16).

A rescue with a changed set-up (for example BCT off on wall contact, or a different wall treatment) would be a new
hunch, registered and frozen before its runs. It is not an amendment of CS-18b.
