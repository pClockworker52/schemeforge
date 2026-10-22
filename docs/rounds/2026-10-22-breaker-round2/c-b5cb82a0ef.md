# Breaker report: c-b5cb82a0ef (H-0009, g019_009_explore.py), euler1d / limiter_stateful, judge euler1d-v1.3

I proposed four new cases (B-0007 to B-0010). Two of the sibling's existing cases (B-0002, B-0005) also expose this candidate. Three of the four new cases are genuine candidate weaknesses; B-0010 is a weakness the compressive zoo members share.

The candidate's own dev run is r-20261022-112355-dad3. All candidate and zoo runs below used the dev suite plus the case.

**How the ratchet fails.** When a cell has Δ₊ = 0, the judge sets r = 0. So at step 600 every cell in an undisturbed constant state, and every extremum, stores ψ = 0. Because the ratchet only keeps the minimum, those cells stay first order for the rest of the run. Any wave that enters them after step 600 is computed at first order.

Two other facts set where this can show up:
- Newton is capped at 300 steps, below K0 = 600, so the ratchet never acts in the implicit solver. Nozzle metrics come from the implicit solution, so in nozzles the ratchet can only affect the explicit convergence flags.
- The frozen zoo members switch at K = 1000. Runs with 600 to 1000 steps therefore separate this candidate from them.

## New cases

| Case (draft) | Definition | Candidate | Zoo range (6 members) | Verdict |
|---|---|---|---|---|
| **B-0007** (B-0901) | Sod, N = 1000, t = 0.2 (about 875 steps) | shock 9.77, contact 24.9, l1 5.05e-4 (r-20261022-112722-8f0f) | shock 2.58–3.68, contact 3.76–12.1, l1 1.15e-4–2.77e-4 | **Genuine.** Frozen members give the same numbers as their plain versions (fewer than 1000 steps). |
| **B-0008** (B-0902) | Isolated contact, u = 1, N = 400 on [0, 2], t = 1 (about 870 steps) | contact 25.9, l1 6.1e-4 (r-20261022-112838-3d4f) | contact 4.11–12.5, l1 3.5e-7–8.9e-5 | **Genuine.** Frozen = plain again. |
| **B-0009** (B-0903) | Left blast (R3 states), N = 800, t = 0.012 | contact 29.9, shock 7.62, l1 2.16e-3 (r-20261022-112953-0cde) | contact 4.94–12.6, shock 2.59–5.99, l1 2.6e-4–5.1e-4 | **Genuine, partly shared.** This run goes past 1000 steps, so the frozen members also smear the shock (5.99 / 5.59 against 2.59 / 2.76 for the plain ones). The candidate is still worst on every metric. |
| **B-0010** (B-0904) | Slowly moving Mach-10 shock, s = 0.05·max(\|u\|+a), N = 200, about 420 steps (ratchet inactive) | tv_increase 1.41, overshoot 0.098, l1 8.7e-3 (r-20261022-113113-8928) | superbee / superbee_frozen 2.00 / 0.105; mc 1.15 / 0.104; van Leer (both) 0.41 / 0.025; van Albada 0.28 / 0.024 | **Shared weakness.** The superbee-relaxed base oscillates after a slow strong shock, as superbee and mc do. It is 3 to 5 times worse than van Leer and van Albada. |

Zoo run ids:
- **B-0007:** superbee r-20261022-113352-6b1f, superbee_frozen r-20261022-113523-2e8c, mc r-20261022-113658-7bab, van_albada r-20261022-113816-4434, van_leer r-20261022-113903-b940, van_leer_frozen r-20261022-113951-0f8d
- **B-0008:** r-20261022-114059-9c5b, r-20261022-114226-9a8d, r-20261022-114356-6fa1, r-20261022-114512-bf40, r-20261022-114556-b6c6, r-20261022-114643-4bf2 (same member order)
- **B-0009:** r-20261022-114745-16fa, r-20261022-114914-d965, r-20261022-115047-9b9f, r-20261022-115206-3b1d, r-20261022-115251-bc16, r-20261022-115341-5bfb
- **B-0010:** r-20261022-115444-bd7e, r-20261022-115613-a20a, r-20261022-115748-f6a9, r-20261022-115905-e4e7, r-20261022-115949-54d9, r-20261022-120035-5129

## Existing sibling cases that expose this candidate

- **B-0002** (smooth wave to t = 2.5): order_smooth −0.86, l1 1.86e-2 (r-20261022-120323-0765).
  - The dev suite already shows this: S1 order is 0.13, against at least 1.67 for every zoo member (dev blocks of the zoo runs above).
  - My diagnostic draft B-0905 (S1 at t = 0.6, fewer than 600 steps on N = 200) gives order 1.34 (r-20261022-113229-0d42). So the smooth-wave failure comes entirely from the ratchet, not from the base limiter.
  - I did not re-run the zoo on B-0002; that comparison is in the sibling breaker's report.
- **B-0005** (Anderson nozzle, p_b = 0.215 / 0.985 / 0.99, N = 120, explicit and implicit): converged_expl 0.67, worst explicit drop 9.5 orders (r-20261022-120155-ebe5).
  - Five zoo members converge on all three back pressures to 12.0 orders: van_albada r-20261022-120609-7afc, van_leer r-20261022-120928-cab1, van_leer_frozen r-20261022-120653-5244, mc r-20261022-121018-78a7, superbee_frozen r-20261022-120752-b692.
  - Only plain superbee fails worse (0.33, 3.3 orders; r-20261022-121138-34d7).
  - **Genuine** for this candidate.
- **B-0004 (Sod, N = 1250, t = 0.75) and B-0006 (123 problem, N = 2000, t = 0.6):** about 1400 and 1650 steps, so the same mechanism applies by construction. Their counterparts in the 600 to 1000 step window, without the frozen members' failure, are B-0007 and B-0008. I did not run the candidate on B-0004 or B-0006.

## Tried, not broken (not proposed)

- **B-0906** (123 problem, N = 1000, t = 0.15, about 825 steps): l1 2.20e-3 (r-20261022-120451-8f1d), against 1.21e-3 to 2.14e-3 for the zoo. Van Albada's 2.14e-3 is within 3 %. Zoo runs: r-20261022-121324-9705, r-20261022-121451-59a2, r-20261022-121621-a896, r-20261022-121734-29d8, r-20261022-121817-662b, r-20261022-121901-c708. The error near the near-vacuum centre dominates and hides the first-order rarefaction heads.
- **B-0907** (Anderson nozzle, N = 240, p_b = 0.6784 / 0.95, explicit only): converged at 12.0 orders, no limit cycle (r-20261022-122012-c649). Away from p_crit1 the ratchet makes the explicit solver more dissipative and helps it converge.

## Verdict

The main weakness is the r = 0 → ψ = 0 lock-in. With K0 = 600 it shows up on ordinary fine-grid Riemann runs (Sod at N = 1000, a contact moving at u = 1) where all six zoo members, frozen ones included, stay 2 to 6 times sharper (B-0007, B-0008). It also explains the dev S1 order of 0.13 and B-0002. The explicit stall near the critical back pressure (B-0005) is specific to this candidate too. B-0010 is a cost of the compressive superbee-relaxed base that superbee and mc share.

Draft files are in `/mnt/c/Users/peter/schemeforge/cases/quarantine/drafts/` (B-0901 to B-0907) and the proposed cases are `/mnt/c/Users/peter/schemeforge/cases/quarantine/B-0007.yaml` to `B-0010.yaml`, all waiting for Peter's review. I did not modify any candidate or judge code.
