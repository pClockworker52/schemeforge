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


def measured() -> dict[str, tuple[float | None, float | None, float]]:
    """cond_id -> (v_low, v_high, v_mid) from the B-B10 rows; bounds are None where the paper prints none."""
    out = {}
    with open(DATA / "vcr_lipit.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["id"].startswith("B-B10-"):
                lo = float(r["vcr_low_mps"]) if r["vcr_low_mps"] else None
                hi = float(r["vcr_high_mps"]) if r["vcr_high_mps"] else None
                mid = float(r["vcr_mid_mps"]) if r["vcr_mid_mps"] else 0.5 * (lo + hi)
                out[r["id"][2:]] = (lo, hi, mid)
    return out


def verdicts(m: dict[str, tuple[float, float, float]]) -> dict[str, object]:
    mean = lambda ids: statistics.mean(m[i][2] for i in ids)  # noqa: E731
    delta = mean(S) - mean(W)
    widths = [hi - lo for lo, hi, _ in m.values() if lo is not None and hi is not None]
    w = statistics.median(widths) if len(widths) == len(m) else None  # undefined unless every window is printed
    spread = max(v[2] for v in m.values()) - min(v[2] for v in m.values())
    und = "undetermined (w unavailable)"
    # verdict rules exactly as frozen; branches that need w are undetermined when w is None
    if delta <= 0:
        cs08 = "refuted"
    else:
        cs08 = und if w is None else ("supported" if delta > w else "inconclusive")
    if delta >= 0:
        cs07 = "refuted"
    else:
        cs07 = "not refuted; support " + und if w is None else ("supported" if delta < -w else "inconclusive")
    cs09 = und if w is None else ("refuted" if spread > 2 * w else "supported" if spread <= w else "inconclusive")
    return {"Delta": delta, "w": w, "spread": spread, "CS-08": cs08, "CS-07 (B10)": cs07, "CS-09": cs09}


def main() -> None:
    m = measured()
    print("measured:", {k: v for k, v in sorted(m.items())})
    rows = []
    with open(DATA / "predictions_b10.csv", newline="") as fh:
        for p in csv.DictReader(fh):
            lo, hi, mid = m[p["row"]]
            v = float(p["v_pred_mps"])
            d = "" if lo is None or hi is None else f"{distance(v, lo, hi):.4f}"
            # post hoc, not a frozen rule: relative error to the printed v_cr, reported because S1 is unavailable
            rows.append({**p, "v_low": lo, "v_high": hi, "v_mid": mid, "d": d,
                         "rel_err_posthoc": f"{(v - mid) / mid:+.4f}"})
    with open(DATA / "scores_b10.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    for model in dict.fromkeys(r["model"] for r in rows):
        es = [float(r["rel_err_posthoc"]) for r in rows if r["model"] == model]
        print(f"{model:20s} rel. error to v_cr (post hoc) {[round(x, 3) for x in es]}")
    z2 = {r["row"]: float(r["v_pred_mps"]) for r in rows if r["model"] == "Z2_Schmidt_static"}
    z2_delta = statistics.mean(z2[i] for i in S) - statistics.mean(z2[i] for i in W)
    v = verdicts(m)
    print({k: (round(x, 1) if isinstance(x, float) else x) for k, x in v.items()},
          f"| Z2 predicted Delta {z2_delta:.1f}")


if __name__ == "__main__":
    main()
