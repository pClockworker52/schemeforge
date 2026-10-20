# Arena 1 judge spec (euler1d)

This spec is the only input for the blind audit (PLAN §9.10). The judge-auditor re-implements everything here
from this file and textbook formulas, without reading `src/schemeforge/arenas/`. Sections marked *(planned)* are
filled in as Phase 1 proceeds.

## 1. Conventions

- Ideal, calorically perfect gas; all quantities nondimensional; float64 throughout.
- Primitive state W = (ρ, u, p). Conserved state U = (ρ, ρu, E) with E = p/(γ−1) + ρu²/2.
  Flux F(U) = (ρu, ρu² + p, (E + p)u). Sound speed a = √(γp/ρ).
- Specific entropy (up to constants): s = ln(p/ρ^γ)/(γ−1).
- γ values: 1.4, 5/3, 1.405, and 1.2 as a stress value.

## 2. Exact Riemann solution (Toro 2009, ch. 4)

Input: W_L, W_R, γ, with ρ, p > 0.

1. **Vacuum.** If (2/(γ−1))(a_L + a_R) ≤ u_R − u_L, the data are rejected (vacuum generation). Such data never
   appear in any family.
2. **Pressure function** for K ∈ {L, R}:
   - shock (p > p_K): f_K(p) = (p − p_K) √(A_K/(p + B_K)), A_K = 2/((γ+1)ρ_K), B_K = (γ−1)/(γ+1) p_K;
   - rarefaction (p ≤ p_K): f_K(p) = (2a_K/(γ−1)) [(p/p_K)^((γ−1)/(2γ)) − 1].
3. **Star pressure.** p* is the unique root of f(p) = f_L(p) + f_R(p) + (u_R − u_L) on (0, ∞). Solve to full double
   precision (relative error ≲ 1e-15).
4. **Star velocity.** u* = (u_L + u_R)/2 + (f_R(p*) − f_L(p*))/2.
5. **Star densities.** Shock: ρ*_K = ρ_K [(p*/p_K) + (γ−1)/(γ+1)] / [((γ−1)/(γ+1))(p*/p_K) + 1].
   Rarefaction: ρ*_K = ρ_K (p*/p_K)^(1/γ).
6. **Wave speeds.** Shock: S_L = u_L − a_L Q_L, S_R = u_R + a_R Q_R with
   Q_K = √((γ+1)/(2γ) · p*/p_K + (γ−1)/(2γ)).
   Rarefaction: head S_HL = u_L − a_L, tail S_TL = u* − a*_L; head S_HR = u_R + a_R, tail S_TR = u* + a*_R,
   with a*_K = a_K (p*/p_K)^((γ−1)/(2γ)).
7. **Sampling** at ξ = (x − x₀)/t. Left of the contact (ξ < u*): W_L outside the left wave, the left star state
   (ρ*_L, u*, p*) inside it. Right of the contact (ξ ≥ u*): symmetric. Inside a left fan (S_HL < ξ < S_TL):
   - c = 2/(γ+1) + (γ−1)/((γ+1)a_L) (u_L − ξ)
   - ρ = ρ_L c^(2/(γ−1)), u = (2/(γ+1)) (a_L + (γ−1)u_L/2 + ξ), p = p_L c^(2γ/(γ−1)).

   Inside a right fan (S_TR < ξ < S_HR):
   - c = 2/(γ+1) − (γ−1)/((γ+1)a_R) (u_R − ξ)
   - ρ = ρ_R c^(2/(γ−1)), u = (2/(γ+1)) (−a_R + (γ−1)u_R/2 + ξ), p = p_R c^(2γ/(γ−1)).

   Points exactly on a wave boundary take the value of the inner (star) side; points exactly on the contact take
   the right star state.

## 3. Exact steady quasi-1D nozzle

Input: area A(x) on [x_in, x_exit] with a single throat x_t (A_t = A(x_t) is the minimum), back pressure
p_b/p₀ ∈ (0, 1), γ. Stagnation state upstream: p₀ = ρ₀ = 1, so T/T₀ = (p/p₀)/(ρ/ρ₀) and a₀ = √γ. The inlet is
subsonic.

