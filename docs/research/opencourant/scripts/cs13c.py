"""Hunch CS-13c runs (docs/research/coldspray-hunch-cs13c.md, frozen in 15fe42f): brick particle on brick substrate
(setup B, brick_particle.py, gap and Stfac frozen by rung B0), Al LAW4 + Grueneisen (P-HG-Al) on both bodies,
R = 7.5 um, quarter symmetry, no erosion, no failure, contact without heat transfer.

Twins (all with /THERMAL and /HEAT/MAT on both bodies, rho c_p from P-HG-Al, EFRAC 1, T0 = 293 K):
  k237   k = 237 W/(m K) (P-HG-Al)          k0   k = 0
  noheat (reported only) no /HEAT/MAT, no /THERMAL: LAW4's adiabatic temperature from the element internal energy.

Run stop: time-step collapse below dt_min = dt0 / 50, dt0 = the deck's own cycle-0 time step (from a one-cycle
pre-run of the same deck at that spacing), or t_e = 0.25 D/V.

Pass 1 ("run"): to the stop. P1 = stop time t_f (not failed if t_e is reached); the controlling element and its
body (from the engine's DTMIN message); check E at the last frame:
  E1 heat  = sum over nodes of m_node c_p (T - T0) (twins with /HEAT/MAT: nodal temperature, nodal mass = rho V0 / 8
             per brick corner) or sum over elements m_e c_p (T_e - T0) (noheat); E1 passes if heat <= 1.05 KE0,
             KE0 = 1/2 m_particle V^2 (quarter model).
  E2 every element with T_e > 933 K (T_melt, P-HG-Al) must satisfy rho c_p (T_e - T0) <= 1.10 x its plastic work
     per unit volume (/ANIM/ELEM/WPLA), if OpenCourant writes WPLA; otherwise reported only.
Pass 2 ("tc"): the same deck to t_c = 0.5 x min t_f over all runs at that velocity (both twins), one frame at t_c:
  P2 per body: max eps_p of that body's elements with centroid within 1.17 um of its contact edge, the edge = the
     body's outermost (largest r) surface node in contact: distance to the other body's surface <= 2 x gap.
  P3 (reported): conductive minus k0 of P2 and of the max element temperature in the same bands.

Usage: [THREADS=n] python cs13c.py run <work> <out_csv> <twin> <n_r> <V> [V ...]
       [THREADS=n] python cs13c.py tc  <work> <pass1_csv> <out_csv> <twin> <n_r> <V> [V ...]
"""

import csv
import os
import re
import sys
import time

import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import brick_particle as bp  # noqa: E402
import h0_sph  # noqa: E402
import ocdeck as oc  # noqa: E402
import option1_alal as o1  # noqa: E402
import sph_interface as si  # noqa: E402
import sphdeck as sd  # noqa: E402
import vtkread  # noqa: E402

R = 7.5e-6
D = 2 * R
AL = o1.AL
CP = AL.rho_cp / AL.rho
T0, T_MELT = 293.0, 933.0
BAND = 1.17e-6
B_FROZEN = bp.BSettings(isolid=17, gap_over_s=0.1, stfac=1.0)  # rung B0 (opencourant-verification.md §13.1)
TWIN_K = {"k237": h0_sph.K_AL, "k0": 0.0}
ANIM = ("EPSP", "TEMP", "WPLA")


def heat_fn(twin):
    if twin == "noheat":
        return None
    return lambda mid: h0_sph.heat_cards(mid, T0, TWIN_K[twin], t_melt=AL.T_melt)  # T1 = T_melt: JC softening on


def _write(d, name, twin, n_r, V, t_end, dt_min, dt_anim):
    return bp.write_case(d, name, AL, R, n_r, V, t_end=t_end, dt_th=t_end / 100, bs=B_FROZEN, dt_anim=dt_anim,
                         anim=ANIM, dt_min=dt_min, heat=heat_fn(twin),
                         extra_engine=["/ANIM/NODA/TEMP"] if twin != "noheat" else [])


