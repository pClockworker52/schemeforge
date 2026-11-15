# Handoff — 2026-11-15, after the route review (cold-spray track; earlier versions in git history)

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." Then read the top of
docs/STATUS.md and the DECISIONS index. Branch: `claude/exciting-fermi-qy077p`. Procedure:
docs/research/coldspray-procedure.md (who writes where; tasks for the other sessions in docs/research/tasks/).

**Route review 2026-11-15 held** (DECISIONS 2026-11-15 "Route review 2026-11-15"; folder
docs/research/route-review-2026-11-15/, with reviewer-1.md and reviewer-2.md verbatim):
- **D1:** the bond stays in the solver (Peter; reviewers and modeller had recommended one-way first).
- **D2:** p_n and Y are judged on a measurement-only skin as 0.5 µm surface-disc averages; depth bands reported only.
- **D3:** one bounded TLSPH attempt (BCT off, skin, fitted flat face) plus a BCT-off survival probe; fallback: the
  reduced route.
- **D4:** dead-end trigger fixed in the DECISIONS entry (p_n and Y − 1 within 3.5 % + U_ref at R/64 on T-B2; no
  convergence R/32 → R/64; survival probe fails; U_ref ≤ 1.75 % first). If it fires: reduced route.
- **D5:** WSL A task 2026-11-15-b (quad R/256 and U_ref, TL internal energy, contact list; then survival probe; then
  fitted face and skin); WSL B task b11 (boundary integration, patch tests, Tang 2021 in full), after b10.

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." First action: read and
merge whatever WSL A (§23) or WSL B (b10, b11) has pushed; leak-scan WSL B branches.

**Done 2026-11-14 (after /clear):**
- §20 merged (7984e1c): **CS-18b refuted at T-S1** by its frozen kill rule (R/32 rebound 0.860). Hunch count 3 of 5.
- §20.4–20.5 merged (c329481): T-S1 R/64 with BCT passes its own criteria; **T-S1 R/32 with BCT off: rebound
  0.9988**. Cause: BCT on curved, few-particle wall patches.
- Peter: stay with TL; **CS-18c** with a corrected BCT; UL SPH (CS-19) is the fallback; no route review; rigour
  without ceremony (DECISIONS 2026-11-14).

**Peter, 2026-11-14 (later):** requirements unchanged for now (bond in the solver stays). **After the next failure, hold a review session before anything else.** Its inputs were raised in chat:
- every SPH failure so far was a surface failure;
- a one-way bond for the first claim, evaluating Bay afterwards from the interface-state histories (exact up to the first bonding, CS-12 (a); v_cr only as a lower bound);
- a dead-end trigger, written down before results.
Modeller's estimates (judgment): CS-18c full ladder 35–50 %; edge convergence 25–35 %; whole chain 5–10 % (about 10–15 % to a first claim with a one-way bond).

**Done 2026-11-15:** §21 merged (7073f1e). No BCT variant is clean; "BCT on flat walls only" rejected
(DECISIONS 2026-11-15).

**(Done.)** The route review was started with "Read docs/research/route-review-2026-11-15/brief.md and run the route
review." The folder holds the session brief (facts, decisions D1–D6, the modeller's recommendations in a section withheld from
independent reviewers) and inputs.md (two external texts verbatim, with the modeller's critiques).

**§22 merged (2026-11-15): the rule is not met** (4 of 20 / 6 of 20 averages within 3.5 %). The face-layer deficit
comes with any point-loaded face, rigid wall or not. **Next: Peter's review session**, before any new BCT variant or
hunch. Its inputs:
- the surface pattern;
- the one-way bond;
- TLSPH energy accounting;
- a written dead-end trigger;
- the external four-step proposal and its critique (in chat 2026-11-15; save them if Peter wants);
- the state report (Claude Docs, "Cold-spray simulation: state report", 2026-11-15).

## 1. The two tracks

**A. Single-impact data track** (unchanged since 2026-11-08):
- The blind papers B06, B07 and B16 are filed by Peter (2026-11-15). Step 1 is WSL B task b10 (branch
  `coldspray/blind-inputs-b06-b07-b16`; leak-scan before merging). The T3 measurement request (v_cr against oxide
  thickness at a fixed oxide type) waits on B06's step 1.
- B03 and B12 are merged as exposed (d67f72c).
- Open data hunches: **CS-10, CS-12, CS-17.** Details: docs/research/coldspray-hunches.md.

**B. SPH host track:** a solver host for an interface (bonding) law. Peter's requirements (DECISIONS 2026-11-12,
amended 2026-11-14):
- particle shape, rebound and v_cr, and the interface state;
- 3D, with the bond acting in the solver;
- interface outputs judged as **averages over 0.5 µm**, point values at the edge reported only;
- since the route review 2026-11-15: p_n and Y measured on a measurement-only surface skin (0.5 µm surface discs),
  depth-band stresses reported only; a dead-end trigger is in force (DECISIONS 2026-11-15).

## 2. History of track B, in one table

