# Handoff — 2026-11-20: CS-22b frozen, waits on WSL A task 2026-11-20-a (cold-spray track; earlier versions in git history)

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." Then read the top of
docs/STATUS.md and the DECISIONS index. Branch: `claude/exciting-fermi-qy077p`. Procedure:
docs/research/coldspray-procedure.md (who writes where; tasks for the other sessions in docs/research/tasks/).

**First action (updated 2026-11-21, later): §32 merged (softening check stopped; quad temperature not written). WSL A does task 2026-11-21-a (quad temperature output, then the spec's verdict as §33), then resumes CS-22b (2026-11-20-a) on engine 27e53d5f0. Merge and judge §33 against softening-check-2026-11-20.md when pushed.** Then: check WSL A task 2026-11-20-a. Fetch `coldspray/opencourant-sph`. If pushed: merge with a merge
commit (diff only §31 and `results/tl_cs22b_*.csv`), recompute dR per δ_c from the rows with the §30 off runs, judge
against coldspray-hunch-cs22b.md (frozen 2026-11-20), and record in coldspray-hunches.md, DECISIONS and STATUS with
the author's predictions. If not pushed: the open items for Peter are R1–R3 and CS-20 parking.

**Session 2026-11-19/20 (cloud):** CS-22 scope note (5b3114a; the refutation covers the registered setting only).
CS-22b drafted (faac6d9) and **frozen 2026-11-20** (Peter: "Let's freeze"; DECISIONS 2026-11-20): δ_c ladder
3×/10×/30× (0.09375, 0.3125, 0.9375 µm), §30 off runs reused, lost-bond check, R/8–R/16 gate on |dR16| ≥ 0.01, at
most 3 R/32 runs. Track B stays open until CS-22b is judged. Hunch count 4 of 5.

**Session 2026-11-19 (cloud):** merged §30 (adf2319; WSL A task 2026-11-18-b, now closed). **CS-22 part 1 refuted**
(DECISIONS 2026-11-19):
- as frozen, by kill (a), on output artefacts only (header date, an uninitialised padding byte, round-off sums,
  `slip`); the motion and the interface fields are identical;
- under Peter's post-hoc A2 (comparison set amended) and R/32 retry, by kill (b): dR −1.0·10⁻⁴ / +4.8·10⁻⁵ /
  +7.1·10⁻⁴ at R/8/16/32, no signal and not converged. Every bond breaks on rebound (δ_c 31.25 nm, σ_B = σ_flow);
- e(off), reported only: 0.094 / 0.065 / 0.057.
Hunch count 3 of 5 (CS-10, CS-17, CS-20). WSL A has no open task.


**Session 2026-11-18 (cloud, later), in order:**
1. **Brainstorm** from multi-particle-spec.md alone, filtered against multi-particle-tried.md
   (multi-particle-brainstorm-2026-11-18.md, afd8f52 and later). 30 raw ideas; 8 kept; #9, the forked bond response
   (a synthesis of #2 paired runs and #5 rollback), added afterwards.
2. **CS-20** (subsonic-edge ring radius, zero-code; no unseen data source) and **CS-21** (paired differences on the
   §25 quad deck) registered (29a38e3).
3. **Peter: CS-12 retired; Track B reopened for the forked bond-response route only.** Local interface-state drivers
   stay closed, and the trigger run and VCIMR's D2 change stay dropped. **CS-22 frozen** (e0cf087), simplified to:
   - Al–Al at 600 m/s on TLSPH with cs12;
   - a fork at t_b = 0.5 t_p, after which every contacting pair bonds;
   - R/8, R/16, R/32 and 7 runs; R/64 is out of reach (about 100 GB estimated).
   The "obtainable data" part of rule 1 is waived for part 2 (the bistable band). The mesh study stays: Peter asked
   whether it could be skipped, and it is the decisive test.
4. **§28–§29 merged (a488f57):**
   - **CS-21 part 1 refuted.** No paired difference is usable (0–0.33 of points against 0.80), so pairing does not
     cancel the edge error on 2D quads.
   - **CS-22 not run.** cs12 refuses Y′ < 0, so the frozen bond setting could not be reached; this was a modeller's
     drafting error. Peter chose an **amendment before any run (A1, 8e6d95e)**:
     - Y′ < 0 allowed, with Y′ = −10⁶;
     - off-skin contacting particles bond;
     - p_E = 0 kept;
     - a `bond.t_on` key with default 0.
     The rule is unchanged. WSL A task 2026-11-18-b.
5. **Switch-radius check: PASS** (switch-check-2026-11-18.md; spec 7465e0f, result b6f23cc; zero-code on the §25
   a(t) rows). The switch radius a_c from a fitted a(t) = A t′^p converges: last step 2.35 % at 600 m/s and 2.88 % at
   500 m/s. Margins are thin, p alone drifts 6.5 % at 600 m/s, a_c is extrapolated, and the host is 2D quads.
   a_c/a_c,rigid ≈ 1.14. This makes the **contact map** (run 1's converged a(t) decides where run 2 bonds, leaving the
   centre out) a candidate trigger for CS-22 part 2, but only if part 1 passes and only on a host that resolves
   a_c ≈ 1.1–1.3 µm. Nothing is registered.
6. **Discussed in chat, not recorded at Peter's wish:** the wall-function (Fluent) analogy, and why it fails here.
   The first layer is the badly represented one (§22), no outer input converges (§27), there is no overlap layer at
   a separating edge, and there is no calibration data.

**2026-11-18: B06 scored** (coldspray-results-b06.md): v_cr 746 (native Al oxide) / 778 m/s (20 nm ZnO); Z6 S1 0.059 /
0.015 and the baseline 0.16 / 0.19, all out of domain; CS-07 supported by 1.5 m/s with the oxide-type confound;
CS-12 T1 not refuted (bonded middle annulus, unbonded centre; exposed); T3 untested (request dropped 2026-11-17).

**2026-11-17: Track B's interface-state route is closed** (DECISIONS "Track B interface-state route closed; reduced
route adopted"), as unverifiable with the references available to this project:
- §27: no outer or non-local driver is usable by the rule fixed in advance (driver-check-2026-11-17.md); only a(t)
  converges;
- §25: Y − 1 converges nowhere, even on 2D quads;
- §26: skin Y peaks at the pole.

The trigger run and VCIMR's D2 change are dropped. Kept: the verified elastic bulk results, `cs12` and VCIMR in the
fork, and the He/H₂ animation (illustration). WSL A has no open task.

**2026-11-17: §26 merged (9b03f79).**
- `cs12` is built on TLSPH and is neutral; D-3/D-4 pass.
- The Ti-6Al-4V survival check at 1584 m/s passes (material data second-hand).
- **Skin Y peaks at the pole**, so skin-Y activation bonds the centre first. With skin-Y activation no choice of
  thresholds gives a bonded ring.
- The illustration (fork `hvi/illustration/v2/`) uses Y′ 0.2 and δ_c 1 s, tuned for the picture. Its ring comes from
  central debonding on spring-back.

**2026-11-17, Peter:** **Track B continues** with `cs12` (Bay activation) on TLSPH; the skin feeds bond activation
(activation only); f_B is a running maximum, σ_B(t) = f_B·σ_flow(T). Illustration runs (`kind = illustration`) for
the homepage are outside the rules. Ti-6Al-4V, 20 µm, several particles per side, He/N₂ 1347 m/s against H₂/N₂
1584 m/s (Peter's nozzle model). Risk: TLSPH has survived only Al–Al at 800 m/s; the fallback for the animation is
Peter's existing OpenRadioss set-up.

**Draft caption for the new animation (for Peter):** "3D-SPH-Simulation (OpenRadioss-Fork, Total-Lagrange-SPH)
mehrerer Ti-6Al-4V-Partikel mit 20 µm Durchmesser auf Ti-6Al-4V, Schnitt durch die Mitte, links mit He/N₂
(1347 m/s), rechts mit H₂/N₂ (1584 m/s). Die Farbe zeigt die plastische Dehnung; markiert ist, wo die Oxidschicht
aufreißt. Die Aufprallgeschwindigkeiten stammen aus dem 1D-Düsenmodell bei gleichen Stagnationsbedingungen. Die
Bindung wird im Löser aktiviert, wo Oberflächendehnung und Kontaktdruck Schwellwerte überschreiten (Bay-Kriterium);
beim Zurückfedern löst sie sich in der Mitte. Schwellwerte und Bindungsgesetz sind für die Darstellung gewählt.
Illustration, nicht verifiziert und experimentell nicht validiert."

**2026-11-17: §24 and §25 merged (5ab274d; calibration, no verdicts).**
- **§25, the P3 probe on 2D quads.** Al–Al at 600 and 500 m/s, R/64–R/256. The finest mesh stops at about
  0.035 t_p (0.8 ns) on a collapsing block cell near the contact edge. Within that window:
  - p_n converges by the rule at 0.25 a and 0.5 a, but not at 0.75 a;
  - **Y − 1 converges at no disc**, and it rises steadily with refinement.

  Three readings, none ruled out:
  1. a reference-deck limit (collapse, contact tolerance);
  2. an ill-posed local quantity, because the model has no length scale;
  3. a start-up window.

  A remeshing or ALE reference host would test reading 1; a regularising length would test reading 2.
- **§24, the interface file and VCIMR.**
  - The interface file (v5) is complete. §23's open item (3) was partly wrong: only rigid-wall contact was missing.
  - VCIMR passes the VCI-DESIGN §8 gate within the time box: S = 0.132 against F2's 0.369. Sphere layer 2 is at
    0.90–0.95, against 0.63–0.65 for F2.
  - Its costs: skin p_n on the axis is +6.6 % at R/64 (F2: +3.6 %); |B − 1| = 0.026 at R/16 (outside the gate);
    the drift reading is unconfirmed (fork SPEC-TL-b §9.1).
  - It is recorded as the candidate (fork 310b21cb7); F2 stays frozen.
  - The trigger run (16-a item 4) is not run; it waits for the D2 decision.
  - A WSL VM ran out of memory during parallel R/64 runs; everything was rerun serially, and no result comes from a
    killed run.

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
  coating) and is not a thickness series, so it does not supply T3. B07 and B16 have no v_cr. B06 is frozen
  (c484494), step 3 is WSL B b12; the T3 measurement request was dropped (2026-11-17).
- B03 and B12 are merged as exposed (d67f72c).
- Open data hunches: **CS-10, CS-17, CS-20** (CS-12 retired 2026-11-18). Details: docs/research/coldspray-hunches.md.

**B. SPH host track:** a solver host for an interface (bonding) law. Peter's requirements (DECISIONS 2026-11-12,
amended 2026-11-14):
- particle shape, rebound and v_cr, and the interface state;
- 3D, with the bond acting in the solver;
- interface outputs judged as **averages over 0.5 µm**, point values at the edge reported only;
- since the route review 2026-11-15: p_n and Y measured on a measurement-only surface skin (0.5 µm surface discs),
  depth-band stresses reported only; a dead-end trigger is in force (DECISIONS 2026-11-15).

**Route state:**
- The interface-state route was closed on 2026-11-17 (no local driver converges).
- It was **reopened on 2026-11-18 for the forked bond-response route only** (CS-22; DECISIONS "Track B reopened for
  the forked bond response").

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

**4 of 5:** CS-10, CS-17, CS-20, CS-22b.
- Retired: CS-12 (2026-11-18).
- Refuted: CS-22 part 1 (§30, 2026-11-19), CS-21 part 1 (§28, 2026-11-18) and CS-18b (T-S1, 2026-11-14).

## 5. Open for Peter

0. **New (2026-11-18), in order:**
   1. CS-22b frozen 2026-11-20 (resolved). After its verdict: if it fails, does Track B close again?
   2. Which of R1–R3 leads (reduced-route-plan.md), still open.
   2b. Physical length scale (length-scale-note-2026-11-20.md; Ge 2026 read, its ℓ is calibrated): pursue after
       CS-22b? First steps would be reading Chakrabarty & Song 2020 and Tang et al. 2024 (blind screen first) and
       finding a measured grain size or gradient length for an Al powder; a hunch only after that (budget 4 of 5).
   3. CS-20 has no unseen ring-map source, so it is a candidate for parking (its author gave 0.3 odds that a source
      appears within three months).

Older items (state of 2026-11-15; items 1–3 lapsed with the 2026-11-17 closure, kept for the record):

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
| WSL A | fork `sph-hvi-contact` branch `cs12`; results to `coldspray/opencourant-sph` | **2026-11-21-a** (quad temperature output + softening check, now), then **2026-11-20-a** (CS-22b, resume); 2026-11-20-b closed (§32 merged); 2026-11-18-b closed (§30) |
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
| Solver log, all sections §1–§30, §32 (§31 reserved for CS-22b, §33 next) | docs/research/opencourant-verification.md; rows in docs/research/opencourant/results/ |
| Multi-particle brainstorm | docs/research/multi-particle-spec.md, multi-particle-tried.md, multi-particle-brainstorm-2026-11-18.md |
| Driver and switch checks | docs/research/driver-check-2026-11-17.md; switch-check-2026-11-18.md (script scripts/switch_check.py) |
| Today's hunches | coldspray-hunch-cs20.md, coldspray-hunch-cs21.md (refuted), coldspray-hunch-cs22.md (frozen with A1) |
| Ladders (frozen) | sph-contact-ladder.md, sph-tlsph-ladder.md, sph-tlsph-b-ladder.md |
| Hunches | coldspray-hunches.md (index), coldspray-hunch-cs18.md, coldspray-hunch-cs18b.md, and the earlier CS files |
| Referee | sph-contact-referee-2026-11-11.md |
| Plan of the fork | sph-hvi-contact-plan.md (milestone 1) |
| Tasks | docs/research/tasks/wsl-a.md, wsl-b.md |
| Route review 2026-11-15 | docs/research/route-review-2026-11-15/ |
