# Phase 6 step 1: Arena 1 unchanged by the per-arena judge split (2026-10-30, cloud session)

Plan docs/plans/2026-10-30-phase6.md step 1: making the generic code arena-neutral (per-arena integrity and hash,
no euler1d defaults; commit 10396a2) and adding the contact arena (6deab2c) must leave Arena 1's scores identical.

Method: `sforge zoo eval --arena euler1d --suite dev` twice, judge euler1d-v1.6 both times:
- **before:** an untouched worktree of a92118c (the commit before step 1), its own venv and registry;
- **after:** the main tree at fa2374d.

Compared: every score of each member's run, bitwise, except per-case wall times (`seconds`) and `cost`. Status
compared too. Result: **21 of 21 members identical.** The run ids live in the cloud session's registries (runs/ is not
in git). The recorded judge hash differs by design (whole arenas/ tree before, euler1d only after; DECISIONS
2026-10-30 "Each arena is its own judge").

| Member | Before run | After run | Status | Scores compared | Result |
|---|---|---|---|---|---|
| flux/hll | r-20261030-071517-f887 | r-20261030-075550-03b6 | ok | 124 | identical |
| flux/hllc | r-20261030-071718-5bde | r-20261030-075645-b984 | ok | 124 | identical |
| flux/rusanov | r-20261030-071930-ad2a | r-20261030-075745-e4b1 | ok | 124 | identical |
| limiter/koren | r-20261030-064659-3e5f | r-20261030-071216-1ad6 | rejected | 122 | identical |
| limiter/mc | r-20261030-065024-93d0 | r-20261030-071708-af25 | ok | 124 | identical |
| limiter/minmod | r-20261030-065308-c099 | r-20261030-072204-15cb | ok | 124 | identical |
| limiter/superbee | r-20261030-065431-da88 | r-20261030-072452-eaaf | ok | 124 | identical |
| limiter/van_albada | r-20261030-065738-9787 | r-20261030-073112-dd4a | ok | 124 | identical |
| limiter/van_leer | r-20261030-065841-143b | r-20261030-073324-08a2 | ok | 124 | identical |
| limiter/venkatakrishnan | r-20261030-065947-479c | r-20261030-073547-eb51 | ok | 124 | identical |
| limiter_stateful/mc | r-20261030-070114-5b48 | r-20261030-073900-7913 | ok | 124 | identical |
| limiter_stateful/superbee | r-20261030-070341-6104 | r-20261030-074416-9e42 | ok | 124 | identical |
| limiter_stateful/superbee_frozen | r-20261030-070642-fe12 | r-20261030-074852-3978 | ok | 124 | identical |
| limiter_stateful/van_albada | r-20261030-071008-0c62 | r-20261030-075226-e636 | ok | 124 | identical |
| limiter_stateful/van_leer | r-20261030-071109-2f25 | r-20261030-075325-0cc4 | ok | 124 | identical |
| limiter_stateful/van_leer_frozen | r-20261030-071224-e2d3 | r-20261030-075429-9a6c | ok | 124 | identical |
| reconstruction/first_order | r-20261030-072106-cfe0 | r-20261030-075831-1165 | ok | 124 | identical |
| reconstruction/thinc_bvd | r-20261030-072307-3c68 | r-20261030-075930-cc95 | rejected | 118 | identical |
| reconstruction/weno5z | r-20261030-073614-39fd | r-20261030-080537-71f4 | ok | 124 | identical |
| reconstruction_stateful/muscl_van_leer | r-20261030-074014-44c0 | r-20261030-080728-6567 | ok | 124 | identical |
| reconstruction_stateful/muscl_van_leer_frozen | r-20261030-074324-ae0a | r-20261030-080855-4d35 | ok | 124 | identical |
