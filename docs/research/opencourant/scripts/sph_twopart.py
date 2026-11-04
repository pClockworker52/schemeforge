"""Do two SPH parts interact through the kernel (welded) in OpenCourant? Striker column of length L (part 1, speed
-V) onto a target column of length 2L (part 2, at rest), lateral motion blocked and four lateral /SPHBCS/SLIDE
planes, free ends, rung-0 material (E = 70 GPa, nu = 0.35, rho = 2700, L = 10 um, V = 100 m/s), h = 1.12 s.

Exact 1D (separable contact): the striker stops at t = 2L/c_d and stays at rest; the gap then only grows (the
target's near end moves at V or 0, never back). A kernel coupling between the parts instead lets the target pull
the striker along (tension across the interface).

Usage: python sph_twopart.py <work_dir> <out_csv> [n_z]
"""

import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ocdeck as oc  # noqa: E402
import sph_rung0 as s0  # noqa: E402
import sphdeck as sd  # noqa: E402


def main(work, out_csv, n_z=50):
    n_z = int(n_z)
    s = s0.L / n_z
    w = 4 * s
    tgt = sd.cubic_net((0, 0, 0), (w, w, 2 * s0.L), s)
    stk = sd.cubic_net((0, 0, 2 * s0.L), (w, w, 3 * s0.L), s)
    mat = oc.Elastic(s0.E, s0.NU, s0.RHO)
    prop = sd.SphProp(h=2 ** (1 / 6) * s)
    b1 = sd.Body(stk, s0.RHO * s**3, mat, prop, velocity=(0, 0, -s0.V), title="striker", fix="110")
    b2 = sd.Body(tgt, s0.RHO * s**3, mat, prop, title="target", fix="110")
    sym = [sd.SymPlane((0, 0, 0), (1, 0, 0)), sd.SymPlane((w, 0, 0), (-1, 0, 0)),
           sd.SymPlane((0, 0, 0), (0, 1, 0)), sd.SymPlane((0, w, 0), (0, -1, 0))]
    name = f"TP{n_z:03d}"
    d = os.path.join(work, name)
    sd.write_deck(d, name, [b1, b2], t_end=4 * s0.T_C, dt_th=s0.T_C / 400, sym=sym, dt_scale=0.3)
    res = sd.run(d, name, threads=2)
    assert res.get("normal"), res
    head, a = oc.read_th(d, name)
    t = a[:, 0] / s0.T_C
    zm = {h.split()[0]: a[:, i] for i, h in enumerate(head) if h.endswith("ZMOM")}
    v1 = zm["striker"] / (len(stk) * s0.RHO * s**3) / s0.V
    v2 = zm["target"] / (len(tgt) * s0.RHO * s**3) / s0.V
    rows = []
    for tt in (0.5, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0):
        k = int(np.argmin(abs(t - tt)))
        rows.append({"t_over_2L_cd": round(float(t[k]), 3), "striker_v_over_V": round(float(v1[k]), 4),
                     "target_mean_v_over_V": round(float(v2[k]), 4)})
        print(rows[-1])
    with open(out_csv, "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)


if __name__ == "__main__":
    main(*sys.argv[1:4])
