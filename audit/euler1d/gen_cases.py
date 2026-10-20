"""Random admissible instance generator for the euler1d blind audit.

Usage: uv run python audit/euler1d/gen_cases.py [SEED]
Writes audit/euler1d/cases/{riemann,nozzle}_NN.yaml (YAML lists, case format of
docs/judge/euler1d_cases.md). Seed default 20261020.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).parent))
import exact  # noqa: E402

HERE = Path(__file__).parent
GAMMAS = [1.4, 5.0 / 3.0, 1.405, 1.2]
BATCH = 200


def riemann_cases(rng: np.random.Generator, n_cases: int) -> list[dict]:
    out = []
    while len(out) < n_cases:
        g = GAMMAS[rng.integers(4)]
        rl, rr = 10.0 ** rng.uniform(-1, 1, 2)
        pl, pr = 10.0 ** rng.uniform(-3, 3, 2)
        al, ar = math.sqrt(g * pl / rl), math.sqrt(g * pr / rr)
        ul = rng.uniform(-1, 1) * al
        ur = rng.uniform(-1, 1) * ar
        if 2.0 / (g - 1.0) * (al + ar) <= ur - ul:
            continue
        x0 = rng.uniform(0.3, 0.7)
        sol = exact.riemann_star((rl, ul, pl), (rr, ur, pr), g)
        smin = min(sol.waves[0][2])
        smax = max(sol.waves[1][2])
        tmax = math.inf
        if smax > 0:
            tmax = min(tmax, (1.0 - x0) / smax)
        if smin < 0:
            tmax = min(tmax, x0 / -smin)
        t_end = tmax * rng.uniform(0.3, 0.95)
        out.append({
            "kind": "riemann", "id": f"A-R{len(out):04d}",
            "left": [float(rl), float(ul), float(pl)],
            "right": [float(rr), float(ur), float(pr)],
            "t_end": float(t_end), "n": 50, "gamma": float(g), "x0": float(x0),
        })
    return out


def nozzle_cases(rng: np.random.Generator, n_cases: int) -> list[dict]:
    out = []
    regimes = ["subsonic", "shock", "supersonic"]
    for i in range(n_cases):
        g = GAMMAS[rng.integers(4)]
        kind = ["anderson", "parabolic", "conical"][i % 3]
        if kind == "anderson":
            noz = {"type": "anderson"}
        else:
            noz = {"type": kind,
                   "area_ratio": float(rng.uniform(2, 10)),
                   "length": float(rng.uniform(2, 4)),
                   "inlet_ratio": float(rng.uniform(1.5, 3))}
            if rng.uniform() < 0.5:
                noz["x_in"] = float(rng.uniform(-0.5, 0.5))
        geo = exact.make_geometry(noz)
        er = geo.area(geo.x_exit) / geo.A_t
        me_sub = exact.mach_from_area(er, g, False)
        me_sup = exact.mach_from_area(er, g, True)
        pc1 = exact.p_ratio(me_sub, g)
        pc3 = exact.p_ratio(me_sup, g)
        pc2 = pc3 * exact.shock_p_jump(me_sup, g)
        reg = regimes[(i // 3) % 3]
        if reg == "subsonic":
            pb = pc1 + (1.0 - pc1) * rng.uniform(0.02, 0.98)
        elif reg == "shock":
            pb = pc2 + (pc1 - pc2) * rng.uniform(0.01, 0.99)
        else:
            pb = pc2 * rng.uniform(0.02, 0.98)
        out.append({"kind": "nozzle", "id": f"A-N{i:04d}", "pb": float(pb), "n": 40,
                    "gamma": float(g), "nozzle": noz})
    return out


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261020
    rng = np.random.default_rng(seed)
    rc = riemann_cases(rng, 600)
    nc = nozzle_cases(rng, 402)
    d = HERE / "cases"
    d.mkdir(exist_ok=True)
    for k in range(0, len(rc), BATCH):
        (d / f"riemann_{k // BATCH:02d}.yaml").write_text(yaml.safe_dump(rc[k:k + BATCH]))
    for k in range(0, len(nc), BATCH):
        (d / f"nozzle_{k // BATCH:02d}.yaml").write_text(yaml.safe_dump(nc[k:k + BATCH]))
    print(len(rc), len(nc))


if __name__ == "__main__":
    main()
