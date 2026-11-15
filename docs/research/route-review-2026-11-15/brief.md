# Route review 2026-11-15: session brief

**Why now.** The rule fixed before calibration task 2026-11-15-a was not met (DECISIONS 2026-11-15, §22). By that
rule this is "the next failure", and the review comes before any further BCT variant or new hunch. Peter decides;
the modeller prepares and records.

**Read first:**
- this brief;
- the state report (Claude Docs, "Cold-spray simulation: state report", 2026-11-15; repository equivalent: STATUS,
  HANDOFF, DECISIONS 2026-11-12 to 2026-11-15);
- [inputs.md](inputs.md): two external texts and the modeller's critiques;
- for numbers, opencourant-verification.md §14–§22.

Sections 1–3 are facts and options. Section 4 holds the modeller's recommendations and is withheld from independent
reviewers (D6).

## 1. Facts (all from committed rows)

| Item | Value | Source |
|---|---|---|
| T-S1 (sphere on rigid wall, 20 m/s), TLSPH, BCT on, R/32 | rebound 0.860, contact time 5.3 % short: CS-18b refuted | §20 |
| T-S1, TLSPH, BCT off, R/32 | rebound 0.9988, peak 1.060 (reference 1.062), approach 0.928 (0.956) | §20.5, §21.3 |
| T-B2 geometry (sphere on block), TLSPH, BCT off, R/32 | peak 1.054, approach 0.952, rebound 0.999 (quad R/128: 1.047 / 0.976) | §21.2 |
| BCT defect | diagonal scaling of the spreading operator; rim loads 2–3× on small or changing patches, flat faces too | §21.1 |
| Face-layer deficit, BCT off | layers 1–2 at 0.62 / 0.86 of the stress, against a rigid wall and a deformable column alike | §19.2, §22.2 |
| 0.5 µm averages, BCT off, T-B2 deck | within 3.5 %: 4 of 20 (R/32), 6 of 20 (R/64, reduced block); block band 1: −24 / −18 % (R/32), −8 / −9 % (R/64); face layer 0.59 / 0.50; sphere side within 3.7 % at R/64 | §22.2 |
| Contact pressure p_n (from penalty forces), block side | 5–10 % high | §22.2 |
| Quad reference drift R/64 → R/128 | 2–4 % | §22.2 |
| Averaging window against kernel reach | at R/32 (10 µm particle): s = 0.31 µm, h = 1.12 s, kernel reach ≈ 0.7 µm > 0.5 µm window | §22.1; input 2 |
| Memory | full T-B2 block at R/64 ≈ 4.7 million particles, ≈ 40 GB (machine 15 GB) | §22.1 |
| Viscous + hourglass work / KE0 | BCT on 0.33 + 0.15; BCT variant up to 0.49; BCT off 0.0016 + 0.0001 | §20.2, §20.5, §21.5 |
| TLSPH internal energy | not implemented; no energy balance can be closed | known limit 3 of CS-18b |
| Not yet run on TLSPH | tension, zero-energy modes, cohesive and bonded rungs, Bay activation, any plastic impact with BCT off | §20.1 |
| Earlier hosts | 2D FE: jet-root collapse at 5–37 % of penetration; collocated SPH: two-body Hertz B-2 fails; S′: rebound falls with refinement | §8, §14, §15 |
| Hunch budget | 3 of 5 open (CS-10, CS-12, CS-17, all track A) | coldspray-hunches.md |
| Modeller's odds after §22 (judgment) | TLSPH host passes full ladder 10–20 %; edge convergence 15–25 %; one-way first claim 6–10 %; whole chain 3–5 % | state report |

## 2. Requirements in force (DECISIONS 2026-11-12, amended 2026-11-14)

(a) shape, rebound and v_cr, and the interface state; (b) the bond acts in the solver during the impact; (c) 3D.
Interface outputs are judged as averages over 0.5 µm; point values at the edge are reported only.

## 3. Decisions to take

