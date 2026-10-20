#!/bin/bash
# Calibration C1 (PLAN §10 task 3): limiter slot, islands seeded with phi = 0 and phi = 1, real LLM backend.
#   bash scripts/headless/c1.sh [gens] [children] [budget]
set -euo pipefail
cd "$(dirname "$0")/../.."
export PATH="$HOME/.local/bin:$PATH"   # uv and claude
uv run python scripts/e2e_evolve.py start runs/c1 --backend claude-cli --model sonnet --wild-model haiku \
    --islands 3 --gens "${1:-4}" --children "${2:-8}" --budget "${3:-96}" \
    --seed src/schemeforge/engine/seeds/limiter/first_order.py \
    --seed src/schemeforge/engine/seeds/limiter/unlimited.py
