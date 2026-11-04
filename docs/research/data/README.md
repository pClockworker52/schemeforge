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
| P19 | HG2019b p. 7 (primary; supplied by Peter) | 2 | Au 253 ± 7 (16 ± 4 µm), Ag 353 ± 2.5 (13 ± 2 µm) |
| Q | Secondary quotes | 7 | Values that later papers attribute to the same primary sources as H20 rows, but which differ from them (see below) |

Distinct matched materials: 11 (Al, Cu, Ni, Ti, Zn, Au, Ag, Sn, Al 6061, Al 2024, Al 7075).

## Columns

| Column | Meaning |
|---|---|
| `id` | Row id, prefix = source |
| `particle`, `substrate` | Material names as printed |
| `particle_condition`, `substrate_condition` | Only what the source states; blank = not stated in the text I read |
| `oxide_state`, `oxide_source` | Native oxide or passivation state as stated by a source I read in full; "not reported" otherwise (36 of 41 rows, 2026-11-03). Main missing source: HG2019b (Al, Ag, Au native oxide) |
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
   and 775 at 30 µm. Resolved for Au and Ag from the primary HG2019b: Au 253 ± 7 (Reiser's quote is right; H20-14 does not
   contain it), Ag 353 ± 2.5 (inside H20-15). HG2019b quotes Zn as 520 ± 2.5, like Panova2026b and unlike H20-13.
   Al, Ni, Cu still need the primary HG2018b (*Scripta* 145).
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
| P-HG | HG2018a preprint, Extended Data Table 1 (F) | Cu, Ni, Al, Ta | ρ, c_p, T_m, B, G, ν, C₀, Hugoniot s, Grüneisen γ₀, Johnson–Cook A, B, n, C, m, reference strain rate and temperature (γ₀ and the last two added 2026-11-04) |
| P-WP | Wikipedia element infoboxes, retrieved 2026-11-03 (tertiary; densities cite Arblaster 2018) | Al, Cu, Ni, Ti, Zn, Sn, Ag, Au, W, Ta, Fe | ρ, T_m, molar C_p, B, G |
| **P-H20** | **Hassani2020 supplementary information, Table S1** (supplied by Peter; F) | Al, Ni, Cu, W, Ti, Zn, Sn, Au, Ag, Al 6061, Al 2024, Al 7075 | ρ, ν, E, Hugoniot C₀ (from Marsh 1980), macroscale dynamic yield (plate impact, 5 metals, cited), **microscale dynamic yield Y_d ± uncertainty** |

P-H20 is the matched source for the v_cr table: same materials, same group, Y_d at impact conditions. Two flags:
- **Partial circularity.** Microscale Y_d was fitted to the sub-critical rebound data of the same LIPIT
  campaigns (Wu et al. 2005 elastic–perfectly-plastic model, prefactor 0.57 from Sun2020). A model that uses
  Y_d to predict v_cr is therefore not fully independent of the impacts that define v_cr. Pre-registration must
  say whether Y_d is an allowed input, and for a blind material it has to come from impacts below v_cr only.
- **W.** Its Y_d (6900 MPa) is estimated from a macro–micro correlation (Fig. S4), not measured.

**Still missing:**
- Melting point and specific heat for the Al alloys, and c_p for the P-WP rows (atomic weights:
  Wikipedia rate-limited the lookup; nothing filled from memory).
- Hugoniot slope s, except for Cu, Ni, Al and Ta (P-HG).
- Tensile strength σ_TS / σ_u (Z1, Z2) and failure strain ε (Z7) for the impact-tested powders.

**The property source changes predictions.** Cu density is 8960 (P-HG) against 8935 kg/m³ (P-WP), and the
"C₀" in P-HG is sqrt(B/ρ), not a Hugoniot intercept. Strength values depend on temper and on how they were
measured. The property source must therefore be fixed as part of pre-registration, before predictions are made
(go/no-go note, step 2), and never chosen after seeing results.

---

# Cu process critical velocity against oxide thickness (`vcr_process_oxide_cu.csv`)

Seven rows from HG2019b Table 1, compiled by those authors from five spray studies (Gilmore1999, Li2010,
Gärtner2006, Van Steenkiste1999, Li2006). The oxide thickness is HG2019b's estimate, assuming all measured powder
oxygen sits in a surface layer. Process quantity (not LIPIT), mixed particle sizes (10–56 µm) and gas
temperatures (200–300 °C). HG2019b's reading: from ~20 to 7.5 nm, v_cr changes by no more than ~15 %; below
2–3 nm it drops by up to ~50 % (to 310–327 m/s).
