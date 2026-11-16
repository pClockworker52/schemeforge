<!-- Odds reviewer 2, 2026-11-16. Fresh general-purpose agent given prompt.md; the modeller's odds withheld. Saved verbatim below this line. -->

# Odds review 2026-11-16: independent estimate

**Scope and exclusions.** I read the prompt, `state-report-no-odds.md`, DECISIONS.md from "2026-11-12 — Set-up S′ not adopted" to the end, `opencourant-verification.md` §20–§23, and `data/boundary_integration_reading.md`. I opened no excluded file. I saw none of the modeller's probabilities. The only mention I met was DECISIONS 2026-11-15, D-consequences: "the modeller's odds … are not revised here", and it gives no numbers. I did not use web search. All base rates below come from the repository and are labelled as such. Every probability is my **judgment**. The measured numbers I cite are the inputs to it.

## P1: the trigger run passes: **≈ 6 % (2–15 %)**

Dominant factors:
1. **Y − 1 on the conforming sphere is far outside the limit.** The skin on T-S1 at R/64 reads Y − 1 13 % low on both discs, and 33–37 % low at R/32 (§23.3). The sphere is still the lattice under F2 (§23.2, "Choice"). On T-B2 the limit is 3.5 % + U_ref, with U_ref(Y − 1) between 1.80 and 3.00 % (DECISIONS 2026-11-16, item 1), so at most 6.5 %. Clause 1 fires on the sphere side unless the sphere surface changes.
2. **Clause 2 has no noise floor.** It fires if |e(R/64)| > 0.8·|e(R/32)| (DECISIONS 2026-11-15, D4). Any quantity that is already accurate at R/32 can trip it. On T-S1 the skin p_n went from +0.3 to +3.6 % on the axis and from +2.8 to +3.1 % at 0.5 a (§23.3), so both would trip it. The project already recorded "a growth clause without a noise floor" as a lesson (DECISIONS 2026-11-13, CS-18 refuted). The trigger judges eight averages (p_n and Y − 1, two discs, two sides), and each must pass both clauses.
3. **The block-side p_n was high before F2.** It was +7.8 / +4.9 % at R/64 against quad R/128 (§22.2). The rising reference moves it inward by about 1 % (U_ref p_n on the axis 0.89–1.31 %, §23.1). F2 fixes flat columns (0.021 against 0.381, §23.2), but it is untested under a Hertz patch.

**What would move it most:** the momentum-restoring VCI passing its gate and being chosen (DECISIONS 2026-11-16, item 2). Original VCI made the sphere's whole-skin uniform pressure exact and put case 5 at 1.07 / 0.95, against the lattice's 0.69 / 0.63 (§23.2). If it wins, I would put P1 at about 15–20 %. If F2 stays, about 3 %.

## P2: full ladder given P1: **≈ 25 % (10–45 %)**

1. **Base rate in this project:** every frozen campaign since 2026-11-08 stopped at its first non-trivial rung. That covers collocated B-2/B-3/D-1 (§14), S′ (§15), CS-18 at T-S0 (§16) and CS-18b at T-S1 (§20.1). The state report's Track B table says the same.
2. **Bonded and cohesive rungs have never run under TLSPH** (state report, "Current technical state"). The only bonded-bar result, from collocated SPH, missed by 0.285 V against a limit of 0.05 V (§14). The tension limit of 0.095 V is loose by construction (DECISIONS 2026-11-14, freeze), which helps the pass chance but weakens what a pass means.
3. **High velocity:** the BCT-off survival probe passes only at R/16 and R/32 (§23.1). Profizi's TLSPH failed at finer meshes at 600–900 m/s (DECISIONS 2026-11-12, SPEC-TL entry).

**What would move it most:** the first bonded rung (T-B1–T-B3 / T-D1). A pass would raise P2 roughly to 40 %.

## P3: 0.5 µm interface averages converge in a 3D plastic jetting impact: **≈ 7 % (2–20 %)**

