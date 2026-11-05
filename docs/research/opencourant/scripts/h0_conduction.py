"""CS-13 prerequisite rung H0: heat conduction alone, 1D slab with an initial temperature step, against erfc.

Bar 0 <= z <= L (L = 20 um), one element across, all nodes fixed (no motion), initial nodal temperature T1 for
z < L/2 and T0 for z > L/2 (the node at L/2 gets the mean). Exact (infinite medium, valid while the front is far
from the insulated ends): T(z, t) = T0 + (T1 - T0)/2 erfc((z - L/2) / (2 sqrt(kappa t))), kappa = k / (rho c_p).

Material: Al, LAW4 Johnson-Cook + /EOS/GRUNEISEN (option1_alal.AL, P-HG-Al) + /HEAT/MAT with rho c_p from P-HG-Al
and conductivity AS = k = 237 W/(m K) (P-HG-Al, properties.csv); engine /THERMAL. Element:
  quad   2D axisymmetric (/ANALY N2D3D = 1), /QUAD with Isolid = 17 (the CS-13 element), mesh r in [0, h];
  brick  3D /BRICK Isolid = 17, cross-section h x h (control: shows whether the deck and the card work).
Output: /TH/NODE TEMP on the nodes of one edge (r = 0 or x = y = 0), /ANIM/NODA/TEMP and /ANIM/ELEM/TEMP.
Metric: max over nodes |T - T_exact| / (T1 - T0) at t_end; pass (frozen, CS-13): within 2 % at the finest spacing,
and the temperature written out.

Usage: python h0_conduction.py <work_dir> <out_csv> <quad|brick> <h_um> [...]
"""

import csv
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ocdeck as oc  # noqa: E402
import option1_alal as o1  # noqa: E402
from ocdeck import _f, _group, _i, _material_cards  # noqa: E402

L = 20e-6
T0, T1 = 293.0, 393.0
K_AL = 237.0  # W/(m K), properties.csv P-HG-Al (HG2018a preprint, Extended Data Table 1)
RHO_CP = o1.AL.rho_cp  # 2700 * 896.9, P-HG-Al
KAPPA = K_AL / RHO_CP
T_END = 10e-9


def exact(z, t):
    from math import erfc
    return np.array([T0 + 0.5 * (T1 - T0) * erfc((zz - L / 2) / (2 * math.sqrt(KAPPA * t))) for zz in z])


