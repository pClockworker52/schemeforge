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
  medium thickness g s_m. Bi-quadratic elements represent it exactly; the FE result agrees to 1e-9 or better
  (measured 1e-12 … 1e-16 except where the force is below 1e-6, where Newton's absolute tolerance 1e-10 dominates).
- Ideal contact: F = 0 for d ≤ g; F = −w P_b((h − (d − g))/h) for d > g.
- Metrics: `leak_pre` = F(g/2) / F_ideal(push); `gap_res` = medium thickness at full push / g; `force_err` =
  F(push) / F_ideal(push) − 1 (positive: the remaining layer takes up height, so the body is compressed more);
  `newton_iters` (sum over steps); `min_J_medium`; `converged` (0 if Newton fails: a result, not a violation).
- Run-level violation: min J of the medium ≤ 0.
- Contact pressure on the wall: nodal reactions solved against the consistent mass matrix of the quadratic edge
  elements (`metrics.edge_traction`), so a uniform pressure comes back exactly (F / w here).
- Classical reference: the body alone over a rigid plane with felupe's frictionless `ContactRigidPlane`; the penalty
  error (∝ 1/k) is removed by Richardson extrapolation over k = 1e2, 1e3, 1e4. Reproduces the ideal force to 2e-10
  and gives exactly zero force before contact.

Dev cases: C0a-g3, C0a-g5, C0a-g6 with γ = 1e-3, 1e-5, 1e-6; h = 1, w = 0.2, g = 0.1, push = 0.15, 6 steps, E = 1,
ν = 0.3, one cell across, 2 cells in the body and 2 in the medium. Smoke: the γ = 1e-3 case.

## C0b, simple shear

The medium alone in F = [[1, s, 0], [0, 1, 0], [0, 0, 1]], evaluated directly: P = 2 F dψ/dC at C = FᵀF.
Metrics: `shear_parasitic` = P_xy / (μ s), the medium's shear stress relative to the body's linear one (0 ideal;
exactly γ for the scaled neo-Hookean); `normal_parasitic` = P_yy / (μ s). Dev cases C0b-s05 and C0b-s2: s = 0.5 and
2, γ = 1e-5.

## Known limits

- The unconfined C0a (free sides) with an unregularized γ = 1e-6 medium fails Newton: the medium bulges sideways.
  The dev cases are confined; the unconfined case belongs with the regularization slot.
- C0b measures the material law only; shear in contact geometry follows with C4 (steady sliding, no friction).
