# sph-contact: E-1 decision point: DRAFT, awaiting Peter, not in force

**Status:** draft of 2026-11-11, by the modeller.
- **Not in force.** On Peter's approval it is renamed `sph-contact-e1-gate.md` and frozen in its own commit. That
  commit comes before any E-1 run at R/32 or R/48.
- **Background:** the success assessment of 2026-11-11 (STATUS). The in-solver route stands or falls on whether the
  contact edge yields interface histories (Y, p_n) that converge with spacing. Every earlier method failed there
  (opencourant-verification.md §8.3, §10.5, §13). E-1 is the first run that can show it, and this rule decides what
  follows, written before the data exist.
- **It judges the host, not the law:** no bond, no v_cr. It does not change the ladder (sph-contact-ladder.md @
  36c34bd) or addendum 1.

## 1. Purpose

Decide whether the route "interface law evaluated inside sph-hvi-contact" (CS-12 → CS-15) continues.

## 2. Runs

- **Case:** Al–Al, quarter symmetry, normal impact, D = 15 µm, `bond.model = none` (contact only).
- **Velocities and spacings:** 500, 800 and 1100 m/s × R/16, R/32, R/48.
- **Set-up:**
  - the frozen §9.1 set-up is the main case;
  - the stabilised set-up S′ runs only if addendum 1 adopts it, as a separate track judged on its own;
  - every row names its set-up.
- **stfac:** as Peter decided for E-1.
- **Deck:** the fork's `hvi/decks/e1_alal.py` (or its successor) at a committed SHA. Material as in that deck,
  stated in the row.
- **End:** t_end = 1.0 D/V, or earlier if contact has ended (no active pair for 0.05 D/V).
- **Output:** the interface file is written every t_out = 0.005 D/V at every spacing.
- **Cost (estimate):** R/48 is about 5 × an R/32 run (3.4 × the particles, 1.5 × the cycles), about 10 h. R/64 is
  30 h or more.
- **Budget:**
  - R/48 at 800 m/s is mandatory;
  - R/48 at 500 and 1100 m/s is run only if the 800 m/s run took ≤ 12 h on 8 workers. Otherwise those cells are
    "not run" and do not count.

## 3. Survival (precondition, every run)

1. reaches t_end with no crash, and the time step never falls below 0.1 × its initial value;
2. **detached mass ≤ 1 %** of the particle's mass. A detached particle is one with no neighbour of its own body
   within 2h. The maximum particle speed is reported, not judged: jet material near the kinematic switch can
   legitimately move faster than 3 V, since the edge speed is close to the sound speed there;
3. no interpenetration: no cross-body particle pair closer than 0.5 s;
4. energy: KE + internal + contact energy + damping work, compared with the initial KE.
   - **Reported, not judged,** until the fork computes internal energy itself: ∫σ:D dV dt over all particles,
     checked to close the energy balance within 2 % in an elastic B-2 run.
   - After that check passes, it is **judged at 5 %**.
   - OpenCourant gives no reliable SPH internal energy (§9.2 item 5; SPEC §4.9), so the engine's printed energy
     error never counts.

If a mandatory run (R/16, R/32 and R/48 at 800 m/s; R/16 and R/32 at 500 and 1100 m/s) fails survival, the gate is
**FAIL (host)**.

## 4. Edge histories (what is measured)

- **Bins (Lagrangian):** the particle's surface particles, grouped by initial polar angle from the impact pole,
  θ₀ ∈ {10°, 20°, 30°, 40°, 50°, 60°}, each ± 2.5°. The outer bins cover the rim, where jetting and the bonded ring sit. The same material is in each bin at every spacing.
- **Per bin, the mean over its particles of:**
  - (a) peak Y over time;
  - (b) peak p_n over time;
  - for (a) and (b), the peak is taken from a centred running mean over 5 output samples, so that contact chatter
    does not set it;
  - (c) Y at the time of the bin's peak p_n;
  - (d) ∫ p_n dt over contact.
