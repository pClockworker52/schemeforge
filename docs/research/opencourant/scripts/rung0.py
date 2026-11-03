"""Rung 0 in OpenCourant: laterally confined elastic plate on a rigid frictionless wall (uniaxial strain).

Same case and metric definitions as the JAX rung 0 (src/schemeforge/research/impact_axisym.py,
confined_plate_on_rigid_wall; tests/test_impact_axisym.py):
    plateau  = mean wall force over 0.2 t_c < t < 0.8 t_c, divided by rho c_d V pi L^2
    contact  = last time with wall force > 1e-9 F_exact, divided by t_c = 2 L / c_d
    rebound  = centre-of-mass velocity at t = 3 L / c_d, divided by V
Wall force = 2 pi d(ZMOM)/dt from the part time history (output is per radian; the wall is the only axial force).
The /TH/RWALL FNZ column is also recorded: in 2D axisymmetric runs it equals the integral of sigma_zz dr (no r weight).

Usage: python rung0.py <work_dir> <out_csv>
"""

import csv
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocdeck as oc  # noqa: E402

E, NU, RHO, L, V = 70e9, 0.35, 2700.0, 10e-6, 100.0
C_D = math.sqrt(E * (1 - NU) / ((1 + NU) * (1 - 2 * NU)) / RHO)
T_C = 2 * L / C_D
F_EX = RHO * C_D * V * math.pi * L**2
VARIANTS = {  # name: (bulk viscosity (qa, qb) or None = defaults 1.10/0.05, time-step scale or None = 0.9)
    "A_q0_dt0.4": ((1e-30, 1e-30), 0.4),
    "B_q0_dt0.9": ((1e-30, 1e-30), None),
    "C_default": (None, None),
}


def col(head, suffix, prefix=""):
    return [i for i, n in enumerate(head) if n.endswith(suffix) and n.startswith(prefix)][0]


def metrics(run_dir, name):
    head, a = oc.read_th(run_dir, name)
    t = a[:, 0]
    zmom = a[:, col(head, "ZMOM", "plate")]
    mass = a[0, col(head, "MASS", "plate")]
    fnz = a[:, col(head, "FNZ")]
    f = 2 * math.pi * np.diff(zmom) / np.diff(t)  # N, full ring; assigned to the end of each interval
    tf = t[1:]
    mid = (tf > 0.2 * T_C) & (tf < 0.8 * T_C)
    midt = (t > 0.2 * T_C) & (t < 0.8 * T_C)
    ke = a[:, col(head, "KE", "plate")]
    return {
        "plateau": float(np.mean(f[mid]) / F_EX),
        "contact": float(tf[f > 1e-9 * F_EX].max() / T_C),
        "rebound": float(zmom[-1] / mass / V),
        "ke_ratio": float(ke[-1] / ke[0]),
        "fnz_over_sigmaR": float(-np.mean(fnz[midt]) / (RHO * C_D * V * L)),
        "mass_over_rhoL3_2": float(mass / (RHO * L**3 / 2)),
        "n_cycles": int(len(t) - 1),
        "dt_first": float(t[1] - t[0]),
    }, (tf / T_C, f / F_EX, t / T_C, zmom / mass / V)


def main(work, out_csv):
    rows, traces = [], {}
    for var, (q, dts) in VARIANTS.items():
        for n in (25, 50, 100, 200):
            name = f"R0{var[0]}{n:03d}"
            d = os.path.join(work, name)
            oc.write_plate_deck(d, name, oc.Elastic(E, NU, RHO), thickness=L, radius=L, n_z=n, n_r=4,
                                velocity=V, t_end=3 * L / C_D, dt_th=T_C / 20000, q=q, dt_scale=dts)
            info = oc.run(d, name)
            if not info.get("normal"):
                msg = info.get("engine_tail", "")[-160:].replace("\n", " ")
                rows.append({"variant": var, "n_z": n, "failed": " ".join(msg.split())})
                print(var, n, "FAILED", msg)
                continue
            m, tr = metrics(d, name)
            traces[(var, n)] = tr
            rows.append({"variant": var, "n_z": n, **m, "engine_s": round(info["engine_s"], 3)})
            print(var, n, {k: (round(v, 5) if isinstance(v, float) else v) for k, v in m.items()})
    with open(out_csv, "w", newline="") as fh:
        keys = list(dict.fromkeys(k for r in rows for k in r))
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    np.save(os.path.join(work, "traces.npy"), {f"{k[0]}|{k[1]}": v for k, v in traces.items()}, allow_pickle=True)
    print("c_d", C_D, "t_c", T_C, "F_exact", F_EX)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
