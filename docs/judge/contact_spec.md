# Arena 2 judge spec: third-medium contact (judge `contact`, written with step 2, 2026-10-30)

This file is the written spec the `judge-auditor` re-implements from without seeing the code (PLAN §14.8). Units are
consistent but arbitrary; plane strain throughout; forces per unit thickness; stresses are first Piola–Kirchhoff (P).

## Slot `medium`

`psi_medium(C, p) -> scalar`: strain energy per unit reference volume of the medium, a `jax.numpy` function of the
right Cauchy–Green tensor C (3 × 3, C₃₃ = 1 in plane strain) and p = {mu, lmbda, gamma}: the body's Lamé moduli and
the medium stiffness scale γ set by the case. The judge differentiates it (JAX) and runs it per quadrature point
inside FElupe (felupe 11.3, `felupe.constitution.jax.Hyperelastic`). Bodies are compressible neo-Hookean:
ψ_b = μ/2 (tr C − 3) − μ ln J + λ/2 ln² J, J = √det C.

**Hard constraints** (reject): on 40 fixed plane-strain deformation gradients (rest; uniaxial stretch 1e-3 … 5;
simple shear 0.1, 1, 5; random with det F in [1e-3, 10]) the energy is a float64 scalar, it and dψ/dC are finite,
and repeated calls are bitwise equal; at rest ψ(I) and dψ/dC(I) are zero to 1e-12 · μγ (p = {μ, λ} of E = 1,
ν = 0.3, γ = 1e-3). More in step 4 (unit scaling, positivity in compression, batch independence).

## C0a, gap closure (laterally confined)

An elastic body (height h, width w, E, ν) sits on a medium layer of thickness g whose bottom is fixed to a rigid wall
at y = 0. Every node has u_x = 0, so each layer is homogeneous: F = diag(1, s, 1) with stretch s_b in the body and
s_m in the medium. The top is pushed down by d ∈ [0, push] in `steps` equal steps.

