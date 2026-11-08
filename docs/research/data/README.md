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
   **Resolved 2026-11-07 from the primary HG2018b** (author's final manuscript, MIT DSpace 1721.1/123866), rows
   `P18-*`: Table 1 gives Al 797–824 (14 ± 2 µm), Ni 650–660 (10 ± 2), Cu 539–568 (14 ± 2), Zn 518–523 (11 ± 2) m/s,
   each from the highest rebound to the lowest adhesion, velocity uncertainty 2 %; the text gives Al 810 at 14 µm
   and 770 at 30 µm. So Panova2026b and Dowding2020 quote the primary correctly. The H20 rows are not misquotes but
   Hassani2020's own equal-count windows. For Al and Ni they contain the primary window; for Cu (560–590) and Zn
   (520–570) they do not, so Hassani2020 must rest on more or other impacts. The H20 rows stay as they are (frozen
   v1 scores use them). Note: the primary windows (5–29 m/s wide) are narrower than the ±2 % velocity error.
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
- (HG2018b and HG2019b primaries: now read, rows P18 and P19);
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
| P-HG | HG2018a preprint, Extended Data Table 1 (F) | Cu, Ni, Al, Ta | ρ, c_p, T_m, B, G, ν, C₀, Hugoniot s, Grüneisen γ₀, Johnson–Cook A, B, n, C, m, reference strain rate and temperature (γ₀ and the last two added 2026-11-04), thermal conductivity k (column `k_W_mK`, added 2026-11-05 for CS-13; Al 237 W/(m K), no temperature condition printed) |
| P-WP | Wikipedia element infoboxes, retrieved 2026-11-03 (tertiary; densities cite Arblaster 2018) | Al, Cu, Ni, Ti, Zn, Sn, Ag, Au, W, Ta, Fe | ρ, T_m, molar C_p, B, G |
| **P-H20** | **Hassani2020 supplementary information, Table S1** (supplied by Peter; F) | Al, Ni, Cu, W, Ti, Zn, Sn, Au, Ag, Al 6061, Al 2024, Al 7075 | ρ, ν, E, Hugoniot C₀ (from Marsh 1980), macroscale dynamic yield (plate impact, 5 metals, cited), **microscale dynamic yield Y_d ± uncertainty** |

P-H20 is the matched source for the v_cr table: same materials, same group, Y_d at impact conditions. Two flags:
- **Partial circularity.** Microscale Y_d was fitted to the sub-critical rebound data of the same LIPIT
  campaigns (Wu et al. 2005 elastic–perfectly-plastic model, prefactor 0.57 from Sun2020). A model that uses
  Y_d to predict v_cr is therefore not fully independent of the impacts that define v_cr. Pre-registration must
  say whether Y_d is an allowed input, and for a blind material it has to come from impacts below v_cr only.
- **W.** Its Y_d (6900 MPa) is estimated from a macro–micro correlation (Fig. S4), not measured.

**Still missing:**
- Thermal conductivity of the Al alloys (Al 6061 not sourced; HG2018a covers pure Al only).
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

## buildup_reiser2024.csv (build-up track, added 2026-11-07)

Per-shot impact velocity and particle diameter for the nine Au particle stacks of Reiser2024 (arXiv:2404.05601v1),
digitized from Figs. 3b (intact stacks I1–I4) and 5b (fractured stacks F1–F5). Evidence level F; digitized, not
printed. Method, validation against the printed stack means, and reading error:
[../coldspray-buildup-track.md](../coldspray-buildup-track.md), section "Q-B1". Script:
`scripts/digitize_reiser2024.py`.

| Column | Meaning |
|---|---|
| `stack`, `figure`, `stack_outcome` | I1–I4 intact (Fig. 3b panels left to right), F1–F5 fractured (Fig. 5b) |
| `shot` | shot number within the stack, 1 = first |
| `v_mps` | impact velocity [m/s]; the paper's measurement error is ±5 % |
| `v_method` | `cap midpoint` (error-bar caps) or `bar end` (grey bar); reading error about ±3 m/s |
| `v_bar_end_mps` | the bar-end reading, as a cross-check, where the cap midpoint was used |
| `d_um` | particle diameter [µm] measured before launch; reading error about ±0.2 µm |
| `fracture_event` | 1 if the shot is marked in Fig. 5b as having fractured the stack |

## Particle-property gap inventory (2026-11-07)

Which v_cr rows have strength data **for the powder that was impacted**: dynamic yield Y_d, static or tensile
strength, failure strain ε_c or hardening exponent n. These inputs block Z1, Z2 (tensile strength), Z7 (failure
strain), CS-10 and Z18 (particle strength) on most rows. The inventory uses only sources already read; no new
search was made. "Same material" means a value for the metal, measured on another powder or on bulk.

| Rows | n | Particle | Y_d of the impacted powder | Static or tensile strength | ε_c or n | Same-material values only |
|---|---|---|---|---|---|---|
| H20 | 20 | 12 metals and alloys | **yes**: Hassani2020 Table S1 (`Yd_micro`, fitted to sub-critical rebounds, rule P2: partly circular) | no | no | bulk Johnson–Cook n for Al, Cu, Ni (P-HG, HG2018a) |
| P18 (HG2018b) | 5 | Al, Cu, Ni, Zn | no (other powders than H20 as far as stated) | no | no | Table S1 Y_d; bulk JC n (Al, Cu, Ni) |
| P19 (HG2019b) | 2 | Au, Ag | no | no | no | Table S1 Y_d |
| DW | 9 | Al, Ti (size series) | no | no | no | Table S1 Y_d; bulk JC n (Al) |
| CH | 3 | Al, Sn, Ti (heated substrates) | no | no | no | Table S1 Y_d |
| PA (Panova2026b) | 3 | Cu 17–21 µm, **Praxair CU-159-3** (thesis ch. 6) | no | no | no | Table S1 Y_d. Not the Alfa Aesar powder of Lucas or Panova 2024 |
| P24 (Panova & Schuh 2024) | 1 | Cu 17–21 µm, Alfa Aesar 15–38 µm gas-atomized | **yes**: 403 ± 90 MPa (CoR fit, Wu model, α = 0.57); bonding-model fit 500 ± 30 MPa | no | no | – |
| B-B10 (Na2025) | 5 | Al 6061, heat treatments | **yes**: CoR-fitted Y_d per batch (Table 1) | **yes**: micro-compression at 50 % strain, 219–351 MPa | no | – |
| B-B14 (Lienhard2020) | 8 | Al, oxide states | no ("none for the metals") | no | no | Table S1 Y_d; bulk JC n |
| B-B02 (Lucas) | 2 | Cu 19 µm | **yes**: 383 ± 65 MPa (Cu-on-sapphire impacts, Lucas ch. 3) | no | **no** for the particle (substrates only: 0.29, 0.16) | bulk JC n |
| Build-up (Reiser2024 Au, Panova2026a Cu) | – | Au, Cu | no | no | no | Table S1 Y_d (Au, Cu) |

**Summary:**
- Three groups have a strength value of the impacted powder: H20 (Y_d, partly circular), B10 (Y_d and static
  strength) and B02 (Y_d).
- **No row has a failure strain or hardening exponent of the impacted powder.** That is the input Z7's mixing rule
  needs (coldspray-results-b02-b14.md, addendum).

**Where more could come from without a new literature search:**

| Source | What might be there | Route |
|---|---|---|
| Lucas thesis ch. 3 (Cu-on-sapphire) and ch. 4 Table 2 | **checked (WSL B b4): no powder row.** The plates' ε_c are derived n (Eq. 18), not measured; the other rows are unattributed literature values | done: data/powder_properties_theses.md |
| Panova thesis ch. 2–4 | **checked:** ch. 2 (released 2026-11-08) gives Y_d 403 ± 90 MPa for the Alfa Aesar powder (row P24-Cu); ch. 3–4 nothing more. Panova2026b's PA powder is a different one (Praxair) | done: data/panova2024_ch2.md |
| Lienhard thesis (B14, B04 source) | **checked: nothing** for any powder or substrate | done |
| Na2025 (read, F) | micro-compression curves to 50 % strain (Table 1 gives only the stress); a full curve would give n | re-read Fig./SI by the modeller (B10 is unblinded) |
| A measurement | micro-compression stress–strain curves of the LIPIT powders (B10's method) give Y and n directly | candidate item for a measurement request, if the campaign trigger is met |
