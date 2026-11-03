# Cold spray: data (Q2) and zoo (Q3)

Research note for the cold-spray track (brief: docs/plans/2026-11-03-coldspray-research-brief.md). Written
2026-11-03 in a cloud session. Breadth first; nothing here has been modelled or run.

## How to read the evidence levels

Every row cites a source key from the register at the end. The level says how directly I checked the claim:

- **F**: I read the full text (arXiv, OSTI or an accepted manuscript).
- **A**: I read the abstract (Crossref, arXiv or OSTI).
- **S**: second-hand. Either a full text I read cites the claim, or it comes from a web-search summary of a page I
  could not open. S claims are leads, not facts. Check them against the original before relying on them.
- **M**: metadata only (title, authors, venue, DOI checked on Crossref). Content not checked.

Access in this session: arXiv, OSTI, Crossref and MIT DSpace pages were readable. ScienceDirect (403),
Springer (bot challenge) and the university repositories (Brunel, ResearchGate) were not. MIT DSpace PDFs were
rate-limited (429). So the classic Elsevier and Springer papers (Schmidt 2006, Assadi 2011) are
**S or M**: Schmidt's formula comes from a Sandia slide that reproduces it [Hall2015], not from the original.
Read the originals before any of these becomes a zoo member.

Update 2026-11-03 (same day): Peter supplied PDFs of Assadi2003, Vlcek2003 and Dykhuizen1998, now read in full
(F).

---

## Q2. Experiments and data

### Q2.1 Single-particle impact (laser-induced particle impact test, LIPIT)

The brief's "to be verified" item checks out with corrections. The method is the laser-induced particle impact
test (LIPIT): Nelson group (chemistry) together with Schuh group (MIT materials). The first bonding paper is a
2016 arXiv preprint; journal papers followed in 2017–2018. It measures the critical adhesion velocity particle by
particle: v_cr is where the coefficient of restitution drops to zero [HG2018a F, HG2018b A, Veysset2021 F].
The method has since spread: the Schuh final report counts at least 12 LIPIT systems being built worldwide
[Schuh2026 F]. Other groups using it include Hassani (Cornell) and Ichikawa (Tohoku) [Tang2024 S, Tang2025 A],
Sandia [Murray2025 M] and McGill [Imbriglio2019 S].

| Study | What is measured | Materials | Range / size | Data points, uncertainty | Level |
|---|---|---|---|---|---|
| HG2018a (preprint 1612.08081) | v_cr from restitution; jetting onset; FE simulations | Al, Cu, Ni, Zn, matched pairs | 100–1200 m/s launch; ~10 µm (Al also 14, 30, 45 µm) | Per-shot velocity ±3–4 %; v_cr bracketed in 25 m/s steps | F |
| HG2018b Scripta | In-situ bonding moment, restitution vs velocity | Al (two sizes) and others | — | — | A (via Veysset2021 F) |
| Hassani2020 Acta 199 | v_cr for **20 particle/substrate combinations**, 9 of them dissimilar; impact-mode map | Matched and mismatched metals | — | 20 v_cr values | S (count and design from Veysset2021 F) |
| Dowding2020 | v_cr against particle size | Al, Ti matched | ~5–50 µm | v_cr ± window (equal numbers bonded/rebounded); exponent ±0.05 | F |
| Chaban2021 | v_cr against substrate temperature | Al–Al, Sn–Sn, Ti–Ti | Heated substrate (hot stage up to 100 °C first; up to 250 °C later [Schuh2026 F]) | Narrow size selection | A (F header) |
| Lienhard2020 | Oxide/hydroxide state against v_cr | Al powder: 300 °C air, 50 % and 95 % relative humidity | — | 95 % RH: +2–3 nm layer, ~+14 % v_cr; other treatments no significant change | S (from Veysset2021 F) |
| HG2019 Appl Surf Sci | Native-oxide role | Al, Ag, Au | — | — | M |
| Imbriglio2019 | LIPIT + cold spray, adhesion | Ti on alumina | ~10 µm; v_cr ≈ 580 m/s | — | S |
| Sun2020 J Appl Mech | Rebound-to-bonding transition, power-law divergence | Cu–Cu (alumina-on-Cu for strength) | — | Per-shot restitution | A |
| Panova2026a Materialia | Two-particle stacks, FIB tomography of bonded fraction | Cu | Around optimal velocity | Bonded fraction at particle–particle interface ≤ 18 % | A (F header) |
| Panova2026b Materialia | v_cr on growth surface: roughness and hardness decoupled | Cu | Polished baseline v_cr = 567 m/s; hard surface ~653 m/s; rough+hard average ~727 m/s | Each factor +10–15 %, together ~30 % above particle–substrate | F |
| Reiser2024 Acta | Stacks of >20 particles, every impact's size and velocity recorded | Au | v_cr = 253 ± 7 m/s (single); build-up needs a higher critical velocity | 4 stacks shown; ±5 % per particle | F |
| Tang2024 Nat Commun | Site-specific bond strength across one splat interface | Al–Al | — | Weak centre, ~2× rise toward edge, plateau | S |
| Tang2025 PNAS | Bond strength against impact velocity | Al–Al | 800 (v_cr) to 1337 m/s | 3× rise to a peak near 1060 m/s, then decline | A |
| Khan2026 Acta | Restricted interfacial melting enabling bonding | Alloy particles, eutectics (AA7075 in a related abstract) | — | — | A (F header) |
| Lucas2024/2025 | Microstructure, substrate strength and ductility against bonding | Cu | — | — | M (cited in Panova2026b F) |

