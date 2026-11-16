<!-- Odds reviewer 1, 2026-11-16. Fresh general-purpose agent given prompt.md; the modeller's odds withheld. Saved verbatim below this line. -->

# Odds review, 2026-11-16 (independent reviewer)

**What I read:** the prompt; `state-report-no-odds.md`; `docs/DECISIONS.md` from "2026-11-12 — Set-up S′ not adopted" to the end; `opencourant-verification.md` §20–§23; `data/boundary_integration_reading.md`.

**Exclusions kept:** I did not open any excluded file and did not see the modeller's numbers. DECISIONS 2026-11-15 (Consequences) mentions that the modeller's odds exist, but it gives no values. I ran no web search, so I used no external numeric base rate. The base rates below come from the repository.

All probabilities are judgment. The evidence behind each is cited.

## P1: the trigger run passes. **8 % (3–20 %)**

Dominant factors:
1. **Y − 1 is already far outside the threshold on the nearest analogue.**
   - Skin on T-S1 at R/64: Y − 1 is 13 % low on both discs; at R/32 it is 33–37 % low (§23.3).
   - The trigger allows 3.5 % + U_ref, and U_ref(Y − 1) is 1.80–3.00 % (§23.1; DECISIONS 2026-11-16 item 1). So the limit is at most about 6.5 %.
   - On T-B2 the sphere side is still the lattice sphere ("on the sphere F2 is the lattice", §23.2). That is the same surface that gave −13 % on T-S1.
   - Clause 1 is therefore likely to fire on sphere-side Y − 1 unless the two-body deck behaves materially differently.
2. **Clause 2 has no noise floor, and p_n already "diverges" on T-S1.**
   - Skin p_n on T-S1 goes from +0.3 / +2.8 % at R/32 to +3.6 / +3.1 % at R/64 (§23.3). On the axis that is |e64| > 0.8·|e32|.
   - If T-B2 behaves the same way, clause 2 fires on an average that is inside clause 1's band.
   - This repeats the flaw recorded at CS-18: "a growth clause without a noise floor" (DECISIONS 2026-11-13).
3. **Block side under F2 is unmeasured.**
   - On the lattice block, p_n was +10.0 / +10.3 % at R/32 and +7.8 / +4.9 % at R/64 (§22.2). The ratios of 0.78 and 0.48 pass clause 2 only narrowly.
   - F2's advantage was shown on flat columns only (S 0.369 against 0.381, §23.2).
   - The interface file still lists the static surface set (DECISIONS 2026-11-16, Context).

**Biggest mover:** sphere-side Y − 1 on T-B2 at R/64. Within 6.5 % would move P1 up sharply, to above 30 %. A miss settles it. The momentum-restoring VCI on the sphere (DECISIONS 2026-11-16 item 2) is the only planned change that could plausibly lift sphere-side Y − 1.

## P2: the full ladder passes, given P1. **30 % (15–50 %)**

Dominant factors:
1. **The rungs that remain have never run under any TLSPH set-up.** These are tension, zero-energy, bonded, cohesive and Bay activation (state report, "Not yet run"; §20.1). Collocated SPH failed the bonded bar badly: 0.285 V against a 0.05 V limit (state report table, §14).
2. **The record of host ladders.** Every one so far stopped at a core rung: CS-18 at T-S0 (§16), CS-18b at T-S1 (§20.1), collocated B-2 / B-3 / D-1 (§14), and S′ (§15). That is zero full passes in four attempts.
3. **High-velocity plastic survival is only partly shown.**
   - The BCT-off probe passes at R/16 and R/32 with contact only and no bond (§23.1).
   - Profizi's TLSPH without an update failed on finer meshes at 600–900 m/s (DECISIONS 2026-11-12, TLSPH set-up).

Conditioning on P1 raises this figure, because a P1 pass would mean the surface treatment works better than the evidence suggests.

**Biggest mover:** the bonded-bar and tension rungs. A pass on them would move P2 up the most.

## P3: interface quantities converge as 0.5 µm averages in 3D plastic jetting, at reachable resolutions. **7 % (2–20 %)**

Dominant factors:
1. **No host and no paper read has shown it.**
   - FE in 2D and 3D, collocated SPH and TLSPH all failed to show converged edge quantities (state report, "Not understood").
   - Tang 2021 does not report Y or p_n under refinement. Its strains "vary drastically with grid size refinement", and its bonded fraction is grid-regularised through D_Cell (boundary reading, G.5).
