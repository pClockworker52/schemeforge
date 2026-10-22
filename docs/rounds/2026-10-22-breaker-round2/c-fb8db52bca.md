# Breaker report: c-fb8db52bca (H-0006, g018_006_crossover.py), euler1d / limiter_stateful, judge euler1d-v1.3

I proposed five new cases (B-0011 to B-0015), all steady nozzles. Three are genuine candidate weaknesses (B-0011, B-0012, B-0013). B-0014 is close to a hard case and B-0015 is a weakness the compressive zoo members share. Of the sibling cases, six still break this candidate, B-0009 does not, and B-0010 is shared. All runs are suite dev with the case added; I edited no candidate or judge code.

## Existing sibling cases on this candidate

Zoo numbers are from the sibling reports; I did not re-run the zoo on these.

| Case | Candidate (run) | Zoo (sibling reports) | Verdict |
|---|---|---|---|
| B-0001 (smooth wave, t = 10) | order 0.31, l1 7.33e-2 (r-20261022-122732-d903) | order 0.49–2.22, l1 1.1e-3–3.7e-3 | **Genuine** |
| B-0002 (smooth wave, t = 2.5) | order −1.33, l1 1.42e-2 (r-20261022-122357-8923) | order 1.31–1.96, l1 ≤ 8.1e-4 | **Genuine**, strongest |
| B-0003 (contact, about 3300 steps) | contact 42.5, l1 1.48e-3 (r-20261022-122837-0194) | frozen members 36.4–36.7; others 4.1–13.0 | Shared with the frozen members; candidate worst |
| B-0004 (long Sod) | shock 9.86, contact 38.1, l1 6.20e-4 (r-20261022-122942-21ed) | frozen contact 15.8 / 18.0; others 3.8–14.4 | Shared with freezing; candidate worst |
| B-0005 (nozzle, N = 120) | converged_expl 0.67, 9.09 orders (r-20261022-122621-7228) | five members 3/3 at 12.0 orders; superbee 1/3 | **Genuine** |
| B-0006 (long 123 problem) | l1 1.79e-3 (r-20261022-123054-6006) | 8.0e-4–2.09e-3 (van_leer_frozen worse) | Mild |
| B-0009 (blast, N = 800) | contact 8.15, shock 6.03, l1 2.99e-4 (r-20261022-123159-813d) | contact 4.94–12.6, shock 2.59–5.99, l1 2.6e-4–5.1e-4 | **Not broken** (shock only 0.04 cells above the worst member) |
| B-0010 (slow Mach-10 shock) | tv 1.35, overshoot 0.095 (r-20261022-122504-2348) | mc 1.15 / 0.104, superbee 2.00 / 0.105, van Leer 0.41 / 0.025, van Albada 0.28 / 0.024 | Shared with the compressive members |

## New cases

All new failures are on the nozzle. The explicit solver stalls with no limit cycle when a weak shock sits just behind the throat (p_b near p_crit1), on the Anderson nozzle. superbee_frozen converges explicitly on B-0011, B-0012 and B-0013 while the candidate stalls. So the stall is not caused by a compressive base alone. My untested guess is that psi keeps following the live value wherever it is lower than the stored one, so freezing never completes. Newton never reaches step 1000, so the implicit solver runs the base limiter only.

**B-0011** (draft B-1106): Anderson, gamma 1.2, N = 120, p_b 0.985 / 0.99, explicit and implicit.
- Candidate: converged_expl 0.5, worst 8.87 orders; Newton converges, 170 steps (r-20261022-132419-bcf4).
- **All six zoo members converge explicitly at 12.0 orders:** van_leer r-20261022-132752-89aa, van_leer_frozen r-20261022-132850-963f, van_albada r-20261022-133009-b61f, mc r-20261022-133107-d0d7, superbee r-20261022-133232-1563, superbee_frozen r-20261022-133414-e27f.
- **Genuine, the cleanest case.**

**B-0012** (draft B-1110): the same at gamma 5/3.
- Candidate: converged_expl 0.5, 8.21 orders (r-20261022-135947-c97c).
- Five members converge explicitly at 12.0 orders: van_leer r-20261022-140314-1764, van_leer_frozen r-20261022-140422-973a, van_albada r-20261022-140542-7f3b, mc r-20261022-140652-2ab9, superbee_frozen r-20261022-141017-2f47.
- Only superbee is worse: 0, 2.70 orders, limit cycle 0.5 (r-20261022-140834-a606).
- **Genuine.** Same mechanism as B-0011; Peter may merge the two.

