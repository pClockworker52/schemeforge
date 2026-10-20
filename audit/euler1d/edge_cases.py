"""Targeted edge cases for the euler1d blind audit (ties, boundaries of regimes).

Usage: uv run python audit/euler1d/edge_cases.py write   -> audit/euler1d/cases_edge/edge.yaml
       (run the judge on it into audit/euler1d/judge_out_edge/edge.json)
       uv run python audit/euler1d/edge_cases.py compare
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import exact  # noqa: E402

HERE = Path(__file__).parent

CASES = [
    # stationary contact exactly on a cell centre (x0 = 0.55, n = 10): spec -> right star state
    {"kind": "riemann", "id": "E-R01", "left": [1.4, 0.0, 1.0], "right": [1.0, 0.0, 1.0],
     "t_end": 0.1, "n": 10, "x0": 0.55},
    # identical states (no waves at all)
    {"kind": "riemann", "id": "E-R02", "left": [1.0, 0.3, 1.0], "right": [1.0, 0.3, 1.0],
     "t_end": 0.1, "n": 10},
    # moving pure contact, u = 0.5, t = 0.1: contact at 0.55 + 0.05 = 0.6 ... (x0=0.5 -> 0.55)
    {"kind": "riemann", "id": "E-R03", "left": [2.0, 0.5, 1.0], "right": [0.5, 0.5, 1.0],
     "t_end": 0.1, "n": 10},
    # rarefaction head exactly on a centre: rho = 1.4, p = 1 -> a = 1, head at x0 - t
    {"kind": "riemann", "id": "E-R04", "left": [1.4, 0.0, 1.0], "right": [0.125, 0.0, 0.1],
     "t_end": 0.25, "n": 10, "x0": 0.5},
    # Toro test 2 (123), symmetric: u* = 0 at x = 0.5 = face; n = 11 puts a centre at 0.5
    {"kind": "riemann", "id": "E-R05", "left": [1.0, -2.0, 0.4], "right": [1.0, 2.0, 0.4],
     "t_end": 0.15, "n": 11},
    # extreme ratios at the edge of the generator ranges
    {"kind": "riemann", "id": "E-R06", "left": [0.1, 0.0, 1000.0], "right": [10.0, 0.0, 0.001],
     "t_end": 0.004, "n": 50, "gamma": 1.2},
    {"kind": "riemann", "id": "E-R07", "left": [10.0, 0.0, 0.001], "right": [0.1, 0.0, 1000.0],
     "t_end": 0.004, "n": 50, "gamma": 1.6666666666666667},
    # throat exactly on a cell centre: x_in = 0.25, L = 2.75, n = 7 -> dx = 0.5, centre 1.0
    {"kind": "nozzle", "id": "E-N01", "pb": 0.5, "n": 7, "gamma": 1.4,
     "nozzle": {"type": "parabolic", "area_ratio": 4.0, "length": 2.75, "inlet_ratio": 2.0,
                "x_in": 0.25}},
    {"kind": "nozzle", "id": "E-N02", "pb": 0.01, "n": 7, "gamma": 1.4,
     "nozzle": {"type": "conical", "area_ratio": 4.0, "length": 2.75, "inlet_ratio": 2.0,
                "x_in": 0.25}},
    {"kind": "nozzle", "id": "E-N03", "pb": 0.999, "n": 7, "gamma": 1.4,
     "nozzle": {"type": "parabolic", "area_ratio": 4.0, "length": 2.75, "inlet_ratio": 2.0,
                "x_in": 0.25}},
    # very weak subsonic flow
    {"kind": "nozzle", "id": "E-N04", "pb": 0.9999999, "n": 40, "gamma": 1.4},
    # extreme parameters inside the generator ranges
    {"kind": "nozzle", "id": "E-N05", "pb": 0.0005, "n": 40, "gamma": 1.2,
     "nozzle": {"type": "conical", "area_ratio": 10.0, "length": 4.0, "inlet_ratio": 3.0}},
    {"kind": "nozzle", "id": "E-N06", "pb": 0.9, "n": 40, "gamma": 1.6666666666666667,
     "nozzle": {"type": "parabolic", "area_ratio": 2.0, "length": 2.0, "inlet_ratio": 1.5}},
]


def boundary_cases() -> list[dict]:
    """pb exactly at p_crit1 / p_crit2 / p_crit3 (audit values; judge values agree to ~1 ulp)."""
    out = []
    for k, (geo, g) in enumerate([({"type": "anderson"}, 1.4),
                                  ({"type": "parabolic", "area_ratio": 4.0, "length": 3.0,
                                    "inlet_ratio": 2.0}, 1.2),
                                  ({"type": "conical", "area_ratio": 6.0, "length": 2.5,
                                    "inlet_ratio": 2.5}, 5 / 3)]):
        base = exact.nozzle_case({"pb": 0.5, "n": 4, "gamma": g, "nozzle": geo})
        for name in ("p_crit1", "p_crit2", "p_crit3"):
            out.append({"kind": "nozzle", "id": f"E-B{k}{name[-1]}", "pb": base[name], "n": 40,
                        "gamma": g, "nozzle": geo})
    return out


def main() -> None:
    cases = CASES + boundary_cases()
    if sys.argv[1] == "write":
        (HERE / "cases_edge").mkdir(exist_ok=True)
        (HERE / "cases_edge" / "edge.yaml").write_text(yaml.safe_dump(cases))
        return
    judge = json.loads((HERE / "judge_out_edge" / "edge.json").read_text())
    scalars = ["p_star", "u_star", "rho_star_L", "rho_star_R", "regime", "x_shock", "M1",
               "p0_ratio", "A_star_1", "A_star_2", "mass_flow", "p_crit1", "p_crit2", "p_crit3"]
    for c, j in zip(cases, judge, strict=False):
        if "error" in j or "kind" not in j:
            print(c["id"], "JUDGE:", j)
            continue
        try:
            a = exact.solve(c)
        except Exception as e:  # noqa: BLE001
            print(c["id"], "AUDIT ERROR", e, "| judge:", {k: j.get(k) for k in scalars if k in j})
            continue
        msgs = []
        for k in scalars:
            if k in a and a[k] != j.get(k):
                va, vj = a[k], j.get(k)
                if isinstance(va, float) and isinstance(vj, float):
                    r = abs(va - vj) / max(abs(va), abs(vj))
                    if r > 1e-12:
                        msgs.append(f"{k}: audit {va!r} judge {vj!r} rel {r:.2e}")
                else:
                    msgs.append(f"{k}: audit {va!r} judge {vj!r}")
        if c["kind"] == "riemann":
            if [w["kind"] for w in a["waves"]] != [w["kind"] for w in j["waves"]]:
                msgs.append(f"waves: audit {a['waves']} judge {j['waves']}")
        for q in (["rho", "u", "p"] + (["M"] if c["kind"] == "nozzle" else [])):
            for i, (va, vj) in enumerate(zip(a[q], j[q], strict=False)):
                d = abs(va - vj) / max(abs(va), abs(vj), 1e-300)
                if d > 1e-12:
                    msgs.append(f"{q}[{i}] x={a['x'][i]!r}/{j['x'][i]!r}: audit {va!r} judge {vj!r}")
        print(c["id"], "OK" if not msgs else "")
        for m in msgs:
            print("   ", m)


if __name__ == "__main__":
    main()
