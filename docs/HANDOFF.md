# Handoff — 2026-11-28: edge-energy check r1 frozen; WSL A task 2026-11-28-a open (current state only)

Earlier versions: docs/handoff-archive.md (verbatim, 2026-11-21; track state at the pause, 2026-11-27) and git history.

**Start the next session with:** "Read docs/HANDOFF.md." Then read docs/STATUS.md (top), the last three DECISIONS
entries (2026-11-28), coldspray-hunch-cs25.md (result section), problem-formalism.md §2(c)-(d), driver-check-2026-11-17.md.

Branch: `claude/exciting-fermi-qy077p` (`main` is behind; no instruction to keep it in step). Two sessions may write:
`git fetch` and fast-forward before every commit; never force-push.

## Current task: edge-energy check, WSL A task 2026-11-28-a

- **Spec frozen:** docs/research/edge-energy-check-2026-11-28.md r1 (929afee; as drafted in 46a4a53). Judged: energy
  delivered to the interface layer per contact area by body, and its excess; Stage 0 output-only fork change first.
- **Task:** docs/research/tasks/wsl-a.md, 2026-11-28-a (fork branch `energy-out` from `27e53d5f0`; results to
  `coldspray/opencourant-sph`, §44). Stops at the first failure: preflight (per-particle accumulators), S0-1..S0-4,
  model checks, Q1.
- **Next for the modeller:** merge §44 when WSL A reports; record the verdict (DECISIONS, solver-facts lines).

- **Peter's priority** (DECISIONS 2026-11-28): "Finding something that converges has priority now."
- **CS-25 done:** undetermined, because the judged rows H20-04/05/07 have no v_cr window (drafting error); parked.
  Reported: reversal symmetry fails (0.711, 0.764). Count 2 of 5.
- **Open for Peter:** the proposed presence check of judged fields before a freeze (DECISIONS 2026-11-28).
- **Known about convergence (record):** a(t) converges; annulus plastic work, pressure-slip history, ring stretch,
  v_edge and ring Y do not (driver check); e(off) drifts 14 % R/16 -> R/32 (§30); the edge field is singular
  (problem-formalism §2(c)); lesson of 2026-11-24: build criteria from finite (energy-type) quantities.

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
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | merge §44 when WSL A reports |
| WSL A | fork `sph-hvi-contact` `energy-out` (new, from `27e53d5f0`); results to `coldspray/opencourant-sph` | task 2026-11-28-a (edge-energy check) |
| WSL B | — | none (b9: only Dai 2025 left, closed access) |

## Open for Peter

- The next task under the convergence priority.
- The proposed presence check before a freeze.
- Later: Phase 7 (Arena 2 search) vs further cold-spray work.
- Small open items:
  - the B4 exposure log entry for the Tang 2024 snippet (details with the desktop session);
  - hunch-preview hunch 1's mechanism text.

## Hunch budget

**2 of 5:** CS-10, CS-17.
- Parked: CS-25 (2026-11-28, not scorable), CS-20 (2026-11-24), CS-14/14b.
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
