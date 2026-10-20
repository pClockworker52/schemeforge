---
name: hunch-round
description: Run one schemeforge hunch round (PLAN Appendix D) — hunch drafts, registration, proposers, engine islands, breakers, round summary. Use when asked to run a hunch round for an arena and slot.
---

# Hunch round (draft until the first round confirms it)

Arguments (from the request; defaults in brackets): arena [euler1d], slot [limiter], n_hunches [4], lenses
[steady-convergence, approximation theory, contrarian], evals_per_proposer [8], islands [2], gens [4],
children [8], top_k_break [3], date (today).

Rules: the judge decides — every claim cites a run id. Never edit src/schemeforge/arenas/. Run inside WSL.

## 1. Hunches
- Use the **hunch-generator** subagent: "Write {n_hunches} hunch drafts for {arena}/{slot}, lenses {lenses}
  (spread the hunches over the lenses)." It writes YAML files into ledger/drafts/.
- Check each draft against ledger/schema.yaml, then register it: `uv run sforge hunch add ledger/drafts/<file>`.
  Note the ids (H-xxxx). Reject drafts that are known methods without a new mechanism (record why).

## 2. Proposals
- For every hunch, in parallel: the **proposer** subagent with "Implement hunch {id} for {arena}/{slot};
  at most {evals_per_proposer} evaluations. Workspace candidates/{id}/proposer/."
- Collect: best candidate path, dev run id, whether the predicted effect appeared.

## 3. Evolve
- From the proposer results and `uv run sforge leaderboard --arena {arena} --slot {slot} --vs-zoo`, pick the
  {islands} most promising hunches (best Pareto rank of their candidates; mechanism still plausible).
- Run `uv run sforge evolve --arena {arena} --slot {slot} --hunch H-a --hunch H-b --gens {gens}
  --children {children} --backend claude-cli --model sonnet --seed <best proposer file of each hunch>`
  (long: run it in the background and wait). Note the evolve run id.

## 4. Break
- `uv run sforge leaderboard --arena {arena} --slot {slot} --pareto --top {top_k_break} --json`: take the
  non-zoo ids.
- For each, the **breaker** subagent: "Break candidate {id} (file {path})." Cases land in cases/quarantine/.

## 5. Summary
- Write docs/rounds/{date}-{arena}-{slot}.md: hunches with suggested verdicts (supported / refuted /
  inconclusive, with run ids and the kill criteria), leaderboard delta against the zoo, quarantined cases,
  open questions for Peter. Do not close hunches yourself; propose verdicts — the main session or Peter closes
  them with `sforge hunch close`.
