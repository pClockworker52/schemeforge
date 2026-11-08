# Tasks for WSL B (extraction)

Procedure: [../coldspray-procedure.md](../coldspray-procedure.md). Pull `claude/exciting-fermi-qy077p`, do the
newest open task, push to the branch named in the task. Write only the files the task names. Blind rules
(coldspray-blind-literature.md) bind you as before.

## Task 2026-11-05-b1: Na et al. 2025 (B10), Eq. 6 (closed: done in the cloud session from Peter's PDF, docs/research/coldspray-reading-na2025.md)

B10 is unblinded and scored, so the full text may be read. From your PDF (sha256 a4cdccfe...), extract:
1. Eq. 6 (the combined strength + oxide model) **exactly as printed**, with every symbol defined as in the paper;
2. its fitted constant(s), with how and on which data they were fitted;
3. the reference(s) it builds on (the Lienhard rule of mixtures), as citations only. Do **not** report anything from
   B14 (Lienhard 2020) beyond what Na et al. print about its model form.

Write `docs/research/data/na2025_eq6.md` on branch `coldspray/b10-eq6` and push.

## Task 2026-11-07-b2: step 3, outcomes of B02 and B14 (closed: add80b8, scored)

Predictions are frozen: commit 27e7eea (`docs/research/coldspray-preregistration-b02-b14.md`,
`docs/research/data/predictions_b02_b14.csv`) and the CS-16 addendum in the commit that adds this task
(`docs/research/data/predictions_b02_cs16.csv`). Do not edit those files or any code.

Use the step-3 prompt (`docs/research/coldspray-extraction-prompt-step3.md`) with these changes:
- **Papers and rows:** B02 conditions c1, c2 → ids `B-B02-c1`, `B-B02-c2`; B14 conditions c1 … c8 → ids
  `B-B14-c1` … `B-B14-c8`, matching `blind_inputs.csv`.
- **Source:** the same thesis chapters you used in step 1 (Lucas 2025 ch. 4 for B02; Lienhard 2022 ch. 2 for B14).
  Say in `read_from` which table, figure or page.
- **Window:** v_cr_low / v_cr_high / v_cr_mid exactly as printed, and `vcr_definition` exactly as the source defines
  it. If no bounds are printed, leave them blank and write the stated velocity uncertainty in `notes` in exactly
  this form: `velocity uncertainty +-X m/s` or `velocity uncertainty +-X %` (rule B6; the scoring script reads it). If
  values exist only in a figure, digitize them and say so (`digitized (+-x m/s)`).
- **Notes:** the items withheld in step 1. For B02: Table 2 of ch. 4 (failure strain, bulk sound speed, bulk
  modulus). For B14: the treatment table (thesis Table 2.1). Also anything the source says about why the
  conditions differ.
- **Interface observations** (oxide fracture, fragments, bonded-area maps) may now be recorded in `notes`. They are
  outcomes, and these papers are frozen.

Commit only `docs/research/data/vcr_lipit.csv` on a new branch `coldspray/b02-b14-outcomes` from
`claude/exciting-fermi-qy077p`, push, and stop. **Do not merge into `claude/exciting-fermi-qy077p`;** the modeller
merges after the scoring script is committed.

## Task 2026-11-07-b3: Panova PhD thesis (MIT DMSE 2026): screen, then the Panova2026a chapter

**Source:** Peter's PDF `C:\Users\peter\schemeforge\panova-vpanova-phd-dmse-2026-thesis Veera Panova.pdf` (in WSL:
`/mnt/c/Users/peter/schemeforge/`). Do not commit the PDF. Report its sha256.

**Why you and not the modeller:** the thesis probably contains the two Panova & Schuh 2024 papers (candidates for a
blind list 2) and quotes pending blind papers in its review. The modeller wants only Panova2026a (Panova & Schuh,
Materialia 46 (2026) 102742, doi:10.1016/j.mtla.2026.102742: two-particle Cu stacks, bonded fraction of the
particle–particle interface by FIB tomography). Rules B1–B6 bind you as before. Pending blind papers (predictions not
frozen): **B03, B05, B06, B07, B12, B16** (coldspray-blind-literature.md).

### Part 1: screen (yes/no only, no values)

Write `docs/research/data/panova_thesis_screen.md` with:
1. Title, author, year, degree, page count, sha256.
2. Chapter list. For each chapter, the publication it corresponds to (citation only), or "none".
3. For each of **B03, B05, B06, B07, B12, B16:** is it cited (yes/no)? Does the thesis reproduce a numeric value
   from it (critical velocity, window, oxide thickness, bonded fraction)? Answer yes/no, with page numbers but
   **without the value**.
4. For each **Panova & Schuh 2024** paper: is it a chapter (yes/no, which)? Does it contain (a) critical velocities
   on oxide layers of different thickness but the same oxide type, or (b) bonded-area or interface maps against
   impact velocity? Answer yes/no only. Do not report anything else from these chapters.
