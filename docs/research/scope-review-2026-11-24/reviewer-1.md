# Review: cold-spray track, local-means question

**Reviewer scope:** I read only `docs/research/coldspray-orientation-2026-11-24.md`. I opened no other file and did not search the web.

## Verdict: STOP

On the note's evidence, the local means can produce no question whose answer can be judged on unseen data or against an exact reference and is worth what it costs.

### The lines that decide it

1. **What the solver can deliver and what the data can judge do not overlap.** The section "Not answerable with local means, and why" ends: *"what the local solver can deliver is **whole-body or area-integrated quantities**. What the data can judge is **v_cr windows and a few stacks**."* The only route from the solver to a v_cr window is the in-solver chain. The same section says the chain has failed: *"with sticking bonds CS-23 is refuted at every δ_c"*, and an independent review put the whole in-solver chain at *"about 0.3 %"*.
2. **None of the routes that skip the solver has unseen data left to judge it.**
   - **R1:** *"Blind list 1 is used up; the stop rule gives no blind list 2"* (table, row R1).
   - **R2:** *"There is no hunch, and a hunch needs unseen stacks"* ("Still open"). The note names only the Reiser 2024 stacks, and those already have a post hoc answer.
   - **R3:** *"the ring data are exposed (any comparison is post hoc)"* ("Still open"). Also *"There is no unseen ring-map source"* (Housekeeping, CS-20).
3. **Point values at the contact edge are ruled out, and the proposed fix for that is gone too.** Edge point values *"do not converge on any host"*. The physical-length fix has *"No zero-code host; the band check found no band narrowing with the mesh"* (table, rows 1 and 3).

### Why the remaining candidates do not pass

I checked every candidate the note leaves open. The obstacle the note names for each one still stands.

- **R2, particle-level build-up rule.** The finite quantity is fine: a stack-level, particle-level rule. The judge is the problem. The only data named are exposed, so any verdict would be post hoc. Removing that obstacle needs unseen stacks. The note does not say any are in hand, and new measurements are parked ("Still open", External measurements). Judgment: a post hoc fit to exposed stacks could only support "consistent with Reiser 2024". That is not worth a hunch slot (budget 3 of 5).
- **R3, kinematic Bay estimate.** The finite quantity, a geometric ring estimate, could be computed. But the only comparison data are exposed, and no unseen ring-map source exists (Housekeeping, CS-20). The geometry code could be checked against an exact sphere-geometry result. Judgment: that would be a code test, not a question about this domain. The code "and its tests exist" already ("Still open").
- **More solver verification against exact elastic solutions.** The note already lists verified elastic bulk TLSPH, energy closed to 0.25 % and converging integral quantities ("Answered"). Judgment: repeating that would be a rediscovery of what the record already holds and would let the project claim nothing new.
- **Track B design questions** (friction, hot-edge choice). The note files these under a paused track and says they *"belong to it, not to the track's direction"* ("Still open"). They do not answer the review question.

### What stopping leaves standing

Stopping takes nothing away from the results already in hand ("Answered"):

- sound speed carries most of the v_cr signal (Z6, CS-03);
- oxide raises v_cr within one metal (CS-07);
- bonding starts in a ring (exposed);
- the solver facts listed there.

Those are the track's closing state. The note's option 1 is to pause cold spray and resume Phase 6 at step 6 ("The one question for Peter"). That option is consistent with this verdict. Whether to take it is Peter's call, not mine.

## Confidence

**Medium** (judgment). The note states each block explicitly and cites a source for each. My uncertainty comes from what the note leaves out, not from what it says. The note says R2 *needs* unseen stacks, but it never says whether any unseen stack data are already in hand. *"a few stacks"* in the common-thread line is ambiguous on this point.

## The one fact that would change the verdict most

**A stack dataset already in hand that has not been used in the 2026-11-07 Q-B1 answer or any other exposure, large enough to judge against.** If one exists, R2 becomes a QUESTION:

- **Quantity:** a particle-level build-up quantity per stack.
- **Judge:** the unseen stacks.
- **Rule:** fixed in a hunch before any run, with a kill criterion.
- **Claim on a pass:** a build-up rule that predicts out of sample.

The note gives no sign that such a dataset exists. On the record as written, the answer is STOP.
