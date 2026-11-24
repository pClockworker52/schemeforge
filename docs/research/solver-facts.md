# Solver facts register (cold-spray track)

**Read before drafting or freezing any spec, hunch, ladder or task.** One line per fact about the tools: what they
output, what they cannot do, their parser bounds, what converges and what does not, costs, and placeholders. Every
line cites its source; nothing here is new or re-derived. "§n" = docs/research/opencourant-verification.md.

Created 2026-11-21 (DECISIONS 2026-11-21, "Solver facts register"). It supersedes the summary table at the top of
the verification log, which stops at §13. **Kept current by the modeller at every merge** (coldspray-procedure.md).

## 1. OpenCourant, 2D axisymmetric quads (`/QUAD`, N2D3D = 1)

| Fact | Consequence for specs | Where |
|---|---|---|
| Use `Isolid = 17` (4-point quad); the default area-weighted 2D solid fails Hertz (about 5× too stiff) and loses momentum in free flight. ALE falls back to the default element | always Isolid 17, Lagrangian only | §5 |
| **The element temperature is computed but not written out with Isolid 17** in upstream OpenCourant and the CS-22b binary (`27e53d5f0`): outputs read `GBUF%TEMP` (stays at T₀ / 293 K); LAW4 heats and softens through `LBUF%TEMP`. **Fork branch `quadtemp` (`078380a0f`) writes the Gauss-point mean of `LBUF%TEMP` to the animation output** (output only; T-A0 55/55); H3D and `/TH/QUAD` still write T₀ in every build | quad temperature only from animation output of a `quadtemp` build | §5.3, §32, §33 |
| In the §25 window the contact-edge temperature exceeds T_m (1.03–1.08 T_m at the last judged frame); LAW4 sets deviatoric stress and yield to zero at a Gauss point with T ≥ T_m; no latent heat | the edge material is outside JC's range late in the window | §33 |
| Disc softening factor S = 1 − T*ᵐ (engine T) is 0.91–0.94 at 0.25 a and 0.5 a already at the first judged frame, 0.21–0.36 at 0.75 a at the last; the engine heats more than plastic work at every point (compression and q heating, not separated) | softening is active throughout the window; part of the heat is numerical (q) or reversible (EOS) | §33 |
| LAW4's temperature = plastic work (∫σ_y dε_p/ρc_p, to 0.4 %) **plus** bulk-viscosity work **plus** reversible Grüneisen compression heating (6–19× the plastic part in coarse plate shocks); no Taylor–Quinney fraction | any "temperature" from LAW4 is not plastic heating alone | §2.1 |
| `/HEAT/MAT` gives T ≈ 0 on quads; **no heat conduction on 2D quads** at all | conduction studies need 3D bricks or SPH | §2, §11 |
| Rigid-wall force `FNZ` is ∫σ dr, not a force, in axisymmetric runs | convert, or use momentum rates | §1, summary |
| Time-history internal energy (and the ERR % energy column) reads zero in axisymmetric runs | no energy balance from TH on quads | summary |
| Default bulk viscosity costs 5–7 % rebound in the elastic case; with default q and dt scale, 50:1 quads go unstable at cycle 0 | state q explicitly; dt scale 0.4 | summary |
| Plateau +0.69 % at every mesh = finite strain (0.42 V/c_d); no small-strain option for quads | use finite-strain references (§18.1) | §3, §18.1 |
| Rung 0, 0p and Hertz (rung 1) agree with exact/JAX to about 1 % | the quads are a valid elastic reference | §3–§6 |
| **Al–Al plastic impact: the mesh fails at the jet root**, earlier with refinement (5–37 % of penetration time; §25: R/256 stops at about 0.8 ns ≈ 0.034 t_p on a collapsing block cell near the contact edge) | anything judged on the §25 deck lives in a ≤ 0.035 t_p window, before the jet is evaluated | §8, §25 |
| In that window: p_n (0.5 µm discs) converges at 0.25 a and 0.5 a, not 0.75 a; **Y − 1 converges at no disc** and rises with refinement; contact radius a(t) converges; v_edge, W_ann, P_s, ring Y do not | local edge drivers are not usable inputs on this host | §25, §27, driver-check-2026-11-17.md |
| Y − 1 already fails at the first output (t/t_p ≈ 0.004). ~~Reconstructed softening factor there 0.98–0.99, so the early failure is not thermal~~ (wrong: the reconstruction left out compression and q heating; engine S is 0.91–0.94 there, §33) | the early failure is not shown to be non-thermal | §25, §32, §33 |
| Paired (hardened-twin) differences do not cancel the edge error | pairing is no fix on this deck | §28 (CS-21) |
| Switch radius a_c from a fitted a(t) converges (2.35 % / 2.88 %), thin margins, p drifts 6.5 % | usable only with those caveats | switch-check-2026-11-18.md |
| §25 decks: about 3 min per R/256 run, 0.7 GB; the six runs of a speed pair in about 8 min | cheap; reruns reproduce exactly (§32) | §25, §32 |
| Quad T-B2 reference: U_ref above 1.75 % for 12 of 16 judged averages at R/256 | not a ≤ 1.75 % reference for skin averages | §23.1 |