**Isentropic relations,** with Ψ(M) = 1 + (γ−1)M²/2:
- A/A* = (1/M) [(2/(γ+1)) Ψ(M)]^((γ+1)/(2(γ−1)))
- p/p₀ = Ψ^(−γ/(γ−1)), ρ/ρ₀ = Ψ^(−1/(γ−1)), T/T₀ = Ψ^(−1), u = M a, a = a₀ √(T/T₀).

**Normal shock** at upstream Mach M₁:
- p₂/p₁ = 1 + 2γ/(γ+1) (M₁² − 1)
- M₂² = (1 + (γ−1)M₁²/2) / (γM₁² − (γ−1)/2)
- p₀₂/p₀₁ = [(γ+1)M₁² / ((γ−1)M₁² + 2)]^(γ/(γ−1)) · [(γ+1) / (2γM₁² − (γ−1))]^(1/(γ−1))
- T₀ is continuous, so ρ₀₂/ρ₀₁ = p₀₂/p₀₁, and A*₂ = A*₁ · p₀₁/p₀₂.

**Critical back pressures** (with A_e = A(x_exit)):
- p_crit1 = p/p₀ at the subsonic root of A_e/A_t (choked, subsonic exit);
- p_crit3 = p/p₀ at the supersonic root of A_e/A_t (design condition);
- p_crit2 = p_crit3 · p₂/p₁(M_e,sup) (normal shock exactly at the exit).

**Regimes:**
- p_b/p₀ > p_crit1: subsonic everywhere, not choked. M_e from p_b/p₀ = Ψ(M_e)^(−γ/(γ−1)); A* = A_e / (A/A*)(M_e);
  M(x) is the subsonic root of A(x)/A* everywhere.
- p_crit2 < p_b/p₀ ≤ p_crit1: choked with a normal shock at x_s ∈ (x_t, x_exit). Upstream of the throat M is
  subsonic, between throat and shock supersonic (A* = A_t), downstream subsonic with A*₂ and p₀₂. x_s is the
  unique root of p_exit(x_s) = p_b, where p_exit(x_s) = p₀₂/p₀₁ · (p/p₀)(M_e), M_e the subsonic root of A_e/A*₂.
- p_b/p₀ ≤ p_crit2: subsonic upstream of the throat, supersonic downstream, no shock inside the nozzle; the exit
  pressure is p_crit3 (the shocks or expansions that match p_b stand outside and are not modelled).

At x = x_t in the choked regimes, M = 1. A point exactly at x_s takes the upstream state.

## 4. Geometries

- **anderson** (Anderson 1995): A(x) = 1 + 2.2 (x − 1.5)², x ∈ [0, 3], throat at x = 1.5, A_e/A_t = 5.95.
  Reference values: PLAN Appendix H.
- **parabolic** (parameters area_ratio R, length L, inlet_ratio Rᵢ, x_in): throat at x = 1 with A = 1;
  A = 1 + (Rᵢ − 1)(1 − x)² for x < 1 and A = 1 + (R − 1)((x − 1)/L)² for x ≥ 1; domain [x_in, 1 + L].
- **conical** (same parameters): the same convergent part; for x ≥ 1, A = r², r = 1 + k(√((x−1)² + δ²) − δ)
  with δ = 0.2 and k = (√R − 1)/(√(L² + δ²) − δ), so that A(1 + L) = R.

x_in only moves the inlet within (or before) the convergent part; the choked flow does not depend on it.
The grid has n uniform cells on [x_in, x_exit]; "cell centres" are x_in + (i + ½)(x_exit − x_in)/n.

`sforge judge exact --arena euler1d --case FILE --json` prints the judge's solution for one case (or a JSON list
for a YAML list of cases). Riemann: p_star, u_star, rho_star_L/R, waves, and x, rho, u, p at the cell centres
of the case grid at t_end. Nozzle: regime, x_shock, M1, p0_ratio, A_star_1/2, mass_flow, p_crit1..3, and
x, M, rho, u, p at the cell centres.

