# Multi-particle cold spray: problem specification (method-neutral, for idea generation)

Written 2026-11-18 for a brainstorm on new approaches. It states **what** must be achieved and **what is known to
constrain it**, deliberately without the methods already tried. Those are listed separately in
[multi-particle-tried.md](multi-particle-tried.md); read that only **after** generating ideas, to filter them. Numbers
are from the project record; no new claims.

## 1. Goal and ideal final result

**Goal.** For a stream of metal particles striking a surface, predict which particles stick, where on their contact
they join, and how the growing deposit evolves. Predict it from material properties, without fitting to the outcome
predicted, inside the explicit impact code OpenCourant (preferably its Total Lagrangian SPH bodies; open to change).

**Ideal final result (TRIZ sense).** Joining emerges by itself from the same computation that moves the material, and
can be checked, with no separate rule that decides it and no quantity that must be resolved below what the
computation can resolve.

## 2. The system, in numbers

| Element | Scale |
|---|---|
| Particle | 10–20 µm diameter; 500–1600 m/s; metals (Al, Cu, Ti, Ni …) |
| Impact | contact time ≈ D/V, about 10–40 ns; heavy plastic flow; a jet of material leaves the contact edge |
| Contact edge | moves outward at about 0.5–0.66 of the sound speed (subsonic) |
| Surface film (oxide) | 2–20 nm thick, brittle, sometimes coated or hydrated |
| Joined region | an annulus: the centre stays oxide-covered and unjoined; the middle joins; the edge piles up oxide |
| Deposit | many impacts on earlier particles; mm scale; each impact changes the surface the next one meets |
| Affordable resolution (3D, 15 GB machine) | particle spacing about R/32–R/64 (0.15–0.3 µm); a full target at R/64 needs about 40 GB |

Six orders of magnitude separate the film (nm) from the deposit (mm).

## 3. Functions the computation must perform

1. **Move the bulk:** large deformation, flow and jetting of both bodies.
2. **Keep the bodies apart** until they join.
3. **Decide joining locally**, during the impact.
4. **Carry the joined region** through rebound, which is tension.
5. **Hand the result on:** the deposit's changed surface (shape, hardness, roughness, film state, residual stress)
   becomes the target of the next impact.
6. **Be checkable** against something independent.

## 4. What is known (constraints, method-neutral)

- **Bulk integral quantities are reproducible and converge under refinement:** contact time, peak force, rebound,
  energy balance (closes to 0.25 %), contact radius.
- **Local surface quantities at the joining edge do not converge under refinement in any discretisation tried,
  including the reference ones:** surface stretch, edge pressure, and averages of them over sub-micron to 2 µm
  patches. Only the first ~3.5 % of the impact could be followed on the finest reference mesh before it failed.
  **Working assumption:** there is no verifiable local interface state at reachable resolution. That is a property
  of the problem, not only a defect to repair.
- **A discretised body misrepresents loads applied to its outermost layer** (a known property of the integration);
  fixes exist but each cost something (locality, momentum, robustness on changing contact patches).
- **Experimental facts:**
  - the threshold velocity v_cr is reported as the velocity where joining and rebound are **equally probable**, so
    joining is statistical at the level of measurement (windows ±2 %);
  - more or different surface film raises v_cr (+4 % to +17 %);
  - a cold-worked target lowers it (−12 %), although it is harder;
  - particle strength alone does not order v_cr;
  - a sprayed deposit surface raises v_cr compared with a polished plate (+15 %);
  - the joined area is a ring; bonded fractions in stacks are low (≤ 18 %).
- **Sound speed alone** predicts v_cr within about 1–8 % for pure metals, and misses alloys and soft heavy metals.

## 5. Contradictions

| # | Improving … | … worsens / conflicts with … |
|---|---|---|
| C1 (physical) | joining needs a **local** surface state | the local surface state is **not defined** (does not converge) at the scale where it acts |
| C2 | finer resolution improves the bulk | it sharpens rather than settles the edge quantities, and memory grows faster than the machine |
| C3 | the bond must act **during** the impact (it changes rebound) | what triggers it is only knowable as an **aggregate**, after the fact |
| C4 | multi-particle needs **many** cheap impacts | each impact seems to need its edge resolved, which is expensive |
| C5 | the film (nm) controls joining | the particle (µm) and the deposit (mm) control everything else |
| C6 | correctness needs an independent reference | the deciding quantity has none |

## 6. Resources

- A bulk solver that is verified on integral quantities (rebound, force, energy).
- An in-solver bond with a cohesive law, a surface skin, and convergent contact radius and kinematics.
- Experimental judges:
  - v_cr windows;
  - ring maps;
  - rebound coefficients;
  - stack erosion and deposit-level data (deposition efficiency, porosity);
  - a pre-registration and blind-scoring protocol.
- Symmetry within an impact; statistics over many impacts; the short contact time.

## 7. What "success" could mean without an interface reference (to be chosen per idea)

- Agreement with experimental v_cr, ring maps and deposit data under blind rules (validation, not verification).
- Convergence of whatever the idea needs as its input (integral or statistical), shown before use.
- Internal consistency, for example energy, momentum, or independence from a chosen regularisation length.
