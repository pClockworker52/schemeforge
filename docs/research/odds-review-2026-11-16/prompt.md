# Odds review 2026-11-16: prompt given to both reviewers (verbatim)

You are an independent reviewer estimating success probabilities for a computational-mechanics project
(cold-spray particle impact simulation). You have no stake in its earlier choices. The project owner asked for these
estimates because the modeller's own estimates may be anchored and biased upward; your job is an honest, calibrated
estimate, not encouragement.

Repository: /home/user/schemeforge (read-only; do not edit, commit or run solvers).

Read fully:
1. docs/research/odds-review-2026-11-16/state-report-no-odds.md (the state report; the modeller's odds are removed).
2. docs/DECISIONS.md, the entries from "2026-11-12 — Set-up S′ not adopted" to the end (the requirements, the
   route review of 2026-11-15, the D3 reopening and the 2026-11-16 entry after §23).
3. docs/research/opencourant-verification.md §20–§23 (numbers; §14–§19 if you need history).
4. docs/research/data/boundary_integration_reading.md (literature on the surface deficit).
You may also use web search for base rates (e.g. how often published cold-spray or particle-method simulations show
converged interface quantities, or how often comparable verification campaigns succeed).

STRICT exclusions, to keep you unanchored: do NOT open docs/STATUS.md, docs/HANDOFF.md, anything in
docs/research/route-review-2026-11-15/, docs/research/sph-route-review-2026-11*.md, the Claude Docs state report
itself, any file in docs/research/odds-review-2026-11-16/ other than state-report-no-odds.md and this prompt, or any
text that states the modeller's probability estimates. If you meet such numbers by accident, say so in your answer.

Estimate, each as a probability with a range, from the current state:
- P1: the frozen trigger run (DECISIONS: D4 as amended on 2026-11-15 and 2026-11-16; T-B2 elastic, R/32 and R/64,
  skin p_n and Y − 1) passes, i.e. the dead-end trigger does not fire.
- P2: given P1, the TLSPH host then passes its full ladder (tension, zero-energy, cohesive and bonded rungs,
  elastic-plastic and high-velocity cases).
- P3: interface quantities (p_n, Y) converge as 0.5 µm surface averages in 3D in a plastic, jetting cold-spray impact
  at resolutions this project can reach.
- P4: the whole chain: a verified first claim with shape, rebound, v_cr and interface state, with the bond acting in
  the solver, in 3D, under the project's own rules.
- P5: the first claim, if the owner instead allowed a one-way bond (Bay criterion evaluated afterwards).

For each: the number and range; the two or three factors that dominate it, each with the file and section it rests
on; and the result that would move it most, in which direction. Then:
- the base rates you used, and where they come from;
- whether you think the chain decomposition P1 → P2 → P4 is the right one, or which step is missing;
- one paragraph: is continuing to the trigger run worth it, as judgment, given that the trigger run is a bounded cost.

Rules: cite files and sections for every number you use; do not invent numbers; label judgment as judgment; do not
round a small number up to make it look meaningful, and say plainly if a probability is below 1 %. Be concise
(600–1200 words). Your final message is saved verbatim as your review, so write it as a finished Markdown document.
