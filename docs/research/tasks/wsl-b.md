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
