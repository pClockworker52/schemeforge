# Open v_cr table (single-particle impact, LIPIT)

`vcr_lipit.csv` collects critical adhesion velocities of metallic microparticles measured one impact at a time
with the laser-induced particle impact test (LIPIT). It is step 1 of the "discipline only" plan in
[../coldspray-go-nogo.md](../coldspray-go-nogo.md). It is a literature table, not a judge. No search runs on
it, and nothing here is held out. Source keys refer to the register in
[../coldspray-data-and-zoo.md](../coldspray-data-and-zoo.md).

Version 0.1, 2026-11-03. Built only from full texts read in this track (evidence level F).

## What is in it

41 rows, 38 with a numeric window:

| Prefix | Source | Rows | What |
|---|---|---|---|
| H20 | Hassani2020 Table 1 (accepted manuscript) | 20 (16 numeric, 4 NA) | 9 mismatched and 11 matched pairs, ~10–15 µm, room temperature, polished substrates; velocity uncertainty 2 % |
| DW | Dowding2020 Fig. 6 | 9 | Size series: Al 10.3–39.4 µm, Ti 6.9–24.9 µm, matched |
| CH | Chaban2021 p. 2 | 3 | Heated substrates: Al and Sn at 364 K, Ti at 348 K; particles at 292 K |
| PA | Panova2026b Table 1 | 3 | Cu on polished plate, polished sprayed Cu, rough sprayed Cu (growth surface) |
| Q | Secondary quotes | 6 | Values that later papers attribute to the same primary sources as H20 rows, but which differ from them (see below) |

Distinct matched materials: 11 (Al, Cu, Ni, Ti, Zn, Au, Ag, Sn, Al 6061, Al 2024, Al 7075).

## Columns

| Column | Meaning |
|---|---|
| `id` | Row id, prefix = source |
| `particle`, `substrate` | Material names as printed |
| `particle_condition`, `substrate_condition` | Only what the source states; blank = not stated in the text I read |
| `d_um`, `d_um_spread` | Particle diameter (µm) and its spread as printed (± value or sieve range) |
| `T_substrate_K` | Substrate temperature; "room" = not heated |
| `vcr_low_mps`, `vcr_high_mps` | Lower and upper bound of the critical-velocity window (m/s) |
| `vcr_mid_mps` | Midpoint (m/s); for DW, CH and PA this is the authors' v_cr |
| `vcr_definition` | How the source defines the window (they differ, see below) |
| `n_impacts` | Number of impacts behind the value, where printed |
| `regime` | Impact mode as classified by Hassani2020 (splatting, co-deformation, penetration); matched pairs are co-deformation |
| `read_from` | Exactly where I read the number |
| `primary_source` | The paper that measured it |
| `extraction` | `printed`, `printed (quote of primary)`, `digitized (+-5 m/s)` or `quote of primary` |
| `notes` | Caveats |

## Caveats a judge would have to handle

1. **Definitions differ.** H20 and DW use the smallest velocity window containing equal numbers of bonded and
   rebounded impacts. PA averages the last two rebounds and the first two bonds. CH prints value ± uncertainty.
   The windows are therefore not directly comparable uncertainties.
2. **Digitized rows.** The DW values exist only as a plot. I read them from Fig. 6 at 400 dpi with a
   log-axis calibration checked against the 700–1000 m/s ticks (within 0.5 px). Reading error about ±5 m/s,
   small against the 30–110 m/s windows. Ti 15.3 µm: the window is hidden inside the marker, so its bounds
   are the marker's extent.
3. **Conflicting quotes of the same primary paper.** Hassani2020 quotes HG2018b as Al 790–835, Ni 620–675 and
   Zn 520–570 m/s. Panova2026b quotes the same paper as 797–824, 650–660 and 518–523. Dowding2020 quotes it
   as Al 810 ± 16 (14 µm) and 770 ± 15 (30 µm). For Au, Hassani2020 gives 260–275 at 14 ± 4 µm, while Reiser2024
   gives 253 ± 7 at 16 ± 4 µm, both from HG2019b. The preprint of HG2018a (arXiv 1612.08081) gives Al 825 at 14 µm
   and 775 at 30 µm. These rows stay flagged until checked against the primaries (HG2018b *Scripta* 145,
   HG2019b *Appl. Surf. Sci.* 476).
4. **Possible duplicates.** DW, CH (room-temperature comparisons) and H20 may reuse impacts from the same group's
   earlier campaigns, so rows are not necessarily independent measurements.
5. **Quantity.** These are single impacts on polished (or prepared) substrates, mostly at room temperature,
   with no carrier gas. They are not process critical velocities (see the data note, "the key caveat for a
   judge").

## Not yet in the table

Known sources with values I have only at abstract or second-hand level, or not at all:
- Tang2025 (Al 800 m/s, abstract only);
- Imbriglio2019 (Ti on alumina, ~580 m/s, second-hand);
- Lienhard2020 (Al oxide states, +14 %);
- the primaries HG2018b and HG2019b;
- Lucas2024 and Lucas2025 (Cu microstructure, substrate strength and ductility);
- Na2025 (powder heat treatment);
- Tiamiyu2021; Sun2020 (Cu);
- the 2024 bulk-metallic-glass study (OSTI 2377827).

Material properties for the models (B, ρ, σ, c_p, T_m) are not part of this table. They need their own sourced
table before any zoo member is evaluated.

## Licence

The numbers are factual measurements from the cited papers, which remain the authority. Cite the primary source
for any use. The table itself is part of this repository (GPL-3.0-or-later).

---

# Material properties (`properties.csv`)

Version 0.1, 2026-11-03. Inputs that zoo members need (Z1: ρ, T_m, σ_u; Z2: σ_TS, ρ, c_p, T_m; Z6: B, ρ; Z7:
C₀, B, dynamic σ_y, ε; Z9: ρ, C₀, Y_d). The table is incomplete on purpose: nothing is filled from memory.

| Prefix | Source | Materials | Fields |
|---|---|---|---|
| P-HG | HG2018a preprint, Extended Data Table 1 (F) | Cu, Ni, Al, Ta | ρ, c_p, T_m, B, G, ν, C₀, Hugoniot s, Johnson–Cook A, B, n, C, m |
| P-WP | Wikipedia element infoboxes, retrieved 2026-11-03 (tertiary; densities cite Arblaster 2018) | Al, Cu, Ni, Ti, Zn, Sn, Ag, Au, W, Ta, Fe | ρ, T_m, molar C_p, B, G |

**Missing, and needed before any zoo member is evaluated:**
- Strength data (σ_u or σ_TS, dynamic σ_y, failure strain ε) for every material.
- Everything for the Al alloys 6061, 2024 and 7075.
- Specific heat c_p for the P-WP rows. Converting molar C_p needs standard atomic weights; the Wikipedia
  lookup was rate-limited, and I did not fill them from memory.
- Hugoniot intercepts C₀ and slopes s. Hassani2020 takes these from Hugoniot data and estimates dynamic yield
  strengths from restitution data, both in its supplementary information. That file was not in the accepted
  manuscript and is the most valuable missing source, because it matches the v_cr table's own materials.

**The property source changes predictions.** Cu density is 8960 (P-HG) against 8935 kg/m³ (P-WP), and the
"C₀" in P-HG is sqrt(B/ρ), not a Hugoniot intercept. Strength values depend on temper and on how they were
measured. The property source must therefore be fixed as part of pre-registration, before predictions are made
(go/no-go note, step 2), and never chosen after seeing results.
