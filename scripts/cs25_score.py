"""CS-25 frozen rule as code (docs/research/coldspray-hunch-cs25.md, section 6). Committed before it is run.

Judged item J (H20 rows):
- Cu on W against Cu on Cu; Sn on Cu against Sn on Sn; W on Cu against Cu on Cu;
- r_obs = v_mid(num) / v_mid(den) * (d_num / d_den)^0.2 (Z8's measured size exponent);
- hw = ln(v_high / v_low) / 2 summed over both rows; tol = hw + 0.15;
- agree if |ln r_obs - ln r_CS25| <= tol; closer if that error is below the errors of both comparators
  (Z6 particle only, Z6 with arithmetic means of B and rho);
- verdict: supported (post hoc) if >= 2 agree and CS-25 is closer on >= 2; refuted if >= 2 disagree; else undetermined.
Reported, not judged: reversal ratios (Al/Cu, Cu/Ti, Cu/W); S1 distance of CS-25's absolute v_cr on all nine H20
mismatched rows; CS-25's limiting face against Z9's regime label; the ratios without the size correction.

Fix 2026-11-28 (after the first run crashed on blank windows, before any number was printed): rows without a numeric
window are reported as not scorable. The rule is unchanged.

Run: uv run python scripts/cs25_score.py [--data PATH]   (PATH defaults to docs/research/data/vcr_lipit.csv)
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cs25_predict import ALPHA, limiting_face, mat, vcr, z6_mean  # noqa: E402

from schemeforge.research.coldspray import load_properties  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "docs" / "research" / "data" / "vcr_lipit.csv"
TOL_EXTRA = 0.15
SIZE_EXPONENT = 0.2
# (numerator pair, denominator pair), each (particle, substrate)
JUDGED = [(("Cu", "W"), ("Cu", "Cu")), (("Sn", "Cu"), ("Sn", "Sn")), (("W", "Cu"), ("Cu", "Cu"))]
REVERSALS = [("Al", "Cu"), ("Cu", "Ti"), ("Cu", "W")]


def vrow(r: dict) -> tuple[float, float, float, float]:
    """(v_low, v_high, v_mid) [m/s] and d [um] of one row."""
    return float(r["vcr_low_mps"]), float(r["vcr_high_mps"]), float(r["vcr_mid_mps"]), float(r["d_um"])


def scorable(*rows: dict) -> bool:
    """True if every row has a numeric window (Hassani 2020 prints NA where no window satisfies its definition)."""
    return all(r["vcr_low_mps"] and r["vcr_high_mps"] and r["vcr_mid_mps"] and r["d_um"] for r in rows)


def ratio(num: dict, den: dict, size: bool = True) -> tuple[float, float]:
    """(r_obs, hw) of two rows."""
    lo1, hi1, m1, d1 = vrow(num)
    lo0, hi0, m0, d0 = vrow(den)
    r = m1 / m0 * ((d1 / d0) ** SIZE_EXPONENT if size else 1.0)
    return r, math.log(hi1 / lo1) / 2 + math.log(hi0 / lo0) / 2


def s1(pred: float, lo: float, hi: float) -> float:
    """Rule S1: 0 inside [lo, hi], else the distance to the nearest bound over the window midpoint."""
    if lo <= pred <= hi:
        return 0.0
    return min(abs(pred - lo), abs(pred - hi)) / (0.5 * (lo + hi))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, default=DATA)
    args = ap.parse_args()
    props = load_properties()
    rows = list(csv.DictReader(open(args.data, encoding="utf-8")))
    h20 = {(r["particle"], r["substrate"]): r for r in rows if r["id"].startswith("H20")}

    print(f"Item J (tol = hw + {TOL_EXTRA}; size exponent {SIZE_EXPONENT})")
    agree = disagree = closer = 0
    for (num, den) in JUDGED:
        if not scorable(h20[num], h20[den]):
            print(f"  {num[0]} on {num[1]} / {den[0]} on {den[1]}: not scorable (no numeric window; notes: "
                  f"{h20[num]['notes'] if not scorable(h20[num]) else h20[den]['notes']})")
            continue
        pp, ss = mat(props, num[0]), mat(props, num[1])
        ref = mat(props, den[0])
        v0 = ALPHA * ref["c"]
        preds = {"CS-25": vcr(pp, ss) / v0, "Z6 particle only": ALPHA * pp["c"] / v0, "Z6 mean": z6_mean(pp, ss) / v0}
        r, hw = ratio(h20[num], h20[den])
        tol = hw + TOL_EXTRA
        err = {k: abs(math.log(r) - math.log(v)) for k, v in preds.items()}
        ok = err["CS-25"] <= tol
        cl = err["CS-25"] < min(err["Z6 particle only"], err["Z6 mean"])
        agree, disagree, closer = agree + ok, disagree + (not ok), closer + cl
        r_ns, _ = ratio(h20[num], h20[den], size=False)
        print(f"  {num[0]} on {num[1]} / {den[0]} on {den[1]}: r_obs {r:.3f} (ln {math.log(r):+.3f}; no size "
              f"correction {r_ns:.3f}), hw {hw:.3f}, tol {tol:.3f} | predicted CS-25 {preds['CS-25']:.3f}, "
              f"Z6 particle only {preds['Z6 particle only']:.3f}, Z6 mean {preds['Z6 mean']:.3f} | |ln error| "
              + ", ".join(f"{k} {v:.3f}" for k, v in err.items())
              + f" | {'agree' if ok else 'disagree'}, {'closer' if cl else 'not closer'}")
    if agree >= 2 and closer >= 2:
        verdict = "supported (post hoc)"
    elif disagree >= 2:
        verdict = "refuted"
    else:
        verdict = "undetermined"
    print(f"  agree {agree}, disagree {disagree}, closer {closer} -> verdict J: {verdict}")

    print("Reported: reversal ratios v_cr(Y on X) / v_cr(X on Y), size-corrected (CS-25 predicts 1.000)")
    for x, y in REVERSALS:
        if not scorable(h20[(y, x)], h20[(x, y)]):
            print(f"  {y} on {x} / {x} on {y}: not scorable (no numeric window)")
            continue
        r, hw = ratio(h20[(y, x)], h20[(x, y)])
        print(f"  {y} on {x} / {x} on {y}: {r:.3f} (ln {math.log(r):+.3f}, hw {hw:.3f})")

    print("Reported: CS-25 absolute v_cr on the H20 mismatched rows (S1 distance), limiting face, Z9 regime")
    for (x, y), r in sorted(h20.items(), key=lambda kv: kv[1]["id"]):
        if x == y:
            continue
        if not scorable(r):
            print(f"  {r['id']} {x} on {y}: not scorable (no numeric window) | Z9 regime {r['regime']}")
            continue
        lo, hi, _, _ = vrow(r)
        pp, ss = mat(props, x), mat(props, y)
        v = vcr(pp, ss)
        print(f"  {r['id']} {x} on {y}: CS-25 {v:.0f} m/s, window [{lo:.0f}, {hi:.0f}], S1 {s1(v, lo, hi):.3f} | "
              f"limiting face {limiting_face(pp, ss)} | Z9 regime {r['regime']}")


if __name__ == "__main__":
    main()
