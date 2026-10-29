# schemeforge

An AI swarm proposes numerical scheme components (limiters, fluxes, reconstructions, third-medium contact
energies). A deterministic judge scores every proposal against exact solutions. No result counts until the
judge has scored it.

- Plan: [docs/PLAN.md](docs/PLAN.md)
- Current state: [docs/STATUS.md](docs/STATUS.md)
- Decisions: [docs/DECISIONS.md](docs/DECISIONS.md)
- Latest overview: [docs/reports/2026-10-29-big-picture.html](docs/reports/2026-10-29-big-picture.html) (open in a browser)

## What is in the repo

| Part | Where | Tied to a problem? |
|---|---|---|
| Search loop: sandbox, run registry, judge versioning and integrity hash, held-out storage the agents cannot read, promotion test with paired bootstraps, hunch ledger, Pareto leaderboard, evolution engine | `src/schemeforge/core`, `src/schemeforge/engine`, `cli.py`, `mcp_server.py` | no (a few per-arena tables in `engine/`) |
| Agents and process: hunch-generator, proposer, breaker, cheater, analyst, referee, judge auditor; path guard; hunch-round skill | `.claude/` | no |
| Arena 1, 1D Euler and nozzle flow: exact solutions (blind-audited, `audit/`), solvers, metrics, hard constraints, held-out families, zoo of published schemes | `src/schemeforge/arenas/euler1d` | yes |
| Known failure modes of agents and candidates | `docs/judge/euler1d_traps.md` | partly |

A new arena reuses the first two rows and adds its own version of the third.

## Where the method fits

It needs three things:

1. a cheap reference that is exact or provably reliable (here: exact solutions in milliseconds);
2. a component small enough to be a pure function inside a fixed harness (a limiter, a flux, a reconstruction);
3. metrics that measure what practitioners care about.

It does not fit problems without ground truth, problems where one evaluation takes hours, or work whose value lies
in a whole solver rather than one component.

## What it has shown so far

Current numbers and open questions are in [docs/STATUS.md](docs/STATUS.md); each line below links to its evidence.

- The judge holds up: its exact solutions agree with an independent re-implementation to 6.5e-13
  ([audit/euler1d/REPORT.md](audit/euler1d/REPORT.md)), and red teams and breakers found real holes, each closed
  by a judge version ([docs/judge/redteam.md](docs/judge/redteam.md), [docs/DECISIONS.md](docs/DECISIONS.md)).
- The agents add something: in round 3 they produced ideas the main session had not; round 3's best
  candidate came from a proposer agent and round 4's from the engine. The pre-registered swarm test ([docs/targets/swarm.md](docs/targets/swarm.md))
  was met for new ideas and only weakly for the engine improving on them.
- Target A ([docs/targets/A.md](docs/targets/A.md)), a limiter or reconstruction that is both sharp and steady-state
  convergent, was not met in four rounds. The nearest miss passes 12 of 13 checks on held-out data and fails Newton
  convergence on 3 of 20 nozzles. The criteria conflict in several ways rather than along one trade-off
  ([docs/results/arena1-negative.md](docs/results/arena1-negative.md)).
