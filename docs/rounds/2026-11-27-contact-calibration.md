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

## Result (2026-11-27, after the run)

Engine run e-20261127-214212-2995 (scratch workdir; registry, ledger and candidates not committed). Five generations
of 10 children: 50 children, 50 ok, 0 rejected by the hard constraints, 0 LLM errors, cost $3.10. The seed's dev
run is r-20261127-214212-13f3.

**Acceptance: not met.** Rediscoveries: none of neo_hooke_iv, faltus2026 or wriggers2013 (0 of the required 2). The
grid half is met: 19 cells occupied (≥ 4).

| Item | Outcome |
|---|---|
| Fingerprint matches with a zoo medium | 1, the seed neo_hooke (`zoo:neo_hooke`, not counted) |
| Closest approach to each other zoo medium (fingerprint distance; duplicate below 1e-3) | wriggers2013 0.070, neo_hooke_iv 0.173, faltus2026 0.282 |
| Nearest zoo medium per child | neo_hooke_iv 23, faltus2026 16, wriggers2013 8, neo_hooke 3 |
| Duplicates among children | 4 (of 3 earlier children) |
| Archive cells | 19 of 110 |
| Descriptor range | compression_stiffening 1.36 … 8.17; shear_stiffening −2.07 … −0.65 (no child on faltus2026's shear-stiffening side, +0.45) |
| Target D dev screen (11 checks): failed checks per child | 2: 6 children; 3: 27; 4: 4; 5: 7; 6: 6. The seed fails 4. |

The best six children by the screen fail two checks each, C0a-g5 gap_res (> 0.0029) and C2-g5 |a_err| (> 0.02).
The best of them is c-e7921c9738 (dev r-20261127-214407-104d): gap_res 0.0088, C2-g5 a_err 0.146, C2-g6 a_err −0.019,
p0_err 0.001, and C4 converges. These are dev numbers from a calibration run, not results. No child was evaluated on
promo.

**Against the prediction:**
- neo_hooke_iv 0.55: not found. faltus2026 0.15: not found. wriggers2013 0.02: not found.
- Acceptance about 0.12: not met, as predicted. Archive ≥ 4 cells 0.7: met.
- "Most children fail D4": right. Every child fails at least two checks, and C2-g5 |a_err| is among the failures of
  the best ones.

**Reading (modeller; for Peter, not a verdict).**
- The engine runs on the arena end to end. The probe, grid, objectives and screen work, and the archive spreads.
- Exact rediscovery is a much stricter test here than in Arena 1. A medium has free choices that a limiter does not:
  which moduli scale which term, and K versus μ. A child one constant away from a zoo medium is not a fingerprint
  match. Arena 1's limiters are fixed functions of one variable.
- The children stayed on the seed's side of the shear axis.

Whether step 7's acceptance can be counted as met on this evidence, or how the run is repeated, is Peter's decision
at Gate 6. The counting rule and the grid are not changed after the run.

**Decided (Peter, 2026-11-27; DECISIONS 2026-11-27 "Gate 6 passed"):** Gate 6 passes. The rediscovery half is
recorded as not met, and the rule is unchanged.