**The key caveat for a judge.** LIPIT v_cr is a single impact at room temperature (unless heated), on a
polished bulk substrate, with no carrier gas. It is not the cold-spray process critical velocity. Panova2026b
[F] puts LIPIT matched-pair values for Al, Ni and Zn at 797–824, 650–660 and 518–523 m/s. The cold-spray
literature gives ~500, ~400–450 and ~350–400 m/s for the same metals [Legoux2007, Zhang2024 via Panova2026b].
Panova2026b attributes the gap mainly to particle and surface heating in the process. A judge must therefore
fix which of the two quantities a candidate predicts.

**Availability.** Results are in the papers (figures and some tables). Veysset2021 [F] states "data available
within the article". A Zenodo search (2026-11-03: "LIPIT", "microparticle impact", "cold spray critical
velocity", "cold spray dataset") found **no deposited LIPIT or critical-velocity dataset**. Several papers are
open as accepted manuscripts (OSTI, DSpace, arXiv). A v_cr table would have to be extracted from figures and
tables, ideally confirmed with the authors.

**Held-out split by material.** Possible in principle. The matched pairs measured so far are about 8 metals
(Al, Cu, Ni, Zn, Ti, Sn, Ag, Au; per HG2018a, Dowding2020, Chaban2021, HG2019), plus 9 dissimilar pairs
[Hassani2020 S]. That allows leave-one-material-out validation, but with very few degrees of freedom.

### Q2.2 Bulk deposition efficiency (DE)

