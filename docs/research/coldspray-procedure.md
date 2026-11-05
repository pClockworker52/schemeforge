# Cold spray: working procedure (adopted 2026-11-05)

How the sessions of the cold-spray track record work. DECISIONS 2026-11-05 "Cold-spray procedure: less
bookkeeping, one standing rigor rule". The research rules themselves (blind rules B1–B6, pre-registration, the
verification ladder, CLAUDE.md iron rules) are unchanged.

## Where things are written

| What | Where | Who | When |
|---|---|---|---|
| Hunch, its protocol, and its approval | `docs/research/coldspray-hunch-<id>.md`; approval is one line in the file ("frozen <date>, approved by Peter"), committed as the freeze commit | modeller (cloud) | at approval; the freeze commit comes before any run |
| Results of runs | the session's own section of its verification doc (e.g. opencourant-verification.md §n) | the running session | as it goes |
| Changes of direction (route, plan, rules) | `docs/DECISIONS.md`, with the index regenerated | modeller | when Peter decides one |
| Session log | `docs/STATUS.md`: **one short line per session**, with commit ids and pointers, no copied content | modeller (cloud), also when merging another session's branch | at session end or at merge |
| Hand-over state | `docs/HANDOFF.md` | modeller | at session end only |
| Next task for another session | `docs/research/tasks/<session>.md` | modeller | when the task is decided |

Not recorded in DECISIONS any more: routine approvals of hunches or rungs. The freeze commit is the proof.

## Sessions and branches

- **Other sessions write only their own section and their own files.** That covers WSL A (simulations) and WSL B
  (extraction). They do not edit STATUS, HANDOFF, DECISIONS, the hunch files or the tasks file. The modeller
  records their result in STATUS when merging. This removes the merge conflict in STATUS.
- **Tasks go through the repository.** The modeller writes the next task into `docs/research/tasks/wsl-a.md` (or
  `wsl-b.md`). Peter tells the session to pull and do the next task. The session marks the task done in its own
  result section, not in the task file. Copy-and-paste prompts are used only for one-off sessions; their prompt is
  committed as a file, as with the literature search.

## Standing rigor rule (new)

**A detection or decision metric gets its own rung before it decides a verdict,** just as the solver does. A metric
such as "jetting onset", "bonded area" or "edge convergence" must first be shown, on a case where the answer is
known (or on an agreed reference case), to detect what it is meant to detect. Origin: CS-11's jet metric J was
frozen without such a rung, and its non-crossing in setup F could not be interpreted (opencourant-verification.md
§10.5).

## Unchanged and still required

- **Freeze commit before any run or reading** of the data a hunch is tested on.
- **Verification rungs stop the work when they fail** (W0 and H0 did; both stops were right).
- **Runs outside a protocol are labelled** as diagnostics and carry no verdict.
- **Negative and inconclusive results are recorded** in the result section and in the hunch index.
