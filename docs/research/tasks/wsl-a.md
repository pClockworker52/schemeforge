# Tasks for WSL A (OpenCourant simulations)

Procedure: [../coldspray-procedure.md](../coldspray-procedure.md). Pull `claude/exciting-fermi-qy077p`, do the
newest open task, push results to `coldspray/opencourant-sph`. Write only your own section of
opencourant-verification.md and your own scripts and results. Do not edit STATUS, HANDOFF, DECISIONS, the hunch
files or this file. Blind-list papers stay closed.

## Task 2026-11-28-a: edge-energy check (Stage 0 fork outputs and rung, then Stage A reruns)

**Basis:** DECISIONS 2026-11-28 (Peter's priority: "finding something that converges"). Spec, frozen 929afee (as
drafted in 46a4a53): [../edge-energy-check-2026-11-28.md](../edge-energy-check-2026-11-28.md). Where this task and
the spec differ, the spec holds. `kind = check`; no hunch, no budget. **Stage 0 must pass before any Stage A run.
Stop and report at the first failure.** Interleave with nothing big: the R/32 rerun runs alone on the machine.

1. **Set-up.**
   - Pull `claude/exciting-fermi-qy077p`. Bring `coldspray/opencourant-sph` up to date with it (fast-forward or
     merge; never force-push).
   - Fork: a new branch `energy-out` from the §30 engine `27e53d5f0` (spec §4: engine as §30 plus the output change).
2. **Preflight (source reading only; no build yet).** Report file:line for each item in the commit message of step 3
   and in §44:
   - where `tl_diag.csv`'s E_int, W_hg and W_visc are accumulated, and whether each is a sum of per-particle terms. If
     any is not (for example a global formula), **stop and report** before building: S0-1 cannot be met as written;
   - where the TL Cauchy stress and det F live per particle at an animation write;
   - the §30 AL08off, AL16off and AL32off decks and their animation times (frames 1.333 ns apart, A019 = 24.0 ns).
3. **Build (output only).** A new key, e.g. `out.energy` (default off). At every animation time it writes one record
   per TL particle, quarter model: id, w_i, h_i, q_i [J] (accumulated stress work V⁰ ∫ P:Ḟ dt, hourglass work, pair
   viscous work, the per-particle terms of E_int, W_hg, W_visc), Cauchy σ_i (6 components) and J_i.
   - Document the format and units in the source header and in §44.
   - T-A0 with the key off: identical on written metrics (55 runs, headers masked). Commit before step 4.
4. **Stage 0 rung** (spec §3), rows `opencourant/results/edge_energy_s0.csv` here and the same in the fork:
   - **S0-1:** AL08off rerun with `out.energy` on; per body Σ w, Σ h, Σ q against `tl_diag.csv` E_int, W_hg, W_visc
     at every frame, ≤ 0.1 % of KE₀;
   - **S0-2:** the same rerun reproduces the §30 AL08off written metrics (e, `tl_diag.csv`, interface file) bit for
     bit, headers masked;
   - **S0-3:** −tr σ_i / 3 against the written P_i, ≤ 10⁻⁶ relative, every particle, every frame;
   - **S0-4:** the T-B2 deck (§22.1) at R/16 with `out.energy` on. After separation the interface-layer ε_b(ρ) (spec
     §4 definition, both bodies, all four ρ) returns to ≤ 5 % of its in-contact peak, and Σ (h + q) stays ≤ 1 % of
     KE₀. If T-B2 has not been run at R/16 before, check its set-up file first (spec §8 item iv).
   - Commit the rows. If any item fails, stop and report: no step 5.
5. **Script and model checks, committed before any real profile is read.**
   - `hvi/scripts/edge_energy.py`: every definition of spec §4 in its docstring (depth, layer sets, A_c, ε_b, ε_ex,
     partner share, Δ and classes, Part B weight and flux, Part C isothermal Johnson–Cook content).
   - Run M1–M4 on the frame-0 lattices of the three meshes. Rows `edge_energy_model_checks.csv`. If M1 or M2 misses
     its class, or M3 comes out converging or converged: stop, **not determinable**.
6. **Stage A reruns.** AL08off, AL16off, AL32off with `out.energy` on, decks otherwise unchanged (about 100 s, 0.5 h,
   11–12 h; R/32 near 14.2 GiB plus the new arrays).
   - Check that each run reproduces its §30 e(off) and `tl_diag.csv`; report any difference, but do not judge it.
   - **Q1:** a(A019) from the interface file on the three meshes, within 5 % of each other. If not: stop, not
     determinable.
7. **Compute and judge** by spec §5 at A019, both bodies: ε_b(ρ) and ε_ex,b with Δ and classes, then the outcome.
   Reported, not judged: ε_b without h + q, h + q per layer, the partner share, the 0.5 t_p frame and the time series,
   Part B (F_b(ρ) profile), Part C (plastic content and its excess). Rows `edge_energy_{a,b,c}.csv`.
8. **Write-up:** verification **§44** on `coldspray/opencourant-sph`.
   - Include the preflight findings, the rung, the model checks, the tables, the verdict, the predictions against the
     outcome, a disclosure of what was read, and any deviation from the spec (listed before the verdict).
   - Observations beyond the rule are labelled. Keep the raw `out.energy` files until the modeller has merged §44;
     then report their size.

**Modeller's clarifications (2026-11-28; they fix details the spec leaves open, all in reported parts):**
- **Part B edge point:** (a, z_e), with z_e the mean current z of the particles carrying contact force within one
  spacing s of r = a, both bodies pooled. ∇q is the analytic gradient of q(ℓ) in the r–z plane. Per unit edge length
  means divided by π a / 2 (quarter).
- **Part B u_e:** (ȧ, ż_e) by central differences over animation frames.
- **Part C:** w_p from ε_p with A 148.4 MPa, B 345.5 MPa, n 0.183 at T_r and CE = 1 (spec r0 definition).

If a definition of the judged part turns out ambiguous while coding, stop and ask the modeller before step 7.

## Task 2026-11-27-b: kernel completion across a TLSPH contact, Stage A (static model; closed: both forms fail, §43, merged)

**Basis:** DECISIONS 2026-11-27, "Cold-spray track unpaused" (Peter: option 1). Spec, frozen 9369e6c (as drafted in
eae3ed5): [../kernel-completion-2026-11-27.md](../kernel-completion-2026-11-27.md). Where this task and the spec
differ, the spec holds. `kind = check`; no hunch, no budget. **Python only: no solver run, no build, no existing
solver output read.**

1. **Set-up.**
   - Pull `claude/exciting-fermi-qy077p`.
   - Recreate `coldspray/opencourant-sph` from it (deleted in the clean-up of 2026-11-27).
   - Fork: work on `cs12`.
2. **Script and model checks, committed before any K2–K5 number.**
   - Write `hvi/scripts/tl_kc_static.py`, built on `tl_endlayer.py`: periodic lateral cell with explicit particles
     and images, the laws L0, KC-f, KC-full and BCT, and the cases K1–K5, all exactly as the spec defines them.
     Write every definition in its docstring.
   - Run only the two model checks:
     - L0 on K1 against 0.6515 / 0.8397 to 0.002 on both sides;
     - KC-full on K1 bulk to 1e-9, transmitted force to 1e-9, residual ≤ 1e-10.
   - Commit the script and the check rows. If a check fails, stop and report; compute nothing else.
3. **Cases.** Run L0, KC-f, KC-full and BCT on K1–K5.
   - Rows `hvi/results/tl_kc_static.csv` in the fork and `docs/research/opencourant/results/tl_kc_static.csv` here,
     `kind = check`.
   - Per law and case: p_k for layers 1–3 on both sides, e_face, e_bulk, transmitted force / (t · area), residual.
     Put the full layer profiles in a second file, `_profiles.csv`.
4. **Verdict** by the spec's rule, separately for KC-f and KC-full: consistent, partial or fails. Name the case that
   decides each. Report BCT; do not judge it. List any deviation from the spec (none expected) before the verdict.
5. **Write-up:** verification §43 on `coldspray/opencourant-sph`.
   - Include the verdicts, the model checks, the full table, the predictions against the outcome, and a disclosure of
     what was read.
   - No reading that goes beyond the rule; observations are labelled as such.

Do not start Stage B, and do not edit the spec. If a definition turns out ambiguous while coding, stop and ask the
modeller before computing K2–K5.

**Step 2 done (fork `8863ccf4`):** both model checks pass, reproduced in the cloud from the committed script (L0 on K1
0.65151 / 0.83971; KC-full on K1 max |p − 1| 2e-13, T = 1 + 1e-14).

**Modeller's answers to the readings in the script's docstring (2026-11-27, before K2–K5; clarifications, not spec
changes):**
1. **K5 lateral alignment:** confirmed. B's lateral lattice contains A's columns (B at (i, j) s_B, i, j = 0, 1). This
   is "layer planes aligned" plus the same alignment as K1 and K4.
2. **K5 B-side layer value:** confirmed. p_k is the volume-weighted layer mean, as §17/§22 report layer averages;
   e_face is judged on the means. Report min and max beside them; they are not judged.
3. **Hourglass over own pairs only:** confirmed. The spec puts cross pairs into the force sum (and into K and F for
   KC-full) only. The hvi contact has no hourglass term either.
4. **L0 point force = t × the particle's lateral area:** confirmed. It is the spec's "+t / −t on every particle", with
   the area explicit so the two sides balance in K5.

Proceed with step 3.

## Task 2026-11-27-a: delete the G1 raw files of task 2026-11-26-a (housekeeping; closed: done, f785d31, merged e67d639)