- Body stress: P_b(s) = μ (s − 1/s) + λ ln(s)/s. Medium stress: P_m(s) = d/ds ψ(diag(1, s², 1), p).
- Exact solution for a given medium: P_b(s_b) = P_m(s_m) with h s_b + g s_m = h + g − d; force F = −w P_m(s_m),
  medium thickness g s_m. Bi-quadratic elements represent it exactly. When the body and medium meshes are merged,
  node coordinates are rounded to 10 decimals. On the dev cases the FE result agrees to 1e-9 or better (measured
  1e-12 … 1e-16, except where the force is below 1e-6 and Newton's tolerance dominates). On random geometry, the
  1e-10 rounding of the layer boundaries limits it to about 1e-8 (blind audit 2026-11-24: force ≤ 1.0e-8,
  thickness ≤ 1.2e-8, wall pressure ≤ 2.5e-8).
- Ideal contact: F = 0 for d ≤ g; F = −w P_b((h − (d − g))/h) for d > g.
- Metrics: `leak_pre` = F(g/2) / F_ideal(push). F(g/2) is solved at push = g/2, which is added to the load steps
  when it is not already one (since contact-v0.10; before, it was interpolated linearly between steps); `gap_res` = medium thickness at full push / g; `force_err` =
  F(push) / F_ideal(push) − 1 (positive: the remaining layer takes up height, so the body is compressed more);
  `newton_iters` (sum over steps, including the g/2 step); `min_J_medium`; `converged` (0 if Newton fails: a
  result, not a violation).
- Newton, every FE solve of the judge: felupe's test |residual of the free dofs| / (ε + |reactions|) < 1e-10, with
  ε = 1e-3 · E · L and L the case's height (C0a, C1: h; C2: H). The test is invariant under a change of force or
  length units, and identical to felupe's default (ε = 1e-3) for E = L = 1. Since contact-v0.10: before, the
  absolute ε made convergence depend on E (blind audit 2026-11-24).
- Run-level violation: min J of the medium ≤ 0.
- Contact pressure on the wall: nodal reactions solved against the consistent mass matrix of the quadratic edge
  elements (`metrics.edge_traction`), so a uniform pressure comes back exactly (F / w here).
- Classical reference: the body alone over a rigid plane with felupe's frictionless `ContactRigidPlane`; the penalty
  error (∝ 1/k) is removed by Richardson extrapolation over k = 1e2, 1e3, 1e4. Reproduces the ideal force to 2e-10
  on the dev cases and to 1.1e-9 on random instances (blind audit: always slightly below ideal; the leftover
  extrapolation term). Gives zero force before contact (≤ 4e-12).

Dev cases: C0a-g3, C0a-g5, C0a-g6 with γ = 1e-3, 1e-5, 1e-6; h = 1, w = 0.2, g = 0.1, push = 0.15, 6 steps, E = 1,
ν = 0.3, one cell across, 2 cells in the body and 2 in the medium. Smoke: the γ = 1e-3 case.

## C0b, simple shear

The medium alone in F = [[1, s, 0], [0, 1, 0], [0, 0, 1]], evaluated directly: P = 2 F dψ/dC at C = FᵀF.
Metrics: `shear_parasitic` = P_xy / (μ s), the medium's shear stress relative to the body's linear one (0 ideal;
exactly γ for the scaled neo-Hookean); `normal_parasitic` = P_yy / (μ s). Dev cases C0b-s05 and C0b-s2: s = 0.5 and
2, γ = 1e-5.

## C1, patch test (step 3)

Adapted from Taylor & Papadopoulos (1991). In third-medium contact the medium's mesh connects the bodies, so the
whole mesh is conforming by construction and non-matching contact interfaces do not occur; the analogue is the
constant-stress patch test on distorted elements. C1 is C0a (confined) with 3 columns, 3 body rows, 3 medium rows
and every corner node moved randomly by up to 0.3 cell sizes (interior nodes in x and y, side nodes along their
side; the layer boundaries stay straight); mid-edge and centre nodes are placed after the move, so edges stay
straight and Q2 reproduces the homogeneous solution exactly. γ = 1e-5, seed 11. Metric added to all gap-closure
cases: `pressure_spread` = (max − min)/mean of the wall pressure at full push (0 exactly). Measured with the zoo
neo-Hooke: force vs the exact solution 6e-13 … 5e-15, pressure spread 5e-9 (Newton tolerance).

## C2, Hertz (step 3)

Elastic cylinder (half model, symmetry at x = 0) with the parabolic profile of Hertz theory, y = g + x²/(2R),
height H, width W, above a rigid flat at y = 0; the medium fills the gap with its bottom fixed to the flat. The top is
pushed down by `push` in `steps` steps. Defaults: R = W = H = 1, g = 0.002, push = 0.006, 12 steps, E = 1, ν = 0.3.
Mesh: 32 columns graded x = W s² (7 elements across the contact at a ≈ 0.045), 16 body rows graded towards the
contact, 4 medium rows; mid-nodes are placed on the curves (a chord placement missed them in the first prototype).

- The judge adds a fixed HuHu-LuLu Hessian regularization of the medium, kr · λ · W² with kr = 5e-7, until the
  regularization slot exists. Measured trade-off (γ = 1e-6, 32 columns): kr = 5e-6 gives a spurious tension on the
  flat outside the contact of about 4 % of p0; 5e-7 about 0.3 %; 5e-8 about 0.04 % but Newton fails on finer meshes
  and at γ = 1e-7; kr = 0 fails Newton. 5e-7 with 12 steps converges at 32 and 64 columns for γ ≥ 1e-6.
- Hertz for the measured load P (rigid flat, 1/E* = (1 − ν²)/E): a = √(4PR/(πE*)), p0 = 2P/(πa),
  p(x) = p0 √(1 − x²/a²).
- The load P is 2 × the reaction on the top edge (full model). It equals 2 Σ f of the flat's nodal forces up to
  the Newton residual (≤ 6e-13 absolute in the audit). Every Hertz quantity below uses this P, with a = a_hertz and
  p0 = p0_hertz from it; x is the reference x of the flat's nodes.
- Metrics:
  - `a_err` = √(8 Σ f x² / P) / a − 1: the width from the second moment of the nodal contact forces
    (∫p x² = P a²/4, exact for consistent forces on quadratic edges). It includes traction outside the contact.
  - `p0_err` = max p / p0 − 1, with p the nodal pressure recovered as in §C0a.
  - `p_l2` = √(∫(p − p_H)² / ∫p_H²), both integrals by the trapezoidal rule over the nodes with x < 1.5 a.
  - `leak_out` = 2 Σ |f| over the nodes with x > 1.2 a, over P (pressure or tension through the open gap).
  - `load`, `newton_iters`, `min_J_medium`, `converged`.
- Classical reference (`solve.hertz_classical`): the cylinder alone with felupe's `ContactRigidPlane` (penalty 1e3;
  1e2 changes p0 by 3e-4, 1e4 does not converge). **Judge error floor**, classical vs Hertz: dev mesh a +0.9 %,
  p0 −0.5 %, p_l2 1.6 %; 64 columns a +0.4 %, p0 −0.35 %; 128 columns a +0.3 %, p0 −0.34 % (the plateau is the
  finite body, not the mesh). Differences between media below about 1 % (dev) are not resolved. On 90 random
  instances in the held-out ranges (blind audit 2026-11-24), the floor is wider: a −1.25 … +1.33 % (median
  +0.30 %), p0 −0.57 … +0.19 % (median −0.32 %), p_l2 1.1 … 9.7 % (median 3.5 %).
