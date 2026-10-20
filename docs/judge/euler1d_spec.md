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

## 4. Reference geometry

Anderson (1995) nozzle: A(x) = 1 + 2.2 (x − 1.5)², x ∈ [0, 3], throat at x = 1.5, A_e/A_t = 5.95.
Reference values: PLAN Appendix H.

## 5. Unsteady and steady solvers *(planned)*
## 6. Cases and families *(planned; format in euler1d_cases.md)*
## 7. Metrics *(planned)*
