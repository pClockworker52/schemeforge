# The single-impact problem as equations (working note)

Status: **working note for reasoning, not a spec.** Written 2026-11-22 from the chat of 2026-11-21 (Peter: keep it
only if every equation is checked). Each equation carries a status:
- **verified**: checked against the named source;
- **source, WSL A**: the form is read from the solver as used here, but the exact expression still has to be
  confirmed against the fork source (WSL A task 2026-11-22-a);
- **textbook**: standard result written from the modeller's knowledge, reference named, not re-derived.

Checks run in the cloud: `scripts/formalism_check.py` (sympy and scipy; output quoted in §3).

## 1. Governing equations

Two bodies, particle Ω_p and substrate Ω_s, Lagrangian (reference coordinates X), SI units.

| # | Equation | Status |
|---|---|---|
| 1 | x = φ(X, t), F = ∂x/∂X, J = det F, L = Ḟ F⁻¹, d = sym L | textbook (continuum mechanics) |
| 2 | Mass: ρ J = ρ₀ | textbook |
| 3 | Momentum: ρ₀ ẍ = ∇_X · P, P = J σ F⁻ᵀ (TLSPH discretises this form; collocated SPH the spatial form ρ ẍ = ∇·σ) | textbook; TLSPH form: source, WSL A (SPEC-TL) |
| 4 | σ = −p I + s | textbook |
| 5 | Mie–Grüneisen pressure, Hugoniot reference: p = p_H(μ) + Γ ρ (e − e_H(μ)), μ = ρ/ρ₀ − 1, Γ ≈ γ₀ (P-HG-Al: C₀ 5305.5 m/s, S 1.339, γ₀ 2.17) | **source, WSL A**: the exact `/EOS/GRUNEISEN` expression (polynomial in μ, γ₀ + aμ, energy per volume or mass) is not in the record |
| 6 | J2 plasticity: f = σ_vm − σ_y ≤ 0, ε̇_p ≥ 0, ε̇_p f = 0; ṡ = 2G(d′ − (3/2) ε̇_p s/σ_vm) in an objective rate (radial return) | textbook; the objective rate used: source, WSL A |
| 7 | Johnson–Cook (LAW4): σ_y = σ₀(ε_p, ε̇_p)(1 − T*ᵐ), σ₀ = (A + B ε_pⁿ)(1 + C ln(ε̇_p/ε̇₀)), T* = (T − T_r)/(T_m − T_r); σ_y = 0 for T ≥ T_m. P-HG-Al: A 148.4 MPa, B 345.5 MPa, n 0.183, C 0.001, m 0.895, ε̇₀ 1 s⁻¹, T_r 293 K, T_m 933 K | parameters **verified** (§8.3, data/properties.csv); thermal factor and zero strength at T ≥ T_m **verified** from the source references in §33/§34 (`m4law.F:127–135, 152, 220`); the rate term's exact form (ε̇ of the step, cap): source, WSL A |
| 8 | Temperature without `/HEAT/MAT`: ρ c_p Ṫ = σ_y ε̇_p (β = 1) + compression heating (Grüneisen, while μ > 0) [+ bulk-viscosity work on quads only] | **verified**: §2.1 (plastic part to 0.4 %), §32–§34 (quads include q; TLSPH does not) |
| 9 | Initial conditions: particle velocity −V e_z, T = T_r everywhere, substrate at rest; quarter symmetry | verified (§25, §26 decks) |
| 10 | Contact on Γ_c(t): g ≥ 0, t_n ≤ 0, g t_n = 0 (as a penalty: F = k⟨−g⟩n + damping, k = stfac B s) | penalty form **verified** (sph-hvi-contact-plan.md A2; solver-facts §3) |
| 11 | Bond off: t_t = 0 (frictionless) | verified (solver-facts §3) |
| 12 | Bond on (cs12): active where Y = 1 − A₀/A > Y′ and p_n > p_E (pair minimum, p_n of the previous cycle); f_B = (Y − Y′)/(1 − Y′) running maximum; σ_B = f_B σ_y(T) frozen at damage onset; bilinear t(δ) normal and tangential, area s², G_c = ½ σ_B δ_c | activation and σ_B **verified** (§26, solver-facts §4); G_c = ½ σ_B δ_c is the bilinear identity (textbook) |
| 13 | Outputs: e = v_z,cm(t_end)/V; v_cr = inf{V : the particle stays bonded} | verified (CS-22 definition; vcr_lipit.csv) |
| 14 | Discretisation: M ẍ = f_int(x; s) + f_c + f_b, consistent as s → 0 (TLSPH with corrected gradients) | source, WSL A (SPEC-TL) |

## 2. What the equations show

**(a) No length below R.** Parameters and units (from `formalism_check.py`): R, s [m]; V, C₀ [m/s]; ρ₀ [kg/m³];
G, K, A, B [Pa]; S, γ₀, n, m, C [–]; ε̇₀ [1/s]; T_r, T_m [K]; c_p [J/(kg K)]; and κ [m²/s] only with conduction.
The only lengths are R and s (V/ε̇₀ = 600 m is no small-scale length); with conduction also √(κ t). So a local edge
field has the form q(r/R, tV/R; s/R, Π_material). A band that localises can only take its width from s.
**Verified** by the parameter list.

