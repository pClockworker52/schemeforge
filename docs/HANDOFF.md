# Handoff — 2026-11-27: Gate 6 passed, clean-up done, cold spray unpaused; kernel-completion spec drafted (current state only)

Earlier versions: docs/handoff-archive.md (verbatim, 2026-11-21; track state at the pause, 2026-11-27) and git history.

**Start the next session with:** "Read docs/HANDOFF.md and continue." Then read docs/STATUS.md (top), the DECISIONS
index (`python scripts/decisions_index.py`) and the last entry (2026-11-27), and docs/reports/2026-11-25-gate6.md.

Branch: `claude/exciting-fermi-qy077p`; `main` is fast-forwarded to it (2026-11-27). **Two sessions write to the
branch** (this cloud session and a desktop session): `git fetch` and fast-forward before every commit, and never
force-push.

## Order (DECISIONS 2026-11-27, Peter)

1. **Finish Gate 6.** Breakers done and reviewed; none accepted (DECISIONS 2026-11-27). Target D committed (a722ef0).
   Judge tagged contact-v1.0 (6eef4c9; docs/judge/2026-11-27-contact-v10-check.md). Step 7 done (calibration K1: 19 cells,
   0 of 2 required rediscoveries; six hunch drafts ledger/drafts/d7_*). **Gate 6 PASSED** (Peter, 2026-11-27; shortfall
   recorded, DECISIONS 2026-11-27). WSL needs `git fetch --tags` before a contact eval.
2. **Clean the repository** (scope confirmed by Peter 2026-11-27; record docs/reports/2026-11-27-repo-cleanup.md).
3. **Unpause cold spray: done** (DECISIONS 2026-11-27): resumes with the kernel-completion probe. Stage A frozen
   (9369e6c; docs/research/kernel-completion-2026-11-27.md). §43 merged: **both forms fail** (KC-full on
   interface spacing and stiffness contrast; KC-f has no static equilibrium). No Stage B. Next: Peter.

## Sync items

- Done 2026-11-27: the desktop commits 9fe91e1..607c851 are pushed (765b44c); §42 is merged (5208b15); Peter deleted
  every `coldspray/*` remote branch. Only `main` and `claude/exciting-fermi-qy077p` remain. The fork's WSL A notes
  still name `coldspray/opencourant-sph` as the results branch: a new task recreates it from this branch.

## Small open items from the desktop session (2026-11-26; HANDOFF lost them in the 765b44c merge)

- **solver-facts §1 line 26:** corrected 2026-11-27 (p_n usable only at 0.25 a; 0.5 a fails on the block at 600 m/s,
  5/7).
- **B4 exposure log:** one exposure not yet logged (a bond-strength pattern in a search snippet, PMC11544021 =
  Tang 2024, data/tang2024_reading.md). Details are with the desktop session.
- **WSL A housekeeping:** task 2026-11-27-a done and merged (e67d639): R/64-check rows (two differences from §42's
  text reported, text unchanged); g1 deleted.
- Noted, not decided: a G1 rerun with nodal contact-force output (B's E1-F), own proposal needed (DECISIONS 2026-11-26
  contact-edge entry). A candidate for the unpause list, with the kernel-completion probe.

## Open threads (facts with sources)

- **Phase 6 (main line), at Gate 6.** Judge contact-v0.12.dev (735b69e). Done: C4; max_step on every HF instance;
  promo zoo and γ-sweep (none of 20 zoo points meets D1–D8); Target D thresholds accepted (DECISIONS 2026-11-25).
- **Cold spray (paused since 2026-11-24).** Diagnostic exception B closed negative (§42). The contact-edge proposal
  (fork `hvi/PROPOSAL…contact-edge…`, 3d658fd8) was not approved (607c851).
- **Peter's partner-aware contact idea** (fork `cs12` 210d98d4, `hvi/NOTE-2026-11-26-partner-aware-contact.md`), an
  idea note. Three toys found no information only a partner model has; the tested readings are known methods. The
  one untested reading tied to a measured defect: TLSPH kernel completion across the contact, compression only,
  against the face-layer deficit (0.655/0.845 §17, 0.62/0.86 §22; note §13 cause C). Cheap known-answer probe: two
  TLSPH blocks in uniform compression, face stress ratio with and without completion. It cannot fix a singular edge
  field (problem-formalism §2(c)). Candidate for the unpause entry, not before.
- **The fork is reachable from the cloud:** `pclockworker52/sph-hvi-contact` at /home/user/sph-hvi-contact
  (shallow; `git fetch --depth=5 origin cs12`).

## Cold-spray track at the pause (for the unpause)

- **Closing state:** docs/research/coldspray-orientation-2026-11-24.md. **Review:** docs/research/scope-review-2026-11-24/summary.md (both STOP; Peter accepted).
- **Resume conditions of 2026-11-24** (unseen multi-particle stacks, an unseen ring-map source, new single-impact
  v_cr data): none has appeared. The unpause rests on Peter's decision (DECISIONS 2026-11-27).
- **Lesson to carry:** point values at the contact edge and the bond boundary may be singular (problem-formalism
  §2(c)), so any new criterion should be built from finite quantities.
- **Track state in brief** (tracks A and B, length-scale path, formalism): moved verbatim to docs/handoff-archive.md,
  section "2026-11-27".

## Sessions and open tasks

| Session | Where | Open task |
|---|---|---|
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | breaker review after Peter's run; clean-up |
| Desktop | schemeforge | — (pushed 765b44c) |
| WSL A | fork `sph-hvi-contact` branch `cs12`; results to `coldspray/opencourant-sph` (deleted; recreate for a new task) | none (2026-11-27-b closed, §43); 2026-11-27-a closed (e67d639); 2026-11-26-a closed (§42); closed tasks: docs/research/tasks/wsl-a.md |
| WSL B | none (`coldspray/bonding-methods-reading` merged cbe2d88, deleted) | b9: only Dai 2025 left (closed access) |

## Open for Peter

- What the cold-spray track does after §43 (kernel completion failed in Stage A).

## Hunch budget

**2 of 5:** CS-10, CS-17. Parked: CS-20 (2026-11-24), CS-14/14b. Supported: CS-22b (§31; caveat DECISIONS 2026-11-23).
Retired: CS-12. Refuted: CS-23 (§39), CS-22 part 1 (§30), CS-21 part 1 (§28), CS-18b (§20). Index:
docs/research/coldspray-hunches.md.

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
