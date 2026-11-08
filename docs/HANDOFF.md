# Handoff — 2026-11-08, session end (cold-spray track; earlier versions in git history)

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." Then read
docs/STATUS.md (top entries) and the DECISIONS index (top of docs/DECISIONS.md). Branch:
`claude/exciting-fermi-qy077p`. Procedure: docs/research/coldspray-procedure.md (who writes where; tasks for other
sessions in docs/research/tasks/; HANDOFF at session end only; DECISIONS for changes of direction only).

**First action next session:** `git fetch` and check for WSL B's branch `coldspray/b03-b12-outcomes` (task b8).
Leak-scan it, then merge it. Its rows are labelled exposed and carry no verdicts.

**Arena 2 is paused** at Phase 6 step 5; resuming means step 6 (blind audit, Target D, tag contact-v1.0). Arena 1 is
released as benchmark-v1.0.

## 1. Where the cold-spray track stands

Peter's application: multi-particle cold spray with coating build-up; deposition efficiency and bonding; a
mechanistic model that states its own range of validity. Verdict "go: discipline only" (DECISIONS 2026-11-03): no
arena and no search, the schemeforge process used to develop models.

**The core** (plan revision 2, DECISIONS 2026-11-04; coldspray-go-nogo.md) is the **interface law**: oxide fracture,
fresh-metal contact, bond or separation. It is a closure, and data come first (stop rule, DECISIONS 2026-11-05).
The thermal question and CS-14b are **parked** (DECISIONS 2026-11-07).

**Two tracks:** single-impact, and **build-up** (coldspray-buildup-track.md). **Hunch budget:** at most 5 open
untested hunches, each must discriminate on obtainable data. The count is **3 of 5** (CS-10, CS-12, CS-17). Rules
are at the top of coldspray-hunches.md.

**End point of the single-impact phase** (DECISIONS 2026-11-07): the six pending blind papers scored or
unobtainable, and the T3 request sent or dropped; then one short synthesis.
- B03, B05 and B12 count as done: closed without pre-registration on 2026-11-08, because nothing could be
  discriminated on them.
- **Remaining: B06, B07, B16 (closed access, with Alex).**
- The campaign trigger for the T3 request (DECISIONS 2026-11-05) named B06 and B05. B05 has no v_cr, so the trigger
  now waits on **B06** alone.

**The decisive open question is test T3,** v_cr against oxide thickness at a fixed oxide type. Frozen predictions
for Al 6061, 15 µm, 17 → 25 nm:

| Model | Δv_cr |
|---|---|
| Z18_Yd (Na2025 Eq. 6) | about +127 m/s |
| Z18_static | about +92 m/s |
| CS-10 | about +37 m/s |
| CS-12 minimal | 0 within one window |

No unseen thickness series is known. The Panova thesis screen and the 2024 paper have none. The request is drafted
in coldspray-measurement-request-t3.md.

## 2. What happened on 2026-11-07/08 (details in STATUS)

