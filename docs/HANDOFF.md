# Handoff — 2026-11-21 (cold-spray track; current state only)

Earlier versions: docs/handoff-archive.md (verbatim, 2026-11-21) and git history.

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." Then read, in order:
1. the top of docs/STATUS.md (entries since 2026-11-18; older ones in docs/status-archive.md);
2. **docs/research/solver-facts.md** (what the tools can and cannot do; check every spec against it);
3. the DECISIONS index (`python scripts/decisions_index.py`).

Branch: `claude/exciting-fermi-qy077p`. Procedure: docs/research/coldspray-procedure.md.

## First action

Fetch `coldspray/opencourant-sph`. §31 (CS-22b supported), §33, §34 and §35 are merged; **WSL A has no open task**.
Nothing is pending from the other sessions.

If nothing is pushed: the open items for Peter below.

## State in brief

- **Track A (single-impact data):** single-impact phase ended (DECISIONS 2026-11-07); B06 scored 2026-11-18
  (coldspray-results-b06.md); synthesis in coldspray-synthesis-single-impact.md. Next is Peter's choice of R1–R3
  (reduced-route-plan.md).
- **Track B (SPH host for a bond law):** the interface-state route is closed (2026-11-17: no local driver
  converges). Open only for the forked bond response: CS-22 refuted for its registered setting (placeholder bond too
  brittle; scope note); **CS-22b supported at δ_c 30×** (§31, DECISIONS 2026-11-22), with caveats: two meshes in one
  regime, a pass by near-cancellation of two drifts, post hoc ladder. History: handoff-archive.md §2, solver-facts.md §3.
- **Length-scale idea (not a hunch):** docs/research/length-scale-note-2026-11-20.md: one fixed ℓ at the feedstock
  grain size plus the interface law. First unjustified step: that the edge failure is caused by a missing length.
  The softening check (task 2026-11-21-a) tests the premise of a cheap test of that step. Readings: data/ge2026_reading.md
  (ℓ calibrated, not physical), data/tang2024_reading.md (measured bond strength against radius; Bay-type law).

## Sessions and open tasks

| Session | Where | Open task |
|---|---|---|
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | — |
| WSL A | fork `sph-hvi-contact` branch `cs12`; results to `coldspray/opencourant-sph` | 2026-11-22-b (slip check), waits for the spec's freeze; 2026-11-20-a closed (§31); 2026-11-21-a/b, 2026-11-22-a closed (§33–§35) |
| WSL B | `coldspray/bonding-methods-reading` | b9: only Dai 2025 left (closed access); Ge 2026 read in the cloud |

## Open for Peter

1. **Next step after CS-22b (supported, with caveats).** Options:
   (a) a confirmatory pre-registered test of the 30× result (another speed, or δ_c 20× / 50×, on R/16 and R/32) to
   see whether the cancellation is robust;
   (b) the reopening/slip analysis of the existing on-runs (post-processing only, cheap; problem-formalism.md §2(g)):
       **chosen 2026-11-22**; spec docs/research/slip-check-2026-11-22.md DRAFTED, waits for Peter's freeze, then
       WSL A task 2026-11-22-b. It cannot change CS-22b's verdict;
   (c) part 2, the bistable band in V (trigger and kill rule registered first);
   (d) R1–R3 (item 2).
2. Which of R1–R3 leads (reduced-route-plan.md).
3. Physical length scale: pursue after CS-22b? Next steps: Chakrabarty & Song 2020 (needs Peter's download), check
   the grain-size numbers (Panova & Schuh, Liu et al.) in the originals, find a grain size for an Al powder like
   P-HG-Al; a hunch only after that.
3b. Softening-off test on the §25 deck: draft it now or not? §33 says it can discriminate; its open first steps
   (twin windows differ, q heating, melt cut-off) are in length-scale-note-2026-11-20.md §9.
4. CS-20: no unseen ring-map source; candidate for parking.
5. Two modelling choices in cs12 to question before any further bond-law work (problem-formalism.md §2(f), §2(g)):
   σ_B ∝ σ_y(T) makes bonds weakest at the hot edge; bonded pairs do not stick under compression.

## Hunch budget

**3 of 5:** CS-10, CS-17, CS-20. Supported: CS-22b (§31). Retired: CS-12. Refuted: CS-22 part 1 (§30), CS-21 part 1
(§28), CS-18b (§20). Index: docs/research/coldspray-hunches.md.

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
| Solver log §1–§35 (§36 next) | docs/research/opencourant-verification.md; rows in docs/research/opencourant/results/ |
| Hunches | coldspray-hunches.md (index); recent: cs20, cs21, cs22, cs22b (supported) |
| Checks | driver-check-2026-11-17.md, switch-check-2026-11-18.md, softening-check-2026-11-20.md, tlsph-temperature-check-2026-11-21.md |
| Ladders (frozen) | sph-contact-ladder.md, sph-tlsph-ladder.md, sph-tlsph-b-ladder.md |
| Multi-particle brainstorm | multi-particle-spec.md, multi-particle-tried.md, multi-particle-brainstorm-2026-11-18.md |
| Readings | data/ge2026_reading.md, data/tang2024_reading.md, data/bonding_methods_reading.md, data/boundary_integration_reading.md, data/profizi2016_reading.md |
| Tasks | docs/research/tasks/wsl-a.md, wsl-b.md |
| Problem as equations (working note) | docs/research/problem-formalism.md (checks: scripts/formalism_check.py) |
| Archives | docs/handoff-archive.md, docs/status-archive.md |
