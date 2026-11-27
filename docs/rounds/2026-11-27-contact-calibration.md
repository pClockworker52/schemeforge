# Arena 2 engine calibration K1 (step 7), 2026-11-27: set-up and prediction (written before the run)

Plan step 7 (docs/plans/2026-10-30-phase6.md): "about 50 engine children seeded from the simplest zoo medium.
Acceptance: at least two distinct zoo media rediscovered (fingerprint match), and the archive spreads over its grid."
Named K1, since C1–C4 are contact cases. Arena 1 precedents: C1 (limiter, 5 zoo limiters rediscovered) and C2 (flux, 2 rediscovered, 3 cells; docs/status-archive.md).

## Set-up (fixed before the run)

- Judge contact-v1.0 (6eef4c9). Engine tables from step 7: a9e0cb2 (probe, grid, objectives, Target D screen),
  906ac08 (slot contract and traps that the prompts paste).
- `scripts/e2e_evolve.py start <workdir> --slot medium --backend claude-cli --model sonnet
  --islands 2 --gens 5 --children 5 --budget 50 --seed src/schemeforge/arenas/contact/zoo/medium/neo_hooke.py`.
  `SFORGE_MAX_PARALLEL=3`; wild operator on haiku (engine default).
- Workdir: own registry, ledger and candidates (scratch, not committed). Two calibration islands, not research
  hunches.
- **Seed:** neo_hooke, the simplest zoo medium. Its file names its source (Bluhm et al. 2021), and the engine shows it
  as the parent. The other zoo media are not shown: the prompt contract does not name them (906ac08 and the edit
  after it).

## Counting rule

- A rediscovery is a child whose fingerprint is within the archive's duplicate distance (1e-3, scale-free) of a zoo
  medium's fingerprint (`duplicate:zoo:<name>`).
- A child that reproduces the seed (neo_hooke) is counted separately and **does not count** towards acceptance.
- **Acceptance:** at least two of neo_hooke_iv, faltus2026 and wriggers2013 rediscovered, and the archive occupies at
  least 4 cells.
- Reported, not judged: cells occupied; the descriptor range; children rejected by the hard constraints; how many
  children pass any Target D dev-screen check; the cost.

## Prediction (modeller, before the run)

- neo_hooke_iv rediscovered (swap ln J for (J − 1)² in the volumetric term, plus the isochoric split): 0.55.
- faltus2026 rediscovered (it needs both terms with κ = γ (λ + 2μ/3), the isochoric term squared): 0.15.
- wriggers2013 rediscovered (the eigenvalue-based anisotropic term with ex20's constants): 0.02.
- **Acceptance met: about 0.12.** The fingerprint match is exact to 1e-3, and only neo_hooke_iv is one edit from the
  seed. More likely outcomes: one rediscovery or none, and many near variants in new cells.
- Archive ≥ 4 cells: 0.7.
- Most children fail the Target D dev screen on D4 (|a_err| ≤ 2 % on both C2 cases), as every zoo member does.

If acceptance fails, the result goes to Peter with the Gate 6 report as it stands. The modeller does not change the
grid, the duplicate distance or the counting rule after the run to make it pass.
