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
[coldspray-hunch-cs13b.md](coldspray-hunch-cs13b.md).
