# Handoff — 2026-11-04 (cold-spray track; replaces the 2026-11-03 version, which is in git history)

**Start the next session with:** "Read docs/HANDOFF.md and continue the cold-spray track." Then read
docs/STATUS.md (top entries) and the DECISIONS index (top of docs/DECISIONS.md). Branch:
`claude/exciting-fermi-qy077p`.

**Arena 2 is paused** at Phase 6 step 5; resuming means step 6 (blind audit, Target D, tag contact-v1.0). Arena 1
is released as benchmark-v1.0.

## 1. Where the cold-spray track stands

Update 2026-11-04 (2nd cloud session): step 3 below done (CS-10).

Peter's application: multi-particle cold spray with coating build-up; deposition efficiency and bonding; a
mechanistic model that states its own range of validity.

- **Verdict of the research brief: "go: discipline only"** (DECISIONS 2026-11-03). No arena and no search yet. Use
  the schemeforge process (pre-registered hunches with kill criteria, held-out data, ledger, referee labels) to
  develop models. Notes:
  - questions: docs/research/coldspray-questions.md;
  - data and zoo: docs/research/coldspray-data-and-zoo.md;
  - plan: docs/research/coldspray-go-nogo.md (assumption inventory H1–H7, local-first order, upgrade trigger).
- **Local first** (DECISIONS 2026-11-03). An external blind campaign is the last resort; its draft is parked
  (docs/research/coldspray-campaign-proposal.md).
- **Data** (docs/research/data/, README there):
  - `vcr_lipit.csv`: 49 single-impact critical-velocity rows, 11 matched materials, source and extraction mode
    per row, oxide state for 20 rows, conflicting secondary quotes flagged (Q rows);
  - `properties.csv`: Hassani 2020 Table S1 first, then the HG2018a preprint table (incl. γ₀, Johnson–Cook),
    then handbook rows;
  - `vcr_process_oxide_cu.csv`: Cu process v_cr against oxide thickness (HG2019b Table 1).
- **Retrospective test v1** (docs/research/coldspray-results-v1.md; rules: coldspray-preregistration.md;
  commits abce3f6 → 045409d → 2324a43):
  - CS-02 (sound speed alone cannot rank Al alloys): supported;
  - CS-03 (sound-speed law beats a property-free baseline): supported;
  - CS-01 and CS-05: inconclusive;
  - CS-06 (process FE values below single-impact windows): refuted;
  - judge-noise check: the data separate the sound-speed law from a constant on 8 of 9 held-out rows.
- **First literature-blind result, B10** (Na et al. 2025, Al 6061 in five heat treatments;
  docs/research/coldspray-results-b10.md; freeze 060fff8 → outcomes 94fd173 → scorer f770a8b → scores b31cdae):
  - CS-08 (strength raises v_cr within one alloy): **refuted**;
  - CS-07 (oxide): not refuted, support undetermined;
  - CS-09: undetermined (no window bounds printed; rule B6 now covers this for future papers);
  - the sound-speed law under-predicts this powder by 8–16 %.
- **Strength-dependent zoo members** (Assadi, Schmidt, spall law) still lack tensile strength and failure strain
  for the impact-tested powders. B10 used the paper's static compression strength (Peter's rule BP1).

## 2. Rules that must not be broken

- **Blind test** (docs/research/coldspray-blind-literature.md, rules B1–B6):
  - the modelling session never opens a hold-out paper or its outcomes before its predictions are committed;
  - inputs are extracted by a separate session (prompt: coldspray-extraction-prompt.md), and its CSV is
    leak-scanned (velocity units, rebound, critical, comparatives) before anyone reads it;
  - outcomes are extracted after the freeze (prompt: coldspray-extraction-prompt-step3.md);
  - the scoring script is committed before outcomes are read;
  - a post-hoc number is labelled post hoc;
  - verdicts follow the frozen rules even when that leaves them undetermined.
- **Pre-registration:** predictions and rules committed before scoring; git order is the proof. Frozen files
  (`predictions_v1.csv`, `predictions_b10.csv`, the preregistration docs) are never edited after scoring.
- **Simulation** (DECISIONS 2026-11-03/04): no simulated v_cr is used before the verification ladder and a mesh- or
  particle-convergence check pass; no erosion or element deletion as a production method.
- **Iron rules of CLAUDE.md:**
  - never call a result novel (labels: rediscovery / variant of X / plausibly new, the last by the referee only);
  - record negative results;
  - no invented values: unsourced inputs stay blank or are flagged.
- **Licence:** OpenCourant's hm_reader, H3D and hm_cfg_files are Siemens-licensed. Local research use only; do not
  commit binaries or QA decks (CC BY-NC).

## 3. Sessions and branches

