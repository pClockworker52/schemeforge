#!/bin/bash
# Run a headless Claude Code orchestrator session inside WSL (hooks and the sforge MCP server work here).
#   bash scripts/headless/run.sh <prompt-file> <log-name> [model]
set -euo pipefail
cd "$(dirname "$0")/../.."
export PATH="$HOME/.local/bin:$PATH"
prompt_file="$1"; log="runs/headless/$2"; model="${3:-opus}"
mkdir -p runs/headless
claude -p "$(cat "$prompt_file")" --model "$model" --permission-mode acceptEdits \
       --output-format json > "$log.json" 2> "$log.err"
python3 - "$log.json" <<'PY'
import json, sys
out = json.load(open(sys.argv[1]))
res = [m for m in (out if isinstance(out, list) else [out]) if m.get("type") == "result"][-1]
print("result:", res.get("subtype"), "| turns:", res.get("num_turns"), "| cost:", res.get("total_cost_usd"))
print(str(res.get("result"))[-3000:])
PY
