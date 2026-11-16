# Handoff — 2026-11-16, after §23 (cold-spray track; earlier versions in git history)

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." Then read the top of
docs/STATUS.md and the DECISIONS index. Branch: `claude/exciting-fermi-qy077p`. Procedure:
docs/research/coldspray-procedure.md (who writes where; tasks for the other sessions in docs/research/tasks/).

**First action:** fetch and merge what WSL A pushed:
- task 2026-11-16-a, results in §24: the contact-particle interface file; the momentum-restoring VCI (time box two
  working days; F2 stands if it fails); then the **trigger run**. Record the rule outcome of the trigger by clause.
  Clause 2 has a noise floor (post hoc);
- task 2026-11-16-b, results in §25: the **P3 probe** on 2D quads, judged by its reading rule. The outcome goes to
  Peter.

**2026-11-16, odds review** (docs/research/odds-review-2026-11-16/, summary.md): two independent reviewers put the
trigger pass at 6–8 % and the whole chain at about 0.3 %, about ten times below the modeller's figures. Peter
(DECISIONS "After the odds review"):
- run the trigger as a bounded cost;
- run the P3 probe in parallel;
- prepare the reduced route: draft docs/research/reduced-route-plan.md, open for Peter (adopt now or on a trigger
  fire; which of R1–R3 leads).

**2026-11-16: §23 merged** (DECISIONS 2026-11-16 "After §23"):
- energy closes with BCT off (0.25 %); BCT on put energy in (B 1.135 / 20.4);
- BCT-off survival probe passes (trigger clause 3 not fired);
- VCI fails its committed momentum gate (drift 2.4× from R/32 to R/64); F2 chosen and frozen (S 0.369 vs lattice
  0.381, flat columns only);
- skin on T-S1 R/64: p_n +3.6 / +3.1 %, **Y − 1 13 % low** (33–37 % at R/32): the likeliest trigger failure;
- quad T-B2 reference missed U_ref ≤ 1.75 % (12 of 16). **Peter: accepted as is**, threshold 3.5 % + measured
  U_ref (post hoc); a momentum-restoring VCI is built (task 2026-11-16-a).

**Later on 2026-11-15:** WSL B b10 and b11 merged (5f7bf7d, 9d954b1; leak scans clean).
- **b11:** the TLSPH face-layer deficit is the integration-constraint failure of nodally integrated Galerkin
  meshfree methods (Hillman 2013; Chen et al. 2001): **rediscovery**. VCI is the known remedy (reference-frame
  correction; load through a surface quadrature; loses exact momentum).
- **D3 reopened (Peter, DECISIONS "D3 reopened after the boundary-integration reading"):** a VCI design note first,
  then one construction (fitted flat face or VCI) chosen by a committed criterion on non-trigger cases. The D4 host is
  "the one construction chosen and frozen in advance". If VCI is chosen, the skin carries the contact load, which
  needs Peter's approval at the trigger-run freeze.
- **b10 (track A):** B06 has two v_cr conditions (native Al oxide 4.5 nm; ZnO coating 20 nm), not a thickness
  series of one oxide type; B07 and B16 have no v_cr; B03 row same as published. Peter: merge only for now; the B06
  pre-registration and the T3 decision come later.

**Route review 2026-11-15 held** (DECISIONS 2026-11-15 "Route review 2026-11-15"; folder
docs/research/route-review-2026-11-15/: brief, inputs, reviewer packet, state-report copy, and reviewer-1.md and
reviewer-2.md verbatim). Peter's decisions:
- **D1:** the bond stays in the solver. Reason: the claim needs the bond's effect on rebound and v_cr. Both
  reviewers and the modeller had recommended one-way first.
- **D2:** p_n and Y are judged on a measurement-only skin, as 0.5 µm surface-disc averages. Depth-band stresses are
  reported only. 2D axisymmetric runs are for references only (SPH is 3D only). This amends 2026-11-14 item 4.
- **D3:** one bounded TLSPH attempt (BCT off, skin, a fitted flat face frozen in advance; amended later the same
  day: fitted face or VCI, see above), plus a BCT-off survival probe. Fallback: the reduced route (a build-up rule or the closed form, on track A).
- **D4, dead-end trigger** (full wording in the DECISIONS entry). It fires if any of these holds:
  - a p_n or Y − 1 surface average on T-B2 misses the quad reference by more than 3.5 % + U_ref at R/64;
  - such an average does not converge from R/32 to R/64;
  - the BCT-off survival probe fails.

  U_ref is the quad change from R/128 to R/256 and must be ≤ 1.75 % first. If the trigger fires, the project moves
  to the reduced route.
