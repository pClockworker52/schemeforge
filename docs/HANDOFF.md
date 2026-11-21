# Handoff — 2026-11-21 (cold-spray track; current state only)

Earlier versions: docs/handoff-archive.md (verbatim, 2026-11-21) and git history.

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." Then read, in order:
1. the top of docs/STATUS.md (entries since 2026-11-18; older ones in docs/status-archive.md);
2. **docs/research/solver-facts.md** (what the tools can and cannot do; check every spec against it);
3. the DECISIONS index (`python scripts/decisions_index.py`).

Branch: `claude/exciting-fermi-qy077p`. Procedure: docs/research/coldspray-procedure.md.

## First action

Fetch `coldspray/opencourant-sph`. §33 (softening check, informative) is merged. WSL A resumes CS-22b:
1. **Task 2026-11-20-a:** CS-22b (δ_c ladder), resumed after a Windows-update abort, on engine `27e53d5f0`.
   When pushed: merge (diff only §31 and `results/tl_cs22b_*`), recompute dR per δ_c with the §30 off runs, judge
   against coldspray-hunch-cs22b.md (frozen c8a6c5c; author's odds 0.15), record in coldspray-hunches.md,
   DECISIONS, STATUS and solver-facts.md. Also report the effective G_c (W_b / bonded area) per δ_c against the
   hunch file's G_c estimates, which assumed room-temperature σ_flow and are upper bounds (solver-facts §4; a
   rationale caveat, not a rule change).

2. **Task 2026-11-21-b** (between CS-22b runs): TLSPH temperature check. When pushed: merge, judge against
   docs/research/tlsph-temperature-check-2026-11-21.md (prediction (a) 0.35, (b) 0.35, (c) 0.25), update solver-facts
   §3/§4. Outcome (c) would mean every TLSPH impact so far ran without thermal softening.

If nothing is pushed: the open items for Peter below.

## State in brief

- **Track A (single-impact data):** single-impact phase ended (DECISIONS 2026-11-07); B06 scored 2026-11-18
  (coldspray-results-b06.md); synthesis in coldspray-synthesis-single-impact.md. Next is Peter's choice of R1–R3
  (reduced-route-plan.md).
- **Track B (SPH host for a bond law):** the interface-state route is closed (2026-11-17: no local driver
  converges). Open only for the forked bond response: CS-22 refuted for its registered setting (placeholder bond too
  brittle; scope note), **CS-22b frozen** and running. History: handoff-archive.md §2, solver-facts.md §3.
- **Length-scale idea (not a hunch):** docs/research/length-scale-note-2026-11-20.md: one fixed ℓ at the feedstock
  grain size plus the interface law. First unjustified step: that the edge failure is caused by a missing length.
  The softening check (task 2026-11-21-a) tests the premise of a cheap test of that step. Readings: data/ge2026_reading.md
  (ℓ calibrated, not physical), data/tang2024_reading.md (measured bond strength against radius; Bay-type law).

## Sessions and open tasks

| Session | Where | Open task |
|---|---|---|
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | — |
| WSL A | fork `sph-hvi-contact` branch `cs12`; results to `coldspray/opencourant-sph` | **2026-11-20-a** (CS-22b, resume now) and **2026-11-21-b** (TLSPH temperature check, between runs); 2026-11-21-a closed (§33) |
| WSL B | `coldspray/bonding-methods-reading` | b9: only Dai 2025 left (closed access); Ge 2026 read in the cloud |

## Open for Peter

1. After CS-22b's verdict: if it fails, does Track B close again?
2. Which of R1–R3 leads (reduced-route-plan.md).
3. Physical length scale: pursue after CS-22b? Next steps: Chakrabarty & Song 2020 (needs Peter's download), check
   the grain-size numbers (Panova & Schuh, Liu et al.) in the originals, find a grain size for an Al powder like
   P-HG-Al; a hunch only after that.
3b. Softening-off test on the §25 deck: draft it now or not? §33 says it can discriminate; its open first steps
   (twin windows differ, q heating, melt cut-off) are in length-scale-note-2026-11-20.md §9.
4. CS-20: no unseen ring-map source; candidate for parking.

## Hunch budget

**4 of 5:** CS-10, CS-17, CS-20, CS-22b. Retired: CS-12. Refuted: CS-22 part 1 (§30), CS-21 part 1 (§28),
CS-18b (§20). Index: docs/research/coldspray-hunches.md.

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
| Solver log §1–§30, §32, §33 (§31 reserved for CS-22b, §34 next) | docs/research/opencourant-verification.md; rows in docs/research/opencourant/results/ |
| Hunches | coldspray-hunches.md (index); open: coldspray-hunch-cs22b.md; recent: cs20, cs21, cs22 |
| Checks | driver-check-2026-11-17.md, switch-check-2026-11-18.md, softening-check-2026-11-20.md, tlsph-temperature-check-2026-11-21.md |
| Ladders (frozen) | sph-contact-ladder.md, sph-tlsph-ladder.md, sph-tlsph-b-ladder.md |
| Multi-particle brainstorm | multi-particle-spec.md, multi-particle-tried.md, multi-particle-brainstorm-2026-11-18.md |
| Readings | data/ge2026_reading.md, data/tang2024_reading.md, data/bonding_methods_reading.md, data/boundary_integration_reading.md, data/profizi2016_reading.md |
| Tasks | docs/research/tasks/wsl-a.md, wsl-b.md |
| Archives | docs/handoff-archive.md, docs/status-archive.md |