2. **The 0.5 µm length is an averaging length, not a physical regularisation.**
   - The constitutive model has no length scale (state report, question 2).
   - Jetting localises at a width set by the discretisation. Averaging does not remove that dependence near the contact edge, which is where Bay activation happens.
3. **Reachable resolution.**
   - The full elastic T-B2 block at R/64 already needs about 40 GB on a 15 GB machine (§22.1).
   - At R/32 the 0.5 µm disc spans 1.6 spacings (§22.1).
   - Two resolutions, one of them on a reduced domain, cannot show convergence. §21.5 makes the same point: "two resolutions do not show convergence".
   - There is also no converged reference for plastic jetting, because the 2D quads fail at the jet root (state report table, 2026-11-04).

**Biggest mover:** a three-resolution plastic self-convergence of disc-averaged Y and p_n away from the jet, in any host. Success would raise P3 several-fold. Failure would cap P4 near zero whatever happens at P1 and P2.

## P4: the whole chain. **Below 1 %: about 0.3 % (0.05–2 %)**

This is roughly P1 × P2 × P(P3 | P1, P2) × P(rest), that is 0.08 × 0.30 × about 0.25 × about 0.6.
- I set P3 conditional on P1 and P2 higher than unconditional: the correlation is positive.
- "Rest" covers four items:
  - the measurement definitions for temperature and bonded area, still open (DECISIONS 2026-11-15 D2);
  - a 3D v_cr velocity sweep at affordable cost;
  - the journal check of eqs. 15, 17, 24 and 32 (DECISIONS 2026-11-12, freeze entry);
  - Bay activation behaving under refinement.

The probability is below 1 %, and I am not rounding it up.

**Biggest mover:** P3. The other steps lie on a path that has been shown at least partially; P3 has not been shown anywhere.

## P5: the first claim with a one-way bond. **About 1 % (0.3–4 %)**

- A one-way bond removes the tension, cohesive and bonded rungs from P2 (DECISIONS 2026-11-15 D4: "A pass … licenses drafting CS-18c with its tension, cohesive, bonded and plastic rungs"). That raises my P2 to about 45 %.
- It does nothing for P1 or P3: Y and p_n must still be right at the surface and converged under jetting.
- The gain is therefore about a factor of 2–3, not an order of magnitude.
- Per the state report's question 3, v_cr becomes a lower bound.

## Base rates used

- **Track B host attempts** (state report Track B table; §14–§23): about 7 stopped or refuted; 0 full ladder passes.
- **Track A hunches meeting blind data** (state report, "Record so far"): 6, of which 1 was supported but exposed.
- **Modeller's own prediction record:** wrong on CS-18, CS-18b, S′ and parts of §20.5, §22.3 and §23.4 (state report, "Weaknesses"; §23.4). Treat favourable expectations from this method family with a discount.
- **Literature:** none of the roughly six full-text cold-spray papers read verifies the interface state against a converged reference (state report, "Not understood"; boundary reading, G). No numeric external base rate was used.

## Is P1 → P2 → P4 the right decomposition?

No. **P3 is the missing, and decisive, step.**
- The trigger and the ladder are elastic or elastic-plastic verification cases. Nothing on the path tests convergence of interface averages under plastic jetting until the claim itself. So the chain can pass P1 and P2 and still fail at the end.
- **A second missing step is a reference for plastic jetting.** Without one, P3 can only be self-convergence, and §22.1 shows the resolution budget is already exhausted at elastic R/64.

I would make P3 an explicit gate, tested cheaply and early, independent of TLSPH. For example: disc-averaged Y and p_n at three resolutions in a reduced 3D plastic deck.

## Is continuing to the trigger run worth it? (judgment)

Yes, provided it stays bounded. Its main value is closing a branch under a rule written in advance, not a meaningful chance of passing.
- The T-S1 skin data (§23.3) already predict a likely fire on Y − 1, and possibly on the p_n growth clause. The information gained is therefore modest.
- The cost is small, and a clean pre-registered stop is worth having: the trigger has already been amended twice, once after the reference result was seen (DECISIONS 2026-11-15 "D3 reopened"; 2026-11-16 item 1).
- **I would not spend more than a short, fixed budget on the momentum-restoring VCI before the run.**
- **I would not amend the trigger again,** including the missing noise floor on clause 2. Flag it in the committed prediction instead.
- **The more valuable next step is the P3 probe.** Whatever the trigger says, it decides whether any particle-host route, or the in-solver bond, can deliver the first claim as defined.