- Dev cases C2-g5, C2-g6 (γ = 1e-5, 1e-6), 7–10 s each. Zoo neo-Hooke: γ = 1e-5 a_err +12 %, p0_err +0.1 %;
  γ = 1e-6 a_err −3.9 %, p0_err +0.9 %, 87 Newton iterations; γ = 1e-4 a_err +104 % (load carried through the open
  gap); γ = 1e-7 does not converge.

## C4, frictionless sliding (step 6, contact-v0.11)

PLAN §14.2: steady sliding of a body on a flat; frictionless, Ft = 0. The C2 cylinder (same profile, medium, fixed
regularization kr) as a **full model**: the half mesh is mirrored at x = 0, with nx columns per half. The top edge
is pushed down by `push` in `steps` equal steps, starting from zero. It is then moved tangentially by `slide` in
+x, in `slide_steps` equal steps, while its vertical displacement is held at −push. The top edge's x and y
displacements are both prescribed throughout, and the medium's bottom is fixed to the flat. Defaults: R = W = H = 1,
g = 0.002, push = 0.006, 12 + 5 steps, slide = 0.0045 (about 0.1 a at the default load), 16 columns per half,
10 body rows, 4 medium rows, E = 1, ν = 0.3.

- **Forces** are the reactions on the top edge, per unit thickness. Ft is the tangential force in the slide
  direction. Fn is the normal compressive force. Fn_press is Fn at the end of the press, the last of its `steps` + 1
  recorded states.
- **Metrics:**
  - `shear_parasitic` = Ft / Fn at the end of the slide: 0 ideal, and positive when the medium resists sliding.
    This is a different case from C0b, whose metric of the same name measures the material law alone.
  - `fn_rise` = Fn(end) / Fn_press − 1: ploughing of the medium ahead of the contact (0 ideal).
  - `load` = Fn(end), `newton_iters`, `min_J_medium` and `converged`.
- **Classical reference** (`solve.sliding_classical`): the cylinder alone, both halves, on felupe's frictionless
  `ContactRigidPlane` (penalty 1e3). Self-check: |shear_parasitic| ≤ 1e-8 and |fn_rise| ≤ 1e-6. Measured: 9e-15 and
  1.7e-10.
