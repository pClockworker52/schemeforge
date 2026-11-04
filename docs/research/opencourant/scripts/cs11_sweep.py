"""Hunch CS-11 sweep (docs/research/coldspray-hunch-cs11.md, frozen protocol): normal Al-Al impact, d = 15 um,
setups W (SPH on SPH, welded) and F (SPH on TYPE7 bricks, frictionless), quarter symmetry, run to
t_e = 0.25 D/V.

Material: LAW4 Johnson-Cook + /EOS/GRUNEISEN, P-HG-Al (option1_alal.AL: gamma0 = 2.17, eps_dot0 = 1 1/s,
T_ref = 293 K), no failure, no erosion, no /HEAT/MAT. Particle and substrate the same material.

Metrics:
  J(V)   = max over t <= t_e and over all particle SPH particles of u_r / V (u_r = outward radial velocity),
           from /TH/NODE (X, Y, VX, VY) of every particle node, sampled every t_e / 100.
  J_s    = the same over the substrate nodes with z >= -R/2 and r <= 2R (reported, no verdict).
  edge eps_p at t_e: contact edge = largest r of a particle particle whose nearest substrate node is closer than
           1.1 s (W: substrate particle; lattice neighbours start at s) or 0.9 s (F: brick node; a particle at the
           gap s/2 above a face centre is 0.87 s from the nearest node); max equivalent plastic strain of particle particles and of
           substrate cells (F: brick centroids, W: particles) within 2.5 s of that edge point.
  F only: time-step collapse = the run stops below dt_min = dt0_est / 50 (as in §8.3, option1_alal.py); the run
           is then evaluated up to the stop time; a stop before 0.1 D/V makes it unevaluable.

Usage: [THREADS=n] python cs11_sweep.py run <work_dir> <out_csv> <W|F> <n_r> <V> [V ...]
"""

import csv
import os
import sys
import time

import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import ocdeck as oc  # noqa: E402
import option1_alal as o1  # noqa: E402
import sph_interface as si  # noqa: E402
import sph_rung0 as s0  # noqa: E402
import sphdeck as sd  # noqa: E402
import vtkread  # noqa: E402

R = 7.5e-6
D = 2 * R
AL = o1.AL
F_FROZEN = si.FSettings()  # frozen in rung F0 (opencourant-verification.md §10.2): Isolid 17, gap s/2, Stfac 10
assert (F_FROZEN.isolid, F_FROZEN.gap_over_s, F_FROZEN.stfac, F_FROZEN.q) == (17, 0.5, 10.0, None)
DT_SPH_PER_M = 2.15e-5  # measured SPH time step per metre of spacing at dt scale 0.3 (§9.3)


def read_th_fast(d, name):
    """Time history CSV as (header list, array (n_t, n_col)); for wide files with many /TH/NODE columns."""
    path = os.path.join(d, f"{name}T01.csv")
    with open(path) as fh:
        head = [h.strip() for h in next(csv.reader([fh.readline()]))]
        a = np.array([[float(x) for x in ln.split(",")] for ln in fh if ln.strip()])
    return head, a


def node_columns(head, var):
    """{node id: column} for /TH/NODE columns named like '<group> <id> <var>' (last token = variable)."""
    out = {}
    for i, h in enumerate(head):
        w = h.replace("_", " ").split()
        if len(w) >= 2 and w[-1] == var:
            ids = [x for x in w[:-1] if x.isdigit()]
            if ids:
                out[int(ids[-1])] = i
    return out


def jet_metric(head, a, ids, V, t_max):
    """max over t <= t_max and the node ids of u_r / V, with the time and node of the maximum."""
    cx, cy, cvx, cvy = (node_columns(head, v) for v in ("X", "Y", "VX", "VY"))
    ids = [k for k in ids if k in cx and k in cvx]
    keep = a[:, 0] <= t_max * (1 + 1e-9)
    X, Y = a[keep][:, [cx[k] for k in ids]], a[keep][:, [cy[k] for k in ids]]
    VX, VY = a[keep][:, [cvx[k] for k in ids]], a[keep][:, [cvy[k] for k in ids]]
    r = np.hypot(X, Y)
    ur = np.where(r > 0, (X * VX + Y * VY) / np.maximum(r, 1e-30), 0.0) / V
    j = np.unravel_index(np.argmax(ur), ur.shape)
    curve = ur.max(axis=1)
    return float(ur[j]), float(a[keep][j[0], 0]), ids[j[1]], a[keep][:, 0], curve, len(ids)