**(b) Thermal softening makes the band, and early.** Along an adiabat (eq. 8, plastic part only),
h_eff = ∂σ_y/∂ε_p + (∂σ_y/∂T)(σ_y/ρc_p), with ∂σ_y/∂T = −σ₀ m T*^(m−1)/(T_m − T_r). (Corrected from the chat:
the thermal term carries σ₀, not σ_y, in its first factor.) Evaluated for P-HG-Al at ε̇ = 10⁸ s⁻¹ (`formalism_check.py`):

| ε_p | 0.1 | 0.2 | 0.3 | 0.5 | 1.0 | 2.0 |
|---|---|---|---|---|---|---|
| T [K] | 307 | 323 | 339 | 371 | 449 | 582 |
| σ_y [MPa] | 370 | 387 | 393 | 391 | 361 | 281 |
| h_eff [MPa] | 287 | 97 | 26 | −34 | −75 | −78 |

**h_eff ≤ 0 from ε_p ≈ 0.37** (at 10⁶ s⁻¹ as well), after a temperature rise of only about 50 K. Because m < 1 the
thermal slope is steep even near T_r. Beyond that the adiabatic stress–strain curve falls and the rate problem loses
ellipticity (the "elliptic problem" of Ge 2026). The compression heating of eq. 8 adds heat, so in the solver the
onset can only come earlier. The §32 rows reach ε_p ≈ 0.3 at 0.75 a by t/t_p ≈ 0.011, so the §25 window is past the
onset for most of its length. JC's rate term (C = 0.001) gives far too little viscous regularisation to set a width.
With a length ℓ in eq. 7 (ε̄ − ℓ²∇²ε̄ = ε_p), the band width becomes about ℓ and fields read
q(…; ℓ/R, s/ℓ): convergent as s/ℓ → 0 but dependent on ℓ/R.

**(c) The bond boundary is a crack tip.** Where bonded meets unbonded, the boundary of the bonded patch is the tip
of an interface crack. For a power-law hardening material (σ ∝ ε_pⁿ, N = 1/n) the near-tip fields are HRR-type:
σ ∼ r^(−1/(N+1)), ε ∼ r^(−N/(N+1)) (textbook: Hutchinson 1968; Rice & Rosengren 1968; not re-derived; interface and
dynamic corrections ignored). For n = 0.183: **σ ∼ r^(−0.155), ε ∼ r^(−0.845)**. (Corrected from the chat, where the
strain exponent was given as −n/(n+1).) So point and edge values near the bond boundary grow under refinement even
with a length scale, unless that scale also regularises the tip. A pointwise threshold such as Y > Y′, p_n > p_E
evaluated there is mesh-dependent by construction; an energy quantity (G_c) is the kind that stays finite at a
crack tip. This fits §25–§27 and Tang's measured gradient of about 50 MPa/µm (data/tang2024_reading.md).

**(d) Integrals can converge while points do not.** The energy dissipated in a band per unit area is about
σ_y × slip, independent of its width, so whole-body quantities (e, energy, a(t)) can converge while local ones do
not: a(t) converges, Y − 1 does not (§25, §27). e(off) still drifts 14 % from R/16 to R/32 (§30), so the TLSPH
meshes are not in that regime yet, or the slip itself is unresolved. (Reasoning, not a theorem.)

**(e) Identifiability.** Unknown bond parameters: Y′, p_E and δ_c (or G_c), plus ℓ if added: at least 3–4. Data: one
v_cr per material and condition. With fewer independent observations than parameters a fitted law predicts nothing.
Tang's strength-versus-radius profile adds a function of r per impact. (Counting argument.)

**(f) The bond is weakest where it forms.** Eq. 12 sets σ_B ∝ σ_y(T), and eq. 7 sets σ_y → 0 as T → T_m. The 2D edge
exceeds T_m in the §25 window (§33). So the law makes bonds weakest at the hot jetting edge, where the clean, hot
metal is thought to bond. That is a modelling choice in cs12, not physics, and worth questioning before any further
bond-law work.

## 3. Check output (`uv run python scripts/formalism_check.py`, 2026-11-22)

- h_eff symbolic form as in (b); adiabat table as above; onset ε_p 0.367 (10⁶ s⁻¹), 0.365 (10⁸ s⁻¹).
- Parameter list as in (a).
- HRR: N = 5.464, σ ∼ r^−0.155, ε ∼ r^−0.845.

## 4. Open (WSL A task 2026-11-22-a, reading only)

Confirm against the fork source with file and line references: eq. 3 and 14 (TLSPH force sum, F, correction),
eq. 5 (exact Grüneisen expression), eq. 6 (objective rate), eq. 7 (rate term as implemented), eq. 10–12 (as coded).