- **D5:** the order of work, as set out in WSL A task 2026-11-15-b and WSL B task b11.
- **D6:** two independent reviewers.

**Choices the modeller made in the tasks** (Peter may change them):
- the survival probe uses the §19.5 survival checks, with the energy balance reported but not judged;
- the fitted flat face and the skin are calibrated only on cases other than the T-B2 trigger deck (column, flat
  free surface, T-S1).

**The trigger run itself** (T-B2 with skin and fitted face at R/32 and R/64) is not yet a task. The modeller drafts
it from §23, with frozen binary, decks and predictions, and Peter approves the freeze.

**Earlier on 2026-11-14 and 2026-11-15** (details in DECISIONS and STATUS):
- CS-18b refuted at T-S1;
- §21: no BCT variant is clean;
- §22: the BCT-off rule was not met (4 of 20 / 6 of 20 averages within 3.5 %), which triggered the review.

## 1. The two tracks

**A. Single-impact data track** (unchanged since 2026-11-08):
- Step 1 for B06, B07 and B16 is merged (5f7bf7d). B06 measures v_cr in two conditions (native Al oxide; ZnO
  coating) and is not a thickness series, so it does not supply T3. B07 and B16 have no v_cr. Open for Peter: the
  B06 pre-registration and whether to send or drop the T3 measurement request.
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
| BCT analysis and variant | diagonal scaling fails on small or changing patches (rim loads 2–3×); no variant clean; T-S1 peak reference 1.062 | §21, DECISIONS 2026-11-15 |
| BCT off at the 0.5 µm scale | rule not met (4 of 20 / 6 of 20 within 3.5 %); face-layer deficit with any point-loaded face | §22, DECISIONS 2026-11-15 |
| **Route review** | bond in the solver kept; skin-based p_n and Y; one bounded TLSPH attempt; dead-end trigger fixed | DECISIONS 2026-11-15 "Route review 2026-11-15" |

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
  - Outstanding, in the background, not blocking: Ge 2026 (browser download by Peter) and Dai 2025,
    doi:10.1007/s00466-025-02714-1 (closed). Tang 2021 moved to task b11.
- **Boundary integration and patch tests** (WSL B b11, merged 9d954b1): data/boundary_integration_reading.md. The
  face-layer deficit is the Galerkin nodal-integration constraint failure (rediscovery); VCI is the known remedy;
  Tang 2021 verifies no Y or p_n.
  - **Lesson:** a literature step must sweep for competing methods.
- **Reviews:** sph-route-review-2026-11.md, with its critique, the meta-review supplied by Peter, and
  sph-route-expert-answers-check.md; route review 2026-11-15 with two independent reviewers
  (docs/research/route-review-2026-11-15/).

## 4. Hunch budget

**3 of 5:** CS-10, CS-12, CS-17 (CS-18b refuted at T-S1, 2026-11-14).

## 5. Open for Peter

1. Track B is settled by the route review until the trigger run: nothing open for Peter until §23 arrives (the
   trigger-run task is drafted from §23 and frozen with Peter). If U_ref > 1.75 %, Peter decides how the reference
   is improved.
2. The E-1 gate draft (docs/research/sph-contact-e1-gate-draft.md): revise to skin-based p_n and Y as 0.5 µm
   surface-disc averages (D2), then thresholds and freeze. It applies only if a host passes its ladder.
3. Compute for E-1 at R/48 and finer (raised in chat; not recorded elsewhere at Peter's wish).
4. Track A items from 2026-11-08: judge v2, the CS-17 domain, the T3 extra items, Tiamiyu 2022, the Tang 2025 SI.

## 6. Sessions and branches

| Session | Where | Open task |
|---|---|---|
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | — |
| WSL A | fork `sph-hvi-contact` branch `tlsph`; results to `coldspray/opencourant-sph` | 2026-11-16-a (§24) and 2026-11-16-b (§25) |
| WSL B | `coldspray/bonding-methods-reading` | b9 (remaining: Ge 2026, Dai 2025); b10 and b11 merged |

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
| Solver log, all sections §1–§23 (§24 next) | docs/research/opencourant-verification.md; rows in docs/research/opencourant/results/ |
| Ladders (frozen) | sph-contact-ladder.md, sph-tlsph-ladder.md, sph-tlsph-b-ladder.md |
| Hunches | coldspray-hunches.md (index), coldspray-hunch-cs18.md, coldspray-hunch-cs18b.md, and the earlier CS files |
| Referee | sph-contact-referee-2026-11-11.md |
| Plan of the fork | sph-hvi-contact-plan.md (milestone 1) |
| Tasks | docs/research/tasks/wsl-a.md, wsl-b.md |
| Route review 2026-11-15 | docs/research/route-review-2026-11-15/ |
