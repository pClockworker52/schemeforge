# Cold-spray track: orientation (2026-11-24)

Written by the modeller at Peter's request ("Do we need an orientation and a clear?"), after the length path was
stopped (DECISIONS 2026-11-24). **From the record only: no new claim, no new proposal beyond the closing question.**
Every line points to its source.

## Where the track sits in the project

- **The cold-spray track is a side track.** Schemeforge's main line, Phase 6 (Arena 2: third-medium contact), was
  paused on 2026-11-03 at a clean checkpoint. Steps 1–5 were done and step 6 had not started: blind audit, Target D,
  tag `contact-v1.0`. The phase plan estimates step 6 at about one session (DECISIONS 2026-11-03 "Arena 2 paused";
  docs/plans/2026-10-30-phase6.md).
- The track was opened as **"research-first, discipline only"**. Upgrading it to an arena requires about 15 matched
  materials, a held-out set frozen by someone else, and a reference that separates the zoo (DECISIONS 2026-11-03).
- **Since 2026-11-17 the track's official main line has been the reduced route** (DECISIONS "Track B interface-state
  route closed; reduced route adopted"; reduced-route-plan.md). Its open question, "which of R1–R3 is the main
  line?", was never answered.

## Answered (what holds)

From coldspray-synthesis-single-impact.md §1:
- sound speed carries most of the v_cr signal for pure metals (Z6, CS-03);
- oxide raises v_cr within one metal (CS-07, twice; type and thickness confounded);
- bonding starts in a ring (exposed).

The negative results are in its §2 and in multi-particle-tried.md.

Solver facts that hold (solver-facts.md):
- verified elastic bulk TLSPH (T-S1, T-B2, BCT off, energy to 0.25 %);
- integral quantities converge, e.g. a(t);
- cs12 with sticking bonds is built, and its energy closes (§37–§39).

## Not answerable with local means, and why

| Question | Why not | Source |
|---|---|---|
| A resolved interface state (local p_n, Y, edge strain) driving a bond law | Point values at the contact edge do not converge on any host. They may be singular in the exact solution (crack-tip-like field). The 2D reference host collapses at the jet root at 0.034 t_p | §25, §27, problem-formalism §2(c), length-scale note §13 |
| A converged rebound difference from an in-solver bond | CS-22b passed only under the free-slip law; with sticking bonds CS-23 is refuted at every δ_c | §31, §39, DECISIONS 2026-11-23 |
| A physical length as the cure for edge non-convergence | No zero-code host; the band check found no band narrowing with the mesh | §40, §41, DECISIONS 2026-11-24 |
| More blind v_cr tests (R1) | Blind list 1 is used up; the stop rule gives no blind list 2 | DECISIONS 2026-11-23, synthesis §4b |
| The whole in-solver chain | An independent odds review put it at about 0.3 % | odds-review-2026-11-16/summary.md |

Common thread: what the local solver can deliver is **whole-body or area-integrated quantities**. What the data can
judge is **v_cr windows and a few stacks**.

## Still open

- **R2, particle-level build-up rule** (coldspray-buildup-track.md): a data audit and an exploratory, post hoc Q-B1
  answer on the Reiser 2024 stacks exist (2026-11-07). There is no hunch, and a hunch needs unseen stacks.
- **R3, kinematic Bay estimate** (coldspray-kinematics.md): the geometry code and its tests exist (2026-11-07). There
  is no hunch, and the ring data are exposed (any comparison is post hoc).
- **Track B, paused** (DECISIONS 2026-11-23). Two design questions belong to it, not to the track's direction:
  - friction for unbonded contact;
  - the hot-edge choice (σ_B ∝ σ_y(T); problem-formalism §2(f)).
- **External measurements:** the campaign proposal has been parked as a last resort since 2026-11-03
  (coldspray-campaign-proposal.md). The T3 request was dropped on 2026-11-17.
- **Hunch budget:** 3 of 5 (CS-10, CS-17, CS-20).

## Housekeeping (modeller's defaults; they leave the open list unless Peter objects)

- **CS-20:** park it. There is no unseen ring-map source.
- **Mohanty 2022 alone:** a footnote to R1. It is post hoc, and one series cannot move R1.
- **WSL A's band-check arrays** (`~/oc_runs/hvi_band`, 5.5 GB): may be deleted; WSL A deletes them when Peter
  confirms.
- **Friction and the hot-edge choice:** filed under Track B (above).

## The one question for Peter

1. **Pause the cold-spray track** with this note as its closing state, and resume schemeforge Phase 6 at step 6
   (about one session to Gate 6). The track stays resumable from here.
2. **Continue cold spray at the reduced level:** R2 or R3, finite quantities only, under the hunch budget.
3. **A review session whose allowed answers include "stop".** Fresh reviewers get this note only, not the history,
   and are asked: "Is there a question in this domain that the local means can answer, and how would it be judged?"
   - The 2026-11-18 brainstorm asked for ideas, so it had to produce some.
   - This review succeeds by producing a decision, not a new path.

**Modeller's recommendation:** 1, with 3 kept as the way back into cold spray. If Peter is unsure whether a local
path is left at all, 3 first.
