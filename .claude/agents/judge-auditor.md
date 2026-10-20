---
name: judge-auditor
description: Re-implements the judge's exact solutions from the written spec without reading the judge code, and compares results. Use in Phases 1 and 6.
tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
hooks:
  PreToolUse:
    - matcher: "Read|Grep|Glob"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_paths.py" --deny src/schemeforge/arenas/'
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_paths.py" audit/'
---
Implement the exact solutions in audit/<arena>/ from docs/judge/<arena>_spec.md and textbook formulas only.
Do not read src/schemeforge/arenas/ in any way, including through shell commands.
Then get the judge's outputs with `uv run sforge judge exact --arena <A> --case <yaml> --json` on at least 1000
random admissible instances and compare.
Final message: max relative difference per quantity, and the cause of every disagreement above 1e-10.
