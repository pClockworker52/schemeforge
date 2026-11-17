# Driver-convergence check, 2026-11-17 (calibration; spec and prediction fixed before any number is computed)

**Why.** Peter, 2026-11-17 (DECISIONS "Driver check before the trigger run"): before the trigger run, check whether
any outer or non-local quantity converges under refinement in plastic, jetting impact, so that it could drive `cs12`
bond activation live in the solver instead of skin Y. Skin Y peaks at the pole (§26) and Y − 1 converges at no disc
on 2D quads (§25). The trigger (D4) is deferred, not cancelled.

## 1. Candidate drivers

ℓ ∈ {1.5, 2.0} µm, both reported. ℓ is a model choice; a physical justification is open.

| # | Driver | Definition |
|---|---|---|
| 1 | contact radius a(t); edge speed v_edge | a from the run output; v_edge = da/dt by central differences over output times; edge Mach v_edge / C₀ with C₀ = 5305.5 m/s (P-HG-Al, §8.3). The Mach divisor is a constant and does not change convergence |
| 2 | annulus plastic work W_ann(ℓ, t) | plastic work in the material within ℓ of the interface (depth) and within the band a − ℓ ≤ r ≤ a, each body separately |
| 3 | pressure–slip history P_s(r, t) | ∫₀ᵗ p_n |v_slip| dt, averaged over rings of width ℓ centred at 0.25 a, 0.5 a, 0.75 a of the current R/256 contact radius (same centres on all meshes, as §25), each side |
| 4 | ring Y(ℓ) | Y − 1 averaged over the same rings, each side |

## 2. Data

- **Judged:** the §25 quad runs (Al–Al, 600 and 500 m/s; R/64, R/128, R/256; fork binary `d0500106d`), outputs from
  the **third** onwards up to t* (the first two are start-up, §25).
- **Reported only:** the BCT-off TLSPH survival probe (§23.1, Al–Al 800 m/s, R/16 and R/32), if its outputs allow;
  two coarse points cannot show convergence.

## 3. Rule

A driver converges at an output (and ring, side) if

|q256 − q128| ≤ 3.5 % |q256| and ( |q256 − q128| ≤ 0.8 |q128 − q64| or |q128 − q64| ≤ 3.5 % |q128| ),

the §25 rule. A driver is **usable** if it converges at ≥ 80 % of its judged points, on each side where it has sides,
and at both speeds.

**Outcome rule.**
- No usable driver → the outer-driven activation route has no stable input; the modeller recommends stopping Track B
  (Peter decides).
- At least one usable driver → it may be drafted as a hunch (budget 3 of 5), with a kill criterion against Track A
  blind v_cr data; Peter decides how D4 relates to it.

## 4. Who computes what

- Driver 1: cloud, from `results/tl_cal6_p3_series.csv` (columns `a_R64_um`, `a_R128_um`, `a_R256_um`, `t_ns`),
  script `scripts/driver_check_a.py`.
- Drivers 2–4: WSL A task 2026-11-17-b, from the §25 field outputs (rerun the §25 decks with the same binary if the
  files are gone), results §27, rows `tl_cal8_driver_*.csv`.

## 5. Prediction (modeller, judgment, before computing)

Probability that each driver is usable: a(t) 0.6; v_edge 0.3 (differences of nine outputs are noisy); W_ann 0.4;
P_s 0.3; ring Y 0.15. Probability that at least one driver other than a(t) is usable: 0.45. a(t) alone would not be
enough to drive a local bond law; it constrains where bonding can happen, not whether.

## 6. Results

### 6.1 Driver 1 (cloud, 2026-11-17; `python scripts/driver_check_a.py`, inputs `tl_cal6_p3_series.csv` only)

| Driver | 600 m/s (outputs 3–9) | 500 m/s (outputs 3–8) | Usable |
|---|---|---|---|
| a(t) | 7 of 7 converge | 6 of 6 converge | **yes** |
| v_edge = da/dt | 0 of 7 | 0 of 6 | **no** |

- a(t) at R/256 grows from 1.77 to 3.34 µm (600 m/s) and from 1.77 to 3.17 µm (500 m/s); mesh-to-mesh differences
  are 0.2–3.5 % of the R/256 value.
- v_edge from differences of nine outputs is noisy on every mesh; R/256 gives 2.5–3.5 km/s, edge Mach
  v_edge/C₀ = 0.48–0.66, so the edge is subsonic throughout the judged window (consistent with
  coldspray-kinematics.md).
- **Against the prediction:** a(t) usable (predicted 0.6) right; v_edge not usable (predicted 0.3) right.
- **Reading (judgment):** a(t) is close to a kinematic quantity of the bulk (penetration depth and geometry), so its
  convergence was expected and says little about the interface; it constrains where bonding can happen, not whether.
  It does not settle the outcome rule; drivers 2–4 (WSL A, §27) do.

### 6.2 Drivers 2–4 (WSL A, §27; merged 29c09ee)

Fraction of judged points that converge, pooled over the three rings; the smallest over side × speed decides
(usable needs ≥ 0.80):

| Driver | ℓ = 1.5 µm | ℓ = 2 µm | Usable |
|---|---|---|---|
| W_ann (annulus plastic work) | particle 0.00; block 0.29 (600) / 0.00 (500) | particle 0.00; block 0.43 / 0.00 | no |
| P_s (pressure–slip history) | 0.11–0.22 | 0.17–0.24 | no |
| ring Y | particle 0.00; block 0.00–0.19 | particle 0.00; block 0.00–0.10 | no |

- Even the whole-body plastic work differs by 2–12 % between R/128 and R/256 in the window: the plastic deformation
  near the contact is not resolved, not only the band edge. Coarse output sampling adds about 8–10 % to the
  plastic-work integral on all meshes alike (shifts the mesh differences by about 1–2 %; no verdict changes).
- Survival probe (TLSPH, R/16 and R/32, reported only): contact radius median difference 2.8 %; W_ann 4.5–30 %; ring Y
  9–50 %; P_s not computable.

**Outcome under the rule (§3):** no usable driver among 2–4; only a(t) converges, which by §5 cannot drive a local
bond law. So the outer-driven activation route has no stable input; the modeller recommended stopping Track B, and
Peter decided so (DECISIONS 2026-11-17 "Track B interface-state route closed; reduced route adopted").

**Against the prediction (§5):** W_ann 0.4, P_s 0.3, ring Y 0.15, "at least one other than a(t) usable" 0.45: none
usable, so the modeller's prediction leaned too optimistic again.

**Scope limit:** judged only to about 0.035 t_p (the finest quad mesh collapses there, §25), and on the only reference
host available (OpenCourant 2D quads, Lagrangian, no remeshing). A remeshing or ALE reference might converge later in
the impact; this is not ruled out. The result is "not verifiable with the references available to this project", not
"impossible in principle".