5. **Panova2026a:** which chapter, and do its pages reproduce values from the pending blind papers (yes/no, pages)?
   **Panova2026b:** which chapter (already seen, so no restriction).

Commit part 1 on its own.

### Part 2: the Panova2026a chapter (only if part 1, item 5 allows it)

If the chapter quotes values from pending blind papers, cut those passages (note page and paragraph, not content) and
extract the rest. If you cannot separate them, stop after part 1 and say why.

Write `docs/research/data/panova2026a_stacks.md` with:
- **Set-up:** powder (material, temper, size and spread, oxide state if stated), substrate, how the stacks were
  made (first particle on the substrate, second on the first; lateral offset), LIPIT details, velocity uncertainty.
- **What was measured and how:** FIB tomography, slice spacing, how "bonded" is defined, how the bonded fraction is
  computed, and its stated uncertainty.
- **Results:** for each specimen, impact velocities of particle 1 and particle 2, sizes, and the bonded fractions of
  the substrate–particle and particle–particle interfaces. Use the printed tables. If values exist only in figures,
  digitize them and say so (`digitized (+-x)`, with axis calibration).
- **The authors' interpretation**, in two or three sentences, labelled as theirs.
- **Supplementary or thesis-only material** (data not in the journal paper), flagged as such.

Exclude: anything from the Panova & Schuh 2024 chapters; values from pending blind papers.

### Delivery

Branch `coldspray/panova-thesis` from `claude/exciting-fermi-qy077p`. Commit only the two files above (part 1, then
part 2), push, and stop. **Do not merge;** the modeller leak-scans and merges.

## Standing rule for fetching papers (from 2026-11-07)

You may fetch papers yourself, but only from legitimate open copies, in this order: MIT DSpace (search by title),
OSTI, arXiv, an author or institutional page, then the publisher's free-to-read version (in a browser if scripted
downloads are blocked). Nothing paywalled, and no shadow libraries. For each PDF, record the URL, the version
(accepted manuscript or published; values can differ) and its sha256 in your result file. Never commit a PDF. List
anything you could not obtain, so Peter can ask for it.

## Task 2026-11-07-b4: powder properties from three theses