| Step | Result | Where |
|---|---|---|
| No-fork dropped; private fork `sph-hvi-contact` (local `~/sph-hvi-contact`, Siemens files untouched, sidecar config) | | DECISIONS 2026-11-08 |
| Separable SPH–SPH contact, ladder 36c34bd plus Addendum 1 (140b84a) | the laws pass; **B-2, B-3 and D-1 FAIL**; S′ (ξ + order 1) not adopted | §14, §15 |
| CS-18: Total Lagrangian SPH (TLSPH), ladder 583912a | **refuted at T-S0** | §16, coldspray-hunch-cs18.md |
| T-S0 diagnosis | plateau offset = finite strain (the judge's linear reference); viscosity causes most of the rebound loss; TL end layers carry 0.655 and 0.845 of the true stress | §17 |
| Calibration before CS-18b | finite-strain references; thresholds 1.25 × quads or collocated SPH; LAMMPS viscosity; BCT (boundary-consistent traction) | §18 |
| Calibration part 2 | BCT implemented (end layers 0.9999); quad two-body Hertz; α = 5 with Q1 = 0.1; **survival probe passed** (Al–Al, 800 m/s, R/16 and R/32, to 1.0 D/V) | §19 |
| **CS-18b and its ladder frozen** (6f0786a) | rung runs: WSL A task 2026-11-14-a, results in §20 | DECISIONS 2026-11-14 |
| CS-18b core rungs | T-A0, T-S0, T-S0p pass; **T-S1 fails** (R/32 rebound 0.860, contact 5.3 % short; R/16 unstable): **refuted** | §20, DECISIONS 2026-11-14 |
| After the verdict | R/64 with BCT passes; R/32 with BCT off rebound 0.9988: BCT on curved patches is the cause; CS-18c next | §20.4–20.5, DECISIONS 2026-11-14 |

**Known limits of CS-18b, named before its freeze:**
- the conforming sphere's layer 2 stays 26–30 % low under BCT (a reported rung; fix later);
- the engine's wall-force output reads 1.485 × the transmitted force under BCT (metrics read the momentum rate);
- there is no TL internal energy (energy closure is reported only);
- the T-tension and T-D1 limit of 0.095 V rests only on the collocated welded bar, so it is loose (source in the
  ladder);
- the Ganzenmüller journal check is deferred, and required before the first claim.

## 3. Literature and reviews

- **Profizi 2016 and thesis** (F level): data/profizi2016_reading.md.
- **Bonding methods** (WSL B task b9, partial merged 51f1e6d): data/bonding_methods_reading.md.
  - Read: Dai et al. 2026 (F): updated-Lagrangian SPH, Lennard-Jones bond switched on at ε_p ≥ 1.4, no exact
    verification, flattening ratio still moving at d/80. Also Ren & Song 2022 and 2024, and the Khoei abstract.
  - Outstanding, in the background, not blocking: Tang 2021, Ge 2026 (both need a browser download by Peter), and
    Dai 2025, doi:10.1007/s00466-025-02714-1 (closed).
  - **Lesson:** a literature step must sweep for competing methods.
- **Reviews:** sph-route-review-2026-11.md, with its critique, the meta-review supplied by Peter, and
  sph-route-expert-answers-check.md.

## 4. Hunch budget

**3 of 5:** CS-10, CS-12, CS-17 (CS-18b refuted at T-S1, 2026-11-14).

## 5. Open for Peter

1. Track B is settled by the route review until the trigger run: nothing open for Peter until §23 arrives (the
   trigger-run task is drafted from §23 and frozen with Peter). If U_ref > 1.75 %, Peter decides how the reference
   is improved.
2. The E-1 gate draft (docs/research/sph-contact-e1-gate-draft.md): revise to 0.5 µm averages, then thresholds and
   freeze. It applies only if a host passes its ladder.
3. Compute for E-1 at R/48 and finer (raised in chat; not recorded elsewhere at Peter's wish).
4. Track A items from 2026-11-08: judge v2, the CS-17 domain, the T3 extra items, Tiamiyu 2022, the Tang 2025 SI.

## 6. Sessions and branches

| Session | Where | Open task |
|---|---|---|
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | — |
| WSL A | fork `sph-hvi-contact` branch `tlsph`; results to `coldspray/opencourant-sph` | 2026-11-15-b (results to §23) |
| WSL B | `coldspray/blind-inputs-b06-b07-b16`, then `coldspray/boundary-integration-reading`, then `coldspray/bonding-methods-reading` | b10 (step 1 for B06, B07, B16; B03 check), then b11, then b9 (remaining papers) |

## 7. Rules that must not be broken

- **Blind test** (rules B1–B6, coldspray-blind-literature.md):
  - leak-scan every WSL B branch before merging;
  - post-hoc numbers are labelled.
- **Frozen files are never edited** (pre-registrations, hunch files, ladders): verdicts and amendments are dated
  sections or addenda, and post hoc where results were seen.
- **Process:**
  - stop rules apply;
  - predictions are committed before runs;
  - rows only from committed binaries;
  - the no-tuning rule applies after a freeze; before a freeze, calibration uses cases that are not rungs.
- **Iron rules** (CLAUDE.md): never "novel"; record negative results; no invented values; float64.
- **Fork:** the Siemens-licensed files stay byte-identical (`hvi/scripts/check_untouched.sh`); PDFs are never
  committed.

## 8. Key files

| What | Where |
|---|---|
| Decisions | docs/DECISIONS.md (index: `python scripts/decisions_index.py`) |
| Solver log, all sections §1–§20 | docs/research/opencourant-verification.md; rows in docs/research/opencourant/results/ |
| Ladders (frozen) | sph-contact-ladder.md, sph-tlsph-ladder.md, sph-tlsph-b-ladder.md |
| Hunches | coldspray-hunches.md (index), coldspray-hunch-cs18.md, coldspray-hunch-cs18b.md, and the earlier CS files |
| Referee | sph-contact-referee-2026-11-11.md |
| Plan of the fork | sph-hvi-contact-plan.md (milestone 1) |
| Tasks | docs/research/tasks/wsl-a.md, wsl-b.md |
