# Handoff — 2026-11-07 (cold-spray track; replaces the 2026-11-04 version, which is in git history)

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." Then read
docs/STATUS.md (top entries) and the DECISIONS index (top of docs/DECISIONS.md). Branch:
`claude/exciting-fermi-qy077p`. Procedure: docs/research/coldspray-procedure.md (who writes where; tasks for other
sessions in docs/research/tasks/; HANDOFF at session end only; DECISIONS for changes of direction only).

**Arena 2 is paused** at Phase 6 step 5; resuming means step 6 (blind audit, Target D, tag contact-v1.0). Arena 1 is
released as benchmark-v1.0.

## 1. Where the cold-spray track stands

Peter's application: multi-particle cold spray with coating build-up; deposition efficiency and bonding; a
mechanistic model that states its own range of validity. Verdict "go: discipline only" (DECISIONS 2026-11-03): no
arena and no search, the schemeforge process used to develop models.

**The core, as of plan revision 2** (DECISIONS 2026-11-04; docs/research/coldspray-go-nogo.md): the **interface
law** (oxide fracture, fresh-metal contact, bond or separation). No affordable simulation resolves it; it is a
closure. Simulated v_cr only with a stated interface law or both bracket bounds. **Data side first** (stop rule,
DECISIONS 2026-11-05).

**The decisive open question: test T3,** v_cr against oxide thickness at a fixed oxide type. Four frozen predictions
for Al 6061, 15 µm, 17 → 25 nm:

| Model | Δv_cr |
|---|---|
| Z18_Yd (Na2025 Eq. 6, as published) | about +127 m/s |
| Z18_static | about +92 m/s |
| CS-10 | about +37 m/s |
| CS-12 minimal | 0 within one window |

No unseen series exists yet. The measurement request is drafted (docs/research/coldspray-measurement-request-t3.md);
it goes out only under the campaign trigger (DECISIONS 2026-11-05): after B06 and B05 are scored, if T3 is still
undecided.

## 2. Hunches and zoo (index: docs/research/coldspray-hunches.md)

