"""Post-hoc sensitivity of every frozen cold-spray verdict to the window rule (judge v2 proposal, draft).

Variants (only the measured windows change; frozen predictions are used as committed):
  (i)   as scored: the windows the verdicts were computed on;
  (ii)  primaries: where a primary source has been read since (P18 = HG2018b, P19 = HG2019b), its window replaces
        the H20 quote or re-analysis;
  (iii) proposed rule: (ii), then each bracket window widened by the stated relative velocity error e:
        [lo (1 - e), hi (1 + e)]. Windows already printed as value +- uncertainty (CH, P19, rule B6) are not widened
        again. Rows with no stated e in our extraction (DW, PA) are left as they are and flagged.

Verdict formulas are copied from the frozen preregistrations (coldspray-preregistration.md section 4;
coldspray-preregistration-b10.md; coldspray-preregistration-b02-b14.md). Nothing here changes a recorded verdict.

Usage: python scripts/judge_v2_sensitivity.py   (prints Markdown tables)
"""

from __future__ import annotations

import csv
import statistics as st
from pathlib import Path

DATA = Path("docs/research/data")
PRIMARY = {"H20-17": "P18-Al", "H20-11": "P18-Ni", "H20-10": "P18-Cu", "H20-13": "P18-Zn",
           "H20-14": "P19-Au", "H20-15": "P19-Ag"}
REL_ERR = {"H20": 0.02, "P18": 0.02, "B-B14": 0.02, "B-B10": 0.02, "B-B02": 0.02}
NO_WIDEN = ("CH", "P19", "B-B02", "B-B10")   # windows already value +- uncertainty (printed, or rule B6)
HELD_OUT_Z6 = ["H20-12", "DW-07", "DW-08", "H20-16", "H20-14", "H20-15", "H20-18", "H20-19", "H20-20"]
HELD_OUT_PURE = ["H20-12", "DW-07", "DW-08", "H20-16", "H20-14", "H20-15"]
ALLOYS = ["H20-18", "H20-19", "H20-20"]
VARIANTS = ("i", "ii", "iii")


def _rows() -> dict[str, dict]:
    return {r["id"]: r for r in csv.DictReader(open(DATA / "vcr_lipit.csv", newline=""))}


ROWS = _rows()


def _err(rid: str) -> float | None:
    for k, e in REL_ERR.items():
        if rid.startswith(k):
            return e
    return None


def window(rid: str, variant: str) -> tuple[float, float, str]:
    """(lo, hi, note) of row rid under a variant. For B10/B02 (no printed bounds) rule B6 is used in (iii) only."""
    src = PRIMARY.get(rid, rid) if variant in ("ii", "iii") else rid
    r = ROWS[src]
    note = src if src != rid else ""
    if r["vcr_low_mps"] == "":
        if variant != "iii":
            return (float("nan"), float("nan"), "no bounds printed")
        v, e = float(r["vcr_mid_mps"]), _err(src)
        return (v * (1 - e), v * (1 + e), "B6: v +- 2 %")
    lo, hi = float(r["vcr_low_mps"]), float(r["vcr_high_mps"])
    if variant == "iii":
        e = _err(src)
        if src.startswith(NO_WIDEN):
            note = (note + "; " if note else "") + "already value +- uncertainty"
        elif e is None:
            note = (note + "; " if note else "") + "no stated velocity error: not widened"
        else:
            lo, hi = lo * (1 - e), hi * (1 + e)
    return lo, hi, note


def dist(pred: float, lo: float, hi: float) -> float:
    """Rule S1: 0 inside [lo, hi], else the distance to the nearest bound over the midpoint."""
    mid = 0.5 * (lo + hi)
    if lo <= pred <= hi:
        return 0.0
    return (lo - pred) / mid if pred < lo else (pred - hi) / mid


def preds_v1() -> dict[tuple[str, str], float]:
    out = {}
    for p in csv.DictReader(open(DATA / "predictions_v1.csv", newline="")):
        if p["v_pred_mps"]:
            out[(p["model"], p["row"])] = float(p["v_pred_mps"])
    return out


def v1(variant: str) -> dict[str, str]:
    P = preds_v1()

    def d(model: str, rid: str) -> float:
        lo, hi, _ = window(rid, variant)
        return dist(P[(model, rid)], lo, hi)

    res = {}
    pure = [d("Z6_a015", r) for r in HELD_OUT_PURE]
    m = st.median(pure)
    res["CS-01"] = (f"median d {m:.3f}, max {max(pure):.3f}: "
                    + ("refuted" if m > 0.10 else "supported" if m <= 0.05 and max(pure) <= 0.15 else "inconclusive"))
    al = [d("Z6_a015", r) for r in ALLOYS]
    res["CS-02"] = (f"d {', '.join(f'{x:.3f}' for x in al)}: "
                    + ("refuted" if sum(x <= 0.05 for x in al) >= 2 else "supported" if min(al) > 0.10
                       else "inconclusive"))
    z, b = st.median(d("Z6_a015", r) for r in HELD_OUT_Z6), st.median(d("baseline_LOMO", r) for r in HELD_OUT_Z6)
    res["CS-03"] = (f"median d {z:.3f} vs baseline {b:.3f}: "
                    + ("refuted" if z >= b else "supported" if z - b <= -0.03 else "inconclusive"))
    dw = [d("DW_size", r) for r in ("H20-12", "H20-17")]
    res["CS-05"] = (f"d Ti {dw[0]:.3f}, Al {dw[1]:.3f}: "
                    + ("refuted" if max(dw) > 0.10 else "supported" if max(dw) <= 0.05 else "inconclusive"))
    fe = [(rid, v) for (mdl, rid), v in P.items() if mdl == "Assadi2003_FE"]
    hits = []
    for rid, v in fe:
        lo, _, _ = window(rid, variant)
        if v >= lo:
            hits.append(f"{rid} {v:.0f} >= {lo:.0f}")
    res["CS-06"] = ("refuted (" + "; ".join(hits) + ")") if hits else "not refuted (all below)"
    sep = 0
    for rid in HELD_OUT_Z6:
        lo, hi, _ = window(rid, variant)
        sep += abs(P[("Z6_a015", rid)] - P[("baseline_LOMO", rid)]) > hi - lo
    res["judge-noise"] = f"separated on {sep} of {len(HELD_OUT_Z6)} (needs at least half)"
    return res


