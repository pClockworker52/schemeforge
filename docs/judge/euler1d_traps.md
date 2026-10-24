# Arena 1 known traps (euler1d)

Mistakes that cost evaluations in rounds 1 and 2. The engine pastes this file into every prompt; proposers and
hunch-generators read it before writing code or hunches. Each line names its source; add new traps after each round.

## All slots

- **Dev overstates held-out success.** Dev has one nozzle per family; c-44f8015f87 converged on dev N1 but on 60 %
  of held-out NF1 nozzles, c-fb8db52bca on dev N5/N6 but on 90 % of NF1 (rounds 1 and 2). Do not claim held-out
  convergence from dev. Dev R1 shock widths also run ~0.1 cell above the RF1 median (c-b5cb82a0ef: 2.69 vs 2.58),
  so A1's 2.6 is too strict as a dev threshold (H-0011's sweep used it).
- **Dev is lenient on overshoot.** R1 (Sod) is mild; Target A's A7 also uses strong held-out shocks (RF2). Every
  round-2 candidate sharp enough for A1/A2 overshot 2–3× van Leer there and was not promoted. Since judge v1.4 dev
  has B-0010 (slowly moving Mach-10 shock) as the proxy for A7b. A sharper profile is only progress if the overshoot
  stays near van Leer's.
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
- **Blending towards superbee costs smooth accuracy.** c-b5cb82a0ef reached A1/A2 but its S1 order fell to 0.13
  (A6 fails): flat-topped φ at smooth extrema clips them. Keep φ(1) = 1 smooth and test S1.

## `limiter_stateful`, `reconstruction_stateful`

- **Freeze or filter the centred factor ψ = 2φ / (1 + r), not φ.** Freezing φ fixes a multiple of the downwind
  difference and is linearly unstable; freezing ψ is stable (round 2). The one-way ratchet ψ = min(ψ(r), s) after
  K0 steps converged on all 20 held-out nozzles (H-0006, c-a84758f0e8).
- **A one-way ratchet locks constant regions at first order.** Where the solution is flat the judge sets r = 0, so
  φ = ψ = 0 there; a ratchet that stores min(ψ) at step K0 keeps every such cell (and every extremum) at ψ = 0 for
  the rest of the run, and waves that arrive later are computed first order (round-2 breakers, B-0001..B-0008:
  S1 run past K0 drops to order −0.8 to −1.3). Since judge v1.4 the dev suite (B-0002, B-0004) and the held-out
  LF1/LF2 runs go past 1,500 steps. Memory has to let go again where the flow changes.
- **Memory acts late.** A state that only changes after K0 ≈ 1000 steps does nothing in the short unsteady runs
  (dev R1–R7, RF1, RF2), so it cannot improve shock or contact width there. Sharpness has to come from the stateless
  part; and in the long runs (B-0002, B-0004, LF1, LF2) the memory must not cost accuracy.

## `reconstruction`, `reconstruction_stateful`

- **Write for a 6-cell window.** Each call gets W of shape (6, 3) (n = 0) and must return (1, 3) states; code that
  needs more cells, or assumes n > 0, is rejected as "not local".
- **A constant state must come back exactly**, to 1e-12 relative, for any state value (hard constraint).
- **Sharp is not enough.** THINC/BVD keeps a moving contact within 2 cells, but on dev it stalls on the N5/N6
  nozzle sweeps (explicit 1/3 and 0, limit cycles; cloud dev run r-20261022-054308-f275). Expect to need a
  convergence mechanism, such as the ratchet in `reconstruction_stateful`.
- **Guard positivity.** The round-3 breakers crashed four of five top candidates (non-finite states) on cold
  collisions (p ≤ 1e-4, B-0016) and strong double rarefactions (B-0030); van Leer survives both, the zoo thinc_bvd
  does not. A sharpened or characteristic reconstruction needs a fallback: where a reconstructed ρ or p would be
  non-positive (or below a small fraction of the cell's own value), use the first-order or van Leer state for that
  interface. Since judge v1.5 these cases are in dev.
- **Thresholds must be relative, not absolute.** An `EPS = 1e-20` in a jump test switches THINC off when ρ and p are
  scaled by ≤ 1e-9 (B-0019; the zoo thinc_bvd had the same bug until v1.5). Scale every tolerance with the local
  values (e.g. `1e-12 * (|q_L| + |q_R|)` plus a tiny floor). Since judge v1.5 a hard constraint checks the scheme
  at ×1e-8 and ×1e8 on the probes; the dev metamorphic ×10 measurement did not catch this.
