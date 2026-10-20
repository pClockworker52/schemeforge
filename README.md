# schemeforge

An AI swarm proposes numerical scheme components (limiters, fluxes, reconstructions, third-medium contact
energies). A deterministic judge scores every proposal against exact solutions. No result counts until the
judge has scored it.

- Plan: [docs/PLAN.md](docs/PLAN.md)
- Current state: [docs/STATUS.md](docs/STATUS.md)
- Decisions: [docs/DECISIONS.md](docs/DECISIONS.md)

## Setup (WSL2 / Linux)

```bash
uv sync
uv run sforge --help
uv run pytest -q
```

The held-out seed lives outside the repo at `~/.schemeforge/heldout_seed` and is never committed.