## 2. OpenCourant 3D bricks and native SPH

| Fact | Consequence for specs | Where |
|---|---|---|
| Native SPH is 3D only; two SPH parts are kernel-welded (tension and shear across the interface) | no native SPH contact between parts | §9, §9.8 |
| `/HEAT/MAT` works on 3D bricks but ignores EFRAC for LAW4 (β via ρc_p/β) | | summary |
| Brick conduction matches erfc to 0.017 %; SPH conduction (H0-SPH) is first order, 2.5 % at s = 0.156 µm | | §11, §12 |
| Conductive bricks with an adiabatic SPH particle: OOM without a particle `/HEAT/MAT`, particle overheats to about 9·10⁴ K with one | that set-up cannot run | §12.2 |
| Brick contact edge collapses at 0.115–0.17 D/V (R/16), before 0.1 D/V at R/32 (setup F) | brick impact decks have short windows too | §10 |
| Heat conduction as a regulariser: t_f still falls 22–37 % from R/32 to R/48, edge ε_p rises 35–66 % (CS-13c refuted) | the thermal length (≈ 0.7 µm at 5 ns) is too small to resolve | §13 |
| Failed SPH particles leave the kernel interaction | | §10.4 |

## 3. Fork `sph-hvi-contact`: hvi contact, TLSPH, BCT, VCI, skin