**Step 1 result (WSL A, 2026-11-27): stopped, nothing deleted.** Everything judged in §42 rests on committed rows; peak
RSS is in `~/oc_runs/hvi_seclin/run_g1_*.log` (outside g1, stays). Only in the raw files: the "R/64 output check"
bullets of §42 / SPEC-TL-b §22.2 (hand-computed from `g1/Q2n032`): 10–14 block edges inside a; p_max/p₀ 1.04–1.08;
|F_int/F_mom − 1| 0.3–0.9 % and halved cadence ≤ 4·10⁻⁴; a_code/a_F 1.35–1.46 and rim node spacing 1.705 → 2.185 µm;
time-history spacing median 21.95 ps. g1: 516 files, 4 787 344 304 B (Q2n032, Q2n064, Q2n128); no .vtk left; six
small files beside it (eval_g1.log, run.log, run_g1_{32,64,128}.log, run_seclin.sh).

**Modeller's decision (2026-11-27): write the R/64-check rows first, then delete all of g1.**
- **1b.** Add a subcommand to `hvi/scripts/tl_cal10_seclin.py` (or a small committed script beside it) that computes
  exactly the five bullet items above from `g1/Q2n032`, with the definitions written in its docstring as §42 states
  them. Reading existing files only; no run, no new quantity, no other mesh. Rows: fork
  `hvi/results/tl_cal10_seclin_g1_r64check.csv` and here `opencourant/results/tl_cal10_seclin_g1_r64check.csv`
  (`kind = calibration`; per item: quantity, frame or frame range, value, unit).
- Compare each value with the §42 text at its stated precision. A difference is reported in the commit message
  and to the modeller, not fixed: §42's text stays as merged. Add one dated line under §42's R/64 output-check bullets
  naming the rows file (and any difference), on `coldspray/opencourant-sph`.
- Then step 2 on the full checked list (all 516 files in g1; the six files beside it stay), and step 3, with the
  rows commit sha in the message.

**Basis:** DECISIONS 2026-11-26 "Proposal B closed" (G1 raw files kept until §42 is merged) and task 2026-11-26-a's
closing note ("keep until §42 is merged to main; then report its size, and delete only with the modeller's OK").
§42 is merged (5208b15) and on `main`. This is the modeller's OK, given at Peter's request (chat 2026-11-27). No run,
no build, no result section. The cold-spray pause is unchanged (DECISIONS 2026-11-27).

1. **Check first.** Pull `claude/exciting-fermi-qy077p`. Confirm that §42 and the five rows files
   `docs/research/opencourant/results/tl_cal10_seclin_{g0,runs,g1,g1_rich,g2_expected}.csv` are there, and that the
   fork holds SPEC-TL-b §22.2 and `hvi/results/tl_cal10_seclin_*` (G1 evaluation `4b4cc0719`, Richardson item
   `2d8c756f6`). The raw files are inputs only; if any number in §42 or SPEC-TL-b §22.2 exists only in a file under
   `~/oc_runs/hvi_seclin/g1`, stop and report it instead of deleting.
2. **List, then delete.** Write the list of entries under `~/oc_runs/hvi_seclin/g1` with the total size, check it, and
   delete exactly that list. Delete nothing outside `g1`. If `~/oc_runs/hvi_seclin` holds anything else, report
   its paths and sizes, untouched. The .vtk cache was already deleted (DECISIONS 2026-11-26); confirm it is gone.
   Leave the §25, §30 and CS-23 run files untouched.
3. **Report in one commit message** (empty commit is enough) on `coldspray/opencourant-sph`. The branch was deleted in
   the clean-up of 2026-11-27, so recreate it from `claude/exciting-fermi-qy077p` first. The message gives the path
   deleted, the number of entries, the space freed in bytes, anything left in `~/oc_runs/hvi_seclin`, and the sha
   that holds §42 (5208b15 on this branch, 87a1d4e as written).

## Task 2026-11-26-a: proposal B, equilibrium resultants around the contact edge (convergence check; closed: G1 failed, negative; §42 87a1d4e)

**Closed (2026-11-26).** Verification §42 on `coldspray/opencourant-sph` at `87a1d4e`. The follow-on contact-edge
proposal (fork `3d658fd82`) was not approved (DECISIONS 2026-11-26 "Contact-edge proposal ... not approved"). Keep
`~/oc_runs/hvi_seclin/g1` until §42 is merged to main; then report its size, and delete only with the modeller's OK.

**Close (2026-11-26, Peter: "Close as negative"; DECISIONS 2026-11-26 "Proposal B closed as a negative result after
G1").** G1 failed (fork `4b4cc0719`): ℓ_out at f = 0.5 converges at 28 of 61 frames, limit 0.8; all other G1 items
pass. G2, G3 and step 6 are not run or read. No revision. **What is left, step 7 only:** verification §42 on
`coldspray/opencourant-sph`, with the negative stated as such, the G0 and G1 tables, the predictions against outcome, the
two listed changes, the binary note, and the disclosure of what was read. SPEC-TL-b §22.2 is already the fork record.
Keep `~/oc_runs/hvi_seclin/g1` until §42 is merged, then report its size; do not delete it without the modeller's OK.
§42 also carries the Richardson extrapolation of G1 ℓ_out (fork `2d8c756f6`, rows `tl_cal10_seclin_g1_rich.csv`) as a
**reported item only** (Peter, 2026-11-26): not frozen, not judged, no bearing on the G1 verdict or the close, with
WSL A's caveats (continuum not Gauss-sampled reference, quasi-static a_F, three meshes, smooth case, nothing about §25).

**Basis:** Peter, chat 2026-11-26 (DECISIONS 2026-11-26 "Cold-spray diagnostic exception: proposal B ... approved").
It is a diagnostic exception to the cold-spray pause. The track stays paused; there is no route verdict, no hunch and
no bonding claim. `kind = calibration`.

**Spec:** fork `sph-hvi-contact`, branch `cs12`, commit `eab2e1c21`,
`hvi/PROPOSAL-2026-11-26-section-linearization.md`, revision 2 (quantities E1, E1-F, E2, E3; gates G0–G3; judged
set; outcomes). Where this task and the spec differ, this task holds. **The hot-spot proposal is dropped:** do not
compute H1 or H2, not even as a by-product.

**Scheduling:** in gaps between Peter's Gate 6 WSL runs, never alongside a big job. The promo zoo and γ-sweep are
done (DECISIONS 2026-11-25 "Target D thresholds accepted"); the breaker run on the zoo is next
(docs/judge/contact_promo_wsl.md §3), and a promo rerun follows if a breaker case is accepted into the judge. Every engine start goes through the watchdog. Estimate
memory before each R/256 run. Check Windows Update before runs of several hours. Gate 6 runs take priority: if one is
waiting, it goes first.

**Values frozen by this task** (from the spec; Peter may change any of them before step 1 is committed, not after):

| Item | Value |
|---|---|
| Reading rule, usable | driver-check-2026-11-17.md §3 unchanged; usable = ≥ 80 % of judged points, block side, both speeds (§25); G1, G2: ≥ 80 % of their frames |
| Judged on §25 | primary ℓ_out at f = 0.25 and 0.5 (headline: usable at either f, each reported); secondary F_out/F_tot at f = 0.5; reported only: F_out/F_tot at f = 0.25, the particle side, E1-F, E2, E3 |
| §25 judged outputs | 3–9 (600 m/s), 3–8 (500 m/s); folded frames flagged and evaluated |
| Upper limit of M_out | r_up = 1.2 a_ref (a_256 on §25, a_code,256 in G1 convergence, a_F in G1 accuracy, a_p in G2); variant at each mesh's own a_m reported |
| G0 tolerance | 1e-4 relative against the spec's continuum values |
| G1 frames | convergence: every frame from 0.2 to 0.8 t_H; accuracy: frame nearest the force peak and the mean over 0.4–0.6 t_H |
| G1 judged | ℓ_out convergence at both f; F_out/F_tot at f = 0.5 (convergence and \|q_FE,256 / q_samp,256 − 1\| ≤ 2 %); F_tot: \|F_mom / F_int − 1\| ≤ 2 % and the change with every second output ≤ 1 %, at every G1 frame on R/256 |
| G2 | a_p = 2.5 µm; ramp over ≥ 20 depth transits, then hold; edge element p_n growth ≥ 1.25 per refinement; ℓ_out at both f and F_out/F_tot at f = 0.5: reading rule and \|q_FE,256 / q_samp,256 − 1\| ≤ 2 % |
| G3 | §25 momentum-rate F_tot, every output against every second output: change ≤ 1 % at ≥ 80 % of the judged points, both speeds |
| Binary | `d0500106d` (the §25 binary) for every gate and run |

**Steps.** A failed gate stops the task. Report it and record the negative result; nothing after it is run or read.
1. **Plan commit (fork), before any run or any reading of output.** It contains: script `hvi/scripts/tl_cal10_seclin.py`
   with every definition in its docstring (cut, F_in by exact intersection lengths, F_tot by momentum-rate central
   differences, M_out, ℓ_out, the G1/G2 sampled references, the reading rule); the G2 punch deck; the expected G2 values
   from the closed-form Sneddon stresses at the actual Gauss points of each mesh; the recomputed ℓ_out orientation at
   1.2 a_p; memory and time estimates for the R/256 runs; and **your predictions for revision 2's judged set** (the
   spec's §7 numbers are revision 1's). Report the sha and stop: the modeller has the frozen plan reviewed before step 2.
2. **G0** (no run). Rows `hvi/results/tl_cal10_seclin_g0.csv`.
3. **G1:** two-body quad Hertz, `tl_cal4_quad.py`, full block (3R × 2R), R/64, R/128, R/256. These are reruns, since no
   tl_cal4 run directories survive. Check the contact-radius rule and the station output on R/64 first; this is a
   facts gap (spec §8). Rows `..._g1.csv`.
4. **G2:** flat rigid punch, the same block and meshes. The prescribed-displacement deck has never been run on quads:
   check the reactions, the free radial motion and the dynamic residual on R/64 before the finer meshes. Rows `..._g2.csv`.
5. **G3** (no run): on the committed §25 frames in `~/oc_runs/hvi_p3`. Rows `..._g3.csv`.
6. **§25 resultants:** the judged set and the reported items. E1-F needs one §25 rerun with contact-force output
   (about 8 min). Check that output on a small 2D TYPE5 deck first. If it does not work, report it and leave E1-F out.
   Rows `..._p3.csv`.