def write(d, name, elem, h):
    nz = int(round(L / h))
    z = np.linspace(0, L, nz + 1)
    s = ["#RADIOSS STARTER", f"# CS-13 rung H0, written by h0_conduction.py: {name}", "/BEGIN", name, _i(2026) + _i(0),
         f"{'kg':>20}{'m':>20}{'s':>20}", f"{'kg':>20}{'m':>20}{'s':>20}"]
    if elem == "quad":
        s += ["/ANALY", _i(1) + _i(0) + _i(0)]
        lat = [(0.0, 0.0), (0.0, h)]  # (x, y=r)
    else:
        lat = [(0.0, 0.0), (h, 0.0), (h, h), (0.0, h)]
    nl = len(lat)
    s += ["/NODE"]
    xyz = []
    for k, zz in enumerate(z):
        for j, (x, y) in enumerate(lat):
            xyz.append((x, y, zz))
            s.append(_i(k * nl + j + 1) + _f(x) + _f(y) + _f(zz))
    xyz = np.array(xyz)
    if elem == "quad":  # counter-clockwise in (r, z): (r0,z0) (r1,z0) (r1,z1) (r0,z1)
        s += ["/QUAD/1"] + [_i(k + 1) + "".join(_i(x) for x in (k * nl + 1, k * nl + 2, (k + 1) * nl + 2,
                                                                (k + 1) * nl + 1)) for k in range(nz)]
    else:
        s += ["/BRICK/1"] + [_i(k + 1) + "".join(_i(k * nl + j + 1) for j in range(4))
                             + "".join(_i((k + 1) * nl + j + 1) for j in range(4)) for k in range(nz)]
    s += ["/PART/1", "slab", _i(1) + _i(1) + _i(0)]
    s += ["/PROP/TYPE14/1", "slab solid", _i(17) + _i(0) * 7 + _f(0.0), _f(0.0) * 5, _f(0.0) * 5, _i(0) * 3]
    s += _material_cards(o1.AL)
    s += ["/HEAT/MAT/1", _f(T0) + _f(RHO_CP) + _f(K_AL) + _f(0.0), _f(0.0) + _f(0.0) + _f(0.0) + _f(1.0)]
    all_ids = range(1, len(xyz) + 1)
    s += _group(1, "all nodes", all_ids) + ["/BCS/1", "all fixed", "   111 000" + _i(0) + _i(1)]
    hot = [i + 1 for i, p in enumerate(xyz) if p[2] < L / 2 - 1e-3 * h]
    cold = [i + 1 for i, p in enumerate(xyz) if p[2] > L / 2 + 1e-3 * h]
    mid = [i + 1 for i, p in enumerate(xyz) if abs(p[2] - L / 2) <= 1e-3 * h]
    for gid, ids, temp in ((2, hot, T1), (3, cold, T0), (4, mid, 0.5 * (T0 + T1))):
        s += _group(gid, f"T {temp}", ids) + [f"/INITEMP/{gid}", f"initial T {temp}", _f(temp) + _i(gid)]
    edge = [k * nl + 1 for k in range(nz + 1)]
    s += ["/TH/NODE/1", "edge nodes", f"{'TEMP':<10}"] + [_i(k) + _i(0) for k in edge]
    s += ["/END"]
    e = ["#RADIOSS ENGINE", f"/RUN/{name}/1", _f(T_END), "/TFILE/4", _f(T_END / 20), "/TH/TITLE", "/PRINT/-100",
         "/THERMAL", _f(1.0), "/ANIM/DT", _f(0.0) + _f(T_END / 2), "/ANIM/NODA/TEMP", "/ANIM/ELEM/TEMP"]
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f"{name}_0000.rad"), "w").write("\n".join(s) + "\n")
    open(os.path.join(d, f"{name}_0001.rad"), "w").write("\n".join(e) + "\n")
    return z, edge


def run_case(work, elem, h_um):
    h = h_um * 1e-6
    name = f"H0{elem[0]}{int(round(h_um * 1000)):04d}"
    d = os.path.join(work, name)
    z, edge = write(d, name, elem, h)
    t0 = time.perf_counter()
    res = oc.run(d, name)
    row = {"name": name, "element": elem, "h_um": h_um, "nz": len(z) - 1, "normal": res.get("normal")}
    if not res.get("normal"):
        row["failed"] = " ".join(res.get("engine_tail", res.get("starter_tail", "")).split())[-300:]
        return row
    head, a = oc.read_th(d, name)
    cols = [i for i, hh in enumerate(head) if hh.endswith("TEMP")]
    T = a[-1, cols]
    t = a[-1, 0]
    Te = exact(z, t)
    err = np.abs(T - Te) / (T1 - T0)
    row.update({"t_end_ns": t * 1e9, "T_min": float(T.min()), "T_max": float(T.max()),
                "T_at_quarter": float(T[len(z) // 4]), "max_err_over_dT": float(err.max()),
                "max_err_central_over_dT": float(err[np.abs(z - L / 2) < 4 * math.sqrt(KAPPA * t)].max()),
                "l_th_um": math.sqrt(KAPPA * t) * 1e6, "engine_s": res.get("engine_s"),
                "wall_s": time.perf_counter() - t0})
    np.save(os.path.join(d, "profile.npy"), {"z": z, "T": T, "T_exact": Te, "t": t,
                                             "T_hist": a[:, cols], "t_hist": a[:, 0]}, allow_pickle=True)
    return row


def main():
    work, out_csv, elem = sys.argv[1:4]
    rows = list(csv.DictReader(open(out_csv))) if os.path.exists(out_csv) else []
    for h in [float(x) for x in sys.argv[4:]]:
        row = run_case(work, elem, h)
        print({k: (round(x, 5) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
        rows.append(row)
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with open(out_csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    main()