| Id | What | State |
|---|---|---|
| CS-01…CS-06 | retrospective v1 | CS-02, CS-03 supported; CS-01, CS-05 inconclusive; CS-06 refuted (coldspray-results-v1.md) |
| CS-07 | oxide raises v_cr | B10: not refuted, support undetermined; B14 test frozen (exposed) |
| CS-08 | strength raises v_cr within an alloy | refuted on B10 |
| CS-09 | sound speed alone within B10 | undetermined (no window bounds) |
| CS-10 | energy balance: jetting + plastic work + shell work (t_ox/d) | frozen, fitted on B10 (β 0.3774, γ 3.19e11 Pa); leave-one-out no better than a constant; relative of Na2025, not a variant |
| CS-11 | interface bracket (welded vs frictionless) | inconclusive: neither bound computable in OpenCourant (§10) |
| CS-12 | interface as Markov blanket; Bay-type criterion; thickness-independent at fixed oxide type | frozen; variant of Bay; T1 exposed; T3 decisive; criterion is a hybrid of Bay's two mechanisms (reading note Zhang & Bay 1997) |
| CS-13 / 13b / 13c | conduction regularises the contact edge | 13b blocked (§12), **13c refuted** (§13); stop rule: no CS-13d |
| CS-14 / 14b | interface submodel cell (t/w, Y', p_E against thickness) | 14b frozen: continuum film with cohesive cracks instead of DEM; DEM rung kept as record (R0 run, R1 not) |
| CS-16 | substrate hardness raises v_cr for matched Cu | frozen on B02 (addendum): 480 / 583 m/s, Δ +102 |
| Z18 | Na2025 Eq. 6 (Lienhard jet model), variants Yd and static | frozen; Z18_static fails on its own calibration data (RMS 72.5) |

Reserved: **CS-15** for a whole-particle model (SPH with the interface law at the interface), not registered.

**Proposed, awaiting Peter:** park the thermal question (no JAX port) and park CS-14b (its answer hinges on the
oxide's unknown cohesive length; it cannot decide T3).

## 3. Blind set (docs/research/coldspray-blind-literature.md; B4 exposure log at its end)

| Paper | State |
|---|---|
| B10 | scored (coldspray-results-b10.md) |
| **B02, B14** | **predictions frozen** (coldspray-preregistration-b02-b14.md, 27e7eea; CS-16 addendum 542f810); **scoring script committed** (f8fb8f5); **WSL B task 2026-11-07-b2 (step 3, outcomes) open**, branch `coldspray/b02-b14-outcomes` |
| B04, B13 | inputs extracted; no v_cr; nothing to predict |
| B01, B08, B09, B11, B15 | no single-impact v_cr |
| B03, B05, B06, B07, B12, B16 | pending (Peter is obtaining them). B06 and B05 matter most (oxide). |

Notes:
- CS-10 and Z18 could not run on B02 or B14 (no particle strength reported). Most future papers will hit the same
  wall unless they report powder strength.
- Extraction rule added 2026-11-05: interface observations after impact are outcomes (withheld in step 1).
- Candidate papers for a **blind list 2** (Tiamiyu 2022; Panova & Schuh 2024 ×2): a yes/no screening task for
  WSL B is proposed, not yet written.

## 4. Next steps (in order)

1. **When WSL B pushes B02/B14 outcomes:** check that only vcr_lipit.csv changed, run
   `python -m schemeforge.research.coldspray_blind2_score`, write the results note, merge.
2. **B03, B05, B06, B07, B12, B16 as they arrive:** WSL B step 1 → leak scan → merge → add their materials to
   `MATERIAL` in coldspray_blind2.py and freeze (new pre-registration file) → step 3 → score.
3. **Peter's open decisions:** the two parkings (section 2); the screening task (section 3); the geometric
   (kinematic) impact view, offered; Idea D (restitution data from Tang 2025 PNAS SI), offered.
4. **Data gaps:**
   - HG2018b primary (Al, Ni, Cu, Zn conflicting quotes);
   - strength of the impacted powders (blocks CS-10 and Z18);
   - Bay 1983 primary (files.aws.org blocked here; Peter can supply it).

## 5. Rules that must not be broken

- **Blind test** (rules B1–B6):
  - the modeller never opens a hold-out paper or its outcomes before its predictions are committed;
  - inputs come from WSL B and are leak-scanned before reading;
  - the scoring script is committed before outcomes are read;
  - post-hoc numbers are labelled;
  - verdicts follow the frozen rules even when that leaves them undetermined.
- **Frozen files are never edited after scoring** (preregistrations, predictions_*.csv, hunch files). Amendments are
  new files (CS-13b, CS-14b) or explicitly allowed addenda committed before outcomes.
- **Simulation:** no simulated v_cr before the verification ladder and convergence; no erosion as a production
  method; no OpenCourant fork.
- **Iron rules of CLAUDE.md:** never call a result novel; record negative results; no invented values.
- **A detection metric gets its own rung** before it decides a verdict (procedure note).
- **Licence:** OpenCourant's Siemens parts for local use only; no binaries or QA decks committed.

## 6. Sessions and branches

| Session | Role | Branch it pushes | Task file |
|---|---|---|---|
| Cloud (modeller) | models, predictions, scoring, notes, merges | `claude/exciting-fermi-qy077p` | — |
| WSL A | OpenCourant simulations | `coldspray/opencourant-sph` | docs/research/tasks/wsl-a.md (no open task) |
| WSL B | blind extraction | `coldspray/blind-inputs`, `coldspray/<paper>-outcomes` | docs/research/tasks/wsl-b.md (task 2026-11-07-b2 open) |

WSL B merged its step-1 inputs into the modeller branch itself (7a9e0b5); by the procedure only the modeller merges.
Its new task says so explicitly.

## 7. Simulation status (record; the thermal path is closed)

- **OpenCourant** (WSL, ~/opt/opencourant/latest-20261011; verification record opencourant-verification.md §1–§13):
  - 2D needs `Isolid = 17`; 2D quads have **no heat conduction** (§11);
  - SPH is 3D-only; SPH–SPH contact is a kernel weld without defined contact (§9.8, §10.3);
  - the SPH heat path is unreliable (§12);
  - every Lagrangian contact edge fails earlier with refinement, with or without conduction (§8.3, §10.5, §13).
- **JAX code:**
  - `impact_axisym.py`: elastic 2D axisymmetric (rungs 0, 1);
  - `blanket_dem.py`: DEM film cell, superseded by CS-14b.

  Figures: docs/research/figures/cs14/; impact animations: docs/research/opencourant/figures/.

## 8. Key files

| What | Where |
|---|---|
| Decisions | docs/DECISIONS.md (index: `python scripts/decisions_index.py`) |
| Plan, assumption inventory H1–H8, triggers | docs/research/coldspray-go-nogo.md |
| Data tables | docs/research/data/ (README there) |
| Zoo, predictions, scorers (not judges) | src/schemeforge/research/coldspray*.py |
| Hunches and preregistrations | docs/research/coldspray-hunch*.md, coldspray-preregistration*.md, coldspray-zoo-z18.md |
| Reading notes | coldspray-reading-zhangbay1997.md, coldspray-reading-na2025.md, coldspray-literature-interface.md (external, exposure header) |
| Blind set, prompts | coldspray-blind-literature.md, coldspray-extraction-prompt*.md, coldspray-literature-prompt-2026-11*.md |
| Measurement request (draft) | coldspray-measurement-request-t3.md |
