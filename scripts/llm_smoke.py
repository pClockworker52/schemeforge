"""One real LLM call through the claude-cli backend with a real engine prompt (flag and output-format check).

    uv run python scripts/llm_smoke.py [model]
"""

from __future__ import annotations

import sys
from pathlib import Path

from schemeforge.arenas.euler1d import zoo
from schemeforge.core.sandbox import validate_source
from schemeforge.engine import backends, prompts


def main() -> int:
    model = sys.argv[1] if len(sys.argv) > 1 else "sonnet"
    hunch = {"id": "H-SMOKE", "statement": "A smooth limiter between van Albada and superbee.",
             "mechanism": "No kinks keeps the Newton Jacobian continuous; more compression sharpens shocks.",
             "predicted_effect": [{"metric": "R1.shock_width", "direction": "down", "size": "0.3 cells"}]}
    parent = {"id": "zoo-van_albada", "code": Path(zoo.members("limiter")["van_albada"]).read_text(),
              "summary": "- R1.shock_width: 3.67 (1.37 x best zoo)  <-- worst\n- R1.contact_width: 7.36 (2.37 x)"}
    prompt = prompts.user_prompt("euler1d", "limiter", hunch, [parent], [], "refine")
    c = backends.ClaudeCLI(model).complete(prompt)
    print(f"latency {c.latency_s:.1f} s, cost {c.cost_usd}, tokens in/out {c.input_tokens}/{c.output_tokens}")
    if c.data is None:
        print("ERROR:", c.error)
        return 1
    print("rationale:", c.data["rationale"])
    print("expected:", c.data["expected_change"])
    print("sandbox:", "ok" if validate_source(c.data["code"]).ok else validate_source(c.data["code"]).violations)
    print(c.data["code"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
