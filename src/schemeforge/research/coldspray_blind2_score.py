"""Score the frozen B02/B14 predictions and hunch tests (committed before the outcomes are read). Not a judge.

Implements docs/research/coldspray-preregistration-b02-b14.md and its addendum 1 (CS-16):
- rule S1 per condition and model (windows as printed, else rule B6: v_cr +- the stated velocity uncertainty, given
  as `uncertainty_mps` in the row notes as "velocity uncertainty +-X m/s" or "+-X %"; if none, S1 is not scored);
- w = median window width per paper (None if any window is undefined);
- CS-07 on B14 (Delta_H = v(c7) - mean v(D)), the dry-series spread, v(c8) - v(c7), all reported as exposed;
- CS-16 on B02 (Delta = v(c2) - v(c1) against +102.2 m/s).
"""

from __future__ import annotations

import csv
import re
import statistics

from schemeforge.research.coldspray import DATA, distance

D_SERIES = ("B14-c1", "B14-c3", "B14-c4", "B14-c5")


def _uncertainty(notes: str, mid: float) -> float | None:
    m = re.search(r"velocity uncertainty \+-\s*([0-9.]+)\s*(m/s|%)", notes or "")
    if not m:
        return None
    x = float(m.group(1))
    return x if m.group(2) == "m/s" else x / 100.0 * mid


def measured(prefixes: tuple[str, ...] = ("B-B02-", "B-B14-")) -> dict[str, tuple[float | None, float | None, float]]:
    """cond_id -> (low, high, mid). Missing bounds are filled by rule B6 from a stated uncertainty, else None."""
    out = {}
    with open(DATA / "vcr_lipit.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r["id"].startswith(prefixes):
                continue
            lo = float(r["vcr_low_mps"]) if r["vcr_low_mps"] else None
            hi = float(r["vcr_high_mps"]) if r["vcr_high_mps"] else None
            if r["vcr_mid_mps"]:
                mid = float(r["vcr_mid_mps"])
            elif lo is not None and hi is not None:
                mid = 0.5 * (lo + hi)
            else:
                continue  # no value for this condition
            if lo is None or hi is None:
                u = _uncertainty(r["notes"], mid)
                lo, hi = (mid - u, mid + u) if u is not None else (None, None)
            out[r["id"][2:]] = (lo, hi, mid)
    return out


def median_width(m: dict, paper: str) -> float | None:
    rows = [v for k, v in m.items() if k.startswith(paper)]
    if not rows or any(lo is None for lo, _, _ in rows):
        return None
    return statistics.median(hi - lo for lo, hi, _ in rows)


def s1_scores(m: dict) -> list[dict]:
    out = []
    with open(DATA / "predictions_b02_b14.csv", newline="") as fh:
        preds = list(csv.DictReader(fh))
    with open(DATA / "predictions_b02_cs16.csv", newline="") as fh:
        preds += [dict(r, in_domain="True") for r in csv.DictReader(fh)]
    for p in preds:
        if not p["v_pred_mps"] or p["row"] not in m:
            continue
        lo, hi, mid = m[p["row"]]
        v = float(p["v_pred_mps"])
        out.append({"model": p["model"], "row": p["row"], "v_pred": v, "v_mid": mid, "in_domain": p["in_domain"],
                    "S1": None if lo is None else distance(v, lo, hi), "rel_err": (v - mid) / mid})
    return out


def verdicts(m: dict) -> dict:
    res: dict = {}
    # ---- B14 (all exposed) ----
    w14 = median_width(m, "B14")
    res["w_B14"] = w14
    if all(k in m for k in (*D_SERIES, "B14-c7")):
        d = m["B14-c7"][2] - statistics.mean(m[k][2] for k in D_SERIES)
        res["CS07_delta_H"] = d
        if d <= 0:
            res["CS07_B14"] = "refuted (exposed)"
        elif w14 is None:
            res["CS07_B14"] = "not refuted, support undetermined (w unavailable) (exposed)"
        else:
            res["CS07_B14"] = ("supported (exposed)" if d > w14 else "inconclusive (exposed)")
        spread = max(m[k][2] for k in D_SERIES) - min(m[k][2] for k in D_SERIES)
        res["dry_series_spread"] = spread
        res["dry_series_vs_w"] = None if w14 is None else spread / w14
    if all(k in m for k in ("B14-c7", "B14-c8")):
        res["c8_minus_c7"] = m["B14-c8"][2] - m["B14-c7"][2]
    # ---- B02, CS-16 ----
    w02 = median_width(m, "B02")
    res["w_B02"] = w02
    if all(k in m for k in ("B02-c1", "B02-c2")):
        with open(DATA / "predictions_b02_cs16.csv", newline="") as fh:
            dpred = float(next(csv.DictReader(fh))["delta_pred_mps"])
        dmeas = m["B02-c2"][2] - m["B02-c1"][2]
        res["CS16_delta_meas"], res["CS16_delta_pred"] = dmeas, dpred
        err = abs(dmeas - dpred)
        if dmeas <= 0:
            res["CS16"] = "refuted"
        elif w02 is None:
            res["CS16"] = "not refuted on sign; rest undetermined (w unavailable)"
        elif err > w02 + 0.5 * dpred:
            res["CS16"] = "refuted"
        elif err <= w02 and dpred > w02:
            res["CS16"] = "supported"
        else:
            res["CS16"] = "inconclusive"
    return res


def write() -> dict:
    m = measured()
    rows = s1_scores(m)
    with open(DATA / "scores_b02_b14.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["model", "row", "v_pred", "v_mid", "in_domain", "S1", "rel_err"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return verdicts(m)


if __name__ == "__main__":
    for k, v in write().items():
        print(k, v)