- **Zoo prototype** (γ = 1e-6, slide 0.1 a, 24 columns per half unless stated). These are scratch measurements, not
  registered runs; the registered values are in the zoo check of this judge version.
  - faltus2026: shear_parasitic 6.2 %, fn_rise 1.9 %. 16, 24 and 32 columns per half give 6.217, 6.221 and 6.221 %,
    so the metric is mesh-stable.
  - wriggers2013: 4.0 %.
  - neo_hooke_iv: 1.0 % at slide 0.05 a, and Newton fails at 0.1 a.
  - neo_hooke: Newton fails at slides of 0.01 a and above, but converges at 0.001 a.
- **Held-out family SL** (4 instances): the HF geometry ranges, slide 0.2–0.9 % of R (about 0.05–0.2 a),
  slide_steps 5, 14–18 columns per half, 10 body rows, E, ν and γ as HF.
- **Limits:**
  - This is small sliding (a fraction of a). Large sliding (ironing) is C5, not in this phase.
  - A thin residual layer sheared by the slide is the mechanism. The metric therefore depends on the slide
    distance, so compare candidates at equal slide only.

## mesh_sens (step 3)

PLAN §14.4 asks for the spread of the metrics over three mesh densities and over Q1/Q2. **Q1 does not apply with a
medium:** the judge's HuHu-LuLu regularization (and the planned regularization slot) needs second derivatives, which
Q1 elements do not have, and an unregularized soft medium fails Newton (step 1). The Q2 part,
`evaluate.hertz_mesh_sensitivity`: C2 at (nx, ny) = (24, 12), (32, 16), (48, 20), spread max − min per metric.
Zoo neo-Hooke (cloud, 2026-11-03):

| γ | a_err | p0_err | p_l2 | leak_out | time per mesh |
|---|---|---|---|---|---|
| 1e-5 | +12.2 / +12.3 / +12.4 % | +0.07 / +0.12 / +0.20 % | 6.1 / 5.0 / 4.7 % | 0.7 / 1.6 / 2.1 % | 6.7 / 6.9 / 12.7 s |
| 1e-6 | −3.8 / −3.9 / −3.5 % | +0.72 / +0.85 / +0.77 % | 6.7 / 10.4 / 4.7 % | 0.5 / 1.1 / 1.8 % | 6.5 / 9.2 / 17.4 s |

