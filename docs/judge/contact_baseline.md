# Arena 2 zoo front (Phase 6 step 5, 2026-11-03, cloud session, judge contact-v0.7.dev)

PLAN §14.7 asks whether the zoo shows the trade-off in the medium's stiffness scale γ: a softer medium leaks less
force before contact and leaves less residual gap, but Newton becomes less robust. If it does not, Phase 7 has no
target and Arena 2 stops here (plan Gate 6 item 4).

**Result: the trade-off exists, for both zoo media.** As γ falls from 1e-3 to 1e-6, the gap-closure leak and residual
gap fall by three orders of magnitude and the Hertz contact-width error from several hundred per cent (γ = 1e-3) to about −4 %; at the same time
the largest stable load step falls from the whole push to 1/4–1/6, the Newton iterations rise, and at γ = 1e-7 Hertz
no longer converges. Classical frictionless contact (no medium) sits in the ideal corner: accurate (the judge's error
floor) and robust in one step. No zoo medium reaches it; a better medium moves the front towards it.

![front](figures/contact_front.png)

Measured with `scripts/contact_front.py` (judge functions, dev-mesh cases, not registered runs; data in
docs/judge/baseline/contact_front.json; registered zoo runs are in STATUS). C0a: gap closure (confined), γ as
listed. C2: Hertz on the dev mesh with the judge's fixed regularization kr = 5e-7. max_step: 1 / fewest of 1, 2, 3,
4, 6, 8, 12 equal load steps in which C2 converges.

| Medium | γ | C0a leak_pre | C0a gap_res | C2 a_err | C2 p0_err | C2 leak_out | C2 Newton iterations | max_step |
|---|---|---|---|---|---|---|---|---|
| neo_hooke | 1e-03 | 1.87e-02 | 3.16e-02 | +3.702 | -0.2194 | 0.206 | 47 | 1.000 |
| neo_hooke | 1e-04 | 1.94e-03 | 4.85e-03 | +1.038 | -0.0374 | 0.056 | 56 | 1.000 |
| neo_hooke | 1e-05 | 1.95e-04 | 6.53e-04 | +0.123 | +0.0012 | 0.016 | 62 | 0.500 |
| neo_hooke | 1e-06 | 1.95e-05 | 8.23e-05 | -0.039 | +0.0085 | 0.011 | 87 | 0.167 |
| neo_hooke | 1e-07 | 1.95e-06 | 9.95e-06 | fails | — | — | — | 0.000 |
| neo_hooke_iv | 1e-03 | 1.42e-02 | 3.32e-02 | +3.751 | -0.1793 | 0.179 | 50 | 1.000 |
| neo_hooke_iv | 1e-04 | 1.45e-03 | 8.54e-03 | +1.000 | -0.0329 | 0.044 | 56 | 1.000 |
| neo_hooke_iv | 1e-05 | 1.45e-04 | 2.16e-03 | +0.118 | -0.0006 | 0.015 | 69 | 0.500 |
| neo_hooke_iv | 1e-06 | 1.45e-05 | 5.44e-04 | -0.036 | +0.0065 | 0.011 | 76 | 0.250 |
| neo_hooke_iv | 1e-07 | 1.45e-06 | 1.37e-04 | fails | — | — | — | 0.000 |
| classical | — | 0.00e+00 | 0.00e+00 | +0.009 | -0.0047 | 0.000 | 37 | 1.000 |

## The zoo, and what is missing

| Member | Source | State |
|---|---|---|
| `neo_hooke` | compressible neo-Hooke scaled by γ, the isotropic medium of Bluhm, Sigmund and Poulios (2021) | in the zoo |
| `neo_hooke_iv` | felupe's isochoric–volumetric neo-Hooke form (volumetric term finite as J → 0); a FElupe variant, not claimed as a published third-medium formulation | in the zoo |
| classical penalty contact | felupe ContactRigidPlane; not a medium, the reference corner | in the front |
| Wriggers, Schröder and Schwarz (2013) anisotropic medium | needs a contact-direction field the ψ(C) slot does not have (a planned later slot) | pending: formula to be taken from the paper, not from memory |
| mixed formulation (felupe ThirdMediumContactMixed) | a different formulation with an extra field, not a ψ(C) candidate | pending: reference point outside the slot, source to be checked |
| friction model ("Adding friction to Third Medium Contact") | Target E, deferred (D4) | not in Phase 6 |

The two media trace almost the same accuracy–robustness curve in Hertz; neo_hooke_iv is slightly more robust at
γ = 1e-6 (max_step 1/4 vs 1/6, 76 vs 87 iterations) at the cost of a 4–7 times larger residual gap in C0a. They are two
points of one family, so the front is narrow: the pending members would widen it. Target D (step 6) is pre-registered
from this front; it should rest on a_err and p0_err (mesh-stable, contact_spec.md §mesh_sens) and on max_step.
