"""Hunch CS-10: combined strength + oxide energy balance for single-impact v_cr (cold-spray research track).

Registration and frozen rules: docs/research/coldspray-hunch-cs10.md (committed before this fit). Not a judge.

    v_cr^2 = (alpha c)^2 + beta sigma_p / rho + gamma (t_ox / d) / rho

Units: v, c in m/s; sigma_p, gamma in Pa; rho in kg/m^3; t_ox and d in the same length unit (ratio only).
Run `python -m schemeforge.research.coldspray_cs10` to write data/cs10_fit.csv.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass

from schemeforge.research.coldspray import DATA, bulk_modulus_pa, load_properties, load_rows
from schemeforge.research.coldspray_blind import b10_conditions

ALPHA = 0.15  # Z6_a015, fixed (not refitted)
MPA = 1e6


@dataclass(frozen=True)
class Cs10:
    """Fitted constants: beta (dimensionless), gamma (Pa)."""

    beta: float
    gamma: float

    def v(self, c_mps: float, rho: float, sigma_pa: float, t_over_d: float) -> float:
        """Predicted v_cr (m/s) for jet sound speed c, density rho, strength sigma_p (Pa), ratio t_ox/d."""
        return math.sqrt((ALPHA * c_mps) ** 2 + self.beta * sigma_pa / rho + self.gamma * t_over_d / rho)


def nnls2(x1: list[float], x2: list[float], y: list[float]) -> tuple[float, float]:
    """Exact non-negative least squares for y ~ b1 x1 + b2 x2 (no intercept), b1, b2 >= 0.

    Tries the unconstrained solution, then each one-variable fit, and returns the feasible candidate with the
    smallest residual sum of squares.
    """
    s11 = sum(a * a for a in x1)
    s22 = sum(b * b for b in x2)
    s12 = sum(a * b for a, b in zip(x1, x2, strict=True))
    s1y = sum(a * c for a, c in zip(x1, y, strict=True))
    s2y = sum(b * c for b, c in zip(x2, y, strict=True))

    def rss(b1: float, b2: float) -> float:
        return sum((c - b1 * a - b2 * b) ** 2 for a, b, c in zip(x1, x2, y, strict=True))

    cands = [(0.0, 0.0), (max(s1y / s11, 0.0), 0.0), (0.0, max(s2y / s22, 0.0))]
    det = s11 * s22 - s12 * s12
    if det != 0.0:
        b1 = (s1y * s22 - s2y * s12) / det
        b2 = (s2y * s11 - s1y * s12) / det
        if b1 >= 0.0 and b2 >= 0.0:
            cands.append((b1, b2))
    return min(cands, key=lambda b: rss(*b))


def calibration_data() -> list[dict]:
    """B10 calibration rows: inputs from blind_inputs.csv / properties.csv, printed v_cr from vcr_lipit.csv."""
    props = load_properties()["Al 6061"]
    rho = props["rho_kg_m3"][0]
    b, _ = bulk_modulus_pa(props)
    c = math.sqrt(b / rho)
    mids = {r.id.removeprefix("B-"): r.mid for r in load_rows() if r.id.startswith("B-B10")}
    out = []
    for k in b10_conditions():
        out.append({"cond_id": k["cond_id"], "rho": rho, "c": c, "sigma_pa": k["sigma_static_MPa"] * MPA,
                    "t_over_d": k["oxide_nm"] * 1e-9 / (k["d_um"] * 1e-6), "v_meas": mids[k["cond_id"]]})
    return out


def fit(rows: list[dict]) -> Cs10:
    """Frozen fitting rule: NNLS of v^2 - (alpha c)^2 on sigma/rho and (t/d)/rho, unweighted."""
    y = [r["v_meas"] ** 2 - (ALPHA * r["c"]) ** 2 for r in rows]
    x1 = [r["sigma_pa"] / r["rho"] for r in rows]
    x2 = [r["t_over_d"] / r["rho"] for r in rows]
    return Cs10(*nnls2(x1, x2, y))


def report() -> dict:
    """Fit on all five B10 rows plus in-sample and leave-one-out residuals (all in-sample / post hoc)."""
    rows = calibration_data()
    m = fit(rows)
    out = {"model": m, "rows": []}
    for i, r in enumerate(rows):
        loo = fit(rows[:i] + rows[i + 1:])
        v_in = m.v(r["c"], r["rho"], r["sigma_pa"], r["t_over_d"])
        v_loo = loo.v(r["c"], r["rho"], r["sigma_pa"], r["t_over_d"])
        out["rows"].append({"cond_id": r["cond_id"], "v_meas": r["v_meas"], "v_fit": v_in, "v_loo": v_loo,
                            "loo_beta": loo.beta, "loo_gamma": loo.gamma})
    v = {r["cond_id"]: r["v_fit"] for r in out["rows"]}
    out["delta_pred"] = (v["B10-c1"] + v["B10-c2"]) / 2 - (v["B10-c3"] + v["B10-c4"] + v["B10-c5"]) / 3
    return out


def write() -> dict:
    rep = report()
    m = rep["model"]
    with open(DATA / "cs10_fit.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["cond_id", "v_meas_mps", "v_fit_mps", "v_loo_mps", "loo_beta", "loo_gamma_Pa",
                    "beta", "gamma_Pa"])
        for r in rep["rows"]:
            w.writerow([r["cond_id"], f"{r['v_meas']:.1f}", f"{r['v_fit']:.1f}", f"{r['v_loo']:.1f}",
                        f"{r['loo_beta']:.4g}", f"{r['loo_gamma']:.4g}", f"{m.beta:.4g}", f"{m.gamma:.4g}"])
    return rep


if __name__ == "__main__":
    rep = write()
    print(rep["model"], f"delta_pred = {rep['delta_pred']:.1f}")
    for r in rep["rows"]:
        print(r)
