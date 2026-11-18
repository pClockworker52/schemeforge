# Cold spray: hunch CS-21 (paired differences converge where absolute edge drivers do not), registration (frozen)

Drafted 2026-11-18 by claude from brainstorm item #2 ([multi-particle-brainstorm-2026-11-18.md](multi-particle-brainstorm-2026-11-18.md)).
Registered on Peter's decision (chat 2026-11-18, DECISIONS 2026-11-18).
- **Registered and frozen 2026-11-18**, before any paired run.
- **Scope:** one factor only, a cold-worked target. The surface film is not modelled in the solver, and roughness
  does not fit the axisymmetric deck, so the film and sprayed-surface facts are out of scope.
- **Reference host only:** the §25 2D quad deck. This is not a reopening of the 3D in-solver route, which stays
  closed (DECISIONS 2026-11-17). Any in-solver use after a pass needs Peter's decision.
- **Budget:** this registration makes the count 5 of 5. Rule 1 ("discriminates on obtainable data"): part 1 is judged
  on new runs, but part 2 has no named unseen source. **Peter waived that on 2026-11-18.** The motivating effect
  (cold-worked target −12 % v_cr) has been seen, so any comparison with it is post hoc.

```yaml
- id: CS-21
  registered: 2026-11-18, frozen 2026-11-18
  assumption_broken: >-
    The working assumption of the 2026-11-17 route closure, as far as it concerns differences: that no interface
    driver at the joining edge is verifiable at reachable resolution (opencourant-verification.md §25, §27). CS-21
    claims this holds for absolute values but not for the difference between two runs that share a discretisation.
  statement: >-
    On the §25 reference deck (opencourant-verification.md §25: §8.3 deck, Al O-grid sphere R = 10 µm on an Al block,
    Isolid = 17, P-HG-Al, LAW4 Johnson-Cook + Gruneisen, fork binary d0500106d; 600 and 500 m/s; R/64, R/128, R/256),
    pair each run with a twin that differs only in the block material: Johnson-Cook A' = A + B eps0^n with
    eps0 = 0.3 (P-HG-Al: A' = 148.4 + 345.5 * 0.3^0.183 = 425.6 MPa), B, n, C, m unchanged, particle unchanged. For
    the drivers of §27 (W_ann, P_s, ring Y; ell = 1.5 and 2 µm; particle and block side) and §25's disc Y - 1, the
    paired difference dq = q(hardened) - q(annealed) converges under refinement by the §25 rule. The absolute
    values do not (§27: none usable).
  mechanism: >-
    The edge error comes mostly from how the mesh represents the contact edge and the folding surface near it, and
    that is nearly the same in both twins: same mesh, same edge geometry for the first part of the window, same
    output times. Hardening the block changes the physics by a finite amount and changes the discretisation error
    only to second order, so the error cancels in dq (common-mode rejection). Where the error depends strongly on
    the flow stress, for example through the time of surface folding, the cancellation fails. That is the test.
  parameters: >-
    eps0 = 0.3, fixed now. A' with an unchanged hardening term over-states later hardening compared with a true
    pre-strain; it was chosen because it needs a deck change only. Judged window per speed and mesh: outputs from
    the third up to the last output before the earlier stop time of the two twins on R/256. Ring centres at 0.25 /
    0.5 / 0.75 a_256(t) of the annealed R/256 run, the same for both twins and all meshes. Definitions as §27 and
    driver-check-2026-11-17.md §1, unchanged.
  predicted_effect:
    - {metric: "part 1: usable fraction of dq (driver-check §3 rule applied to dq)", direction: up,
       size: ">= 0.80 on each side and both speeds for at least one driver (absolute values: <= 0.43, §27)"}
    - {metric: "part 2: sign of dq of the usable driver", direction: "any",
       size: "fixed at the part-1 result and predicts the sign of the change in v_cr for a cold-worked target; seen datum -12 % (post hoc only)"}
  kill_criterion: >-
    Part 1 (decisive, on new runs). Apply the driver-check-2026-11-17 §3 rule to dq at each judged output, ring and
    side: |dq256 - dq128| <= 3.5 % |dq256| and (|dq256 - dq128| <= 0.8 |dq128 - dq64| or |dq128 - dq64| <= 3.5 %
    |dq128|). A point where |dq256| < 1 % of |q256| (annealed) has no signal and counts as not converging. A driver is
    usable if it converges at >= 80 % of its judged points, on each side and at both speeds. Refuted if no driver
    (any ell, including disc Y - 1) is usable. Supported if at least one is. Inconclusive if either speed has fewer
    than 5 judged outputs on R/256 in the paired window, or if a hardened twin fails before the third output.
    Part 2 runs only if part 1 is supported. Its kill rule is registered with the choice of the usable driver and
    the sign convention, before any comparison, and against unseen paired data only (none named).
  known_relatives:
    - common random numbers / correlated sampling (variance reduction by pairing; Monte Carlo practice)
    - differential and perturbation analyses in numerical sensitivity studies (shared discretisation error cancels)
    - driver-check-2026-11-17.md and opencourant-verification.md §25, §27 (same deck, drivers, rule; absolute values)
    - "CS-17 (substrate hardening capacity; closed form, same seen fact)"
  label: none yet (referee); never "novel"
  status: open
  author: claude (from brainstorm #2), Peter (registration)
```

## Author's prediction (judgment, recorded 2026-11-18, before any run)

- **Part 1 supported (at least one dq usable): 0.25.** Against cancellation: on these meshes even whole-body plastic
  work differs by 2–12 % between R/128 and R/256 (§27). Hardening the block by a factor of about 2.9 in yield changes
  the plastic zone, and probably the folding time as well, so the error is not purely common-mode.
- **Most likely to pass, if any does:** P_s or disc Y − 1 at 0.25 a on the block side (the best absolute fractions in
  §25 and §27).
- **Cost:** six extra runs, about 8 minutes of engine time for both speeds (§25), plus post-processing as in §27. Runs
  need the fork binary (WSL A). No task has been written for them yet.