7. **Write-up:** a new SPEC-TL-b section (fork) and verification §42 (on `coldspray/opencourant-sph`), with the
   disclosure of what was read (the spec, §6). Negative results are stated as such.

**Facts check before each step** (solver-facts.md): the spec's §8 list of facts not yet covered applies. Parser keys:
the E1-F output card and the punch's `/IMPDISP` (or equivalent) and `/BCS` are new; check each on a small deck first.
Delete `.vtk` cache after evaluation, from a checked file list (C: at 84 %).

**Step 1 review (2026-11-26, desktop; Peter: "match the cadence first").** Plan `c4b34b2c5` (SPEC-TL-b §22.1)
accepted with one change. Step 2 may start once the change is committed.
- **Change: G1 time-history cadence = §25's.** The plan has G1 `/TFILE` at t_H/4000 = 9.5 ps. §25 writes its time
  history at dt_anim/4 with dt_anim = (D/V)/400 (tl_cal6_p3.py): 20.8 ps at 600 m/s, 25.0 ps at 500 m/s. Set G1 to
  20.8 ps (the finer of the two), so G1's F_mom check tests the estimator §25 uses (s = 1 window 41.7 ps, s = 2
  83.3 ps), not a shorter, chattier one. Reason: with t_H/4000 a G1 failure from contact chatter would stop the task
  although §25's longer window might not show it. No output had been read; this is not tuning. Record it in §22.1
  and in the script docstring as a listed change, in its own commit, before any run. Predictions may be revised in
  the same commit (say which).
- **Flagged readings, all accepted:** F_mom from the time-history outputs (G3 stride 2 on that cadence); G1 F_tot
  check at every frame 0.2–0.8 t_H on R/256, not 80 % (literal task reading; keep it); r-weighted Gauss-point mean
  (verified: `q4forc2.F:612` calls `S8EFMOY3`); G0 against high-precision continuum at 1e-4, printed values to half
  a unit of the last digit; surface edges from the deck node lists.
- **Checked, no change:** G2 expected values (continuum F_out/F 0.96825 / 0.86603, ℓ_out 0.5557 / 0.3546 agree with
  the review's recomputation); the punch kernel σ_zz/p_mean = −½ ∫ sin t (1 + ζt) e^{−ζt} J0(ρt) dt follows from the
  Love/Boussinesq σ_zz kernel and the Hankel transform of p_mean/(2√(1 − ρ²)); G2 load linear (u0 = 0.064 h on
  R/256), ramp quasi-static; cost and memory consistent with tl_cal4_quad.csv; prediction arithmetic adds up
  (G1 0.3 above its sub-item product 0.19, read as correlated).

**After steps 2–3 (2026-11-26, desktop; Peter: "Confirm, evaluate G1").** Fork: listed change 1 `8b8ecae2d`
(G1 TH 20.8 ps), G0 `35dddfa3a` (pass, worst 3.8·10⁻⁶), listed change 2 `3c1e161d4`, G1 runs `55ab7da2a`
(R/64, R/128, R/256 rc = 0; R/256 7973 s, 0.66 GB RSS; not evaluated).
- **Listed change 2 confirmed:** F_mom = +2π dZMOM/dt. The plan's code had −2π, against its own frozen definition
  ("positive when the block pushes the particle up"); found in the required R/64 output check (−1.04 F_max at the
  peak), before any judged quantity; post-processing only, the sign of tl_cal2_quad2body and tl_cal6_p3.
- **Evaluate G1 now** (rows `..._g1.csv`, pass/fail per judged item); if it passes, step 4 (G2, R/64 checks first).
- **Write-up note:** `fork_sha` in `tl_cal10_seclin_runs.csv` (`38639859c`) is the working tree's last solver commit,
  not the binary's; the runs used `~/oc_runs/ocroot_d0500106d` (built 2026-11-16). State it, or add a binary column.

## Task 2026-11-24-b: delete the band-check arrays (housekeeping; closed: done, 14d15aa)

**Basis:** Peter, chat 2026-11-24 (DECISIONS 2026-11-24 "Cold-spray scope review"). No run, no build, no result
section.
1. Check that every number in §41 and its rows is already committed on `coldspray/opencourant-sph` (the per-frame
   arrays are inputs only).
2. Delete `~/oc_runs/hvi_band` (about 5.5 GB). Leave the §30 and CS-23 run files untouched.
3. Report in one line on your branch (commit message is enough): the path deleted, the space freed, and the sha that
   holds §41.

## Task 2026-11-24-a: band check (closed: §41 intermediate; merged)

**Basis:** Peter, chat 2026-11-24 ("Freeze"). **Spec, rule and prediction, frozen:**
[../band-check-2026-11-24.md](../band-check-2026-11-24.md), frozen in the commit that adds this task. Cite it in
every row. `kind = check`.

**No run, no build:** read and post-process existing files only. Which files:
- the §30 off runs AL08off, AL16off, AL32off (engine `27e53d5f0`);
- for the reported bonded item, the CS-23 30× runs (engine `38639859c`, §39).

If anything more is needed (a rerun, a new output, another deck), stop and report.

1. **Q1 first**, before any profile is computed (spec §Q1): ε_p and positions per particle in every frame with
   stable ids on all three meshes; the frame times and the frame nearest t = t_p; per-particle volume; the same for
   the CS-23 30× runs.
   - If Q1 fails for an off run: stop and report "not determinable from existing files".
   - If it fails only for the CS-23 runs: drop their reported item and continue.
2. **Fix the definitions in the script's docstring before any profile number is read:**
   - the station membership (0.75 s of the reference line, azimuth 45°);
   - depth d in the reference configuration;
   - ε_bg (median at 3 ≤ d ≤ 5 µm);
   - ε_peak;
   - w_½ with linear interpolation;
   - the qualifying test;
   - q and q′.

   Commit the script before running it on the data.
3. **Judged item:** per station and mesh, at the frame nearest t_p: ε_bg, ε_peak, w_½ (µm and in spacings), the
   qualifying test, q and q′, and the station class (mesh-scale / resolved / unclear). Then the verdict line against
   the spec's rule.
4. **Reported items, as the spec lists them:**
   - the sink table at t_end from `tl_diag.csv` and the interface file (KE of particle and substrate, E_int, W_hg,
     W_visc, W_d, E_c, each with its R/8 → R/32 change against ΔKE);
   - zone and rest plastic work, trapezoid and left-point;
   - last-frame widths;
   - current-configuration widths;
   - non-qualifying stations;
   - the peak's layer index;
   - the CS-23 30× widths.
5. Rows `results/band_check_*.csv`; the next free section of opencourant-verification.md (§41), with the verdict
   line and the prediction against the outcome. Then stop and report.

## Task 2026-11-23-c: what `/NONLOCAL/MAT` regularises, and what a length for our decks would cost (closed: §40 damage-only, no zero-code length; merged)

**Basis:** Peter, chat 2026-11-23 (DECISIONS 2026-11-23, "Focus on the physical length scale; Track B paused").
Note: [../length-scale-note-2026-11-20.md](../length-scale-note-2026-11-20.md) §10. **No build, no run.** Read the
`cs12` source at `38639859c`; give file and line references for every answer. If anything beyond reading is needed,
stop and report.

Modeller's reading from an old copy of the fork (`main` `e9432e6e`, unconfirmed): the OpenRadioss base has
`/NONLOCAL/MAT` (keys LENGTH, LE_MAX; `hm_read_nonlocal.F`); the regularisation is solved only in 3D solid and shell
routines (`*fint_reg*`); quads (`qforc2.F`) and SPH (`spstres.F`) only pass `NLOC_DMG` through; laws touched include
mat002 (LAW2) but not mat004 (LAW4). Confirm or correct each point on `cs12`.

1. **The equation and the variable.** Which equation is solved (implicit gradient f̄ − ℓ²∇²f̄ = f, or another form),
   with which time integration and damping (`DENS`, `DAMP`, `SSPNL`), and which variable is regularised.
2. **Where it enters LAW2.** Does the nonlocal variable enter LAW2's yield stress (hardening, rate or temperature
   term), or only a failure or damage model? Is the temperature that softens LAW2 local?
3. **Element and law coverage.** Which element formulations solve the regularisation. What happens when a deck sets
   `/NONLOCAL/MAT` on 2D quads (Isolid 17), on native SPH or TLSPH particles, or with LAW4: an error, or silently
   ignored?
4. **LAW2 against LAW4 for the §25 / §30 decks:**
   - Can LAW2 take `/EOS/GRUNEISEN` in this version?
   - How does LAW2 heat (adiabatic from internal energy?), and what does it do at T ≥ T_m?
   - Any differences from LAW4 that would change the §25 quad deck or the §30 TLSPH deck.
5. **Cost estimate, design only.** What would a Ge-type nonlocal model (ε_p and T regularised, over-nonlocal factor m;
   data/ge2026_reading.md §4) need in (a) 2D axisymmetric quads (the §25 deck) and (b) TLSPH (the §30 deck):
   - files touched (Siemens-licensed files must stay byte-identical);
   - the solve and its time-step effect;
   - a calibration check with a closed form: a softening bar whose band width scales with ℓ.

   Give a rough effort estimate.
6. Write up as §40 of opencourant-verification.md (the next free number) on `coldspray/opencourant-sph`. Then stop
   and report.

## Task 2026-11-21-a: softening check with a quad temperature output (closed: §33 informative; merged)

**Basis:** DECISIONS 2026-11-21, "Softening check stopped; quad temperature output to be fixed" (Peter: option (b)
of §32). **Spec, rule and prediction, frozen:** [../softening-check-2026-11-20.md](../softening-check-2026-11-20.md)
(66636c8), unchanged. `kind = check`. If anything beyond an output change is needed, stop and report.

