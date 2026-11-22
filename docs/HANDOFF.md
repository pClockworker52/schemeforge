# Handoff — 2026-11-22: CS-22b supported; bonded stick built and made energy-consistent (§38); CS-23 waits for Peter's freeze (cold-spray track; current state only)

Earlier versions: docs/handoff-archive.md (verbatim, 2026-11-21) and git history.

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." Then read, in order:
1. the top of docs/STATUS.md (entries since 2026-11-18; older ones in docs/status-archive.md);
2. **docs/research/solver-facts.md** (what the tools can and cannot do; check every spec against it);
3. the DECISIONS index (`python scripts/decisions_index.py`).

Branch: `claude/exciting-fermi-qy077p`. Procedure: docs/research/coldspray-procedure.md.

## First action

§38 (WSL A task 2026-11-22-c, cap fix) is **merged**; engine `38639859c`. CS-23 (coldspray-hunch-cs23.md) is updated
(engine named, facts line rewritten, ghost-weighting validity check proposed) and **waits for Peter's freeze**. If
Peter has frozen it: write the freeze line as its own commit, then the WSL A task (stage gate as CS-22b, R/8 and R/16
first). If he edited it: apply the edits, recheck the facts line, ask again.

## State in brief

- **Track A (single-impact data):** R1 is at its end point (DECISIONS 2026-11-23): blind list 1 used up, no blind
  list 2 (stop rule), synthesis §4b; further R1 progress needs new measurements. R2 and R3 stay open.
- **Track B (SPH host for a bond law), forked bond response only:**
  - CS-22b supported at δ_c 30× (§31), with caveats: two meshes in one regime, a pass by near-cancellation of two
    drifts, post hoc ladder; addendum: §31's G_c,eff biased upward (§37).
  - Slip check mixed (§36): whether bonds tear or hold depends largely on slip accumulated while compressed.
  - §37: `bond.stick` (bonded pairs stick, shear capped at σ_B/√3) and `out.pairs` built on engine `0153cae04`;
    the old law books G_c·A at reopening without work input.
  - §38: energy-consistent cap shrink on engine `38639859c` (S2 ≤ 0.30 %, release 2.7·10⁻⁴; two S3 predictions
    missed, read post hoc; R/32 with stick on + `out.pairs` ≈ 14.8 GiB; no run yet with bonded ghost pairs).
  - **CS-23 drafted and updated** (coldspray-hunch-cs23.md: the CS-22b set-up with sticking bonds; not frozen, not
    counted).
- **Length-scale idea (not a hunch):** length-scale-note-2026-11-20.md. Softening is active from the first judged
  frame on quads (§33); TLSPH heats and softens without q heating (§34). Step 0 ("a missing length causes the edge
  failure") is still unjustified; the softening-off test is on hold.
- **Problem as equations:** problem-formalism.md, every equation checked against the fork source (§35); points
  (c) crack-tip bond boundary, (e) identifiability, (f) bonds weakest at the hot edge, (g) slip vs ASI.

## Sessions and open tasks

| Session | Where | Open task |
|---|---|---|
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | — |
| WSL A | fork `sph-hvi-contact` branch `cs12`; results to `coldspray/opencourant-sph` | none (CS-23 waits for its freeze); 2026-11-22-c closed (§38); 2026-11-23-a closed (§37); 2026-11-22-b closed (§36); 2026-11-20-a closed (§31); 2026-11-21-a/b, 2026-11-22-a closed (§33–§35) |
| WSL B | `coldspray/bonding-methods-reading` | b9: only Dai 2025 left (closed access); b13 closed (merged) |

## Open for Peter

1. Freeze CS-23 (or edit it); the cap fix is merged (§38). Includes the proposed ghost-weighting validity check, the
   pair-level lost-bond wording (swept pairs) and the reassessed odds (supported 0.45; draft section "Odds reassessed").
2. Friction for unbonded contact (the off branch is frictionless; physics leans toward sticking friction at GPa).
3. Mohanty 2022 alone (oxide-thickness series in Al, pre-registered post hoc) or not; R2 and R3.
4. Physical length scale: Chakrabarty & Song 2020 (needs Peter's download); check the grain-size numbers (Panova &
   Schuh, Liu et al.) in the originals; a grain size for an Al powder like P-HG-Al; a hunch only after that.
5. CS-20: no unseen ring-map source; candidate for parking.
6. The hot-edge choice in cs12: σ_B ∝ σ_y(T) makes bonds weakest where they form (problem-formalism.md §2(f)).

## Hunch budget

**3 of 5:** CS-10, CS-17, CS-20 (CS-23 is a draft, not counted). Supported: CS-22b (§31). Retired: CS-12. Refuted: CS-22 part 1 (§30), CS-21 part 1
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
| Solver log §1–§38 (§39 next) | docs/research/opencourant-verification.md; rows in docs/research/opencourant/results/ |
| Hunches | coldspray-hunches.md (index); recent: cs20, cs21, cs22, cs22b (supported) |
| Checks | driver-check-2026-11-17.md, switch-check-2026-11-18.md, softening-check-2026-11-20.md, tlsph-temperature-check-2026-11-21.md, slip-check-2026-11-22.md |
| Ladders (frozen) | sph-contact-ladder.md, sph-tlsph-ladder.md, sph-tlsph-b-ladder.md |
| Multi-particle brainstorm | multi-particle-spec.md, multi-particle-tried.md, multi-particle-brainstorm-2026-11-18.md |
| Readings | data/ge2026_reading.md, data/tang2024_reading.md, data/bonding_methods_reading.md, data/boundary_integration_reading.md, data/profizi2016_reading.md |
| Tasks | docs/research/tasks/wsl-a.md, wsl-b.md |
| Problem as equations (working note) | docs/research/problem-formalism.md (checks: scripts/formalism_check.py) |
| Archives | docs/handoff-archive.md, docs/status-archive.md |
