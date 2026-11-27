# Arena 2 slot contracts (contact)

The engine pastes these contracts into its prompts; proposers follow them. A candidate is one Python file that
defines the slot's function. All arrays are float64. Use only `jax.numpy`, `jax.lax` and `math`
(`import jax.numpy as jnp`, `from jax import lax`, `import math`), no I/O, no hidden state, no Python loops over
quadrature points or cells, deterministic. Module-level values must be numeric constants (or tuples of them); helper
functions are allowed; decorators, classes, `global`, mutable default arguments and attribute assignment are
rejected. Size limit: 150 lines. `lax.stop_gradient` is rejected. Judge: contact-v1.0; spec docs/judge/contact_spec.md.

## `medium` — strain energy of the third medium (active)

```python
def psi_medium(C, p):
    """C: (3, 3) right Cauchy-Green tensor of the medium (plane strain: C[2, 2] == 1). p: dict with the body's Lamé
    moduli p["mu"], p["lmbda"] [force/area] and the medium stiffness scale p["gamma"] [-], set by the case.
    Return the strain energy per unit reference volume [force/area], a float64 scalar."""
```

How the judge uses it:
- The medium fills the gap between the bodies (and between a body and a rigid flat). The judge differentiates ψ with
  JAX (stress and tangent) and calls it once per quadrature point. Plane strain, bi-quadratic quads, felupe 11.3. The
  function only ever sees one C, so it cannot depend on the batch.
- Bodies are compressible neo-Hookean, ψ_b = μ/2 (tr C − 3) − μ ln J + λ/2 ln² J. The medium sees the body's μ and λ
  and the case's γ. How ψ scales with γ is the candidate's choice.
- The judge adds a fixed HuHu-LuLu Hessian regularization of the medium (kr · λ · W², kr = 5e-7) on the Hertz and
  sliding cases. It is not part of the slot.
- ψ depends on C alone. It cannot see the contact normal, the gap thickness, the load step or any history.

**Hard constraints** (reject), on 40 fixed plane-strain deformations (rest; uniaxial thickness ratios 1e-3 … 5;
simple shear 0.1, 1, 5; random with det F in [1e-3, 10]) at μ, λ of E = 1, ν = 0.3 and γ = 1e-3:
- the energy is a float64 scalar; it, dψ/dC and the tangent are finite; repeated calls are bitwise equal;
- ψ ≥ 0, and ψ > 0 whenever det F < 1 (the medium must resist compression);
- ψ(I) = 0 and dψ/dC(I) = 0 to 1e-12 · μγ;
- unit scaling: ψ(C; c μ, c λ, γ) = c ψ(C; μ, λ, γ) to 1e-9 for c = 1e-6 and 1e6. An absolute constant or epsilon
  breaks this.

**Dev suite** (what the engine selects on): C0a gap closure at γ = 1e-3, 1e-5, 1e-6 (leak_pre, gap_res, force_err,
newton_iters, converged); C0b simple shear at s = 0.5 and 2 (shear_parasitic); C2 Hertz at γ = 1e-5 and 1e-6 (a_err,
p0_err, newton_iters, converged); C1 patch test (pressure_spread); C4 frictionless sliding at γ = 1e-6
(shear_parasitic, fn_rise, converged). Objectives and the Target D dev screen: src/schemeforge/engine/objectives.py.

**Target D** (docs/targets/D.md) is judged on the held-out families: tight (GF gap_res), robust (HF converged and
max_step in one load step), accurate (HF |a_err|, |p0_err| ≤ 2 %), and no worse than the robust zoo member on leak before
contact, parasitic shear and sliding. The zoo's front over γ is the reference. A candidate that only rescales a zoo member is
that zoo member at another γ.
