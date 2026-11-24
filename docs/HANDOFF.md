# Handoff — 2026-11-24: orientation written; one question for Peter (pause cold spray / reduced level / review) (current state only)

Earlier versions: docs/handoff-archive.md (verbatim, 2026-11-21) and git history.

**Start the next session with:** "Read docs/HANDOFF.md and the orientation, then ask me the question." Then read, in
order:
1. **docs/research/coldspray-orientation-2026-11-24.md** (one page: where the track sits, what holds, what local means
   cannot answer, what is open, the one question);
2. the top of docs/STATUS.md;
3. the DECISIONS index (`python scripts/decisions_index.py`).

Read solver-facts.md only if the answer is option 2 or 3.

Branch: `claude/exciting-fermi-qy077p`. Procedure: docs/research/coldspray-procedure.md.

## First action

Put the orientation's one question to Peter. Record his answer in DECISIONS, and only then act.
1. **Pause the cold-spray track** and resume schemeforge Phase 6 at step 6 (docs/plans/2026-10-30-phase6.md: blind
   audit, Target D, tag `contact-v1.0`; about one session to Gate 6).
2. **Continue cold spray at the reduced level** (R2 or R3, finite quantities only).
3. **A review session whose allowed answers include "stop"** (fresh reviewers, the orientation only).

Modeller's recommendation: 1, with 3 kept as the way back; 3 first if Peter is unsure whether a local path is left.
Also confirm the housekeeping defaults (orientation, "Housekeeping").

Lesson to carry: point values at the contact edge and the bond boundary may be singular (problem-formalism §2(c)), so
any new criterion should be built from finite quantities (energies, averages over a fixed area).

## State in brief

- **Track A (single-impact data):** R1 is at its end point (DECISIONS 2026-11-23): blind list 1 used up, no blind
  list 2 (stop rule), synthesis §4b; further R1 progress needs new measurements. R2 and R3 stay open.
- **Track B (SPH host for a bond law), forked bond response only — PAUSED 2026-11-23 (Peter):**
  - CS-22b supported at δ_c 30× (§31), with caveats: two meshes in one regime, a pass by near-cancellation of two
    drifts, post hoc ladder; addendum: §31's G_c,eff biased upward (§37).
  - Slip check mixed (§36): whether bonds tear or hold depends largely on slip accumulated while compressed.
  - §37: `bond.stick` (bonded pairs stick, shear capped at σ_B/√3) and `out.pairs` built on engine `0153cae04`;
    the old law books G_c·A at reopening without work input.
  - §38: energy-consistent cap shrink on engine `38639859c` (S2 ≤ 0.30 %, release 2.7·10⁻⁴; two S3 predictions
    missed, read post hoc; R/32 with stick on + `out.pairs` ≈ 14.8 GiB; no run yet with bonded ghost pairs).
  - **CS-23 refuted** (§39, DECISIONS 2026-11-23): sticking bonds on the CS-22b set-up; all 9 runs valid; dR moves
    toward 0 from R/16 to R/32 at every δ_c (3× also |dR32| < 0.01). Sticking changed tear/hold as predicted (3× tears,
    10× mostly holds, 30× holds); tears mixed mode. Caveat: CS-22b's 30× pass depends on the free-slip law.
- **Length-scale path: STOPPED 2026-11-24 (Peter; DECISIONS 2026-11-24).** length-scale-note-2026-11-20.md §11–§14:
  - no host carries ℓ in σ_y and T (§40);
  - the band check was intermediate, with no band narrowing with the mesh; the edge drift is a surface-layer ε_p
    spike, and numerical dissipation is the largest drift (§41);
  - the premise was never tested against a singular edge field, a surface-layer error or numerical dissipation (§13);
  - step 0 leans against on TLSPH, not refuted; the softening-off test is shelved.
- **Problem as equations:** problem-formalism.md, every equation checked against the fork source (§35); points
  (c) crack-tip bond boundary, (e) identifiability, (f) bonds weakest at the hot edge, (g) slip vs ASI.

## Sessions and open tasks

| Session | Where | Open task |
|---|---|---|
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | — |
| WSL A | fork `sph-hvi-contact` branch `cs12`; results to `coldspray/opencourant-sph` | none; 2026-11-24-a closed (§41); 2026-11-23-c closed (§40); 2026-11-22-d closed (§39); 2026-11-22-c closed (§38); 2026-11-23-a closed (§37); 2026-11-22-b closed (§36); 2026-11-20-a closed (§31); 2026-11-21-a/b, 2026-11-22-a closed (§33–§35) |
| WSL B | `coldspray/bonding-methods-reading` | b9: only Dai 2025 left (closed access); b13 closed (merged) |

## Open for Peter

1. **The one question** (First action).
2. **Housekeeping defaults to confirm** (orientation):
   - CS-20 parked;
   - Mohanty 2022 a footnote to R1;
   - WSL A's band-check arrays (`~/oc_runs/hvi_band`, 5.5 GB) may be deleted;
   - friction for unbonded contact and the hot-edge choice filed under Track B (paused) as its design questions.

## Hunch budget

**3 of 5:** CS-10, CS-17, CS-20. Supported: CS-22b (§31; caveat DECISIONS 2026-11-23). Retired: CS-12. Refuted: CS-23 (§39), CS-22 part 1 (§30), CS-21 part 1
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
| Solver log §1–§41 (§42 next) | docs/research/opencourant-verification.md; rows in docs/research/opencourant/results/ |
| Hunches | coldspray-hunches.md (index); recent: cs22b (supported), cs23 (refuted) |
| Checks | driver-check-2026-11-17.md, switch-check-2026-11-18.md, softening-check-2026-11-20.md, tlsph-temperature-check-2026-11-21.md, slip-check-2026-11-22.md, band-check-2026-11-24.md (frozen) |
| Ladders (frozen) | sph-contact-ladder.md, sph-tlsph-ladder.md, sph-tlsph-b-ladder.md |
| Multi-particle brainstorm | multi-particle-spec.md, multi-particle-tried.md, multi-particle-brainstorm-2026-11-18.md |
| Readings | data/ge2026_reading.md, data/tang2024_reading.md, data/bonding_methods_reading.md, data/boundary_integration_reading.md, data/profizi2016_reading.md |
| Tasks | docs/research/tasks/wsl-a.md, wsl-b.md |
| Problem as equations (working note) | docs/research/problem-formalism.md (checks: scripts/formalism_check.py) |
| Archives | docs/handoff-archive.md, docs/status-archive.md |
