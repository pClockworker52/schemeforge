# Cold spray: literature-blind hold-out set (frozen)

Frozen 2026-11-03 (DECISIONS "Cold-spray track: local first"). Built from titles, venues and DOIs (Crossref
metadata) only. No abstract or full text of a listed paper has been opened for this purpose. The commit of this
file is the timestamp.

## Purpose

All data in `data/vcr_lipit.csv` have been seen. These papers have not. Models and simulation setups are frozen
first, then these papers are read and scored. This is weaker than a new experiment (exposures below), but it is
out-of-sample evidence that can be produced locally.

## Rules

- **B1.** No listed paper is opened (abstract or full text) before the predictions for it are frozen and
  committed. Crossref metadata (title, venue, year, DOI) is allowed.
- **B2, two-step extraction.** Inputs and outputs sit in the same paper, so extraction is role-separated:
  - **Step 1:** someone other than the modeller (Peter, or an agent Peter approves that reports inputs only)
    extracts the inputs: materials, temper, oxide state, particle size, substrate preparation, temperatures,
    and any strength or property data. Measured critical velocities, restitution data and figures showing them
    are not passed on.
  - **Step 2:** predictions are frozen and committed.
  - **Step 3:** outputs are extracted into `data/vcr_lipit.csv` with prefix `B-` and scored.
- **B3.** Scoring follows the frozen rules of the retrospective test (P1, P2, Q, S1–S3, D1), with models and
  simulation setups as committed at step 2. A material that a model was calibrated on is flagged in-sample
  even when the condition is new.
- **B4.** Any value from a listed paper that reaches the modeller before step 2 is logged below, and the
  affected rows are reported separately.
- **B5.** The list is closed. Papers found later go to a new list with its own freeze date.
- **B6 (adopted 2026-11-04, DECISIONS "Blind test rule B6").** If a paper prints no window bounds and they cannot
  be digitized, the window is v_cr ± the paper's stated velocity uncertainty. If no uncertainty is stated, only
  sign- and rank-based verdicts are scored. B6 applies only to papers whose predictions are frozen after
  2026-11-04; B10 stays scored as in coldspray-results-b10.md.

## Hold-out papers (experimental, single-particle, metallic)

| # | Year | First author | Title (abridged) | Venue | DOI | Known exposure |
|---|---|---|---|---|---|---|
| B01 | 2024 | Lucas | Microstructure effects on high velocity microparticle impacts of copper | Acta Mater. 280 | 10.1016/j.actamat.2024.120329 | none |
| B02 | 2025 | Lucas | Single particle impact study on substrate strength and ductility | Int. J. Mech. Sci. 303 | 10.1016/j.ijmecsci.2025.110676 | Panova2026b quotes "half-hard Cu v_cr 539–588 m/s" from B02, B03 and HG2018b together |
| B03 | 2021 | Tiamiyu | Site-specific study of jetting, bonding and local deformation | Acta Mater. 202 | 10.1016/j.actamat.2020.10.057 | as B02 |
| B04 | 2022 | Lienhard | Tin and zinc microparticle impacts above the critical adhesion velocity | Surf. Coat. Technol. 432 | 10.1016/j.surfcoat.2021.128053 | Sn and Zn v_cr already in the table from other papers |
| B05 | 2022 | Chen | Additional hindrances to metallurgical bonding from impurities | Surf. Coat. Technol. | 10.1016/j.surfcoat.2022.128114 | none |
| B06 | 2026 | Wu | Mechanisms of oxide layer fracture during microparticle impact bonding | Scripta Mater. | 10.1016/j.scriptamat.2026.117444 | none |
| B07 | 2025 | Liu | Impact bonding between titanium particle and substrate | Surf. Interfaces | 10.1016/j.surfin.2025.107537 | none (may be simulation only) |
| B08 | 2026 | Chen | Substrate surface roughness and single-particle impact, bonding and critical velocity | Results Surf. Interfaces | 10.1016/j.rsurfi.2026.100939 | none |
| B09 | 2025 | Ağır | Single-particle impact of Ti6Al4V and Ti-5553 in cold spray | J. Therm. Spray Technol. | 10.1007/s11666-025-02063-8 | none (may be wipe tests, i.e. process quantity) |
| B10 | 2025 | Na | Single particle impact explorations on powder heat treatments | J. Mater. Res. Technol. 36 | (title via Schuh2026; DOI to fetch) | none |
| B11 | 2019 | Imbriglio | Adhesion strength of titanium particles to alumina substrates | Surf. Coat. Technol. 361 | 10.1016/j.surfcoat.2019.01.071 | a web-search summary gave ~580 m/s (Ti on alumina) |
| B12 | 2020 | Tiamiyu | Particle flattening during cold spray: single particle impact tests | Surf. Coat. Technol. | 10.1016/j.surfcoat.2020.126386 | none |
| B13 | 2024 | (OSTI 2377827) | Surface oxide and impact ratio dictate interfacial adhesion of cold spray bulk metallic glass single particles | Surf. Coat. Technol. | 10.1016/j.surfcoat.2024.131057 | none; amorphous, so a domain-claim test |
| B14 | 2020 | Lienhard | Surface oxide and hydroxide effects on aluminum microparticle impact bonding | Acta Mater. 197 | 10.1016/j.actamat.2020.07.011 | relative effect seen (+14 % at 95 % RH) via Veysset2021; absolute values not seen |
| B15 | 2025 | Khan | Eutectic melting of alloy microparticles upon low velocity impact | Scripta Mater. 265 | 10.1016/j.scriptamat.2025.116763 | none (may contain no v_cr) |
| B16 | 2024 | Kajihara | Velocity measurement method for a microparticle projectile and high-speed impact testing | Acta Mater. | 10.1016/j.actamat.2023.119467 | none (may contain no v_cr) |

Excluded as already exposed: Tang2025 (Al v_cr 800 m/s seen in the abstract), Panova2024 (Cu 540 m/s quoted in
Panova2026b), HG2018b (values quoted in three papers read).

## Model and simulation papers, unread (zoo candidates)

Read only after the blind scoring, because they may quote measured values: Palodhi 2020 (J. Therm. Spray
Technol., v_cr vs material properties, 10.1007/s11666-020-01105-7); Wiehler 2024 (J. Therm. Spray Technol.,
calibration of the critical velocity description, 10.1007/s11666-024-01892-3); Moonga 2024 (engrXiv, interfacial
energy at v_cr, 10.31224/3491); Hirmand 2024 (J. Therm. Spray Technol., particle-based bonding model,
10.1007/s11666-024-01803-6); Suresh 2020 (Acta Mater., mesoscale jet initiation, 10.1016/j.actamat.2019.10.039);
Zhang 2025 (J. Therm. Spray Technol., peridynamic v_cr and spray-angle window, 10.1007/s11666-025-02097-y); Sandhu
2026 (preprint, simulation of rebound, flattening and penetration regimes, 10.21203/rs.3.rs-8930301/v1).

## Access (to be checked at step 1, by the extractor)

Schuh-group papers often have accepted manuscripts on OSTI. J. Mater. Res. Technol. and Results in Surfaces and
Interfaces are open access. The rest via Peter.