**B-0013** (draft B-1102): Anderson, N = 240, p_b 0.985 / 0.99, explicit and implicit.
- Candidate: converged_expl 0 (fails at both), 6.54 orders; implicit converges, 247 Newton steps on average (r-20261022-130714-1f45).
- Converge explicitly at 12.0 orders: van_leer r-20261022-131127-3248, van_albada r-20261022-131404-eb31, van_leer_frozen r-20261022-131849-6904, superbee_frozen r-20261022-131653-f30f.
- mc (0.5, 4.23, r-20261022-131227-c4c7) and superbee (0, 3.00, r-20261022-131502-0359) fail both solvers.
- **Genuine against the smooth and frozen members.** The candidate's Newton does better than mc's and superbee's.

**B-0014** (draft B-1107): Anderson, single nozzle, p_b 0.99, N = 360.
- Candidate: both solvers fail (Newton at the 300 cap, explicit 4.83 orders). shock_pos_err 4.94 cells, shock_width 24 (the transition never completes), l1 4.3e-3 (r-20261022-134553-39d1).
- The smooth members converge, but only just under the cap:
  - van_leer: 298 steps, shock_pos_err 0.32, l1 1.3e-4 (r-20261022-134743-8cd4)
  - van_leer_frozen: 298 steps (r-20261022-134906-eade)
  - van_albada: 286 steps, l1 1.1e-4 (r-20261022-135046-eb8a)
- mc fails: l1 3.2e-2, shock_pos_err 3.95 (r-20261022-135157-6fee). superbee and superbee_frozen fail: l1 6.7e-2, shock_pos_err 19.2 (r-20261022-135347-98c7, r-20261022-135552-4029).
- **Shared with the compressive members, close to a hard case.** The candidate is 33 times worse than van Leer on l1 but better than mc and superbee.

**B-0015** (draft B-1103): conical (N6 geometry), p_b 0.96 / 0.965 / 0.97, N = 120.
- Candidate: both solvers converge, roughness_J 0.93 (r-20261022-130850-3097).
- Smooth members: van_leer and van_leer_frozen 0.113 (r-20261022-132021-f9d3, r-20261022-134255-c378), van_albada 0.039 (r-20261022-132653-4fdb).
- Compressive members fail Newton: mc 250 (r-20261022-132531-317b); superbee_frozen 2795 (r-20261022-134109-8e8f) and superbee 2795 (r-20261022-140117-378b).
- **Base-limiter weakness shared with the compressive members, moderate:** 8 to 24 times rougher than the smooth members.

## Tried, not broken (not proposed)

- **B-1101** (parabolic nozzle near p_crit1): converged at 12.0 orders (r-20261022-130604-591f).
- **B-1104** (Anderson, N = 60, near p_crit1): roughness 144, against 22.5 for van_leer (r-20261022-132105-51c9) and 16.0 for van_albada (r-20261022-132155-8961), candidate run r-20261022-130958-cef7. With closely spaced back pressures the exact J is nearly linear, so the metric's denominator is tiny and the values mean little.
- **B-1105** (smooth wave, coarse grids, under 1000 steps, tests the base alone): the candidate is the best scheme, order 1.78, l1 5.5e-4 (r-20261022-132319-8d53). Zoo: van_leer 1.70 (r-20261022-133616-4405), mc 1.64 (r-20261022-133710-bfe3), van_albada 1.65 (r-20261022-134015-9617), superbee 0.66 (r-20261022-133840-2081).
- **B-1108** (mirror of B-0010): the base limiter is not symmetric, but the mirrored case is milder, tv 0.86, overshoot 0.049 (r-20261022-134442-3aea).
- **B-1109** (Anderson, N = 240, p_b 0.6784 / 0.8, explicit only): converged at 12.0 orders (r-20261022-135822-ba69).
- **Dev N2:** the candidate's explicit solver stalls at 4.06 orders, but so does every zoo member: van_leer 4.16 (r-20261022-131127-3248), and 3.1 to 5.6 for the rest. Hard case.

## Verdict

- **Genuine weaknesses of this candidate:**
  - **B-0001 and B-0002:** once a run passes 1000 steps, cells that had r = 0 at step 1000 stay first order.
  - **B-0005, B-0011, B-0012 and B-0013:** the explicit solver stalls near p_crit1. Most zoo members converge here, superbee_frozen included.
- **Shared with freezing:** B-0003, B-0004 and B-0006. The candidate is the worst scheme on all but B-0006.
- **Shared with the compressive zoo members:** B-0010, B-0014 and B-0015. The crossover base sits between mc and superbee. It is worse than van Leer and van Albada but generally better than mc and superbee.
- **No case breaks all six zoo members.** B-0014 is close to a hard case, because the smooth members converge only just under the 300-step cap.

The case files are in `/mnt/c/Users/peter/schemeforge/cases/quarantine/` (B-0011.yaml to B-0015.yaml) and the drafts in `/mnt/c/Users/peter/schemeforge/cases/quarantine/drafts/` (B-1101 to B-1110), waiting for Peter's review.
