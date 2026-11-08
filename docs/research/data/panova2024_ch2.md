# Panova & Schuh 2024 (Panova thesis ch. 2): Cu-on-Cu single impacts, Y_d, V_cr, bonded fraction

WSL B task 2026-11-08-b7. Peter released this paper on 2026-11-08 (B4 exposure log).

- **Source:** V. Panova, PhD thesis, MIT DMSE 2026, ch. 2, "Bonding at Particle-Substrate Interfaces", pp. 41–72.
  Peter's copy `coldspray-papers/notlisted_Panova_PhD-thesis_2026.pdf`, sha256
  `5a809e428cbdd5268adb2d92520ddefd717f1648d9d51a25f469e5250c538b00`. Page numbers are thesis pages.
- **The journal paper:** the chapter says it "closely follows" V. Panova, C.A. Schuh, Acta Mater. 276 (2024)
  120105, doi:10.1016/j.actamat.2024.120105 (thesis ref. [75]).
- **Journal version not compared.** OpenAlex lists it only as free-to-read on the publisher's site (bronze), with no
  repository copy; MIT DSpace returns only the thesis, and the OSTI search failed. I therefore could not say whether
  the journal values differ from the thesis values below.

**Excluded under the blind rules:**
- Pp. 56–57 (Fig. 8a, which plots B03 data with the thesis's own) were not read. They were not needed: every
  per-specimen bonded fraction is printed in Fig. 7 (p. 55).
- Text that reports B03's findings (p. 43, p. 48, p. 54) is not reproduced.
- One sentence on p. 45 quotes a range of earlier Cu-on-Cu critical velocities. It cites refs. [6] (Assadi 2016),
  [83] (HG2018b) and [108] (Sun 2020); none of them is a pending blind paper. The range is not repeated here
  because it is not this paper's data.
- P. 146 was not read.

## 1. Powder and substrate

| Item | Value | Where |
|---|---|---|
| Powder | Cu, gas-atomized, spherical, nominal 15–38 µm, Alfa Aesar. Lot, temper and oxide state not stated | p. 44 |
| Size used | 17–21 µm, each particle measured optically before launch. Table 1 gives the radius of each tomography particle (item 4) | p. 44, p. 47 |
| Substrate | C101 H02 (half-hard) Cu sheet, 0.05″ (1.27 mm) thick, Online Metals (Wallingford CT). Vickers hardness 100 (load not stated). Cut to 4 × 10 mm with a diamond saw, ground and polished to a 0.04 µm mirror finish | p. 44 |
| Substrate, more detail (ch. 6, same plate type) | ch. 6 calls its H02 substrate "the same substrate used for single particle experiments in [75]": grain size ~10 µm, 98 ± 1 HV. Ch. 3 says ~15–20 µm grains for the ch. 2 substrate | ch. 6 p. 143; ch. 3 p. 85 |
| LIPIT | Glass 210 µm / Cr 100 nm / polyurea ~75 µm launch pad. Nd:YAG 10 ns, 532 nm, laser power 3–65 mW. Illumination laser 50 µs, 640 nm. SIMX 16 camera, 16 frames. Inbound and rebound velocities measured | p. 44 |
| Temperature, angle | not stated | — |

**Is this the powder of ch. 3–6 and of Panova2026b?**
- **Ch. 3: yes.** Ch. 3 re-analyses the ch. 2 dataset itself (p. 76).
- **Ch. 4 and ch. 5: same specification.** Both use 15–38 µm Alfa Aesar gas-atomized Cu on C101 H02 Cu, HV 100
  (ch. 4 p. 101). No lot is stated, so "same powder" is the specification, not a stated lot.
- **Ch. 6 / Panova2026b: no.** Its LIPIT particles are **Praxair CU-159-3** spherical Cu powder sieved to 17–21 µm,
  the same powder used to cold-spray its coating substrates (ch. 6 pp. 142–143). Only its polished H02 substrate is
  the ch. 2 substrate.

## 2. Dynamic yield strength of the powder (CoR fit)

**Y_d = σ_y = 403 ± 90 MPa** (p. 69; Fig. 13 p. 70).

- **Model:** Wu et al. [232,233], CoR = V_r/V_i = α (V_y/V_i · E*/σ_y)^(1/2) (Eq. 9).
  - α = 0.57, "for matched particle and substrate impacts", taken from Sun et al. [108].
  - E* is the reduced modulus of particle and substrate (Eq. 10). The E and ν values used are not stated.
  - V_y = (26 σ_y⁵ / (ρ E*⁴))^(1/2) (Eq. 11).
- **Data:** the rebounding impacts from the first-phase CoR campaign (Fig. 4, item 3). The fit is limited to
  impacts that follow the V^(-1/2) power law, which "begins to break down above ~450 m/s".
  - Fig. 13b shows the per-impact Y_d values against velocity from ~75 to ~445 m/s. I counted about 40 points
  (digitized, ± 3 points); the number is not printed.
- **Value and uncertainty:**
  - 403 MPa is the average effective strength from the fit (Fig. 13a).
  - ± 90 MPa is the standard deviation of the per-impact values (Fig. 13b).
  - The per-impact values range from about 260 to about 720 MPa (digitized from Fig. 13b, ± 15 MPa; one outlier
    at ~720 MPa, the next highest ~550 MPa).
- **A second, model-based strength:**
  - Fitting the bonding model, Eq. 8 below, to the bonded fractions between V_cr and 1.4·V_cr gives
    σ_y ≈ 500 ± 30 MPa (p. 67, Fig. 12).
  - The ± 30 MPa is the sensitivity band shown, not a statistical error.
  - The authors say the upper end of the CoR range agrees with it (p. 69).
- **Comparison quoted:** Sun et al. [108], 14.0 ± 0.5 µm alumina on Cu, CoR fit σ_y = 450 ± 45 MPa (p. 68). This
  is for the substrate, not this powder.
- **Not given:** hardening exponent, failure strain, or stress–strain curve.

## 3. Critical velocity

**V_cr = 540 ± 5 m/s** for ~17–21 µm Cu particles on the H02 Cu substrate (p. 45; Fig. 4 caption, p. 46).

- **Definition:** "the average velocity between the two fastest non-bonded particles and the two slowest bonded
  ones", following [108]. The ± 5 m/s is the standard deviation of those four velocities.
- **Bounds:** no window bounds are printed.
- **Velocity uncertainty:** not stated in ch. 2. Ch. 1 p. 21 gives ±2 % in general.
- **Number of impacts:** the first phase had 70 single-particle impacts between 50 and 730 m/s, each with V_i and
  V_r recorded (p. 45). V_cr comes from this set.
  - A second phase added impacts between V_cr and ~1.5·V_cr; their number is not stated.
  - Fig. 5a plots all impacts, and 10 were selected for tomography.

This is the value Panova2026b quotes (task b7). Ch. 3 (p. 76) and ch. 4 (p. 101) repeat V_cr = 540 m/s.

## 4. Bonded fraction against impact velocity

**Definition and method** (pp. 48–50):
- **Imaging:** FIB-SEM serial sectioning (FEI Helios 660), slice thickness 50 nm, ~620 slices per particle.
  Backscatter and through-lens detectors at 3 kV.
- **Segmentation:** Dragonfly 2022.2. The total particle–substrate interface was labelled manually on every slice.
  "Unbonded" regions are those with a visible dark band (lower-Z contrast) at ~14 nm resolution, found with
  Dragonfly machine-learning models plus exhaustive manual labelling.
- **Formula:** β = 1 − A_non-bonded / A_interface.
- **Upper bound:** β is an **upper bound** on bonding, since separations finer than ~14 nm are not resolved.
- **Uncertainty:** ~3 % on each area, because ~3 % of interface pixels were hard to classify. The error on β is
  propagated from that.

**Per specimen.**
- **Sources:** β and velocity are printed in the Fig. 7 panel labels (p. 55). Particle radius, contact radius R0
  and crater depth h come from Table 1 (p. 47).
- **Size:** particle diameter = 2 × the Table 1 radius. Each particle's size was measured before launch, within
  17–21 µm.

| Specimen (Fig. 7) | V_i (m/s) | V_i / V_cr | Particle radius (µm) | R0 (µm) | h (µm) | β |
|---|---|---|---|---|---|---|
| a | 552 | 1.02 | 9.7 | 12.3 | 5.7 | 6 ± 4 % |
| b | 585 | 1.08 | 9.6 | 13.3 | 6.8 | 18 ± 3 % |
| c | 600 | 1.11 | 8.7 | 11.3 | 6.1 | 40 ± 3 % |
| d | 656 | 1.21 | 9.2 | 11.8 | 8.9 | 35 ± 3 % |
| e | 660 | 1.22 | 10.3 | 11.5 | 6.0 | 27 ± 3 % |
| f | 678 | 1.26 | 9.6 | 12.8 | 8.0 | 40 ± 3 % |
| g | 700 | 1.30 | 9.6 | 12.9 | 8.1 | 89 ± 1 % |
| h | 779 | 1.44 | 8.8 | 11.2 | 8.4 | 80 ± 1 % |
| i | 823 | 1.52 | 9.2 | 11.8 | 8.2 | 74 ± 1 % |
| j | 875 | 1.62 | 9.5 | 12.7 | 10.1 | 13 ± 3 % |

- **Table 1 averages** (V_cr to 1.3·V_cr, the seven specimens a–g): radius 9.5 ± 0.5 µm, R0 12.3 ± 0.8 µm,
  h 7 ± 1 µm (SD). The model uses these averages.
- **Cross-check:** Fig. 12 (p. 68) plots specimens a–g as bonded fraction against V_i/V_cr. Its points match the
  Fig. 7 labels to within the reading error of ±0.02.
- **Not extracted:** Fig. 9b (p. 59) plots crater area, contact area and bonded area normalized by crater area
  against velocity. It is not digitized here because Fig. 7 gives β directly.

**The authors' bonding model** (pp. 60–67):
- The bonding pressure needed to extrude metal through gaps in a rarefied oxide (slip-line extrusion, Johnson) is
  p = (σ_y/√3)(1 + 5π/2)(1 − 4r²h²/(R0² + h²)²)^(1/2) (Eq. 5).
- The available impact pressure is ½ρv_i² (Eq. 6), with ρ = 8960 kg/m³.
- Setting the two equal gives the critical radius r_c (Eq. 7) and β (Eq. 8). The fit to specimens a–g gives
  σ_y ≈ 500 ± 30 MPa.
- The authors' interpretation: bonding between V_cr and ~1.4·V_cr is driven by the creation of new interface area,
  with the "south pole" bonding last. Above ~1.5·V_cr, interface-opening (peeling) strains of hydrodynamic
  penetration reduce bonding.

## 5. Coefficient of restitution data

**Not tabulated.** The CoR data appear only in Fig. 4 (p. 46) and Fig. 13a (p. 70, log–log). Item 2 is printed
(403 ± 90 MPa), so they are not digitized, as the task instructs.
