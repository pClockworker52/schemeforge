# Agent runs from WSL

The plan's subagents (hunch-generator, proposer, breaker, cheater) need hooks that call `python3` and the `sforge`
MCP server. Both work only in a Claude Code session started inside WSL; the Windows desktop app blocked them in
rounds 1 and 2 (docs/STATUS.md). Run everything below from `/mnt/c/Users/peter/schemeforge` in WSL.

## Before the first agent run

1. `git status` is clean and the judge you want is checked out (`uv run sforge judge version --arena euler1d`
   prints "integrity: ok"). No `sforge evolve` or other evaluation is running.
2. `uv run pytest -q` passes.
3. The MCP server starts: `timeout 20 uv run sforge-mcp < /dev/null; echo $?` exits without a traceback.
4. In an interactive `claude` session in the repo, `/mcp` lists `sforge` as connected and `/agents` lists the
   seven project agents. If `sforge` is not connected, the agents have no tools: stop and fix that first.
5. Optional: start the session with `claude remote-control` so it can be followed from the Claude app.

## Runs (PLAN §11.5)

| Step | Command | Output |
|---|---|---|
| 3b(i), 3d | `bash scripts/headless/run.sh scripts/headless/redteam_v13.txt redteam-v13` | candidates/redteam/v13/REPORT.md |
| 3b(ii) | `bash scripts/headless/run.sh scripts/headless/breaker_ratchet.txt breaker-round2` | candidates/breaker-round2/, cases/quarantine/ |
| 3c | see `scripts/feasibility_a1a7.py --help` | runs/feasibility-a1a7/ |
| 3d round | `bash scripts/headless/run.sh scripts/headless/round3.txt round3`, or paste round3.txt into an interactive WSL session | docs/rounds/…-reconstruction_stateful.md |
| round 4 | `bash scripts/headless/run.sh scripts/headless/round4.txt round4`, or paste round4.txt | docs/rounds/…-reconstruction_stateful-r4.md |

`run.sh` logs to runs/headless/<name>.json and prints turns and cost. One agent run at a time, never next to
`evolve`: parallel evaluations caused false timeouts on 2026-10-21 (memory; K is now capped at one worker per 2 GB).

Round 3's swarm criterion is fixed in docs/targets/swarm.md; read it before the round starts.
