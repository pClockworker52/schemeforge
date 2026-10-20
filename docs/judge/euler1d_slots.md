# Arena 1 slot contracts (euler1d)

The engine pastes these contracts into its prompts; proposers follow them. A candidate is one Python file that
defines the slot's function. All arrays are float64. Use only `jax.numpy`, `jax.lax` and `math`
(`import jax.numpy as jnp`, `from jax import lax`, `import math`), no I/O, no hidden state, no Python loops over
cells, deterministic. Module-level values must be numeric constants (or tuples of them); helper functions are
allowed; decorators, classes, `global`, mutable default arguments and attribute assignment are rejected.
Size limit: 150 lines.

Phase 1 implements `limiter` and `flux`. The other contracts are fixed but built when a target needs them.

## `limiter` — MUSCL slope limiter (active)

```python
def phi(r):
    """r: array of slope ratios (any shape). Return phi(r), same shape, finite for every finite r
    (including r <= 0 and very large |r|). TVD and second-order properties are measured, not required."""
```

How the judge uses it, per primitive variable q ∈ {ρ, u, p} and cell i:
- Δ₋ = q_i − q_{i−1}, Δ₊ = q_{i+1} − q_i, r = Δ₋/Δ₊ (r = 0 where Δ₊ = 0), clipped to [−1e10, 1e10];
- slope σ_i = φ(r) Δ₊; face states q_{i+½}⁻ = q_i + σ_i/2 and q_{i−½}⁺ = q_i − σ_i/2.
- Default flux: HLLC with Einfeldt wave speeds; time integration SSP-RK3; nozzle pseudo-time as in the spec.

Notes: φ(r) = r φ(1/r) (symmetry) makes the scheme mirror-symmetric; it is measured, not required.
φ(1) = 1 and Sweby's TVD region are measured too.

## `flux` — numerical flux (active)

```python
def flux(UL, UR, gamma):
    """UL, UR: (m, 3) conserved [rho, rho*u, E]. Return F: (m, 3). Must satisfy flux(U, U) == F(U)."""
```

Hard constraints: consistency flux(U, U) = F(U) to 1e-12 and mirror symmetry
flux(R·U_R, R·U_L) = −R·flux(U_L, U_R) with R = diag(1, −1, 1). Reconstruction: MUSCL with the van Leer limiter.

## `limiter_stateful` (planned, seed hunch 2)

```python
def phi_s(r, state):
    """state has the same shape as r and starts at 0. Return (phi, new_state)."""
```

## `reconstruction` (planned, seed hunches 3–5)

```python
def reconstruct(W, gamma):
    """W: (n + 6, 3) primitive [rho, u, p], including 3 ghost cells per side.
    Return (WL, WR), each (n + 1, 3): the states left and right of interfaces 0..n."""
```

The implicit nozzle solver assumes that a cell's residual depends only on cells within ±3; a reconstruction
that reaches further gets a less accurate Newton Jacobian (slower convergence, same converged solution).

## `operator` (planned, Target B)

```python
def fluxes_and_source(U, A_face, dx, gamma, ghosts):
    """U: (n, 3) quasi-1D conserved [rho*A, rho*u*A, E*A]; A_face: (n + 1,); ghosts: boundary data built by the judge.
    Return (F_face: (n + 1, 3), S_mom: (n,)). The judge assembles dU/dt = -(F[1:] - F[:-1]) / dx + [0, S_mom, 0],
    so mass and energy conservation hold by construction."""
```
