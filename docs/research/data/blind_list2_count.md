# Blind list 2: metadata count (WSL B task 2026-11-23-b13)

**N_v = 7** (1 yes, 12 half). **N_q = 1.5** (1 yes, 1 half).

Definitions and stop rule: [../r1-status-2026-11-23.md](../r1-status-2026-11-23.md) §5. The stop rule is the
modeller's to apply; it is not judged here. Rows: [blind_list2_candidates.csv](blind_list2_candidates.csv) (29 titles:
everything counted, plus the near misses as `no` so that the classification can be checked).

## How the count was made

- **Source:** Crossref REST API, 2026-11-21, with `select=DOI,title,author,issued,container-title,type`, so no
  abstract was returned. Publication dates 2019-01-01 to 2026-12-31.
- **Queries:** about 78 in total.
  - Topic queries: LIPIT, microparticle or single-particle impact, critical, bonding or adhesion velocity, rebound to
    bonding, oxide, substrate, heat-treated powder.
  - Author queries for the single-impact groups: Hassani, Schuh, Veysset, Tiamiyu, Lienhard, Ichikawa, J.-H. Lee,
    Müftü, Champagne and others.
  - A final sweep limited to 2024-06 to 2026.
  - 4,252 records came back (3,964 unique DOIs). They were narrowed by title keywords and then classified by hand from
    the title and venue only. The last sweeps returned only titles already seen.
- **Nothing was opened:** no abstract and no full text. Crossref returned no snippets, and no title contained a
  velocity value.
- **Classification:**
  - `yes` means the title names the rebound/bonding transition or the critical velocity of single metallic particles,
    or a single-impact series that implies one.
  - `half` means single-impact bonding is plausible, but the title does not name a threshold, or does not make clear
    whether the work is single-particle or experimental.
  - `no` means a deposit-level study, a method paper, a regime above bonding, a non-metal, or probable modelling.
- **Reviewed** by a separate agent before commit (classification, counts, missed titles, exposure against the
  repository). Its corrections are applied: two counted papers turned out to be exposed, and one missed title is added.

## N_q

- N_q is counted only among N_v papers.
- **Mohanty 2022:** an oxide-thickness series within Al, so `yes`. The series could be partly simulated; the title
  does not say.
- **Li 2026:** a grain-size series of metallic microparticles, so `half`. Grain size stands in for particle strength,
  and the title does not say whether the particle or the substrate is varied. Read strictly, N_q would be 1.0.
- **Not found:** a substrate series of one metal or a temper series of single particles (other than exposed papers,
  below). Sabard 2019 and Williamson 2024 vary the powder heat treatment, but by title they are deposit-level studies,
  so `no`.

## Not counted

- **List 1 papers:** every list-1 paper except B11 appeared in the results, and all were skipped.
- **Excluded as exposed:**
  - Tang 2025 (PNAS), Panova 2024 (Acta Mater.) and HG2018b.
  - HG2019b (Appl. Surf. Sci., Al/Ag/Au): read in full, values in vcr_lipit.csv.
  - Hassani 2020 (Acta Mater., with its SSRN preprint and corrigendum), Dowding 2020 and Chaban 2021: rows in
    vcr_lipit.csv.
  - Panova 2026b (Materialia 102788, a substrate-hardness series of Cu, values in vcr_lipit.csv). It would otherwise
    have been an N_q paper.
  - Panova 2026a (Materialia 102742) and Reiser 2024, both read.
  - **Sun 2020** (J. Appl. Mech. 87, 10.1115/1.4047206, "rebound to bonding"):
    - its abstract was read (coldspray-data-and-zoo.md row 49);
    - B03 uses its Cu rebound points and compares its v_cr with it (b03_b12_provenance.md);
    - the Panova thesis quotes a v_cr range citing it (panova2024_ch2.md).
    - Excluded as exposed and not independent of B03, as B12-c1 was treated. Before review it was counted `yes`.
  - **Tang 2024** (Nat. Commun., "strength gradient"): read on 2026-11-20 (tang2024_reading.md), which states no v_cr
    in the main text. Before review it was counted `half`.
- **Not single-impact experiments:**
  - modelling papers;
  - reviews and book chapters (Veysset 2021 and 2024, Lee 2023);
  - launcher and method papers (Veysset 2020, Gu 2022, Song 2025, Chen 2025);
  - LIPIT uses other than bonding (hardness, dislocation drag, Kajihara texturing);
  - polymer and ceramic particles.

## Exposure log (seen_values)

- **Khan 2026 (Acta Mater. 121888):** the modeller already read its abstract (coldspray-data-and-zoo.md row 55; no
  value). It is counted `half` here. Whether an abstract read excludes a paper is Peter's call; if it does, N_v = 6.5.
- **Mohanty 2022:** its title, and one qualitative statement citing it, were seen in B06 (ref. [34], p. 3). No value.
- **Tiamiyu 2022 (Appl. Surf. Sci.):** its conclusion is already in the B4 log of list 1 (2026-11-05). No value.
- **Tiamiyu 2022 (Nature Mater.):** its starting grain sizes reached the modeller on 2026-11-20. No v_cr.
- **Tang 2024 (now excluded):** I read the full text of B06 during task b12, and B06 cites Tang 2024 for a location on
  the interface. It is not a velocity.
- No other value reached me.

## For the modeller

- **Two Tiamiyu 2022 papers:** the R1 note's "Tiamiyu et al. 2022 (Nature Mater.)" merges them.
  - Appl. Surf. Sci. 151673, on oxide delamination: the paper of the 2026-11-05 B4 log, counted `half`.
  - Nature Mater., 10.1038/s41563-022-01250-0, on DRX: the source of the 2026-11-20 grain-size exposure. Its title
    names no bonding, so `no`.
- **Halves at the `no` edge:** Nastic 2021, Song 2021 and Sugihara 2021. By title they point to process splats,
  deposit adhesion and a conference abstract.
- **What halves usually yield:** most halves are titles about bonding behaviour that do not name a threshold. On list 1,
  of 16 papers, 4 clearly reported a v_cr and 2 more (B03, B12) were "yes or unclear" at step 1.
