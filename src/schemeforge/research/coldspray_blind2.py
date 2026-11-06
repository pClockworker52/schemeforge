"""Frozen predictions for blind papers after B10 (first use: B02 and B14), cold-spray research track.

Rules: docs/research/coldspray-blind-literature.md (B1-B6) and docs/research/coldspray-preregistration-b02-b14.md.
Inputs come only from docs/research/data/blind_inputs.csv (leak-scanned) and properties.csv. Every frozen zoo member
and hunch with a numeric prediction is run with its own registered input rule; a model whose inputs are missing
gives "no prediction" with the reason, never a filled value. Not a judge.

Run `python -m schemeforge.research.coldspray_blind2` to write data/predictions_b02_b14.csv.
"""

from __future__ import annotations

import csv
import math
import re

from schemeforge.research import coldspray_cs10 as cs10
from schemeforge.research import coldspray_z18 as z18
from schemeforge.research.coldspray import (
    DATA,
    Row,
    bulk_modulus_pa,
    dw_size_law,
    load_properties,
    load_rows,
    make_baseline,
    z6_sound_speed,
)

# Base metal of particle and substrate, read from the particle / substrate fields of blind_inputs.csv (frozen here).
MATERIAL = {"B02": ("Cu", "Cu"), "B14": ("Al", "Al")}
PAPERS = tuple(MATERIAL)


def oxide_thickness_nm(text: str) -> float | None:
    """Numeric oxide thickness of the powder (nm) as stated, else None (rule: not reported -> no prediction).

    Accepts "~8 nm" or "~5-6 nm" (midpoint). Relative statements ("thinner than ... by less than 1 nm") and
    "not separately reported" give None.
    """
    if text.startswith("not ") or "thinner than" in text or "thicker than" in text:
        return None
    m = re.search(r"~([0-9.]+)(?:-([0-9.]+))? nm", text)
    if not m:
        return None
    return float(m.group(1)) if not m.group(2) else 0.5 * (float(m.group(1)) + float(m.group(2)))


