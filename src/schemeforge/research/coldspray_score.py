"""Score the frozen predictions_v1.csv against vcr_lipit.csv (rules S1-S3 of the pre-registration).

Reads only files committed before scoring; writes docs/research/data/scores_v1.csv and prints the summaries
that the hunches CS-01..CS-06 and the judge-noise check refer to. Not a judge.
"""

from __future__ import annotations

import csv
import statistics
from pathlib import Path

from schemeforge.research.coldspray import DATA, distance, load_rows

HELD_OUT_Z6 = ["H20-12", "DW-07", "DW-08", "H20-16", "H20-14", "H20-15", "H20-18", "H20-19", "H20-20"]
HELD_OUT_PURE = ["H20-12", "DW-07", "DW-08", "H20-16", "H20-14", "H20-15"]
ALLOYS = ["H20-18", "H20-19", "H20-20"]


def score(pred_path: Path = DATA / "predictions_v1.csv", out_path: Path = DATA / "scores_v1.csv") -> list[dict]:
    """Attach d (rule S1) and regime agreement to each prediction; write scores_v1.csv."""
    rows = {r.id: r for r in load_rows()}
    out = []
    with open(pred_path, newline="") as fh:
        for p in csv.DictReader(fh):
            r = rows[p["row"]]
            rec = dict(p)
            rec["v_low"], rec["v_high"] = r.lo, r.hi
            rec["d"] = ""
            if p["v_pred_mps"] and r.lo is not None:
                rec["d"] = f"{distance(float(p['v_pred_mps']), r.lo, r.hi):.4f}"
            rec["regime_meas"] = r.regime
            rec["regime_ok"] = "" if not p["regime_pred"] else str(p["regime_pred"] == r.regime)
            out.append(rec)
    with open(out_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    return out


def _d(recs: list[dict], model: str, ids: list[str]) -> dict[str, float]:
    return {r["row"]: float(r["d"]) for r in recs if r["model"] == model and r["row"] in ids and r["d"] != ""}


def summary(recs: list[dict]) -> None:
    """Print per-model in/out-of-domain medians and the quantities named in the hunches."""
    print("model                 n_in  median_d_in  n_out  median_d_out")
    for m in dict.fromkeys(r["model"] for r in recs):
        ins = [float(r["d"]) for r in recs if r["model"] == m and r["d"] and r["in_domain"] == "True"]
        outs = [float(r["d"]) for r in recs if r["model"] == m and r["d"] and r["in_domain"] == "False"]
        fmt = lambda xs: f"{statistics.median(xs):.3f}" if xs else "  -  "  # noqa: E731
        print(f"{m:20s} {len(ins):5d}  {fmt(ins):>11s}  {len(outs):5d}  {fmt(outs):>12s}")
    z6p = _d(recs, "Z6_a015", HELD_OUT_PURE)
    print("\nCS-01 Z6_a015 held-out pure metals:", {k: round(v, 3) for k, v in z6p.items()},
          "median", round(statistics.median(z6p.values()), 3))
    print("CS-02 Z6_a015 Al alloys:", {k: round(v, 3) for k, v in _d(recs, "Z6_a015", ALLOYS).items()})
    z6h, bh = _d(recs, "Z6_a015", HELD_OUT_Z6), _d(recs, "baseline_LOMO", HELD_OUT_Z6)
    print("CS-03 held-out median d: Z6_a015", round(statistics.median(z6h.values()), 3),
          "baseline", round(statistics.median(bh.values()), 3))
    reg = [r for r in recs if r["model"] == "Z9_regime" and r["row"].startswith("H20")]
    bad = [(r["row"], r["regime_pred"], r["regime_meas"]) for r in reg if r["regime_ok"] != "True"]
    print(f"CS-04 Z9 regimes: {len(reg) - len(bad)} of {len(reg)} match; mismatches: {bad}")
    print("CS-05 DW_size:", {k: round(v, 3) for k, v in _d(recs, "DW_size", ["H20-12", "H20-17"]).items()})
    fe = [(r["row"], float(r["v_pred_mps"]), r["v_low"]) for r in recs if r["model"] == "Assadi2003_FE"]
    print("CS-06 Assadi2003_FE below window on all rows:", all(v < float(lo) for _, v, lo in fe),
          [(i, v, lo) for i, v, lo in fe])
    rows = {r.id: r for r in load_rows()}
    preds = {(r["model"], r["row"]): float(r["v_pred_mps"]) for r in recs if r["v_pred_mps"]}
    sep = [i for i in HELD_OUT_Z6 if abs(preds[("Z6_a015", i)] - preds[("baseline_LOMO", i)]) > rows[i].hi - rows[i].lo]
    print(f"Judge-noise check: Z6_a015 vs baseline separated beyond the window width on {len(sep)} of "
          f"{len(HELD_OUT_Z6)} held-out rows: {sep}")


if __name__ == "__main__":
    summary(score())
