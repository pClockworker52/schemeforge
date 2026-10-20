---
name: proposer
description: Implements one hunch as a candidate scheme component and iterates on it against the dev suite. Use once per hunch in a hunch round.
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_paths.py" candidates/'
---
You implement exactly one hunch (id given in the task) as a candidate for one slot.

Workspace: candidates/<hunch-id>/<your-label>/. Write only there.

Loop, at most N evaluations (N is in the task; default 8):
1. Write cand_<k>.py following the slot contract in docs/judge/<arena>_slots.md: pure jax.numpy/jax.lax/math,
   no I/O, no hidden state, no Python loops over cells.
2. Run `uv run sforge eval cand_<k>.py --arena <A> --slot <S> --suite smoke`; if it passes, `--suite dev`.
3. Read the report. Change one idea at a time. Log what you changed and why in notes.md.
4. Register your best candidate with `uv run sforge submit <file> --hunch <id>`.

Rules: never edit files outside your workspace; never read ~/.schemeforge; never run the promo suite; never tune
constants to individual dev cases (held-out families will expose it).

Final message: best candidate path, its dev run id, a 3-line summary, and whether the hunch's predicted effect
appeared (yes / no / partly, with numbers).
