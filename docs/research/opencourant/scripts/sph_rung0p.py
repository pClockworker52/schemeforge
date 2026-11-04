"""SPH rung S0p: confined elastic-perfectly-plastic column on a rigid frictionless wall (1D two-wave case), 3D SPH.

Same set-up as sph_rung0.py (cubic net, lateral /BCS + four /SPHBCS/SLIDE planes, /RWALL/PLANE through the bottom
layer), material LAW2 with Y = 100 MPa and no hardening, V = 50 m/s, as rung 0p (rung0p.py holds the closed form:
elastic precursor sigma_HEL at c_d, plastic wave sigma_2 at c_b, eps_p = (2/3)(V - u_HEL)/c_b behind it).

Metrics: wall plateau / sigma_2 (wall force / A over 0.2..0.8 of 2L/c_d); from one snapshot at t = 0.75 L/c_d:
mean -sigma_zz per particle layer, plateau behind the plastic wave / sigma_2, elastic step / sigma_HEL, front
speeds (half-level crossings) / c_b and / c_d, and eps_p behind the plastic wave / closed form. Layer position
z0 = initial distance of the particle centre from the wall plane.

Usage: python sph_rung0p.py <work_dir> <out_csv> <variant> [n_z ...]
"""

import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import ocdeck as oc  # noqa: E402
import rung0p as r0p  # noqa: E402
import sph_rung0 as s0  # noqa: E402
import sphdeck as sd  # noqa: E402
import vtkread  # noqa: E402

V = 50.0


def layer_profile(fr, n_z, nxy, key):
    sel = fr["cell"]["ELEMENT_ID"] > 0
    val = fr["cell"][key][sel][: nxy * nxy * n_z]
    return val.reshape(nxy * nxy, n_z).mean(0)  # cubic_net order: (ix, iy) outer, iz inner


def run_case(work, n_z, variant, threads=1):
    v = s0.VARIANTS[variant]
    mat = oc.PlasticLinear(E=s0.E, nu=s0.NU, rho=s0.RHO, sigma_y=r0p.Y, hardening=0.0)
    s, body, sym = s0.column(n_z, v["hf"], v["q"], v["nxy"], v.get("xi", 0.0), mat=mat, velocity=V)
    name = f"P0{variant[:4]}{n_z:04d}"
    d = os.path.join(work, name)
    t_snap = 0.75 * s0.L / r0p.C_D
    sd.write_deck(d, name, [body], t_end=1.5 * r0p.T_C, dt_th=r0p.T_C / 1000, sym=sym, z_wall=0.5 * s,
                  dt_scale=v["dts"], dt_anim=t_snap / 15, anim=("EPSP", "SIGZ", "P"))
    res = sd.run(d, name, threads=threads)
    if not res.get("normal"):
        raise SystemExit(f"{name} failed: {res.get('engine_tail')}")
    head, a = oc.read_th(d, name)
    t = a[:, 0]
    col = {h: i for i, h in enumerate(head)}
    f = -a[:, [i for h, i in col.items() if "wall" in h.lower() and h.endswith("FNZ")][0]]
    zmom = a[:, [i for h, i in col.items() if h.endswith("ZMOM")][0]]
    area = (v["nxy"] * s) ** 2
    ex = r0p.exact(V)
    mid = (t > 0.2 * r0p.T_C) & (t < 0.8 * r0p.T_C)
    frames = [vtkread.read(p) for p in oc.convert_anim(d, name)]
    k = int(np.argmin([abs(fr["time"] - t_snap) for fr in frames]))
    ts = frames[k]["time"]
    z0 = (np.arange(n_z) + 0.5) * s - 0.5 * s  # initial distance of each layer from the wall plane
    sz = -layer_profile(frames[k], n_z, v["nxy"], "SPHELEM_Stress_Z_")
    ep = layer_profile(frames[k], n_z, v["nxy"], "SPHELEM_Plastic_Strain")
    zp = r0p.front(z0, sz, 0.5 * (r0p.S_HEL + ex["sigma_2"]))
    ze = r0p.front(z0, sz, 0.5 * r0p.S_HEL)
    between = (z0 > zp + 3 * s) & (z0 < ze - 3 * s)
    plat = (z0 > 3 * s) & (z0 < zp - 3 * s)
    ncyc = s0.read_cycles(d, name)
    row = {"variant": variant, "n_z": n_z, "s_um": s * 1e6, "h_over_s": v["hf"],
           "wall_plateau": float(f[mid].mean() / area / ex["sigma_2"]),
           "sigma2_profile": float(sz[plat].mean() / ex["sigma_2"]) if plat.any() else float("nan"),
           "sigmaHEL_profile": float(sz[between].mean() / r0p.S_HEL) if between.any() else float("nan"),
           "c_b_front": float(zp / ts / r0p.C_B), "c_d_front": float(ze / ts / r0p.C_D),
           "epsp_behind_plastic_wave": float(ep[plat].mean() / (2 / 3 * (V - r0p.U_HEL) / r0p.C_B))
           if plat.any() else float("nan"),
           "rebound": float(zmom[-1] / (len(body.xyz) * body.mass) / V), "cycles": ncyc,
           "engine_s": res["engine_s"], "t_snap": ts}
    np.save(os.path.join(d, "trace.npy"), {"t": t / r0p.T_C, "f": f / area / ex["sigma_2"], "z0": z0 / s0.L,
                                           "profiles": [(fr["time"], -layer_profile(fr, n_z, v["nxy"],
                                                                                    "SPHELEM_Stress_Z_"))
                                                        for fr in frames]}, allow_pickle=True)
    return row


def main():
    work, out_csv, variant = sys.argv[1], sys.argv[2], sys.argv[3]
    ns = [int(x) for x in sys.argv[4:]] or [25, 50, 100]
    rows = list(csv.DictReader(open(out_csv))) if os.path.exists(out_csv) else []
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
