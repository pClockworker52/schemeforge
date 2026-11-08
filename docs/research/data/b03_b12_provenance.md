# Provenance of the B03 and B12 impact data (citations only)

WSL B task 2026-11-08-b6. This file gives citations and yes/no answers only. It contains no velocities and no
outcomes, and any quotes that held either have been paraphrased without them. Page numbers are the page numbers of
the accepted manuscripts.

| Paper | PDF used (same as task b5) | sha256 |
|---|---|---|
| B03, Tiamiyu, Sun, Nelson, Schuh, Acta Mater. 202 (2021), doi:10.1016/j.actamat.2020.10.057 | accepted manuscript, `coldspray-papers/B03_Tiamiyu_2021_am.pdf` | `fcfb76f54118bc8a4e2bc0689bffd4760475c958dc2d0f27a7df35dfdb8a2fc6` |
| B12, Tiamiyu, Schuh, Surf. Coat. Technol. (2020) 126386, doi:10.1016/j.surfcoat.2020.126386 | accepted manuscript, `coldspray-papers/B12_Tiamiyu_2020_am.pdf` | `82f236e59d48093d8b33a0d242c6d10fb9fbe6580fca7977ba1dd15e57a33bb6` |

## 1. B12 refs. [27] and [31]

- **[27]** M. Hassani-Gangaraj, D. Veysset, K.A. Nelson, C.A. Schuh, "In-situ observations of single micro-particle
  impact bonding", Scr. Mater. 145 (2018) 9–13, doi:10.1016/j.scriptamat.2017.09.042. **This is HG2018b.**
- **[31]** M. Hassani-Gangaraj, D. Veysset, K.A. Nelson, C.A. Schuh, "Impact-bonding with aluminum, silver, and gold
  microparticles: Toward understanding the role of native oxide layer", Appl. Surf. Sci. 476 (2019) 528–532,
  doi:10.1016/j.apsusc.2019.01.111.

## 2. B12: new or reused impacts?

**Al: reused.** "LIPIT data for the Al particles that we analyze here can be found in Refs. [27,31]." (p. 6)

**Cu: new, by the paper's statement.** "LIPIT data for Cu particles of about the same size are also available in
Ref. [27], although here we present analysis of particles that were newly subjected to LIPIT at MIT for a related
study that will be published in the future." (p. 6)

**Both, for the paper overall.** "We study particles that were previously subjected to testing in the LIPIT
single-particle tester described in Refs. [27,30]." (p. 5; [30] = Veysset et al., Sci. Rep. 6 (2016), the LIPIT
method paper.)

The acknowledgements thank "M. Hassani-Gangaraj, D. Veysset, and Y. Sun (all of MIT) for providing the LIPIT-tested
particles as well as some SEM images of the Al particles" (p. 22). The B12 authors therefore analysed impact sites
that others had launched.

## 3. B03: new or reused impacts?

B03 does not say in so many words that its Cu impacts are new. Its methods section describes its own LIPIT set-up
and launch campaign: "We use LIPIT-launched copper particles in an extensive site-specific study…" (p. 4), and
Sec. 2 (pp. 4–5). Two places use data from earlier work:

- **Fig. 3 caption (p. 8, a plot of rebound data):** "Open data points were taken from previous work in Ref. [26]."
  [26] = Y. Sun, D. Veysset, K.A. Nelson, C.A. Schuh, "The transition from rebound to bonding in high-velocity
  metallic microparticle impacts: jetting-associated power-law divergence", J. Appl. Mech. 87 (2020) 091002.
- **Sec. 4.1.3, rim-deflection measurements (p. 16):** "We note that some of these data were originally reported
  in a prior work and are reproduced here for completeness [40]." [40] = A.A. Tiamiyu, C.A. Schuh, "Particle
  Flattening during Cold Spray: Mechanistic Regimes Revealed by Single Particle Impact Tests", Surf. Coat. Technol.
  (2020), cited as accepted. **This is B12.**

**Observation (mine, not a statement of either paper):** B12 says its Cu particles were "newly subjected to LIPIT
… for a related study that will be published in the future". B03 reproduces some B12 data and has the same first
author and the same suppliers. Neither paper says outright that the two Cu datasets share impact sites. Even so,
B03 and B12-c1 are probably not independent, and B12's Cu sites are probably B03's, at least in part.

## 4. Do B03 or B12 cite HG2018a or HG2018b?

| Paper | HG2018b (Scr. Mater. 145, 9) | HG2018a (Acta Mater. 158, 430) |
|---|---|---|
| B03 | **yes, ref. [22]** | **yes, ref. [9]** |
| B12 | **yes, ref. [27]** | no (not in the reference list) |

**B03 [22], HG2018b, cited for:**
- *Method:* LIPIT as the platform for single-particle impacts (p. 3), and the details of LIPIT and the launch pad,
  together with [23] (p. 5).
- *Prior findings:* listed among earlier LIPIT work on determining v_cr and observing jetting in matched metal
  systems (p. 3).
- *Comparison:* B03's own Cu result is compared with the value reported in [22] for Cu of similar particle size,
  and with [26] (p. 7). The values and the outcome of the comparison are not reported here.

**B03 [9], HG2018a, cited for:**
- *Mechanism only:* pressure release at a free surface and jetting when the induced tension exceeds the dynamic or
  spall strength (p. 2), together with [7] and [10].
- *Mechanism only:* jetting onset when the shock speed exceeds the collision-point velocity (p. 13).
- *Mechanism only:* the particle rim flowing laterally under azimuthal tension (p. 16).
- It is not cited for data.

**B12 [27], HG2018b, cited for:**
- *Background:* possible particle–particle interactions in the cold-spray stream, with [26] (p. 4).
- *Method:* the LIPIT single-particle tester, with [30] (p. 5).
- *Data:* the source of the Al LIPIT data B12 analyses, with [31] (p. 6). This is the use the task asked about.
- *Data, not used:* a source of Cu LIPIT data for particles of about the same size, which B12 explicitly does not
  use (p. 6).

## 5. Powder and plate lots

**Neither paper states that its powder or plates come from the same batch or lot as earlier work.** Both give only
the suppliers:
- B03: Alfa Aesar Cu powder and an OnlineMetals Cu plate (p. 4).
- B12: Alfa Aesar Cu, Valimet Al, and OnlineMetals Cu and Al plates (p. 5).

B12's Al impacts are reused from [27] and [31] (item 2), so those Al particles and substrates are by construction
the materials of those papers. B12 does not describe that as a batch statement.

## Summary for the B4 exposure log

| Condition | Impact data from | Overlap with HG2018b |
|---|---|---|
| B12-c2 (Al on Al) | reused from [27] = HG2018b and [31] = HG2019 Appl. Surf. Sci. | **yes, by the paper's own statement** |
| B12-c1 (Cu on Cu) | stated as newly launched for a future related study | none stated; HG2018b Cu data named but not used. Probably shared with B03 (see item 3) |
| B03-c1 (Cu on Cu) | its own campaign; some rebound points from [26] (Sun 2020) and some rim data from [40] (= B12) | HG2018b used only as a method and comparison reference |
