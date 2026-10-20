"""Promotion test (PLAN §5.8, docs/targets/): thresholds on held-out aggregates plus paired bootstraps of
log(candidate / zoo reference) over the same held-out instances.

Per-instance values come from ~/.schemeforge/heldout_runs/<run>.json (written by the evaluator). This module
reads them as part of the judge; it only ever prints verdicts, medians and confidence intervals, never
instance data.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from .evaluation import HELDOUT_DIR

N_BOOT = 10_000


@dataclass(frozen=True)
class Check:
    id: str
    description: str
    ok: bool
    detail: str


# Target A (docs/targets/A.md). Bootstrap references: sharpness against the convergent zoo member (van Albada),
# smoothness against the sharp one (MC).
TARGET_A: dict[str, Any] = {
    "thresholds": [
        ("A1", "RF1", "shock_width", "median", "<=", 2.6),
        ("A2", "RF1", "contact_width", "median", "<=", 6.5),
        ("A3", "NF1", "converged_expl", "mean", ">=", 0.95),
        ("A4", "NF1", "converged_impl", "mean", ">=", 1.0),
        ("A5", "NF3", "roughness_J", "p90", "<=", 0.002),
    ],
    "relative": [  # (id, family, metric, stat, factor x reference member's value)
        ("A7a", "RF1", "overshoot", "p90", 1.1, "van_leer"),
        ("A7b", "RF2", "overshoot", "p90", 1.1, "van_leer"),
    ],
    "bootstrap": [  # (id, family, metric, reference zoo member): 95 % CI of log(cand/ref) entirely below 0
        ("B1", "RF1", "shock_width", "van_albada"),
        ("B2", "RF1", "contact_width", "van_albada"),
        ("B5", "NF3", "roughness_J", "mc"),
    ],
    "dev": [("A6", "S1", "order_smooth", ">=", 1.9)],
}
TARGETS = {"A": TARGET_A}


def load_instances(run_id: str, heldout_dir: Path = HELDOUT_DIR) -> dict[str, dict[str, Any]]:
    return json.loads((heldout_dir / f"{run_id}.json").read_text(encoding="utf-8"))


def aggregate_stat(instances: dict[str, dict], family: str, metric: str, stat: str) -> float:
    vals = np.array([d["metrics"][metric] for d in instances.values()
                     if d["family"] == family and metric in d["metrics"]], dtype=float)
    vals = vals[np.isfinite(vals)]
    if vals.size == 0:
        return math.nan
    if stat == "median":
        return float(np.median(vals))
    if stat == "mean":
        return float(np.mean(vals))
    if stat == "p90":
        return float(np.percentile(vals, 90))
    raise ValueError(stat)


def paired_bootstrap(cand: np.ndarray, ref: np.ndarray, n: int = N_BOOT, seed: int = 0) -> tuple[float, float, float]:
    """Mean of log(cand/ref) over paired instances and its 95 % percentile bootstrap interval."""
    d = np.log(cand) - np.log(ref)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, d.size, size=(n, d.size))
    means = d[idx].mean(axis=1)
    return float(d.mean()), float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def _paired(cand: dict, ref: dict, family: str, metric: str) -> tuple[np.ndarray, np.ndarray]:
    ids = sorted(i for i, d in cand.items() if d["family"] == family and metric in d["metrics"]
                 and i in ref and metric in ref[i]["metrics"])
    c = np.array([cand[i]["metrics"][metric] for i in ids], dtype=float)
    r = np.array([ref[i]["metrics"][metric] for i in ids], dtype=float)
    ok = np.isfinite(c) & np.isfinite(r) & (c > 0) & (r > 0)
    return c[ok], r[ok]


def check_target(target: str, cand_run: str, zoo_runs: dict[str, str], dev_values: dict[str, float],
                 heldout_dir: Path = HELDOUT_DIR) -> list[Check]:
    spec = TARGETS[target]
    cand = load_instances(cand_run, heldout_dir)
    out: list[Check] = []
    ops = {"<=": lambda a, b: a <= b, ">=": lambda a, b: a >= b}
    for tid, fam, metric, stat, op, thr in spec["thresholds"]:
        v = aggregate_stat(cand, fam, metric, stat)
        out.append(Check(tid, f"{fam} {metric} {stat} {op} {thr}", bool(ops[op](v, thr)), f"{v:.4g}"))
    for tid, fam, metric, stat, factor, member in spec["relative"]:
        ref = aggregate_stat(load_instances(zoo_runs[member], heldout_dir), fam, metric, stat)
        v = aggregate_stat(cand, fam, metric, stat)
        out.append(Check(tid, f"{fam} {metric} {stat} <= {factor} x {member}", bool(v <= factor * ref),
                         f"{v:.4g} vs {factor * ref:.4g}"))
    for tid, fam, metric, member in spec["bootstrap"]:
        c, r = _paired(cand, load_instances(zoo_runs[member], heldout_dir), fam, metric)
        if c.size < 3:
            out.append(Check(tid, f"bootstrap {fam} {metric} vs {member}", False, f"only {c.size} paired instances"))
            continue
        m, lo, hi = paired_bootstrap(c, r)
        out.append(Check(tid, f"bootstrap {fam} {metric} vs {member}: 95 % CI of log ratio < 0", hi < 0.0,
                         f"mean {m:+.3f} [{lo:+.3f}, {hi:+.3f}] over n = {c.size} (ratio {math.exp(m):.3f})"))
    for tid, case, metric, op, thr in spec["dev"]:
        v = dev_values.get(f"{case}.{metric}", math.nan)
        out.append(Check(tid, f"dev {case} {metric} {op} {thr}", bool(ops[op](v, thr)), f"{v:.4g}"))
    return out
