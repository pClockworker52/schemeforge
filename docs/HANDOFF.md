# Handoff — 2026-11-24: focus on the physical length scale; no zero-code length (§40); Peter chooses the next step (cold-spray track; current state only)

Earlier versions: docs/handoff-archive.md (verbatim, 2026-11-21) and git history.

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." Then read, in order:
1. the top of docs/STATUS.md (entries since 2026-11-18; older ones in docs/status-archive.md);
2. **docs/research/solver-facts.md** (what the tools can and cannot do; check every spec against it);
3. the DECISIONS index (`python scripts/decisions_index.py`).

Branch: `claude/exciting-fermi-qy077p`. Procedure: docs/research/coldspray-procedure.md.

## First action

§40 (WSL A task 2026-11-23-c) is merged: `/NONLOCAL/MAT` is damage-only and silently ignored on quads and TLSPH, so
no zero-code length exists. The length-scale note §11 holds the chain, the ℓ-against-band-width table and three
options. **Peter chooses:**
- (i) a Ge-type nonlocal build on quads (design note first, about 4–5 sessions), then a frozen step-0 test on the
  §25 deck;
- (ii) literature first (choose the ℓ reading; Liu band and grain sizes, an Al feedstock grain size, Chakrabarty & Song
  2020, a primary source for the band-width factor);
- (iii) the softening-off test.

The modeller recommends (ii) with the design note of (i). Then write the WSL A or WSL B task. Draft no hunch before
that.

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
- **Length-scale idea (not a hunch), the current focus (Peter 2026-11-23):** length-scale-note-2026-11-20.md (§11:
  no host carries ℓ in σ_y and T (§40); a gradient band is about 4.7ℓ wide, so "ℓ = grain size" and "band = grain
  size" are different models; Ge's nonlocal runs still drift 7–9 % at the edge). Softening is active from the first judged
  frame on quads (§33); TLSPH heats and softens without q heating (§34). Step 0 ("a missing length causes the edge
  failure") is still unjustified; the softening-off test is on hold.
- **Problem as equations:** problem-formalism.md, every equation checked against the fork source (§35); points
  (c) crack-tip bond boundary, (e) identifiability, (f) bonds weakest at the hot edge, (g) slip vs ASI.

## Sessions and open tasks

| Session | Where | Open task |
|---|---|---|
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | — |
| WSL A | fork `sph-hvi-contact` branch `cs12`; results to `coldspray/opencourant-sph` | none; 2026-11-23-c closed (§40); 2026-11-22-d closed (§39); 2026-11-22-c closed (§38); 2026-11-23-a closed (§37); 2026-11-22-b closed (§36); 2026-11-20-a closed (§31); 2026-11-21-a/b, 2026-11-22-a closed (§33–§35) |
| WSL B | `coldspray/bonding-methods-reading` | b9: only Dai 2025 left (closed access); b13 closed (merged) |

## Open for Peter

1. **Track B is paused** (DECISIONS 2026-11-23); it resumes only by your decision.
2. Friction for unbonded contact (the off branch is frictionless; physics leans toward sticking friction at GPa).
3. Mohanty 2022 alone (oxide-thickness series in Al, pre-registered post hoc) or not; R2 and R3.
4. Physical length scale (the focus): options (i)–(iii) of the note §11 (see First action). Chakrabarty & Song 2020
   needs your download.
5. CS-20: no unseen ring-map source; candidate for parking.
6. The hot-edge choice in cs12: σ_B ∝ σ_y(T) makes bonds weakest where they form (problem-formalism.md §2(f)).

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
| Solver log §1–§40 (§41 next) | docs/research/opencourant-verification.md; rows in docs/research/opencourant/results/ |
| Hunches | coldspray-hunches.md (index); recent: cs22b (supported), cs23 (refuted) |
| Checks | driver-check-2026-11-17.md, switch-check-2026-11-18.md, softening-check-2026-11-20.md, tlsph-temperature-check-2026-11-21.md, slip-check-2026-11-22.md |
| Ladders (frozen) | sph-contact-ladder.md, sph-tlsph-ladder.md, sph-tlsph-b-ladder.md |
| Multi-particle brainstorm | multi-particle-spec.md, multi-particle-tried.md, multi-particle-brainstorm-2026-11-18.md |
| Readings | data/ge2026_reading.md, data/tang2024_reading.md, data/bonding_methods_reading.md, data/boundary_integration_reading.md, data/profizi2016_reading.md |
| Tasks | docs/research/tasks/wsl-a.md, wsl-b.md |
| Problem as equations (working note) | docs/research/problem-formalism.md (checks: scripts/formalism_check.py) |
| Archives | docs/handoff-archive.md, docs/status-archive.md |