def dt0(work, twin, n_r, threads):
    """Cycle-0 time step of the deck at this spacing (one-cycle pre-run, 800 m/s)."""
    name = f"dt0{twin}{n_r:02d}"
    d = os.path.join(work, name)
    out = os.path.join(d, f"{name}_0001.out")
    if not os.path.exists(out) or "NORMAL TERMINATION" not in open(out, errors="replace").read():
        _write(d, name, twin, n_r, 800.0, 1e-15, 0.0, None)
        sd.run(d, name, threads=threads, vmem_gb=12, timeout_s=3600)
    for ln in open(out, errors="replace"):
        w = ln.split()
        if len(w) > 3 and w[0] == "0" and re.match(r"^[0-9.]+E[-+]\d+$", w[2]):
            return float(w[2])
    raise RuntimeError(f"no cycle-0 line in {out}")


def stop_info(d, name):
    msgs = [ln.split("DTMIN FOR", 1)[1].split() for ln in open(os.path.join(d, f"{name}_0001.out"), errors="replace")
            if "DTMIN FOR" in ln]
    if not msgs:
        return "", "", ""
    kind = " ".join(msgs[0][:-1])
    ids = sorted({int(m[-1]) for m in msgs if m[-1].isdigit()})
    body = "particle" if kind.startswith("SOLID") and ids and ids[0] > bp.P_ELEM0 else (
        "substrate" if kind.startswith("SOLID") else "?")
    return kind, " ".join(map(str, ids)), body


def frame_arrays(fr):
    ids = fr["point"]["NODE_ID"].astype(int)
    cells = fr["cells"]
    cid = fr["cell"]["ELEMENT_ID"].astype(int)
    part = fr["cell"]["PART_ID"].astype(int)
    return ids, cells, cid, part


def check_e(fr, fr0, info, twin, V):
    """Check E at frame fr (fr0 = the first frame, for the initial volumes)."""
    ids, cells, cid, part = frame_arrays(fr)
    assert np.array_equal(fr0["point"]["NODE_ID"].astype(int), ids), "node order differs between frames"
    c8 = np.array([list(c) for c in cells])
    v0 = np.abs(bp.hex_volumes(fr0["xyz"], c8))
    ke0 = 0.5 * info["m_particle"] * V**2
    Te = np.asarray(fr["cell"].get("3DELEM_Temperature", np.zeros(len(cid))))
    if twin == "noheat":
        heat = float((AL.rho * v0 * CP * (Te - T0)).sum())
    else:
        Tn = np.asarray(fr["point"]["Nodal_Temperature"])
        mn = np.zeros(len(ids))
        np.add.at(mn, c8.ravel(), np.repeat(AL.rho * v0 / 8, 8))
        heat = float((mn * CP * (Tn - T0)).sum())
    out = {"E_heat_over_KE0": heat / ke0, "E1_pass": heat <= 1.05 * ke0, "T_elem_max": float(Te.max()),
           "n_elem_above_Tmelt": int((Te > T_MELT).sum())}
    w = fr["cell"].get("3DELEM_Plastic_Work") if "3DELEM_Plastic_Work" in fr["cell"] else None
    if w is None:
        keys = [k for k in fr["cell"] if "WPLA" in k.upper() or "PLASTIC_WORK" in k.upper()]
        w = fr["cell"][keys[0]] if keys else None
    if w is None:
        out.update({"E2_status": "no WPLA output (reported only)", "E2_pass": ""})
    else:
        hot = Te > T_MELT
        ok = AL.rho_cp * (Te[hot] - T0) <= 1.10 * np.asarray(w)[hot]
        out.update({"E2_status": "checked", "E2_pass": bool(ok.all()), "E2_n_fail": int((~ok).sum())})
    return out


