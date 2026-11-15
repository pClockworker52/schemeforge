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

## Task 2026-11-08-b8: outcomes of B03 and B12 for the data table (no scoring) (closed: merged d67f72c)

Peter closed B03, B05 and B12 without a pre-registration (coldspray-blind-literature.md, "Closure of B03, B05 and
B12"). Nothing is frozen against them, so their outcomes may be extracted now, for the data table only.

Use the step-3 prompt (`docs/research/coldspray-extraction-prompt-step3.md`) on the PDFs of task b5 (sha256 in
`blind_inputs.csv`), with these changes:
- **Rows:** `B-B03-c1`, `B-B12-c1` (Cu), `B-B12-c2` (Al). If a paper gives more than one critical velocity (sizes,
  definitions), one row each, with the condition in `notes`.
- **In `notes`, start with:** `exposed; no verdict (closed without pre-registration 2026-11-08)`. For B12-c2, add
  `impacts reused from HG2018b and HG2019b`; for B03 and B12-c1, add `probably shared impact sites (B03 reproduces
  B12 data)`.
- **Window, definition, uncertainty:** exactly as printed (rule B6 form if no bounds: `velocity uncertainty +-X %`).
- **Where B03 compares its Cu value with HG2018b or Sun 2020:** record the comparison as printed.
- B05 has no v_cr: no row.

Commit only `docs/research/data/vcr_lipit.csv` on a new branch `coldspray/b03-b12-outcomes` from
`claude/exciting-fermi-qy077p`, push, and stop. **Do not merge.**

## Task 2026-11-15-b11: boundary integration and patch tests in corrected particle methods (open; after b10, before the rest of b9)

**Why:** route review 2026-11-15 (DECISIONS, D5 step 1). The TLSPH face layer carries only 0.5–0.6 of the stress
under any point-loaded flat face (§22), and an external review claims that the literature proves strong-form
corrected particle methods fail the patch test at traction boundaries unless boundary integrals are evaluated over
surface cells. Neither independent reviewer could confirm "proves". The answer decides whether the deficit is a
known property of the method (then "rediscovery") and whether a known remedy exists. These are methods papers; none
is on the blind list. **Blind screen first:** check each source for numbers from B06, B07 or B16; if any appear,
note page and paragraph without the value, and leave them out.

**Papers** (standing fetch rule; record URL, version and sha256; never commit a PDF):

| # | Paper | Access |
|---|---|---|
| 1 | Chen, Wu, Yoon, You (2001), stabilized conforming nodal integration (SCNI), IJNME 50:435–466 | find an open copy |
| 2 | Chen, Hillman, Rüter (2013), variationally consistent integration (VCI), IJNME, doi:10.1002/nme.4512 | find an open copy |
| 3 | Hillman (2013), PhD dissertation, UCLA (eScholarship qt2s8848b6), the chapter on the patch test for collocation | open |
| 4 | Ganzenmüller (2015), TLSPH with hourglass control, Comput. Methods Appl. Mech. Eng.: what it says about boundaries | find an open copy |
| 5 | Up to three more found by a sweep for: Neumann / traction boundary conditions in kernel-corrected SPH or RKPM collocation; surface (boundary) integrals in corrected SPH; meshfree bodies with surface meshes or skins for contact | as found |
| 6 | Tang, J. (2021), MASc thesis, University of Waterloo (UWSpace 10012/17030), **full text** (moved here from b9) | open |

**For each paper, a section** in `docs/research/data/boundary_integration_reading.md`, with page references, stating
exactly what the text says and labelling your own reading as such:
1. Which formulation (Galerkin or collocation / strong form; kernel correction order) the result applies to.
2. What it shows at loaded boundaries: a patch-test failure, a proof, or a numerical observation; the size of the
   boundary error and how it scales with spacing.
3. The remedy (surface integrals, stabilised boundary cells, ghost particles, a corrected traction form) and what it
   requires from the code.
4. Whether it carries over to strong-form TLSPH with penalty contact applied to the outer layer, as the text says
   or as your reading (labelled).
5. For Tang 2021: what converges under refinement (bonded area, Y, p_n, shape), against what reference, and which
   length or regularisation it needs.

End with a short table: claim of the external review (inputs.md, input 2, point 4) against what the sources show.
Push to a new branch `coldspray/boundary-integration-reading` from `claude/exciting-fermi-qy077p` and stop; the
modeller leak-scans and merges.

## Task 2026-11-15-b10: step 1 for B06, B07 and B16 (open; do before the rest of b9)

**Why:** Peter has filed the publisher versions in `coldspray-papers/` (your message of 2026-11-15, identified from
PDF metadata only). These are the last three blind papers. Their step 1 unblocks the end point of the single-impact
phase and, for B06, the decision on the T3 measurement request (CS-12 against CS-10).

| Id | File | sha256 (as you reported) |
|---|---|---|
| B06 | B06_Wu_2026_published.pdf (Scripta Mater. 283, 117444) | 188dadc36e0ee3a01f1cf45d4aaa61ad1e13da856f226af2405b8f7cccec8b2b |
| B07 | B07_Liu_2025_published.pdf (Surf. Interfaces 73, 107537) | 272e1e69d2e426fc7a1f0da5fa9adba3bceea58590eef85252e5c6e214ec4058 |
| B16 | B16_Kajihara_2024_published.pdf (Acta Mater. 262, 119467) | 351beb1c0bd89433f1d42ae670d4ea08deb9304af052be46ddb24506339f6d2d |

1. **Step 1 exactly as `docs/research/coldspray-extraction-prompt.md` says:** inputs only. Replace the rows
   `B06-pending`, `B07-pending` and `B16-pending` in `docs/research/data/blind_inputs.csv` with one row per condition.
   Re-hash each file first and give the hash in `access`.
2. **Extra care for B06 (oxide fracture).** The oxide state of each condition is an input: type, thickness,
   preparation. Do **not** pass on:
   - critical velocities, bonding or rebound outcomes;
   - descriptions of fracture patterns, bonded areas or oxide residue, and figures showing them;
   - the paper's conclusions or mechanisms.

   These are outcomes for CS-12 (T1, T3) and CS-10.
   - If B06 has a series of one oxide type over several thicknesses, write only that the inputs form such a series
     (types and thicknesses as inputs), nothing about the result.
3. **B07 and B16 may contain no v_cr** (the list says so). Then give one row with `measures_vcr = no` and nothing
   else, as the prompt says.
4. **B03 check (small; B03 is closed and exposed, so no blinding applies):** the list owner asks for it. Compare row
   B-B03-c1 in `data/vcr_lipit.csv` (588–590 m/s, from the accepted manuscript) with the published
   B03_Tiamiyu_2021_published.pdf (sha256 ab89767c…cb3). Report "same" or the published values, with page and
   figure, in a note on the same branch.
   - **Do not open B05 or B12** for this.

Commit only `docs/research/data/blind_inputs.csv` (and the B03 note) on a new branch
`coldspray/blind-inputs-b06-b07-b16` from `claude/exciting-fermi-qy077p`, push, and stop. **Do not merge;** the
modeller leak-scans and merges.

## Task 2026-11-13-b9: interface-bonding methods in cold spray, reading at F level (open)

**Status 2026-11-13:** the partial note is merged (51f1e6d): Dai 2026, Ren & Song 2022/2024, the Khoei 2023 abstract,
and the comparison table. **Open:**
- Tang 2021 and Ge 2026: Peter downloads them in a browser into `coldspray-papers/` (Tang 2021 moved to task b11,
  2026-11-15);
- Dai et al. 2025, doi:10.1007/s00466-025-02714-1 (closed; this is the task's "Wang et al. 2025").

Continue on the same branch, then stop.

**Why:** CS-18b (Total Lagrangian SPH) is on hold (DECISIONS 2026-11-13, "CS-18b freeze on hold for a methods
literature step"). A search sweep on 2026-11-13 found recent method work that the project's literature checks had
missed. Several groups claim what the SPH route kept failing at: bonding that does not depend on the
discretisation, a regularised contact edge, and updated-Lagrangian SPH bonding at multi-particle scale. These papers
are methods papers; none is on the blind list.

**Blind screen first:** before extracting, check each source for numbers taken from the pending blind papers **B06,
B07 and B16** (coldspray-blind-literature.md). If any appear, note page and paragraph without the value, and leave
them out.

**Papers.** The open ones go first, under the standing fetch rule. Record the URL, version and sha256; never commit
a PDF.

| # | Paper | Access |
|---|---|---|
| 1 | Tang, J. (2021), *Predictive model of impact-induced bonding in cold spray using the Material Point Method*, MASc thesis, University of Waterloo (UWSpace handle 10012/17030) | open |
| 2 | Ge, Zhou, Bagherifard, Guagliano (2026), cold spray FE with nonlocal and over-nonlocal regularisation, Int. J. Mech. Sci. (Politecnico di Milano repository, re.public.polimi.it handle 11311/1314673) | open (repository) |
| 3 | Peridynamic simulation of particles impact and interfacial bonding in cold spray process (PMC9109757) | open |
| 4 | Dai, Xu, Wang, Ye, Feng (2026), "Investigation of interfacial adhesion and pore formation in cold spray using the updated Lagrangian SPH method", Comput. Mech. 78, doi:10.1007/s00466-026-02813-7 | closed: from Peter or Alex |
| 5 | Wang, J. et al. (2025), "Physically based interaction model of cold spray particle bonding via smoothed particle hydrodynamics" (cited by #4; find the exact reference) | probably closed: from Peter or Alex |
| 6 | Khoei (2023), ITSC abstract on MPM adhesion strength (extends #1) | abstract only; record what it states |

Do 1–3 now, and 4–5 when the PDFs arrive. If a source is not obtainable, list it.

**For each paper, write a section** in `docs/research/data/bonding_methods_reading.md`, with page references,
stating exactly what the text says and labelling your own reading as such:
1. **Method:** the formulation (SPH variant: total or updated Lagrangian, kernel correction, stabilisation against
   tensile instability and zero-energy modes; MPM variant; FE with remeshing, ALE or CEL; peridynamics), and the
   solver or code.
2. **Contact and interface:** how the bodies are kept separate; the contact algorithm; how surface normals and
   surface area are obtained.
3. **Bonding law:** activation criterion, cohesive or adhesion law, parameters, and how they are obtained (fitted to
   what).
4. **Regularisation or length scale:** what makes results independent of the discretisation, and whether that is
   shown.
5. **Verification against exact references** (Hertz, wave solutions, tension), with numbers.
6. **Convergence:** resolutions used (in particle spacings across the radius), the quantities shown to converge, and
   which do not (especially edge quantities: plastic strain, temperature, surface stretch, contact pressure at the
   contact edge).
7. **Validation against experiment:** what data, and the agreement in numbers.
8. **Impact conditions reached:** material, size, velocity range, and whether fine-resolution runs finish at
   800–1100 m/s.
9. **3D or axisymmetric; single or multi-particle; cost.**
10. **Stated limits.**

**Then a comparison table** across the papers, with the columns of items 1–9 in short form, and our own SPH route as
the last row (from sph-route-review-2026-11.md). No ranking and no recommendation: the cloud session and Peter do
that.

**Commit** only `docs/research/data/bonding_methods_reading.md`, on a new branch `coldspray/bonding-methods-reading`
from `claude/exciting-fermi-qy077p`. Push and stop. **Do not merge;** the modeller leak-scans and merges.
