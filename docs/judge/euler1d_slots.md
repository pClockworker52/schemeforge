# Arena 1 slot contracts (euler1d)

The engine pastes these contracts into its prompts; proposers follow them. A candidate is one Python file that
defines the slot's function. All arrays are float64. Use only `jax.numpy`, `jax.lax` and `math`
(`import jax.numpy as jnp`, `from jax import lax`, `import math`), no I/O, no hidden state, no Python loops over
cells, deterministic. Module-level values must be numeric constants (or tuples of them); helper functions are
allowed; decorators, classes, `global`, mutable default arguments and attribute assignment are rejected.
Size limit: 150 lines. `lax.stop_gradient` is rejected.

Since judge v1.1 the judge calls a limiter with one slope ratio at a time (a 0-d array) and a flux with one
interface at a time ((1, 3) arrays), so code must not depend on the batch: its size, shape, order or statistics.
The hard constraints reject code whose batch output differs from its one-at-a-time output.

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

## `limiter_stateful` — MUSCL slope limiter with memory (active since judge v1.2)

```python
def phi_s(r, s):
    """r: slope ratios, s: limiter state, same shape (one value per slope ratio), s = 0 at the start.
    Return (phi, s_new), both of r's shape, finite for every finite r and s."""
```

How the judge uses it: as the `limiter` slot (σ = φ Δ₊, HLLC, SSP-RK3), with one state value per cell and primitive
variable. Within a step the state is fixed: all three RK stages, and the Newton Jacobian, use the state from the
start of the step; s_new from the step's first evaluation replaces it once the step is accepted. Steps are time
steps (unsteady cases), explicit pseudo-time iterations and accepted Newton steps (at most 300); a rejected Newton
step keeps the old state. Hard constraints as for `limiter`, on (r, s) pairs with s = 0, s of order one and s up to
1e6, plus a finite s_new; elementwise in (r, s) pairs. Zoo: stateless limiters with the state passed through, and
limiter freezing (`superbee_frozen`, `van_leer_frozen`: the centred factor ψ = 2φ/(1+r) is fixed after 1000 steps).

## `reconstruction` (hard constraints since judge v1.3.dev; seed hunches 3–5)

```python
def reconstruct(W, gamma):
    """W: (n + 6, 3) primitive [rho, u, p], including 3 ghost cells per side.
    Return (WL, WR), each (n + 1, 3): the states left and right of interfaces 0..n."""
```

Interface k separates padded cells k + 2 and k + 3. Since judge v1.3 runs call the reconstruction one interface
at a time: each call gets the 6 cells k..k+5 around one interface (a (6, 3) array, i.e. n = 0) and returns
(1, 3) arrays (`numerics.stencilwise`). So code must work for n = 0, may use only those 6 cells, and must not
depend on the grid size, its statistics or the position of the interface. This also keeps a cell's residual
within ±3 cells, the stencil the implicit solver's Jacobian assumes.

Hard constraints (`constraints.check_reconstruction`): the right shapes, float64, finite and deterministic on
random admissible grids, step profiles and smooth waves of run-like sizes (1–404 interfaces); a constant state
is reproduced to 1e-12 relative; and the output on those grids equals the one-interface-at-a-time output to
1e-13 relative ("not local" otherwise). Zoo: `first_order`, `weno5z`; MUSCL with any zoo limiter also passes.

## `operator` (planned, Target B)

```python
def fluxes_and_source(U, A_face, dx, gamma, ghosts):
    """U: (n, 3) quasi-1D conserved [rho*A, rho*u*A, E*A]; A_face: (n + 1,); ghosts: boundary data built by the judge.
    Return (F_face: (n + 1, 3), S_mom: (n,)). The judge assembles dU/dt = -(F[1:] - F[:-1]) / dx + [0, S_mom, 0],
    so mass and energy conservation hold by construction."""
```
