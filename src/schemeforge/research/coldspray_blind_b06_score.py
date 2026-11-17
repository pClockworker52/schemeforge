"""Score the frozen B06 predictions and the CS-07 sign test (committed before the outcomes are read). Not a judge.

Implements docs/research/coldspray-preregistration-b06.md (frozen in c484494):
- rule S1 per condition and model (windows as printed, else rule B6: v_cr +- the stated velocity uncertainty, read
  from the row notes as "velocity uncertainty +-X m/s" or "+-X %"; if none, S1 is not scored);
- w = median window width of B06 (None if any window is undefined);
- CS-07 on B06: Delta = v(c2) - v(c1); refuted if Delta <= 0, supported if Delta > w, inconclusive otherwise.
CS-12 T1 is read from the notes by hand (exposed), not scored here. Reuses the frozen B02/B14 helpers unchanged.

Run `python -m schemeforge.research.coldspray_blind_b06_score` to write data/scores_b06.csv and print the verdicts.
"""

from __future__ import annotations

import csv
from pathlib import Path

from schemeforge.research import coldspray_blind2_score as s2
from schemeforge.research.coldspray import distance

PREFIX = ("B-B06-",)


def s1_scores(m: dict, preds_path: Path) -> list[dict]:
    """Rule S1 for every frozen prediction with a value whose condition has an outcome row."""
    with open(preds_path, newline="") as fh:
        preds = list(csv.DictReader(fh))
    out = []
    for p in preds:
        if not p["v_pred_mps"] or p["row"] not in m:
            continue
        lo, hi, mid = m[p["row"]]
        v = float(p["v_pred_mps"])
        out.append({"model": p["model"], "row": p["row"], "v_pred": v, "v_mid": mid, "in_domain": p["in_domain"],
                    "S1": None if lo is None else distance(v, lo, hi), "rel_err": (v - mid) / mid})
    return out


def verdicts(m: dict) -> dict:
    """CS-07 sign test on B06 and the paper's median window width."""
    w = s2.median_width(m, "B06")
    res: dict = {"w_B06": w}
    if not all(k in m for k in ("B06-c1", "B06-c2")):
        res["CS07_B06"] = "no outcome rows"
        return res
    d = m["B06-c2"][2] - m["B06-c1"][2]
    res["CS07_delta"] = d
    if d <= 0:
        res["CS07_B06"] = "refuted"
    elif w is None:
        res["CS07_B06"] = "not refuted, support undetermined (w unavailable)"
    else:
        res["CS07_B06"] = "supported" if d > w else "inconclusive"
    return res


def write(data: Path | None = None) -> dict:
    """Score from data/ (default: the repository's research data) and write scores_b06.csv there."""
    data = data or s2.DATA
    old = s2.DATA
    s2.DATA = data  # measured() reads vcr_lipit.csv from the module's DATA
    try:
        m = s2.measured(PREFIX)
    finally:
        s2.DATA = old
    rows = s1_scores(m, data / "predictions_b06.csv")
    with open(data / "scores_b06.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["model", "row", "v_pred", "v_mid", "in_domain", "S1", "rel_err"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    res = verdicts(m)
    res["n_scored"] = len(rows)
    return res


if __name__ == "__main__":
    for k, v in write().items():
        print(f"{k}: {v}")