def conditions(papers: tuple[str, ...] = PAPERS) -> list[dict]:
    """Parsed inputs per condition. Strength and oxide are taken only as the registered input rules allow."""
    out = []
    with open(DATA / "blind_inputs.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            paper = r["cond_id"][:3]
            if paper not in papers or r["measures_vcr"] != "yes":
                continue
            part, sub = MATERIAL[paper]
            # static compression strength of the powder (rule BP1), else powder microhardness (Tabor); else none
            m = re.search(r"static (?:uniaxial |compression )?strength[^:]*: ([0-9.]+)", r["properties_reported"])
            hv = re.search(r"powder microhardness ([0-9.]+) \+/- [0-9.]+ HV", r["properties_reported"])
            sigma = float(m.group(1)) if m else (9.807 * float(hv.group(1)) / 3.0 if hv else None)
            oxide = oxide_thickness_nm(r["oxide_state"])
            out.append({"cond_id": r["cond_id"], "paper": paper, "particle": part, "substrate": sub,
                        "d_um": float(r["d_um"]),
                        "polished": any(k in r["substrate_condition"] for k in ("polished", "mirror finish")),
                        "sigma_static_MPa": sigma, "oxide_nm": oxide})
    return out


def predict(papers: tuple[str, ...] = PAPERS) -> list[dict]:
    props = load_properties()
    baseline = make_baseline(load_rows())
    zoo = {"Z6_a015": z6_sound_speed(0.15), "Z6_a015_C0": z6_sound_speed(0.15, use_hugoniot_c0=True),
           "baseline_LOMO": baseline, "DW_size": dw_size_law}
    cs10_model = cs10.Cs10(0.3774067948140878, 319047040167.4167)  # frozen in 2ce15c6
    k_static = 0.07138911874953116  # frozen Z18_static, 5ab3442
    out = []
    for c in conditions(papers):
        # temperatures not stated in B02; B14 states room temperature: room for both (rule BP3)
        row = Row(c["cond_id"], c["particle"], c["substrate"], "polished" if c["polished"] else "other",
                  c["d_um"], "room", None, None, None, "co-deformation")
        for name, model in zoo.items():
            p = model(row, props)
            out.append({"model": name, "row": c["cond_id"], "v_pred_mps": "" if p.v is None else f"{p.v:.1f}",
                        "in_domain": str(p.in_domain), "note": p.note})
        # CS-10: needs particle strength and numeric oxide thickness (registration, prediction rule)
        p = props[c["particle"]]
        if c["sigma_static_MPa"] is None or c["oxide_nm"] is None:
            out.append({"model": "CS-10", "row": c["cond_id"], "v_pred_mps": "", "in_domain": "False",
                        "note": "no prediction: " + ("no particle strength" if c["sigma_static_MPa"] is None
                                                     else "no numeric oxide thickness")})
        else:
            rho = p["rho_kg_m3"][0]
            cc = math.sqrt(bulk_modulus_pa(p)[0] / rho)
            v = cs10_model.v(cc, rho, c["sigma_static_MPa"] * 1e6, c["oxide_nm"] * 1e-9 / (c["d_um"] * 1e-6))
            out.append({"model": "CS-10", "row": c["cond_id"], "v_pred_mps": f"{v:.1f}", "in_domain": "True",
                        "note": ""})
        # Z18: Al and Al alloys only; Z18_static needs strength, Z18_Yd needs a sub-critical Y_d for an Al powder
        if c["particle"] != "Al":
            for name in ("Z18_static", "Z18_Yd"):
                out.append({"model": name, "row": c["cond_id"], "v_pred_mps": "", "in_domain": "False",
                            "note": "no prediction: sigma0 sourced for aluminium oxide only"})
        else:
            for name in ("Z18_static", "Z18_Yd"):
                if name == "Z18_static" and c["sigma_static_MPa"] is not None and c["oxide_nm"] is not None:
                    v = z18.v_cr(k_static, p["C0_mps"][0], bulk_modulus_pa(p)[0], c["sigma_static_MPa"] * 1e6,
                                 c["oxide_nm"])
                    out.append({"model": name, "row": c["cond_id"], "v_pred_mps": f"{v:.1f}", "in_domain": "True",
                                "note": ""})
                else:
                    out.append({"model": name, "row": c["cond_id"], "v_pred_mps": "", "in_domain": "False",
                                "note": "no prediction: no particle strength reported"})
    return out


def write() -> int:
    preds = predict()
    with open(DATA / "predictions_b02_b14.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(preds[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(preds)
    return len(preds)


if __name__ == "__main__":
    print(write())


# ---- CS-16 (addendum to the B02/B14 pre-registration): substrate hardness raises v_cr for matched Cu ----
HV_PER_MPA = 1.0 / 9.807
B02_SUBSTRATE_HV_MPA = {"B02-c1": 622.0, "B02-c2": 1032.0}  # Vickers as printed (blind_inputs.csv), MPa
PA_ROWS = {"PA-01": 98.0, "PA-02": 142.0}  # Panova2026b substrate hardness (HV), same 19 um Cu powder (seen data)


def cs16_exponent() -> float:
    """n in v_cr ~ HV_substrate^n, from PA-01 and PA-02 (vcr_lipit.csv midpoints)."""
    mids = {r.id: r.mid for r in load_rows() if r.id in PA_ROWS}
    return math.log(mids["PA-02"] / mids["PA-01"]) / math.log(PA_ROWS["PA-02"] / PA_ROWS["PA-01"])


def cs16_predict() -> dict[str, float]:
    """v_cr (m/s) for B02-c1, B02-c2 scaled from PA-01: v = v_PA01 (HV / 98)^n."""
    n = cs16_exponent()
    v01 = next(r.mid for r in load_rows() if r.id == "PA-01")
    out = {k: v01 * (mpa * HV_PER_MPA / PA_ROWS["PA-01"]) ** n for k, mpa in B02_SUBSTRATE_HV_MPA.items()}
    out["delta_pred"] = out["B02-c2"] - out["B02-c1"]
    out["n"] = n
    return out


def write_cs16() -> dict[str, float]:
    p = cs16_predict()
    with open(DATA / "predictions_b02_cs16.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["model", "row", "v_pred_mps", "substrate_HV", "exponent_n", "delta_pred_mps"])
        for k in ("B02-c1", "B02-c2"):
            w.writerow(["CS-16", k, f"{p[k]:.1f}", f"{B02_SUBSTRATE_HV_MPA[k] * HV_PER_MPA:.1f}", f"{p['n']:.4f}",
                        f"{p['delta_pred']:.1f}"])
    return p
