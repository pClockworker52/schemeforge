"""Compare the contact judge's `judge exact` answers with the blind audit (model.py).

Inputs: audit/contact/cases/batch_*.yaml and audit/contact/judge/batch_*.json. Output: printed tables and
audit/contact/results.json (per-quantity maxima, worst case ids, and every row above 1e-10 with a diagnosis).

Difference measures: rel = |judge - audit| / |audit|; abs = |judge - audit| where the reference is zero or a
noise-level quantity (stated per row).
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import yaml

import model as m

HERE = Path(__file__).resolve().parent
NEWTON_ATOL = 1e-10  # spec §C0a: Newton's absolute tolerance
TOL = 1e-10

GAP_DEF = dict(gap=0.1, height=1.0, width=0.2, push=0.15, steps=6, nx=1, ny_body=2, ny_medium=2, E=1.0, nu=0.3,
               gamma=1e-6, distort=0.0, seed=0)
SHEAR_DEF = dict(shear=0.5, E=1.0, nu=0.3, gamma=1e-5)
HERTZ_DEF = dict(R=1.0, W=1.0, H=1.0, gap=0.002, push=0.006, steps=12, nx=32, ny=16, ny_medium=4, E=1.0, nu=0.3,
                 gamma=1e-6, kr=5e-7)


class Table:
    """Running max of a difference per quantity, with the worst case and all rows above TOL."""

    def __init__(self):
        self.rows = {}
        self.over = defaultdict(list)
        self.count = defaultdict(int)

    def add(self, q, cid, judge, ref, mode="rel", info=None):
        judge, ref = float(judge), float(ref)
        if mode == "rel":
            d = abs(judge - ref) / abs(ref) if ref != 0 else (0.0 if judge == 0 else math.inf)
        else:
            d = abs(judge - ref)
        self.count[q] += 1
        if q not in self.rows or d > self.rows[q][0] or (math.isnan(d)):
            self.rows[q] = (d, cid, judge, ref, mode)
        if d > TOL or math.isnan(d):
            self.over[q].append(dict(id=cid, diff=d, judge=judge, ref=ref, **(info or {})))

    def print(self, title):
        print(f"\n## {title}")
        print(f"| quantity | measure | n | max diff | worst case | n > 1e-10 |")
        print("|---|---|---|---|---|---|")
        for q, (d, cid, j, r, mode) in self.rows.items():
            print(f"| {q} | {mode} | {self.count[q]} | {d:.2e} | {cid} | {len(self.over[q])} |")

    def as_dict(self):
        return {q: dict(max=v[0], case=v[1], judge=v[2], ref=v[3], measure=v[4], n=self.count[q],
                        n_over=len(self.over[q]), over=self.over[q]) for q, v in self.rows.items()}


def stiffness(case, sm, sb, mu, lmbda):
    """Series stiffnesses (force per displacement) of the body and medium layers at the solution."""
    def dP(s):
        return mu * (1 + 1 / s**2) + lmbda * (1 - math.log(s)) / s**2
    kb = case["width"] * dP(sb) / case["height"]
    km = case["width"] * case["gamma"] * dP(sm) / case["gap"]
    return kb, km


def load_pairs():
    pairs = []
    for cf in sorted((HERE / "cases").glob("batch_*.yaml")):
        jf = HERE / "judge" / (cf.stem + ".json")
        cases = yaml.safe_load(cf.read_text())
        if not jf.exists() or jf.stat().st_size == 0:
            err = (HERE / "judge" / (cf.stem + ".err"))
            print(f"MISSING judge output for {cf.name}: {err.read_text()[-2000:] if err.exists() else ''}")
            continue
        ans = json.loads(jf.read_text())
        assert len(ans) == len(cases), cf
        pairs += list(zip(cases, ans))
    return pairs


def main():
    pairs = load_pairs()
    errors, nonconv = [], []
    T_gx, T_gfe, T_cl, T_sh, T_hz, T_hzJ = Table(), Table(), Table(), Table(), Table(), Table()
    T_gfeR, T_clR, T_leak = Table(), Table(), Table()
    floor = defaultdict(list)
    counts = defaultdict(int)
    for case, ans in pairs:
        cid = case["id"]
        assert ans.get("id") == cid, (cid, ans.get("id"))
        if "error" in ans:
            errors.append(dict(id=cid, error=ans["error"], case=case))
            continue
        kind = case["kind"]
        counts[kind + ("_C1" if kind == "gap_closure" and case.get("distort", 0) > 0 else "")] += 1
        if kind == "gap_closure":
            c = dict(GAP_DEF, **case)
            ex = m.gap_closure_exact(c)
            # judge exact vs audit exact
            for q in ["ideal_force", "exact_force", "exact_thickness", "exact_force_half", "exact_thickness_half",
                      "exact_leak_pre", "exact_gap_res", "exact_force_err"]:
                T_gx.add(q, cid, ans[q], ex[q])
            T_gx.add("exact_force_err (abs)", cid, ans["exact_force_err"], ex["exact_force_err"], "abs")
            # FE vs audit exact
            F, t, sm, sb = m.exact_homogeneous(c["push"], c["gap"], c["height"], c["width"], ex["mu"],
                                               ex["lmbda"], c["gamma"])
            kb, km = stiffness(c, sm, sb, ex["mu"], ex["lmbda"])
            info = dict(force=F, gamma=c["gamma"], distort=c["distort"], s_m=sm, kb=kb, km=km,
                        newton_force_bound=NEWTON_ATOL, newton_thick_bound=NEWTON_ATOL / (kb + km),
                        converged=ans.get("converged"))
            fe_force = ans["fe_force"]
            fe_push = ans["fe_push"]
            T_gfe.add("fe_push (abs)", cid, max(abs(a - b) for a, b in zip(fe_push, ex["steps_push"])), 0.0, "abs")
            if any(v is None or (isinstance(v, float) and math.isnan(v)) for v in fe_force) or \
                    ans.get("fe_converged", 1) == 0:
                nonconv.append(dict(id=cid, case=case))
                continue
            T_gfe.add("fe_force (full push)", cid, fe_force[-1], F, info=info)
            T_gfe.add("fe_force (full push, abs)", cid, fe_force[-1], F, "abs", info=info)
            # every load step against the exact solution at that push (extra), split at |F| = 1e-6 (spec §C0a:
            # below it Newton's absolute tolerance dominates); also against the 1e-10-rounded geometry
            gR, topR = round(c["gap"], 10), round(c["gap"] + c["height"], 10)
            for d, fv in zip(fe_push[1:], fe_force[1:]):
                Fd = m.exact_homogeneous(d, c["gap"], c["height"], c["width"], ex["mu"], ex["lmbda"], c["gamma"])[0]
                FdR = m.exact_homogeneous(d, gR, topR - gR, c["width"], ex["mu"], ex["lmbda"], c["gamma"])[0]
                sinfo = dict(info, push_step=d, force=Fd)
                if abs(Fd) >= 1e-6:
                    T_gfe.add("fe_force (every step, |F| >= 1e-6)", cid, fv, Fd, info=sinfo)
                    T_gfeR.add("fe_force (every step, |F| >= 1e-6)", cid, fv, FdR, info=sinfo)
                else:
                    T_gfe.add("fe_force (every step, |F| < 1e-6, rel)", cid, fv, Fd, info=sinfo)
                    T_gfe.add("fe_force (every step, |F| < 1e-6, abs)", cid, fv, Fd, "abs", info=sinfo)
                    T_gfeR.add("fe_force (every step, |F| < 1e-6, abs)", cid, fv, FdR, "abs", info=sinfo)
            T_gfe.add("fe_thickness", cid, ans["fe_thickness"], t, info=info)
            T_gfe.add("fe_thickness (abs)", cid, ans["fe_thickness"], t, "abs", info=info)
            pw = np.asarray(ans["fe_wall_pressure"], float)
            iw = int(np.argmax(np.abs(pw - F / c["width"])))
            T_gfe.add("fe_wall_pressure vs F/w (worst node)", cid, pw[iw], F / c["width"], info=info)
            T_gfe.add("fe_leak_pre", cid, ans["fe_leak_pre"], ex["exact_leak_pre"], info=info)
            T_gfe.add("fe_gap_res", cid, ans["fe_gap_res"], ex["exact_gap_res"], info=info)
            T_gfe.add("fe_force_err", cid, ans["fe_force_err"], ex["exact_force_err"], info=info)
            T_gfe.add("fe_force_err (abs)", cid, ans["fe_force_err"], ex["exact_force_err"], "abs", info=info)
            T_gfe.add("fe_pressure_spread (abs, exact 0)", cid, ans["fe_pressure_spread"], 0.0, "abs", info=info)
            T_gfe.add("fe_min_J_medium vs s_m", cid, ans["fe_min_J_medium"], sm, info=info)
            # Diagnostic (black box): exact solution on layer boundaries rounded to 10 decimals
            gR, topR = round(c["gap"], 10), round(c["gap"] + c["height"], 10)
            FR, tR, smR, _ = m.exact_homogeneous(c["push"], gR, topR - gR, c["width"], ex["mu"], ex["lmbda"],
                                                 c["gamma"])
            T_gfeR.add("fe_force (full push)", cid, fe_force[-1], FR, info=info)
            T_gfeR.add("fe_force (full push, abs)", cid, fe_force[-1], FR, "abs", info=info)
            T_gfeR.add("fe_thickness", cid, ans["fe_thickness"], tR, info=info)
            T_gfeR.add("fe_thickness (abs)", cid, ans["fe_thickness"], tR, "abs", info=info)
            T_gfeR.add("fe_wall_pressure vs F/w (worst node)", cid, pw[int(np.argmax(np.abs(pw - FR / c["width"])))],
                       FR / c["width"], info=info)
            T_gfeR.add("fe_min_J_medium vs s_m", cid, ans["fe_min_J_medium"], smR, info=info)
            # fe_leak_pre: the spec's F(g/2) vs linear interpolation between load steps
            interp = float(np.interp(0.5 * c["gap"], fe_push, fe_force)) / ex["ideal_force"]
            on_step = any(abs(p_ - 0.5 * c["gap"]) < 1e-12 for p_ in fe_push)
            T_leak.add("fe_leak_pre vs exact F(g/2)/F_ideal" + (" [g/2 on a load step]" if on_step else
                       " [g/2 between steps]"), cid, ans["fe_leak_pre"], ex["exact_leak_pre"], info=info)
            T_leak.add("fe_leak_pre vs lin. interp. of judge fe_force at g/2", cid, ans["fe_leak_pre"], interp,
                       info=info)
            # classical vs ideal at every step
            Fi_full = ex["ideal_force"]
            for d, fv in zip(ans["classical_push"], ans["classical_force"]):
                Fi = m.ideal_force(d, c["gap"], c["height"], c["width"], ex["mu"], ex["lmbda"])
                cinfo = dict(push_step=d, gap=c["gap"], height=c["height"], ideal=Fi, steps=c["steps"], E=c["E"],
                             indent_rel=(d - c["gap"]) / c["height"])
                FiR = m.ideal_force(d, gR, topR - gR, c["width"], ex["mu"], ex["lmbda"])
                if FiR != 0.0:
                    T_clR.add("classical_force, in contact", cid, fv, FiR, info=cinfo)
                if Fi == 0.0:
                    T_cl.add("classical_force, before contact (abs / F_ideal(push))", cid, fv / Fi_full, 0.0,
                             "abs", info=cinfo)
                else:
                    T_cl.add("classical_force, in contact", cid, fv, Fi, info=cinfo)
                    T_cl.add("classical_force, in contact (abs / F_ideal(push))", cid, fv / Fi_full, Fi / Fi_full,
                             "abs", info=cinfo)
        elif kind == "simple_shear":
            c = dict(SHEAR_DEF, **case)
            r = m.simple_shear(c)
            T_sh.add("mu", cid, ans["mu"], r["mu"])
            T_sh.add("lmbda", cid, ans["lmbda"], r["lmbda"])
            T_sh.add("P_xy", cid, ans["P_xy"], r["P_xy"])
            T_sh.add("P_xy vs closed form gamma mu s", cid, ans["P_xy"], r["P_xy_closed"])
            T_sh.add("P_yy (abs, exact 0)", cid, ans["P_yy"], 0.0, "abs")
            T_sh.add("P_yy (abs / (mu s))", cid, ans["P_yy"] / (r["mu"] * c["shear"]), 0.0, "abs")
            T_sh.add("shear_parasitic", cid, ans["shear_parasitic"], r["shear_parasitic"])
            T_sh.add("shear_parasitic vs gamma", cid, ans["shear_parasitic"], c["gamma"])
            T_sh.add("normal_parasitic (abs, exact 0)", cid, ans["normal_parasitic"], 0.0, "abs")
            T_sh.add("audit numeric P_yy/(mu s) (abs; audit round-off)", cid, r["normal_parasitic"], 0.0, "abs")
        elif kind == "hertz":
            c = dict(HERTZ_DEF, **case)
            x, f = np.asarray(ans["x"], float), np.asarray(ans["f"], float)
            r = m.hertz_metrics(x, f, c["R"], c["E"], c["nu"])
            rJ = m.hertz_metrics(x, f, c["R"], c["E"], c["nu"], load=ans["load"])
            hinfo = dict(load=r["load"], load_judge=ans["load"], rel_load=ans["load"] / r["load"] - 1,
                         mid_offset=r["mid_offset"], argmax_p=r["argmax_p"])
            T_hz.add("load: judge vs 2 sum f", cid, ans["load"], r["load"], info=hinfo)
            T_hz.add("load: 2 int p dx vs 2 sum f (audit self-check)", cid, r["load_mass"], r["load"])
            pj = np.asarray(ans["p"], float)
            T_hz.add("p (max abs / max p)", cid, np.abs(pj - r["p"]).max() / np.abs(r["p"]).max(), 0.0, "abs")
            for q in ["E_star", "a_hertz", "p0_hertz", "a_err", "p0_err", "p_l2", "leak_out"]:
                mode = "abs" if q == "leak_out" else "rel"
                lab = q + (" (abs)" if mode == "abs" else "")
                T_hz.add(lab, cid, ans[q], r[q], mode, info=hinfo)
                T_hzJ.add(lab, cid, ans[q], rJ[q], mode, info=hinfo)
            T_hz.add("a_err (abs)", cid, ans["a_err"], r["a_err"], "abs", info=hinfo)
            T_hz.add("p0_err (abs)", cid, ans["p0_err"], r["p0_err"], "abs", info=hinfo)
            T_hz.add("x mid-nodes centred (abs / W)", cid, r["mid_offset"], 0.0, "abs")
            for q in ["a_err", "p0_err", "p_l2", "leak_out"]:
                floor[q].append(ans[q])
            floor["argmax_p"].append(r["argmax_p"])
            floor["p_l2_nodal"].append(r["p_l2_nodal"])
            floor["p_l2_int"].append(r["p_l2_int"])
            floor["leak_out_abs_sum"].append(r["leak_out_abs_sum"])
            floor["p0_err_at0"].append(r["p0_err_at0"])
            floor["nx"].append(c["nx"])

    print("instances answered:", dict(counts), " judge errors:", len(errors), " non-converged FE:", len(nonconv))
    for e in errors:
        print("ERROR", e["id"], str(e["error"])[:300])
    for t, name in [(T_gx, "gap_closure: judge exact vs audit exact"),
                    (T_gfe, "gap_closure: judge FE vs audit exact"),
                    (T_gfeR, "gap_closure DIAGNOSTIC: judge FE vs audit exact on layer boundaries rounded to 1e-10"),
                    (T_leak, "gap_closure: fe_leak_pre"),
                    (T_cl, "gap_closure: judge classical vs audit ideal (every load step)"),
                    (T_clR, "gap_closure DIAGNOSTIC: classical vs ideal on rounded geometry"),
                    (T_sh, "simple_shear: judge vs audit"),
                    (T_hz, "hertz: judge vs audit recomputation from judge x, f (audit load P = 2 sum f)"),
                    (T_hzJ, "hertz: same, audit uses the judge's load")]:
        t.print(name)
    fl = {k: np.asarray(v, float) for k, v in floor.items()}
    if len(fl.get("a_err", [])):
        print("\n## hertz: classical vs Hertz (judge error floor)")
        for q in ["a_err", "p0_err", "p_l2", "leak_out", "p_l2_nodal", "p_l2_int", "p0_err_at0", "leak_out_abs_sum"]:
            v = fl[q]
            print(f"{q}: min {v.min():+.4e} median {np.median(v):+.4e} max {v.max():+.4e}")
        print("argmax p index values:", sorted(set(fl["argmax_p"].astype(int).tolist())))
    res = dict(counts=dict(counts), errors=errors, nonconverged=nonconv,
               gap_exact=T_gx.as_dict(), gap_fe=T_gfe.as_dict(), gap_fe_rounded=T_gfeR.as_dict(),
               leak=T_leak.as_dict(), classical_rounded=T_clR.as_dict(), classical=T_cl.as_dict(), shear=T_sh.as_dict(),
               hertz=T_hz.as_dict(), hertz_judge_load=T_hzJ.as_dict(),
               hertz_floor={k: dict(min=float(v.min()), median=float(np.median(v)), max=float(v.max()))
                            for k, v in fl.items()})
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=float))


if __name__ == "__main__":
    main()
