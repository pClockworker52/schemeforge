# Cold spray: hunch CS-18 (Total Lagrangian SPH bodies carry an accurate surface layer): DRAFT, awaiting Peter

Drafted 2026-11-12 by the modeller. Direction: Peter (DECISIONS 2026-11-12: TLSPH directly in the fork).
- **Not registered.** It is frozen together with its ladder ([sph-tlsph-ladder-draft.md](sph-tlsph-ladder-draft.md))
  in one commit, before the first TLSPH run.
- **Research track,** a method hunch like CS-11 and CS-13. It is judged on exact references, not on blind data.
- **Budget:** registered, it makes the count 4 of 5. It discriminates on obtainable data: the exact references of
  its ladder.

```yaml
- id: CS-18
  registered: draft 2026-11-12 (not frozen)
  assumption_broken: >-
    H8 at the level of the body formulation. Milestone 1 of sph-hvi-contact showed that collocated SPH bodies with
    Eulerian kernels cannot carry an accurate surface layer: kernel truncation at the body surface (B-2
    checkerboard) and the tensile instability (D-1). The solver's own repairs (order 1, xi) fail the host rungs
    (opencourant-verification.md §14, §15). The assumption broken is that a body discretisation with Eulerian kernels
    is adequate for interface quantities.
  statement: >-
    Particle and substrate as Total Lagrangian SPH bodies have three properties: kernels and corrected
    (first-order consistent) gradients evaluated in the reference configuration; a fixed neighbourhood per body, so
    there is no kernel coupling across bodies; and hourglass control. Combined with the existing hvi contact and
    bond laws (ported, unchanged in form), they pass, at the same spacings, the rungs the collocated form failed:
    the host rungs with numeric thresholds, the exact tension wave, Hertz contact (B-2, B-3) and the bonded bar
    (D-1).
  mechanism: >-
    Corrected reference gradients restore first-order consistency at free surfaces, which removes the
    truncated-sum error of the interface layer. With reference kernels no particle moves through another's support
    in the kernel sense, so the tensile instability of Eulerian kernels is absent. Bodies are separate by
    construction, so the body filter and its artificial surfaces are not needed.
  predicted_effect:
    - {metric: "T-host S0, S0p, S1", direction: "pass", size: "frozen thresholds of the TLSPH ladder"}
    - {metric: "T-tension (welded TLSPH bar vs exact)", direction: "pass", size: "max deviation <= 0.05 V"}
    - {metric: "B-2, B-3, D-1 with ported hvi laws", direction: "pass", size: "frozen ladder thresholds"}
    - {metric: "T-large-strain", direction: "reported", size: "decides whether a reference update is needed"}
  kill_criterion: >-
    Refuted if any of T-host, T-tension or T-zero-energy fails at its frozen threshold in the frozen set-up.
    Supported if every core rung of the TLSPH ladder passes. Inconclusive if a core rung cannot be run, for
    example because the implementation is unfinished. A failing contact rung (B-2, B-3, D-1) with all host and
    tension rungs passing refutes the claim that the body formulation was the only cause. It is recorded as such and
    is not tuned. Separately, the formulation is refuted for cold-spray use without a reference update if
    T-survival fails (Al-Al, 800 m/s, R/16 and R/32, survival checks). The elastic part of the claim is judged on
    its own rungs and stands or falls independently.
  parameters: >-
    Kernel, h, hourglass coefficient and reference-update rule are fixed once in the ladder's freeze commit. They
    are not varied per rung.
  known_relatives:
    - Profizi, Combescure & Ogawa 2016 (C. R. Mecanique 344, 211-224) and Profizi's thesis (INSA Lyon 2016), read at
      F level (data/profizi2016_reading.md). Shared: TLSPH with a first-order (Belytschko 2000) correction, bodies
      separated with a pair contact between them, an energy-limited cohesive pair law with an activation criterion,
      Al-on-Al cold spray. Different here: hourglass control (alpha = 10), penalty contact with surface normals
      instead of pinballs with Lagrange multipliers, Bay-type activation instead of a yield-drop criterion, and
      verification against exact references (none in Profizi)
    - Vignjevic, Reveles & Campbell 2006 (TLSPH, first-order consistency); Bonet & Kulasegaram (Lagrangian SPH)
    - Ganzenmueller 2015 (hourglass control for TLSPH)
    - LAMMPS SMD/MACHDYN (open TLSPH with smd/hertz contact between bodies)
    - updated-reference Lagrangian SPH (Gil, Lee et al. 2022); stabilised TLSPH with configuration update
      (arXiv:1907.06990)
  provenance: fork analysis hvi/ANALYSIS-2026-11-12.md section 3; Peter's direction 2026-11-12
  label: none yet (referee); expected at most "variant of Profizi et al. 2016"
  status: draft
  author: Peter (direction), claude (formulation)
```

## Author's prediction (judgment, recorded 2026-11-12, before any TLSPH code)

- The elastic host rungs (T-S0, T-S0p, T-S1), T-tension and T-zero-energy: **likely to pass.** The correction and
  the reference kernels address both roots of milestone 1. The dispersion of the stencil (2.8 % slow at 16 particles
  per wavelength, SPEC-TL §3.5) makes the 1 % S0 thresholds the tightest of these.
- T-B2 and T-B3: **uncertain, leaning pass.** The surface layer is first-order consistent, but the colour normal and
  the radial gap are unchanged.
- T-survival at R/32, 800 m/s: **uncertain, leaning fail.** Profizi's evidence, and the hourglass control is nearly
  off in plastic zones (SPEC-TL §3.5 item 5).

## Risks named before any run

1. **The reference update at jetting strains** (literature check, claim 3). Without an update, TLSPH cannot follow
   large distortion. With one, zero-energy modes tend to return.
   - Profizi's TLSPH without an update failed on finer meshes at high speed: 600–900 m/s at R/12.5 and finer, from a
     time-step collapse with particles "fleeing" the contact zone (thesis p. 70). The author concludes that the model
     lacks "consistency and stability at very high impact speeds mostly due to the total Lagrangian nature" and that
     updated Lagrangian should be considered (p. 87).
   - The early rung T-survival (Peter, 2026-11-12) tests this before the bond work.
2. **Hourglass control is a new parameter.** It is fixed once at the freeze, and T-zero-energy tests it.
3. **Effort.** TLSPH is a new element formulation in the solver, not a switch. Peter decided against a prototype
   first, so the first exact-reference evidence comes only after the solver implementation runs.
4. **Exposure.** The B-2, B-3 and D-1 failure modes of the collocated form are known. The ladder keeps their
   thresholds unchanged, so this knowledge cannot be used to choose thresholds.