def edge_strain(frame, info, n_part, setup):
    """Contact edge radius and max eps_p near it (particle, substrate) from the animation frame at t_e."""
    s = info["s"]
    ids = frame["point"]["NODE_ID"].astype(int)
    xyz = frame["xyz"]
    cell_ids = frame["cell"]["ELEMENT_ID"].astype(int)
    single = np.array([len(c) == 1 for c in frame["cells"]])
    zero = np.zeros(len(cell_ids))
    ep = np.where(single, frame["cell"].get("SPHELEM_Plastic_Strain", zero),
                  frame["cell"].get("3DELEM_Plastic_Strain", zero))
    centres = np.array([xyz[c].mean(axis=0) for c in frame["cells"]])
    is_part = np.array([sg and ids[c[0]] <= n_part for sg, c in zip(single, frame["cells"], strict=True)])
    is_sub = ~is_part
    p_xyz = centres[is_part]
    sub_nodes = xyz[ids > n_part] if setup == "W" else xyz[ids >= si.BRICK_NODE0]
    dist, _ = cKDTree(sub_nodes).query(p_xyz)
    touch = dist < (1.1 * s if setup == "W" else 0.9 * s)  # W: lattice neighbours at s; F: centre at gap s/2
    if not touch.any():
        return {"a_edge_over_R": 0.0, "ep_edge_particle": 0.0, "ep_edge_substrate": 0.0}
    rr = np.hypot(p_xyz[:, 0], p_xyz[:, 1])
    k = int(np.argmax(np.where(touch, rr, -1)))
    edge = p_xyz[k]
    near_p = np.linalg.norm(p_xyz - edge, axis=1) < 2.5 * s
    near_s = np.linalg.norm(centres[is_sub] - edge, axis=1) < 2.5 * s
    return {"a_edge_over_R": float(rr[k] / R), "ep_edge_particle": float(ep[is_part][near_p].max()),
            "ep_edge_substrate": float(ep[is_sub][near_s].max()) if near_s.any() else 0.0}


def run_case(work, setup, n_r, V, threads=1):
    t_e = 0.25 * D / V
    s = R / n_r
    dt_min = DT_SPH_PER_M * s / 50
    name = f"C{setup}{n_r:02d}v{int(V):04d}"
    d = os.path.join(work, name)
    info = si.write_case(d, name, setup, AL, R, n_r, V, t_end=t_e, dt_th=t_e / 100, fs=F_FROZEN, dt_anim=t_e,
                         anim=("EPSP", "P"), dt_min=dt_min, th_sub=(0.5 * R, 2 * R))
    t0 = time.perf_counter()
    res = sd.run(d, name, threads=threads)
    row = {"name": name, "setup": setup, "n_r": n_r, "V": V, "s_um": s * 1e6, "particles": info["n_particles"],
           "substrate_particles": info["n_sub_particles"], "bricks": info.get("n_bricks", 0), "threads": threads,
           "t_e_ns": t_e * 1e9}
    if not res.get("starter_rc", 1) == 0 or "engine_s" not in res:
        row["failed"] = " ".join(res.get("starter_tail", "").split())[-300:]
        return row
    head, a = read_th_fast(d, name)
    t_last = float(a[-1, 0])
    stopped = t_last < 0.995 * t_e
    row.update({"t_stop_over_D_V": t_last / (D / V), "stopped_early": stopped,
                "evaluable": not (stopped and t_last < 0.1 * D / V),
                "negative_volume": "NEGATIVE VOLUME" in open(os.path.join(d, f"{name}_0001.out"), errors="replace").read()})
    n_part = info["n_particles"]
    J, tJ, nJ, tt, curve, nn = jet_metric(head, a, range(1, n_part + 1), V, t_e)
    Js, tJs, _, _, curve_s, nns = jet_metric(head, a, info["th_sub_ids"], V, t_e)
    row.update({"J": J, "t_J_over_t_e": tJ / t_e, "node_J": nJ, "J_s": Js, "t_Js_over_t_e": tJs / t_e,
                "n_th_particle": nn, "n_th_sub": nns})
    frames = [f for f in oc.convert_anim(d, name)]
    if frames and not stopped:
        row.update(edge_strain(vtkread.read(frames[-1]), info, n_part, setup))
    ncyc = s0.read_cycles(d, name)
    row.update({"cycles": ncyc, "engine_s": res["engine_s"], "wall_s": time.perf_counter() - t0,
                "us_per_item_cycle": res["engine_s"] * threads / ((n_part + info["n_sub_particles"]
                                                                   + info.get("n_bricks", 0)) * ncyc) * 1e6
                if ncyc else float("nan")})
    np.save(os.path.join(d, "jet.npy"), {"t": tt, "J_t": curve, "J_s_t": curve_s, "t_e": t_e, "V": V},
            allow_pickle=True)
    for f in os.listdir(d):  # keep the run directory small: the wide TH CSV and raw animation files go
        if f.endswith("T01.csv") or (f.startswith(f"{name}A") and not f.endswith(".vtk")):
            os.remove(os.path.join(d, f))
    return row


def main():
    if sys.argv[1] != "run":
        raise SystemExit(__doc__)
    work, out_csv, setup, n_r = sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
    threads = int(os.environ.get("THREADS", "1"))
    for V in [float(x) for x in sys.argv[6:]]:
        row = run_case(work, setup, n_r, V, threads=threads)
        print({k: (round(x, 4) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
        rows = list(csv.DictReader(open(out_csv))) if os.path.exists(out_csv) else []
        rows.append(row)
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with open(out_csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    main()
