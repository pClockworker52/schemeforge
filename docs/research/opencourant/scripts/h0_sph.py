"""CS-13b prerequisite rung H0-SPH: heat conduction alone in SPH particles, 1D temperature step, against erfc.

The H0 slab of h0_conduction.py (opencourant-verification.md §11.2) built from SPH particles: a column
0 <= x, y <= W (W = 12 s), 0 <= z <= L (L = 20 um), cubic net of spacing s, §9.1 settings (h = 2^(1/6) s, mass in
/PROP/TYPE34 only, dt scale 0.3), every particle fixed (/BCS 111), no symmetry planes (the lateral faces are free;
the measured line is the particle column nearest the centre, 6 s = 2.7 kernel supports from them). Initial nodal
temperature T1 for z < L/2 and T0 for z > L/2 (the cubic net has no particle at L/2). The step is set as two SPH
parts, hot (z < L/2) and cold, each with its own /HEAT/MAT whose T0 is that temperature: with thermal analysis on,
the starter sets every SPH particle's temperature to its /HEAT/MAT T0 and ignores /INITEMP (starter spinit3.F,
"INITIALISATION OF THERMAL BEHAVIOR"). The two parts are the same material, and SPH particles of different parts
interact through the kernel as one body (sphdeck.py), the conduction loop included (engine sptemp.F, no part filter).
Exact (infinite medium): T(z, t) = T0 + (T1 - T0)/2 erfc((z - L/2) / (2 sqrt(kappa t))), kappa = k / (rho c_p).

Material: Al LAW4 + Grueneisen (option1_alal.AL, P-HG-Al) + /HEAT/MAT (rho c_p from P-HG-Al, AS = k = 237 W/(m K),
P-HG-Al k_W_mK); engine /THERMAL. Output: /TH/NODE TEMP on the centre column, /ANIM/NODA/TEMP, /ANIM/ELEM/TEMP.
Metric: max over the centre column |T - T_exact| / (T1 - T0) at t_end = 10 ns; pass (frozen, CS-13b): within 2 %
at the finest spacing, with the temperature written out.

Usage: python h0_sph.py <work_dir> <out_csv> <s_um> [...]
"""

import csv
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import h0_conduction as h0  # noqa: E402
import ocdeck as oc  # noqa: E402
import option1_alal as o1  # noqa: E402
import sphdeck as sd  # noqa: E402
from ocdeck import _f, _i  # noqa: E402

L, T0, T1, K_AL, RHO_CP, KAPPA, T_END = h0.L, h0.T0, h0.T1, h0.K_AL, h0.RHO_CP, h0.KAPPA, h0.T_END
N_W = 12  # column width in spacings


def heat_cards(mat_id, t_init=T0, k=K_AL, t_melt=0.0):
    """/HEAT/MAT for material mat_id: T0 = t_init, rho c_p, AS = k, BS = 0; T1 = t_melt, AL = BL = 0, EFRAC = 1.

    T1 matters whenever the material softens with temperature: with /HEAT/MAT the Johnson-Cook T* is
    (T - T_ref) / (T1 - T_ref) (engine mmain.F90), and T1 = 0 is read as 1e20, which switches thermal softening
    off. Pure conduction rungs (H0) do not depend on it."""
    return [f"/HEAT/MAT/{mat_id}", _f(t_init) + _f(RHO_CP) + _f(k) + _f(0.0),
            _f(t_melt) + _f(0.0) + _f(0.0) + _f(1.0)]


def write(d, name, s):
    p = sd.cubic_net((0.0, 0.0, 0.0), (N_W * s, N_W * s, L), s)
    hot = p[:, 2] < L / 2
    p = np.concatenate([p[hot], p[~hot]])  # node ids: hot part first (part 1), then cold (part 2)
    prop = sd.SphProp(h=2 ** (1 / 6) * s)
    bodies = [sd.Body(xyz=p[: hot.sum()], mass=o1.AL.rho * s**3, mat=o1.AL, prop=prop, title="hot", fix="111"),
              sd.Body(xyz=p[hot.sum():], mass=o1.AL.rho * s**3, mat=o1.AL, prop=prop, title="cold", fix="111")]
    ids = np.arange(1, len(p) + 1)
    extra = heat_cards(1, T1) + heat_cards(2, T0)
    c = (N_W // 2 - 0.5) * s  # particle centre nearest the column axis
    line = ids[(np.abs(p[:, 0] - c) < 1e-3 * s) & (np.abs(p[:, 1] - c) < 1e-3 * s)]
    line = line[np.argsort(p[line - 1, 2])]
    extra += ["/TH/NODE/5", "centre column", f"{'TEMP':<10}"] + [_i(int(k)) + _i(0) for k in line]
    sd.write_deck(d, name, bodies, t_end=T_END, dt_th=T_END / 20, dt_scale=0.3, dt_anim=T_END / 2, anim=("TEMP",),
                  extra_starter=extra, extra_engine=["/THERMAL", _f(1.0), "/ANIM/NODA/TEMP"])
    return p[line - 1, 2], len(p)


def run_case(work, s_um, threads):
    s = s_um * 1e-6
    name = f"HS{int(round(s_um * 1000)):04d}"
    d = os.path.join(work, name)
    z, n = write(d, name, s)
    t0 = time.perf_counter()
    res = sd.run(d, name, threads=threads)
    row = {"name": name, "element": "sph", "s_um": s_um, "particles": n, "normal": res.get("normal")}
    if not res.get("normal"):
        row["failed"] = " ".join((res.get("engine_tail") or res.get("starter_tail", "")).split())[-300:]
        return row
    head, a = oc.read_th(d, name)
    cols = [i for i, hh in enumerate(head) if hh.endswith("TEMP")]
    T, t = a[-1, cols], a[-1, 0]
    Te = h0.exact(z, t)
    err = np.abs(T - Te) / (T1 - T0)
    row.update({"t_end_ns": t * 1e9, "n_line": len(cols), "T_min": float(T.min()), "T_max": float(T.max()),
                "max_err_over_dT": float(err.max()), "max_dT_run_K": float(np.abs(a[-1, cols] - a[0, cols]).max()),
                "l_th_um": math.sqrt(KAPPA * t) * 1e6, "engine_s": res.get("engine_s"),
                "wall_s": time.perf_counter() - t0})
    np.save(os.path.join(d, "profile.npy"), {"z": z, "T": T, "T_exact": Te, "t": t, "T_hist": a[:, cols],
                                             "t_hist": a[:, 0]}, allow_pickle=True)
    return row


def main():
    work, out_csv = sys.argv[1:3]
    threads = int(os.environ.get("THREADS", "8"))
    rows = list(csv.DictReader(open(out_csv))) if os.path.exists(out_csv) else []
    for s_um in [float(x) for x in sys.argv[3:]]:
        row = run_case(work, s_um, threads)
        print({k: (round(x, 5) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
        rows.append(row)
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with open(out_csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    main()
