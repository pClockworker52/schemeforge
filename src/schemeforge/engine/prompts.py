"""Engine prompt templates (PLAN Appendix E)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from schemeforge.core.integrity import REPO_ROOT

SYSTEM = (
    "You improve one component of a numerical scheme. You see a contract, a hunch, parent code and evaluation "
    "reports. Return JSON only, matching the schema. The code must satisfy the contract exactly: pure jax.numpy / "
    "jax.lax / math, no I/O, no hidden state, no Python loops over cells, deterministic. Do not special-case "
    "particular test inputs: held-out cases are drawn from families you have not seen. Also rejected by the "
    "validator: decorators, classes, global/nonlocal, attribute assignment, non-constant default arguments, "
    "print, `import jax` or `import jax.numpy` without an alias, file helpers such as jnp.load, and str.format."
)

OPERATORS: dict[str, str] = {
    "refine": "Improve the parent's two worst metrics (marked) without regressing any other metric by more than 5 %. "
              "Change one idea.",
    "crossover": "Combine parent A's mechanism with the strength of parent B described in its report. Explain the "
                 "combination.",
    "explore": "Implement the hunch in a way that differs from every archive member listed.",
    "simplify": "Keep the behavior (scores within 1 %) with fewer lines and branches.",
    "wild": "Try an unusual variation that still satisfies the contract.",
}
OPERATOR_WEIGHTS = {"refine": 0.45, "crossover": 0.20, "explore": 0.15, "simplify": 0.10, "wild": 0.10}

OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["code", "rationale", "expected_change"],
    "properties": {"code": {"type": "string"}, "rationale": {"type": "string"},
                   "expected_change": {"type": "string"}},
    "additionalProperties": False,
}


def contract_text(arena: str, slot: str) -> str:
    """The slot's section of docs/judge/<arena>_slots.md (plus the shared preamble)."""
    doc = (Path(REPO_ROOT) / "docs" / "judge" / f"{arena}_slots.md").read_text(encoding="utf-8")
    preamble = doc.split("\n## ", 1)[0]
    m = re.search(rf"\n## `{re.escape(slot)}`.*?(?=\n## |\Z)", doc, flags=re.S)
    return preamble.strip() + "\n\n" + (m.group(0).strip() if m else f"(no contract found for slot {slot})")


def report_summary(values: dict[str, float], vs_zoo: dict[str, float], keys: list[str]) -> str:
    """One line per objective; the two worst (largest vs-zoo ratio) are marked."""
    worst = sorted((k for k in keys if k in vs_zoo), key=lambda k: -vs_zoo[k])[:2]
    lines = []
    for k in keys:
        v = values.get(k)
        r = vs_zoo.get(k)
        mark = "  <-- worst" if k in worst else ""
        lines.append(f"- {k}: {'n/a' if v is None else f'{v:.4g}'}"
                     f" ({'n/a' if r is None else f'{r:.3g}'} x best zoo){mark}")
    return "\n".join(lines)


def user_prompt(arena: str, slot: str, hunch: dict[str, Any], parents: list[dict[str, Any]],
                archive_context: list[str], operator: str) -> str:
    parts = [f"## Contract ({arena}/{slot})\n{contract_text(arena, slot)}",
             f"## Hunch {hunch['id']}\n{' '.join(str(hunch['statement']).split())}\n"
             f"Mechanism: {' '.join(str(hunch['mechanism']).split())}\n"
             f"Predicted effect: {hunch['predicted_effect']}"]
    for i, p in enumerate(parents):
        label = "Parent" if len(parents) == 1 else f"Parent {'AB'[i]}"
        parts.append(f"## {label} ({p['id']})\n```python\n{p['code']}\n```\nDev report (lower ratio is better):\n"
                     f"{p['summary']}")
    if archive_context:
        parts.append("## Archive context\n" + "\n".join(f"- {a}" for a in archive_context))
    parts.append(f"## Task: {operator}\n{OPERATORS[operator]}\n\n"
                 'Return {"code": "<full file>", "rationale": "<at most 3 sentences>", '
                 '"expected_change": "<metric: direction, size>"}')
    return "\n\n".join(parts)
