"""Score CS-24 (docs/research/coldspray-hunch-cs24.md, frozen 9262c78) by its frozen rule. Post hoc (exposed data).

Item A: the six H20 mismatched pairs, v_cr(X on Y) / v_cr(X on X), size-corrected by (d_XY / d_XX)^(1/5); resolved if
|ln r| exceeds the summed half-widths ln(v_high / v_low) / 2 of both rows; agree if sign(ln r) = sign(e_Y - e_X).
Item B: CH heated matched rows against the authors' room-temperature values quoted in the rows' notes (Al 810 m/s at
14.4 um, Sn 330, Ti 765); Al size-corrected by (15.5 / 14.4)^(1/5); resolved if |ln r| exceeds the row's printed
relative uncertainty (v_high - v_low) / (2 v_mid) plus 0.02; agree if r < 1.
Reported: predicted ratios, and a mechanical comparator (sign of the substrate's minus the particle's Yd_micro_MPa,
P-H20 rows; "harder substrate -> higher v_cr").

Usage: python scripts/cs24_score.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "docs" / "research" / "data"
PAIRS = [("Al", "Cu"), ("Al", "Ni"), ("Al", "Ti"), ("Cu", "Al"), ("Cu", "Ti"), ("Ti", "Cu")]
ROOM_T = {"Al": (810.0, 14.4), "Sn": (330.0, None), "Ti": (765.0, None)}  # quoted in the CH rows' notes
T_PARTICLE = 292.0
TM = {"Al": 933.0, "Sn": 505.0, "Ti": 1941.0}  # P-HG-Al, P-WP-Sn, P-WP-Ti (rounded as in the hunch)


def props() -> tuple[dict[str, float], dict[str, float]]:
    rows = list(csv.DictReader(open(DATA / "properties.csv", encoding="utf-8")))
    rho = {r["material"]: float(r["rho_kg_m3"]) for r in rows if r["id"].startswith("P-H20-") and r["rho_kg_m3"]}
    wp = {r["material"]: r for r in rows if r["id"].startswith("P-WP-")}
    e = {m: math.sqrt(rho[m] * float(wp[m]["cp_J_kgK"]) * float(wp[m]["k_W_mK"])) for m in ("Al", "Cu", "Ni", "Ti")}
    yd = {r["material"]: float(r["Yd_micro_MPa"]) for r in rows if r["id"].startswith("P-H20-") and r["Yd_micro_MPa"]}
    return e, yd


def vrow(r: dict) -> tuple[float, float, float, float]:
    return float(r["vcr_low_mps"]), float(r["vcr_high_mps"]), float(r["vcr_mid_mps"]), float(r["d_um"])


def main() -> None:
    e, yd = props()
    rows = list(csv.DictReader(open(DATA / "vcr_lipit.csv", encoding="utf-8")))
    h20 = {(r["particle"], r["substrate"]): r for r in rows if r["id"].startswith("H20")}
    print("Item A (H20 mismatched pairs)")
    agree = disagree = unresolved = 0
    for x, y in PAIRS:
        lo1, hi1, m1, d1 = vrow(h20[(x, y)])
        lo0, hi0, m0, d0 = vrow(h20[(x, x)])
        r = m1 / m0 * (d1 / d0) ** 0.2
        half = math.log(hi1 / lo1) / 2 + math.log(hi0 / lo0) / 2
        pred = ((e[x] + e[y]) / (2 * e[x])) ** 0.4
        mech = math.copysign(1.0, yd[y] - yd[x])
        if abs(math.log(r)) <= half:
            status = "unresolved"
            unresolved += 1
        elif math.copysign(1.0, math.log(r)) == math.copysign(1.0, e[y] - e[x]):
            status = "agree"
            agree += 1
        else:
            status = "disagree"
            disagree += 1
        mech_ok = "" if status == "unresolved" else ("yes" if math.copysign(1.0, math.log(r)) == mech else "no")
        print(f"  {x} on {y}: r_obs {r:.3f} (ln {math.log(r):+.3f}, half-width {half:.3f}) | predicted {pred:.3f} "
              f"(ln {math.log(pred):+.3f}) | {status} | mechanical comparator agrees: {mech_ok or '-'}")
    resolved = agree + disagree
    if resolved >= 4 and agree >= 2 * disagree:
        va = "supported (post hoc)"
    elif resolved and disagree >= agree:
        va = "refuted"
    else:
        va = "undetermined"
    print(f"  resolved {resolved} (agree {agree}, disagree {disagree}), unresolved {unresolved} -> verdict A: {va}")

    print("Item B (CH heated substrates, matched)")
    ch = {r["particle"]: r for r in rows if r["id"].startswith("CH")}
    ba = bd = 0
    for m, (v_rt, d_rt) in ROOM_T.items():
        lo, hi, mid, d = vrow(ch[m])
        r = mid / v_rt * ((d / d_rt) ** 0.2 if d_rt else 1.0)
        tol = (hi - lo) / (2 * mid) + 0.02
        ts = float(ch[m]["T_substrate_K"])
        pred = ((TM[m] - (T_PARTICLE + ts) / 2) / (TM[m] - T_PARTICLE)) ** 0.4
        if abs(math.log(r)) <= tol:
            status = "unresolved"
        elif r < 1:
            status, ba = "agree", ba + 1
        else:
            status, bd = "disagree", bd + 1
        print(f"  {m}: r_obs {r:.3f} (ln {math.log(r):+.3f}, tol {tol:.3f}) | predicted {pred:.3f} | {status}")
    if ba >= 2 and bd == 0:
        vb = "supported (post hoc)"
    elif ba + bd >= 1 and bd >= ba:
        vb = "refuted"
    else:
        vb = "undetermined"
    print(f"  resolved {ba + bd} (agree {ba}, disagree {bd}) -> verdict B: {vb}")
    if va.startswith("supported") and vb != "refuted":
        overall = "supported (post hoc)"
    elif va == "refuted":
        overall = "refuted"
    else:
        overall = "mixed / undetermined"
    print(f"Overall: {overall}")


if __name__ == "__main__":
    main()