def _tri_dist(p, a, b, c):
    """Distance of points p (n, 3) to triangles (a, b, c) (n, 3) each (Ericson, closest point on triangle)."""
    ab, ac, ap = b - a, c - a, p - a
    d1, d2 = (ab * ap).sum(1), (ac * ap).sum(1)
    bp_, cp_ = p - b, p - c
    d3, d4 = (ab * bp_).sum(1), (ac * bp_).sum(1)
    d5, d6 = (ab * cp_).sum(1), (ac * cp_).sum(1)
    va = d3 * d6 - d5 * d4
    vb = d5 * d2 - d1 * d6
    vc = d1 * d4 - d3 * d2
    den = np.where(np.abs(va + vb + vc) > 0, va + vb + vc, 1e-300)
    v, w = vb / den, vc / den
    q = a + ab * v[:, None] + ac * w[:, None]  # interior
    for cond, qq in (
        ((d1 <= 0) & (d2 <= 0), a), ((d3 >= 0) & (d4 <= d3), b), ((d6 >= 0) & (d5 <= d6), c),
        ((vc <= 0) & (d1 >= 0) & (d3 <= 0), a + ab * (d1 / np.where(d1 - d3 != 0, d1 - d3, 1))[:, None]),
        ((vb <= 0) & (d2 >= 0) & (d6 <= 0), a + ac * (d2 / np.where(d2 - d6 != 0, d2 - d6, 1))[:, None]),
        ((va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0),
         b + (c - b) * ((d4 - d3) / np.where((d4 - d3) + (d5 - d6) != 0, (d4 - d3) + (d5 - d6), 1))[:, None])):
        q = np.where(cond[:, None], qq, q)
    return np.linalg.norm(p - q, axis=1)


def surface_distance(pts, X, faces, s):
    """Distance of each point to the quad surface (faces = node index quads into X), via nearby faces."""
    cen = X[faces].mean(axis=1)
    tree = cKDTree(cen)
    best = np.full(len(pts), np.inf)
    _, j = tree.query(pts, k=8)
    for kk in range(8):  # the 8 nearest face centroids, both triangles of each
        f = faces[j[:, kk]]
        for t in ((0, 1, 2), (0, 2, 3)):
            best = np.minimum(best, _tri_dist(pts, X[f[:, t[0]]], X[f[:, t[1]]], X[f[:, t[2]]]))
    return best


def edge_metrics(fr, info, gap):
    ids, cells, cid, part = frame_arrays(fr)
    pos = {int(k): i for i, k in enumerate(ids)}
    X = fr["xyz"]
    pf = np.vectorize(pos.get)(info["particle_faces"])
    nx, nz = info["nx"], info["nz"]
    nid = si.BRICK_NODE0 + np.arange(nx * nx * nz).reshape(nx, nx, nz)
    it, jt = np.meshgrid(np.arange(nx - 1), np.arange(nx - 1), indexing="ij")
    it, jt = it.ravel(), jt.ravel()
    k = nz - 1
    sf = np.stack([nid[it, jt, k], nid[it + 1, jt, k], nid[it + 1, jt + 1, k], nid[it, jt + 1, k]], 1)
    sf = np.vectorize(pos.get)(sf)
    p_surf = np.unique(pf)
    s_surf = np.unique(sf)
    s = info["s"]
    out = {}
    Te = np.asarray(fr["cell"].get("3DELEM_Temperature", np.zeros(len(cid))))
    ep = np.asarray(fr["cell"]["3DELEM_Plastic_Strain"])
    cen = X[np.array([list(c) for c in cells])].mean(axis=1)
    for body, own, other, pid in (("particle", p_surf, sf, bp.P_PART), ("substrate", s_surf, pf, si.BRICK_PART)):
        dist = surface_distance(X[own], X, other, s)
        touch = dist <= 2 * gap
        if not touch.any():
            out.update({f"a_edge_{body}_over_R": 0.0, f"P2_{body}": float("nan"), f"Tband_{body}": float("nan")})
            continue
        r = np.hypot(X[own, 0], X[own, 1])
        e = int(np.argmax(np.where(touch, r, -1)))
        edge = X[own[e]]
        band = (part == pid) & (np.linalg.norm(cen - edge, axis=1) <= BAND)
        out.update({f"a_edge_{body}_over_R": float(r[e] / R), f"P2_{body}": float(ep[band].max()),
                    f"Tband_{body}": float(Te[band].max()), f"n_band_{body}": int(band.sum()),
                    f"n_touch_{body}": int(touch.sum())})
    return out