## 5. Solvers

The solvers are not part of the blind audit (only the exact solutions are), but candidates are scored through
them, so their conventions are fixed here. Slot interfaces: `euler1d_slots.md`.

### 5.1 Common pieces
- Uniform grid, cell centres x_i, 3 ghost cells per side.
- Default reconstruction: MUSCL on primitive variables with the limiter slot (slot doc for the slope formula).
- Default flux: HLLC (Toro §10.4) with Einfeldt wave speeds S_L = min(u_L − a_L, ũ − ã),
  S_R = max(u_R + a_R, ũ + ã), where ũ, H̃ are Roe averages and ã² = (γ−1)(H̃ − ũ²/2).

### 5.2 Unsteady 1D
- Boundaries: transmissive (ghost = edge cell) or periodic.
- SSP-RK3 with global dt = CFL·dx / max(|u| + a), CFL 0.5 by default; the last step is shortened to hit t_end.

### 5.3 Steady quasi-1D nozzle
- Cell areas A_i = A(x_i), face areas A_{i±½} = A(x_{i±½}); unknowns U_i = (ρA, ρuA, EA)_i.
- dU_i/dt = −(F_{i+½}A_{i+½} − F_{i−½}A_{i−½})/dx + (0, p_i (A_{i+½} − A_{i−½})/dx, 0). Flow at rest is balanced.
- Inlet ghosts: p₀ = T₀ = 1 imposed; the outgoing invariant J⁻ = u − 2a/(γ−1) is taken from the first cell, and
  u_in is the root with a > 0 of a² + (γ−1)u²/2 = γ, a = (γ−1)(u − J⁻)/2. Then T = 1 − (γ−1)u²/(2γ),
  p = T^(γ/(γ−1)), ρ = p/T.
- Outlet ghosts: if p_b > p_crit2 (pressure outlet, decided from geometry and p_b only) or the last cell is
  subsonic: p = p_b, entropy and J⁺ = u + 2a/(γ−1) from the last cell; otherwise all variables from the last
  cell. Forcing p_b while the transient is locally supersonic keeps the shock inside: with plain extrapolation a
  shock near the exit can leave during the transient, and the discrete problem then settles on a spurious
  supersonic-exit steady state.