| Source | What | Materials | Notes | Level |
|---|---|---|---|---|
| Assadi2003 | Process v_cr: Cu 570 m/s (99.8 %, 5–22 µm), Al 660 m/s (99.93 %, < 45 µm). Coating adhesion (EN 582) just above v_cr ≈ 20 % of bulk Cu UTS | Cu, Al | **v_cr is inferred, not measured**: CFD velocity distribution (checked only against the LDA mean) combined with measured DE and size distribution (method in their ref. 12). The process v_cr therefore depends on a gas-dynamics model | F |
| Gilmore1999 | DE against measured particle velocity | Cu, ~19 µm (11–26 µm) | DE ~53 % at 640 m/s, ~95 % at 725 m/s | S (numbers via Dowding2020 F) |
| Alkimov1990 | DE against particle velocity | Cu, Ni, Al | Classic S-curves; the origin of the "critical velocity" | S (figure reproduced in Hall2015 F) |
| Raletz2006 | v_cr inferred from DE and the velocity distribution | — | — | M |
| Stoltenhoff2002 | Process analysis; Cu v_cr ≈ 570 m/s (as cited) | Cu | — | M (value via Hall2015) |
| Legoux2007 | Substrate temperature effect | Al, Zn, Sn | Source of the process v_cr values compared in Panova2026b | M |
| Ichikawa2015 | Substrate oxide thickness against DE | Al-based | Thicker substrate oxide → lower DE | S |
| Zhang2025 JMP | Reduced-order DE model validated by experiment | Al | 10 validation runs on two systems (per a TMS abstract) | S |
| HUGO-CS (Price2026) | Literature compilation: 4,383 experiments, 144 features, 1,124 sources; 1,765 hand-labelled | Many alloys, compositions resolved | Selected for **mechanical-property** papers (SCOPUS). DE is a target, but only 16.2 % of DE values carry an uncertainty. **Whether particle velocity is a field is unchecked** (github.com was blocked; raw.githubusercontent.com works, but I could not list file names) | F (paper) |
| Prior compilations (Table 1 of Price2026) | 11 datasets, mean 45 experiments; largest Yin 2024, 137 experiments from 27 articles | — | Mostly not machine-readable | F |

**What bulk DE data lack mechanistically.** A DE value integrates over particle size, velocity and temperature
distributions, oxide state, a growing rough and hardened surface, and nozzle effects. Dowding2020 [F] argues the
Gilmore1999 rise from 53 % to 95 % "can be almost entirely explained" by the size effect on v_cr. That is a
plausibility argument, not a test. The same DE curve is compatible with several mechanisms unless the velocity
and size distributions are measured run by run. This supports Peter's position 2 for bulk DE specifically.

### Q2.3 Bond strength, cross-sections, interface and oxide analysis

| Source | Method | Material(s) | Mechanistic content | Level |
|---|---|---|---|---|
| Tang2024, Tang2025 | In-situ micromechanical (SEM) tensile test of single-particle bonds | Al–Al | Local strength map; strength against velocity | S / A |
| Ichikawa2019 Acta | Tensile test inside an Auger spectrometer; oxide state on the fracture surface | — | Oxide remains at crater centre; adhesion strong at the edge where oxide is removed (ITSC 2018 abstract) | S |
| Hussain2009 JTST | Coating adhesion with a composite model: metallurgical bonding plus mechanical interlocking | Cu on Al alloy (thesis) | Splits the bond into two contributions | M / S |
| Panova2024, 2025, 2026 | FIB-SEM tomography of bonded interfacial area | Cu | Bonded fraction, recrystallization | M / A |
| Tiamiyu2022 Appl Surf Sci | TEM of oxide-layer delamination | — | Oxide as an energy sink | M (title via Schuh2026) |
| Sabard2018 (arXiv 1811.08694) | EBSD of coatings from heat-treated powder | Al 6061 | Dislocation accumulation at interfaces linked to better bonding | A |
| Standard adhesion tests (tubular coating tensile test standard; pull-off tests) | Coating-level adhesion | Any | Bulk outcome; no mechanism | M |

No bond-strength dataset exists that spans several materials at the single-particle level: Tang2024/2025
cover Al–Al only. So **no held-out material split is possible for bond strength today**.

---

## Q3. The zoo: existing models

