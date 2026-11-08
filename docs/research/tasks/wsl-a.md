# Tasks for WSL A (OpenCourant simulations)

Procedure: [../coldspray-procedure.md](../coldspray-procedure.md). Pull `claude/exciting-fermi-qy077p`, do the
newest open task, push results to `coldspray/opencourant-sph`. Write only your own section of
opencourant-verification.md and your own scripts and results. Do not edit STATUS, HANDOFF, DECISIONS, the hunch
files or this file. Blind-list papers stay closed.

## Task 2026-11-08-a: sph-hvi-contact, milestone 1 (open)

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
