# Cold spray: what a deposition-efficiency and bonding model must answer (Q1)

Draft for Peter to correct. Written 2026-11-03. This list defines what "better" means for this track. Source keys
and evidence levels (F full text, A abstract, S second-hand, M metadata) are those of
[coldspray-data-and-zoo.md](coldspray-data-and-zoo.md). Z-numbers refer to its zoo table.

Status: **answered** = a model gives a quantitative prediction that has been checked against data across more
than one material; **partly** = a model or correlation exists, but it is calibrated on few materials, untested
out of sample, or only qualitative; **not answered** = no model found.

## A. Will it bond at all?

| # | Question | Status | Best current answer (source) |
|---|---|---|---|
| A1 | Does particle material P bond to substrate S at all within reachable velocities? | **partly** | Matched metals bond above a v_cr [HG2018a F]. Some mismatched pairs show no v_cr in the tested range (Al–Zn per Nelson group page; Al on some steels per a TMS abstract) [S]. The impact-mode map (Z9) classifies splatting, co-deformation and penetration but does not predict "never bonds". |
| A2 | Which mechanism makes the bond: jetting and oxide break-up, interlocking, diffusion, nanoscale melting? | **partly; contested** | ASI view (Z1, Z5) against the hydrodynamic/spall view (Z6, Z7). The Assadi–Schuh exchange in Scripta 162 (2019) is unresolved in the literature I found [Assadi2019c M, HG2019 A]. Mechanical interlocking dominates some dissimilar pairs [Hussain2009 S]. Restricted melting can bond [Khan2026 A]. |
| A3 | How do oxide/hydroxide films on powder and substrate change bonding? | **partly** | +2–3 nm hydroxide → ~+14 % v_cr for Al [Lienhard2020 S]; thicker substrate oxide → lower DE [Ichikawa2015 S]; peridynamics trend [Ren2024 A]. No quantitative cross-material model. |

## B. At what conditions?

| # | Question | Status | Best current answer (source) |
|---|---|---|---|
| B1 | Critical velocity v_cr for a matched pair, ~10 µm, room temperature | **partly** (closest to answered) | v_cr ≈ 0.15·sqrt(B/ρ), fitted over Al, Cu, Ni, Zn [HG2018a F]. Empirical Z1, Z2 are calibrated mainly on Cu [S]. Not yet tested on held-out materials. |
| B2 | v_cr against particle size | **partly** | Power law, n ≈ 0.19–0.21 (LIPIT Al, Ti) [Dowding2020 F]; 0.19 Cu and 0.14 316L from nozzle experiments [Schmidt2006 via Dowding2020]; mechanism proposed (jet temperature → spall strength). |
| B3 | v_cr against particle and substrate temperature | **partly** | Particle: sqrt-type dependence on T* [HG2018a F], temperature terms in Z1 and Z2 [S]. Substrate: lower v_cr when heated (Al, Sn, Ti) [Chaban2021 A]. |
| B4 | v_cr for dissimilar pairs | **partly** | Arithmetic-mean rule in Z7 [Panova2026b F]; 9 dissimilar pairs measured [Hassani2020 S]. |
| B5 | v_cr on the growing coating (particle on particle), not on a polished substrate | **partly; one material** | ~1.3× the substrate value for Cu [Panova2026b F]; build-up v_cr above single-bond v_cr for Au [Reiser2024 F]. |
| B6 | How single-particle (LIPIT) v_cr maps to process v_cr | **not answered** | LIPIT values for Al, Ni, Zn are ~40–60 % above cold-spray literature values. The gap is attributed to process heating [Panova2026b F], with no quantitative model. |
| B7 | Upper limit of the window (erosion/melting velocity) | **partly** | Melting hinders adhesion; erosion velocity measured for Sn and modelled [HG2017 M, HG2018c S, Lucas2025b M]. |

## C. Deposition efficiency (DE)

| # | Question | Status | Best current answer (source) |
|---|---|---|---|
| C1 | DE as a function of the particle velocity and size distribution, given v_cr(d) | **partly** | Fraction above v_cr(d) (Z14) [Zhang2025 S, Raletz2006 M]. Validated on Al only, as far as found. Dowding2020 [F] argues the size distribution can explain Gilmore's DE rise (plausibility only). |
| C2 | DE against gas pressure, temperature and gas type (process maps) | **partly; per material** | η-maps [Assadi2011 S]; ML on Al 6061 [Hamrani2024 A]; energy classifier [Canales2020 S]. Calibrated per material, no extrapolation claim. |
| C3 | Is the bonding probability a sharp threshold or a sigmoid in v (at fixed d)? How wide is it? | **not answered** | LIPIT gives brackets (equal numbers bonded and rebounded) [Dowding2020 F]. On rough, hard surfaces the threshold is "not as sharp" [Panova2026b F]. No model of the width. |
| C4 | DE once the coating grows: erosion of deposited material by later impacts, peening | **not answered** | Qualitative only [Reiser2024 F, Panova2026a A]. |

## D. Bond quality

| # | Question | Status | Best current answer (source) |
|---|---|---|---|
| D1 | Bonded fraction of the interface against velocity | **partly; one material** | Cu FIB tomography; particle–particle ≤ 18 % [Panova2026a A]. |
| D2 | Bond strength against velocity (single particle) | **partly; one material** | Al: 3× rise from v_cr to a peak near 1060 m/s, then decline [Tang2025 A]; spatial gradient across the splat [Tang2024 S]. |
| D3 | Coating adhesion and cohesion strength from process parameters | **partly; empirical** | Per material, from tests [Hussain2009 M]; HUGO-CS holds the mechanical outcomes [Price2026 F]. |

## E. Extrapolation and validity domain (Peter's positions 3 and 5)

| # | Question | Status | Best current answer (source) |
|---|---|---|---|
| E1 | Prediction for a **new material** (not in the calibration) | **not answered (not tested)** | Z6 and Z7 are material-property-based and could be tested this way. I found no held-out-material test. |
| E2 | Prediction for an **extended parameter range** of a known material (higher velocity, temperature, finer powder) | **partly** | Upper limits (Z10, Z13) show non-monotonic effects that empirical fits miss (strength peaks, erosion). |
| E3 | Does the model state **for which materials and conditions it predicts**? | **not answered** | Domains exist only as prose remarks (Z1, Z6). No model outputs a validity predicate. |

## Summary for Peter

- Position 1 (models answer few questions): **supported**. Of 20 questions, none is "answered" by the strict
  definition. Only B1 comes close, and only within its fitted set.
- Position 2 (data taken with the wrong mindset): **supported for bulk DE and coating adhesion**, which
  integrate over distributions and rarely report uncertainty (DE: 16.2 % of values in HUGO-CS [Price2026 F]).
  **Challenged for single-particle work**: since ~2016 LIPIT provides per-particle, mechanistic data (v_cr,
  restitution, jetting, bond strength, interface tomography). But it covers few materials (~8 matched metals),
  mostly one group, room temperature, and no process heating.
- Position 4 (mechanistic structure with few dimensionless groups): **this already exists in the literature**
  and is the leading candidate: v_cr/C₀, T*, d/d₀, the impact-mode ratio, and a spall group
  (2σ_y ε / B) (Z6–Z9). It is a variant of existing work, not a gap to fill from scratch.
- Position 5 (the validity domain as an output): **a real gap** (E3).

Please correct: missing questions, wrong statuses, and which questions matter most for your application
(multi-particle build-up).