| # | Model | Inputs | Form (as verified) | Assumptions / basis | Claimed validity | Reported accuracy | Level |
|---|---|---|---|---|---|---|---|
| Z1 | Assadi2003 linearised v_cr | ρ (g/cm³), T_m (°C), σ_u (MPa), T_i (°C) | v_cr = 667 − 14ρ + 0.08 T_m + 0.1 σ_u − 0.4 T_i (Eq. 3; Table 2 gives the derivatives per K, which is equivalent for differences). Not a fit: a first-order Taylor expansion around the Cu reference (v_cr,ref = 570 m/s). The derivatives come from FE sensitivities of the peak interface temperature T_max (Appendix A, Eq. A.3) | Bonding when ASI is reached at the particle surface; FE of Cu–Cu (and Al) impacts, 5–100 µm | Authors: "valid only for small changes of involved parameters"; for Al a full FE run is needed | Cu: FE 545–580 against 570 m/s experiment. Al: Eq. 3 gives ~620, full FE 675, experiment 660 m/s. Fig. 14 values for other materials are "for qualitative comparison" only | F |
| Z2 | Schmidt2006 generalized window | σ_u, ρ, c_p, T_m, T_i, d | v_cr = sqrt( 4F₁σ_u(1 − (T_i−T_R)/(T_m−T_R))/ρ + F₂ c_p (T_m − T_i) ), with v_cr ∝ d^(−n), n = 0.19 Cu, 0.14 316L | Fitting coefficients F₁, F₂ (values unverified); spray, ballistic and explosive-compaction data | Not verified | Not verified | S (form from Hall2015 F; n from Dowding2020 F) |
| Z3 | Schmidt2009 refinement; Assadi2011 parameter maps | v_p/v_cr = η; gas pressure and temperature | Coating properties as a unique function of η; constant-η contours on a gas-temperature × pressure plane | Cu as worked example | — | — | S |
| Z4 | Li2014 Eulerian window | V_f = sqrt(σ/ρ) | v_cr increases with the "material characteristic velocity" | Eulerian FE | — | — | S |
| Z5 | ASI simulation criteria (Grujicic2003/2004; Assadi2003) | Constitutive model, impact velocity | v_cr ≈ velocity at onset of shear localisation in FE | Johnson–Cook-type plasticity, adiabatic | Correlates with v_cr for several metals (as cited) | — | S |
| Z6 | Hydrodynamic / sound-speed law (HG2018a) | B, ρ (+ T*, d) | v_cr,ref = α·sqrt(B/ρ), α = 0.15 (experiments), 0.14 (simulations), ~10 µm matched pairs, room temperature; extension with sqrt-type dependence on T* = (T−T_room)/(T_m−T_room) and a weak size power law | Shock and release at the particle edge drive jetting; strength negligible against impact pressure | ~10 µm, matched, room temperature | Linear fit in Fig. 4 over Al, Cu, Ni, Zn (+ simulations) | F |
| Z7 | Spall-based jetting v_cr (HG2019 response; Lucas & Schuh 2025) | C₀, B, dynamic σ_y, tensile failure strain ε | v_cr ∝ C₀·(2σ_y ε / B)^0.5, with an arithmetic mean of particle and substrate properties for mismatched pairs | Jetting as a hydrodynamic spall process | Explains size, strength and temperature effects (claim) | — | S (form from Panova2026b F); A for HG2019 |
| Z8 | Size effect via jet temperature and spall strength (Dowding2020) | d, FE jet temperature | v_cr ∝ d^(−n), n = 0.19 Al, 0.21 Ti (±0.05) | Larger particles → hotter jet → lower spall strength | 5–50 µm | "Reasonable agreement" with LIPIT | F |
| Z9 | Impact-mode map (Hassani2020) | ρ, C₀, dynamic σ_y of both bodies | Dimensionless ratio; ~1: co-deformation; < 1/2: splatting; > 2: penetration | — | 9 dissimilar plus matched pairs | Observations on the map | S (Veysset2021 F) |
| Z10 | Melting limits: melting hinders adhesion (HG2017 PRL); melt-driven erosion velocity (HG2018c); erosion model (Lucas2025b); restricted melt enables bonding (Khan2026) | Thermal properties, velocity | Upper bound of the bonding window: an erosion velocity; adhesion fails where the interface is liquid unless the melt layer is nanoscale | Resolidification time against contact time | Sn, Zn, Al (erosion); alloys with eutectics (Khan) | — | S / A |
| Z11 | Oxide-controlled v_cr | Oxide thickness, particle size | Thicker oxide → higher v_cr for metal–metal contact; larger particles clean better | Peridynamics (Ren2024); LIPIT Al +14 % at +2–3 nm [Lienhard2020] | Cu, Fe (simulation) | — | A / S |
| Z12 | Growth-surface correction (Panova2026b) | Surface roughness, hardness | Particle–particle v_cr ≈ 1.3 × particle–substrate (Cu) | LIPIT on sprayed and polished surfaces | Cu, room temperature | Each factor 10–15 % | F |
| Z13 | Bond strength against velocity (Tang2025) | Velocity | Peak strength near 1.3 v_cr, then decline from elastic recovery and adiabatic softening | — | Al–Al | — | A |
| Z14 | DE from v_cr and velocity distribution (Zhang2025 reduced-order) | Gas T and p, particle size | DE = fraction of particles above v_cr(d); v_cr from the spall mechanism; impact velocity with a bow-shock correction | — | Calibrated on Al; 10 validation runs | "Remarkable agreement" (abstract) | S |
| Z15 | ML: Canales2020 energy-window classifier | Kinetic and thermal particle energy (CFD) | Classifier → critical total energy → DE | — | Cu, Al and others | "Acceptable accuracy" | S |
| Z17 | Vlcek2003 material eligibility ranking | Crystal structure (fcc > hcp > bcc), K·G against homologous temperature, Grüneisen parameter, Hugoniot elastic limit, T_m | Qualitative ranking. "Significantly more difficult" compactability above T_m ≈ 1600 °C; Zn, Al, Cu ideal; most Fe- and Ni-based materials hard at low process temperature | Shock physics (equations of state, HEL), FE impact pressures (up to 25 GPa at 1200 m/s), literature coating outcomes | Authors: "only a rough framework"; properties at 1–10 s⁻¹ and room temperature, the "main inaccuracy" | None quantitative | F |
| Z16 | ML: Wang2021 v_cr with feature selection; Hamrani2024 two-stage DE (Al 6061) | Process and material features | Black box | — | Within training data | Not verified | M / A |

