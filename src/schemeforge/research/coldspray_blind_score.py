"""Score the frozen B10 predictions (data/predictions_b10.csv) against the B-B10 rows of data/vcr_lipit.csv.

Implements the scoring section of docs/research/coldspray-preregistration-b10.md: rule S1 per condition, the group
contrast Delta = mean(S) - mean(W) of measured midpoints with S = {c1, c2}, W = {c3, c4, c5}, the typical window
width w = median(v_high - v_low), and the verdicts of CS-08, CS-07 (on B10) and CS-09. Not a judge.
"""

from __future__ import annotations

import csv
import statistics

from schemeforge.research.coldspray import DATA, distance

S, W = ("B10-c1", "B10-c2"), ("B10-c3", "B10-c4", "B10-c5")


def measured() -> dict[str, tuple[float, float, float]]:
    """cond_id -> (v_low, v_high, v_mid) from the B-B10 rows."""
    out = {}
    with open(DATA / "vcr_lipit.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["id"].startswith("B-B10-"):
                lo, hi = float(r["vcr_low_mps"]), float(r["vcr_high_mps"])
                mid = float(r["vcr_mid_mps"]) if r["vcr_mid_mps"] else 0.5 * (lo + hi)
                out[r["id"][2:]] = (lo, hi, mid)
    return out


def verdicts(m: dict[str, tuple[float, float, float]]) -> dict[str, object]:
    mean = lambda ids: statistics.mean(m[i][2] for i in ids)  # noqa: E731
    delta = mean(S) - mean(W)
    w = statistics.median(hi - lo for lo, hi, _ in m.values())
    spread = max(v[2] for v in m.values()) - min(v[2] for v in m.values())
    cs08 = "refuted" if delta <= 0 else "supported" if delta > w else "inconclusive"
    cs07 = "refuted" if delta >= 0 else "supported" if delta < -w else "inconclusive"
    cs09 = "refuted" if spread > 2 * w else "supported" if spread <= w else "inconclusive"
    return {"Delta": delta, "w": w, "spread": spread, "CS-08": cs08, "CS-07 (B10)": cs07, "CS-09": cs09}


def main() -> None:
    m = measured()
    print("measured:", {k: v for k, v in sorted(m.items())})
    rows = []
    with open(DATA / "predictions_b10.csv", newline="") as fh:
        for p in csv.DictReader(fh):
            lo, hi, _ = m[p["row"]]
            d = distance(float(p["v_pred_mps"]), lo, hi)
            rows.append({**p, "v_low": lo, "v_high": hi, "d": f"{d:.4f}"})
    with open(DATA / "scores_b10.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    for model in dict.fromkeys(r["model"] for r in rows):
        ds = [float(r["d"]) for r in rows if r["model"] == model]
        print(f"{model:20s} d per condition {[round(x, 3) for x in ds]}  median {statistics.median(ds):.3f}")
    z2 = {r["row"]: float(r["v_pred_mps"]) for r in rows if r["model"] == "Z2_Schmidt_static"}
    z2_delta = statistics.mean(z2[i] for i in S) - statistics.mean(z2[i] for i in W)
    v = verdicts(m)
    print({k: (round(x, 1) if isinstance(x, float) else x) for k, x in v.items()},
          f"| Z2 predicted Delta {z2_delta:.1f}")


if __name__ == "__main__":
    main()