def run_case(work, twin, n_r, V, threads, t_end=None, tag=""):
    t_e = 0.25 * D / V
    s = R / n_r
    dtmin = dt0(work, twin if twin != "noheat" else "noheat", n_r, threads) / 50
    name = f"C{twin}{n_r:02d}v{int(V):04d}{tag}"
    d = os.path.join(work, name)
    t_end = t_end or t_e
    info = _write(d, name, twin, n_r, V, t_end, dtmin, t_end)
    t0 = time.perf_counter()
    res = sd.run(d, name, threads=threads, vmem_gb=12, timeout_s=4 * 3600)
    row = {"name": name, "twin": twin, "n_r": n_r, "V": V, "s_um": s * 1e6, "t_e_ns": t_e * 1e9,
           "t_end_ns": t_end * 1e9, "dt_min": dtmin, "particle_bricks": info["n_particle_bricks"],
           "substrate_bricks": info["n_bricks"], "threads": threads}
    if "engine_s" not in res:
        row["failed"] = " ".join(res.get("starter_tail", "").split())[-300:]
        return row, None, None
    frames = oc.convert_anim(d, name)
    fr0, fr = vtkread.read(frames[0]), vtkread.read(frames[-1])
    t_last = float(fr["time"])
    kind, ids, body = stop_info(d, name)
    stopped = bool(kind) and t_last < 0.999 * t_end
    row.update({"t_stop_ns": t_last * 1e9, "t_stop_over_D_V": t_last / (D / V), "failed_collapse": stopped,
                "stop_kind": kind, "stop_ids": ids, "stop_body": body, "engine_s": res["engine_s"],
                "engine_rc": res.get("engine_rc"), "wall_s": time.perf_counter() - t0})
    row.update(check_e(fr, fr0, info, twin, V))
    info.update({"nx": len(si.graded(1.5 * R, 3 * R, s)), "nz": len(si.graded(1.5 * R, 2 * R, s))})
    for f in os.listdir(d):  # keep the run directory small
        if f.endswith(".rst") or (f.startswith(f"{name}A") and not f.endswith(".vtk")):
            os.remove(os.path.join(d, f))
    return row, fr, info


def _append(out_csv, row):
    rows = list(csv.DictReader(open(out_csv))) if os.path.exists(out_csv) else []
    rows.append(row)
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def t_c(pass1_csv, V):
    rows = [r for r in csv.DictReader(open(pass1_csv)) if float(r["V"]) == V and r["twin"] in TWIN_K]
    return 0.5 * min(float(r["t_stop_ns"]) for r in rows) * 1e-9, len(rows)


def main():
    mode = sys.argv[1]
    threads = int(os.environ.get("THREADS", "8"))
    if mode == "run":
        work, out_csv, twin, n_r = sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
        for V in [float(x) for x in sys.argv[6:]]:
            row, _, _ = run_case(work, twin, n_r, V, threads)
            print({k: (round(x, 4) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
            _append(out_csv, row)
    elif mode == "tc":
        work, p1, out_csv, twin, n_r = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], int(sys.argv[6])
        for V in [float(x) for x in sys.argv[7:]]:
            tc, n = t_c(p1, V)
            row, fr, info = run_case(work, twin, n_r, V, threads, t_end=tc, tag="tc")
            row.update({"t_c_ns": tc * 1e9, "n_runs_for_tc": n})
            if fr is not None:
                row.update(edge_metrics(fr, info, info["gap"]))
            print({k: (round(x, 4) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
            _append(out_csv, row)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
