"""LLM backends for single-shot mutations (PLAN §5.9): `claude-cli` (default) and `dummy` (tests).

Every call is logged in the registry table llm_calls (backend, model, prompt hash, latency, cost, tokens).
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol

import numpy as np

from .prompts import OUTPUT_SCHEMA, SYSTEM


@dataclass
class Completion:
    data: dict[str, Any] | None  # {"code", "rationale", "expected_change"} or None on failure
    cost_usd: float | None
    latency_s: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    error: str | None = None


class Backend(Protocol):
    name: str
    model: str

    def complete(self, prompt: str) -> Completion: ...


class ClaudeCLI:
    """`claude -p` headless mode in an empty temporary directory, with structured JSON output."""

    name = "claude-cli"

    def __init__(self, model: str = "sonnet", timeout: float = 300.0, executable: str = "claude") -> None:
        self.model, self.timeout, self.executable = model, timeout, executable

    def command(self) -> list[str]:
        return [self.executable, "-p", "Follow the task on stdin.", "--system-prompt", SYSTEM,
                "--output-format", "json", "--json-schema", json.dumps(OUTPUT_SCHEMA), "--model", self.model]

    def complete(self, prompt: str) -> Completion:
        t0 = time.perf_counter()
        with tempfile.TemporaryDirectory(prefix="sforge-llm-") as cwd:
            try:
                proc = subprocess.run(self.command(), input=prompt, text=True, capture_output=True, cwd=cwd,
                                      timeout=self.timeout, check=False)
            except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
                return Completion(None, None, time.perf_counter() - t0, error=f"{type(exc).__name__}: {exc}")
        latency = time.perf_counter() - t0
        try:
            out = json.loads(proc.stdout)
        except json.JSONDecodeError:
            tail = (proc.stderr or proc.stdout).strip()[-300:]
            return Completion(None, None, latency, error=f"exit {proc.returncode}: {tail}")
        usage = out.get("usage") or {}
        data = out.get("structured_output")
        if data is None and isinstance(out.get("result"), str):  # fallback: JSON in the text result
            try:
                data = json.loads(out["result"])
            except json.JSONDecodeError:
                data = None
        ok = isinstance(data, dict) and isinstance(data.get("code"), str)
        return Completion(data if ok else None, out.get("total_cost_usd"), latency, usage.get("input_tokens"),
                          usage.get("output_tokens"), None if ok else f"no structured output: {str(out)[:300]}")


class Dummy:
    """Deterministic limiter mutations for tests: a C-infinity family phi = r (r + b) / (r^2 + c r + d) clipped to
    r >= 0, with parameters drawn from a seeded generator."""

    name = "dummy"

    def __init__(self, model: str = "dummy", seed: int = 0) -> None:
        self.model = model
        self.rng = np.random.default_rng(seed)

    def complete(self, prompt: str) -> Completion:
        b, c, d = (float(v) for v in np.round(self.rng.uniform([0.5, 0.0, 0.5], [2.0, 1.0, 2.0]), 4))
        code = ('"""Dummy-backend limiter."""\nimport jax.numpy as jnp\n\n\n'
                f"def phi(r):\n    rp = jnp.maximum(r, 0.0)\n"
                f"    return rp * (rp + {b}) / (rp * rp + {c} * rp + {d})\n")
        return Completion({"code": code, "rationale": f"rational limiter b={b} c={c} d={d}",
                           "expected_change": "none (dummy)"}, 0.0, 0.0, 0, 0)


def make_backend(name: str, model: str, seed: int = 0) -> Backend:
    if name == "claude-cli":
        return ClaudeCLI(model)
    if name == "dummy":
        return Dummy(model, seed)
    raise ValueError(f"unknown backend {name!r}")


def log_call(conn, backend: Backend, prompt: str, c: Completion, candidate_id: str | None) -> None:
    conn.execute(
        "INSERT INTO llm_calls (backend, model, prompt_hash, latency_s, cost_usd, input_tokens, output_tokens, "
        "candidate_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (backend.name, backend.model, hashlib.sha256(prompt.encode()).hexdigest()[:16], c.latency_s, c.cost_usd,
         c.input_tokens, c.output_tokens, candidate_id, datetime.now(UTC).isoformat(timespec="seconds")))
    conn.commit()