- **Cells:** 4 metrics × 6 bins × 3 velocities = 72. A bin with no contact at a velocity is "empty" and is not
  counted.
- **Source:** the interface file (Y as `surface.area` is set in the committed SPEC; p_n per area, O13).

## 5. Convergence rule (per cell)

With m₁₆, m₃₂, m₄₈ the values at the three spacings:
- d₁ = |m₃₂ − m₁₆|
- d₂ = |m₄₈ − m₃₂|

The cell **converges** if **d₂ ≤ 0.03 |m₄₈|** (noise floor: already converged), **or** if **d₂ ≤ 0.10 |m₄₈| and
d₂ ≤ d₁**.

## 6. Verdict

- **PASS:** all of these hold:
  - survival in all mandatory runs;
  - every (a) and (b) cell at 800 m/s converges, in the bins that are non-empty at 800 m/s;
  - at least 80 % of all counted cells converge.
- **FAIL (histories):** survival holds, and one of these is true:
  - fewer than 60 % of counted cells converge;
  - the peak-Y cells (a) at 800 m/s diverge (d₂ > d₁ and d₂ > 0.03 |m₄₈|) in at least 2 of the non-empty bins.
- **INCONCLUSIVE:** anything else. One extension is allowed: R/64 at 800 m/s, judged on the 800 m/s cells with
  R/32 → R/48 → R/64 by the same rule (PASS if every (a) and (b) cell and at least 80 % of the 800 m/s cells
  converge; otherwise FAIL). That result is final.

## 7. Consequences (fixed now)

- **PASS:**
  - E-2 may run;
  - CS-15 (whole-particle model with the interface law) may be registered, with its law, Y', p_E, fitting rule and
    kill rule frozen before any fit;
  - the stage-2 risk counts as retired, recorded as a solver diagnostic, not a judge result.
- **FAIL (host or histories), or INCONCLUSIVE after the extension:**
  - **The in-solver interface-law route stops** (stop rule, as for CS-13). For this gate there is no further tuning of
    stabilisers, contact law or deck without a new registration and a new decision by Peter.
  - **Fallbacks, in this order, each needing Peter's go:**
    1. a particle-level contact rule for build-up (DEM-like: bond or rebound, bonded fraction and target-state change
       as functions of v/v_cr and the target state);
    2. the closed-form route (approximate Y(r, t) and p(r, t) fields for a penetrating sphere, plus Bay's law).
  - The SPH–SPH contact stays a verified tool if milestone 1's ladder passes. The failure is recorded as a negative
    result (iron rule 7).

## 8. Exposure and labels

- **Exposure:** the probe already run (R/16, 800 m/s, tangent-plane gap; particles thrown out, J = 4.4) is exposed.
  It informed none of the thresholds here. The values 10 %, 3 %, 80 %, 60 %, 1 %, 0.5 s and 5 % are judgment, set
  before any convergence data existed.
- **Revision of 2026-11-11:** prompted by Peter's question on strictness, still before any E-1 data at R/32 or R/48.
  - the 3 V speed limit was replaced by detached mass;
  - the energy check is reported until internal energy is computed by the fork;
  - bins at 50° and 60° were added;
  - peaks are smoothed;
  - the convergence rule has a 3 % noise floor.
- **Labels:** every E-1 result is labelled "exploratory; solver diagnostic; no v_cr". Nothing from E-1 feeds back
  into the ladder or addendum 1.

## 9. Records

- One CSV row per run with:
  - fork SHA (committed binary), deck hash, set-up, stfac;
  - the four survival checks;
  - wall time and workers;
  - the 16 bin values.
- A verdict script `hvi/scripts/e1_gate.py` in the fork, committed before the R/32 runs.
- Results go to schemeforge on `coldspray/opencourant-sph` (§14), like the rungs.

## Open for Peter

1. Approve, change or reject the thresholds (§3, §5, §6), the six bins and the smoothing (§4), and the 3 % noise
   floor (§5).
2. Whether S′ is judged here at all, which depends on addendum 1.
3. The 12 h budget line for R/48.
