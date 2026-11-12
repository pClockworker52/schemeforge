# Tasks for WSL A (OpenCourant simulations)

Procedure: [../coldspray-procedure.md](../coldspray-procedure.md). Pull `claude/exciting-fermi-qy077p`, do the
newest open task, push results to `coldspray/opencourant-sph`. Write only your own section of
opencourant-verification.md and your own scripts and results. Do not edit STATUS, HANDOFF, DECISIONS, the hunch
files or this file. Blind-list papers stay closed.

## Task 2026-11-12-b: freeze preconditions for the TLSPH ladder (open; no code, no runs)

**Basis:** DECISIONS 2026-11-12 "TLSPH set-up from SPEC-TL adopted"; ladder draft
[../sph-tlsph-ladder.md](../sph-tlsph-ladder.md), "Freeze preconditions".

1. **Journal check of SPEC-TL's equations:** eqs. 15 (correction matrix), 17 (F), 24 (force) and 32 (hourglass) of
   Ganzenmüller, CMAME 286 (2015) 87–106.
   - Compare the journal version with the preprint arXiv:1410.7221 that SPEC-TL used. If the journal version is
     paywalled, ask Peter for the PDF.
   - Compare with one independent source, for example Bonet & Lok 1999 or Vidal, Bonet & Huerta 2007 for the
     correction and force, or another TLSPH paper for the hourglass term.
   - Record every difference in SPEC-TL, with page references.
2. **`tl.cond_max`:** compute the condition numbers of the reference correction matrices at t = 0 with a script,
   with no engine run. Cover:
   - the bulk cubic net;
   - free faces, edges and corners;
   - symmetry-plane neighbourhoods with images;
   - the surface-conforming sphere at R/16, R/32 and R/64 (including the merged particles).

   Propose a limit with its reason (for example 10× the largest value found in these sets-ups), and write it into
   SPEC-TL §5.3.
3. **Push** the fork branch `tlsph`, and stop. No solver code until the freeze commit in schemeforge exists.

## Task 2026-11-12-a: TLSPH in the fork, preparation only (closed: done; reading note merged bc3376b, SPEC-TL at fork tlsph 1ae689c)

**Basis:**
- DECISIONS 2026-11-12: TLSPH directly in the solver, 3D, bond in the solver.
- Hunch draft [../coldspray-hunch-cs18.md](../coldspray-hunch-cs18.md) and ladder draft
  [../sph-tlsph-ladder.md](../sph-tlsph-ladder.md).
- Literature: [../tlsph-literature-check.md](../tlsph-literature-check.md).

**Allowed now (no runs):**
1. **Read Profizi, Combescure & Ogawa 2016** (C. R. Mécanique 344, 211–224, doi:10.1016/j.crme.2016.02.001) and
   **Profizi's PhD thesis** (INSA Lyon 2016), at F level. Fetch them yourself under the standing fetch rule (the
   journal page and the lamcos.insa-lyon.fr thesis PDF are open; the cloud session cannot reach those hosts).
   Write `docs/research/data/profizi2016_reading.md` covering:
   - the SPH formulation (kernel, correction, stabilisation, viscosity);
   - the reference update, if any, and its trigger;
   - the body-to-body contact;
   - the adhesion law;
   - the verification shown, with numbers;
   - resolution and cost;
   - the stated limits.

   These papers are not on the blind list.
2. **In the fork, on a new branch `tlsph` from `main`,** write two documents:
   - `hvi/SPEC-TL.md`: a design proposing the set-up section of the ladder (kernel, h, correction, hourglass α,
     viscosity, reference-update rule) with reasons. It also covers where the hvi contact and bond laws attach.
   - A **CODEMAP addendum:** where a new SPH formulation plugs into the engine, whether the SPH arrays can hold
     reference neighbours, reference gradients and F, how symmetry planes would work with fixed reference
     neighbourhoods, and how SPMD/OpenMP split the loops.

   Commit both. **No solver code and no runs** until CS-18 and the TLSPH ladder are frozen in schemeforge.
3. **Push** the reading note to schemeforge on a branch `coldspray/profizi2016-reading`, and the fork branch
   `tlsph`. Then stop.

## Task 2026-11-11-b: ladder reruns under set-up S′ (closed: stopped at step 1, §15; Peter 2026-11-12)

**Basis:** [../sph-contact-ladder.md](../sph-contact-ladder.md), **Addendum 1** (frozen in 140b84a, post hoc; adopted by
Peter 2026-11-11). Cite 36c34bd + 140b84a in every row.
- **S′** = the §9.1 settings plus ξ = 0.3 and kernel-correction order 1 on **all** particles. It is one set-up for
  every rung below.
