# Cold spray: hunch CS-23 (forked bond response with sticking bonds), registration (frozen)

Drafted 2026-11-22 by claude (DECISIONS 2026-11-22, "Bonded pairs stick under compression"), after WSL A task
2026-11-22-c (energy-consistent cap shrink) was merged (§38, engine `38639859c`).

Status:
- **Registered and frozen 2026-11-22, approved by Peter** ("Freeze"), as drafted in ba4bcb3, before any CS-23 run.
  The freeze adopts the two items of "Proposed before the freeze" (W_s validity check; swept-pair wording) into the
  rule below. Budget 4 of 5. WSL A task 2026-11-22-d.
- **Post hoc by construction**, as CS-22b: the set-up, ladder and rule were chosen after §30, §31 and §36–§38 were
  seen. Nothing is chosen after a CS-23 run is seen.

**Why:** CS-22b is supported at δ_c 30× (§31), but the slip check (§36, mixed) and §37 showed that its tear/hold
outcome depends substantially on slip accumulated while compressed, which cs12 allowed because a bonded pair carried no
shear for g ≤ 0. The old law even booked G_c·A at reopening without work input (§37). CS-23 asks whether the forked
bond response still converges when bonded pairs stick, as a metallurgical bond should (shear up to τ_B = σ_B/√3).

**Facts checked (coldspray-procedure.md), updated 2026-11-22 after §38:** solver-facts §3 (TLSPH heats and softens;
costs; candidate-list release; lost-bond check a lower bound; stuck-particle e = target motion) and §4 (cs12
activation; `bond.stick`, `out.pairs`, 17-slot records; old-law energy finding; energy-consistent stick law on engine
`38639859c`; R/32 with stick on and `out.pairs` about 14.8 GiB of 23.5 GiB). **Not covered — never read/used before;
check the output first:** (i) the per-pair file v2 (16 fields) in an impact run; (ii) stick on with bonded
symmetry-ghost pairs (the quarter model has them; ghost weighting ½ checked by code reading only, §38); (iii) the
pair-level lost-bond check (new post-processing). s_pl > 0 at re-compression is expected for tilted pairs (§38 S3),
not an error.

```yaml
- id: CS-23
  registered: frozen 2026-11-22 (Peter: "Freeze")
  assumption_broken: >-
    As CS-22/CS-22b, and in addition: that CS-22b's support depends on bonded pairs sliding freely while compressed.
  statement: >-
    With bonded pairs sticking under compression (bond.stick = on), run the CS-22b set-up. For at least one delta_c in
    the ladder, the rebound difference dR = e(on) - e(off) converges under refinement and |dR32| >= 0.01.
  mechanism: >-
    As CS-22: up to t_b the branches are one computation, so errors made there cancel in dR. With sticking bonds the
    tear/hold outcome is set by the bond's strength and energy in opening, not by slip accumulated while compressed, so
    a converging dR would reflect the bond rather than the slip artefact.
  parameters: >-
    Fixed at the freeze; drafted now.
    - As CS-22b (coldspray-hunch-cs22b.md, c8a6c5c): the §30 deck (quarter model, CS-18b TL settings, BCT off, F2,
      stfac 3), P-HG-Al, R = 10 um, V = 600 m/s, t_end = 2.0 D/V; cs12 with Y' = -1e6, p_E = 0, bond.t_on = 11.78 ns;
      delta_c ladder 3x, 10x, 30x (0.09375, 0.3125, 0.9375 um); meshes R/8, R/16, R/32; e as in CS-22.
    - New: bond.stick = on; out.pairs on; engine = fork cs12 `38639859c` (binary ~/oc_runs/ocroot_38639859c, §38).
    - Off branch: the §30 off runs (stick does not act without a bond; neutrality of the new engine shown in §37 and
      §38).
    - Lost-bond check as CS-22b, now at pair level from out.pairs: a pair that leaves "bonded" by neither tearing
      (D reaching 1 under the law) nor a sweep from the candidate list (§31 item 1) is lost; any lost pair makes the
      run invalid for that delta_c. A pair swept with D < 1 just before the sweep is reported (count, delta/delta_c
      at the sweep) and does not invalidate the run.
    - W_s validity check on the first R/8 on-run (before any other on-run is read): the per-pair W_s summed over the
      out.pairs records equals the interface file's global W_s to 1e-10 relative at every record; if not, stop and
      report before any dR is read.
    - Stage gate as CS-22b: R/8 and R/16 first; R/32 for a delta_c only if both are valid, reach t_end (or the stuck
      exception) and |dR16| >= 0.01; at most 3 R/32 runs; memory checked before each (VM 23.5 GiB; estimate
      14.8 GiB, §38).
  predicted_effect:
    - {metric: "dR on R/8, R/16, R/32, for at least one delta_c", direction: same,
       size: "converges by the driver-check §3 rule, |dR32| >= 0.01"}
  kill_criterion: >-
    Per delta_c, exactly as CS-22b: refuted if it fails the stage gate on |dR16| or on reaching t_end, or |dR32| < 0.01,
    or not (|dR32 - dR16| <= 3.5 % |dR32| and (|dR32 - dR16| <= 0.8 |dR16 - dR8| or |dR16 - dR8| <= 3.5 % |dR16|)).
    Inconclusive for that delta_c if a run is invalid by the lost-bond check, fails before t_end without the stuck
    exception, or R/32 does not fit. Externally killed runs are rerun (DECISIONS 2026-11-21).
    CS-23 supported if at least one delta_c passes; refuted if every delta_c is refuted; otherwise inconclusive.
    Reported, not judged: per-pair delta_t at tearing against delta_c; s_pl and W_s; the energy balance including
    W_s; for a stuck particle, e(on) as target motion (§31); W_proj against W_s; s_pl gained at re-compression;
    swept pairs (count, delta/delta_c at the sweep).
  known_relatives:
    - CS-22b (same set-up; free slip while compressed)
    - §36 slip check (mixed), §37 old-law energy finding
    - sticking friction / bonded-interface shear limited by the shear flow stress (metal forming, textbook)
  label: none yet (referee); never "novel"
  status: frozen
  author: claude (draft), Peter (decision to make bonds stick)
```

