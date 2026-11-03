"""Frozen predictions for the literature-blind set (B10: Na et al. 2025, Al 6061 heat-treatment series).

Rules: docs/research/coldspray-blind-literature.md (B1-B5) and docs/research/coldspray-preregistration-b10.md.
Inputs come only from docs/research/data/blind_inputs.csv (leak-scanned) and properties.csv. Run
`python -m schemeforge.research.coldspray_blind` to write data/predictions_b10.csv. Not a judge.
"""

from __future__ import annotations

import csv
import math
import re

from schemeforge.research.coldspray import DATA, Row, load_properties, load_rows, make_baseline, z6_sound_speed

T_ROOM_C = 20.0  # temperatures not stated in B10: room temperature assumed (rule BP3)


def b10_conditions() -> list[dict]:
    """B10 rows of blind_inputs.csv with the static compression strength parsed (MPa)."""
    out = []
    with open(DATA / "blind_inputs.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r["cond_id"].startswith("B10"):
                continue
            m = re.search(r"at 50% strain \(Table 1\): ([0-9.]+) \+/- ([0-9.]+) MPa", r["properties_reported"])
            ox = re.search(r"thickness ([0-9.]+) \+/- ([0-9.]+) nm", r["oxide_state"])
            out.append({"cond_id": r["cond_id"], "d_um": float(r["d_um"]), "sigma_static_MPa": float(m.group(1)),
                        "sigma_static_unc_MPa": float(m.group(2)), "oxide_nm": float(ox.group(1))})
    return out


def assadi_eq3(rho_kg_m3: float, tm_k: float, sigma_mpa: float, ti_c: float = T_ROOM_C) -> float:
    """Z1, Assadi2003 Eq. 3 (rho g/cm^3, T_m and T_i in degC, sigma_u MPa), m/s."""
    return 667.0 - 14.0 * rho_kg_m3 / 1000.0 + 0.08 * (tm_k - 273.15) + 0.1 * sigma_mpa - 0.4 * ti_c


def schmidt_eq8(rho_kg_m3: float, tm_k: float, cp: float, sigma_mpa: float, ti_k: float = 293.15,
                f1: float = 1.2, f2: float = 0.3, tr_k: float = 293.0) -> float:
    """Z2, Schmidt2006 Eq. 8 (SI), m/s; calibrated for 25 um particles (process quantity)."""
    mech = f1 * 4.0 * sigma_mpa * 1e6 * (1.0 - (ti_k - tr_k) / (tm_k - tr_k)) / rho_kg_m3
    return math.sqrt(mech + f2 * cp * (tm_k - ti_k))


def predict_b10() -> list[dict]:
    props = load_properties()
    al6061, al = props["Al 6061"], props["Al"]
    rho = al6061["rho_kg_m3"][0]
    tm, cp = al["Tm_K"][0], al["cp_J_kgK"][0]  # rule BP2: pure-Al T_m and c_p (P-HG-Al), flagged
    baseline = make_baseline(load_rows())
    z6, z6c0 = z6_sound_speed(0.15), z6_sound_speed(0.15, use_hugoniot_c0=True)
    out = []
    for c in b10_conditions():
        row = Row(c["cond_id"], "Al 6061", "Al 6061", "polished", c["d_um"], "room", None, None, None,
                  "co-deformation")
        s = c["sigma_static_MPa"]
        preds = {
            "Z6_a015": (z6(row, props).v, True),
            "Z6_a015_C0": (z6c0(row, props).v, True),
            "baseline_LOMO": (baseline(row, props).v, True),
            "Z1_Assadi_static": (assadi_eq3(rho, tm, s), False),
            "Z2_Schmidt_static": (schmidt_eq8(rho, tm, cp, s), False),
        }
        for name, (v, dom) in preds.items():
            out.append({"model": name, "row": c["cond_id"], "v_pred_mps": f"{v:.1f}", "in_domain": str(dom),
                        "sigma_static_MPa": s, "oxide_nm": c["oxide_nm"]})
    return out


def write() -> int:
    preds = predict_b10()
    with open(DATA / "predictions_b10.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(preds[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(preds)
    return len(preds)


if __name__ == "__main__":
    print(write())
