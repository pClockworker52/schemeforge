"""Probe the judge ulp by ulp around p_crit1 and p_crit2 (targeted extra cases).

Usage: uv run python audit/euler1d/probe_crit.py
"""
import json
import math
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import exact  # noqa: E402

D = Path(__file__).parent / "cases_edge" / "probe"
D.mkdir(exist_ok=True, parents=True)


def judge(c):
    c = {"id": "P-0001", **c}
    f = D / "p.yaml"
    f.write_text(yaml.safe_dump(c))
    r = subprocess.run(["uv", "run", "sforge", "judge", "exact", "--arena", "euler1d", "--case", str(f),
                        "--json"], capture_output=True, text=True)
    if r.returncode:
        return {"error": (r.stdout + r.stderr).strip()}
    v = json.loads(r.stdout)
    return v[0] if isinstance(v, list) else v


GEOS = [({"type": "anderson"}, 1.4),
        ({"type": "parabolic", "area_ratio": 4.0, "length": 3.0, "inlet_ratio": 2.0}, 1.2),
        ({"type": "conical", "area_ratio": 6.0, "length": 2.5, "inlet_ratio": 2.5}, 5 / 3)]

for geo, g in GEOS:
    base = judge({"kind": "nozzle", "pb": 0.5, "n": 4, "gamma": g, "nozzle": geo})
    a = exact.nozzle_case({"pb": 0.5, "n": 4, "gamma": g, "nozzle": geo})
    print(geo["type"], g, "judge pc1, pc2", repr(base["p_crit1"]), repr(base["p_crit2"]),
          "| audit", repr(a["p_crit1"]), repr(a["p_crit2"]))
    for name in ("p_crit1", "p_crit2"):
        pc = base[name]
        for k in (-2, -1, 0, 1, 2, 4, 16, 64, 1024, 2**20):
            pb = pc
            for _ in range(min(abs(k), 2000)):
                pb = math.nextafter(pb, 2.0 if k > 0 else -1.0)
            if abs(k) > 2000:
                pb = pc * (1 + k * 2.2e-16)
            j = judge({"kind": "nozzle", "pb": pb, "n": 40, "gamma": g, "nozzle": geo})
            au = exact.nozzle_case({"pb": pb, "n": 40, "gamma": g, "nozzle": geo})
            print(f"  {name} {k:+d} ulp  judge:", j.get("error") or (j["regime"], j["x_shock"], j["M1"]),
                  " audit:", (au["regime"], au["x_shock"], au["M1"]))
