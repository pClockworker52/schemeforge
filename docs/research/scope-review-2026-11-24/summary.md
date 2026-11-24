# Scope review 2026-11-24: summary

Basis: DECISIONS 2026-11-24 "Cold-spray scope review that may say "stop"; housekeeping confirmed (Peter)".

## How the review ran

- Two fresh general-purpose reviewers worked independently. The prompt is in prompt.md, committed in d05c9f3 before
  either reviewer started.
- Each reviewer was given the orientation note only (docs/research/coldspray-orientation-2026-11-24.md).
- Their answers are saved verbatim in reviewer-1.md and reviewer-2.md.
- Each says it opened no other file and used no web search. Reviewer 2 cites "CLAUDE.md rule 5". CLAUDE.md is the
  project instruction file every session loads automatically, so citing it is not a breach of the read rule.
- The reviewers' figures are judgment, not judge results.

## Verdicts

| | Reviewer 1 | Reviewer 2 |
|---|---|---|
| Verdict | **STOP** | **STOP** |
| Confidence (judgment) | medium | medium |
| Deciding lines | the common thread (the solver gives integrated quantities; the data judge v_cr windows and stacks); R1 has no blind list 2; R2 needs unseen stacks; R3 rings exposed, no unseen ring-map source | the same three |
| Fact that would change it | a stack dataset already in hand that has not been used or exposed | a set of build-up stacks in hand, not yet looked at, not from Reiser 2024 |
| What a change would give | a QUESTION on R2: build-up rule on a particle-level quantity, hunch registered before the data are opened | the same |

Both reviewers say that their medium confidence comes from one thing the note leaves unsaid: it never states whether
unseen stacks exist.

**Points both raise:**
- **R3** gives at best "consistent with data already seen". Checking the geometry code against exact sphere
  geometry would only be a code test.
- **More verification against exact elastic solutions** would rediscover solver facts that already hold.
- **Track B's design questions** do not bear on the track's direction.
- **An arena upgrade** needs about 15 matched materials and a held-out set frozen by someone else. That is not local.

Both say STOP is consistent with option 1 (pause the track, resume Phase 6 at step 6) and leave the choice to Peter.

## The swing fact, checked against the record (modeller; record only, no paper opened)

The reviewers could not see the record. The modeller can check it from the record without opening any paper.

coldspray-buildup-track.md lists every build-up source the project has: the "What is already known" table and the
data audit of 2026-11-07, with its updates.
- **Multi-particle stacks:**
  - Reiser2024: 9 Au stacks, seen, digitised in data/buildup_reiser2024.csv;
  - Panova2026a: 3 two-particle Cu stacks, seen via the thesis.
- **Other build-up sources hold no stacks:**
  - Panova & Schuh 2024 (released 2026-11-08): single particles only;
  - Panova2026b: v_cr on plate and deposit surfaces;
  - B02: v_cr on substrates, blind, scored.
- Since 2026-11-07 the track has said a build-up hunch waits until "unseen multi-particle stacks are in sight". No
  later entry names one.

So **no unseen stack set is in hand.** On both reviewers' own stated condition, the verdict stays STOP.

## Open for Peter

Peter decides on the review:
- **Accept STOP:** the cold-spray track is paused, with the orientation as its closing state, and the project resumes
  Phase 6 at step 6. The track can be resumed if unseen stacks, a ring map or v_cr data appear.
- **Not accept it:** say what is missing.