**Why:** no LIPIT powder in the repository has a measured failure strain or hardening exponent, and only three row
groups have any strength value for the impacted powder (inventory: `docs/research/data/README.md`, "Particle-property
gap inventory"). Z7 (spall law) and the strength terms of CS-10 and Z18 need them.

**Sources** (you used the first and third before; the second is Peter's copy, sha256 `5a809e42…0538b00`):
1. Lucas PhD thesis (MIT, 2025): ch. 3 (Cu-on-sapphire impacts, the 383 ± 65 MPa dynamic yield strength of the
   19 µm Alfa Aesar Cu powder) and ch. 4 Table 2 (Y_d, C₀, B, failure strain ε_c per material). **Key question: does
   Table 2, or any part of ch. 3–4, give a failure strain, hardening exponent or stress–strain curve for the
   powder itself**, not only for the soft and hard plates?
2. Panova PhD thesis (MIT, 2026): ch. 3 and 4 (Cu-on-Cu impacts, 15–38 µm Alfa Aesar Cu). **Do not read pp. 56–57 or
   p. 146** (values from the pending blind paper B03).
3. Lienhard PhD thesis (MIT, 2022): the Al powders of ch. 2 (B14) and the Sn and Zn powders of B04.

**Report, per powder** (manufacturer, nominal and measured size, which chapter or paper uses it):
- hardness (method, load);
- dynamic yield strength Y_d, and how it was obtained (CoR fit, sapphire impacts, other);
- static or tensile strength, and how (micro-compression, nanoindentation, bulk handbook);
- failure strain, hardening exponent n, or a stress–strain curve (if only a figure: digitize it, with axis
  calibration and reading error);
- grain size and temper, if stated.

Do the same for the substrates where a thesis gives a failure strain or n.

**Do not report:** critical velocities; bonding or rebound outcomes; and any value attributed to a pending blind
paper (B03, B05, B06, B07, B12, B16). For those, give the citation and page only, flagged `pending blind paper`.

**Write** `docs/research/data/powder_properties_theses.md` on a new branch `coldspray/powder-properties` from
`claude/exciting-fermi-qy077p`. Commit only that file, push, and stop. **Do not merge.**

## Task 2026-11-07-b5: step 1 for B03, B05 and B12 (fetch them yourself)

**Why:** Alex has not sent the PDFs yet. OpenAlex lists these three as free to read on the publisher's site
("bronze"); B06, B07 and B16 are closed and still need Alex.

| Id | Paper | DOI |
|---|---|---|
| B03 | Tiamiyu 2021, site-specific study of jetting, bonding and local deformation, Acta Mater. 202 | 10.1016/j.actamat.2020.10.057 |
| B05 | Chen 2022, additional hindrances to metallurgical bonding from impurities, Surf. Coat. Technol. | 10.1016/j.surfcoat.2022.128114 |
| B12 | Tiamiyu 2020, particle flattening during cold spray: single particle impact tests, Surf. Coat. Technol. | 10.1016/j.surfcoat.2020.126386 |

1. **Fetch** under the standing rule above. Your earlier scripted attempt was blocked by the publisher, so try MIT
   DSpace first (B03 and B12 are MIT papers), then the publisher's page in a browser. If a paper cannot be
   obtained, leave its `-pending` row and write why in `access`.
2. **Step 1** exactly as `docs/research/coldspray-extraction-prompt.md` says: inputs only, nothing that reveals or
   hints at an outcome. Replace the rows `B03-pending`, `B05-pending` and `B12-pending` in
   `docs/research/data/blind_inputs.csv` with one row per condition (`B03-c1`, …).
3. Under the access column, give the URL, version and sha256 of the PDF you used.

Commit only `docs/research/data/blind_inputs.csv` on a new branch `coldspray/blind-inputs-b03-b05-b12` from
`claude/exciting-fermi-qy077p`, push, and stop. **Do not merge;** the modeller leak-scans and merges.

Order: do b5 first (it unblocks the blind test), then b4.

## Task 2026-11-08-b6: where do the B03 and B12 data come from? (citations only)

**Why:** B03 and B12 use the same suppliers as HG2018b (Alfa Aesar ~10 µm Cu, Valimet Al, OnlineMetals 3.175 mm
plates), which the modeller has read (rows P18). B12-c2 says its Al impacts are "LIPIT data from the authors' earlier
refs. [27,31]". If those impacts are HG2018b's, their v_cr is already seen, and B12-c2 is exposed. This must be
settled before predictions are frozen (B4 exposure log, entry of 2026-11-07).

From the PDFs you used in task b5 (sha256 in `blind_inputs.csv`), report **citations and yes/no answers only, no
values**:
1. **B12 refs. [27] and [31]:** full citations (authors, year, journal, volume, pages, DOI).
2. **B12, Cu and Al separately:** does the paper say its impacts are new, reused from earlier work, or both? Quote
   the sentence (it must not contain a velocity or an outcome; if it does, paraphrase without them) and give the
   page.
3. **B03:** the same question. Are its Cu impacts new, or taken from earlier work (which refs)?
4. **B03 and B12:** does either paper cite HG2018b (Hassani-Gangaraj et al., Scripta Mater. 145 (2018) 9,
   doi:10.1016/j.scriptamat.2017.09.042) or HG2018a (Acta Mater. 158 (2018) 430)? Give the reference numbers, and say
   for what each is cited (method, data, comparison), without values.
5. **Powder and plate lots:** does either paper say its powder or plates are the same batch as in earlier work?

Write `docs/research/data/b03_b12_provenance.md` on a new branch `coldspray/b03-b12-provenance` from
`claude/exciting-fermi-qy077p`. Commit only that file, push, and stop. **Do not merge.**

## Task 2026-11-08-b7: Panova & Schuh 2024 (thesis ch. 2), released (do after b6)

**Why:** Peter released this paper on 2026-11-08 (B4 exposure log). It is no longer a blind-list-2 candidate, so
its own values may now be reported. It probably supplies the only powder strength for the Panova Cu powder (rows
PA-01…03 in `vcr_lipit.csv`).

**Source:** the Panova thesis, ch. 2 (pp. 41–72; Peter's copy, sha256 `5a809e42…0538b00`). If you can obtain the
journal paper (Acta Mater. 276 (2024) 120105, doi:10.1016/j.actamat.2024.120105) under the standing fetch rule, say
whether the two differ in any value you report.

**Still excluded:** values from pending blind papers. Thesis pp. 56–57 (Fig. 8a) plot B03 data against the thesis's
own data. Report only the thesis's own points, and only if they can be told apart from B03's without reading B03's
values; otherwise skip that figure and say so. Do not read p. 146.

**Report** in `docs/research/data/panova2024_ch2.md`:
1. **Powder and substrate:** supplier, size (nominal and as used), lot or temper if stated, preparation, hardness.
   Say whether the powder is the one used in ch. 3–6 and in Panova2026b.
2. **Dynamic yield strength of the powder** (the CoR fit): value, uncertainty, fit model and parameters, the data
   it was fitted to, and the velocity range.
3. **Critical velocity:** as printed, with its definition, bounds or uncertainty, and number of impacts. This is the
   value Panova2026b quotes.
4. **Bonded fraction against impact velocity:** per specimen, impact velocity, particle size and bonded fraction,
   with its uncertainty and its definition (as in your b3 extraction of ch. 5). Use tables where printed; else
   digitize, with axis calibration and reading error.
5. **Coefficient of restitution data**, if tabulated (velocity, CoR, size); do not digitize a CoR plot unless it is
   the only source for item 2.

Branch `coldspray/panova2024-ch2` from `claude/exciting-fermi-qy077p`. Commit only that file, push, and stop.
**Do not merge.**