- Initial guess (depends on geometry and the regime of p_b only, never on the case's own exact solution):
  for p_crit2 < p_b ≤ p_crit1 the exact flow with a standing shock at x_t + (x_exit − x_t)/2; otherwise
  isentropic with p linear from 1 (inlet) to p_b (exit), ρ = p^(1/γ), u from the energy equation. The isentropic
  guess has a supersonic exit, which let shocks near the exit escape for good in the shock regime.
- Known limit: the explicit solver still loses shocks within about 2 % of the divergent length from the exit
  (x_s = 2.95 on the Anderson nozzle); families keep shocks within 15–90 % of the divergent length.
- Residual R_k: L2 norm over all cells and components of dU/dt, reported as R_k/R_0. Converged: R_k/R_0 ≤ 1e-12.
- Explicit: SSP-RK3 with local dt_i = 0.8·dx/(|u_i| + a_i), at most 50,000 iterations.
- Implicit: backward Euler, (diag(1/dt_i) − ∂R/∂U) ΔU = R(U), exact Jacobian (forward mode, coloured with a
  ±3-cell stencil), dense LU. dt_i as above with CFL_k = min(1e8, s·R_0/R_k); a non-physical update is rejected
  and s is multiplied by 0.25 (12 consecutive rejections = failure), each accepted step doubles s up to 1.
  At most 300 linear solves, rejected ones included.
- Limit cycle: not converged, the median residual over the last 5 % of iterations is at least 0.9× that over the
  5 % before, and the residual still varies by more than 1 % within the last 10 %.
## 6. Cases and families *(planned; format in euler1d_cases.md)*
## 7. Metrics

Lower is better unless noted. Implemented in `arenas/euler1d/metrics.py`.

**Jumps of a Riemann solution.** Shocks and contacts of nonzero strength (|p*/p_K − 1| > 1e-12, resp.
|ρ*_L/ρ*_R − 1| > 1e-12) at t_end. Each has a window bounded by the midpoints to the neighbouring features (shock
positions, contact, rarefaction heads and tails) or the domain ends. Shocks are measured in p, contacts in ρ;
a and b are the exact values left and right of the jump. Width and overshoot are measured only for resolved
jumps: at least 8 cells of window on each side and |b − a|/max(|a|, |b|) ≥ 0.05; otherwise they are skipped
for that case (features a few cells apart, e.g. R3's contact and shock at N = 200, are not separable).

| Metric | Definition |
|---|---|
| `l1_smooth` | Mean over ρ, u, p of mean\|W − W_exact\| / scale over cells more than 5 cells from every jump (nozzle: from the shock). Scales: max\|ρ\|, max(\|u\| + a), max\|p\| of the exact solution. |
| `order_smooth` | S1: log(e₅₀/e₂₀₀)/log 4 with e = L1 density error at t = 1 (higher is better). |
| `shock_width`, `contact_width` | In the window, f = (q − a)/(b − a). x_hi: first cell with f ≥ 0.95; x_lo: last cell before it with f ≤ 0.05; both linearly interpolated; width = (x_hi − x_lo)/dx. If the transition never completes: the window width in cells. Mean over jumps of that kind. Nozzle: window ±12 cells around x_s, a = p just upstream, b = p just downstream. |
| `overshoot` | Largest excursion of q beyond [min, max] of the exact values in the window, divided by \|b − a\|; max over jumps. |
| `tv_increase` | max over ρ, p of (TV(q) − TV(q_exact))/TV(q_exact), floored at 0, TV on cell values at t_end. |
| `shock_pos_err` | \|x_s,num − x_s\|/dx; x_s,num is where p first rises through (p₁ + p₂)/2 downstream of the pressure minimum (linear interpolation). |
| `mdot_var` | max over cells \|ρuA / ṁ_exact − 1\|. |
| `h0_var` | max over cells \|h₀/h₀,exact − 1\|, h₀ = γ/(γ−1) p/ρ + u²/2, h₀,exact = γ/(γ−1). |
| `entropy_spurious` | max(0, max over cells more than 5 cells from the shock of s − s_exact). |
| `res_orders_expl` | −log₁₀ of the smallest R_k/R₀ reached by the explicit solver (higher is better). |
| `newton_iters` | linear solves of the implicit solver until R_k/R₀ ≤ 1e-12 (300 if not reached). |
| `limit_cycle` | the explicit solver's flag (§5.3). |
| `roughness_J` | J = Σ over cells with x_i > x_t of p_i (A_{i+½} − A_{i−½}); J_exact = ∫ p dA/dx over [x_from, x_exit], x_from the left face of the first such cell. roughness = RMS(Δ²(J − J_exact))/RMS(Δ²J_exact) over the sweep. |
| `cost` | wall time per cell update, normalized to the zoo median (computed by the evaluator). |

## 8. Hard constraints and metamorphic tests

**Hard (reject):** on fixed probe sets (`constraints.py`):
- limiter: output shape and dtype, finite for all probe r (negative, zero, tiny, huge, ±1e10), bitwise
  deterministic, pointwise (permuted input gives permuted output; reshaping does not matter);
- flux: finite on 256 fixed admissible state pairs, consistency max\|flux(U, U) − F(U)\|/max\|F\| ≤ 1e-12,
  mirror symmetry \|flux(RU_R, RU_L) + R·flux(U_L, U_R)\| ≤ 1e-12 · max(\|F_num\|, \|F(U_L)\|, \|F(U_R)\|) per
  row, deterministic, row-wise;
- every run: finite output, ρ > 0, p > 0, and no solver failure.

**Measured, not required** (`metamorphic.py`, on R1): mirror symmetry of the whole run (exact for symmetric
limiters, not for Koren), scaling homogeneity (ρ, p, E) → 10·(ρ, p, E), Galilean shift by 10 cells.
