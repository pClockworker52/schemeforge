"""Predictions for blind paper B06 (Wu et al. 2026, Scripta Mater. 283, 117444), cold-spray research track.

Rules: docs/research/coldspray-blind-literature.md (B1-B6) and docs/research/coldspray-preregistration-b06.md.
Inputs come only from docs/research/data/blind_inputs.csv (rows B06-c1, B06-c2; leak-scanned, merged 5f7bf7d) and
properties.csv. Each frozen zoo member and hunch is run with its own registered input rule; a model whose inputs
are missing gives "no prediction" with the reason, never a filled value. coldspray_blind2.py (B02/B14) stays as
frozen. Not a judge.

Run `python -m schemeforge.research.coldspray_blind_b06` to write data/predictions_b06.csv.
"""

from __future__ import annotations

import csv

from schemeforge.research.coldspray import (
    DATA,
    Row,
    dw_size_law,
    load_properties,
    load_rows,
    make_baseline,
    z6_sound_speed,
)

PAPER = "B06"
MATERIAL = ("Al", "Al")  # Al single-crystal particles on a 99 % Al plate (blind_inputs.csv, particle / substrate)
OUT = DATA / "predictions_b06.csv"


def conditions() -> list[dict]:
    """B06 rows with measures_vcr = yes. Diameters are withheld by the extractor (mixed with outcome): d = None."""
    out = []
    with open(DATA / "blind_inputs.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r["cond_id"].startswith(PAPER) or r["measures_vcr"] != "yes":
                continue
            out.append({"cond_id": r["cond_id"],
                        "d_um": float(r["d_um"]) if r["d_um"] else None,
                        "polished": "polished" in r["substrate_condition"]})
    return out


def predict() -> list[dict]:
    """One row per model and condition: v_pred_mps (empty if no prediction), in_domain, note."""
    props = load_properties()
    zoo = {"Z6_a015": z6_sound_speed(0.15), "Z6_a015_C0": z6_sound_speed(0.15, use_hugoniot_c0=True),
           "baseline_LOMO": make_baseline(load_rows()), "DW_size": dw_size_law}
    out = []
    for c in conditions():
        # temperatures not stated: room (rule BP3)
        row = Row(c["cond_id"], MATERIAL[0], MATERIAL[1], "polished" if c["polished"] else "other",
                  c["d_um"], "room", None, None, None, "co-deformation")
        for name, model in zoo.items():
            p = model(row, props)
            note = p.note if c["d_um"] is not None or p.v is None else p.note + "; d not reported (out of domain)"
            out.append({"model": name, "row": c["cond_id"], "v_pred_mps": "" if p.v is None else f"{p.v:.1f}",
                        "in_domain": str(p.in_domain), "note": note})
        # CS-10 prediction rule (coldspray-hunch-cs10.md): needs d, a static particle strength, a numeric oxide
        out.append({"model": "CS-10", "row": c["cond_id"], "v_pred_mps": "", "in_domain": "False",
                    "note": "no prediction: d not reported; no static particle strength (only a cited dynamic yield)"})
        # Z18 (coldspray-zoo-z18.md): Z18_static needs a static strength; Z18_Yd a Y_d fitted by the paper itself to
        # rebounds below v_cr; sigma0 is sourced for aluminium oxide only
        out.append({"model": "Z18_static", "row": c["cond_id"], "v_pred_mps": "", "in_domain": "False",
                    "note": "no prediction: no static particle strength reported"})
        out.append({"model": "Z18_Yd", "row": c["cond_id"], "v_pred_mps": "", "in_domain": "False",
                    "note": "no prediction: Y_d only cited from another study, not fitted by B06 to rebounds"})
    return out


def write() -> int:
    preds = predict()
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(preds[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(preds)
    return len(preds)


if __name__ == "__main__":
    print(write())
