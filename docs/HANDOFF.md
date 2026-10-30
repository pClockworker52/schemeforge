# Handoff — 2026-10-30 (replaces the 2026-10-28 version)

The short version for the next session. The working record is docs/STATUS.md; decisions are in docs/DECISIONS.md;
every number below has its run id there or in the linked file.

## Where things stand

- **Arena 1 (euler1d) is closed.** Four rounds, no Target A promotion; nearest miss c-4ece6bb6f7 fails only A4
  (Newton 0.85). Write-up: docs/results/arena1-negative.md. All hunches closed (H-0019 refuted, H-0024 inconclusive).
- **Judges:** `euler1d-v1.6` (tagged; B-0042/52/54 in dev; the 20-candidate rescore is deferred, DECISIONS
  2026-10-30). `contact-v0.2.dev` (untagged, Phase 6 in progress).
- **Benchmark released:** `benchmark-v1.0`, GPL-3.0-or-later, https://github.com/pClockworker52/schemeforge/releases/tag/benchmark-v1.0.
  Held-out seed stays private; scoring on request (BENCHMARK.md).
- **Phase 6 (Arena 2, third-medium contact):** plan docs/plans/2026-10-30-phase6.md, approved (D1–D5, step 7 added).
  Steps 1 and 2 done, steps 3–7 open.

## Git

- Work branch `claude/exciting-fermi-qy077p` is **9 commits ahead of main** (Phase 6 steps 1–2, plan, licence
  files already on main). Before anything else in WSL: `git fetch origin && git merge origin/claude/exciting-fermi-qy077p`,
  `uv sync --extra contact`, `uv run pytest -q` (289 passed in the cloud), push main.
- `uv sync` alone does not install FElupe: Arena 2 needs `--extra contact` (felupe 11.3.0, tensortrax 0.30.0).

## Phase 6: what exists

| Step | State | Where |
|---|---|---|
| 1 skeleton + generic plumbing | done: each arena is its own judge (hash, integrity, tag); `--arena` required in CLI/MCP; Arena 1 zoo dev identical before/after (21/21) | DECISIONS "Each arena is its own judge"; docs/judge/2026-10-30-phase6-step1-euler1d-check.md |
| 2 exact small cases | done: C0a confined gap closure (exact for any medium, FE agrees ≤ 1e-9), C0b simple shear (exact from ψ), wall pressure from reactions, classical ContactRigidPlane + penalty extrapolation (2e-10) | docs/judge/contact_spec.md; zoo dev run r-20261030-082524-e9a2 (cloud registry) |
| 3 Hertz C2 + patch test C1, error floor | **next** | plan §3 step 3 |
| 4 constraints, metrics, held-out families | open | |
| 5 zoo + trade-off front (stop if no trade-off) | open | |
| 6 blind audit, Target D pre-registration, tag contact-v1.0 | open | |
| 7 search readiness: engine tables, prompts, calibration run, hunch preview | open | |

Code: src/schemeforge/arenas/contact/ (`cases.py`, `solve.py` FElupe models, `reference.py` exact solutions,
`metrics.py`, `constraints.py`, `evaluate.py`, `zoo/medium/neo_hooke.py`); tests/test_contact.py (11 tests).
Candidate contract: `psi_medium(C, p)` in jax.numpy, p = {mu, lmbda, gamma}. Spike timings and scripts:
docs/spikes/2026-10-30-phase6-tooling.md, scripts/spikes/.

## Step 3, concretely (start here)

1. Hertz C2 as decided (D2): elastic cylinder, half model, on a **rigid** flat, medium between, medium bottom fixed;
   1/E* = (1 − ν²)/E; a/R ≤ 0.1, flat ≥ 20 a wide. Start from scripts/spikes/phase6_hertz_felupe.py (its geometry is
   two bodies; change the lower body to the fixed medium base).
2. Pressure p(x) from the wall reactions with `metrics.edge_traction`; compare a, p0, p(x) with the Hertz formula and
   with the classical reference (`ContactRigidPlane` on the cylinder, penalty extrapolation as in
   `solve.gap_closure_classical`).
3. Three meshes and Q1/Q2 → `mesh_sens`; the judge's error floor = classical vs formula, written into the spec.
   Acceptance: classical within 1 % of Hertz on a and p0 at the finest mesh, dev Hertz ≤ 15 s.
4. C1 patch test with non-matching meshes (uniform pressure).
5. Judge commit with a version bump (contact-v0.3.dev), `sforge zoo eval --arena contact --suite dev`, STATUS.

## Traps (cost time before)

- **Integrity is per arena now.** A change under arenas/contact/ never blocks euler1d, but any uncommitted judge file
  refuses scoring in its own arena: commit judge changes before `sforge eval`.
- **Unconfined soft media fail Newton** (γ = 1e-6, no regularization: the medium bulges sideways). Confine, or wait
  for the regularization slot. A Newton failure is recorded as `converged = 0`, not a violation.
- **Penalty contact error ∝ 1/k**: never compare a single penalty run with an exact value; extrapolate over three k.
- **Quadratic edge forces are 1/6, 2/3, 1/6 of a uniform load**: recover pressure with `edge_traction`, never by
  dividing by a tributary length.
- **Memory:** Arena 1 stateful reconstructions need 4.4 GB per worker (SFORGE_MAX_PARALLEL=3 on the PC); Arena 2 needs
  0.2–0.5 GB.
- **`sforge case accept` only works in an interactive terminal** (Peter), not inside an agent session.
- **The sforge MCP server does not connect from the Windows desktop app**; agent runs go from a WSL `claude` session.
- **Cloud vs PC registries differ**: cloud run ids (r-20261030-…) exist only in the cloud session; WSL repeats checks
  that need the PC's registry or the held-out seed.

## Open decisions / later

- When to run the deferred euler1d-v1.6 rescore (only if a round 5 or the benchmark leaderboard needs it).
- Optional: a "coffee" link (GitHub Sponsors or Ko-fi): Peter creates the account, then `.github/FUNDING.yml` and one
  README line.
- 17 round-4 breaker cases stay in quarantine.
