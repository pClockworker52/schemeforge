# Odds review 2026-11-16: summary

Two fresh general-purpose reviewers estimated the odds independently (prompt.md; answers verbatim in reviewer-1.md
and reviewer-2.md). Neither saw the modeller's estimates: the state report was given without its Odds section, and
STATUS, HANDOFF and the route-review folder were excluded. Neither used web search, so their base rates come from the
repository. All figures are judgment, not judge results.

| Milestone | Reviewer 1 | Reviewer 2 | Modeller (2026-11-16, chat) |
|---|---|---|---|
| P1: the trigger run passes | 8 % (3–20) | 6 % (2–15) | 10–20 % |
| P2: full TLSPH ladder, given P1 | 30 % (15–50) | 25 % (10–45) | — |
| P3: 0.5 µm interface averages converge in 3D plastic jetting | 7 % (2–20) | 7 % (2–20) | 20–30 % |
| **P4: whole chain, bond in the solver** | **0.3 % (0.05–2)** | **0.3 % (0.05–1.5)** | 3–6 % |
| P5: first claim with a one-way bond | ≈ 1 % (0.3–4) | ≈ 1 % (0.2–3) | ≈ 8–12 % |

The modeller's figures are about ten times higher on P4 and P5. That fits the upward bias the modeller had flagged
itself: the figures were drafted on this route and anchored step by step.

**Points both reviewers raise:**
- **Y − 1 on the sphere is the likely fire of clause 1.**
  - The T-S1 skin reads Y − 1 13 % low at R/64 (§23.3).
  - The limit is at most about 6.5 % (3.5 % + U_ref).
  - On T-B2 the sphere is still the lattice under F2 (§23.2).
- **Clause 2 has no noise floor.** It can fire on averages that are already accurate (T-S1 skin p_n +0.3 → +3.6 %
  on the axis). This repeats the lesson recorded at CS-18. The modeller drafted D4 and missed it. Adding a floor now
  would be post hoc.
- **P3 is the missing gate.** No rung tests interface convergence in plastic, jetting impact, and no source read
  shows it. Both reviewers suggest a cheap early P3 probe that does not depend on TLSPH.
- **The trigger run is worth running as a bounded cost,** for a clean, pre-registered stop rather than in hope of
  P4. Time-box the momentum-restoring VCI build. Do not amend the trigger again.
- **Reviewer 2 adds:** prepare the reduced route now, in parallel.