- **Build-up, Q-B1** (is deposit fracture set by the striking shot or by the stack's history?): Reiser2024 was
  digitized (data/buildup_reiser2024.csv, 137 shots, 7 fracture events).
  - Answer, descriptive: removal only by slow, rebounding particles (below v_cr) is not supported; striker and
    history cannot be separated.
  - Post hoc: all fracturing shots lie in 0.98–1.20 v_cr. A near-threshold-striker hunch is **parked**.
- **Panova thesis via WSL B:**
  - Panova2026a (ch. 5): three two-particle Cu stacks, particle–particle bonded fraction 7, 18 and 9 %.
  - Panova & Schuh 2024 (ch. 2), **released by Peter**: Cu (Alfa Aesar) on H02 Cu, V_cr 540 ± 5 m/s (row P24-Cu).
    Powder Y_d 403 ± 90 MPa. Bonded fraction 6–89 % against velocity, peaking at 1.30 V_cr and falling to 13 % at
    1.62 V_cr.
  - Panova2026b's PA rows used a **different powder** (Praxair CU-159-3).
- **HG2018b primary read** (rows P18): Al 797–824, Ni 650–660, Cu 539–568, Zn 518–523 m/s (±2 %).
  - Panova2026b and Dowding quote it correctly. The H20 rows are Hassani2020's own windows, not misquotes.
  - Post hoc, CS-05 would cross its kill line against the primary Al window; its frozen verdict stays.
  - To reach MIT DSpace files, the host `cf003.cdn.4science.cloud` was added to the Default environment.
- **Z7 on B02, post hoc:** soft/hard ratio 1.064 against a measured 1.133 ± 0.032 (right sign, half the contrast).
  Its plate ε_c inputs are derived hardening exponents, not measurements.
- **Judge v2 proposal** (draft, not adopted; coldspray-judge-v2-proposal.md): R1 primaries first, R2 widen bracket
  windows by the stated velocity error. 7 of 10 window-dependent verdicts are robust.
- **Powder properties:** no impacted powder in any source read has a failure strain or hardening exponent
  (inventory in data/README.md; data/powder_properties_theses.md).
- **B03, B05, B12:** step-1 inputs merged. Provenance (data/b03_b12_provenance.md): B12's Al data are reused from
  HG2018b and HG2019b, and B03 and B12-c1 are probably not independent. All three closed without pre-registration;
  outcomes go to the data table as exposed (task b8).

## 3. Hunches and zoo (index: docs/research/coldspray-hunches.md)

| Id | What | State |
|---|---|---|
| CS-01…CS-06 | retrospective v1 | CS-02, CS-03 supported; CS-01, CS-05 inconclusive; CS-06 refuted (caveats 1–2 in coldspray-results-v1.md) |
| CS-07 | oxide raises v_cr | B10: not refuted, support undetermined; B14: supported (exposed; type and thickness changed together) |
| CS-08 | strength raises v_cr within an alloy | refuted on B10 |
| CS-09 | sound speed alone within B10 | undetermined (would be refuted under judge-v2 R2) |
| CS-10 | energy balance with oxide shell term | frozen, open; no blind paper reports particle strength |
| CS-11 | interface bracket | inconclusive |
| CS-12 | interface as Markov blanket; thickness-independent at fixed oxide type | frozen, open; T3 decisive |
| CS-13 / 13b / 13c | conduction regularises the contact edge | 13c refuted; stop rule |
| CS-14 / 14b | interface submodel cell | **parked** 2026-11-07 |
| CS-16 | substrate hardness raises v_cr (Cu) | refuted on B02 |
| CS-17 | substrate strain-hardening capacity (directional) | frozen, open; domain restricted post hoc to wrought substrates; no unseen test data |
| Z18 | Na2025 Eq. 6 | frozen zoo member |

Reserved: CS-15 (whole-particle model with the interface law). Parked, not registered: the near-threshold striker
(build-up).

## 4. Blind set (coldspray-blind-literature.md; B4 exposure log and the closure note at its end)

| Paper | State |
|---|---|
| B10 | scored |
| B02, B14 | scored (coldspray-results-b02-b14.md, with Z7 addendum and note) |
| B03, B05, B12 | closed without pre-registration (2026-11-08); outcomes via WSL B b8, labelled exposed |
| B04, B13 | no v_cr; nothing to predict |
| B01, B08, B09, B11, B15 | no single-impact v_cr |
| **B06, B07, B16** | **closed access, with Alex.** B06 (oxide fracture) is the one that matters |

Thesis pages with B03 values (Panova pp. 56–57, 146) are no longer restricted once B03's outcomes are merged.
Tiamiyu 2022 remains an unscreened blind-list-2 candidate.

## 5. Next steps (in order)

1. **Merge WSL B b8** (B03, B12 outcomes) after a leak scan; add one STATUS line.
2. **B06, B07, B16 when Alex sends them:** WSL B step 1 → leak scan → merge → check whether anything frozen can be
   discriminated. If so, freeze (new pre-registration file) → step 3 → score. If not, close as for B03.
3. **After B06:** the campaign-trigger decision for the T3 request (Peter), then the single-impact synthesis.
4. **Peter's open decisions:** section 9.
5. **Data gaps:**
   - a failure strain or hardening exponent of any impacted powder; only a measurement or a new source would close
     it (micro-compression curves, as in Na2025);
   - Bay 1983 primary (Peter can supply it).

## 6. Rules that must not be broken

- **Blind test** (rules B1–B6):
  - the modeller never opens a hold-out paper or its outcomes before its predictions are committed, or before Peter
    closes it;
  - inputs come from WSL B and are leak-scanned before reading;
  - the scoring script is committed before outcomes are read;
  - post-hoc numbers are labelled;
  - verdicts follow the frozen rules even when that leaves them undetermined.
- **Frozen files are never edited after scoring** (preregistrations, predictions_*.csv, scores_*.csv, hunch
  files). Amendments are new files or dated addenda.
- **Simulation:** no simulated v_cr before the verification ladder and convergence; no erosion as a production
  method; no OpenCourant fork.
- **Iron rules of CLAUDE.md:** never call a result novel; record negative results; no invented values.
- **Hunch budget:** a new hunch must discriminate on obtainable data.
- **Licence:** OpenCourant's Siemens parts for local use only. PDFs are never committed.

## 7. Sessions and branches

| Session | Role | Branch it pushes | Task file |
|---|---|---|---|
| Cloud (modeller) | models, predictions, scoring, notes, merges | `claude/exciting-fermi-qy077p` | — |
| WSL A | OpenCourant simulations | `coldspray/opencourant-sph` | docs/research/tasks/wsl-a.md (**no open task**; thermal path parked) |
| WSL B | blind extraction and source checks | one branch per task | docs/research/tasks/wsl-b.md (**open: b8**; standing fetch rule at b4) |

WSL B may fetch open copies itself (standing rule in wsl-b.md); paywalled papers come from Peter or Alex.

## 8. Key files

| What | Where |
|---|---|
| Decisions | docs/DECISIONS.md (index: `python scripts/decisions_index.py`) |
| Plan, assumption inventory, triggers | docs/research/coldspray-go-nogo.md |
| Data tables | docs/research/data/ (README there, with the powder-property inventory) |
| Zoo, predictions, scorers | src/schemeforge/research/coldspray*.py |
| Hunches, preregistrations | docs/research/coldspray-hunch*.md, coldspray-preregistration*.md |
| Build-up track | coldspray-buildup-track.md; scripts/digitize_reiser2024.py, buildup_qb1.py, plot_buildup_reiser2024.py |
| Judge v2 proposal | coldspray-judge-v2-proposal.md; scripts/judge_v2_sensitivity.py |
| Z7 post-hoc check | scripts/z7_cu_posthoc.py; addendum in coldspray-results-b02-b14.md |
| WSL B extractions | data/panova_thesis_screen.md, panova2026a_stacks.md, panova2024_ch2.md, powder_properties_theses.md, b03_b12_provenance.md |
| Measurement request (draft) | coldspray-measurement-request-t3.md |

## 9. Open for Peter

Nothing below has been decided.

1. **Judge v2** (coldspray-judge-v2-proposal.md): adopt R1 and R2 for future freezes? Is the ±2 % velocity error per
   shot or shared within a campaign? Rescore B10 under B6 (CS-09 would be refuted, CS-07 inconclusive), or leave it
   undetermined as recorded?
2. **CS-17's post-hoc domain restriction** (wrought substrates only): accept, or drop or reformulate CS-17.
3. **Measurement request, extra items** (only if the campaign trigger is met):
   - the deposit-vs-plate contrast: one powder on a deposit, an annealed deposit and a cold-rolled plate of matched
     hardness;
   - one powder on several tempers of one wrought alloy (tests CS-17);
   - micro-compression stress–strain curves of the LIPIT powders (closes the failure-strain gap).
4. **Oxide-chemistry hunch:** two budget slots are free. Note that the B14 RH-95-D signal drops from 1.6 to 0.9
   window widths if windows include the velocity error (judge v2, post hoc).
5. **Blind list 2:** screen Tiamiyu 2022 or drop the idea.
6. **Idea D** (restitution data, Tang 2025 PNAS SI): Peter can supply the SI files.