**Keep CS-22b's binary untouched:** build this on a separate fork commit and engine directory. Before resuming
2026-11-20-a, confirm that its engine is still `27e53d5f0` (same binary hash as in §30's runs).

1. A short design note (fork SPEC-TL-b) first: write the Gauss-point average of `LBUF%TEMP` as the element
   temperature output for 2D quads (Isolid 17), as shells and 3D solids already do. Output only.
2. Run `hvi/scripts/check_untouched.sh`. If any Siemens-licensed file would change, stop and report.
3. Build; T-A0 must be bit-identical (55 of 55).
4. Rerun the two §25 R/256 decks (600 and 500 m/s, `/ANIM/ELEM/TEMP` as in §32) on the new build. Every output
   except the temperature field must be byte-identical to §32's reruns; else stop and report.
5. Compute the spec's quantity S = 1 − T*ᵐ (disc averages, edge minimum, T_max) at every judged output and apply the
   spec's rule. Also compare with §32's reconstruction (reported, not judged). Rows
   `results/softening_check2_*.csv`; section §33 with a verdict line. Then stop and report.

## Task 2026-11-22-d: CS-23 (forked bond response with sticking bonds) (closed: §39 CS-23 refuted; merged)

**Basis:** Peter, chat 2026-11-22 ("Freeze"). **Judge, frozen:** [../coldspray-hunch-cs23.md](../coldspray-hunch-cs23.md),
frozen in the commit that adds this task. Cite it in every row. Run jobs one at a time, each under the watchdog. If
anything beyond the hunch file is needed (a code change, another deck, another δ_c, another key), stop and report.
Abort handling as task 2026-11-20-a (externally killed runs are rerun from t = 0 and reported as rows with
`reached_t_end = 0`; defer Windows updates before the R/32 runs).

1. **Engine** `38639859c` (binary `~/oc_runs/ocroot_38639859c`). Deck: the CS-22b deck script (`hvi/decks/al_cs22b.py`),
   byte for byte except `bond.stick = on` and `out.pairs` on. State the deck diff against CS-22b's in the write-up.
2. **First run: R/8 at δ_c = 0.09375 µm.** Before reading anything else from it, apply the hunch's **W_s validity
   check** (per-pair W_s summed over `out.pairs` = global W_s in the interface file to 1e-10 relative at every
   record). If it fails: stop and report; no dR is read.
3. **Stage 1:** on runs at δ_c = 0.09375, 0.3125, 0.9375 µm, each at R/8 and R/16 (6 runs). No off runs: the off
   branch is §30's AL08off, AL16off, AL32off.
4. **Lost-bond check at pair level** on every run, as the hunch defines it (lost = leaves "bonded" by neither tearing
   nor a sweep; a lost pair makes the run invalid for that δ_c). Report swept pairs (count, δ/δ_c at the sweep);
   they do not invalidate. Say how a swept pair appears in the per-pair file (from the source) before the first
   verdict.
5. **Gate:** R/32 for a δ_c only if its R/8 and R/16 runs are valid, reach t_end (or the CS-22 stuck exception
   applies) and |dR16| ≥ 0.01. At most 3 R/32 runs. Check memory before each (estimate 14.8 GiB, §38; VM 23.5 GiB).
6. **Report per δ_c and mesh:** e(on), dR, bonded pairs and bonded area at t_end, maximum bonded area, W_b, W_s,
   W_proj, s_pl (total and gained at re-compression), the energy balance including W_s, lost and swept pairs,
   per-pair δ_t at tearing against δ_c; for a stuck particle, the target-surface velocity at t_end. Rows
   `results/tl_cs23_*.csv`.
7. Write up as §39 of opencourant-verification.md on `coldspray/opencourant-sph`, with a verdict line per δ_c and
   overall against the frozen rule, and the hunch's predictions against the outcome. Then stop and report.

## Task 2026-11-22-c: stick law, energy-consistent cap shrink (closed: §38; merged)

**Basis:** §37 limitations (settle before CS-23); modeller's decision 2026-11-22 (approved by Peter). Fork branch
`cs12`, on top of `0153cae04`; earlier binaries stay unchanged. Design note first (SPEC-TL-b, own subsection). If
anything beyond the items below is needed, stop and report.

1. When δ_cap = τ_B s²/k drops below |δ_t,el| without new tangential motion (σ_B softening with σ_flow(T), or
   re-compression), scale δ_t,el down to δ_cap (direction kept) and book the released elastic energy
   ½(1 − D)k(|δ_t,el|² − δ_cap²) as dissipation in W_s, not force × slip; s_pl is unchanged by this step.
2. Book the energy lost in the tangent-plane projection of δ_t,el the same way (into W_s, with a separate per-pair
   counter so its size can be reported).
3. Weight ghost records ½ in the per-pair W_s, as in the global.
4. Checks (calibration):
   - a bonded shear deck where σ_B is ramped down (e.g. a prescribed temperature rise) while the pair is held at the
     cap: the energy balance W_in = E_c + W_d + E_b + W_b + W_s must close to 1 %;
   - §37's shear checks S0 and S1 unchanged in their force-law results;
   - T-A0 55/55; stick off unchanged against `0153cae04`;
   - a memory estimate for the §30 R/32 deck with stick on and `out.pairs` (16-slot records), against the 23.5 GiB VM.
5. Next free section with rows; then stop. **No impact runs**: CS-23 waits for its freeze.

## Task 2026-11-23-a: cs12 option "bonded pairs stick" and per-pair output (closed: §37; merged)

**Basis:** DECISIONS 2026-11-22, "Bonded pairs stick under compression". Fork branch `cs12` (new commits on top of
`27e53d5f0`; CS-22b's binary stays available unchanged). If anything beyond the items below is needed, stop and
report.

1. **Design note first** (fork SPEC-TL-b, own section), committed before any code:
   - new key `bond.stick` (default off; off must be bit-identical to `27e53d5f0` in every output);
   - with stick on, a bonded pair with g ≤ 0 carries a tangential traction t_t = −k δ_t,el (k the contact penalty
     stiffness), capped at τ_B = σ_B/√3; beyond the cap the pair slides at τ_B, and that plastic slip dissipates, is
     booked separately (energy and per pair), and does **not** enter δ or D;
   - for g > 0 the existing mixed-mode law is unchanged; state exactly what δ_t is at reopening (the elastic part
     δ_t,el only);
   - unbonded contact unchanged (frictionless);
   - per-pair output at each interface record: pair ids, δ_t (elastic), g, D, bond state, compressed-slip total,
     σ_B (new file or a new interface-file version; the reader updated).
2. **Code and build.** T-A0 must be 55 of 55 identical; with stick off, a §30 deck must be bit-identical in its written
   metrics to `27e53d5f0`.
3. **Checks (calibration, not rungs):**
   - two TL blocks, bonded, pressed then sheared: the transmitted shear equals k δ_t,el below the cap and τ_B at the
     cap; zero shear with stick off; the energy balance closes (plastic slip work booked);
   - D-3/D-4 of §26 unchanged with stick off;
   - the per-pair output, summed to particles, reproduces §36's per-particle slip on one existing deck with stick off.
4. Write up as the next free section with rows; then stop and report. **No impact runs**: they wait for CS-23's freeze.

## Task 2026-11-22-b: slip check (closed: §36 mixed; merged)

**Basis:** Peter, chat 2026-11-22. **Spec, rule and prediction:** [../slip-check-2026-11-22.md](../slip-check-2026-11-22.md).
Do not start before its title reads "frozen". `kind = check`. Reading and post-processing of the existing CS-22b
on-run files only: no run, no build. If anything more is needed, stop and report.

1. Q1 from the source, with file and line references. If Q1 says "not determinable", stop and report.
2. Q2 from the existing CS-22b on-runs (§31).
3. Rows `results/slip_check_*.csv`; the next free section of opencourant-verification.md with the verdict line
   (slip decides / opening decides / mixed / not determinable) against the spec's rule. Then stop and report.

## Task 2026-11-22-a: confirm the formalism note's equations against the source (closed: §35; merged)

**Basis:** Peter, chat 2026-11-22. Note: [../problem-formalism.md](../problem-formalism.md), §1 and §4. No run, no
build. For each item give the exact expression as coded, with file and line references, and say whether the note's
form is right; do not edit the note.
1. Eq. 3 and 14: the TLSPH force sum, deformation gradient and gradient correction (SPEC-TL).
2. Eq. 5: the `/EOS/GRUNEISEN` pressure expression (compression and expansion, μ convention, energy per volume or
   per mass, the role of γ₀ and a).
3. Eq. 6: the objective stress rate used for SPH/TL particles.
4. Eq. 7: LAW4's rate term as implemented (which ε̇, any cap, ε̇₀).
5. Eq. 10–12: hvi penalty contact and the cs12 law as coded.
Results as a short section of opencourant-verification.md (next free number). Then stop.

## Task 2026-11-21-b: TLSPH temperature check (closed: §34 (b) heats, not written; merged)

**Basis:** Peter, chat 2026-11-21. **Spec, rule and prediction, fixed:**
[../tlsph-temperature-check-2026-11-21.md](../tlsph-temperature-check-2026-11-21.md). Cite it in every row.
`kind = check`. No engine run, no build; CS-22b's binary `27e53d5f0` stays untouched. If anything beyond source
reading and post-processing of existing files is needed, stop and report.

1. Q1 from the source, with file and line references.
2. Q2 from the §30 runs AL08off and AL16off (existing files only).
3. Rows `results/tlsph_temp_check_*.csv`; a short section of opencourant-verification.md (next free number) with the
   verdict line (a)–(d) against the spec's rule. Then return to CS-22b.

## Task 2026-11-20-a: CS-22b (δ_c ladder) (closed: §31 CS-22b supported at 30×; merged)

**Abort handling (Peter, DECISIONS 2026-11-21):** an externally killed run (OS update, VM restart) is not a run
failure under the frozen rule. Report which runs reached t_end (they stand). Rerun the killed run from t = 0 with the
same engine, deck and δ_c (no restart). Report the killed attempt as a row with `reached_t_end = 0` and the cause, as
with §30's try rows. Before the long R/32 runs, defer Windows updates (active hours or pause) if possible.

**Basis:** DECISIONS 2026-11-20, "CS-22b frozen". **Judge, frozen:**
[../coldspray-hunch-cs22b.md](../coldspray-hunch-cs22b.md), frozen in the commit that adds this task. Cite it in
every row. Run jobs one at a time, each under the watchdog. If anything beyond the hunch file is needed (a code
change, another deck, another δ_c), stop and report.

1. **Before any run:** report from the fork the opening at which a cross-body pair leaves the candidate list
   (expectation only; it changes no rule).
2. **Stage 1:** engine `27e53d5f0`, the §30 deck script (`hvi/decks/al_cs22.py`), on branch settings as §30 except
   δ_c. On runs at δ_c = 0.09375, 0.3125 and 0.9375 µm, each at R/8 and R/16 (6 runs). No off runs: the off branch
   is §30's AL08off, AL16off, AL32off.
3. **Lost-bond check** on every run, from the interface file: a skin facet whose bond state goes from bonded to not
   bonded between two records while D < 1. Any lost bond makes the run invalid for that δ_c.
4. **Gate:** R/32 for a δ_c only if its R/8 and R/16 runs are valid, reach t_end (or the CS-22 stuck exception
   applies) and |dR16| ≥ 0.01. At most 3 R/32 runs. Check memory before each (VM at 23.5 GiB).
5. **Report per δ_c and mesh:** e(on), dR, bonded pairs and bonded area at t_end, maximum bonded area, bond work,
   lost bonds. Rows `results/tl_cs22b_*.csv`.
6. Write up as §31 of opencourant-verification.md on `coldspray/opencourant-sph`, with a verdict line per δ_c and
   overall against the frozen rule. Then stop and report.

## Task 2026-11-20-b: softening check (closed: §32 stopped, the quad temperature output is not the material temperature; merged)

**Basis:** Peter, chat 2026-11-20. **Spec, rule and prediction, fixed:**
[../softening-check-2026-11-20.md](../softening-check-2026-11-20.md). Cite it in every row. `kind = check`.

1. From the §25 R/256 field files (600 and 500 m/s, binary `d0500106d`), compute the JC softening factor
   S = 1 − T*ᵐ as the spec defines: disc averages at 0.25, 0.5, 0.75 a_256 on both sides, the edge minimum, and the
   maximum temperature, at every judged output.
2. If the field files hold no temperature: rerun the two R/256 decks with temperature output added and nothing else
   changed; the stop time and a_256(t) must match §25 exactly, else stop and report.
3. Rows `results/softening_check_*.csv`; a short section of opencourant-verification.md with the verdict line
   (uninformative / informative) against the spec's rule. Then stop and report.

## Task 2026-11-18-b: CS-22 part 1 with amendment A1 (closed: §30 CS-22 refuted; merged adf2319)

**Basis:** DECISIONS 2026-11-18, "Merge of §28–§29". **Judge, frozen:**
[../coldspray-hunch-cs22.md](../coldspray-hunch-cs22.md), with amendment A1 (in the commit that adds this task).
Cite it in every row. Run jobs one at a time. If anything beyond A1 is needed, stop and report.

1. **Fork changes (A1)** on branch `cs12`. A short design note first (fork SPEC-TL-b), then:
   - remove the `bond.Yp` lower bound;
   - let off-skin particles bond when Y′ < −1, for this setting only;
   - add `bond.t_on` with default 0.
   Leave `bond.pE` and the p_n,ij > p_E test unchanged. Build, then rerun T-A0, which must be bit-identical.
2. **Kill (a):** R/8 at 600 m/s.
   - The on branch: Y′ = −10⁶, p_E = 0, `bond.t_on` = 1 s (never active within the run).
   - The off branch: bond `none`.
   - Compare all written metrics. If any differs, CS-22 is refuted: stop and report.
3. **Kill (b):** off and on, with `bond.t_on` = 0.354 D/V = 11.8 ns (0.5 t_p; D/V = 33.3 ns), at R/8, R/16 and R/32. 600 m/s, to 2.0 D/V,
   on the §26 deck with P-HG-Al and δ_c = 31.25 nm.
   - Check R/32's memory before starting it. If it does not fit, CS-22 is inconclusive: stop and report.
   - Report e(off) at each mesh, and the bonded-pair count at t_end. Both are reported, not judged.
   Rows: `results/tl_cs22_*.csv`.
4. Write up as a new section of opencourant-verification.md on `coldspray/opencourant-sph`, with a verdict line
   against the frozen rule. Then stop and report.

## Task 2026-11-18-a: CS-21 part 1 and CS-22 part 1 (closed: §28 CS-21 refuted; §29 CS-22 stopped at the design note; merged a488f57)

**Basis:** DECISIONS 2026-11-18, "CS-20 and CS-21 registered" and "Track B reopened for the forked bond response".
**Judges, frozen:**
- [../coldspray-hunch-cs21.md](../coldspray-hunch-cs21.md);
- [../coldspray-hunch-cs22.md](../coldspray-hunch-cs22.md), frozen in the commit that adds this task.

Cite the hunch file and its commit in every row. Do not change the set-ups, parameters or rules. If something cannot
be run as written, stop and report. Run jobs one at a time (15 GB; §24 OOM).

1. **CS-21 part 1** (2D quads, fork binary `d0500106d`, the §25 deck):
   - six hardened twins (block A′ = 425.6 MPa) of the §25 runs, at 600 and 500 m/s × R/64, R/128 and R/256;
   - if the §25 field files are gone, also rerun the annealed decks with the same binary;
   - compute dq for the §27 drivers and disc Y − 1 as the hunch specifies, and apply its part-1 rule.
   Rows: `results/tl_cs21_*.csv`.
2. **CS-22 fork change** (fork branch `cs12`):
   - a short design note before any code: a key for the activation start time (e.g. `cs12.t_on`), and the low Y′
     value that gives f_B = 1 within 10⁻³ with p_E = 0;
   - then code and build, and a T-A0 rerun (bit-identical);
   - if cs12 rejects such a Y′, stop and report; do not write a new mode.
3. **CS-22 kill (a):** an R/8 on branch with t_on = ∞ against the R/8 off branch. Compare all written metrics. If they
   differ, CS-22 is refuted: stop and report.
4. **CS-22 kill (b):** off and on (t_b = 0.5 t_p = 0.354 D/V) at R/8, R/16 and R/32, 600 m/s, to 2.0 D/V, on the §26
   deck with P-HG-Al.
   - Check R/32's memory before starting it. If it does not fit, CS-22 is inconclusive: stop and report.
   - Report e(off) at each mesh as well. It is reported, not judged.
   Rows: `results/tl_cs22_*.csv`.
5. Write up both as new sections of opencourant-verification.md on `coldspray/opencourant-sph`, each with a verdict
   line against its frozen rule. Then stop and report.

Items 1 and 2–4 are independent. Item 1 is cheap (about 8 min engine time), so run it first.

## Task 2026-11-17-b: driver-convergence check, drivers 2–4 (post-processing) (closed: §27, merged 29c09ee)

**Basis:** DECISIONS 2026-11-17 "Driver check before the trigger run"; spec, rule and prediction in
docs/research/driver-check-2026-11-17.md, fixed before any number. Do not change the definitions or the rule; if one
cannot be computed as written, say so and report what was computed instead, labelled.

1. From the §25 quad runs (fork binary `d0500106d`; Al–Al 600 and 500 m/s; R/64, R/128, R/256), outputs from the third
   onwards up to t*, compute drivers 2–4 of the spec (W_ann, P_s, ring Y) for ℓ = 1.5 and 2.0 µm, each side. If the
   field files are gone, rerun the §25 decks with the same binary (about 8 min each).
2. Apply the spec's rule; report per driver, ℓ, ring, side and speed the fraction of converging points and whether
   it is usable.
3. Report the same drivers on the BCT-off TLSPH survival probe (§23.1, R/16 and R/32) if its outputs allow; reported
   only.
4. No solver changes. Rows `kind = calibration`, `results/tl_cal8_driver_*.csv`; schemeforge §27 on
   `coldspray/opencourant-sph`. Then stop and report.

## Task 2026-11-17-a: cs12 (Bay activation) on TLSPH, then a He/H₂ multi-particle illustration (closed: §26, merged 9b03f79)

**Basis:** DECISIONS 2026-11-17 "Track B continues with cs12 on TLSPH; illustration runs". The code serves Track B;
the illustration runs (`kind = illustration`) sit outside the ladders and support no claim. Each step commits its
plan and prediction in the fork before its runs. Stop and report after any failure. Run jobs one at a time (15 GB;
§24 OOM). Task 2026-11-16-a item 4 (trigger run) stays waiting on Peter's D2 decision.

1. **Branch** `cs12` from fork `tlsph` f226cd4.
2. **Design note `hvi/CS12-DESIGN.md`** (short, no code):
   - activation per SPEC §4.6: a pair bonds when Y_ij > Y′ and p_n > p_E. Y_ij from the TLSPH skin: the
     facet-area-weighted Y of each partner's facets, the minimum of the two partners; p_n the per-particle sum (O13);
   - bonded fraction f_B = (Y − Y′)/(1 − Y′), kept as a running maximum; σ_B(t) = f_B·σ_flow(T(t)) (O3/O14);
   - cohesive law and damage per SPEC §4.7;
   - output in the interface file: bond state, damage, and an "oxide broken" flag (Y > Y′) per skin facet;
   - what is fed back: activation only; the skin does not feed contact forces.
3. **Build.** `bond.model = none` and `tie` bitwise neutral against `f226cd4`'s binary; T-A0 55 of 55.
4. **Checks (reported, not frozen):** D-3 and D-4 of the sph-contact ladder (docs/research/sph-contact-ladder.md).
5. **Survival check:** one Ti-6Al-4V particle of 20 µm on Ti-6Al-4V at 1584 m/s, R/16, quarter model, to 1.0 D/V,
   with `cs12`, against the E-1 gate draft §3 survival checks. Johnson–Cook and EOS parameters for Ti-6Al-4V from a
   cited primary source (not a blind-list paper; say which). If it fails, stop and report.
6. **Illustration runs** (only if step 5 passes):
   - full 3D (no symmetry plane), about 5 particles per side, staggered positions and arrival times, R/12–R/16;
   - side A He/N₂ at 1347 m/s, side B H₂/N₂ at 1584 m/s (Peter's 1D nozzle model, equal stagnation conditions),
     everything else identical;
   - `bond.model = cs12` with placeholder Y′ and p_E chosen so the ring is visible; state the values;
   - construction F2 (frozen, fork 0b58b6a46), BCT off, CS-18b set-up.
7. **Rendering** under `hvi/illustration/`: mid-plane section through the particles, colour by plastic strain (same
   scale both sides); skin facets marked where the oxide breaks (Y > Y′); bonded interface drawn, damaged bonds
   (damage = 1) as a gap or dark band. Frames and an MP4 per side, plus a side-by-side MP4. Report cost and any stop.

## Task 2026-11-16-b: P3 probe, interface averages in plastic jetting impact (2D axisymmetric quads) (closed: §25, merged 5ab274d)

**Basis:** DECISIONS 2026-11-16 "After the odds review". Question: do 0.5 µm surface averages of p_n and Y − 1
converge under refinement in a plastic, jetting impact, before the jet root collapses? A calibration diagnostic, no
route verdict; the outcome goes to Peter. Run it at low thread count beside task 16-a; 16-a has priority.

1. **Deck:** the §8 deck (OpenCourant 2D axisymmetric, `Isolid = 17`, Lagrangian, Johnson–Cook plus Grüneisen with
   the sourced γ₀ = 2.17), Al–Al, 600 m/s; add 500 m/s if 600 m/s collapses before 10 % of the penetration time on
   the finest mesh. Meshes R/64, R/128, R/256 (the §8 mesh family, contact as in §8).
2. **Quantities:** contact pressure p_n and surface expansion Y − 1 (from the surface element edge stretch, radial
   times hoop) averaged over 0.5 µm surface discs centred at 0.25 a, 0.5 a and 0.75 a of the current contact radius,
   particle side and substrate side, as time histories up to the earliest jet-root collapse time of the three meshes,
   reported against penetration fraction. Edge point values reported only.
3. **Reading rule (commit it with the prediction, before any run):** at a disc and output time the averages
   "converge" if |q256 − q128| ≤ 3.5 % of |q256| and either |q256 − q128| ≤ 0.8 |q128 − q64| or
   |q128 − q64| ≤ 3.5 % of |q128|. Report the fraction of disc-time points that converge per quantity and side, and
   the penetration fraction at which convergence is first lost at each disc.
4. **Report** the collapse time per mesh, the cost per run, and anything that stopped a run. Rows
   `kind = calibration`, `results/tl_cal6_p3_*.csv`; schemeforge §25 on `coldspray/opencourant-sph`. Then stop.

## Task 2026-11-16-a: contact-particle interface file, momentum-restoring VCI, then the trigger run (closed: items 1–3 done, §24; item 4 dropped, Track B route closed 2026-11-17)

**Basis:** §23 and DECISIONS 2026-11-16 "After §23: reference accepted as is; momentum-restoring VCI". F2 stays the
frozen default (fork 0b58b6a46). The trigger run is **not** part of this task. Rows `kind = calibration`; results
to schemeforge §24 on `coldspray/opencourant-sph`.

1. **Interface file (outstanding from task 2026-11-15-b step 1.3).** List the particles actually in contact at each
   output time, on both bodies, not the static surface set. Show on T-S1 R/32 and on the T-B2 deck **without the skin
   averages being evaluated** (count of contact particles per body against time, force share outside the listed set).
   Do not compute the trigger quantities on T-B2.
2. **Momentum-restoring VCI (VCI-DESIGN §6).** Commit its plan and prediction in the fork first. Build it, show
   VCI off is bitwise neutral, and judge it by the **same** gate and selection criterion (VCI-DESIGN §8) on the same
   non-trigger cases as §23 (columns, flat free surface, case 5 at R/32 and R/64, T-S1 skin p_n at R/64), against
   F2's S = 0.369.
   - If it passes the gate and has the lower S, it is the candidate; freeze it in the fork and **stop**: its D2
     change (the skin becomes part of the operator) needs Peter's approval before any trigger run.
   - Otherwise F2 stands; report and stop.
3. Report the momentum drift at R/32 and R/64 and the net VCI force as in §23.

**Amended 2026-11-16 (later; DECISIONS "After the odds review"):**
- **Time box for item 2:** two working days from its start. If the variant has not passed its gate by then, stop
  it, report what ran, and F2 stands.
- **Item 4, the trigger run (D4 as amended 2026-11-15 and 2026-11-16).** After item 2 (or the time box):
  - host: TLSPH, CS-18b set-up, BCT off, skin, and the frozen construction: F2 (fork 0b58b6a46), or the VCI variant
    only after Peter has approved its D2 change;
  - T-B2 elastic deck, R/32 on the full block and R/64 on the reduced block, with the contact-particle interface file
    of item 1;
  - commit the plan, the binary and the prediction first. The prediction states the clause-2 noise floor (clause 2
    applies only where |e(R/32)| exceeds that quantity's 3.5 % + U_ref) and the reviewers' expected fire
    (sphere-side Y − 1);
  - report the eight 0.5 µm surface averages (p_n and Y − 1; axis and 0.5 a; block and sphere side, at the force
    peak) at both resolutions, each error against quad R/256 with its U_ref from §23, and for each of clauses 1 and 2
    whether it fires. Report; the modeller records the rule outcome.

## Task 2026-11-15-b: reference, energy, survival, flat face and skin before the trigger run (closed: §23, merged; step 1.3 moved to 2026-11-16-a)

**Amended 2026-11-15 (later):** D3 was reopened after WSL B's boundary-integration reading (b11; DECISIONS
2026-11-15 "D3 reopened after the boundary-integration reading"). Steps 1 and 2 are unchanged. **Step 3 is replaced
by step 3′ below**; the original step 3 text is kept for the record.

**Step 1 (in parallel; any order):**
1. **Quad reference and U_ref.**
   - The quad axisymmetric two-body run of §22 (T-B2, same block sizes: full and reduced) at R/256, beside the
     existing R/64 and R/128.
   - Extract on the contact surface, at the force peak, 0.5 µm disc averages on the axis and at 0.5 a, block and
     sphere side: p_n, and the surface expansion Y − 1 from the stretch of the surface element edges
     (axisymmetric: radial edge stretch times hoop stretch).
   - Report per quantity U_ref = |quad R/128 − quad R/256| (for Y as a relative error on Y − 1), the observed order
     and a Richardson estimate where the order is stable.
   - If any U_ref > 1.75 %, say so and stop this item: the trigger cannot be evaluated until the reference improves
     (DECISIONS, D4).
2. **TLSPH internal energy.**
   - Accumulate per particle ΔE_int = V₀ P : ΔF each step, and report the hourglass work, the viscous work (from
     pair relative velocities) and the contact penalty energy separately.
   - Check the balance KE + E_int + E_contact + dissipated work against KE0 on T-S1 at R/32 with BCT off, and on the
     T-S0 column. Report the closure, no threshold.
   - Also rerun T-S1 at R/32 with BCT on and report its budget: the 0.33 + 0.15 KE0 at rebound 0.860 is listed as
     "not understood" (state report). Diagnosis only.
3. **Interface file.** List the particles actually in contact at each output time, not the static surface set
   (§22 open item).

**Step 2 (after the internal energy of step 1.2): BCT-off survival probe = trigger clause 3.**
- Commit the prediction first.
- The §19.5 deck (Al–Al quarter model, 800 m/s, contact only, t_end = 1.0 D/V) at R/16 and R/32, with `tl.bct = off`.
- Report against the E-1 gate draft §3 survival checks exactly as §19.5 did, plus the energy balance now available
  (reported).
- **If any survival check fails, the trigger has fired:** stop the task and report. No variant, no rerun with other
  settings.

**Step 3 (only if step 2 passes): fitted flat face, then the skin.** Calibration on cases other than the trigger deck.
1. **Fitted flat face.** Build the block's top face like the conforming sphere: a fitted outer layer over the lattice
   with adjusted mass (§19, conforming sphere construction).
   - State the construction and its selection criterion in a commit before its calibration runs; if more than one
     construction is tried, the criterion picks one.
   - Calibrate on the 2L column against the rigid wall and against the deformable TL column (layers 1–4 against the
     momentum-rate plateau), and on the flat free surface under load (T-surface b).
   - Freeze the chosen construction (commit) before stopping.
2. **Measurement-only skin.** A triangulated surface over the boundary particles of each body, moved by the
   particles, with Y per facet from the area stretch and p_n per facet from the penalty forces over the facet area.
   - It feeds nothing back: show that a run with the skin on is bitwise identical in particle state to the same run
     with it off.
   - Calibrate on the flat free surface under uniform load (known p_n and Y), on the column, and on T-S1 at R/32 and
     R/64 (p_n against the FE reference on the axis and at 0.5 a).
   - 0.5 µm surface-disc averages as in D2.

**Step 3′ (replaces step 3; only if step 2 passes).**
1. **VCI design note, no code** (`hvi/` design note in the fork, summary in §23). Basis:
   `docs/research/data/boundary_integration_reading.md` (E, items 3–4: Hillman 2013 §4.1.2, §6.1.3). State:
   - the surface quadrature (points, normals, weights) and the surface Ψ_I chosen for TLSPH (Shepard or RK);
   - ξ_I computed once in the reference configuration, and how the Petrov–Galerkin term enters `tl_mod.F90`;
   - how penalty contact applies its traction through the surface facets instead of point forces on layer 1;
   - the expected size of the linear-momentum loss, and how it would be monitored;
   - the interaction with hourglass control (the §22 layer split depends on α);
   - cost and code size; what would make it unworkable.
2. **Selection criterion, committed before any calibration run:** how one construction (fitted flat face or VCI)
   is chosen on non-trigger cases (column against rigid and deformable walls, flat free surface under load, T-S1).
   Stop and report after the note and the criterion: Peter confirms before any VCI code is written.
3. Then, per Peter: build and calibrate the candidate(s), choose by the committed criterion, freeze the chosen
   construction, and build the measurement skin (as in the original step 3.2; under VCI the skin also carries the
   contact load, which needs Peter's approval at the trigger-run freeze).

**Then stop and report.** The modeller drafts the trigger-run task (frozen binary, decks and predictions) from §23.

## Task 2026-11-15-a: is BCT needed at the 0.5 µm scale? (closed: rule not met, §22)

**Basis:** §21 and DECISIONS 2026-11-15. Every BCT form misbehaves on small or changing loaded patches, which is
the cold-spray contact regime. BCT off is clean on curved and body-on-body contact, but the column end layers carry
0.62 / 0.86 of the stress. The interface outputs are judged as 0.5 µm averages (DECISIONS 2026-11-14), and at R/32
two layers are about that length. This task measures whether the BCT-off deficit matters at that scale.
**Set-up:** the CS-18b set-up with `tl.bct = off`, binary `8188ca5ec` (or `18ffc51c1` with the default rule).
Rows `kind = calibration`. Commit the prediction before the runs. Stop and report.

1. **Sphere on block, body-on-body (T-B2 deck), R/32 and R/64,** hvi contact with `contact.stfac = 3`.
   - At the time of peak force, and averaged over 0.4–0.6 t_H: contact pressure p_n and normal stress σ_zz on the
     block side and the sphere side, averaged over discs of 0.5 µm radius on the axis and at 0.5 a, and over depth
     bands of 0.5 µm from the contact (first and second band).
   - Compare with the two-body Hertz field, and with the quad axisymmetric two-body run of task 2026-11-13-c item 3
     (same averaging) as the numerical reference.
   - Also report the layer-1 and layer-2 point values and the contact-area radius.
   - State the particle size used to convert 0.5 µm into spacings.
2. **The column check (2L at V/2) loaded by a deformable wall instead of the kinematic rigid wall:** a TL or
   collocated block through hvi penalty contact, BCT off. Report layers 1–4 against the momentum-rate plateau.
   Is the 0.62 / 0.86 deficit a rigid-wall artefact, or does it come with any point-loaded face?
3. **Decision rule (fixed before the runs, DECISIONS 2026-11-15):**
   - if the 0.5 µm averages in item 1 are within 3.5 % of the reference at R/32 and R/64, CS-18c will be the CS-18b
     set-up with BCT off;
   - otherwise this counts as the next failure, and Peter's review session comes before any further BCT variant.
4. **Results:** fork `hvi/results/tl_cal4_*.csv`; schemeforge §22 on `coldspray/opencourant-sph`. Then stop.

## Task 2026-11-14-c: BCT under non-uniform and curved loads (closed: done, §21, merged 7073f1e)

**Basis:** §20.4–20.5 and DECISIONS 2026-11-14 "CS-18c: TL with a corrected BCT, not a switch to UL SPH". With BCT
off, T-S1 at R/32 gives a rebound of 0.9988; with BCT on it gives 0.860, and at R/64 0.9788. The TL bodies with the
CS-18b viscosity and α handle curved contact. The defect is BCT's coupling to the load on a curved patch with few
particles. BCT cannot be dropped: without it the end layers carry 0.65 / 0.84 of the stress (§17, §19.2).
**Status of the cases:** this is calibration for a hunch not yet drafted (CS-18c). T-S1 is now a known case, and it
will be a non-blind rung of the CS-18c ladder. Rows `kind = calibration`. Commit a prediction before each group of
runs. Stop and report at the end.

**Leading hypothesis (cloud, untested):** the rigid wall is kinematic (the wall particle is stopped, force = m Δa).
BCT spreads that force over the end layers, and the §19.2 amendment then scales the load so that the wall particle
still receives its full stopping force. This is exact only for a uniform load on a flat face. On a curved patch, and
when particles enter and leave contact, the two disagree, which shows up as the 1.485 × wall-output mismatch, the
chatter and the energy exchange. Under the hvi penalty contact (body on body, what cold spray uses) there is no
kinematic constraint to fight, so BCT may already behave there.

1. **Static and code analysis.** Where exactly does the wall scaling misload a curved patch, or one that changes
   from step to step? Compare it with BCT spreading a penalty force. One page in the fork's SPEC-TL-b.
2. **Body-on-body probe first** (the most decisive and the cheapest): the T-B2 geometry (Hertz sphere on a TL
   block, hvi contact, `contact.stfac = 3`), R/32, BCT on and off, the CS-18b set-up otherwise. Report peak,
   approach, rebound, chatter (contact segments), viscous and hourglass work. This is a calibration run of a T-B2
   deck: name it as such in the rows.
3. **A BCT variant**, chosen from 1 and 2 (WSL A proposes; examples: a penalty wall for TL bodies in place of the
   kinematic wall; per-particle wall loads without the global stopping-force scaling; BCT only on patches above a
   stated particle count, with a stated rule). One variant, fixed and committed before its runs:
   - T-S1 at R/16, R/32 and R/64;
   - the §19.2 column check (layers 1–4 within 1 % of the momentum-rate plateau);
   - the flat free surface under load (§18.4 deck, T-surface b);
   - the conforming-sphere layer-2 check of §19.1 (static model): does the variant change the 26–30 % deficit?
   - T-A0 (no TL body: identical).
4. **Also, for the CS-18c ladder:** the T-S1 peak reference (1.073, JAX §9.6). All hosts tend to 1.02–1.05 at R/64
   (collocated 1.027, S′ 1.019, TL 1.040), and the quad two-body peak is 1.047. Check the reference's resolution
   and, if needed, give a converged value. This is a reference check, not a change to any verdict.
5. **Results:** fork `hvi/results/tl_cal3_*.csv`, SPEC-TL-b updated; schemeforge §21 on `coldspray/opencourant-sph`.
   Then stop.

## Task 2026-11-14-b: T-S1 at R/64 and one BCT-off diagnostic (closed: done, §20.4–20.5, merged c329481)

**Basis:** CS-18b refuted at T-S1 (DECISIONS 2026-11-14). Peter is moving towards an updated-Lagrangian SPH hunch
(CS-19, drafted by the cloud session). This task only answers whether BCT is carried into that draft. **It is not a
rescue of CS-18b, and not a diagnostic campaign:** two runs, one table, no further runs without a new task.
**Binary:** the same as task a (clean tree `8188ca5ec`), deck switch `HVI_TL_SET=cs18b`; wall forces from the
momentum rate.

1. **T-S1 at R/64:** let the running case finish and add its row and numbers to §20.4, labelled "reported, after the
   verdict" (it cannot change the CS-18b verdict).
2. **One diagnostic run:** T-S1 at R/32 with `tl.bct = off`, everything else as task a.
   - Rows `kind = diagnostic`, no verdict; `binary_state = committed`, fork SHA, deck hash.
   - Commit a one-line prediction in its own commit before the run.
   - Report the same quantities as the §20.2 table: contact at 10⁻² (first drop and last time above), peak,
     approach, rebound, largest and final KE / KE0, smallest det F, number of contact segments, viscous and
     hourglass work.
3. **Reading rule, fixed now (before the run):**
   - rebound ≥ 0.9796 with BCT off: the wall–BCT coupling is the main cause, so BCT is **not** carried unchanged
     into CS-19 for curved contact;
   - rebound < 0.9796 with BCT off: the TL bodies (or the viscosity/hourglass set-up) fail curved contact on their
     own, so BCT is not shown to be the cause; CS-19 may carry BCT, and must test it at T-S1;
   - either way the row is a diagnostic, and nothing is tuned on it.
4. **Results:** fork `hvi/results/tlb_diag.csv`; §20.4 and a short §20.5 on `coldspray/opencourant-sph`. Then stop.

## Task 2026-11-14-a: CS-18b core rungs (closed: T-S1 FAIL, CS-18b refuted, §20, merged 7984e1c)

**Judge, frozen:** [../sph-tlsph-b-ladder.md](../sph-tlsph-b-ladder.md) and hunch
[../coldspray-hunch-cs18b.md](../coldspray-hunch-cs18b.md), frozen in 6f0786a. Cite it in every row.
**Binary:** fork `tlsph`, solver source of 43791edbc (as in the ladder's set-up), built from a clean tree.

1. **Core rungs, in the frozen order:** T-A0, T-S0, T-S0p, T-S1, T-tension, T-zero-energy, T-surface, T-B1, T-B2,
   T-B3, T-survival, T-C1, T-D1, T-D2. T-D3 waits for A3.5.
2. **Metrics under BCT:** every wall force is read from the body's momentum rate (ladder, "Metrics under BCT").
   Rung scripts that read `/TH/RWALL` must be switched before the runs; the switch is a script commit that comes
   before the predictions.
3. **Reported rungs,** labelled, whenever convenient:
   - T-surface-sphere;
   - T-large-strain-1 and -2;
   - T-cost;
   - energy closure;
   - BCT guard fallbacks (count and location) in every impact run.
4. **Rules:**
   - commit the source and decks before each campaign;
   - commit each prediction in its own commit before its runs;
   - every row records `binary_state = committed`, the fork SHA, ladder 6f0786a and the deck hash;
   - a failing core rung means stop and report to Peter, with no tuning;
   - if T-survival fails, stop TLSPH without a reference update (CS-18b kill clause).
5. **Results:** fork `hvi/results/tlb_*.csv`; schemeforge §20 on `coldspray/opencourant-sph`, with a verdict table per
   rung and the reported rungs kept apart.

## Task 2026-11-13-c: CS-18b calibration part 2 and BCT implementation (closed: done, §19, merged b5a4424)

**Basis:** DECISIONS 2026-11-13 "CS-18b calibration decisions" and §18.
**Rules (as task b):**
- this is still before the freeze; no TLSPH rung deck is used to choose anything;
- predictions and criteria are committed before their runs;
- rows `kind = calibration`, with fork SHA (committed binary) and deck hash.

1. **BCT on the conforming sphere** (static model, no engine run).
   - The BCT weights of §18.4 on the conforming sphere at R/16, R/32 and R/64, for contact patches of 3 to 10
     spacings in radius.
   - Report:
     - the sign and conditioning of Σ φ (B·n), with a proposed guard threshold;
     - the uniformity of the layer stresses under a Hertz-like pressure;
     - the torque error per pair and in total.
   - **If no robust guard exists, stop here and report.**
2. **BCT implementation** in the fork: a TL-only step after the hvi contact and wall forces; the hvi code is
   unchanged. Then:
   - T-A0 again (no TL body: identical);
   - a non-rung check: a confined TL column of length 2L at V/2 with BCT. The steady stresses of layers 1 to 3 should
     be within 1 % of the plateau.
3. **Quad two-body Hertz** (Isolid 17, axisymmetric, the B-2 geometry):
   - a deformable sphere on a deformable block, elastic, 20 m/s, at the finest affordable meshes, with convergence
     shown;
   - peak, approach and rebound against two-body Hertz. These are the quad errors for the T-B2 limits (quad error +
     3.0 points, rounded up to the next 0.5 %).
4. **α recalibration** with the LAMMPS viscosity (Q1 = 0.05, Q2 = 0), on non-rung cases: the free bar of §18.3, and
   a free block with a smooth initial field at a size other than T-zero-energy's.
   - Criterion, stated before the runs:
     - no resolved wave faster than exact (the SPEC-TL §3.5 rule);
     - the share of shortest-wavelength energy ≤ 1 %;
     - then the least dissipation.
   - Report α, and whether Q1 should change (re-run §18.3's criterion if it does).

5. **Survival probe** (added 2026-11-13, DECISIONS "CS-18b hold lifted"; a calibration-phase diagnostic, no
   verdict). Run it after item 2 (BCT implemented).
   - **Set-up:** TLSPH with the §18 set-up (LAMMPS viscosity Q1 = 0.05, α as recalibrated in item 4 or 10 if item 4 is
     not done yet, BCT).
   - **Case:** Al–Al quarter model, 800 m/s, R/16 and R/32, contact only (`bond.model = none`), t_end = 1.0 D/V.
   - **Judged by** the survival checks of the E-1 gate draft §3:
     - dt ≥ 0.1 of its initial value;
     - detached mass ≤ 1 %;
     - no cross-body pair closer than 0.5 s;
     - no det F ≤ 0 and no ill-conditioned-matrix stop;
     - energy reported, not judged.
   - **Also report:** how far beyond the kinematic switch (0.002–0.019 D/V) the run gets, the smallest det F, the
     largest stretch, and the time step history.
   - **The prediction** is committed in its own commit before the runs. Rows `kind = calibration, diagnostic`.

**Output:** fork `hvi/SPEC-TL-b.md` updated and `hvi/results/tl_cal2_*.csv`; schemeforge §19 on
`coldspray/opencourant-sph`. Then stop.

## Task 2026-11-13-b: CS-18b calibration and design (closed: done, §18, merged 3a89b1c)

**Basis:** DECISIONS 2026-11-13 "CS-18b with a calibration phase before its freeze". The T-S0 diagnosis is in §17.
This is the phase **before** the CS-18b freeze: tuning on the calibration cases below is allowed and recorded. The
TLSPH rungs themselves (the decks of `sph-tlsph-ladder.md`) are not used to choose anything.

**Rules:**
- source committed before each campaign;
- rows `kind = calibration`, with fork SHA (committed binary) and deck hash;
- no verdicts.

**(a) Finite-strain references.** For T-S0, T-S0p and T-tension, derive the exact 1D solution including finite
strain:
- the plateau stress and front speed for the solver's hypoelastic material at the deck's velocity (the offset
  0.42·V/c_d found in §17 is a check, not the definition);
- check it against the quad elements (Isolid 17) and against TL runs at V/2 and V/4 (from §17).

Write the reference formulas into the fork's `hvi/SPEC-TL-b.md`.

**(b) Threshold calibration.** Run the quad elements (Isolid 17, 2D) and collocated SPH (frozen §9.1 set-up) on the
T-S0, T-S0p and T-S1 decks at the ladder's resolutions, measured against the references of (a).
- Propose each CS-18b threshold as a stated margin over what these methods achieve.
- Every growth clause gets a noise floor.
- For B-2 and T-surface, propose a threshold with its reason.

**(c) Viscosity.** Take one viscosity form from the literature, for example the LAMMPS SMD TLSPH viscosity
(Ganzenmüller) or Monaghan with a switch, read from the source and cited. Choose its coefficients on calibration
cases that are **not** ladder rungs:
- a confined column at a different length (2×) and velocity (V/2);
- a free elastic bar ringing in its first mode, judged by damping per period.

The criterion is stated before the runs: stable without ringing, and the least dissipation.

**(d) End-layer stress design note.** In the steady state the TL end layers carry 0.655 and 0.845 of the true stress
(§17.2).
- From the literature, find why a corrected-gradient formulation does this at a truncated neighbourhood, and what
  corrects it. Candidates: corrected pair-force sums, boundary integral terms, ghost or mirror layers at free
  surfaces.
- Propose a fix (new code, described, not implemented) or argue for none.
- Define a rung **T-surface:** the steady stress of the first two layers against the traction, in the T-S0 column
  and at a free surface under load, with its threshold from (b).

**Output:** fork `hvi/SPEC-TL-b.md` and `hvi/results/tl_cal_*.csv`; schemeforge §18 on `coldspray/opencourant-sph`.
Then stop. The cloud session drafts CS-18b and its ladder from this output, and Peter approves the freeze.

## Task 2026-11-13-a: T-S0 diagnosis (closed: done, §17, merged 7638d1a)

**Why:** CS-18 is refuted at T-S0 (§16; DECISIONS 2026-11-13). Before Peter decides on a CS-18b, find out which
part of the set-up sets the contact-time and rebound errors, and whether the plateau offset is finite strain.

**Rules:**
- no solver code changes; deck and sidecar switches only;
- each case changes one thing against the frozen set-up;
- each prediction is committed in its own commit before its runs;
- rows are marked `diagnostic`, carry the fork SHA (committed binary) and the deck hash, and never a verdict.

**Deck:** the T-S0 column (h = 1.12 s, 4 wide), at 100 and 200 particles unless stated otherwise.

| Case | Change |
|---|---|
| D-visc-off | viscosity off (q_a = q_b = 1e-30); report if unstable |
| D-visc-P | Profizi's linear 0.8 / quadratic 4 |
| D-hg | α = 0, and α = 20 |
| D-vel | V/2 and V/4, at 200 particles (a finite-strain offset should scale with V) |
| D-width | width 16, at 100 particles (no effect expected with complete images) |
| D-layer | post-processing only: plateau stress per layer; where the +21 % start spike sits (first layers or bulk); the same for the collocated order-1 run of §15.9 |

**Report per case:** plateau, contact time, rebound, viscous and hourglass work as shares of the initial kinetic
energy, and the start spike. Then a short reading:
- which item sets the contact-time and rebound errors;
- whether the plateau offset is finite strain;
- whether the start spike comes from the end-layer correction.

**Results:** fork `hvi/results/tl_diag_s0.csv`; schemeforge §17 on `coldspray/opencourant-sph`. Then stop.

## Task 2026-11-12-c: TLSPH implementation and core rungs (closed: stopped at T-S0, §16; CS-18 refuted)

**Basis:**
- **Judge, frozen:** [../sph-tlsph-ladder.md](../sph-tlsph-ladder.md) and hunch
  [../coldspray-hunch-cs18.md](../coldspray-hunch-cs18.md), frozen in 583912a. Cite it in every row.
- **Design:** fork `sph-hvi-contact`, branch `tlsph`, `hvi/SPEC-TL.md` at 3e9aa6b. A change to the ladder's set-up
  after the freeze is an addendum labelled post hoc, and goes to Peter first.

1. **Implementation, in SPEC-TL §6 order.** Report each step's check in the fork CHANGELOG.
   1. Sidecar keys (`tl.*`) and fatal checks → T-A0 (no TL body: bit-identical).
   2. Reference lists with complete images; the correction matrix; the first-cycle self-check (completeness sums,
      image counts, the `tl.cond_max` and `tl.smin_min` stops).
   3. Kinematics and force without hourglass and viscosity; the one-cycle uniform-stretch check.
   4. Hourglass force, viscosity, energies and diagnostics (smallest det F, principal stretches, plastic strain,
      hourglass energy).
   5. hvi attachment (SPEC-TL §5, hvi code unchanged).
2. **Core rungs, in the frozen order:** T-A0, T-S0, T-S0p, T-S1, T-tension, T-zero-energy, T-B1, T-B2, T-B3,
   **T-survival**, T-C1, T-D1, T-D2. T-D3 waits for A3.5. The reported rungs (T-large-strain-1 and -2, T-cost)
   whenever convenient, labelled.
3. **Rules:**
   - commit the source and decks before each campaign;
   - commit each prediction in its own commit before its runs;
   - every row records `binary_state = committed`, the fork SHA, the ladder commit 583912a and the deck hash;
   - a failing core rung means stop and report to Peter, with no tuning;
   - **if T-survival fails, stop TLSPH without a reference update** (CS-18 kill clause).
4. **Results:**
   - fork `hvi/results/tl_*.csv`;
   - schemeforge `coldspray/opencourant-sph`, with a new **§16** in opencourant-verification.md (a verdict table per
     rung, diagnostics kept apart).

## Task 2026-11-12-b: freeze preconditions for the TLSPH ladder (closed: tl.cond_max 30, tl.smin_min 0.025 at fork 3e9aa6b; journal check deferred by Peter)

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