**Gaps in the zoo** (what no model above does):
- No model states its own validity domain as an output. Domains are prose remarks (Z1 "small parameter
  changes", Z6 "~10 µm matched pairs at room temperature"). The closest thing is Z17, a qualitative
  eligibility ranking of materials, which is a domain statement about the process rather than about a model.
- No model has been tested on materials held out from its calibration, as far as I found. Z6 was fitted
  across materials (Al, Cu, Ni, Zn), which is the closest.
- None predicts the bonded area or bond strength across materials. Z13 covers one material.
- The single-particle to process gap (~40 % in v_cr per Panova2026b) has no quantitative model. Z12 covers
  one factor (growth surface), Chaban2021 another (substrate temperature).

---

## Source register

DOIs were checked on Crossref on 2026-11-03 unless marked otherwise.

| Key | Reference |
|---|---|
| Alkimov1990 | Alkimov, Kosarev, Papyrin, Sov. Phys. Dokl. 35(12) (1990) 1047–1049. No DOI; cited via Hall2015. |
| Assadi2003 | Assadi, Gärtner, Stoltenhoff, Kreye, Acta Mater. 51 (2003) 4379. doi:10.1016/s1359-6454(03)00274-x |
| Assadi2011 | Assadi et al., J. Therm. Spray Technol. 20 (2011) 1161. doi:10.1007/s11666-011-9662-9 |
| Assadi2016 | Assadi, Kreye, Gärtner, Klassen, Acta Mater. 116 (2016) 382. doi:10.1016/j.actamat.2016.06.034 |
| Assadi2019c | Assadi, Gärtner, Klassen, Kreye, Scripta Mater. 162 (2019) 512 (comment). doi:10.1016/j.scriptamat.2018.10.036 |
| Bae2008 | Bae, Xiong, Kumar, Kang, Lee, Acta Mater. 56 (2008) 4858. doi:10.1016/j.actamat.2008.06.003 |
| Canales2020 | Canales, Cano, Dosta, Surf. Coat. Technol. 401 (2020) 126143. doi:10.1016/j.surfcoat.2020.126143 |
| Chaban2021 | Chaban, Sun, Veysset, Nelson, Schuh, Appl. Phys. Lett. 119 (2021) 011903. doi:10.1063/5.0055274 (OSTI 1852492) |
| Dowding2020 | Dowding et al., Acta Mater. 194 (2020) 40. doi:10.1016/j.actamat.2020.04.044 (OSTI 1658603, accepted manuscript) |
| Dykhuizen1998 | Dykhuizen, Smith, J. Therm. Spray Technol. 7 (1998) 205. doi:10.1361/105996398770350945 (1-D isentropic nozzle model for particle velocity; harness, not zoo) |
| Gilmore1999 | Gilmore et al., J. Therm. Spray Technol. 8 (1999) 576. doi:10.1361/105996399770350278 |
| Grujicic2003 | Grujicic et al., Appl. Surf. Sci. 219 (2003) 211. doi:10.1016/s0169-4332(03)00643-3 |
| Grujicic2004 | Grujicic et al., Mater. Des. 25 (2004) 681. doi:10.1016/j.matdes.2004.03.008 |
| Hall2015 | Hall, Sarobol, Urrea, Beatty, "Microstructural characterization of cold sprayed Cu-W MMCs", SAND2015-3457C, OSTI 1251553 (slides reproducing Z1, Z2, Z4 and Alkimov's curves) |
| Hamrani2024 | Hamrani et al., Coatings 15 (2024) 12. doi:10.3390/coatings15010012 |
| Hassani2020 | Hassani, Veysset, Sun, Nelson, Schuh, Acta Mater. 199 (2020) 480. doi:10.1016/j.actamat.2020.08.038 |
| HG2017 | Hassani-Gangaraj et al., Phys. Rev. Lett. 119 (2017) 175701. doi:10.1103/physrevlett.119.175701 |
| HG2018a | Hassani-Gangaraj, Veysset, Champagne, Nelson, Schuh, Acta Mater. 158 (2018) 430. doi:10.1016/j.actamat.2018.07.065. Read as preprint arXiv:1612.08081 ("Supersonic impact of metallic micro-particles"); published text may differ |
| HG2018b | Hassani-Gangaraj et al., Scripta Mater. 145 (2018) 9. doi:10.1016/j.scriptamat.2017.09.042 |
| HG2018c | Hassani-Gangaraj et al., Nat. Commun. 9 (2018) 5077. doi:10.1038/s41467-018-07509-y |
| HG2019 | Hassani-Gangaraj et al., Scripta Mater. 162 (2019) 515 (response). doi:10.1016/j.scriptamat.2018.12.015 |
| HG2019b | Hassani-Gangaraj et al., Appl. Surf. Sci. 476 (2019) 528. doi:10.1016/j.apsusc.2019.01.111 |
| Hussain2009 | Hussain, McCartney, Shipway, Zhang, J. Therm. Spray Technol. 18 (2009) 364. doi:10.1007/s11666-009-9298-1 |
| Ichikawa2015 | Ichikawa, Ogawa, J. Therm. Spray Technol. 24 (2015) 1269. doi:10.1007/s11666-015-0299-y |
| Ichikawa2019 | Ichikawa, Tokoro, Tanno, Ogawa, Acta Mater. 164 (2019) 39. doi:10.1016/j.actamat.2018.09.041 |
| Imbriglio2019 | Imbriglio et al., Surf. Coat. Technol. 361 (2019) 403. doi:10.1016/j.surfcoat.2019.01.071 |
| Khan2026 | Khan, Schuh, Acta Mater. 306 (2026) 121888. doi:10.1016/j.actamat.2025.121888 (OSTI 3367681) |
| Legoux2007 | Legoux, Irissou, Moreau, J. Therm. Spray Technol. 16 (2007) 619. doi:10.1007/s11666-007-9091-y |
| Li2006 | Li, Li, Liao, J. Therm. Spray Technol. 15 (2006) 212. doi:10.1361/105996306x108093 |
| Li2014 | Li, Yu, Wang, Yin, Liao, J. Therm. Spray Technol. 23 (2014) 557. doi:10.1007/s11666-013-0023-8 |
| Lienhard2020 | Lienhard et al., Acta Mater. 197 (2020) 28. doi:10.1016/j.actamat.2020.07.011 |
| Lucas2025 | Lucas, Schuh, Int. J. Mech. Sci. 303 (2025) 110676. doi:10.1016/j.ijmecsci.2025.110676 |
| Lucas2025b | Lucas, Barton, Saunders, Schuh, Acta Mater. 301 (2025) 121488. doi:10.1016/j.actamat.2025.121488 |
| Murray2025 | Murray et al., J. Therm. Spray Technol. (2025). doi:10.1007/s11666-025-02085-2 (OSTI 3009523) |
| Panova2026a | Panova, Schuh, Materialia 46 (2026) 102742. doi:10.1016/j.mtla.2026.102742 (OSTI 3367627) |
| Panova2026b | Panova, Roper, Kracum, Schuh, Materialia (2026) 102788. doi:10.1016/j.mtla.2026.102788 (OSTI 3376515) |
| Price2026 | Price et al., "HUGO-CS", arXiv:2605.04257; data at github.com/sprice134/HUGO (dataset CC-BY per paper; code Apache-2.0 per README) |
| Raletz2006 | Raletz, Vardelle, Ezo'o, Surf. Coat. Technol. 201 (2006) 1942. doi:10.1016/j.surfcoat.2006.04.061 |
| Reiser2024 | Reiser, Schuh, Acta Mater. 281 (2024) 120301. arXiv:2404.05601 (OSTI 2437835) |
| Ren2024 | Ren, Song, arXiv:2403.01311 (peridynamics, oxide and size) |
| Sabard2018 | Sabard, Hussain, arXiv:1811.08694 |
| Schmidt2006 | Schmidt, Gärtner, Assadi, Kreye, Acta Mater. 54 (2006) 729. doi:10.1016/j.actamat.2005.10.005 |
| Schmidt2009 | Schmidt et al., J. Therm. Spray Technol. 18 (2009). doi:10.1007/s11666-009-9357-7 |
| Schuh2026 | Schuh, Final Technical Report DE-SC0018091 (2026). doi:10.2172/3367728 (OSTI 3367728) |
| Stoltenhoff2002 | Stoltenhoff, Kreye, Richter, J. Therm. Spray Technol. 11 (2002) 542. doi:10.1361/105996302770348682 |
| Sun2020 | Sun, Veysset, Nelson, Schuh, J. Appl. Mech. 87 (2020). doi:10.1115/1.4047206 |
| Tang2024 | Tang, Veysset, Assadi, Ichikawa, Hassani, Nat. Commun. 15 (2024) 9630. doi:10.1038/s41467-024-53990-z |
| Tang2025 | Tang, Ichikawa, Hassani, PNAS 122 (2025). doi:10.1073/pnas.2424355122 |
| Veysset2021 | Veysset et al., Appl. Phys. Rev. 8 (2021) 011319. doi:10.1063/5.0040772 (arXiv:2012.08402) |
| Vlcek2003 | Vlcek, Gimeno, Huber, Lugscheider, ITSC 2003, pp. 37–44. doi:10.31399/asm.cp.itsc2003p0037 (journal version: J. Therm. Spray Technol. 14 (2005) 125, doi:10.1361/10599630522738; the PDF read is the 8-page proceedings version) |
| Wang2021 | Wang, Cai, Chen, Ali, Jin, J. Therm. Spray Technol. 30 (2021) 1213. doi:10.1007/s11666-021-01198-8 |
| Zhang2024 | Zhang, Li, Yang, Huang, Surf. Coat. Technol. 478 (2024) 130492. doi:10.1016/j.surfcoat.2024.130492 (via Panova2026b) |
| Zhang2025 | Zhang, Molla, Brandl et al., J. Manuf. Process. 134 (2025) 547. doi:10.1016/j.jmapro.2024.12.077 |