| Session | Role | Branch it pushes | Must not |
|---|---|---|---|
| Cloud (this one, modeller) | models, predictions, scoring, notes | `claude/exciting-fermi-qy077p` | read blind papers or outcomes before a freeze |
| WSL A | OpenCourant: verification, simulations | `coldspray/opencourant-sph` (current), earlier `coldspray/opencourant-verification` | open blind papers |
| WSL B | blind extraction (inputs; outcomes after freeze) | `coldspray/blind-inputs`, `coldspray/b10-outcomes` | edit anything but its CSV |

All earlier branches are merged into `claude/exciting-fermi-qy077p` (last: a5fd07e).

## 4. Simulation status

- **JAX code** (src/schemeforge/research/impact_axisym.py, tests/test_impact_axisym.py), 2D axisymmetric, elastic
  only:
  - rung 0 (confined plate) passes against the exact 1D solution (ccec9db);
  - rung 1 (Hertz sphere) agrees with OpenCourant `Isolid = 17` to about 1 %. Both sit 4–5 % short of Hertz at
    20 m/s and approach it at lower speed (a dynamic effect).
- **OpenCourant latest-20261011** (fork of the withdrawn OpenRadioss; DECISIONS 2026-11-03), installed in WSL at
  ~/opt/opencourant/latest-20261011. docs/research/openradioss-setup.md and opencourant-verification.md cover it:
  - **2D axisymmetric must use `Isolid = 17`**; the default element is area-weighted and fails Hertz. §6 there
    lists the deck rules;
  - Johnson–Cook + Mie–Grüneisen runs on 2D quads;
  - temperature is computed but not written out with `Isolid = 17` (open item);
  - **2D Lagrangian fails at the jet root**, earlier with refinement (also with γ₀ = 2.17);
  - SPH is 3D-only; there is no 2D remeshing.
- **Decision 2026-11-04:** everything after jetting onset goes to **3D SPH in OpenCourant** (quarter symmetry), no
  fork. 2D ALE comes last. A 2D-axisymmetric cross-check, if needed, is built in the JAX code later.
- **WSL A's current task** (message given 2026-11-04):
  - 3D SPH ladder: confined column (measure cost first), two-wave, Hertz against JAX and `Isolid = 17`, quarter
    against half model, particle-spacing convergence;
  - then an Al–Al jet-onset diagnostic, with no v_cr claimed;
  - results go into opencourant-verification.md §9.

## 5. Next steps (in order)

1. **SPH ladder merged** (f156b94; S0, S0p pass, S1 not clean, SPH parts kernel-welded). Route A + B decided
   (DECISIONS 2026-11-04). Next: Peter approves CS-11 (docs/research/coldspray-hunch-cs11.md, draft) and decides S1;
   then WSL A runs rungs F0 and W0, then the CS-11 sweep. No Al–Al run before the CS-11 freeze commit.
2. **Blind set:** 10 papers still pending (B02–B07, B12–B14, B16; Peter is fetching them).
   - For each paper whose inputs arrive: leak-scan, merge, register any new hunch, freeze predictions (commit),
     then outcomes via the step-3 prompt, then score.
   - B09 is process-level (splat tests), not single-impact; B01, B08, B11, B15 contain no v_cr.
3. **Model development:** CS-10 (combined strength + oxide energy balance) is registered (3f181ed) and fitted on B10
   (2ce15c6; beta 0.3774, gamma 3.19e11 Pa, frozen): docs/research/coldspray-hunch-cs10.md and coldspray-cs10-fit.md.
   B10 cannot determine it (leave-one-out no better than a constant; beta fragile). Add CS-10 to every blind freeze
   from now on, with its input rule (static compression strength, else Tabor HV/3; numeric oxide thickness, else no
   prediction). The referee must still compare it with Na2025 Eq. 6 (not read in the modelling session).
4. **Data gaps:**
   - the primary HG2018b (*Scripta Mater.* 145, 9) for Al, Ni, Cu, Zn (conflicting quotes);
   - tensile strength and failure strain of the tested powders;
   - c_p for the handbook rows (atomic weights: no fill from memory).
5. **Simulation type 2** (a pre-registered setup as a zoo member) only after the 3D SPH ladder and convergence pass.

## 6. Key files

| What | Where |
|---|---|
| Decisions (index at top, regenerate with `python scripts/decisions_index.py`) | docs/DECISIONS.md |
| Plan and assumption inventory | docs/research/coldspray-go-nogo.md |
| Data tables and their README | docs/research/data/ |
| Zoo code, scorers (not judges) | src/schemeforge/research/coldspray*.py |
| Hunches | docs/research/coldspray-hunches.md, coldspray-preregistration*.md |
| Blind set and prompts | docs/research/coldspray-blind-literature.md, coldspray-extraction-prompt*.md |
| Solver verification | docs/research/opencourant-verification.md, openradioss-setup.md |
