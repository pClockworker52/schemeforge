# Cold spray: open hunches for the blind set

Registered before any blind measurement exists. Each must be tested on materials or conditions measured after
its registration, never on the rows of `data/vcr_lipit.csv` v0.1, which inspired it. Ledger format as in
`ledger/schema.yaml`; research track, not a ledger arena. Assumption numbers refer to the inventory in
[coldspray-go-nogo.md](coldspray-go-nogo.md).

```yaml
- id: CS-07
  registered: 2026-11-03
  assumption_broken: H4 (oxide enters as a thickness at most) and the clean-surface assumption of Z6
  statement: >-
    Part of v_cr is the cost of fracturing and expelling the native oxide. A sound-speed law fitted on
    oxide-forming metals therefore over-predicts v_cr for metals without a native oxide, and for one metal
    v_cr rises with oxide thickness.
  mechanism: >-
    Bonding needs fresh metal contact. Jetting must strain the interface past the oxide's fracture strain and
    sweep the fragments out of the contact (Hassani/Schuh view; oxide left at the crater centre per
    Ichikawa2019). An oxide-free surface needs less jet strain, so a lower impact velocity, than Z6 (which
    absorbs an average oxide penalty from Al, Cu, Ni, Zn) implies. A thicker or tougher oxide needs more.
  predicted_effect:
    - {metric: "residual r = (v_meas - v_Z6_a015) / v_Z6_a015 on blind matched metals", direction: down,
       size: "r(oxide-free metals) below the median r of oxide-forming metals by more than the median window width"}
    - {metric: "v_cr of one metal across controlled oxide states", direction: up,
       size: "monotone in oxide thickness, step larger than the window width"}
  kill_criterion: >-
    Refuted if, on the blind set, oxide-free metals do not have lower residuals than the median of
    oxide-forming metals (difference smaller than the median window width), or if a same-metal oxide series
    of at least three states shows no monotone increase beyond the window widths. Inconclusive if fewer than
    two oxide-free metals or no oxide series are measured.
  known_relatives:
    - HG2019b (Al, Ag, Au; role of native oxide). It makes this argument itself: Au and Ag lie ~50 % and ~30 %
      below Zn at similar bulk sound speed, and Cu process v_cr drops by up to ~50 % below 2-3 nm oxide
      (its Table 1). CS-07 is a variant of HG2019b; its added value is the quantitative kill test on blind data.
    - Lienhard2020 (Al, +2-3 nm hydroxide, about +14 % v_cr)
    - Ren2024 (peridynamics, oxide thickness raises v_cr)
    - Ichikawa2015, Ichikawa2019 (substrate oxide, oxide at the crater centre)
    - Tang2024 (oxide form sets local bond strength)
  provenance: >-
    Inspired by retrospective test v1 (Z6 over-predicts Au, Ag, Sn). Au is stated as oxide-free in Veysset2021.
    The oxide state of Ag and Sn is not reported in the sources read, and Sn competes with melting, so v1
    cannot confirm this hunch.
  needs: an oxide-state column filled from primaries (HG2019b; authors) and, ideally, an oxide series for one
    or two metals besides Al.
  label: variant of HG2019b (label set 2026-11-03 after reading HG2019b; referee to confirm)
  status: open
  results: B10 (2026-11-04) not refuted (direction agrees), support undetermined; see coldspray-results-b10.md
  author: claude (with Peter)
```

CS-08 and CS-09 are in [coldspray-preregistration-b10.md](coldspray-preregistration-b10.md). CS-10 (combined
strength + oxide energy balance, registered 2026-11-04) is in [coldspray-hunch-cs10.md](coldspray-hunch-cs10.md).
CS-11 (interface bracket; frozen; inconclusive, DECISIONS 2026-11-05; see opencourant-verification.md §10.6) is in
[coldspray-hunch-cs11.md](coldspray-hunch-cs11.md). Frozen 2026-11-05: CS-12 (bonding as local dissolution of
the interface blanket, criterion: surface expansion) in [coldspray-hunch-cs12.md](coldspray-hunch-cs12.md), and
CS-13 (heat conduction gives the contact edge its length scale) in [coldspray-hunch-cs13.md](coldspray-hunch-cs13.md).
CS-13b (protocol amendment of CS-13: 3D setup F with conduction, after H0 failed on 2D quads) is frozen (2026-11-05) in
[coldspray-hunch-cs13b.md](coldspray-hunch-cs13b.md); blocked before its runs, no verdict
(opencourant-verification.md §12). CS-13c (brick particle on brick substrate, k = 0 twin) is frozen (2026-11-05) in
[coldspray-hunch-cs13c.md](coldspray-hunch-cs13c.md).