**D1. Requirement (b): in-solver bond or one-way bond for the first claim?**
- (i) keep (b);
- (ii) one-way first: contact only, Bay criterion evaluated afterwards; exact until the first point bonds anywhere;
  v_cr becomes a lower bound; the in-solver bond is a second stage.

**D2. The averaging length against the host's resolution.** A 0.5 µm window lies inside the kernel reach at R/32;
several kernel reaches would need about R/100 in 3D. Options:
- (i) keep 0.5 µm and accept that 3D needs a resolution this machine cannot reach;
- (ii) measure surface quantities on a surface (a measurement-only skin: Y from facet stretch, p_n per facet), so
  that the depth band is no longer needed;
- (iii) a coarser averaging length, only if it can be justified physically (not for numerical convenience);
- (iv) 2D axisymmetric work for resolution studies, which relaxes (c) for that purpose.

**D3. Host.**
- (i) TLSPH with BCT off, plus a measurement skin, plus the best flat-face construction;
- (ii) another particle host (UL SPH; MPM, where Tang 2021 claims discretisation independence, not yet read);
- (iii) FE with remeshing (not available in OpenCourant for 2D elements);
- (iv) a reduced route: a particle-level build-up rule or the closed form, using track A.

**D4. Dead-end trigger, written before any further result.** It names a host, resolutions, quantities, a threshold
above the reference's own uncertainty, and what happens if it fires.

**D5. Order of work.** Candidates:
- a literature check on boundary integration and patch tests in corrected particle methods (WSL B);
- a flat face with a fitted outer layer, built like the conforming sphere (WSL A, cheap);
- a measurement skin (WSL A);
- TLSPH internal energy (WSL A; before any plastic run).

**D6. Independent reviewers before the decision?** Two fresh general-purpose agents, each given sections 1–3, the
state report and inputs.md, but not section 4, answer D1–D4 separately. Their answers are saved verbatim in this
folder.

## 4. Modeller's recommendations (withheld from independent reviewers)

Judgment, not results; the modeller's predictions on this track have been wrong several times.
- **D1: (ii), one-way first.** It removes the tension and bond risks without touching the surface problem, and is
  exact until first bonding. The in-solver bond follows once the one-way claim stands.
- **D2: (ii), measure on a surface,** and state plainly what resolution a depth-band average would need. Do not
  change the physical length for numerical reasons.
- **D3: (i) as a short, capped calibration** (fitted flat face and measurement skin), with (iv) as the named fallback.
  (ii) only after Tang 2021 is read.
- **D4, draft for Peter's wording:** "If TLSPH with BCT off, a measurement skin and the best flat-face construction
  does not bring the 0.5 µm averages of p_n and Y on the T-B2 deck within X % of the converged quad reference at R/32
  and R/64, the 3D particle-host route for the interface state stops, and the project moves to the reduced route."
  X is set above the reference's drift.
- **D5:** literature check and fitted flat face first, in parallel (both cheap and decisive); then the skin; internal
  energy before any plastic run.
- **D6: yes,** two reviewers; it costs little and counters anchoring on this session's line of argument.

## 5. How to run the session

1. Peter starts a fresh session (after /clear): "Read docs/research/route-review-2026-11-15/brief.md and run the
   route review."
2. If D6 is yes: start the two reviewers first (sections 1–3, the state report, inputs.md; not section 4). Save each
   answer verbatim as reviewer-1.md and reviewer-2.md in this folder.
3. Go through D1–D5 with Peter, one at a time; for each, show the options, the reviewers' answers and the modeller's
   recommendation.
4. **Outputs:**
   - a DECISIONS entry "Route review 2026-11-15";
   - an amendment of the requirements if D1 or D2 changes them;
   - the dead-end trigger as worded by Peter;
   - new tasks in tasks/wsl-a.md and tasks/wsl-b.md;
   - STATUS and HANDOFF updated;
   - the state report updated.
5. No hunch is registered and no run is started in the session itself.
