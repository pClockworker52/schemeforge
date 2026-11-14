# Handoff — 2026-11-14, session end before /clear (cold-spray track; earlier versions in git history)

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." Then read the top of
docs/STATUS.md and the DECISIONS index. Branch: `claude/exciting-fermi-qy077p`. Procedure:
docs/research/coldspray-procedure.md (who writes where; tasks for the other sessions in docs/research/tasks/).

**Done 2026-11-14 (after /clear):**
- §20 merged (7984e1c): **CS-18b refuted at T-S1** by its frozen kill rule (R/32 rebound 0.860). Hunch count 3 of 5.
- §20.4–20.5 merged (c329481): T-S1 R/64 with BCT passes its own criteria; **T-S1 R/32 with BCT off: rebound
  0.9988**. Cause: BCT on curved, few-particle wall patches.
- Peter: stay with TL; **CS-18c** with a corrected BCT; UL SPH (CS-19) is the fallback; no route review; rigour
  without ceremony (DECISIONS 2026-11-14).

**Next:** when WSL A pushes §21 (task 2026-11-14-c), merge it (check that the diff touches only the verification log
and results), then draft CS-18c and its ladder from the CS-18b ladder: the BCT variant, T-S1 marked non-blind, the
checked T-S1 peak reference. Then a fresh general-purpose agent checks the draft (distinct from CS-18b? any
threshold set on a rung?). Then Peter freezes it. If no BCT variant passes, draft CS-19 (UL SPH) instead.

## 1. The two tracks

**A. Single-impact data track** (unchanged since 2026-11-08):
- The blind papers B06, B07 and B16 are with Alex. The T3 measurement request (v_cr against oxide thickness at a
  fixed oxide type) waits on B06.
- B03 and B12 are merged as exposed (d67f72c).
- Open data hunches: **CS-10, CS-12, CS-17.** Details: docs/research/coldspray-hunches.md.

**B. SPH host track:** a solver host for an interface (bonding) law. Peter's requirements (DECISIONS 2026-11-12,
amended 2026-11-14):
- particle shape, rebound and v_cr, and the interface state;
- 3D, with the bond acting in the solver;
- interface outputs judged as **averages over 0.5 µm**, point values at the edge reported only.

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

1. CS-18c freeze, after §21 (the earlier options, UL / another host / reduced route, are fallbacks). The candidates named earlier:
   - an updated-Lagrangian variant (Dai type) with our surface fixes, as its own hunch;
   - another host;
   - a reduced route (a particle-level build-up rule, or the closed form).
2. The E-1 gate draft (docs/research/sph-contact-e1-gate-draft.md): revise to 0.5 µm averages, then thresholds and
   freeze. It applies only if a host passes its ladder.
3. Compute for E-1 at R/48 and finer (raised in chat; not recorded elsewhere at Peter's wish).
4. Track A items from 2026-11-08: judge v2, the CS-17 domain, the T3 extra items, Tiamiyu 2022, the Tang 2025 SI.

## 6. Sessions and branches

| Session | Where | Open task |
|---|---|---|
| Cloud (modeller) | schemeforge, `claude/exciting-fermi-qy077p` | — |
| WSL A | fork `sph-hvi-contact` branch `tlsph`; results to `coldspray/opencourant-sph` | 2026-11-14-c (BCT variant; §21) |
| WSL B | `coldspray/bonding-methods-reading` | b9 (remaining papers) |

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
