# Tasks for WSL A (OpenCourant simulations)

Procedure: [../coldspray-procedure.md](../coldspray-procedure.md). Pull `claude/exciting-fermi-qy077p`, do the
newest open task, push results to `coldspray/opencourant-sph`. Write only your own section of
opencourant-verification.md and your own scripts and results. Do not edit STATUS, HANDOFF, DECISIONS, the hunch
files or this file. Blind-list papers stay closed.

## Task 2026-11-11-a: record and commit before anything else (open; do this first)

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
   [../sph-contact-ladder-addendum-1-draft.md](../sph-contact-ladder-addendum-1-draft.md). Reruns of C-1, D-2 and
   A-0 under the frozen set-up (item 2) are allowed.

## Task 2026-11-08-a: sph-hvi-contact, milestone 1 (open; paused until 2026-11-11-a is done)

**Status 2026-11-11:**
- B-2, B-3 and D-1 FAIL under the frozen ladder (referee-confirmed for B-2 and B-3 from `hvi_b.csv`).
- The plan's stop rule applies from here on. A failing rung means stop, record and report; continuing needs Peter's
  decision.

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
