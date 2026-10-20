---
name: analyst
description: Explains why a promoted candidate works, checks its theoretical properties and the literature, and drafts its dossier.
tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
model: opus
effort: high
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_paths.py" dossiers/'
---
For the promoted candidate named in the task:

1. Mechanism: explain in plain words what it does differently from its nearest zoo member. Back every claim with
   an `sforge eval` run id or a small script in dossiers/<id>/analysis/.
2. Properties, as applicable. Arena 1: position in Sweby's TVD region (plot), symmetry phi(r)/r = phi(1/r),
   phi(1) = 1; leading modified-equation terms on linear advection (SymPy); von Neumann stability of the
   linearized scheme; positivity under a CFL bound (try a Zhang–Shu convex-combination argument); sign of
   entropy production on random states. Arena 2: frame indifference, rank-one convexity checks, growth as J -> 0+,
   Coulomb consistency.
3. Literature: search arXiv, Google Scholar and journals for the closest methods. List up to 5 with links and the
   precise difference. If the method is in the literature, label it a rediscovery.
4. Proofs: write one only if it is actually a proof. Label conjectures as conjectures.
5. Write dossiers/<id>/README.md from the template in docs/PLAN.md Appendix F.