## Author's prediction (judgment, recorded 2026-11-22 with the draft; superseded by the reassessment below)

- **Supported: 0.45.** For: sticking removes the slip that tore most 3× and 10× bonds, so more δ_c values may hold
  on R/16 and R/32. Against: a stuck particle's e(on) is target motion, so dR leans on the same near-cancellation as
  CS-22b; R/8 may still tear.
- **More δ_c values hold than in CS-22b** (at least one of 3× or 10× holds on R/16): 0.6.
- **30× passes again: 0.5.**
- **Tears that remain are opening-driven** (per-pair δ_t at tearing mostly below 0.2 δ_c): 0.6.

## Proposed before the freeze (2026-11-22, after §38; adopted into the rule at the freeze)

- **Ghost-weighting validity check:** on the first R/8 on-run, the per-pair W_s summed over the pairs file must equal
  the global W_s in the interface file to 1e-10 relative at every record. If not, stop and report before any dR is
  read (covers not-covered item (ii)).
- **Reported, not judged (addition):** W_proj total against W_s, and s_pl gained at re-compression (§38 S3).

## Odds reassessed 2026-11-22 before the freeze (Peter: "Assess our probabilities first")

Judgment, not a judge result. Written after §38, before any CS-23 run. No blind review (Peter's choice).

**Track record.** 17 recorded binary predictions on this track:
- Sources: §31 "Against the predictions" (author and fork), CS-22 (a)/(b), the slip check, the TLSPH temperature
  check (b)/(c), the softening check (two), and the switch-radius check.
- Brier score 0.30; always 0.5 would score 0.25.
- The confident misses (0.6–0.85) were all about engine or output behaviour: CS-22 bit identity, softening, lost
  bonds. §38's design note also missed two S3 predictions.
- The low-odds hits were rule outcomes: CS-22b 0.15, slip "mixed" 0.35, switch check 0.35.
- Consequence: hunch-level odds stay near 0.5, and the "never used before" items are where we are most often wrong.

**Energy argument (new; from §31 and §37).**
- Rebound kinetic energy per quarter model is e(off)² · ½ m V², with m = 2.83·10⁻¹² kg and ½ m V² = 5.09·10⁻⁷ J.
  That gives **4.5 / 2.1 / 1.7 nJ** at R/8 / R/16 / R/32.
- G_c·A from §31 (W_b ≈ G_c,eff · A_b,max) is **1.4–2.0 nJ at 3×**, **4.8–6.5 nJ at 10×**, and more at 30×.
- CS-22b's 10× bonds took 4.8–6.5 nJ while e fell by only 0.004. That fits §37: the old law booked G_c·A without work.
- With stick on, tearing has to be paid from the recoverable elastic energy, of which the final rebound energy is a
  lower bound. G_c,eff is biased upward (§31).
- Reading:
  - 10× and 30× probably stick;
  - 3× is marginal (G_c·A ≈ the rebound energy);
  - |dR16| ≥ 0.01 becomes likely for every δ_c, so the gate stops filtering, and up to 3 R/32 runs (the full budget)
    may be needed.
- A pass then rests on the convergence of a stuck dR, which 10× and 30× share; they are not independent chances.
  - In CS-22b the margin was 2× (|dR32 − dR16| 0.0014 against 0.0026).
  - e(on) drifted −0.0091 between R/16 and R/32, of which only −0.002 was target-surface motion. The rest is particle
    residual motion, which sticking shear can change.

| Item | Draft | Reassessed | Basis |
|---|---|---|---|
| CS-23 supported | 0.45 | **0.45** | ≈ 0.85 (some δ_c stuck and valid on R/16 and R/32) × 0.55 (stuck dR converges) + ≈ 0.05 (3×), × 0.9 (validity) |
| More δ_c hold than in CS-22b (3× or 10× holds on R/16) | 0.6 | **0.7** | energy argument at 10× |
| 30× passes again | 0.5 | **0.45** | a fresh draw on a near-cancellation with a 2× margin last time |
| 10× passes (new) | — | **0.35** | likely stuck; convergence shared with 30× |
| \|dR16\| ≥ 0.01 for all three δ_c (new) | — | **0.6** | 3× pays G_c from the rebound |
| Remaining tears opening-driven (δ_t at tearing mostly < 0.2 δ_c) | 0.6 | **0.55** | δ_t,el ≤ δ_cap (a few nm) at reopening, but tangential opening after reopening is unresisted in mixed mode |
| A run invalid or stopped by a "never used before" item (new) | — | **0.15** | track record on engine items |

**Open question for the freeze: the lost-bond wording at pair level.**
- The draft says a pair is lost if it "leaves bonded with D < 1 and is not swept as described in §31". The sweep sets
  D = 1, so a swept pair counts as torn.
- At 30× R/32, δ_c / g_L ≈ 2 (§31 item 1). A pair that opens past about 1.5 s is swept at about ½ δ_c, and the rest
  of G_c is booked without work: the §37 artefact in another form.
- This is rare for a stuck particle (CS-22b 30× R/32: 0 transitions), but the rule should say what out.pairs records
  for a swept pair.
- Proposed: a pair swept with D < 1 just before the sweep is reported (count, δ/δ_c at the sweep) and does not
  invalidate a run. A pair that leaves "bonded" by neither tearing nor a sweep is lost. Peter decides at the freeze.
