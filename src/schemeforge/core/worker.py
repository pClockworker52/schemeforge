"""Sandboxed evaluation worker (PLAN §5.6): `python -m schemeforge.core.worker` with a JSON job on stdin.

The process pins itself to one CPU and sets CPU-time and memory limits before importing JAX, loads the candidate
through the AST-validating loader and prints one line `SFORGE_REPORT <json>` with the arena's report.
Job: {arena, slot, suite, candidate (path), extra_cases (list of case dicts), core, cpu_seconds, memory_bytes}.
"""

from __future__ import annotations

import json
import os
import resource
import sys

MARKER = "SFORGE_REPORT "


def _limit(job: dict) -> None:
    os.sched_setaffinity(0, {int(job["core"])})
    cpu = int(job["cpu_seconds"])
    resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu + 5))
    mem = int(job.get("memory_bytes") or 0)
    if mem:
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
    os.environ.setdefault("XLA_FLAGS", "--xla_cpu_multi_thread_eigen=false")
    os.environ["OMP_NUM_THREADS"] = "1"


def main() -> int:
    job = json.loads(sys.stdin.read())
    _limit(job)
    import importlib
    from pathlib import Path

    from schemeforge.core.loader import CandidateRejected, load_function

    arena = importlib.import_module(f"schemeforge.arenas.{job['arena']}.evaluate")
    cases_mod = importlib.import_module(f"schemeforge.arenas.{job['arena']}.cases")
    zoo = importlib.import_module(f"schemeforge.arenas.{job['arena']}.zoo")
    try:
        fn = load_function(Path(job["candidate"]), zoo.SLOT_FUNCTIONS[job["slot"]])
    except CandidateRejected as exc:
        report = {"status": "rejected", "violations": exc.violations, "cases": {}, "metamorphic": {}}
    except Exception as exc:  # noqa: BLE001 - e.g. an exception raised while executing the module body
        report = {"status": "rejected", "violations": [f"loading failed: {type(exc).__name__}: {exc}"],
                  "cases": {}, "metamorphic": {}}
    else:
        extra = []
        for d in job.get("extra_cases", []):
            case = cases_mod.case_from_dict(d)
            cases_mod.validate_case(case)
            extra.append(case)
        report = arena.evaluate(fn, job["slot"], job["suite"], extra)
        if job.get("probe") and report.get("status") == "ok":
            from schemeforge.engine.probes import probe  # search policy: descriptors and fingerprint

            try:
                report["probe"] = probe(fn, job["arena"], job["slot"])
            except Exception as exc:  # noqa: BLE001 - a probe failure must not hide the evaluation
                report["probe"] = {"error": f"{type(exc).__name__}: {exc}"}
    print(MARKER + json.dumps(report, default=float), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
