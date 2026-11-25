# Arena 2 traps (started 2026-11-24, plan §4; add to it whenever a trap is found)

Each trap is something that makes a number look better or worse than the numerics are. Each line names its source.

## Judge traps (found and fixed)

- **leak_pre was interpolated between load steps.** Before contact-v0.10, F(g/2) was read by linear interpolation
  between steps. It was exact on the dev cases (g/2 = step 2 of 6) and off by up to 9.2e4× on random instances.
  Now g/2 is a load step. Blind audit 2026-11-24, cause 1.
- **Newton's test depended on the force unit.** felupe tests |r_free| / (1e-3 + |reactions|) with an absolute 1e-3,
  so large E was harder to converge. Because `converged` and `max_step` are Target D's robustness axis, this would
  have scored units as robustness. Since contact-v0.10, ε = 1e-3 · E · L. Blind audit 2026-11-24, cause 7.
- **Dev cases hide what held-out instances show.** Both findings above were invisible on the dev suite: E = 1, L = 1,
  and g/2 on a step. Check any claim of the form "agrees to X" on random instances, not on dev.

## Candidate traps (for Target D and the breakers)

- **Rescaling γ.** ψ = c γ ψ_zoo passes every constraint, unit scaling included, and moves a zoo member along its own
  front. Compare candidates with the zoo's front over γ, not with the zoo at the same γ (Target D draft, item 1).
- **The fixed regularization.** The judge adds HuHu-LuLu with kr = 5e-7 (spec §C2). A medium that only works because
  of it may fail once the regularization slot exists. Results hold for this kr only.
- **ψ(C) cannot see the contact direction, the thickness or a history** (plan D5). Ideas that need them belong to
  later slots, not to clever tricks in ψ(C).
- **p_l2 and leak_out are mesh-sensitive** (spec §mesh_sens). Do not threshold them on the dev mesh.
- **One HX instance.** max_step is measured on a single held-out instance (Target D draft, item 2).

## Known limits (not traps, but easy to forget)

- Q1 elements do not apply: the regularization needs second derivatives (spec §mesh_sens).
- The unconfined C0a with a soft unregularized medium fails Newton. The dev C0a is confined (spec §Known limits).
- On random geometry, FE vs exact is about 1e-8, not round-off: node coordinates are rounded to 10 decimals when the
  meshes are merged (spec §C0a).