Classical at (48, 20): a +0.2 %, p0 −0.3 %, p_l2 2.1 %. **a_err and p0_err are mesh-stable** (spread ≤ 0.4 points),
fit for Target D thresholds. **p_l2 is not** (the node-to-node zigzag of soft media, see the pressure plot) and
**leak_out grows with refinement** (the regularization's spurious tension is resolved better); thresholds on them
need the fine mesh or a margin above the spread. mesh_sens costs about 30 s per medium: promo only (step 4).

## Step 4: hard constraints, held-out families, promo

**Hard constraints (complete for the medium slot):** on the 40 deformation probes, in addition to the step-1 checks,
the tangent (Hessian w.r.t. C) is finite; the energy is non-negative (rest is the minimum); it is strictly positive
for det F < 1 (the medium resists compression); and it scales with the moduli: ψ(C, cμ, cλ, γ) = c ψ(C, μ, λ, γ) to
1e-9 for c = 1e-6, 1e6 (an absolute constant or epsilon fails; Arena 1's v1.5 lesson). Batch independence holds by
construction: felupe.constitution.jax maps ψ over cells and quadrature points, so a candidate sees one C at a time.

**Held-out families** (`families.py`; seed ~/.schemeforge/heldout_seed, never read in the cloud session; salt
"contact"):

| Family | n | Instance parameters (random per instance) |
|---|---|---|
| GF gap closure | 10 | gap 0.03–0.2, height 0.6–1.5, width 0.1–0.4, push = gap + 2–8 % of height, 8 steps, 2–4 medium rows, E 0.1–10 (log), ν 0.15–0.45, γ 1e-6–1e-3 (log), distortion 0–0.35 |
| SF simple shear | 10 | shear 0.1–3, E, ν, γ as GF |
| HF Hertz | 6 | R 0.5–2 (log), W = H = R, gap 0.15–0.3 % of R, indentation 0.3–0.5 % of R beyond the gap, 12 steps, 28–36 columns, E, ν as GF, γ 1e-6–1e-5 (log) |
| HX Hertz | 1 | as HF; adds mesh_sens_* (three meshes) and `max_step` = 1 / fewest of 1, 2, 3, 4, 6, 8, 12 equal steps that converge |

Promo report: family aggregates (n, pass rate; per metric median, mean, p90, worst; `converged` and `max_step` are
higher-is-better), seed fingerprint; instances are stripped by the parent and stored outside the repo. A test-seed
run with the zoo neo-Hooke (not the real seed) takes 114 s; every instance converges; HX: max_step 0.5,
mesh_sens_a_err 0.0014.

## Known limits

- The unconfined C0a (free sides) with an unregularized γ = 1e-6 medium fails Newton: the medium bulges sideways.
  The dev cases are confined; the unconfined case belongs with the regularization slot.
- C0b measures the material law only; C4 measures shear in contact geometry (small frictionless sliding).

## Audit (step 6): `sforge judge exact --arena contact`

`uv run sforge judge exact --arena contact --case <yaml> --json` answers one case, or a YAML list of cases with a JSON
list. The case format is in docs/judge/contact_cases.md. The **audit medium** is the zoo neo-Hooke,
ψ_m(C) = γ ψ_b(C) with the body's μ and λ (ψ_b as in §Slot). All forces are per unit thickness and compressive
positive. Reported per kind:

- `gap_closure` (C0a, and C1 when `distort` > 0):
  - `ideal_force`: the ideal contact force at full push (§C0a).
  - `exact_force`, `exact_thickness`: the exact homogeneous solution with the audit medium at full push.
  - `exact_force_half`, `exact_thickness_half`: the same at push = g/2.
  - `exact_leak_pre`, `exact_gap_res`, `exact_force_err`: the metrics of §C0a, computed from the exact solution.
  - `fe_push`, `fe_force`: the judge's FE solve with the audit medium (load steps, including 0). Also `fe_thickness`
    (at the symmetry line, x = 0), `fe_wall_pressure` (wall nodes sorted by x) and the judge's metrics `fe_leak_pre`,
    `fe_gap_res`, `fe_force_err`, `fe_pressure_spread` and `fe_min_J_medium`.
  - `classical_push`, `classical_force`: the classical reference extrapolated to infinite penalty, per load step.
- `simple_shear` (C0b): `mu`, `lmbda`, `P_xy`, `P_yy`, `shear_parasitic` and `normal_parasitic` for the audit medium.
- A gap closure or Hertz case whose Newton solve fails is answered with {kind, id, converged: 0}. Every other
  report carries converged: 1.
- `sliding` (C4): the classical reference (no medium): `ft` and `fn` per recorded state (press from zero load,
  then slide), `n_press` = steps + 1, and `shear_parasitic` and `fn_rise` computed on it (ideal 0).
- `hertz` (C2): the classical reference (no medium; penalty 1e3):
  - `x`, `f`: the reference x of the contact nodes on the flat, sorted, and their consistent nodal forces (half model);
  - `p`: the recovered pressure (§C0a, consistent mass matrix);
  - `load` P of the full model, `E_star`, `a_hertz`, `p0_hertz`;
  - the judge's metrics `a_err`, `p0_err`, `p_l2` and `leak_out` computed on this solution.

  Classical vs Hertz is the judge error floor of §C2, not round-off.

`sforge judge verify --arena contact` runs the judge's self-checks:
- quadratic edge tractions come back exactly;
- on the dev C0a and C1 cases, FE vs exact to 1e-9, classical vs ideal to 1e-9, zero force before contact, and
  pressure spread ≤ 1e-7;
- C0b with the neo-Hooke medium gives P_xy/(μ s) = γ;
- classical Hertz on the dev mesh: |a_err| ≤ 1.5 % and |p0_err| ≤ 1 %;
- every zoo member passes the hard constraints.