| Fact | Consequence for specs | Where |
|---|---|---|
| hvi contact is frictionless penalty, F = k⟨−g⟩n + damping, repulsive only, k = stfac·B·s with **B = ρ₀C₀² from the EOS card (76.0 GPa for P-HG-Al, not the elastic bulk modulus)**; damping 0.05 of critical, cannot pull; no friction (fatal if requested), max 2 bodies, OpenMP only, no restart | the "no bond" branch is frictionless; no restart means a killed run starts from t = 0 | sph-hvi-contact-plan.md A2, DECISIONS 2026-11-21, §35 |
| Separable SPH–SPH contact on collocated SPH: B-2, B-3 and D-1 FAIL; S′ (ξ + order 1) not adopted | collocated SPH is not the host | §14, §15 |
| TLSPH plateau offset is finite strain; end layers 1–2 carry 0.655 / 0.845 of the stress under a point-loaded face (also against a deformable wall) | judge against finite-strain references; face-layer deficit exists with any point load | §17, §22 |
| **BCT** (boundary-consistent traction): exact on flat uniform loads; **fails on small or changing patches** (rim loads 2–3×), feeds energy with the kinematic wall (B 1.135 / 20.4); with BCT the engine wall force reads 1.485× the transmitted force | BCT off for curved and body-on-body contact; read wall forces from momentum rates | §19, §20, §21, §23 |
| BCT off: energy closes to 0.25 %; T-S1 R/32 rebound 0.9988; survives Al–Al 800 m/s R/16 and R/32 | the CS-18b set-up with BCT off is the working host | §20.5, §23.1 |
| **No TL internal energy in the engine output**; the hourglass-work diagnostic is unreliable | energy balance only via the fork's B diagnostic | §17, §19.5, §23 |
| Face constructions: F2 frozen (flat faces only; the sphere stays the lattice); VCIMR candidate (S 0.132; skin p_n on the axis +6.6 %; R/16 \|B − 1\| 0.026) | | §23.2, §24 |
| **Skin** (`out.skin`, output only, bitwise neutral): T-S1 R/64 p_n +3.6 / +3.1 %, **Y − 1 13 % low** (R/32: 33–37 % low) | skin Y is the weakest skin output | §23.3 |
| Interface file v5 lists every particle with hvi or rigid-wall contact force; the static surface set (SURF0) misses most conforming-sphere contact particles | sphere-side averages come from the list or the skin, not SURF0 | §24.1 |
| Interface file: a facet that was debonded can show state 0 or 1 later (pair leaving the pair list or re-pairing; not checked) | bond-state histories need a lost-bond check (CS-22b) | §26 |
| Bonded pairs and the candidate list: cross-body pairs within 2h; whether a bonded pair is kept beyond that range is not documented | report the release opening before relying on large δ_c (task 2026-11-20-a item 1) | sph-hvi-contact-plan.md A2, §26 |
| T-A0 (55 runs) is the neutrality check for every fork build; "bit-identical" is on written metrics; output headers carry dates and uninitialised padding bytes, contact sums differ at round-off between `none` and a never-active bond | compare written metrics, mask headers; see A2 | §16.2, §30 |
| Costs (Al–Al quarter, TLSPH): R/8 about 100 s; R/16 about 0.5 h, 1.6 GB; R/32 11–12 h on 24 threads (10.8 h for CS-22b 30×), 12.7–14.2 GiB (WSL VM now 23.5 GiB); R/64 estimated about 100 GB (out of reach) | | §26, §30, coldspray-hunch-cs22.md |
| e(off) (Al–Al 600 m/s, P-HG-Al) does not converge: 0.094 / 0.065 / 0.057 at R/8 / R/16 / R/32 | any rebound-based quantity inherits this drift | §30 |
| A cross-body pair leaves the candidate list at the latest at r > 2.51 s (opening g_L ≈ 1.51 s along the centre line; earlier through list truncation or symmetry ghosts); a bonded pair leaving it is broken by the sweep. The facet-level lost-bond check is a **lower bound** (a sweep-broken pair on a still-bonded facet is hidden) | δ_c above g_L risks list-broken bonds; check at pair level if it matters | §31 |
| Al–Al 600 m/s, cs12 every pair from 0.5 t_p: δ_c 30× (937.5 nm) bonds hold at R/16 and R/32 (particle stays bonded) and all tear at R/8; 3× and 10× tear on every mesh | the bonded/torn regime switches between R/8 and R/16 | §31 |
| For a bonded (stuck) particle, e = v_z,cm/V measures the target surface's residual motion (−0.005 to −0.007 V at t_end), not a rebound | a dR involving a stuck particle mixes rebound and target motion | §31 |
| **TL particles heat and soften** (engine `27e53d5f0`; read from the source): LAW4 is called unchanged; `LBUF%TEMP` is heated each cycle by plastic work and Grüneisen compression, **with no bulk-viscosity heating** (unlike quads); the next cycle's σ_y uses it (1 − T*ᵐ, zero strength at T ≥ T_m), and so does cs12's σ_flow. Earlier engines and cards (CS-18b, §26) were not checked | TLSPH impacts on this engine ran with thermal softening; no numerical q heating | §34 |
| TLSPH temperature output: for SPH, `GBUF%TEMP` is the same array as `LBUF%TEMP`, so `/ANIM/ELEM/TEMP` (and H3D) should show the heated T, **untested**; the §30 decks request none; time history writes TEMP only with a thermal analysis | before a spec relies on TLSPH temperature, one small run with `/ANIM/ELEM/TEMP` must show written T ≥ the plastic-work lower bound (modeller's decision on §34; no output change needed) | §34 |
| Plastic-work lower bound in the §30 off runs: T_lb max 0.47 / 0.56 T_m at R/8 / R/16 (rising with refinement); softening factor 0.77–0.81 at the median strained particle, 0.61 at the hottest | | §34 |
| **`/NONLOCAL/MAT` (OpenRadioss base, `cs12` `38639859c`; source reading only) is a damage regulariser**: implicit gradient ū − ℓ²∇²ū = ε_p, solved as a damped pseudo-dynamic system on extra nodal dofs; for laws with mtn < 28 (LAW2, LAW4) ū reaches **only the `/FAIL` models** (plastic strain, its rate, the element length), never σ_y or T; without `/FAIL` it is not fed. Solved only on bricks (and other 3D solids) and 3- and 4-node shells; **accepted and silently ignored on 2D quads, native SPH and TLSPH**. LE_MAX > 0 overrides LENGTH (ℓ = 3 LE_MAX/√π); no step penalty; relaxation lag ≈ 10 steps (derived) | **no zero-code length on the §25 (quads) or §30 (TLSPH) deck**; a length in σ_y and T needs new engine code (Ge-type estimate: quads 4–5 task sessions, TLSPH 3 more; kernel-average form on TLSPH ≈ 17 GB at R/32, does not fit) | §40 |

## 4. `cs12` bond model and its keys

| Fact | Consequence for specs | Where |
|---|---|---|
| Activation needs **all of** g < 0, t ≥ `bond.t_on`, Y_ij > Y′, p_n,ij > p_E and σ_flow,ij > 0 (pair minima; Y per particle, area-weighted over its skin facets; p_n from the previous gather pass, so activation lags contact by one cycle); f_B = (Y − Y′)/(1 − Y′) running maximum; σ_B = f_B σ_flow(T) refreshed while D = 0, frozen from damage onset; law: bilinear, one damage variable on δ = √(g² + \|δ_t\|²), K₀ = the contact penalty k, d₀ = σ_B s²/k, G_c = ½ σ_B δ_c per area s² | | §26, §35 |
| **A bonded pair carries no cohesive traction while g ≤ 0**: in compression it transmits no shear; its tangential opening δ_t keeps accumulating and counts in δ when it reopens. A bonded pair leaving the candidate list counts as broken (remaining G_c booked to W_b, approximate for unequal pairs) | bonds formed under compression may reopen with δ ≫ δ_c after microns of slip and fail at once (untested reading; problem-formalism.md §2(g)) | §35 |
| Interface-file `slip` (field 6) is **per particle**: the maximum over its current pair records of \|S_r\|, the total tangential slip of a record since its first g < 0, accumulated in every state (contact only, bonded, debonded). For a bonded record S_r = S_r(t_act) + δ_t,r. **Per-pair δ_t, g and D are written nowhere.** D is updated only while g > 0, so a compressed bond can pass δ_c and tear at its first reopening. SURF0 misses bonded particles: use SURF0 plus the per-record contact lists | `slip` is a proxy for δ_t that includes pre-activation slip; pair-level questions need a new output | §36 |
| **`bond.stick`** (engine `0153cae04`, cs12 only, default off): a bonded pair with g ≤ 0 carries (1 − D) k δ_t,el, capped at τ_B s² with τ_B = σ_B/√3; beyond the cap it slides, and the plastic slip s_pl and work W_s are booked per pair and globally (interface file v7), not in δ, κ or D; at reopening δ_t = δ_t,el. **`out.pairs`**: per-pair records (state, g, δ_t, D, σ_B, κ, s_c, s_pl, W_s, S) at every interface record. Neutral with stick off (T-A0 55/55; §30 deck identical except thread-order global sums at 1e-16 and one header integer, which also differ between two runs of the old binary). Record grows from 12 to 16 slots (17 from `38639859c`, §38) | estimate memory before R/32; W_s, E_b, W_b are not in the engine's energy balance | §37 |
| **The old law (stick off) books G_c·A at reopening without work input**: slip accumulated while compressed enters δ when the pair reopens, so damage and its dissipation happen without work (S0 shear check: E_b + W_b jumps by the full G_c A while the work changes by 3·10⁻¹⁷ J) | W_b in CS-22b's runs (and §31's G_c,eff) can include energy no force supplied | §37 |
| **Stick law, energy-consistent (engine `38639859c`, on `0153cae04`)**: the stick step is projection (dropped ½(1 − D)k(δ_t·n)² booked to W_s and a per-pair W_proj), cap shrink (if δ_cap = τ_B s²/k < \|δ_t,el\|, δ_t,el scaled to δ_cap, release ½(1 − D)k(\|δ_t,el\|² − δ_cap²) booked to W_s, s_pl unchanged), then trial/slip at the cap. Per-pair W_s and W_proj weight ghost records ½ (sum = global). Record 17 slots; per-pair file v2 (16 fields) with stick on, v1 with stick off; interface W_s includes the releases. Checks: σ_B ramped down at the cap closes to ≤ 0.30 %; release at re-compression to 2.7·10⁻⁴; stick off byte-identical (D-3/D-4, S0, CS-22b R/8 per-pair file); T-A0 55/55. On `0153cae04` the same releases were booked as slip (20 % low at re-compression, s_pl grew without motion) | the engine for CS-23. s_pl can still grow at re-compression when a pair sheared in tension has tilted its normal (genuine slip, S3: 0.030 δ_cap, = s_c): do not read s_pl > 0 as an error. Ghost weighting checked by code reading only; **no deck with bonded ghost pairs has run with stick on** (the quarter model has them): check pair sum = global on the first run. Small-W_in decks: the residual is set by the press (≈10⁻¹² J), so relative balances there can read 8–12 % | §38 |
| Memory, cs12 with stick on and `out.pairs`: §30/CS-22b R/32 deck (1 238 463 particles, 12 pair slots) ≈ **14.8 GiB** (14.2 measured on `27e53d5f0` + 0.61 for 17 slots and the list flag); formula checked at R/8 (+10 112 KiB vs +9 977 predicted); stick on adds none; per-pair file < 1 MB per output, < 100 MB per run expected at R/32 | fits the 23.5 GiB VM with 8.7 GiB spare | §38 |
| **Stick on in an impact run (CS-23, engine `38639859c`):** in `out.pairs` a pair leaves bonded only as torn (state 2, D = 1, κ ≥ δ_c, set by the law) or swept (state 2, D = 1, κ < δ_c, set by `bond_sweep`); no code path sets 1 → 0 or state 2 with D < 1; δ_t at tearing is the first state-2 record. Tears are mixed mode (median \|δ_t\|/δ_c 0.60–0.83, g/δ_c 0.56–0.80); s_pl Σ 7–100 µm per run; W_proj < 3·10⁻⁶ W_s. Energy balance with E_b, W_b, W_s 1.000–1.014 of KE₀. Per-pair W_s sum = global to 4.6·10⁻¹⁴. **No symmetry-ghost pair carried W_s**: the ½ ghost weight is still unexercised. Cost: R/8 1.5 min, R/16 29 min (8 threads), R/32 9.9 h (24 threads), peak RSS 14.82 GiB | on the CS-22b deck dR does not converge with stick on (every δ_c moves toward 0 from R/16 to R/32) | §39 |
| Slip at tearing (CS-22b on-runs, proxy): pure opening is rare (3 % of torn particles slid ≤ 0.2 δ_c); slip ≥ δ_c before tearing for 82 % at 3×, 40–53 % at 10×, 8–37 % at 30×; at 30× R/16 torn particles tear at slip 0.96–1.05 δ_c; held 30× bonds slide less (R/32 90th percentile 0.53 δ_c) | the tear/hold outcome depends substantially on compressed slip, a feature of cs12 | §36 |
| **Parser bounds:** `bond.Yp` < 1 (lower bound 0 removed by A1); `bond.pE` ≥ 0; `bond.t_on` (cs12 only, default 0) | check every key against its bounds before freezing | §29, §30 |
| Off-skin particles carry the sentinel Y = −1; they bond only when Y′ < −1 (A1) | | §29, §30 |
| **Placeholders, not physical:** Y′, p_E (survival 0.3 / 0.5 GPa) and δ_c. δ_c = 31.25 nm (0.05 s at R/16) gives a bond of a few J/m²; every bond tears on rebound and dR < 10⁻³ | check that a placeholder lets the effect act before freezing (CS-22 scope note) | §26, §30, DECISIONS 2026-11-19 |
| Skin Y peaks at the particle's pole (largest facet Y 0.72 at r < 3 µm), so skin-Y activation bonds the centre first; no thresholds give a bonded ring | | §26 |
| σ_B = f_B σ_flow(T) uses the material's current temperature (rate and adiabatic heating included). Where the interface nears T_m, σ_B of an unbroken bond falls with σ_flow; at T ≥ T_m σ_B is frozen at its last positive value and no new bond forms (LAW4 sets the strength to zero at T ≥ T_m; the 2D edge reaches 1.03–1.08 T_m in the §25 window) | bond fracture energies estimated from room-temperature σ_flow are upper bounds (e.g. CS-22b's G_c estimates); report W_b / bonded area. Confirmed for engine `27e53d5f0`: from T_lb alone σ_flow is 19–23 % below room temperature at the median strained particle, 39 % at the hottest | §26, §33, §34, §35 |
| Illustration δ_c sweep (Ti, 1584 m/s, R/12): still-bonded share 0.06–0.11 / 0.63 / 1.00 at δ_c/s = 0.3 / 1 / 3 | seen data on another material | §26 |

