"""Rung 1: elastic sphere on a rigid frictionless wall (Hertz impact), OpenCourant vs the JAX code vs Hertz.

Same case as impact_axisym.elastic_sphere_on_rigid_wall: sphere radius R, touching the wall at t = 0, speed V,
graded square-to-disk mesh (n_u, n_v), run to 1.6 Hertz contact times. Metrics, identical for both codes:
    contact  = last time with F > 1e-3 F_Hertz, divided by t_Hertz
    peak     = max F / F_Hertz
    approach = max centre-of-mass approach / d_Hertz
    rebound  = centre-of-mass velocity at the end / V   (Hertz: 1; less = energy left in vibrations)
OpenCourant force = 2 pi d(ZMOM)/dt (per-radian output); approach from the integrated centre-of-mass velocity.

Usage:
    python rung1.py oc  <work_dir> <out_csv> <traces.npy>     (numpy only; OpenCourant runs)
    python rung1.py jax <out_npy>                              (needs the schemeforge env: uv run python ...)
"""

import csv
import math
import os
import sys

import numpy as np

E, NU, RHO, R, V = 70e9, 0.35, 2700.0, 10e-6, 20.0
MESHES = ((15, 30), (30, 60), (60, 120))
THRESH = 1e-3


def hertz():
    """Hertz contact time, peak force, max approach, and the force history F(t) (RK4 of m d'' = -k d^1.5)."""
    e_star = E / (1 - NU**2)
    m = RHO * 4 / 3 * math.pi * R**3
    k = 4 / 3 * e_star * math.sqrt(R)
    d_max = (15 * m * V**2 / (16 * e_star * math.sqrt(R))) ** 0.4
    h = d_max / V / 20000
    y, t, ts, fs = np.array([0.0, V]), 0.0, [0.0], [0.0]

    def rhs(y_):
        return np.array([y_[1], -k * max(y_[0], 0.0) ** 1.5 / m])

    while True:
        k1 = rhs(y)
        k2 = rhs(y + 0.5 * h * k1)
        k3 = rhs(y + 0.5 * h * k2)
        k4 = rhs(y + h * k3)
        yn = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if yn[0] < 0:
            t += h * y[0] / (y[0] - yn[0])
            ts.append(t)
            fs.append(0.0)
            break
        y, t = yn, t + h
        ts.append(t)
        fs.append(k * y[0] ** 1.5)
    return {"t_contact": t, "F_max": k * d_max**1.5, "d_max": d_max, "t": np.array(ts), "F": np.array(fs)}


def metrics(t, f, v, z_appr, H):
    on = t[f > THRESH * H["F_max"]]
    return {"contact": float(on.max() / H["t_contact"]), "peak": float(f.max() / H["F_max"]),
            "approach": float(z_appr.max() / H["d_max"]), "rebound": float(v[-1] / V)}


def run_oc(work, out_csv, out_npy):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ocdeck as oc

    H = hertz()
    rows, store = [], {}
    for var, q, dts in (("A_q0_dt0.4", (1e-30, 1e-30), 0.4), ("C_default", None, None)):
        for n_u, n_v in MESHES:
            name = f"S{var[0]}{n_u:03d}"
            d = os.path.join(work, name)
            rz, quads = oc.sphere_mesh(R, n_u, n_v)
            oc.write_deck(d, name, oc.Elastic(E, NU, RHO), rz, quads, velocity=V, t_end=1.6 * H["t_contact"],
                          dt_th=H["t_contact"] / 2000, q=q, dt_scale=dts)
            info = oc.run(d, name)
            if not info.get("normal"):
                rows.append({"code": "OpenCourant", "variant": var, "n_u": n_u, "n_v": n_v,
                             "failed": " ".join(info.get("engine_tail", info.get("starter_tail", "")).split())[-200:]})
                print(name, "FAILED", rows[-1]["failed"])
                continue
            head, a = oc.read_th(d, name)
            t = a[:, 0]
            zmom = a[:, [i for i, h in enumerate(head) if h.startswith("plate") and h.endswith("ZMOM")][0]]
            mass = a[0, [i for i, h in enumerate(head) if h.startswith("plate") and h.endswith("MASS")][0]]
            vz = zmom / mass
            f = 2 * math.pi * np.diff(zmom) / np.diff(t)
            appr = -np.concatenate([[0.0], np.cumsum(0.5 * (vz[1:] + vz[:-1]) * np.diff(t))])
            m = metrics(t[1:], f, vz, appr, H)
            m["mass_check"] = float(2 * math.pi * mass / (RHO * 4 / 3 * math.pi * R**3))
            rows.append({"code": "OpenCourant", "variant": var, "n_u": n_u, "n_v": n_v, **m,
                         "engine_s": round(info["engine_s"], 2)})
            store[f"{var}|{n_u}"] = (t[1:] / H["t_contact"], f / H["F_max"], t / H["t_contact"], vz / V)
            print(name, {k: (round(x, 4) if isinstance(x, float) else x) for k, x in rows[-1].items()})
    with open(out_csv, "w", newline="") as fh:
        keys = list(dict.fromkeys(k for r in rows for k in r))
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    np.save(out_npy, store, allow_pickle=True)
    print("Hertz", {k: v for k, v in H.items() if k in ("t_contact", "F_max", "d_max")})


def run_jax(out_npy):
    import time

    from schemeforge.research import impact_axisym as ia

    H = hertz()
    ref = ia.hertz_reference(R, V, E, NU, RHO)
    print("Hertz here vs impact_axisym:", H["t_contact"] / ref["t_contact"], H["F_max"] / ref["F_max"])
    out = {}
    for n_u, n_v in MESHES:
        t0 = time.perf_counter()
        res = ia.elastic_sphere_on_rigid_wall(R, V, E, NU, RHO, n_u=n_u, n_v=n_v)
        m = metrics(res.t, res.force, res.v_cm, -(res.z_cm - res.z_cm[0]) + 0.0, H)
        m["wall_s"] = round(time.perf_counter() - t0, 1)
        print("JAX", n_u, n_v, {k: round(x, 4) for k, x in m.items()})
        out[n_u] = {"t": res.t / H["t_contact"], "f": res.force / H["F_max"], "v": res.v_cm / V, **m}
    np.save(out_npy, out, allow_pickle=True)


if __name__ == "__main__":
    if sys.argv[1] == "oc":
        run_oc(*sys.argv[2:5])
    else:
        run_jax(sys.argv[2])
