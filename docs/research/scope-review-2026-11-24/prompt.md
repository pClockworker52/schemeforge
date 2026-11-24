# Scope review 2026-11-24: prompt given to both reviewers (verbatim)

Basis: DECISIONS 2026-11-24 "Cold-spray scope review that may say "stop"; housekeeping confirmed (Peter)". This file
was committed before either reviewer started.

---

You are an independent reviewer of a computational-mechanics research side track. The topic is cold-spray particle
impact: when a sprayed metal particle bonds to a substrate. You have no stake in the track's earlier choices. The
project owner wants a decision from you. They do not want encouragement, and they do not want new ideas for their
own sake. "Stop" is a complete, acceptable answer.

Repository: /home/user/schemeforge. It is read-only for you: do not edit, commit, run solvers or run scripts.

**Read exactly one file:** docs/research/coldspray-orientation-2026-11-24.md.
- Do not open any other file in the repository. That includes the files the note cites, docs/STATUS.md,
  docs/HANDOFF.md, docs/DECISIONS.md and anything under docs/research/scope-review-2026-11-24/ other than this prompt.
- Do not use web search.
- If you open anything else by accident, say so in your answer.
- If the note is not enough to decide, that is an answer in itself (CANNOT DECIDE below). Do not go looking for more.

"Local means" is used as the note uses it: the project's own solver and workstation, and the data and code already
in hand. It excludes new measurements and the external campaign, which the note lists as parked.

**The question:** "Is there a question in this domain that the local means can answer, and how would it be judged?"

Give exactly one verdict:
- **STOP:** on the note's evidence, no such question exists. Quote or cite the two or three lines of the note that
  decide it.
- **QUESTION:** name one question, or at most two. For each, give:
  - the finite quantity it rests on, such as a whole-body or area-integrated quantity (the note says why point values
    at the contact edge are not usable);
  - the data or exact reference that would judge it, and whether they are unseen or already exposed (a verdict on
    exposed data only is post hoc and must be labelled so);
  - a judging rule that can be fixed before any run and that can fail;
  - what a pass would let the project claim, and why that claim is worth its cost.

  A question the note already lists as not answerable, or as open with a known obstacle, counts only if you say
  exactly what removes that obstacle.
- **CANNOT DECIDE:** the note is not enough. Name exactly what is missing and which verdict each missing item would
  decide.

Then add:
- your confidence in the verdict (judgment: low, medium or high);
- the one fact that would change your verdict most.

Rules:
- Cite the note's sections for every claim.
- Do not invent numbers.
- Label judgment as judgment.
- Never call anything "novel".

Be concise (300–800 words). Your final message is saved verbatim as your review, so write it as a finished Markdown
document.
