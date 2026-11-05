"""Zoo member Z18: Na et al. 2025 Eq. 6 (Lienhard jet rule of mixtures), cold-spray research track.

Registration and frozen rules: docs/research/coldspray-zoo-z18.md (committed before this fit). Not a judge.

    V_cr = (2/k) (C0/B) [sigma0 t0/t + sigma_m (t - t0)/t]

Units: V, C0 in m/s; B, sigma in Pa; t0 and t in nm (ratio only).
Run `python -m schemeforge.research.coldspray_z18` to write data/z18_fit.csv.
"""

from __future__ import annotations

import csv

from schemeforge.research.coldspray import DATA, bulk_modulus_pa, load_properties, load_rows
from schemeforge.research.coldspray_blind import b10_conditions

SIGMA0_PA = 870e6  # oxide strength, Na2025 (from Lienhard 2020, Sun 2020); aluminium oxide only
T_JET_NM = 100.0  # jet thickness, Na2025 (from Lienhard 2020)
K_PUBLISHED = 0.062  # Na2025, fitted on the as-received B10 powder
MPA = 1e6
# Na2025 Table 1, dynamic yield strength Y_d (MPa) from CoR data; B10 is unblinded and scored.
B10_YD_MPA = {"B10-c1": 246.3, "B10-c2": 197.4, "B10-c3": 197.8, "B10-c4": 163.1, "B10-c5": 188.9}


def sigma_eff(sigma_m_pa: float, t0_nm: float, t_nm: float = T_JET_NM, sigma0_pa: float = SIGMA0_PA) -> float:
    """Eq. 5: effective jet strength (Pa), rule of mixtures by thickness."""
    return sigma0_pa * t0_nm / t_nm + sigma_m_pa * (t_nm - t0_nm) / t_nm


def v_cr(k: float, c0: float, b_pa: float, sigma_m_pa: float, t0_nm: float) -> float:
    """Eq. 6: critical velocity (m/s)."""
    return (2.0 / k) * (c0 / b_pa) * sigma_eff(sigma_m_pa, t0_nm)


def al6061_c0_b() -> tuple[float, float]:
    """C0 (Hugoniot, Table S1) and B = E/(3(1-2nu)) (Table S1) for Al 6061, rule P1."""
    p = load_properties()["Al 6061"]
    return p["C0_mps"][0], bulk_modulus_pa(p)[0]


def calibration_rows() -> list[dict]:
    mids = {r.id.removeprefix("B-"): r.mid for r in load_rows() if r.id.startswith("B-B10")}
    return [{"cond_id": c["cond_id"], "sigma_static_pa": c["sigma_static_MPa"] * MPA, "t0_nm": c["oxide_nm"],
             "v_meas": mids[c["cond_id"]]} for c in b10_conditions()]


def fit_k(rows: list[dict], c0: float, b_pa: float) -> float:
    """Frozen rule: one-parameter least squares on V; V = x/k with x = (2 C0/B) sigma_eff."""
    xs = [2.0 * c0 / b_pa * sigma_eff(r["sigma_static_pa"], r["t0_nm"]) for r in rows]
    return sum(x * x for x in xs) / sum(r["v_meas"] * x for x, r in zip(xs, rows, strict=True))


def report() -> dict:
    c0, b = al6061_c0_b()
    rows = calibration_rows()
    k = fit_k(rows, c0, b)
    out = {"k_static": k, "c0": c0, "B": b, "rows": []}
    for i, r in enumerate(rows):
        k_loo = fit_k(rows[:i] + rows[i + 1:], c0, b)
        out["rows"].append({
            "cond_id": r["cond_id"], "v_meas": r["v_meas"],
            "z18_static": v_cr(k, c0, b, r["sigma_static_pa"], r["t0_nm"]),
            "z18_static_loo": v_cr(k_loo, c0, b, r["sigma_static_pa"], r["t0_nm"]),
            "z18_yd": v_cr(K_PUBLISHED, c0, b, B10_YD_MPA[r["cond_id"]] * MPA, r["t0_nm"]),
        })
    v = {r["cond_id"]: r for r in out["rows"]}
    for key in ("z18_static", "z18_yd"):
        s = (v["B10-c1"][key] + v["B10-c2"][key]) / 2
        w = (v["B10-c3"][key] + v["B10-c4"][key] + v["B10-c5"][key]) / 3
        out[f"delta_{key}"] = s - w
    return out


def write() -> dict:
    rep = report()
    with open(DATA / "z18_fit.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["cond_id", "v_meas_mps", "z18_static_mps", "z18_static_loo_mps", "z18_yd_mps", "k_static",
                    "k_published"])
        for r in rep["rows"]:
            w.writerow([r["cond_id"], f"{r['v_meas']:.1f}", f"{r['z18_static']:.1f}", f"{r['z18_static_loo']:.1f}",
                        f"{r['z18_yd']:.1f}", f"{rep['k_static']:.5f}", K_PUBLISHED])
    return rep


if __name__ == "__main__":
    rep = write()
    print({k: v for k, v in rep.items() if k != "rows"})
    for r in rep["rows"]:
        print(r)