def b10(variant: str) -> dict[str, str]:
    ids = [f"B-B10-c{i}" for i in range(1, 6)]
    v = {r: float(ROWS[r]["vcr_mid_mps"]) for r in ids}
    delta = st.mean([v[ids[0]], v[ids[1]]]) - st.mean([v[i] for i in ids[2:]])
    widths = [window(r, variant)[1] - window(r, variant)[0] for r in ids]
    w = st.median(widths)
    have_w = w == w   # not NaN
    res = {"CS-08": f"Delta {delta:+.1f}: " + ("refuted" if delta <= 0 else
                                               "supported" if have_w and delta > w else "undetermined")}
    if delta >= 0:
        c7 = "refuted"
    elif not have_w:
        c7 = "not refuted; support undetermined"
    else:
        c7 = "supported" if delta < -w else "inconclusive"
    res["CS-07 (B10)"] = f"Delta {delta:+.1f}, w {w:.1f}: {c7}" if have_w else f"Delta {delta:+.1f}, w n/a: {c7}"
    spread = max(v.values()) - min(v.values())
    if have_w:
        c9 = "refuted" if spread > 2 * w else "supported" if spread <= w else "inconclusive"
        res["CS-09"] = f"spread {spread:.0f}, w {w:.1f}, 2w {2 * w:.1f}: {c9}"
    else:
        res["CS-09"] = f"spread {spread:.0f}, w n/a: undetermined"
    return res


def b02_b14(variant: str) -> dict[str, str]:
    v = {r: float(ROWS[r]["vcr_mid_mps"]) for r in ROWS if r.startswith(("B-B02", "B-B14"))}
    b02 = ["B-B02-c1", "B-B02-c2"]
    # B02 has no printed bounds: rule B6 was part of the frozen B02/B14 rules, so (i) and (ii) use it too
    w02 = st.median(2 * 0.02 * v[r] for r in b02)
    d_meas, d_pred = v["B-B02-c2"] - v["B-B02-c1"], 102.2
    if d_meas <= 0 or abs(d_meas - d_pred) > w02 + 0.5 * d_pred:
        c16 = "refuted"
    elif abs(d_meas - d_pred) <= w02 and d_pred > w02:
        c16 = "supported"
    else:
        c16 = "inconclusive"
    res = {"CS-16": f"Delta {d_meas:+.1f} (pred +102.2), w {w02:.1f}: {c16}"}
    b14 = [f"B-B14-c{i}" for i in range(1, 9)]
    w14 = st.median(window(r, variant)[1] - window(r, variant)[0] for r in b14)
    dh = v["B-B14-c7"] - st.mean([v["B-B14-c1"], v["B-B14-c3"], v["B-B14-c4"], v["B-B14-c5"]])
    res["CS-07 (B14)"] = (f"Delta_H {dh:+.1f}, w {w14:.1f}: "
                          + ("refuted" if dh <= 0 else "supported" if dh > w14 else "inconclusive"))
    dry = [v[f"B-B14-c{i}"] for i in (1, 3, 4, 5)]
    res["B14 dry spread (no verdict)"] = f"{max(dry) - min(dry):.1f} = {(max(dry) - min(dry)) / w14:.2f} w"
    dd = v["B-B14-c8"] - v["B-B14-c7"]
    res["RH-95-D minus RH-95 (no verdict)"] = f"{dd:+.1f} = {abs(dd) / w14:.2f} w"
    return res


def main() -> None:
    for title, fn in (("v1 retrospective (coldspray-results-v1.md)", v1), ("B10", b10), ("B02 and B14", b02_b14)):
        out = {k: fn(k) for k in VARIANTS}
        print(f"\n#### {title}\n")
        print("| Item | (i) as scored | (ii) primaries | (iii) primaries + velocity error |")
        print("|---|---|---|---|")
        for key in out["i"]:
            print(f"| {key} | " + " | ".join(out[k][key] for k in VARIANTS) + " |")
    print("\nWindow notes under (iii):")
    for rid in HELD_OUT_Z6 + ["H20-17", "H20-10", "H20-11", "H20-13"]:
        lo, hi, note = window(rid, "iii")
        print(f"- {rid}: {lo:.0f}-{hi:.0f} {note}")


if __name__ == "__main__":
    main()
