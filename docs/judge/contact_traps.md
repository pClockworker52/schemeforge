# Arena 2 traps (started 2026-11-24, plan §4; add to it whenever a trap is found)

Each trap is something that makes a number look better or worse than the numerics are. Each line names its source.

## All slots: judge traps (found and fixed)

- **leak_pre was interpolated between load steps.** Before contact-v0.10, F(g/2) was read by linear interpolation
  between steps. It was exact on the dev cases (g/2 = step 2 of 6) and off by up to 9.2e4× on random instances.
  Now g/2 is a load step. Blind audit 2026-11-24, cause 1.
- **Newton's test depended on the force unit.** felupe tests |r_free| / (1e-3 + |reactions|) with an absolute 1e-3,
  so large E was harder to converge. Because `converged` and `max_step` are Target D's robustness axis, this would
  have scored units as robustness. Since contact-v0.10, ε = 1e-3 · E · L. Blind audit 2026-11-24, cause 7.
- **Dev cases hide what held-out instances show.** Both findings above were invisible on the dev suite: E = 1, L = 1,
  and g/2 on a step. Check any claim of the form "agrees to X" on random instances, not on dev.

## `medium`: candidate traps (Target D, breakers)

- **Rescaling γ.** ψ = c γ ψ_zoo passes every constraint, unit scaling included, and moves a zoo member along its own
  front. Compare candidates with the zoo's front over γ, not with the zoo at the same γ (Target D draft, item 1).
- **The fixed regularization.** The judge adds HuHu-LuLu with kr = 5e-7 (spec §C2). A medium that only works because
  of it may fail once the regularization slot exists. Results hold for this kr only.
- **ψ(C) cannot see the contact direction, the thickness or a history** (plan D5). Ideas that need them belong to
  later slots, not to clever tricks in ψ(C).
- **p_l2 and leak_out are mesh-sensitive** (spec §mesh_sens). Do not threshold them on the dev mesh.
- **One HX instance.** max_step is measured on a single held-out instance (Target D draft, item 2).

- **The held-out ranges are wider than dev.** Breakers 2026-11-27 (docs/rounds/2026-11-27-contact-breakers.md):
  - at ν = 0.15, the HF lower edge, neo_hooke fails Newton on Hertz;
  - at ν = 0.45, the HF upper edge, every zoo member misses |a_err| 2 % by 8–21 %;
  - faltus2026's parasitic shear at s = 3, the SF upper edge, is about 170 γ (the neo-Hookean media stay at γ).

  Dev runs ν = 0.3 and s ≤ 2 only. Check a candidate at the range edges before claiming D2, D4 or D7.
- **Dev optimism on the robust media.** faltus2026 meets |a_err| 1.0 % on dev C2-g6 but has a median of 7.6 % on
  HF (D.md, promo references). Do not read D4 from one dev case.

## All slots: known limits (not traps, but easy to forget)

- Q1 elements do not apply: the regularization needs second derivatives (spec §mesh_sens).
- The unconfined C0a with a soft unregularized medium fails Newton. The dev C0a is confined (spec §Known limits).
- On random geometry, FE vs exact is about 1e-8, not round-off: node coordinates are rounded to 10 decimals when the
  meshes are merged (spec §C0a).
- **Exact rediscovery is rare.** In calibration K1, 50 children from neo_hooke matched no other zoo medium's
  fingerprint. The closest distances were 0.07–0.28, against a match below 1e-3
  (docs/rounds/2026-11-27-contact-calibration.md). A near miss is a variant, not a rediscovery: say which constant
  differs.
