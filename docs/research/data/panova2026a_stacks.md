# Panova2026a: two-particle Cu stacks (WSL B task 2026-11-07-b3, part 2)

Source: Panova PhD thesis (MIT DMSE, Feb. 2026; sha256 `5a809e42…0538b00`), **chapter 5**, pp. 123–139, which
matches Panova & Schuh, Materialia 46 (2026) 102742 by content (the chapter names no publication). The journal paper
itself was not available, so everything below is the thesis version. The stacks' particle–substrate interfaces were
analysed in **chapter 4** (Panova & Schuh, Surf. Coat. Technol. (2025) 133048), and chapter 5 reuses the same
specimens; the chapter 4 values for these specimens are included and labelled as such.

**Excluded, as the task requires:**
- Everything from chapter 2 (Panova & Schuh, Acta Mater. 2024): the single-impact comparators shown in ch. 5
  (Fig. 27b–d, black points in Figs. 28 and 29, Fig. 30j–l, and the single-impact percentages in the text on p. 134),
  and the critical velocity that ch. 4 quotes from ch. 2 (p. 101–102).
- Pending blind papers: chapter 5 cites B03 and B05 only without values (pp. 125, 135). Nothing was cut.

## Set-up

| Item | Value | Where |
|---|---|---|
| Powder | Cu, gas-atomized, spherical, 15–38 µm, Alfa Aesar; temper and purity not stated | ch. 5 p. 126; ch. 4 p. 101 |
| Particles used | selected in the 19–21 µm range; "all particles are of diameter 20 ± 1 µm" | p. 126; ch. 4 p. 103 |
| Oxide state | not stated (native oxide assumed in the discussion, not measured) | – |
| Substrate | Cu C101, H02 (half-hard) sheet, Vickers 100 HV; cut 4 × 10 mm, ground and manually polished to a 0.04 µm mirror finish | p. 126; ch. 4 p. 101 |
| Stack build-up | first particle launched on a clean polished spot; launchpad then translated **without moving the substrate** and a second particle launched at the same spot. Launchpad–substrate separation ~400 µm, so slight misalignment shifts the second impact; many attempts landed partly or fully off the first particle (ch. 4 Fig. 21). Three "direct strike" stacks with the particles directly overlapping were selected; the lateral offset is not quantified. Velocities of the two particles matched within ±6 % | p. 126; ch. 4 pp. 102–103 |
| LIPIT | launchpad 210 µm glass / 100 nm sputtered Cr / ~75 µm polyurea; Nd:YAG 10 ns, 532 nm; laser power 20–45 mW; SIMX 16 camera, 16 frames; illumination laser 50 µs, 640 nm (ch. 4) | p. 126; ch. 4 p. 102 |
| Velocity uncertainty | "typical uncertainties are on the order of ±2 % in velocity" (general statement, ch. 1) | p. 21 |
| Temperatures | not stated (room) | – |

## What was measured and how

- **FIB-SEM tomography:** Pt-Pd sputter coat; excavation at 30 kV, 21 nA; serial sectioning at 30 kV, 2.5 nA
  (dwell 3 µs in ch. 5, 1 µs in ch. 4); SEM imaging at 10 kV with backscatter and through-lens detectors; slice
  spacing **50 nm**; ~600 slices per stack (ch. 5) or ~700 images (ch. 4). Reconstruction in Dragonfly (ORS).
- **"Bonded":** non-bonded regions are labelled manually in each slice as dark hairlines in backscatter contrast,
  visible at **~14 nm** resolution (impurities such as C or O, or a gap). Everything not labelled non-bonded counts as
  bonded, so the reported bonded fraction is an **upper bound** (unbonded area at least as large as reported).
- **Bonded fraction:** β = 1 − A_non-bonded / A_interface, from the reconstructed areas of the whole bowl-shaped
  interface.
- **Uncertainty:** crater and non-bonded areas carry a 3 % uncertainty, propagated into β by standard uncertainty
  propagation (Fig. 30 caption, p. 136).
- **Other measures:** flattening ratio FR = w/h of the top splat; equatorial strain ε = (d1 + d2)/(2 d0) − 1 (Eq. 19);
  interfacial area normalized by the impacting particle's initial surface area.

## Results per stack

Velocities, diameters and particle–particle β are printed in the Fig. 30 panel labels (p. 135); particle–substrate
values are printed in ch. 4 Table 3 (p. 105). Flattening, strain and area exist only as plotted points and were
digitized.

| Stack | v1 bottom (m/s) | d1 (µm) | v2 top (m/s) | d2 (µm) | β particle–particle (top interface) | β particle–substrate (bottom interface, after both impacts; ch. 4) | Bonded area / bottom particle surface (ch. 4) |
|---|---|---|---|---|---|---|---|
| 1 | 602 | 19 | 636 | 19 | 7 ± 4 % | 23 ± 3 % | 0.97 |
| 2 | 669 | 21 | 668 | 20 | 18 ± 3 % | 41 ± 3 % | 1.06 |
| 3 | 697 | 19 | 738 | 20 | 9 ± 4 % | 81 ± 1 % | 1.27 |

Top-particle deformation (red points, **digitized**):

| Stack (v2) | FR = w/h, Fig. 28b, digitized (+-0.1) | Equatorial strain, Fig. 28c, digitized (+-0.02) | A_interface / A_particle surface, Fig. 29a, digitized (+-0.02) |
|---|---|---|---|
| 1 (636 m/s) | 3.8 | 0.38 | 0.83 |
| 2 (668 m/s) | 3.2 | 0.48 | 0.82 |
| 3 (738 m/s) | 4.0 | 0.46 | 0.86 |

Axis calibration used: Fig. 28b, x 550–850 m/s, y 1.0–5.0 (ticks every 0.5); Fig. 28c, x 550–850 m/s, y 0.0–0.8
(ticks every 0.1); Fig. 29a, x 500–800 m/s, y 0–1.5. Fig. 29b plots the same particle–particle β as Fig. 30 (red
points consistent with 7, 18 and 9 %).

Qualitative interface observations (p. 133–134, Fig. 30): at 636 m/s the least continuous particle-side jetting and
the least bonding, bonded region next to the two largest jets at the bottom edge, a hairline unbonded lip at
bottom right; at 668 m/s jetting almost all around, bonded on the right and upper side, a thick dark gap and severe
target jetting on the left (described as resembling the onset of peel-off); at 738 m/s bonded only along the upper
edge and a narrow band on the left. In all three, bonded patches sit at the perimeter, where particle- and
target-side jetting overlap, and opposite the dark gap. The target (bottom) particle appears to jet more than the
impacting particle.

## The authors' interpretation (theirs)

The top particle striking a domed, previously deformed particle flattens more and indents the target less than a
particle striking the polished substrate at the same velocity, while creating a similar interfacial area. Bonding at
the particle–particle interface is nevertheless much lower, which they attribute to reduced jetting localization,
specifically too few regions where both surfaces jet, caused by the dome geometry and by the target being already
work-hardened (citing Lucas et al. on hardened substrates localizing more). They conclude that geometry and
hardness of the underlying surface act together and cannot be separated in these experiments (addressed in ch. 6).

## Supplementary or thesis-only material

The Materialia paper was not available, so it cannot be said which items are thesis-only. Items that certainly come
from a different publication: the particle–substrate β and bonded-area values (ch. 4 Table 3, Surf. Coat. Technol.
2025). The figure numbering (Figs. 27–30) is the thesis's.