- **stfac 3** for all S′ rungs (Peter's choice for E-1; one value throughout). B-3 must pass for it.
- The FAILs under the frozen set-up stand (§14.2); S′ is a second, labelled track.

**Rules:**
- Commit the source and decks before each campaign.
- Commit each recorded prediction in its own commit before its runs.
- Every run gets a row with `binary_state = committed`.
- A failing **required** rung means stop, record it and report to Peter, with no tuning. Optional items do not stop
  the task.

**Order:**
1. **Host rungs at S′:** S0, S1 and F0 of opencourant-verification.md, on the fork binary without a sidecar. Same
   references and thresholds as in §9.4, §9.6 and §10.2. If one fails, stop: S′ is then not a valid host set-up.
2. **A-0 at S′:**
   - build the base `d791761` unmodified;
   - run S0, S0p, S1 and the two-part column at S′ on it and on the fork without a sidecar;
   - the two must be bit-identical.
3. **A-2, B-1, B-2** (R/16 and R/32), **B-3** (R/32, start at s against 2.4 s, within 1 %).
4. **B-2 convergence:** B-2 at R/48 (R/64 if R/48 is affordable and inconclusive). It must be in the same direction
   and within the same limits as at R/32. Report whether the 3.4 % peak overshoot of F2 is the SPH sphere's own: the
   F0 rerun at S′ from step 1 is the comparison.
5. **C-1, D-2** at S′.
6. **Cost:** cycles and µs per particle-cycle for S′ against §9.1, measured on an idle machine. Use B-2 R/32 and one
   column run.
7. **D-3** needs A3.5 (cs12 and bay83 activation) first:
   - A4.0: code the bay83 form as printed in the primary source (Kebriaei 2014, and Bay 1983 if Peter supplies it),
     with page references in SPEC;
   - implement, check A-0 again, then run D-3 at S′.
8. **Optional, not stopping:** the D-1 refinement path of Addendum 1 A2.4 at S′ (50 → 100 → 200 particles per L;
   maximum deviation over the whole run). Then C-2 and C-3 at S′ with `surface.area = rate` and `cone + fit` named
   as settings, as diagnostics. Changing a default is a fix with its own CHANGELOG entry.

**Results:** `hvi_*.csv` rows with a `setup` column (`frozen` or `S'`), plus a new §15 in opencourant-verification.md
on `coldspray/opencourant-sph`. §15 lists, per required rung, the verdict under S′ next to the frozen-set-up verdict.

**Not in this task:** E-1. It waits for the E-1 gate
([../sph-contact-e1-gate-draft.md](../sph-contact-e1-gate-draft.md)) to be approved and frozen. E-1 itself runs under
Addendum 1 A4: frozen set-up as the main case, S′ alongside, stfac 3.

## Task 2026-11-11-a: record and commit before anything else (closed: done, §14, merged 5a251fc)

**Why:** the referee ([../sph-contact-referee-2026-11-11.md](../sph-contact-referee-2026-11-11.md)) found that most
results in the fork's VERIFY-RESULTS.md exist only in `~/oc_runs`. Several were made on binaries that were never
committed, and the predictions after 937ff00 cannot be dated by git. Until this is fixed, the C-1 and D-2 PASS claims
are **not admissible as verdicts**.

1. **Commit every run reported in VERIFY-RESULTS.md as a CSV row in `hvi/results/`.** Each row carries:
   - the fork SHA of the binary it ran on;
   - the ladder commit 36c34bd;
   - the deck hash;
   - the settings (ξ, kernel-correction order, α_cs, stfac, normal, gap).

   This covers:
   - C-1, C-2, C-3;
   - D-1, D-2;
   - B-2d at R/32;
   - the cone + fit full run and the fast-deck acceptance runs;
   - the stabiliser matrix (cases a and c);
   - the welded bars;
   - F1 and F2;
   - the E-1 probe (R/16, 800 m/s), labelled `unauthorised probe, diagnostic`.
2. **Uncommitted binaries.** Rows from a binary that was never committed are marked `binary uncommitted`.
   - Commit the current source, rebuild, and rerun the core rungs C-1 and D-2 on that committed binary. Only those
     rows can carry a verdict.
   - Also rerun A-0 on it (no sidecar, bit-identical).
3. **From now on:**
   - commit the source before every run campaign;
   - commit each recorded prediction (CHANGELOG) in its own commit before its runs;
   - never run on a dirty tree.
4. **Push to schemeforge,** as task 2026-11-08-a item 3 says: the `hvi_*.csv` files and a new **§14** in
   opencourant-verification.md, on `coldspray/opencourant-sph`. §14 states which rows are verdicts and which are
   diagnostics.
5. **Stop after this.** Make no new runs under ξ = 0.3 + order 1 (set-up S′) and no E-1 until Peter decides
   the addendum draft (since adopted as Addendum 1 of the ladder, 140b84a). Reruns of C-1, D-2 and
   A-0 under the frozen set-up (item 2) are allowed.

## Task 2026-11-08-a: sph-hvi-contact, milestone 1 (open; the S′ reruns are task 2026-11-11-b)

**Status 2026-11-11:**
- B-2, B-3 and D-1 FAIL under the frozen ladder (referee-confirmed for B-2 and B-3 from `hvi_b.csv`).
- The plan's stop rule applies from here on. A failing rung means stop, record and report; continuing needs Peter's
  decision.
- 2026-11-12: milestone 1 is blocked under the frozen set-up (S′ not adopted, DECISIONS 2026-11-12). The work
  continues as TLSPH (hunch CS-18, draft).
- E-1 waits for the frozen E-1 gate ([../sph-contact-e1-gate-draft.md](../sph-contact-e1-gate-draft.md), draft until
  Peter approves).

**Plan:** [../sph-hvi-contact-plan.md](../sph-hvi-contact-plan.md) (approved by Peter, DECISIONS 2026-11-08 "No-fork
dropped"). **Judge, frozen:** [../sph-contact-ladder.md](../sph-contact-ladder.md), commit 36c34bd. Cite its commit in every result.

1. **Repo.** Create the private repo `sph-hvi-contact` at `~/sph-hvi-contact`, in the WSL filesystem, not under
   `/mnt/c`. Start it from the OpenCourant source at the commit behind `latest-20261011`, and copy the plan there
   as `hvi/PLAN.md`.
2. **Part A, in order:** A0 (baseline; stop if it fails), A1 (CODEMAP), A2 (SPEC committed before code), then A3
   with the core rungs. E-1 comes after B-3, and E-2 after D-3.
3. **Results here:** push to `coldspray/opencourant-sph`:
   - one CSV per rung group under `docs/research/opencourant/results/` (`hvi_*.csv`), with the fork SHA and the
     ladder commit in every row;
   - a new section **§14** in opencourant-verification.md.
4. **Stops:** a failing core rung goes to Peter. Never run `check_untouched.sh` red. E runs are diagnostics only:
   no v_cr.

## Task 2026-11-05-b: CS-13c (closed: refuted, §13)

Protocol: [../coldspray-hunch-cs13c.md](../coldspray-hunch-cs13c.md), frozen in commit 15fe42f. Follow it exactly and
in this order:

1. **Rung B0:** elastic brick sphere on an elastic brick block, two TYPE7 contacts, 20 m/s, R/16 and R/32, against
   two-body Hertz. Choose and report the gap and Stfac; they are then frozen.
2. **Rung H0-k0:** the §11.2 brick slab with `/HEAT/MAT` and k = 0. The temperature may change by at most 0.1 K.
3. **Check whether OpenCourant writes per-element plastic work.** If it does not, the second clause of check E is
   reported only, as the protocol says.
4. **The 24 runs** (500 / 800 / 1100 m/s × R/16, R/24, R/32, R/48 × twins k = 237 and k = 0), plus one run per
   velocity at R/16 without `/HEAT/MAT`, reported only.
   - Check E in every run.
   - Keep the memory and time caps.
   - Budget stop: one R/48 run over 1 h, stop and report.
5. **Metrics P1–P3,** with the controlling element's body recorded, and P2 for both bodies. Then apply the frozen
   verdict rule exactly as written.

Results go in opencourant-verification.md **§13**. A failed rung or an impossible step goes to Peter.

## Task 2026-11-05-a: CS-13b (closed: blocked, §12)

Protocol: [../coldspray-hunch-cs13b.md](../coldspray-hunch-cs13b.md), frozen in commit 9a36aae. Follow it exactly and
in this order:

1. **Rung H0-SPH.** The H0 slab of §11.2 built from SPH particles (cubic net, §9.1 settings), with conduction,
   against erfc at t = 10 ns. Pass: within 2 % at the finest spacing, with the temperature written out. If it fails,
   the particle stays adiabatic, as the protocol says, and you continue.
2. **The 24 runs.**
   - Setup F as frozen in §10.2; 500, 800 and 1100 m/s; R/16, R/24, R/32 and R/48.
   - Each case adiabatic and conductive. Conduction in the bricks, and in the particle only if H0-SPH passed.
   - Contact adiabatic: no heat across TYPE7.
   - Budget stop: if one R/48 run takes more than 1 h, stop and report before the rest.
3. **Metrics, as defined in the protocol:**
   - P1: t_f;
   - P2: maximum substrate edge plastic strain within 1.17 µm of the contact edge, at t_c = 0.5 × the smallest t_f
     at that velocity;
   - P3: conductive minus adiabatic, reported only;
   - P0: comparison with the §10.5 values, reported only;
   - also report which element controls each run's stop (a brick or a particle).
4. **Apply the frozen verdict rule exactly as written,** including the adiabatic-twin control and the 6 % tolerance
   for R/32 → R/48.

Results go in opencourant-verification.md **§12**. A failed rung or an impossible step goes to Peter, as before.
