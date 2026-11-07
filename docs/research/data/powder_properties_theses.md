# Powder (and substrate) properties from three MIT theses

WSL B task 2026-11-07-b4. Extracted 2026-11-07. Page numbers are PDF page numbers (pp.), which match the printed
page numbers in all three theses.

**Not reported here, by the task's rule:**
- critical velocities, including the v_cr column of Lucas Table 2;
- bonding or rebound outcomes;
- anything from Panova pp. 56–57 or p. 146. Those pages and their neighbours (pp. 55–58, 145–147) were removed from
  the text before it was read.

None of the property values below is attributed to a pending blind paper (B03, B05, B06, B07, B12, B16).

| Source | File (Peter's copy, not committed) | sha256 |
|---|---|---|
| Lucas, PhD thesis, MIT DMSE 2025, 135 pp. | `coldspray-papers/B01_B02_Lucas_PhD-thesis_2025.pdf` | `1697751c5268afd41b290bb8bb48739e96dde8fd4194c1991f0ac6e2eafd7eac` |
| Panova, PhD thesis, MIT DMSE 2026, 186 pp. | `coldspray-papers/notlisted_Panova_PhD-thesis_2026.pdf` | `5a809e428cbdd5268adb2d92520ddefd717f1648d9d51a25f469e5250c538b00` |
| Lienhard, PhD thesis, MIT DMSE 2022, 91 pp. | `coldspray-papers/B04_B14_Lienhard_PhD-thesis_2022.pdf` | `530c7a1c62d8522098fde7320548ef9e66d0fb5ffeeecf659eeae87a360834da` |

## Answer to the key question

**No.** Neither Lucas Table 2 nor anything else in Lucas ch. 3–4 gives a failure strain, a hardening exponent or a
stress–strain curve for the impacted Cu powder.

- **The Cu entries in Table 2 are the plates.** The rows "Cu, Soft" and "Cu, Hard" are the annealed and full-hard
  substrate plates. Their ε_c values (0.29, 0.16) are hardening exponents n computed from Eq. (18),
  n = (ln σ_Y − ln K) / ln ε_pre. That uses each plate's quasi-static strength, an initial plastic strain matched
  to the Tanner & McDowell OFHC compression curve, and K ≈ 350 MPa taken from that same literature source. It is
  not a measurement (p. 76; Table 1 p. 48; Sec. 2.4 p. 44).
- **The other Table 2 rows are compiled literature values.** These are Al, Ni, Sn, Ti, Zn, Au, 6061, 2024 and
  7075. The table cites them only jointly ("Data from Refs. [59,153,161,164,183,198,225,255–264]") and never says
  which value came from which reference or which material form (powder, plate or bulk) it describes (p. 77).
- **The only powder-specific strength in Lucas** is the dynamic yield strength of ch. 3, given below.

The other two theses also contain no failure strain, hardening exponent or stress–strain curve for any powder or
substrate. I searched the whole Panova thesis (minus the excluded pages) and Lienhard ch. 2–4 for: hardening
exponent, stress–strain, failure strain, tensile, elongation, Hollomon, Johnson–Cook, micro-compression and
nanoindentation.

## Per powder

### P1. Cu, Alfa Aesar, 19 ± 1 µm (Lucas ch. 3, ch. 4; = B02 powder)

| Property | Value | How / where |
|---|---|---|
| Manufacturer, size | Alfa Aesar (Ward Hill MA), spherical, 99.9 % purity, D = 19 ± 1 µm (as used) | ch. 3 Sec. 3.1 p. 51; ch. 4 Sec. 4.1 p. 63 |
| Hardness | not reported | — |
| Dynamic yield strength Y_d | **383 ± 65 MPa** | Wu et al. EPP-sphere-on-rigid-target power law (α = 0.78 case; Eq. 5–7), fitted to the CoR of Cu particles striking a polished alumina target (Edmund Optics). The amplitude is the single fit parameter, and the fit is limited to the power-law regime (Sec. 3.2 pp. 51–53, Fig. 16). The thesis says "sapphire" in places and "alumina" in Sec. 3.1. |
| Cross-check | PTW-model FEA (annealed-Cu parameters, Mie–Grüneisen EOS) gives a time- and mass-averaged J2 stress of ~250–500 MPa over the contact time, inside the Wu fit band of 317–448 MPa | Sec. 3.3 pp. 55–56, Fig. 18f |
| Static / tensile strength | not reported | — |
| Failure strain, n, stress–strain curve | **not reported** for the powder | see key question |
| Grain size, temper | not reported. "Detailed microstructural analysis on similar particles" is deferred to Tiamiyu et al. [123] | p. 51 |
| Behaviour stated by the author | "the present particles behave rather like annealed copper" (basis for choosing the PTW annealed-Cu model) | p. 54 |

### P2. Cu, Alfa Aesar, gas-atomized 15–38 µm (Panova ch. 3, ch. 4)

| Property | Value | How / where |
|---|---|---|
| Manufacturer, size | Alfa Aesar, gas-atomized spherical, nominal 15–38 µm. Ch. 3 particles are 17–21 µm; ch. 4 particles were selected in the 19–21 µm range, and the stacked particles are 20 ± 1 µm | ch. 3 Sec. 3.2 p. 76; ch. 4 Sec. 4.2 pp. 101, 103 |
| Hardness | not reported | — |
| Dynamic yield strength Y_d | not reported in ch. 3 or ch. 4 | — |
| Static / tensile strength | not reported | — |
| Failure strain, n, stress–strain curve | not reported | — |
| Grain size | "a handful of grains in their initial condition, meaning a grain size of order ~5–10 µm". Revealed on polished cross-sections etched with Klemm's I (Fig. 14b) | ch. 3 Sec. 3.2 p. 76 |
| Temper | not stated (as-atomized implied, not stated) | — |
| Thermal inputs used in ch. 3 | C_p,Cu = 0.385 J g⁻¹ K⁻¹ [259]; Taylor–Quinney β ~0.8 ± 0.2 (literature range); T0 = 298 K | ch. 3 Sec. 3.5 p. 88 (handbook values, not measured) |
| Not reported, by the task's rule | Ch. 2 (= Panova & Schuh, Acta Mater. 2024) fits a CoR-based dynamic yield strength for this powder on this substrate. I did not report the value, because ch. 2 is a Panova & Schuh 2024 chapter (a blind list 2 candidate; task b3 restriction). | ch. 2 |

### P3. Al, Valimet, gas-atomized, 8 treated batches (Lienhard ch. 2; = B14 powder)

| Property | Value | How / where |
|---|---|---|
| Manufacturer, size | Valimet (Stockton CA), gas-atomized, high purity (grade not stated); treated at UTRC. Launched particles 11 ± 2 µm; TEM lift-outs from 20–30 µm particles | Sec. 2.1.1 p. 19, 2.1.2–2.1.3 p. 21 |
| Hardness, Y_d, static strength | not reported | — |
| Failure strain, n, stress–strain curve | not reported | — |
| Grain size, temper | not reported (temper: as-atomized plus the batch heat treatments of Table 2.1 p. 20) | — |
| Literature (not powder-specific) | Lucas Table 2 lists "Al": Y_d 247 MPa, C0 5380 m/s, B 84 GPa, ε_c 0.22. The source is not given per row, and the table does not say whether these values describe the Valimet powder | Lucas p. 77 |

### P4. Sn, US Research Nanomaterials, 10 µm nominal (Lienhard ch. 3; = B04-c1 powder)

| Property | Value | How / where |
|---|---|---|
| Manufacturer, size | US Research Nanomaterials (Houston TX), spherical, 99.95 % purity, nominal 10 µm. Selected particles 11 ± 0.4 µm | Sec. 3.1 p. 35 |
| Hardness, Y_d, static strength | not reported | — |
| Failure strain, n, stress–strain curve | not reported | — |
| Grain size, temper | not reported | — |
| Hugoniot / EOS (literature) | ρ = 7270 kg/m³, s = 1.49, c0 = 3200 m/s [19,118,119] | Sec. 3.3 p. 46 |
| Literature (not powder-specific) | Lucas Table 2 "Sn": Y_d 182 MPa, C0 2590 m/s, B 32 GPa, ε_c 0.2 (source not given per row) | Lucas p. 77 |

### P5. Zn, American Elements, −325 mesh (Lienhard ch. 3; = B04-c2 powder)

| Property | Value | How / where |
|---|---|---|
| Manufacturer, size | American Elements (Los Angeles CA), spherical, 99.9 % purity, −325 mesh. Selected particles 13 ± 0.8 µm; some satellites | Sec. 3.1 pp. 35–36 |
| Hardness, Y_d, static strength | not reported | — |
| Failure strain, n, stress–strain curve | not reported | — |
| Grain size, temper | not reported | — |
| Hugoniot / EOS (literature) | ρ = 7140 kg/m³, s = 1.55, c0 = 4020 m/s [19,118,119] | Sec. 3.3 p. 46 |
| Tangent modulus (estimate) | E_a is taken as 1.2–12.8 GPa, from the rule that the plastic wave speed is 1/10 to 1/3 of the elastic sound speed [123]. This is an assumption, not a measurement | Sec. 3.3 p. 51 |
| Literature (not powder-specific) | Lucas Table 2 "Zn": Y_d 350 MPa, C0 3130 m/s, B 65 GPa, ε_c 0.21 (source not given per row) | Lucas p. 77 |

## Substrates

The task asked for substrates only where a thesis gives a failure strain or n. Only Lucas does: n for the two Cu
plates, derived as described under the key question, not measured. For context, the measured hardnesses and grain
sizes of the same plate family are listed below.

**Lucas, Cu plates: ch. 2 Table 1 (p. 48), Sec. 2.1.1 (pp. 34–36), Table 2 (p. 77).**

- Plates: McMaster-Carr C110 (99.9 %) in tempers O and H00; H04 made by cold-rolling H00 from 6.25 to 1.95 mm in
  0.03 mm steps; and Online Metals OFHC in temper H02.
- Hardness: Vickers, LECO LM247AT, 100 g load, at least 30 indents per temper.
- Grain size: ASTM E112 intercept method.
- Quasi-static strength: σ = H/3.

| Plate | HV (MPa) | σ_qs (MPa) | Grain (µm) | ε_pre (fitted to Tanner & McDowell) | n (Eq. 18) | Y_d (Table 2) |
|---|---|---|---|---|---|---|
| Annealed (O), ch. 4 "soft" | 622 | 207 | 12.5 | 0.17 | 0.29 | 351 MPa |
| Eighth-hard (H00) | 790 | 264 | 15.9 | 0.33 | — | — |
| Half-hard (H02, OFHC, Online Metals) | 986 | 329 | 7.7 | 0.73 | — | — |
| Full-hard (H04), ch. 4 "hard" | 1032 | 344 | 6.6 | 0.83 | 0.16 | 562 MPa |

The substrate Y_d values come from CoR fits of 14.5 µm alumina spheres on the plates (ch. 2 Sec. 2.2.2 pp. 39–40).
Table 2 lists both Cu rows with C0 = 3950 m/s and B = 137 GPa. Lucas ch. 2 reports an average dynamic-to-quasi-static
strength ratio of ~1.66 across the tempers (p. 40, Fig. 13).

**Panova substrate (ch. 3 and 4):**
- Material: C101 H02 Cu sheet, 0.05″ thick (Online Metals), HV 100. Load and method not stated.
- Preparation: cut to 4 × 10 mm and polished to a 0.04 µm finish (ch. 4 p. 101; ch. 2 p. 44).
- Grain size: ~15–20 µm (ch. 3 p. 85).
- No failure strain or n.
- Comparison with Lucas: this is the same supplier and temper as Lucas's H02 plate (HV 986 MPa ≈ 100 HV,
  grain 7.7 µm), but neither thesis says the two are the same lot. The grain sizes differ.

**Lienhard substrates:**
- Ch. 2: 99.999 % Al (Laurand Associates).
- Ch. 3: 99.85 % Sn plate, 3.2 mm; and 99.9985 % Zn foil, 1 mm (Alfa Aesar). Grain size of order several hundred
  µm (Sn) and several dozen µm (Zn) (p. 36).
- No hardness, strength, failure strain or n for any of them.

## Pending blind papers

No property value used above is attributed in these theses to B03, B05, B06, B07, B12 or B16. The two places where
these theses describe the Cu powder's microstructure by deferring to other work:

- Lucas p. 51 refers to Tiamiyu et al. [123] for the microstructure of "similar particles". That is Tiamiyu,
  Lucas, Pang, Chen, LeBeau and Schuh, Materials Today 2023 (hydrodynamic penetration of a Cu microparticle),
  which is not a blind paper. It was not opened.
- Lucas Table 2 (p. 77) also cites Refs. [59,153,161,164,183,198,225,255–264] jointly. I did not check whether any
  of these is a pending blind paper.

`pending blind paper` flags: none raised, because no value in this file comes from one.
