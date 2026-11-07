# Handoff — 2026-11-07, session end (cold-spray track; earlier versions in git history)

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

**Two tracks since 2026-11-07:** single-impact (this section) and **build-up** (docs/research/coldspray-buildup-track.md;
questions and data audit first, no hunches yet). **Hunch budget:** at most 5 open untested hunches across both
tracks, each must discriminate on obtainable data; count 4 of 5 (rules at the top of coldspray-hunches.md).
**End point of the single-impact phase:** the six pending papers scored or unobtainable, and the T3 request sent or
dropped; then one short synthesis (DECISIONS 2026-11-07).

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
| CS-07 | oxide raises v_cr | B10: not refuted, support undetermined; **B14: supported (exposed;** type and thickness changed together) |
| CS-08 | strength raises v_cr within an alloy | refuted on B10 |
| CS-09 | sound speed alone within B10 | undetermined (no window bounds) |
| CS-10 | energy balance: jetting + plastic work + shell work (t_ox/d) | frozen, fitted on B10 (β 0.3774, γ 3.19e11 Pa); leave-one-out no better than a constant; relative of Na2025, not a variant |
| CS-11 | interface bracket (welded vs frictionless) | inconclusive: neither bound computable in OpenCourant (§10) |
| CS-12 | interface as Markov blanket; Bay-type criterion; thickness-independent at fixed oxide type | frozen; variant of Bay; T1 exposed; T3 decisive; criterion is a hybrid of Bay's two mechanisms (reading note Zhang & Bay 1997) |
| CS-13 / 13b / 13c | conduction regularises the contact edge | 13b blocked (§12), **13c refuted** (§13); stop rule: no CS-13d |
| CS-14 / 14b | interface submodel cell (t/w, Y', p_E against thickness) | 14b frozen: continuum film with cohesive cracks instead of DEM; DEM rung kept as record (R0 run, R1 not) |
| CS-16 | substrate hardness raises v_cr for matched Cu | **refuted on B02:** hard − soft = −75 m/s against +102 predicted |
| CS-17 | substrate strain-hardening capacity, not hardness (directional) | frozen 2026-11-07; domain restricted to wrought substrates **post hoc** (Panova PA-02 contradicts it otherwise); no unseen test data known |
| Z18 | Na2025 Eq. 6 (Lienhard jet model), variants Yd and static | frozen; Z18_static fails on its own calibration data (RMS 72.5) |

Reserved: **CS-15** for a whole-particle model (SPH with the interface law at the interface), not registered.

**Proposed, awaiting Peter:** park the thermal question (no JAX port) and park CS-14b (its answer hinges on the
oxide's unknown cohesive length; it cannot decide T3).

## 3. Blind set (docs/research/coldspray-blind-literature.md; B4 exposure log at its end)

| Paper | State |
|---|---|
| B10 | scored (coldspray-results-b10.md) |
| **B02, B14** | **scored** (coldspray-results-b02-b14.md; freeze 27e7eea → addendum 542f810 → scorer f8fb8f5 → outcomes add80b8 → scores dabe6a7). Z6 within 1–6 % on dry B14 (in-sample material); RH-95-D 68.5 m/s below RH-95 at near-equal thickness |
| B04, B13 | inputs extracted; no v_cr; nothing to predict |
| B01, B08, B09, B11, B15 | no single-impact v_cr |
| B03, B05, B06, B07, B12, B16 | pending: Peter asked Alex for the PDFs on 2026-11-07; they go to WSL B, never to the modeller. B06 and B05 matter most (oxide). |

Notes:
- CS-10 and Z18 could not run on B02 or B14 (no particle strength reported). Most future papers will hit the same
  wall unless they report powder strength.
- Extraction rule added 2026-11-05: interface observations after impact are outcomes (withheld in step 1).
- Candidate papers for a **blind list 2** (Tiamiyu 2022; Panova & Schuh 2024 ×2): a yes/no screening task for
  WSL B is proposed, not yet written.

## 4. Next steps (in order)

1. **B03, B05, B06, B07, B12, B16 as they arrive:** WSL B step 1 → leak scan → merge → add their materials to
   `MATERIAL` in coldspray_blind2.py and freeze (new pre-registration file) → step 3 → score.
2. **Build-up track:** audit done (33152ad); **Q-B1 adopted and answered descriptively** (coldspray-buildup-track.md,
   "Q-B1"; data/buildup_reiser2024.csv; figure figures/buildup/reiser2024_stacks.png). The data rule out removal only by
   sub-v_cr rebounders; striker vs history not separable (7 events). Post hoc: all fracturing shots in 0.98–1.20 v_cr.
   Near-threshold-striker hunch parked. Panova2026a: Peter has the Panova thesis; route via WSL B (item 0 of section 9).
3. **Peter's open decisions:** section 9.
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
| WSL B | blind extraction | `coldspray/blind-inputs`, `coldspray/<paper>-outcomes` | docs/research/tasks/wsl-b.md (no open task) |

WSL B merged its step-1 inputs into the modeller branch itself (7a9e0b5); by the procedure only the modeller merges.
Its new task says so explicitly.

## 7. Simulation status (record; the thermal path is closed)

- **OpenCourant** (WSL, ~/opt/opencourant/latest-20261011; verification record opencourant-verification.md §1–§13):
  - 2D needs `Isolid = 17`; 2D quads have **no heat conduction** (§11);
  - SPH is 3D-only; SPH–SPH contact is a kernel weld without defined contact (§9.8, §10.3);
  - the SPH heat path is unreliable (§12);
  - every Lagrangian contact edge fails earlier with refinement, with or without conduction (§8.3, §10.5, §13).
- **Kinematic view** (2026-11-07, coldspray-kinematics.md; `impact_kinematics.py`, figures in
  docs/research/figures/kinematics/): rigid sphere into a rigid flat, contact-edge speed against the bulk sound
  speed. Geometry only. The edge turns subsonic at every impact speed (β_c = atan(V/c): Al 5–12°, Cu 7–16°, at
  65–261 ps for d = 15 µm), so geometry gives no threshold; Z6 reads as "subsonic at a fixed angle of 8.5°" (post hoc
  reading).
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
| Kinematic view | coldspray-kinematics.md |
| Results B02/B14 | coldspray-results-b02-b14.md |

## 9. Open for Peter

Adopted 2026-11-07 (no longer open): the build-up track (coldspray-buildup-track.md), the hunch budget (max 5 open
untested; now 4/5, rules in coldspray-hunches.md), and the end point of the single-impact phase (DECISIONS
2026-11-07). An oxide-chemistry hunch (item 5) would take the fifth slot.

Nothing below has been decided; each needs Peter's call.

0. **Build-up:** the near-threshold-striker hunch is **parked** (Peter, 2026-11-07; budget stays 4/5). Open: whether
   the deposit-vs-plate contrast goes into the T3 measurement request; and the **Panova thesis** (MIT DMSE 2026,
   on Peter's machine, not opened by the modeller): proposed route is WSL B, first a yes/no screen (does it contain
   Panova & Schuh 2024, or values from pending blind papers B03/B05/B06/B07/B12/B16?), then a role-separated
   extraction of the Panova2026a chapter (two-particle stacks, bonded fraction) if it is clean or can be cut.

1. **Parkings:** the thermal question (no JAX port after CS-13c) and CS-14b (its answer hinges on the oxide's unknown
   cohesive length; it cannot decide T3). Recommendation: park both.
2. **Blind list 2 screening task** for WSL B: yes/no screen of Tiamiyu 2022 and the two Panova & Schuh 2024 papers
   (oxide series? interface maps?) before anyone reads them. Not written yet.
3. **CS-17's post-hoc domain restriction** (wrought substrates only, because Panova PA-02 contradicts it otherwise):
   accept as frozen, or treat the PA-02 tension as a reason to drop or reformulate CS-17 before it meets data.
4. **A second item for the measurement request:** one powder on annealed, cold-rolled and peak-aged tempers of one
   wrought alloy (tests CS-17). Only if the campaign trigger is met.
5. **Oxide chemistry as its own hunch:** B14's RH-95-D result (−68.5 m/s at near-equal thickness) suggests an oxide
   type term. Any hunch inspired by it cannot be tested on B14. Register or not.
6. **Idea D** (restitution data, Tang 2025 PNAS SI): the source host is probably blocked here; Peter can supply the
   SI files.
7. **Post-hoc spall law Z7 for Cu** from Lucas's Table 2 (failure strain now known): run as a labelled post-hoc
   check, or skip.
