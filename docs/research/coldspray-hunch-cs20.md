# Cold spray: hunch CS-20 (inner ring radius from the subsonic-edge switch), registration (frozen)

Drafted 2026-11-18 by claude from brainstorm item #1 ([multi-particle-brainstorm-2026-11-18.md](multi-particle-brainstorm-2026-11-18.md)),
narrowed to reduced-route option R3 on Peter's decision (chat 2026-11-18, DECISIONS 2026-11-18).
- **Registered and frozen 2026-11-18**, before anything was compared with ring data.
- **Zero-code:** it uses only the rigid-sphere kinematics already in
  [coldspray-kinematics.md](coldspray-kinematics.md) (`src/schemeforge/research/impact_kinematics.py`). There is no
  solver run and no in-solver bond. The Track B route stays closed (DECISIONS 2026-11-17).
- **Not the in-solver form of brainstorm #1:** the solver's v_edge = da/dt does not converge
  ([driver-check-2026-11-17.md](driver-check-2026-11-17.md) §6.1, 0 of 7 and 0 of 6), so this hunch does not use it.
- **Budget:** this registration makes the count 4 of 5 (CS-21 then makes it 5 of 5). Rule 1 ("discriminates on obtainable
  data"): it discriminates, since CS-12 T1 predicts the opposite direction (below). No unseen ring-map source is
  named. **Peter waived the "obtainable" part on 2026-11-18.**

```yaml
- id: CS-20
  registered: 2026-11-18, frozen 2026-11-18
  assumption_broken: >-
    CS-12's reading that jetting matters only through what it does to the surface stretch Y and pressure p_n at
    the edge. Here jetting onset itself sets where bonding can start.
  statement: >-
    In a single normal impact near and above v_cr, the inner radius r_in of the bonded ring is set by the rigid-
    geometry switch of the contact edge from supersonic to subsonic:
      r_in / R = k * sin(beta_c),  tan(beta_c) = V / c,  i.e. sin(beta_c) = V / sqrt(V^2 + c^2),
    where c is the bulk sound speed sqrt(B/rho) by rule P1 (Table S1; Al 5367 m/s, Cu 3858 m/s), R is the particle
    radius before impact, and r_in is measured on the final interface. k is a single constant shared by all
    materials and velocities (weak form). The strong form is k = 1.
  mechanism: >-
    While the contact edge moves faster than the sound speed, the shock stays attached to it and no material can
    leave ahead of it. No jet forms, and the oxide inside that radius is not swept away (simplified Walsh condition,
    as applied to the sphere by Hassani-Gangaraj et al. 2018). Once the edge is subsonic, the jet removes the film
    and fresh metal can meet. The centre inside the switch radius therefore keeps its oxide and stays unbonded. The
    material at the switch radius is later stretched outward. The weak form assumes that this stretch factor (k) is
    about the same across materials and velocities, so ratios cancel it.
  parameters: "none fitted. k is free in the weak form and cancels in every ratio used by the kill criterion."
  predicted_effect:
    - {metric: "r_in vs V, one material", direction: up,
       size: "r_in(V2)/r_in(V1) = sin(beta_c(V2))/sin(beta_c(V1)); about V2/V1 for V << c (e.g. Al 700 -> 900 m/s: 0.165/0.129 = 1.28)"}
    - {metric: "r_in, Cu vs Al at equal V", direction: up,
       size: "ratio sin(beta_c,Cu)/sin(beta_c,Al); about c_Al/c_Cu = 1.39 for V << c (700 m/s: 0.179/0.129 = 1.38)"}
    - {metric: "strong form, r_in/R", direction: same,
       size: "0.09-0.27 for Al and Cu at 500-1100 m/s (coldspray-kinematics.md table); reported, not decisive"}
  kill_criterion: >-
    On an unseen source (published or measured after 2026-11-18, not used for CS-12 T1) that maps the bonded area
    of single normal splats at two or more velocities of one material spanning at least 20 % in V, or two or more
    materials at matched V (within 5 %), take q = measured r_in ratio / predicted ratio.
    Refuted if r_in does not rise with V (any pair where it falls by more than the source's stated scatter), or if
    q lies outside [0.70, 1.43] for any pair. Supported if every pair has q in [0.85, 1.18]. Inconclusive
    otherwise, and inconclusive if the source reports no r_in or no scatter. The strong form (k = 1) is reported
    against measured r_in/R but cannot refute the weak form. Any comparison with data already seen (the ring maps
    exposed for CS-12 T1, or the spec's ring facts) is labelled post hoc and decides nothing.
  known_relatives:
    - Walsh, Shreffler & Willig 1953 (jetting condition in oblique collisions; simplified form, not read here)
    - Hassani-Gangaraj et al. 2018 (supersonic-to-subsonic edge switch applied to cold spray; via coldspray-kinematics.md)
    - coldspray-kinematics.md and reduced-route option R3 (same geometry; this hunch adds the ring-radius reading)
    - "CS-12 T1 (opposite direction: the unbonded centre shrinks as V rises above v_cr)"
    - "zoo Z6 (v_cr = 0.15 c), read post hoc as a fixed switch angle of 8.5 deg (coldspray-kinematics.md reading 2)"
  label: variant of the Hassani-Gangaraj jetting picture; never "novel"
  status: open
  author: claude (from brainstorm #1), Peter (narrowing and registration)
```

## Author's prediction (judgment, recorded 2026-11-18, before any comparison)

- **Weak form survives an unseen test: 0.25.** The weakest step is constant k. Deformation after the switch is large:
  in TLSPH the pole flattens to A/A₀ ≈ 3.6 (opencourant-verification.md §26), a linear stretch of about 1.9. There is
  no reason for that stretch to be the same at all V/c.
- **Direction (r_in rises with V): 0.4.** CS-12 predicts the opposite, and the rigid estimate overstates the time the
  edge stays supersonic (coldspray-kinematics.md, Limits).
- **An unseen source with r_in at two velocities appears within three months: 0.3.** Without one, CS-20 holds a
  budget slot and cannot be tested. Parking it frees the slot.