## Labels after the literature search (2026-11-05)

Source: docs/research/coldspray-literature-interface.md (external AI; many claims S-level). Proposed labels, for the
referee to confirm; the frozen hunch files are not edited.

| Hunch | Proposed label | Closest relatives | Note |
|---|---|---|---|
| CS-10 | relative of Na2025 Eq. 6 and Lienhard2020 (both superpose strength and oxide); not the same form | Na2025 (F), Lienhard2020 (B14, via Na2025) | Read 2026-11-05 (coldspray-reading-na2025.md): Na/Lienhard put the oxide into the **jet** strength (t₀/t, t ≈ 100 nm jet thickness, linear in V); CS-10 into shell work (t_ox/d, quadratic). The external report's "t_ox/d_p" description of Lienhard was wrong. For T3 (Al 6061, 17 → 25 nm): Na Eq. 6 ≈ +126 m/s, CS-10 ≈ +37 m/s, CS-12 0. |
| CS-12 | variant of Bay (cold pressure welding) applied to cold spray | Bay 1979/1983; Kebriaei, Vladimirov & Reese 2014 (FE interface element with Bay-evolving cohesive strength, roll bonding); Rahmati 2021 (explicit oxide shell + cohesive contact in cold spray) | Markov-blanket framing not found in prior art; it adds no testable content beyond (b), (c). **T1 is exposed** (ring pattern documented) and was never discriminating; only T3 and T2 remain. Read 2026-11-05: Zhang & Bay 1997 (F; coldspray-reading-zhangbay1997.md). CS-12(b) merges Bay's two mechanisms (thin film: threshold Y', no p_E; cover layer: no threshold, p_E(t/w, G, Y)), so it is a hybrid; thickness enters only through t/w in the cover-layer extrusion term. Bay 1983 itself not read. |
| CS-13 (13b, 13c) | rediscovery (thermal regularisation of adiabatic shear bands) | Needleman 1988, Batra & Kim 1991, Grady & Kipp 1987 | Prior evidence for the counter-mechanism: HG2018a shows jetting without thermal softening; Li 2006 (S) reports Lagrangian distortion persisting with conduction. Expect CS-13c refuted or inconclusive. |
| Idea C (explosive welding, not registered) | rediscovery | HG2018a (Walsh kinematics applied to the sphere), Grujicic 2003 | New lead: Deribas' lower limit V ≥ k₁ √(H_V/ρ), k₁ 0.6–1.2 by surface cleanliness, a candidate closed-form zoo member (strength-based; B10 refuted strength alone). |
| Idea D (rebound, not registered) | rediscovery | Wu 2006, HG2017 (PRL), Tiamiyu 2022, Tang 2025 (PNAS, open SI) | Data lead: restitution curves in HG2017 and Tang 2025 SI. |

To check before relying on them: Assadi 2003's reported conduction comparison (we have the full text), the Grady–Kipp
formula (plugging Al values gives a centimetre-scale width), the Kebriaei citation.

CS-14 (Peter: simulate the interface blanket alone in a small DEM cell; t/w, Y', p_E against oxide thickness) is
frozen (2026-11-05) in [coldspray-hunch-cs14.md](coldspray-hunch-cs14.md), with review notes.
CS-14b (method amendment and clarification of CS-14: CS-14 is a nanometre-scale interface submodel, not the
whole-particle model; the oxide becomes a continuum film with cohesive cracks instead of DEM) is frozen
(2026-11-05) in [coldspray-hunch-cs14b.md](coldspray-hunch-cs14b.md).
CS-13c result (2026-11-05, opencourant-verification.md §13): **refuted** by both clauses of its frozen rule. The thermal
question in OpenCourant is closed (stop rule, DECISIONS 2026-11-05).
