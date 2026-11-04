"""SPH rung S0: confined column (uniaxial strain) on a frictionless rigid wall, against the exact 1D solution.

Rung-0 parameters (identical to the JAX and Isolid = 17 rung 0): E = 70 GPa, nu = 0.35, rho = 2700 kg/m^3,
L = 10 um, V = 100 m/s. Exact: wall stress rho c_d V, contact time 2 L / c_d, rebound velocity V.

Column: n_z particles along z (spacing s = L / n_z), n_xy x n_xy in the cross-section, cubic net. Lateral motion
blocked on every particle (/BCS x, y) and four /SPHBCS/SLIDE planes on the lateral faces (cell boundaries,
half a spacing from the particle centres), so the kernel sees an infinite slab. Wall /RWALL/PLANE through the
bottom particle layer (z = s/2): the column starts in contact. Mass per particle rho s^3, so the column mass is
rho L A exactly.

Metrics (from /TH/PART momentum, cross-checked with /TH/RWALL):
  plateau: mean wall force over the middle half of the contact / (rho c_d V A)
  contact: first time after the peak at which the wall force falls below 5 % of rho c_d V A, / (2 L / c_d)
  rebound: axial centre-of-mass velocity at t_end / V

Usage: python sph_rung0.py <work_dir> <out_csv> <variant> [n_z ...]
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
import sphdeck as sd  # noqa: E402

E, NU, RHO, L, V = 70e9, 0.35, 2700.0, 10e-6, 100.0
CD = math.sqrt(E * (1 - NU) / ((1 + NU) * (1 - 2 * NU) * RHO))
T_C = 2 * L / CD

# variants: smoothing length factor h/s, artificial viscosity (qa, qb), time-step scale, cross-section particles
VARIANTS = {
    "base": dict(hf=1.5, q=(2.0, 1.0), dts=0.3, nxy=4),  # manual defaults: h = 1.5 c (cubic net), q, dt 0.3
    "q0": dict(hf=1.5, q=(1e-30, 1e-30), dts=0.3, nxy=4),  # artificial viscosity off
    "h12": dict(hf=1.25, q=(2.0, 1.0), dts=0.3, nxy=4),  # lower end of the manual's h range
    "h11": dict(hf=2 ** (1 / 6), q=(2.0, 1.0), dts=0.3, nxy=4),  # starter default (sqrt2 m/rho)^(1/3) = 1.122 s
    "xi3": dict(hf=2 ** (1 / 6), q=(2.0, 1.0), dts=0.3, nxy=4, xi=0.3),  # + Monaghan artificial stress 0.3
    "dt9": dict(hf=1.5, q=(2.0, 1.0), dts=0.9, nxy=4),  # default time-step scale
    "w8": dict(hf=1.5, q=(2.0, 1.0), dts=0.3, nxy=8),  # wider cross-section (cost and edge check)
}


def column(n_z, hf, q, nxy, xi=0.0, mat=None, velocity=V):
    s = L / n_z
    xyz = sd.cubic_net((0.0, 0.0, 0.0), (nxy * s, nxy * s, L), s)
    prop = sd.SphProp(h=hf * s, qa=q[0], qb=q[1], xi_stab=xi)
    body = sd.Body(xyz=xyz, mass=RHO * s**3, mat=mat or oc.Elastic(E, NU, RHO), prop=prop,
                   velocity=(0.0, 0.0, -velocity), title="column", fix="110")
    w = nxy * s
    sym = [sd.SymPlane((0, 0, 0), (1, 0, 0)), sd.SymPlane((w, 0, 0), (-1, 0, 0)),
           sd.SymPlane((0, 0, 0), (0, 1, 0)), sd.SymPlane((0, w, 0), (0, -1, 0))]
    return s, body, sym


def metrics(t, f, vz, area, t_c=T_C, f_ref=None):
    f_ref = f_ref or RHO * CD * V * area
    k_pk = int(np.argmax(f))
    below = np.nonzero((np.arange(len(f)) > k_pk) & (f < 0.05 * f_ref))[0]
    t_end_c = float(t[below[0]]) if len(below) else float("nan")
    mid = (t > 0.25 * t_end_c) & (t < 0.75 * t_end_c)
    return {"plateau": float(f[mid].mean() / f_ref), "contact": t_end_c / t_c, "rebound": float(vz[-1] / V),
            "peak": float(f.max() / f_ref)}


def run_case(work, n_z, variant, tag=None, threads=1):
    v = VARIANTS[variant]
    s, body, sym = column(n_z, v["hf"], v["q"], v["nxy"], v.get("xi", 0.0))
    name = tag or f"S0{variant[:4]}{n_z:04d}"
    d = os.path.join(work, name)
    sd.write_deck(d, name, [body], t_end=1.5 * T_C, dt_th=T_C / 1000, sym=sym, z_wall=0.5 * s,
                  dt_scale=v["dts"])
    t0 = time.perf_counter()
    res = sd.run(d, name, threads=threads)
    wall = time.perf_counter() - t0
    if not res.get("normal"):
        print(res.get("starter_tail"), res.get("engine_tail"))
        raise SystemExit(f"{name} failed")
    head, a = oc.read_th(d, name)
    t = a[:, 0]
    col = {h: i for i, h in enumerate(head)}
    zmom = a[:, [i for h, i in col.items() if h.endswith("ZMOM")][0]]
    mass = len(body.xyz) * body.mass
    area = (v["nxy"] * s) ** 2
    f_mom = np.gradient(zmom, t)  # wall force = d(momentum)/dt (only the wall acts)
    fnz = [i for h, i in col.items() if "wall" in h.lower() and h.endswith("FNZ")]
    f_wall = a[:, fnz[0]] if fnz else np.full_like(t, np.nan)
    m = metrics(t, -f_wall, zmom / mass, area)  # rigid-wall force (FNZ is a force in 3D; sign: on the wall)
    mw = metrics(t[1:], f_mom[1:], zmom[1:] / mass, area)  # cross-check: d(momentum)/dt
    ncyc = read_cycles(d, name)
    row = {"variant": variant, "n_z": n_z, "s_um": s * 1e6, "h_over_s": v["hf"], "nxy": v["nxy"],
           "particles": len(body.xyz), **m, "plateau_dPdt": mw["plateau"], "contact_dPdt": mw["contact"],
           "cycles": ncyc, "engine_s": res["engine_s"], "threads": threads,
           "us_per_particle_cycle": res["engine_s"] / (len(body.xyz) * ncyc) * 1e6 if ncyc else float("nan"),
           "wall_s": wall}
    np.save(os.path.join(d, "trace.npy"), {"t": t / T_C, "f": f_mom / (RHO * CD * V * area), "v": zmom / mass / V,
                                           "fw": f_wall / (RHO * CD * V * area)}, allow_pickle=True)
    return row


def read_cycles(d, name):
    """Total number of cycles from the engine listing ('TOTAL NUMBER OF CYCLES  :  n')."""
    for ln in open(os.path.join(d, f"{name}_0001.out"), errors="replace"):
        if "TOTAL NUMBER OF CYCLES" in ln:
            return int(ln.split(":")[1])
    return None


def main():
    work, out_csv, variant = sys.argv[1], sys.argv[2], sys.argv[3]
    ns = [int(x) for x in sys.argv[4:]] or [25, 50, 100]
    rows = []
    if os.path.exists(out_csv):
        rows = list(csv.DictReader(open(out_csv)))
    for n in ns:
        row = run_case(work, n, variant)
        rows.append(row)
        print({k: (round(x, 5) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
        with open(out_csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(row))
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    main()
