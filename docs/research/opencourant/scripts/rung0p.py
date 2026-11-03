"""Rung 0p in OpenCourant: confined elastic-perfectly-plastic plate on a rigid frictionless wall (1D two-wave case).

Uniaxial strain, von Mises yield Y, no hardening. Closed-form solution (small strain), for t < 2L/c_d:
    sigma_HEL = Y (1 - nu) / (1 - 2 nu)          elastic precursor, speed c_d = sqrt((lambda + 2 mu) / rho)
    u_HEL     = sigma_HEL / (rho c_d)
    sigma_2   = sigma_HEL + rho c_b (V - u_HEL)   plastic wave, speed c_b = sqrt(K / rho)
    eps_p     = (2/3) (V - u_HEL) / c_b           equivalent plastic strain behind the plastic wave
    wall stress = sigma_2 from t = 0 until the release from the back face returns at t = 2L/c_d.
Stress magnitude in the plate: |sigma_zz| = p + (2/3) sigma_vM (uniaxial strain, compression).

Usage: python rung0p.py <work_dir> <out_csv> <traces.npy>
"""

import csv
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import ocdeck as oc  # noqa: E402
import vtkread  # noqa: E402

E, NU, RHO, L, Y = 70e9, 0.35, 2700.0, 10e-6, 100e6
LAM = E * NU / ((1 + NU) * (1 - 2 * NU))
MU = E / (2 * (1 + NU))
K = LAM + 2 * MU / 3
C_D, C_B = math.sqrt((LAM + 2 * MU) / RHO), math.sqrt(K / RHO)
S_HEL = Y * (1 - NU) / (1 - 2 * NU)
U_HEL = S_HEL / (RHO * C_D)
T_C = 2 * L / C_D


def exact(V):
    s2 = S_HEL + RHO * C_B * (V - U_HEL)
    return {"sigma_HEL": S_HEL, "sigma_2": s2, "c_d": C_D, "c_b": C_B, "force": s2 * math.pi * L**2}


def exact_profile(V, t, z):
    """|sigma_zz|(z, t) for t < L / c_d (before the precursor reaches the back face)."""
    ex = exact(V)
    return np.where(z < C_B * t, ex["sigma_2"], np.where(z < C_D * t, S_HEL, 0.0))


def front(z, s, level):
    """Last z where the profile is above `level`, linearly interpolated to the crossing."""
    above = np.nonzero(s >= level)[0]
    if len(above) == 0 or above[-1] + 1 >= len(s):
        return float("nan")
    k = above[-1]
    return float(z[k] + (level - s[k]) / (s[k + 1] - s[k]) * (z[k + 1] - z[k]))


def axial_profile(frame, n_z, n_r):
    """Mean |sigma_zz| per element layer (Lagrangian layer centre z0, m); cells e = i_r * n_z + i_z."""
    p = frame["cell"]["2DELEM_Pressure"][: n_r * n_z].reshape(n_r, n_z)
    vm = frame["cell"]["2DELEM_Von_Mises"][: n_r * n_z].reshape(n_r, n_z)
    z0 = (np.arange(n_z) + 0.5) * L / n_z
    return z0, (p + 2.0 / 3.0 * vm).mean(0)


def main(work, out_csv, out_npy):
    mat = oc.PlasticLinear(E=E, nu=NU, rho=RHO, sigma_y=Y, hardening=0.0)
    rows, store = [], {}
    cases = [(50.0, n, var) for n in (25, 50, 100, 200) for var in ("q_default_dt0.4", "q0_dt0.4")]
    cases += [(v, 100, "q_default_dt0.4") for v in (25.0, 100.0, 200.0)]
    for V, n, var in cases:
        q = None if var.startswith("q_default") else (1e-30, 1e-30)
        name = f"P{int(V):03d}{n:03d}{'D' if q is None else 'Z'}"
        d = os.path.join(work, name)
        t_snap = 0.75 * L / C_D
        oc.write_plate_deck(d, name, mat, thickness=L, radius=L, n_z=n, n_r=4, velocity=V, t_end=3 * L / C_D,
                            dt_th=T_C / 20000, dt_anim=t_snap / 15, q=q, dt_scale=0.4,
                            anim_fields=("P", "EPSP", "VONM"))
        info = oc.run(d, name)
        if not info.get("normal"):
            rows.append({"V": V, "n_z": n, "variant": var, "failed": " ".join(info.get("engine_tail", "").split())})
            print(name, "FAILED")
            continue
        head, a = oc.read_th(d, name)
        t = a[:, 0]
        zmom = a[:, [i for i, h in enumerate(head) if h.startswith("plate") and h.endswith("ZMOM")][0]]
        mass = a[0, [i for i, h in enumerate(head) if h.startswith("plate") and h.endswith("MASS")][0]]
        f = 2 * math.pi * np.diff(zmom) / np.diff(t)
        tf = t[1:]
        ex = exact(V)
        mid = (tf > 0.2 * T_C) & (tf < 0.8 * T_C)
        frames = [vtkread.read(v) for v in oc.convert_anim(d, name)]
        k = int(np.argmin([abs(fr["time"] - t_snap) for fr in frames]))
        z0, s = axial_profile(frames[k], n, 4)
        ts = frames[k]["time"]
        zp = front(z0, s, 0.5 * (S_HEL + ex["sigma_2"]))
        ze = front(z0, s, 0.5 * S_HEL)
        between = (z0 > zp + 3 * L / n) & (z0 < ze - 3 * L / n)
        plat = (z0 < zp - 3 * L / n)
        row = {
            "V": V, "n_z": n, "variant": var,
            "wall_plateau": float(np.mean(f[mid]) / ex["force"]),
            "sigma2_profile": float(np.mean(s[plat]) / ex["sigma_2"]) if plat.any() else float("nan"),
            "sigmaHEL_profile": float(np.mean(s[between]) / S_HEL) if between.any() else float("nan"),
            "c_b_front": float(zp / ts / C_B),
            "c_d_front": float(ze / ts / C_D),
            "rebound": float(zmom[-1] / mass / V),
            "epsp_behind_plastic_wave": float(
                frames[k]["cell"]["2DELEM_Plastic_Strain"][: 4 * n].reshape(4, n).mean(0)[plat].mean()
                / (2.0 / 3.0 * (V - U_HEL) / C_B)) if plat.any() else float("nan"),
            "epsp_max_run": float(max(fr["cell"]["2DELEM_Plastic_Strain"].max() for fr in frames)),
            "t_snap": float(ts),
        }
        rows.append(row)
        print(name, {k_: (round(v, 4) if isinstance(v, float) else v) for k_, v in row.items()})
        store[name] = {"V": V, "n": n, "var": var, "tf": tf / T_C, "f": f / ex["force"],
                       "profiles": [(fr["time"], *axial_profile(fr, n, 4)) for fr in frames]}
    with open(out_csv, "w", newline="") as fh:
        keys = list(dict.fromkeys(k_ for r in rows for k_ in r))
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    np.save(out_npy, store, allow_pickle=True)
    print("c_d", C_D, "c_b", C_B, "sigma_HEL", S_HEL, "u_HEL", U_HEL, "sigma_2(50)", exact(50.0)["sigma_2"])


if __name__ == "__main__":
    main(*sys.argv[1:4])