## 5. Material data in use

| Fact | Consequence for specs | Where |
|---|---|---|
| LAW4 rate term: CE = 1 + C ln(ε̇/ε̇₀) with **ε̇ = max \|d_ij\| of the total strain rate in global axes** (not ε̇_p, not frame-invariant, no cap); Grüneisen: compression branch with Hugoniot reference, **linear expansion branch** p = ρ₀C₀²μ + γ₀E, Γ = γ₀ exactly for a = 0, no tension cut-off; stress rate Jaumann | small for C = 0.001 (CE 1.018 at 10⁸ s⁻¹) | §35 |
| P-HG-Al: JC A 148.4, B 345.5 MPa, n 0.183, C 0.001, m 0.895, T_r 293 K, T_m 933 K; Grüneisen C₀ 5305.5 m/s (√(B/ρ)), s 1.339, γ₀ 2.17; k 237 W/(m K) | | §8.3, data/properties.csv |
| LAW2 (solid Johnson–Cook) against LAW4 (source reading, §40): LAW2 accepts `/EOS/GRUNEISEN` and heats the same way (plastic work, EOS compression); **no melt branch**: above T_m, 1 − T*ᵐ < 0, the yield stress turns negative and the deviator is reversed (not zeroed), and plastic-work heating turns negative; T_max (switch to m = 1) is unused for JC; on TLSPH the hourglass modulus is σ_y once plastic (LAW4: E) | LAW2 is not a drop-in for the §25 quad deck (its edge reaches 1.03–1.08 T_m) without a melt guard, and it carries no length either | §40 |
| Ti-6Al-4V JC and EOS are second-hand (Khamsepour 2022 citing Meyer & Kleponis, Steinberg); primaries not retrieved | verify before any claim | §26 |

## Maintenance

- At every merge of a WSL section, the modeller adds or updates the lines it touches, in the same commit.
- A fact that is later found wrong is struck through and corrected, with the section that corrected it.
