# Phase 6 tooling spike: FElupe for third-medium contact (2026-10-30, cloud session)

PLAN §14.1: reproduce FElupe's third-medium contact example, time a 2D plane-strain Hertz case with Q2 elements at
about 10,000 DOF, and choose between FElupe and custom JAX. Machine: cloud container, 4 cores, 15 GB. FElupe 11.3.0,
tensortrax 0.30.0, JAX 0.12, Python 3.12, in a separate venv (not the project's). Scripts:
`scripts/spikes/phase6_felupe_ex20_headless.py`, `scripts/spikes/phase6_hertz_felupe.py`. These are spike timings,
not judge runs, so they have no run ids.

## Results

**1. The example reproduces.** FElupe's `ex20_third-medium-contact.py` (Bluhm–Sigmund–Poulios neo-Hookean medium,
γ0 = 5e-6, HuHu-LuLu Hessian regularization, Q2 quads, line search) runs headless to the full 0.62 L push in 6
substeps, with line-search cutbacks in the last two, in 1.4 s.

**2. Hertz case** (`phase6_hertz_felupe.py`). Symmetric half model: lower block 1 × 1, upper body with a parabolic
surface (R = 1) 0.002 above it, medium in the gap. E = 1, ν = 0.3, mesh graded towards the contact, bottom fixed,
top pushed down by 0.006 in total.

| Mesh (nx, ny body, ny medium) | DOF | Load steps | Newton iterations | Wall time | Peak memory | a from P (Hertz) | a from medium thickness |
|---|---|---|---|---|---|---|---|
| 12, 6, 3 | 1,560 | 4 | 36 | 1.5 s | – | 0.0449 | 0.0276 |
| 32, 16, 4 | 9,508 | 4 | 42 | 11.6 s | 181 MB | 0.0454 | 0.0477 |
| 32, 16, 4 | 9,508 | 8 | 55 | 14.6 s | 182 MB | 0.0454 | 0.0477 |
| 48, 24, 6 | 21,174 | 8 | 55 | 40.5 s | 294 MB | 0.0454 | 0.0523 |

About 0.26 s per Newton iteration at 9.5k DOF, 0.74 s at 21k. The reaction force is mesh-independent to three
digits (Fy = 8.90e-4 / 8.90e-4 / 8.90e-4 per unit length); a/R ≈ 0.045 and the block is 22 a wide, inside Hertz's
validity range (PLAN §14.2). The two contact half-widths disagree by 5–15 %, and the thickness-based estimate gets
worse with refinement. That criterion (medium thinner than 25 % of the initial gap) is a rough stand-in. The judge
needs the contact pressure itself, from the block's surface traction, before any Hertz number can be trusted
(metrics `p0_err`, `a_err`, `p_l2`).

**3. Candidate energies in `jax.numpy` work.** With the medium's neo-Hookean energy written as a plain
`jax.numpy` function of C = FᵀF (`felupe.constitution.jax.Hyperelastic`, automatic differentiation by JAX), the
9.5k-DOF case gives the identical Newton iteration sequence (1, 2, 13, 15, 11) and reaction force. It takes 14.9 s
instead of 10.9 s (JIT compilation) and 483 MB. An energy in terms of C is frame-indifferent by construction, which
removes one of the attack surfaces the slot contract planned to test (PLAN §14.3).

## Against the spike's criteria

| Criterion (PLAN §14.1) | Result |
|---|---|
| dev suite ≤ 60 s per candidate | **plausible, not shown.** One Hertz case at 9.5k DOF takes 11–15 s. Six to eight cases fit only at 3–6k DOF each, and `max_step` by bisection must be cheap or move to promo. |
| AD of user energy functions | **yes**, by JAX, with the candidate in `jax.numpy` (iron rule 4 holds unchanged) |
| Q2 elements | **yes** (`RegionBiQuadraticQuad`) |
| Hessian (second-gradient) regularization | **yes**, as weak forms (HuHu-LuLu in the example). A candidate `psi_reg(F, gradF)` slot needs a custom form: more work than the medium slot. |
| memory | 0.2–0.5 GB per worker, against 4.4 GB for Arena 1's stateful reconstructions: parallel evaluation is not memory-bound |

**Technical recommendation: FElupe**, not custom JAX. It meets every criterion that was tested, the candidate
interface stays `jax.numpy`, and custom JAX FE (meshes, Q2 shape functions, assembly, Newton with line search,
Hessian forms) would cost several sessions before the first reference case.

## Licence (resolved 2026-10-30: the whole repository is GPL-3.0-or-later)

FElupe and tensortrax are **GPL-3.0-or-later**; the repository was MIT for a few hours on 2026-10-30, then Peter
switched it to GPL-3.0-or-later (DECISIONS 2026-10-30), so FElupe can be used without a licence split. The options
considered: An Arena 2 that imports FElupe
is commonly read as a work that must be distributed under the GPL as a whole. This needs Peter's decision, not
legal advice from here:

1. **FElupe, Arena 2 under GPL-3.0 (superseded: the whole repository is GPL now):** keep `core/`, `engine/` and Arena 1 MIT; license the Arena 2 package (and the
   spike scripts) GPL-3.0, stated in its own LICENSE file. Least work.
2. **Custom JAX FE, all MIT:** no GPL dependency; several extra sessions; the judge owns more code to audit.
3. **Ask FElupe's author** for an exception or dual licence; possible, not in our control.
