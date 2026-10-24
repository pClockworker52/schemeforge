# Judge v1.5 step 1: refactor acceptance check (2026-10-24, cloud session)

Plan docs/plans/2026-10-24-round4.md step 2.1: the judge clean-up (one slot table in `evaluate.py`, one shared checker
for both reconstruction slots in `constraints.py`, commit "Judge v1.5.dev step 1") must leave every zoo member's dev
scores identical to v1.4. Compared: every score in the registry of each member's latest dev run, bitwise, except the
per-case wall times (`<case>.seconds`). Result: **21 of 21 members identical, status ok in both.**

The run ids are in the cloud session's registry (runs/ is not in git); WSL repeats the check on promo. The check covers dev only; promo is checked in WSL before the tag (plan step 2.6). Not done in step 1 (deferred,
see STATUS): running stateless schemes as stateful with the state passed through (the `.stateful` flag and
`reconstruct_with_state`, ~59 call sites in the solvers), and merging the two limiter checkers.

| Member | v1.4 run (tree 6f98188c) | v1.5.dev run (b9b16d65) | Scores compared | Result |
|---|---|---|---|---|
| flux/hll | r-20261024-093241-b67b | r-20261024-103156-f529 | 90 | identical |
| flux/hllc | r-20261024-093352-0cd3 | r-20261024-103312-97cb | 90 | identical |
| flux/rusanov | r-20261024-093512-2146 | r-20261024-103428-bb07 | 90 | identical |
| limiter/koren | r-20261024-085709-2fe1 | r-20261024-095609-cf4f | 90 | identical |
| limiter/mc | r-20261024-090113-db35 | r-20261024-095931-1f0f | 90 | identical |
| limiter/minmod | r-20261024-090559-1936 | r-20261024-100304-607e | 90 | identical |
| limiter/superbee | r-20261024-090757-99b6 | r-20261024-100457-553e | 90 | identical |
| limiter/van_albada | r-20261024-091158-6c54 | r-20261024-100922-6306 | 90 | identical |
| limiter/van_leer | r-20261024-091316-e9b5 | r-20261024-101056-122d | 90 | identical |
| limiter/venkatakrishnan | r-20261024-091435-8d40 | r-20261024-101226-f418 | 90 | identical |
| limiter_stateful/mc | r-20261024-091622-49b7 | r-20261024-101425-32ae | 90 | identical |
| limiter_stateful/superbee | r-20261024-091941-97a2 | r-20261024-101803-e51d | 90 | identical |
| limiter_stateful/superbee_frozen | r-20261024-092336-fb0c | r-20261024-102208-d448 | 90 | identical |
| limiter_stateful/van_albada | r-20261024-092818-0c7a | r-20261024-102717-e42b | 90 | identical |
| limiter_stateful/van_leer | r-20261024-092931-ac05 | r-20261024-102837-465c | 90 | identical |
| limiter_stateful/van_leer_frozen | r-20261024-093049-d4d0 | r-20261024-103002-e829 | 90 | identical |
| reconstruction/first_order | r-20261024-093611-0d13 | r-20261024-103530-c8e9 | 90 | identical |
| reconstruction/thinc_bvd | r-20261024-093726-c0a6 | r-20261024-103647-c9a8 | 90 | identical |
| reconstruction/weno5z | r-20261024-094530-a8c1 | r-20261024-104452-3396 | 90 | identical |
| reconstruction_stateful/muscl_van_leer | r-20261024-094751-a736 | r-20261024-104718-6ceb | 90 | identical |
| reconstruction_stateful/muscl_van_leer_frozen | r-20261024-094944-25c9 | r-20261024-104911-5e8c | 90 | identical |

## Step 2: v1.5 contents on the zoo (dev, commit 5421a9c)

Accepted cases B-0016, B-0019, B-0021, B-0030, relative EPS in thinc_bvd, scaling hard constraint. Compared with the
v1.4 runs above on the 18 old cases: every member identical except its wall-time cost, and thinc_bvd, whose old-case
scores move at rounding level (≤ 8e-9 relative; Newton iteration means on B-0011 and N4 by < 1 %). Every member
passes the new scaling constraint. **Two zoo members are rejected under v1.5**, both by a crash on an accepted case
(the run-level constraint "non-finite state"):

- `limiter/koren`: B-0030 (double rarefaction);
- `reconstruction/thinc_bvd`: B-0016 (cold collision) and B-0030 — as the round-3 breakers reported.

| Member | v1.5.dev run | Status |
|---|---|---|
| flux/hll | r-20261024-114205-9c5f | ok |
| flux/hllc | r-20261024-114316-f076 | ok |
| flux/rusanov | r-20261024-114435-0460 | ok |
| limiter/koren | r-20261024-110723-bbcf | rejected |
| limiter/mc | r-20261024-111053-08d1 | ok |
| limiter/minmod | r-20261024-111428-5cac | ok |
| limiter/superbee | r-20261024-111622-8eb3 | ok |
| limiter/van_albada | r-20261024-112029-2fda | ok |
| limiter/van_leer | r-20261024-112151-7980 | ok |
| limiter/venkatakrishnan | r-20261024-112316-6bd4 | ok |
| limiter_stateful/mc | r-20261024-112510-4f38 | ok |
| limiter_stateful/superbee | r-20261024-112833-ec17 | ok |
| limiter_stateful/superbee_frozen | r-20261024-113236-2e3e | ok |
| limiter_stateful/van_albada | r-20261024-113733-0f63 | ok |
| limiter_stateful/van_leer | r-20261024-113856-815c | ok |
| limiter_stateful/van_leer_frozen | r-20261024-114020-1d51 | ok |
| reconstruction/first_order | r-20261024-114533-7a0a | ok |
| reconstruction/thinc_bvd | r-20261024-114653-9c0d | rejected |
| reconstruction/weno5z | r-20261024-115536-7dfb | ok |
| reconstruction_stateful/muscl_van_leer | r-20261024-115753-279c | ok |
| reconstruction_stateful/muscl_van_leer_frozen | r-20261024-115944-d3ac | ok |
