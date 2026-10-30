# schemeforge benchmark: 1D shock-capturing components (judge `euler1d-v1.6`)

A judge for one component of a finite-volume scheme for the 1D Euler equations: a slope limiter, a numerical flux or
a reconstruction, with or without per-cell memory. It runs the component inside fixed solvers on cases with exact
solutions (Riemann problems, quasi-1D Laval nozzles with a normal shock) and reports sharpness, overshoot, accuracy,
steady-state convergence and smoothness of a steady objective. A zoo of published schemes gives the reference front.

Release `benchmark-v1.0` = judge `euler1d-v1.6` (tag `euler1d-v1.6`). Licence: GPL-3.0-or-later ([LICENSE](LICENSE)). How to cite:
[CITATION.cff](CITATION.cff).

## What you can trust

- **Exact solutions, audited.** An independent re-implementation from the written spec, without the judge code,
  agrees on 1,002 random instances to 6.5e-13 ([audit/euler1d/REPORT.md](audit/euler1d/REPORT.md)).
- **Hard to game.** Candidates are applied one item (cell, interface, window) at a time, so they cannot see the batch
  or guess the case. A red team and four breaker rounds found holes that each led to a judge version
  ([docs/judge/redteam.md](docs/judge/redteam.md), [docs/DECISIONS.md](docs/DECISIONS.md)). Known gaps are listed
  there.
- **Held-out families.** Promotion is judged on instances generated from a secret seed, never on the dev cases a
  scheme was tuned on (see "Held-out data" below).

## Install

