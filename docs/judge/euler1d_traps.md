# Arena 1 known traps (euler1d)

Mistakes that cost evaluations in rounds 1 and 2. The engine pastes this file into every prompt; proposers and
hunch-generators read it before writing code or hunches. Each line names its source; add new traps after each round.

## All slots

- **Dev overstates held-out success.** Dev has one nozzle per family; c-44f8015f87 converged on dev N1 but on 60 %
  of held-out NF1 nozzles, c-fb8db52bca on dev N5/N6 but on 90 % of NF1 (rounds 1 and 2). Do not claim held-out
  convergence from dev.
- **Dev is lenient on overshoot.** Dev scores overshoot on Sod (R1); Target A's A7 also uses strong held-out shocks
  (RF2). Every round-2 candidate sharp enough for A1/A2 overshot 2–3× van Leer there and was not promoted. A sharper
  profile is only progress if the overshoot stays near van Leer's.
- **Newton needs finite derivatives.** The implicit solver differentiates the scheme (`jax.jacfwd`). A branch inside
  `jnp.where` is differentiated even where it is not selected: `1 / r`, `log`, `sqrt` or a division by a difference
  that can be 0 puts inf · 0 = NaN into the Jacobian (round 1, H-0004's first implementation). Make every branch
  safe, e.g. `jnp.where(ok, x, 1.0)` inside the division.
- **The batch is invisible.** The judge calls a candidate on one item (limiter), one interface (flux) or one 6-cell
  window (reconstruction) at a time and rejects code whose output depends on batch size, statistics or position
  (red team, docs/judge/redteam.md). Tuning to dev case sizes cannot work.

## `limiter`, `limiter_stateful`

- **A soft max breaks the TVD bound near r = 0.** A log-sum-exp max adds about log 2 / k at r = 0⁺, above 2r, and R3
  blew up (round 1, H-0001 with k = 2, 5). Use a soft min against 2r, or clip to Sweby's region.
- **Smoothing kinks alone does not stop the explicit limit cycle** (round 1, H-0001, H-0002 refuted). The cycle is a
  feedback loop between the limiter and the shock position; memory (`limiter_stateful`) addresses it.
- **Freeze or filter the centred factor ψ = 2φ / (1 + r), not φ.** Freezing φ fixes a multiple of the downwind
  difference and is linearly unstable; freezing ψ is stable (round 2). The one-way ratchet ψ = min(ψ(r), s) after
  K0 steps converged on all 20 held-out nozzles (H-0006, c-a84758f0e8).
- **Blending towards superbee costs smooth accuracy.** c-b5cb82a0ef reached A1/A2 but its S1 order fell to 0.13
  (A6 fails): flat-topped φ at smooth extrema clips them. Keep φ(1) = 1 smooth and test S1.
- **Memory acts late.** A state that only changes after K0 ≈ 1000 steps does nothing in unsteady runs (all shorter),
  so it cannot improve shock or contact width. Sharpness has to come from the stateless part.

## `reconstruction`, `reconstruction_stateful`

- **Write for a 6-cell window.** Each call gets W of shape (6, 3) (n = 0) and must return (1, 3) states; code that
  needs more cells, or assumes n > 0, is rejected as "not local".
- **A constant state must come back exactly**, to 1e-12 relative, for any state value (hard constraint).
- **Sharp is not enough.** THINC/BVD keeps a moving contact within 2 cells, but on dev it stalls on the N5/N6
  nozzle sweeps (explicit 1/3 and 0, limit cycles; cloud dev run r-20261022-054308-f275). Expect to need a
  convergence mechanism, such as the ratchet in `reconstruction_stateful`.
