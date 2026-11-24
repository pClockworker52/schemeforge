# Review: cold-spray track, local-means question

**Scope:** I read only `docs/research/coldspray-orientation-2026-11-24.md`. I opened no other file and used no web search.

## Verdict: STOP

On the note's evidence, the local means cannot answer any question in this domain under a rule that is fixed in advance, can fail, and is judged on unseen data or an exact reference.

### The lines that decide it

1. **"what the local solver can deliver is whole-body or area-integrated quantities. What the data can judge is v_cr windows and a few stacks."** (§"Not answerable with local means", closing paragraph). Any surviving question must sit where these two meet. Apart from those, the only possible judge is an exact solution.
2. **"More blind v_cr tests (R1) | Blind list 1 is used up; the stop rule gives no blind list 2"** (§"Not answerable", table row 4). This closes the v_cr-window side of that overlap.
3. **"R2 … There is no hunch, and a hunch needs unseen stacks"** and **"R3 … the ring data are exposed (any comparison is post hoc)"** (§"Still open"). This closes the stack side and the ring side. On rings, §"Housekeeping" adds: "There is no unseen ring-map source."

### Why no candidate survives

- **v_cr windows (R1):** the solver's integrated output could be compared with v_cr, but no unseen v_cr data remain (§"Not answerable", row 4). Mohanty 2022 is post hoc and "one series cannot move R1" (§"Housekeeping").
- **Stacks (R2):** a judged hunch needs unseen stacks. The only stack analysis named is "exploratory, post hoc" on Reiser 2024 (§"Still open"). The note names no unseen stack source in hand, and new measurements are outside local means (§"Still open", external measurements parked).
- **Ring onset (R3):** only a post hoc comparison is possible (§"Still open"). *Judgment:* a post hoc match with a kinematic geometry estimate would let the project claim only consistency with data it had already seen. That does not justify spending part of the hunch budget, which stands at 3 of 5 (§"Still open").
- **Exact-reference judging:** the exact-solution checks the note lists are solver facts that already hold: elastic bulk verified, energy to 0.25 %, a(t) converges, cs12 energy closes (§"Answered", solver-facts). These are verification results, not bonding questions. The one bonding-relevant integrated quantity, a rebound difference from an in-solver bond, is refuted under sticking bonds "at every δ_c" (§"Not answerable", row 2). The resolved interface state and the physical-length cure are both closed (rows 1 and 3).
- **Arena upgrade:** this needs "about 15 matched materials, a held-out set frozen by someone else" (§"Where the track sits"). None of that is local.

None of the obstacles the note lists has a removal I can name from local means. Each one needs either unseen data that the note does not say exist, or external measurements, which are parked.

### What follows (judgment)

This verdict supports option 1 in §"The one question for Peter": pause the track with the note as its closing state and resume Phase 6 at step 6. The note estimates that step at about one session (§"Where the track sits"). The track stays resumable from here.

## Confidence

**Medium** (judgment). Each closure is stated directly in the note, except one. On stacks the note says a hunch "needs unseen stacks" but never says whether any exist in hand. For ring maps, by contrast, it rules them out explicitly. So the R2 closure rests partly on the note being silent.

## The one fact that would change the verdict most

**A set of build-up stacks already in hand, not yet looked at, and not from Reiser 2024.** If such a set exists, the verdict would become QUESTION: an R2 build-up rule over a finite, particle-level quantity, judged on those stacks. The pass/fail rule would be registered as a hunch before anyone opens the data (§"Still open"; CLAUDE.md rule 5). Without that set, the answer is STOP.
