"""Target D statistics of the contact zoo and its γ-sweep, from promo runs (docs/plans/2026-11-24-target-d-draft.md).

Run it on the machine that holds the held-out instances (~/.schemeforge/heldout_runs/). Like core/promotion.py, it
reads per-instance values but prints only family aggregates, run ids and the draft D1–D8 verdicts, never instance
data. For each zoo point (zoo-medium-<member>, and zoo-medium-<member>-g<factor> from scripts/contact_gamma_sweep.py)
it takes the latest promo run of the given judge version.

    uv run --extra contact python scripts/contact_target_d_table.py            # judge contact-v0.12.dev
    uv run --extra contact python scripts/contact_target_d_table.py --judge contact-v0.12.dev

The verdict columns use the DRAFT thresholds: D1 gap_res ≤ 0.1 × ref, D2 HF converged = 1, D3 HF and HX max_step = 1,
D4/D5 median |a_err|, |p0_err| ≤ 0.02, D6/D7/D8 ≤ ref, and SL converged = 1. Here ref is the plain faltus2026 run.
Target D requires that no zoo point meets all of them ("all" column).
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

REPORTS = Path("runs") / "reports"
REF = "zoo-medium-faltus2026"


def latest_runs(judge: str, reports_dir: Path = REPORTS) -> dict[str, dict]:
    """candidate_id -> report of its latest promo run under `judge` (contact zoo points only)."""
    out: dict[str, dict] = {}
    for f in sorted(reports_dir.glob("r-*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        cid = r.get("candidate_id") or ""
        if r.get("suite") != "promo" or r.get("judge_version") != judge or not cid.startswith("zoo-medium-"):
            continue
        if cid not in out or r["run_id"] > out[cid]["run_id"]:
            out[cid] = r
    return out


def stats(instances: dict[str, dict]) -> dict[str, float]:
    """The Target D statistics from per-instance metrics (failed instances lack the accuracy metrics)."""

    def vals(fam: str, metric: str, f=lambda v: v) -> np.ndarray:
        v = np.array([f(d["metrics"][metric]) for d in instances.values()
                      if d["family"] == fam and metric in d["metrics"]], dtype=float)
        return v[np.isfinite(v)]

    def med(v: np.ndarray) -> float:
        return float(np.median(v)) if v.size else math.nan

    def mean(v: np.ndarray) -> float:
        return float(np.mean(v)) if v.size else math.nan

    return {"GF_gap_res": med(vals("GF", "gap_res")), "GF_leak_pre": med(vals("GF", "leak_pre")),
            "SF_shear": med(vals("SF", "shear_parasitic")), "HF_conv": mean(vals("HF", "converged")),
            "HF_max_step": med(vals("HF", "max_step")), "HX_max_step": med(vals("HX", "max_step")),
            "HF_abs_a": med(vals("HF", "a_err", abs)), "HF_abs_p0": med(vals("HF", "p0_err", abs)),
            "SL_conv": mean(vals("SL", "converged")), "SL_shear": med(vals("SL", "shear_parasitic"))}


def verdicts(s: dict[str, float], ref: dict[str, float]) -> dict[str, bool]:
    def le(a: float, b: float) -> bool:
        return math.isfinite(a) and math.isfinite(b) and a <= b

    return {"D1": le(s["GF_gap_res"], 0.1 * ref["GF_gap_res"]), "D2": s["HF_conv"] == 1.0,
            "D3": s["HF_max_step"] == 1.0 and s["HX_max_step"] == 1.0, "D4": le(s["HF_abs_a"], 0.02),
            "D5": le(s["HF_abs_p0"], 0.02), "D6": le(s["GF_leak_pre"], ref["GF_leak_pre"]),
            "D7": le(s["SF_shear"], ref["SF_shear"]),
            "D8": s["SL_conv"] == 1.0 and le(s["SL_shear"], ref["SL_shear"])}


def main() -> None:
    from schemeforge.core.promotion import load_instances

    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--judge", default="contact-v0.12.dev")
    args = ap.parse_args()
    runs = latest_runs(args.judge)
    if REF not in runs:
        raise SystemExit(f"no promo run of {REF} under {args.judge}: "
                         "run `sforge zoo eval --arena contact --suite promo`")
    table = {cid: stats(load_instances(r["run_id"])) for cid, r in runs.items()}
    ref = table[REF]
    cols = list(next(iter(table.values())))
    fps = sorted({r.get("seed_fingerprint", "?") for r in runs.values()})
    print(f"judge {args.judge}; {len(runs)} zoo points; seed fingerprint(s) {', '.join(fps)}; ref = {REF}")
    print("| point | run | " + " | ".join(cols) + " | D1..D8 | all |")
    print("|" + "---|" * (len(cols) + 4))
    for cid in sorted(table):
        v = verdicts(table[cid], ref)
        flags = "".join("+" if ok else "-" for ok in v.values())
        print(f"| {cid.removeprefix('zoo-medium-')} | {runs[cid]['run_id']} | "
              + " | ".join(f"{table[cid][c]:.3g}" for c in cols)
              + f" | {flags} | {'YES' if all(v.values()) else 'no'} |")


if __name__ == "__main__":
    main()
