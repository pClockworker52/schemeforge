"""Exact temperature check for LAW4: with a constant yield stress (JC with B = C = 0) every element must heat by
dT = A * eps_p / (rho c_p) if the temperature comes from plastic work only.

Confined plate (2D axisymmetric, 20 x 2) and confined brick column (3D, 20 bricks) at 500 m/s on a rigid wall;
with / without /EOS/GRUNEISEN, bulk viscosity default / ~0, and (3D) /HEAT/MAT with EFRAC 0.9 and 0.5.
Nominal copper-like values (heat3d.CU), feature check only. Prints the median ratio over plastic elements.

Usage: python tcheck.py <work_dir> [out_csv]
"""

import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import heat3d  # noqa: E402
import ocdeck as oc  # noqa: E402
import vtkread  # noqa: E402

A = 300e6
BASE = dict(heat3d.CU, A=A, B=0.0, n=1.0, C=0.0)
Q0 = (1e-30, 1e-30)


def strip_eos(path):
    lines = open(path).read().split("\n")
    i = lines.index("/EOS/GRUNEISEN/1")
    del lines[i : i + 5]
    open(path, "w").write("\n".join(lines))


def case(work, name, dim, eos, q, efrac=None):
    d = os.path.join(work, name)
    mat = oc.JohnsonCookGruneisen(**BASE, heat_efrac=efrac)
    if dim == 3:
        te = 1.5 * 20 * 0.5e-6 / BASE["c0"]
        heat3d.write(d, name, mat, h=0.5e-6, n_z=20, V=500.0, t_end=te, dt_anim=te / 6, thermal=efrac is not None,
                     q=q, dt_scale=0.4)
    else:
        te = 1.5 * 10e-6 / BASE["c0"]
        oc.write_plate_deck(d, name, mat, thickness=10e-6, radius=10e-6, n_z=20, n_r=2, velocity=500.0, t_end=te,
                            dt_th=1e-11, dt_anim=te / 6, q=q, dt_scale=0.4, anim_fields=("TEMP", "EPSP", "P"))
    if not eos:
        strip_eos(os.path.join(d, f"{name}_0000.rad"))
    info = oc.run(d, name)
    if not info.get("normal"):
        return {"case": name, "failed": True}
    fr = vtkread.read(oc.convert_anim(d, name)[3])
    sel = fr["cell"]["ELEMENT_ID"] > 0  # 3D files put two non-element cells first, 2D files last
    pre = f"{dim}DELEM_"
    T = fr["cell"][pre + "Temperature"][sel]
    ep = fr["cell"][pre + "Plastic_Strain"][sel]
    m = ep > 0.01
    return {"case": name, "dim": dim, "eos": "Gruneisen" if eos else "none", "q": "~0" if q else "default",
            "heat_mat_efrac": efrac or "", "t_ns": round(fr["time"] * 1e9, 3), "plastic_cells": int(m.sum()),
            "dT_median_K": float(np.median(T[m] - 293.0)), "A_epsp_over_rhocp_K": float(np.median(A * ep[m] / BASE["rho_cp"])),
            "ratio": float(np.median((T[m] - 293.0) / (A * ep[m] / BASE["rho_cp"])))}


def main(work, out_csv=None):
    rows = []
    for name, dim, eos, q, efrac in (("T2Lq0", 2, False, Q0, None), ("T2Lqd", 2, False, None, None),
                                      ("T2Gq0", 2, True, Q0, None), ("T2Gqd", 2, True, None, None),
                                      ("T3Lq0", 3, False, Q0, None), ("T3Gq0", 3, True, Q0, None),
                                      ("T3H09", 3, False, Q0, 0.9), ("T3H05", 3, False, Q0, 0.5)):
        r = case(work, name, dim, eos, q, efrac)
        rows.append(r)
        print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
    if out_csv:
        with open(out_csv, "w", newline="") as fh:
            keys = list(dict.fromkeys(k for r in rows for k in r))
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    main(*sys.argv[1:3])