1. **No host, and no published simulation the project has read, shows this** (state report, "Not understood", third bullet). Tang 2021 reports neither Y nor p_n under refinement. Its strains "vary drastically with grid size", and its shape and jetting still change between 1.0 and 0.7 µm (boundary_integration_reading.md, G item 5).
2. **There is no physical length at the jet.** The 2D FE mesh fails at the jet root earlier as it is refined (state report, Track B table, 2026-11-04). The 0.5 µm length is an averaging choice, not a regularisation (DECISIONS 2026-11-14, item 4).
3. **Reachable resolution is low.** The full T-B2 block at R/64 already needs about 40 GB on a 15 GB machine (§22.1). At R/32 the disc is only 1.6 spacings (§22.1). A plastic convergence study would have two points at most, and the coarse one under-resolved.

**What would move it most:** a published or in-project 3D result showing p_n or Y converging near a jetting edge. I know of none (judgment).

## P4: the whole chain: **≈ 0.3 % (0.05–1.5 %), below 1 %**

I take this as P1 × P2 × P(plastic interface convergence | P1, P2) ≈ 0.3 × P(the bond in the solver gives a verified rebound and v_cr) ≈ 0.6. That is about 0.06 × 0.25 × 0.3 × 0.6 ≈ 0.3 %.
1. P1 and P3 dominate: the surface pattern (state report, "Pattern").
2. **Measurement of temperature and bonded area is still undefined** (DECISIONS 2026-11-15, D2), and the equation journal check is still owed (DECISIONS 2026-11-12, CS-18 freeze).
3. **v_cr needs a velocity sweep of 3D plastic runs at the cost limit** (§22.1).

**What would move it most:** a P1 pass, about a factor of 5–10 upward. A trigger fire sets P4 to roughly zero by design (D4, "If it fires").

## P5: the first claim with a one-way bond: **≈ 1 % (0.2–3 %)**

A one-way bond removes the bonded, cohesive and tension rungs, and the solver-feedback step. It keeps P1 and P3, because requirement 2 (the interface state) is unchanged. It buys about a factor of 2–3, not an order of magnitude (judgment). It also turns v_cr into a lower bound (state report, question 3).

## Base rates used
- **In-project ladder record:** 4 of 4 particle configurations stopped since 2026-11-08, plus FE and heat conduction ruled out before that (state report, Track B).
- **Modeller predictions:** often wrong on this method family (§20.5, §22.3, §23.4; state report, "Weaknesses"). I discounted the implied optimism behind each calibration step.
- **Literature:** none of about 6 full-text papers verifies Y or p_n against a converged reference (state report; reading, G). In Hillman 2013, direct nodal integration fails the traction patch test (reading, E), and TLSPH is that method (reading, claim table).
- **External base rates:** not obtained, because I did no web search.

## Is P1 → P2 → P4 the right decomposition?

No, two steps are missing.
- **Before P1: the construction choice.** The result depends on whether momentum-restoring VCI or F2 is frozen, which is still open (DECISIONS 2026-11-16).
- **Between P2 and P4: interface convergence in plastic, jetting impact.** Every rung on the ladder has an exact or converged reference. The cold-spray impact does not, and P3 is the step no ladder rung tests. P2's elastic-plastic and high-velocity rungs do not imply it.

It is also worth stating plainly that clause 2 as written can fire on noise. Adding a floor now would be post hoc, because the T-S1 skin numbers have been seen. If it is done, it needs to be labelled post hoc.

## Is continuing to the trigger run worth it? (judgment)

Yes, provided it stays bounded. The run is a few machine-hours: T-S1 at three resolutions took 1 h 26 min (§20.4). It turns an argued dead end into a recorded one under a rule written in advance, which is worth more than abandoning the route on judgment. Its expected outcome is a fire. The case for running it is a clean, citable stop, not hope for P4.

Two things make it less bounded than it looks. The trigger run is waiting on the momentum-restoring VCI build (DECISIONS 2026-11-16, Consequences), and that build should get its own time box. And if the run is to be read fairly, clause 2's missing floor needs to be settled openly beforehand.

With P4 well below 1 %, the reduced route (D3 (iv)) should be prepared now, in parallel, not after the fire.
