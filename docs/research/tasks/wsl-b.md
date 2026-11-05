# Tasks for WSL B (extraction)

Procedure: [../coldspray-procedure.md](../coldspray-procedure.md). Pull `claude/exciting-fermi-qy077p`, do the
newest open task, push to the branch named in the task. Write only the files the task names. Blind rules
(coldspray-blind-literature.md) bind you as before.

## Task 2026-11-05-b1: Na et al. 2025 (B10), Eq. 6 (open)

B10 is unblinded and scored, so the full text may be read. From your PDF (sha256 a4cdccfe...), extract:
1. Eq. 6 (the combined strength + oxide model) **exactly as printed**, with every symbol defined as in the paper;
2. its fitted constant(s), with how and on which data they were fitted;
3. the reference(s) it builds on (the Lienhard rule of mixtures), as citations only. Do **not** report anything from
   B14 (Lienhard 2020) beyond what Na et al. print about its model form.

Write `docs/research/data/na2025_eq6.md` on branch `coldspray/b10-eq6` and push.
