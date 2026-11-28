# Handoff — 2026-11-28: CS-25 drafted, waiting on Peter (waiver, tolerance, freeze) (current state only)

Earlier versions: docs/handoff-archive.md (verbatim, 2026-11-21; track state at the pause, 2026-11-27) and git history.

**Start the next session with:** "Read docs/HANDOFF.md." Then read docs/STATUS.md (top) and
**docs/research/coldspray-hunch-cs25.md** (the draft). Background: docs/research/interface-as-object-2026-11-28.md
(the brief), coldspray-hunch-cs24.md (result section).

Branch: `claude/exciting-fermi-qy077p` (`main` is behind; no instruction to keep it in step). Two sessions may write:
`git fetch` and fast-forward before every commit; never force-push.

## Current task: CS-25 draft → Peter

- **Draft:** docs/research/coldspray-hunch-cs25.md (not registered). Predictions: `scripts/cs25_predict.py` (reads
  properties.csv only; no v_cr value read in the drafting session).
- **Form:** the contact holds a model of both partners (B, Z) and the edge kinematics a(t). Each face is cleaned iff
  the edge is subsonic for it and it is compressed by μ_i = p/B_i ≥ α/2 under the shared acoustic pressure; the
  particle bonds iff both faces are clean (co-exposure).
  - v_cr = (α/2) max(B_p, B_s)(1/Z_p + 1/Z_s), α = 0.15 from Z6, nothing fitted. Matched pairs: Z6 + CS-20 strong form.
  - Chosen with the six CS-24 ratios in view (sound-speed-only and OR forms discarded); they are context only.
- **Judged item J** (post hoc, H20 rows outside the record, not yet read): Cu on W 1.689, Sn on Cu 1.794, W on Cu
  1.689 (against Cu on Cu); comparators Z6 particle-only and Z6-mean; tol = summed half-widths + 0.15.
- **Open for Peter:**
  1. rule 1 data-clause waiver, or not registering it (registration makes the count 3 of 5);
  2. the tolerance (0.15) and the verdict thresholds;
  3. freeze.
- **After a freeze:** `scripts/cs25_score.py` committed before it is run; literature step after the freeze (a search
  would surface Hassani 2020's pair values); verdict labelled post hoc.
- **Known gaps (in the draft):** no strength, temperature or size term; CH heating not explained; nothing new for
  matched pairs; planar partition likely misses penetration pairs (Cu on Al context miss ×1.5).

## State in brief (2026-11-28)

- **Phase 6: Gate 6 PASSED** (2026-11-27). Judge contact-v1.0 (6eef4c9, tag); Target D pre-registered (a722ef0).
  - The step 7 rediscovery shortfall is recorded: calibration K1 rediscovered 0 of 2 zoo media and filled 19 archive
    cells.
  - Six Target D hunch drafts sit in ledger/drafts/d7_*, not registered. Hunch 1's text needs a fix: its term also
    acts in biaxial tension.
  - **Phase 7 (search in Arena 2) not started.**
- **Repository clean-up done** (docs/reports/2026-11-27-repo-cleanup.md): `coldspray/*` branches deleted except
  `coldspray/opencourant-sph` (recreated for WSL A results).
- **Cold spray UNPAUSED** (DECISIONS 2026-11-27); resume conditions of 2026-11-24 still unmet.
  - Kernel completion, Stage A: **both forms fail** (§43). No Stage B.
  - **CS-24 refuted** (post hoc; DECISIONS 2026-11-28): substrate effusivity does not order the mismatched pairs.
    Heated-substrate shifts are 2.6–5× the thermal-partition prediction.

## Sessions and open tasks

| Session | Where | Open task |
|---|---|---|
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | CS-25 draft to Peter; score after a freeze |
| WSL A | fork `sph-hvi-contact` `cs12`; results to `coldspray/opencourant-sph` | none (2026-11-27-b closed, §43) |
| WSL B | — | none (b9: only Dai 2025 left, closed access) |

## Open for Peter

- CS-25 draft → rule 1 waiver, tolerance, freeze (docs/research/coldspray-hunch-cs25.md).
- Later: Phase 7 (Arena 2 search) vs further cold-spray work.
- Small open items:
  - the B4 exposure log entry for the Tang 2024 snippet (details with the desktop session);
  - hunch-preview hunch 1's mechanism text.

## Hunch budget

**2 of 5:** CS-10, CS-17.
- Parked: CS-20 (2026-11-24), CS-14/14b.
- Supported: CS-22b (§31; caveat DECISIONS 2026-11-23).
- Retired: CS-12.
- Refuted: CS-24 (2026-11-28, post hoc), CS-23 (§39), CS-22 part 1 (§30), CS-21 part 1 (§28), CS-18b (§20).

Index: docs/research/coldspray-hunches.md.

## Rules that must not be broken

- **Blind test** (coldspray-blind-literature.md, B1–B6): leak-scan every WSL B branch; post-hoc numbers labelled.
- **Frozen files are never edited** (hunches, ladders, specs): verdicts and amendments are dated sections or
  DECISIONS entries, post hoc where results were seen.
- **Process:** predictions committed before runs; rows only from committed binaries; stop rules apply; no tuning
  after a freeze; externally killed runs are rerun, not counted (DECISIONS 2026-11-21).
- **Before any freeze:** check every output quantity, parser key and placeholder against solver-facts.md; list any
  that are not covered as "never read/used before" (coldspray-procedure.md).
- **Iron rules** (CLAUDE.md): never "novel"; record negative results; no invented values; float64.
- **Fork:** Siemens-licensed files stay byte-identical (`hvi/scripts/check_untouched.sh`); PDFs never committed.

## Key files

| What | Where |
|---|---|
| Solver facts (read first) | docs/research/solver-facts.md |
| Decisions | docs/DECISIONS.md (index: `python scripts/decisions_index.py`) |
| Solver log §1–§41 (§42 next) | docs/research/opencourant-verification.md; rows in docs/research/opencourant/results/ |
| Hunches | coldspray-hunches.md (index); recent: cs22b (supported), cs23 (refuted) |
| Checks | driver-check-2026-11-17.md, switch-check-2026-11-18.md, softening-check-2026-11-20.md, tlsph-temperature-check-2026-11-21.md, slip-check-2026-11-22.md, band-check-2026-11-24.md (frozen) |
| Ladders (frozen) | sph-contact-ladder.md, sph-tlsph-ladder.md, sph-tlsph-b-ladder.md |
| Multi-particle brainstorm | multi-particle-spec.md, multi-particle-tried.md, multi-particle-brainstorm-2026-11-18.md |
| Readings | data/ge2026_reading.md, data/tang2024_reading.md, data/bonding_methods_reading.md, data/boundary_integration_reading.md, data/profizi2016_reading.md |
| Tasks | docs/research/tasks/wsl-a.md, wsl-b.md |
| Problem as equations (working note) | docs/research/problem-formalism.md (checks: scripts/formalism_check.py) |
| Archives | docs/handoff-archive.md, docs/status-archive.md |