Linux or WSL2, Python ≥ 3.11, [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/pClockworker52/schemeforge && cd schemeforge
git checkout benchmark-v1.0          # = judge euler1d-v1.6 plus these docs
uv sync
uv run pytest -q
uv run sforge judge version --arena euler1d     # prints euler1d-v1.6 and "integrity: ok"
```

The judge refuses to score when its own files differ from the tagged version.

## Write a component

One Python file with one pure function: imports only from `jax.numpy`, `jax.lax` and `math`, float64, no I/O, no
hidden state, no Python loops over cells. Contracts, array shapes and units for every slot:
[docs/judge/euler1d_slots.md](docs/judge/euler1d_slots.md). The slots:

| Slot | You write | The judge supplies |
|---|---|---|
| `limiter` | φ(r), elementwise | MUSCL on primitive variables, HLLC |
| `limiter_stateful` | φ(r, s) → (φ, s_new), one state value per cell, carried across steps | as above |
| `flux` | F(U_L, U_R), one interface at a time | MUSCL with van Leer |
| `reconstruction` | (W_L, W_R) from a 6-cell window per interface | HLLC |
| `reconstruction_stateful` | as above, plus a per-cell state | HLLC |

The zoo in `src/schemeforge/arenas/euler1d/zoo/` has one worked example per slot. Common mistakes, with the round
that found each: [docs/judge/euler1d_traps.md](docs/judge/euler1d_traps.md).

## Evaluate

```bash
uv run sforge eval my_limiter.py --arena euler1d --slot limiter --suite smoke   # seconds: does it run?
uv run sforge eval my_limiter.py --arena euler1d --slot limiter --suite dev     # 25 visible cases
uv run sforge eval my_limiter.py --arena euler1d --slot limiter --suite promo   # held-out families
uv run sforge zoo eval --arena euler1d --suite promo                            # zoo references, same seed
uv run sforge promote <candidate id> --arena euler1d --target A                 # verdict per check
uv run sforge leaderboard --arena euler1d --slot limiter --pareto --vs-zoo
```

Every evaluation gets a run id and is stored in a local registry (`runs/registry.sqlite`). A component is
**rejected** if it breaks a hard constraint: non-finite or non-positive states, dependence on the batch, a broken
symmetry, unit dependence (density and pressure × 1e-12 or × 1e12 must scale the output), and others listed in
[docs/judge/euler1d_spec.md](docs/judge/euler1d_spec.md). Case definitions: [docs/judge/euler1d_cases.md](docs/judge/euler1d_cases.md).
Plan for about 1–8 minutes per dev run and 2 GB of memory per parallel worker (4–5 GB for stateful
reconstructions); `SFORGE_MAX_PARALLEL` caps the workers.

## Held-out data

The promo suite is drawn from a seed in `~/.schemeforge/heldout_seed` that is never committed. Create your own:

```bash
mkdir -p ~/.schemeforge && python3 -c "import secrets; print(secrets.token_hex(32))" > ~/.schemeforge/heldout_seed
```

The family generators are public, so your instances follow the same distributions as ours but are different
instances. Medians and shares are comparable to the tables below within sampling noise, not identical. For an exact
comparison, evaluate the zoo under your own seed (`sforge zoo eval --suite promo`) and compare against that: this is
what `promote` does.

**Our seed stays private.** Reports identify it by its fingerprint. To have a component scored on our held-out
instances, open an issue on the repository with the component file; we run `eval --suite promo` and `promote`, and
reply with the aggregates and verdicts, never the instances.

## Reference results (zoo, judge v1.6, our seed)

Held-out promo aggregates. Under v1.6 every value is identical to v1.5 (docs/judge/2026-10-30-v16-check.md). Shock and
contact: median width in cells over RF1. Explicit / Newton: share of NF1 nozzle instances that converge. Roughness:
p90 of the second difference of the nozzle wall force over a back-pressure sweep (NF3). Overshoot: p90 over RF1 /
RF2.

| Member (slot) | Promo run | Shock | Contact | Explicit | Newton | Roughness | Overshoot RF1 / RF2 |
|---|---|---|---|---|---|---|---|
| thinc_bvd (reconstruction)¹ | r-20261030-032002-e8b6 | 2.182 | 2.918 | 0.35 | 0.65 | 0.0620 | 0.0193 / 0.0232 |
| weno5z (reconstruction) | r-20261030-032009-ded5 | 2.350 | 4.312 | 0.65 | 0.65 | 22.2 | 0.0717 / 0.0696 |
| superbee (limiter) | r-20261030-030643-9169 | 2.493 | 4.576 | 0.05 | 0 | 7.70 | 0.107 / 0.0915 |
| koren (limiter)¹ | r-20261030-030443-f2db | 2.529 | 6.370 | 0.55 | 0.25 | 17.6 | 0.0662 / 0.0531 |
| mc (limiter) | r-20261030-030442-67bf | 2.543 | 6.117 | 0.45 | 0.30 | 20.2 | 0.0601 / 0.0727 |
| hll (flux) | r-20261030-031759-fa33 | 2.936 | 7.283 | 0.65 | 0.90 | 0.00179 | 0.0225 / 0.0241 |
| venkatakrishnan (limiter) | r-20261030-031030-5b4f | 2.944 | 7.583 | 0.60 | 1.00 | 0.00179 | 0.0207 / 0.0284 |
| van Leer (limiter; = hllc flux, = muscl_van_leer) | r-20261030-030840-32ce | 2.945 | 7.124 | 0.60 | 1.00 | 0.00179 | 0.0219 / 0.0233 |
| van Leer frozen (limiter_stateful) | r-20261030-031632-f740 | 2.945 | 7.124 | 0.85 | 1.00 | 0.00179 | 0.0219 / 0.0233 |
| van Albada (limiter) | r-20261030-030835-ce2f | 3.424 | 8.416 | 0.95 | 1.00 | 0.00146 | 0.0136 / 0.0244 |
| rusanov (flux) | r-20261030-031904-cb2b | 3.472 | 8.463 | 0.40 | 0.95 | 0.00184 | 0.0119 / 0.0162 |
| minmod (limiter) | r-20261030-030442-7c0f | 3.894 | 10.71 | 0.90 | 1.00 | 0.000871 | 0.0049 / 0.0294 |
| first order (reconstruction) | r-20261030-031932-9a90 | 11.01 | 46.0 | 1.00 | 1.00 | 0.00112 | 0.0031 / 0.0063 |

¹ Rejected on dev under v1.5 and v1.6 (crashes on B-0016 / B-0030); its promo run is ok.

**The open problem the numbers show.** Every zoo member with a shock of 2.6 cells or less has Newton convergence of
0.65 or less and roughness of 0.06 or more. Every member with Newton 1.00 has a shock of 2.94 cells or more. Target A
([docs/targets/A.md](docs/targets/A.md)) asks for a scheme in the gap: shock ≤ 2.6, contact ≤ 6.5, Newton 1.00,
roughness ≤ 0.002, overshoot ≤ 1.1 × van Leer, second order on smooth flow and on long runs.

## What the search found

Four rounds of LLM-agent and evolutionary search (1,316 candidates) did not meet Target A. The nearest miss passes
12 of 13 checks and fails Newton convergence on 3 of 20 held-out nozzles. Full account, every hypothesis and verdict:
[docs/results/arena1-negative.md](docs/results/arena1-negative.md) and [ledger/hunches.yaml](ledger/hunches.yaml).
Searched candidate files are not in the repository; their registry records and run ids are cited in docs/rounds/.
