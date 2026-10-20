"""Compare audit exact solutions with the judge's `sforge judge exact` output.

Usage: uv run python audit/euler1d/compare.py
Reads audit/euler1d/cases/*.yaml and audit/euler1d/judge_out/*.json (same basename).
Relative difference: |a - b| / max(|a|, |b|, floor). floor = 0 except for velocity-like
quantities (u_star, wave speeds, sampled u), where floor = max(|u_K| + a_K) of the case,
reported separately as 'rel (no floor)' too.
"""

from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import exact  # noqa: E402

HERE = Path(__file__).parent
THRESH = 1e-10


def rel(a, b, floor=0.0):
    if a is None or b is None:
        return 0.0 if a is None and b is None else math.inf
    d = abs(a - b)
    if d == 0.0:
        return 0.0
    return d / max(abs(a), abs(b), floor)


def main() -> None:
    mx = defaultdict(float)
    mx_nofloor = defaultdict(float)
    worst = {}
    flagged = []
    counts = defaultdict(int)
    for cf in sorted((HERE / "cases").glob("*.yaml")):
        cases = yaml.safe_load(cf.read_text())
        judge = json.loads((HERE / "judge_out" / (cf.stem + ".json")).read_text())
        assert len(cases) == len(judge), cf
        for c, j in zip(cases, judge, strict=False):
            a = exact.solve(c)
            counts[c["kind"]] += 1
            diffs = {}
            if c["kind"] == "riemann":
                g = c["gamma"]
                vs = max(abs(s[1]) + math.sqrt(g * s[2] / s[0]) for s in (c["left"], c["right"]))
                for k in ("p_star", "rho_star_L", "rho_star_R"):
                    diffs[k] = (rel(a[k], j[k]), rel(a[k], j[k]))
                diffs["u_star"] = (rel(a["u_star"], j["u_star"], vs), rel(a["u_star"], j["u_star"]))
                kinds_ok = [w["kind"] for w in a["waves"]] == [w["kind"] for w in j["waves"]]
                diffs["wave_kinds"] = (0.0 if kinds_ok else math.inf,) * 2
                for wa, wj in zip(a["waves"], j["waves"], strict=False):
                    for sa, sj in zip(wa["speeds"], wj["speeds"], strict=False):
                        diffs.setdefault("wave_speeds", (0.0, 0.0))
                        diffs["wave_speeds"] = (max(diffs["wave_speeds"][0], rel(sa, sj, vs)),
                                                max(diffs["wave_speeds"][1], rel(sa, sj)))
                fl = {"rho": 0.0, "u": vs, "p": 0.0, "x": 1.0}
            else:
                diffs["regime"] = ((0.0 if a["regime"] == j["regime"] else math.inf),) * 2
                for k in ("x_shock", "M1", "p0_ratio", "A_star_1", "A_star_2", "mass_flow",
                          "p_crit1", "p_crit2", "p_crit3"):
                    r = rel(a[k], j[k])
                    diffs[k] = (r, r)
                fl = {"M": 0.0, "rho": 0.0, "u": 0.0, "p": 0.0, "x": 1.0}
            for k, f in fl.items():
                worst_f = worst_nf = 0.0
                arg = None
                for i, (va, vj) in enumerate(zip(a[k], j[k], strict=False)):
                    r = rel(va, vj, f)
                    if r > worst_f:
                        worst_f, arg = r, i
                    worst_nf = max(worst_nf, rel(va, vj))
                if len(a[k]) != len(j[k]):
                    worst_f = worst_nf = math.inf
                diffs["profile_" + k] = (worst_f, worst_nf)
                if worst_f > THRESH:
                    flagged.append((c["id"], "profile_" + k, worst_f, arg, a[k][arg], j[k][arg],
                                    a["x"][arg]))
            prefix = c["kind"][0].upper() + ":"
            for k, (r, rn) in diffs.items():
                key = prefix + k
                if r > mx[key]:
                    mx[key] = r
                    worst[key] = c["id"]
                mx_nofloor[key] = max(mx_nofloor[key], rn)
                if r > THRESH and not k.startswith("profile_"):
                    flagged.append((c["id"], k, r, None, a.get(k), j.get(k), None))
    print("counts", dict(counts))
    print(f"{'quantity':28s} {'max rel':>10s} {'no floor':>10s}  worst case")
    for k in sorted(mx_nofloor):
        print(f"{k:28s} {mx[k]:10.3e} {mx_nofloor[k]:10.3e}  {worst.get(k, '-')}")
    print(f"\nflagged > {THRESH}: {len(flagged)}")
    for fl_ in flagged:
        print(fl_)


if __name__ == "__main__":
    main()
