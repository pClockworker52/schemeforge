# Handoff — 2026-11-28: CS-25 frozen; scoring script committed, run waits for Peter's go (current state only)

Earlier versions: docs/handoff-archive.md (verbatim, 2026-11-21; track state at the pause, 2026-11-27) and git history.

**Start the next session with:** "Read docs/HANDOFF.md." Then read docs/STATUS.md (top), the last DECISIONS entry
(2026-11-28, CS-25 registered) and **docs/research/coldspray-hunch-cs25.md** (frozen).

Branch: `claude/exciting-fermi-qy077p` (`main` is behind; no instruction to keep it in step). Two sessions may write:
`git fetch` and fast-forward before every commit; never force-push.

## Current task: score CS-25 on Peter's go

- **CS-25 frozen** (fc2d232; as drafted in a5a82be, tolerance 0.15 unchanged; rule 1 data clause waived). Count 3 of 5.
- **Scoring:** `scripts/cs25_score.py` (35f803c), committed before it is run, checked only on synthetic tables. Not
  yet run on `vcr_lipit.csv`; no judged row (H20-04, -05, -07) or denominator read.
- **Why it waits:** Peter asked "0.15 seems strict. Why?" at the freeze. Answer (chat; DECISIONS): the effective
  tolerance is half-widths + 0.15, about 0.23–0.37 in ln; looser would let comparator-like values agree. Until the
  run, a dated amendment of the tolerance is still before any judged value is read.
- **After the run:** result section in the hunch file (post hoc label), DECISIONS entry, hunch index, then the
  literature step (label only).
- **Then:** Peter's priority (DECISIONS 2026-11-28): "finding something that converges". CS-25 does not address the
  solver's non-converging interface states; the next task should.

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
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | score CS-25 on Peter's go; then a convergence task |
| WSL A | fork `sph-hvi-contact` `cs12`; results to `coldspray/opencourant-sph` | none (2026-11-27-b closed, §43) |
| WSL B | — | none (b9: only Dai 2025 left, closed access) |

## Open for Peter

- Go for the CS-25 run (or a tolerance amendment first).
- The next task under the convergence priority.
- Later: Phase 7 (Arena 2 search) vs further cold-spray work.
- Small open items:
  - the B4 exposure log entry for the Tang 2024 snippet (details with the desktop session);
  - hunch-preview hunch 1's mechanism text.

## Hunch budget

**3 of 5:** CS-10, CS-17, CS-25.
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
