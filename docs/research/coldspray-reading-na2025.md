# Reading note: Na et al. 2025 (B10), the combined strength + oxide model (Eq. 6)

**Source key Na2025, evidence level F.** H. Na et al., "Single particle impact explorations on the role of powder heat
treatments in cold spray: Effects of strength and oxide structure", J. Mater. Res. Technol. 36 (2025) 7026–7034,
doi:10.1016/j.jmrt.2025.04.261. PDF supplied by Peter on 2026-11-05 (not committed). B10 is unblinded and scored
(coldspray-results-b10.md), so the full text may be read. This replaces WSL B task 2026-11-05-b1.

## The model as printed (Sec. 5)

| Eq. | Content |
|---|---|
| (4) | V_cr ≈ (2/k) · (C₀/B) · Y_d. "All other things being equal, the critical velocity scales linearly with the dynamic yield strength" (their ref. 32). k is a constant; C₀ and B are the sound speed and the bulk modulus. "Explicitly tested against changes in strength across a suite of aluminum alloys" (their ref. 39). |
| (5) | Lienhard rule of mixtures for the jet: σ_eff = σ₀ · t₀/t + σ_m · (t − t₀)/t. The jet is a thin strip in pure tension; the oxide (strength σ₀, thickness t₀) and the metal (σ_m ≈ Y_d) load in parallel. |
| (6) | V_cr ≈ (2/k) · (C₀/B) · [σ₀ · t₀/t + σ_m · (t − t₀)/t]. |

**Parameters:**
- **k = 0.062,** fitted on one powder (as received), with C₀ = 5300 m/s and B = 67.55 GPa for Al 6061;
- **t = 100 nm,** the jet thickness "measured" in Lienhard 2020 (their ref. 14); ±10 % in t changes V_cr by ±0.6–2 %;
- **σ₀ = 870 MPa,** the oxide strength estimated in Lienhard 2020 and Sun 2020 (refs. 14, 17) from the high-rate
  strength of aluminium oxide, assumed to hold for Al 6061's oxide; ±10 % changes V_cr by ±0.6–2 %;
- **σ_m = Y_d,** the dynamic yield strength **extracted from the coefficient-of-restitution data** of the same
  impacts (Table 1: 246.3, 197.4, 197.8, 163.1, 188.9 MPa). These values were withheld from the blind inputs as
  mixed with the outcome.

Authors' result: of Y_d alone (Eq. 4), oxide alone (Eq. 5) and both (Eq. 6), Eq. 6 aligns best with the five measured
values (their Fig. 8).

## Comparison with CS-10 (structural, no judgement of which is better)

| | Na2025 Eq. 6 | CS-10 |
|---|---|---|
| Mechanism of the oxide term | The oxide stiffens the **jet** (rule of mixtures in a thin tensile strip of thickness t) | Work to fracture and expel the oxide **shell** of the particle |
| Oxide variable | t₀ / t, with t ≈ 100 nm the jet thickness | t_ox / d, with d the particle diameter |
| Combination | Linear in V_cr, strengths added inside one bracket | Quadratic, energies added in V_cr² |
| Strength input | Y_d from restitution data (impact-fitted) | Static compression strength (rule BP1) |
| Size dependence through the oxide | None (t is a jet property), unless t scales with d | Yes, v_cr falls with d at fixed t_ox |
| Fitted constants | 1 (k), plus σ₀ and t taken from the literature | 2 (β, γ) |

So CS-10 is a **relative** of Na2025 and Lienhard2020 (both superpose strength and oxide), **not a variant of the same
form**: the oxide enters through a different length (particle diameter against jet thickness) and with a different
mechanism. The label in the hunch index is changed accordingly.

## What Eq. 6 predicts for CS-12's thickness test T3 (my evaluation of the printed equation; not a judge run)

At fixed σ_m:

dV_cr/dt₀ = (2/k) · (C₀/B) · (σ₀ − σ_m)/t.

With the printed constants and the as-received σ_m = 246.3 MPa:
- (2 / 0.062) · (5300 / 67.55·10⁹) = 2.53·10⁻⁶ (m/s)/Pa;
- (870 − 246.3) MPa / 100 nm = 6.24·10⁶ Pa/nm;
- **≈ 15.8 m/s per nm, so about +126 m/s from 17 to 25 nm.**

| Hunch or model | Al 6061, 15 µm, oxide 17 → 25 nm, same oxide type, same strength |
|---|---|
| Na2025 Eq. 6 (Lienhard jet model) | about +126 m/s |
| CS-10 (frozen β, γ) | about +37 m/s |
| CS-12 minimal | no change beyond the window width |

**A same-type thickness series decides between three models,** not two. The disagreement is larger than the
typical window width of about 45–50 m/s, so one series separates them.

## Caveats

- Eq. 6 uses Y_d fitted to rebound data of the same impacts. Like P2 in the v1 rules, it is partly circular and cannot
  be used for a blind prediction unless Y_d comes from impacts below v_cr only, or from another source.
- k is fitted on one of the five points; the other four are in-sample in the sense that the authors chose the form
  after seeing them.
- t = 100 nm and σ₀ = 870 MPa come from Lienhard 2020 (B14). Their use here is printed in Na2025, so they are not a
  new route of exposure, but they are logged (B4 exposure log).
