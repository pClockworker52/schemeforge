#!/bin/bash
# Calibration C2 (PLAN §10 task 4): flux slot seeded with Rusanov, real LLM backend.
#   bash scripts/headless/c2.sh [gens] [children] [budget]
set -euo pipefail
cd "$(dirname "$0")/../.."
export PATH="$HOME/.local/bin:$PATH"   # uv and claude
uv run python scripts/e2e_evolve.py start runs/c2 --slot flux --backend claude-cli --model sonnet \
    --wild-model haiku --islands 2 --gens "${1:-3}" --children "${2:-8}" --budget "${3:-48}" \
    --seed src/schemeforge/arenas/euler1d/zoo/flux/rusanov.py
