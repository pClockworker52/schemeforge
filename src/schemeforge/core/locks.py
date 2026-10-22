"""CPU fairness (PLAN §5.6): at most K evaluations at a time, each pinned to its own logical CPU.

K defaults to physical cores - 1 (logical CPUs / 2 - 1 on SMT machines), capped by memory: one worker per
WORKER_MEMORY_BYTES of MemTotal (a `limiter_stateful` dev worker peaks at ~1.45 GB; 15 of them on 15.6 GB thrashed
into 600 s timeouts in round 2). SFORGE_MAX_PARALLEL overrides it. CPU 0 is left free for the orchestrator.
"""

from __future__ import annotations

import fcntl
import os
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

LOCK_DIR = Path("runs") / ".locks"
WORKER_MEMORY_BYTES = 2 * 1024**3


def mem_total_bytes(meminfo: Path = Path("/proc/meminfo")) -> int | None:
    """MemTotal in bytes, or None if unknown."""
    try:
        for line in meminfo.read_text().splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) * 1024
    except OSError:
        return None
    return None


def max_parallel() -> int:
    env = os.environ.get("SFORGE_MAX_PARALLEL")
    if env:
        return max(1, int(env))
    k = len(os.sched_getaffinity(0)) // 2 - 1
    mem = mem_total_bytes()
    if mem is not None:
        k = min(k, mem // WORKER_MEMORY_BYTES)
    return max(1, k)


@contextmanager
def acquire_core(lock_dir: Path = LOCK_DIR, timeout: float = 3600.0, poll: float = 0.25) -> Iterator[int]:
    """Block until one of K core locks is free; yield the logical CPU to pin the evaluation to."""
    lock_dir.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout
    k = max_parallel()
    while True:
        for core in range(1, k + 1):
            fh = open(lock_dir / f"core-{core}.lock", "w")  # noqa: SIM115 - held for the duration of the job
            try:
                fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                fh.close()
                continue
            try:
                yield core
            finally:
                fcntl.flock(fh, fcntl.LOCK_UN)
                fh.close()
            return
        if time.monotonic() > deadline:
            raise TimeoutError("no free evaluation slot")
        time.sleep(poll)
