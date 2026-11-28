# Handoff — 2026-11-28: next task is drafting hunch CS-25 (the contact as an object with a model of its partners) (current state only)

Earlier versions: docs/handoff-archive.md (verbatim, 2026-11-21; track state at the pause, 2026-11-27) and git history.

**Start the next session with:** "Read docs/HANDOFF.md and draft CS-25." Then read:
- docs/STATUS.md (top);
- the last four DECISIONS entries (`python scripts/decisions_index.py`);
- **docs/research/interface-as-object-2026-11-28.md**, the brief;
- problem-formalism.md;
- coldspray-hunch-cs24.md (result section);
- multi-particle-tried.md;
- coldspray-hunch-cs20.md;
- reduced-route-plan.md (R3).

Branch: `claude/exciting-fermi-qy077p` (`main` was fast-forwarded on 2026-11-27 and is behind again; no instruction to
keep it in step). Two sessions may write: `git fetch` and fast-forward before every commit; never force-push.

## Next task: draft CS-25 (Peter, chat 2026-11-28: "Write it as a hunch. This will need a bit of reasoning and a fresh session.")

- **Idea** (Peter's reframing): what is missing is the *contact's* model of its partners, not a body's model of its
  partner. The interface as an object with its own state and length, fed by both partners.
- **Brief:** docs/research/interface-as-object-2026-11-28.md. It covers:
  - what the contact is in the formalism today;
  - why the interface is the home for the missing length and for regularising the bond-front singularity;
  - the third-body view;
  - the CS-24 observations (co-exposure; heating acts through supply);
  - the limits: near the closed interface-state route, inputs must be converged (only a(t) is), identifiability, no
    unseen ring maps, and what was already tried;
  - the one feasible form the modeller sees: an a(t)-driven interface-state model with a film-coverage state and a
    co-exposure rule;
  - five questions to settle before drafting.
- **Process:** `coldspray-hunch-cs25.md`, drafted first; mechanism, predictions and kill criterion fixed before any
  data. Literature (relatives) checked without exposing data. Peter freezes.
  - Budget: 2 of 5 open, so registration would make it 3 of 5.
  - Rule 1's data clause will most likely need a waiver, since all v_cr data is exposed and there are no unseen ring
    maps. Say so in the draft.
- **Do not** re-propose CS-12 (Bay stretch), CS-20 (switch radius) or the pressure–slip driver without saying how CS-25
  differs.

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
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | draft CS-25 (fresh session) |
| WSL A | fork `sph-hvi-contact` `cs12`; results to `coldspray/opencourant-sph` | none (2026-11-27-b closed, §43) |
| WSL B | — | none (b9: only Dai 2025 left, closed access) |

## Open for Peter

- CS-25 draft → freeze (and probably a rule 1 waiver).
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
