"""Option 1 diagnostic: Al particle on Al substrate, 2D axisymmetric, Lagrangian, Isolid = 17, no erosion.

Runs to 2 D/V or until the first element failure (engine stop on zero/negative volume) or time-step collapse
(/DT minimum, about dt0 / 30; the engine then stops with NORMAL TERMINATION, so the stop is judged from the time
reached). Reports the failure time as a fraction of D/V and the equivalent plastic strain at the contact edge
just before failure. No critical velocity is derived from this (Peter, open item 8).

Material: LAW4 (Johnson-Cook) + /EOS/GRUNEISEN, Al. Values from docs/research/data/properties.csv:
  P-HG-Al (HG2018a preprint, Extended Data Table 1): rho, T_m, c_p, nu, C0 = sqrt(B/rho), s, gamma0 = 2.17,
  JC A, B, n, C, m, reference strain rate 1 1/s, T_ref = 293 K
  P-H20-Al (Hassani2020 Table S1): E = 70 GPa (consistent with B = 76, G = 26 of P-HG-Al)
  (The first sweep used the placeholder gamma0 = 2 s - 1 = 1.678; replaced 2026-11-04, see section 8.3.)
Temperature: computed but not written out with Isolid = 17 (opencourant-verification.md section 5.3).

Usage: python option1_alal.py run <work_dir> <out_csv> [V ...]      (velocities in m/s; default 500 750 1000)
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
from ocdeck import _f, _group, _i, _material_cards  # noqa: E402

R = 10e-6
S_HUG = 1.339
GAMMA0 = float(os.environ.get("GAMMA0", "2.17"))  # P-HG-Al; env override only to reproduce the 1.678 sweep
AL = oc.JohnsonCookGruneisen(E=70e9, nu=0.35, rho=2700.0, A=148.4e6, B=345.5e6, n=0.183, C=0.001, eps_dot0=1.0,
                             m=0.895, T_melt=933.0, rho_cp=2700.0 * 896.9, T_r=293.0, c0=5305.5, S1=S_HUG,
                             gamma0=GAMMA0, heat_efrac=None)
MESHES = {"coarse": 8, "medium": 16, "fine": 32}  # n = core cells across the particle radius / 2 ... see ogrid


def ogrid_halfdisk(radius, n, m):
    """Half-disk r >= 0 centred at the origin: core rectangle [0, a] x [-a, a] (a = radius/2, n x 2n cells) plus
    m layers between its outer boundary (bottom, right, top: 4n segments) and the circle. Returns nodes (k, 2)
    as (r, z), quads (e, 4) 0-based counter-clockwise, and the boundary node chain along the circle (south to
    north pole)."""
    a = radius / 2
    nodes, index = [], {}

    def add(key, p):
        if key not in index:
            index[key] = len(nodes)
            nodes.append(p)
        return index[key]

    quads = []
    # core: i in 0..n (r), j in 0..2n (z)
    for i in range(n + 1):
        for j in range(2 * n + 1):
            add(("c", i, j), (a * i / n, -a + a * j / n))
    for i in range(n):
        for j in range(2 * n):
            quads.append([index[("c", i, j)], index[("c", i + 1, j)], index[("c", i + 1, j + 1)],
                          index[("c", i, j + 1)]])
    # core outer boundary chain: bottom (i = 0..n, j = 0), right (i = n, j = 1..2n), top (i = n-1..0, j = 2n)
    chain = [("c", i, 0) for i in range(n + 1)] + [("c", n, j) for j in range(1, 2 * n + 1)]
    chain += [("c", i, 2 * n) for i in range(n - 1, -1, -1)]
    ns = len(chain) - 1  # 4n segments
    theta = -math.pi / 2 + math.pi * np.arange(ns + 1) / ns
    for k, key in enumerate(chain):
        p = np.array(nodes[index[key]])
        q = radius * np.array([math.cos(theta[k]), math.sin(theta[k])])
        for layer in range(1, m + 1):
            t = layer / m
            add(("o", k, layer), tuple((1 - t) * p + t * q))
    for k in range(ns):
        for layer in range(m):
            k0 = index[chain[k]] if layer == 0 else index[("o", k, layer)]
            k1 = index[chain[k + 1]] if layer == 0 else index[("o", k + 1, layer)]
            quads.append([k0, index[("o", k, layer + 1)], index[("o", k + 1, layer + 1)], k1])
    rim = [index[("o", k, m)] for k in range(ns + 1)]
    X = np.array(nodes)
    Q = np.array(quads)
    # orient counter-clockwise in (r, z)
    for e, q in enumerate(Q):
        p = X[q]
        area = 0.5 * np.sum(p[:, 0] * np.roll(p[:, 1], -1) - np.roll(p[:, 0], -1) * p[:, 1])
        if area < 0:
            Q[e] = q[::-1]
    return X, Q, rim


def graded(h, l_fine, l_total, growth=1.15):
    """Coordinates 0..l_total: uniform spacing h up to l_fine, then geometric growth."""
    xs = list(np.arange(0.0, l_fine + 0.5 * h, h))
    d = h
    while xs[-1] < l_total - 1e-12:
        d *= growth
        xs.append(min(xs[-1] + d, l_total))
    return np.array(xs)


def substrate(h):
    r = graded(h, 1.5 * R, 5 * R)
    z = -graded(h, 1.5 * R, 5 * R)  # 0 .. -5R
    rr, zz = np.meshgrid(r, z, indexing="ij")
    X = np.stack([rr.ravel(), zz.ravel()], 1)
    idx = np.arange(len(X)).reshape(len(r), len(z))
    # counter-clockwise in (r, z) with z decreasing along j: (i,j+1),(i+1,j+1),(i+1,j),(i,j)
    Q = np.stack([idx[:-1, 1:].ravel(), idx[1:, 1:].ravel(), idx[1:, :-1].ravel(), idx[:-1, :-1].ravel()], 1)
    top = idx[:, 0]
    bottom = idx[:, -1]
    return X, Q, top, bottom


def write(d, name, V, n, t_end, dt_anim, dtmin):
    m = n  # outer layers
    Xp, Qp, rim = ogrid_halfdisk(R, n, m)
    Xp = Xp + np.array([0.0, R + 1e-3 * R])  # south pole 0.001 R above the substrate
    h = (R / 2) / n
    Xs, Qs, top, bottom = substrate(h)
    off = len(Xp)
    X = np.vstack([Xp, Xs])
    s = ["#RADIOSS STARTER", f"# schemeforge option-1 diagnostic {name}", "/BEGIN", name, _i(2026) + _i(0),
         f"{'kg':>20}{'m':>20}{'s':>20}", f"{'kg':>20}{'m':>20}{'s':>20}", "/ANALY", _i(1) + _i(0) + _i(0), "/NODE"]
    s += [_i(k + 1) + _f(0.0) + _f(r) + _f(z) for k, (r, z) in enumerate(X)]
    s += ["/QUAD/1"] + ["".join(_i(x) for x in [e + 1, *(q + 1)]) for e, q in enumerate(Qp)]
    s += ["/QUAD/2"] + ["".join(_i(x) for x in [len(Qp) + e + 1, *(q + off + 1)]) for e, q in enumerate(Qs)]
    for pid, title in ((1, "particle"), (2, "substrate")):
        s += [f"/PART/{pid}", title, _i(1) + _i(1) + _i(0)]
    s += ["/PROP/TYPE14/1", "Al solid", _i(17) + _i(0) * 7 + _f(0.0), _f(0.0) * 5, _f(0.0) * 5, _i(0) * 3]
    s += _material_cards(AL)
    s += _group(1, "particle nodes", range(1, off + 1))
    s += _group(2, "substrate nodes", range(off + 1, len(X) + 1))
    s += ["/INIVEL/TRA/1", "impact velocity", _f(0.0) + _f(0.0) + _f(-V) + _i(1) + _i(0), _f(0.0) + _i(0)]
    axis = [k + 1 for k, (r, _) in enumerate(X) if r < 1e-15]
    s += _group(3, "axis nodes", axis)
    s += ["/BCS/1", "axis u_r = 0", "   110 000" + _i(0) + _i(3)]
    s += _group(4, "substrate bottom", bottom + off + 1)
    s += ["/BCS/2", "substrate bottom fixed", "   111 000" + _i(0) + _i(4)]
    others = [k + 1 for k, (r, _) in enumerate(X) if r >= 1e-15 and k + 1 not in set(bottom + off + 1)]
    s += _group(5, "x fixed", others)
    s += ["/BCS/3", "out-of-plane x", "   100 000" + _i(0) + _i(5)]
    s += ["/SURF/SEG/1", "substrate top"] + [_i(k + 1) + _i(top[k] + off + 1) + _i(top[k + 1] + off + 1)
                                             for k in range(len(top) - 1)]
    s += ["/SURF/SEG/2", "particle surface"] + [_i(k + 1) + _i(rim[k] + 1) + _i(rim[k + 1] + 1)
                                                 for k in range(len(rim) - 1)]
    s += _group(6, "substrate top nodes", top + off + 1)
    s += _group(7, "particle rim nodes", [k + 1 for k in rim])
    for iid, grp, line in ((1, 7, 1), (2, 6, 2)):
        s += [f"/INTER/TYPE5/{iid}", f"contact {iid}", _i(grp) + _i(line) + " " * 40 + _i(0) + _i(0),
              _f(0.0) + _f(0.0) + _f(0.0) + _f(0.0) + _f(0.0), " " * 7 + "000" + " " * 10 + _i(0) + _i(0),
              _i(0) + _i(0) + _f(0.0) + " " * 10 + _i(0) + _f(0.0)]
    s += ["/TH/PART/1", "parts", "DEF", _i(1) + _i(2), "/END"]
    e = ["#RADIOSS ENGINE", f"/RUN/{name}/1", _f(t_end), "/TFILE/4", _f(dt_anim / 4), "/TH/TITLE", "/PRINT/-500",
         "/DT", _f(0.9) + _f(dtmin), "/ANIM/DT", _f(0.0) + _f(dt_anim), "/ANIM/ELEM/EPSP", "/ANIM/ELEM/P",
         "/ANIM/ELEM/VONM", "/ANIM/VECT/VEL"]
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f"{name}_0000.rad"), "w").write("\n".join(s) + "\n")
    open(os.path.join(d, f"{name}_0001.rad"), "w").write("\n".join(e) + "\n")
    return {"n_particle_el": len(Qp), "n_substrate_el": len(Qs), "h": h, "rim": rim, "off": off, "top": top}


def listing_stop(d, name, t_end):
    """Why the run stopped. OpenCourant prints NORMAL TERMINATION also when it stops on the /DT minimum time
    step (flag 1 = stop run), so the stop is judged from the last time reached in the time history."""
    txt = open(os.path.join(d, f"{name}_0001.out"), errors="replace").read()

    def is_row(w):
        try:
            return len(w) >= 10 and w[0].isdigit() and "E" in w[2].upper() and w[3].isalpha() and float(w[1]) >= 0
        except ValueError:
            return False

    rows = [ln.split() for ln in txt.splitlines() if is_row(ln.split())]
    dt0 = float(rows[0][2]) if rows else float("nan")
    head, a = oc.read_th(d, name)
    t_last = float(a[-1, 0])
    dtmin = float("nan")
    for ln in txt.splitlines():
        if "QUAD MINIMUM TIME STEP" in ln:
            dtmin = float(ln.split()[-1])
    if "NEGATIVE VOLUME" in txt:
        reason = "negative volume"
    elif t_last < 0.995 * t_end:
        reason = "time-step collapse (dt < dt_min)"
    elif "NORMAL TERMINATION" in txt:
        reason = "reached t_end"
    else:
        reason = "other"
    return reason, t_last, dt0, dtmin, (head, a)


def edge_metrics(frames, n_p_el, info):
    """Per frame: contact radius (largest r of particle rim nodes within h/2 of the substrate top surface height
    at that r) and max eq. plastic strain in particle elements touching the rim within 2h of the contact edge."""
    out = []
    h = info["h"]
    for fr in frames:
        X = fr["xyz"][:, 1:3]
        ids = fr["point"]["NODE_ID"].astype(int)
        pos = {i: k for k, i in enumerate(ids)}
        rim = np.array([X[pos[k + 1]] for k in info["rim"]])
        top = np.array([X[pos[k + info["off"] + 1]] for k in info["top"]])
        ztop = np.interp(rim[:, 0], top[:, 0], top[:, 1])
        touching = rim[:, 1] - ztop < 0.5 * h
        a = rim[touching, 0].max() if touching.any() else 0.0
        sel = fr["cell"]["ELEMENT_ID"] > 0
        eid = fr["cell"]["ELEMENT_ID"][sel].astype(int)
        ep = fr["cell"]["2DELEM_Plastic_Strain"][sel]
        cells = [c for c, s_ in zip(fr["cells"], sel, strict=True) if s_]
        cen = np.array([X[c].mean(0) for c in cells])
        part = eid <= n_p_el
        near = part & (np.hypot(cen[:, 0] - a, cen[:, 1] - np.interp(a, top[:, 0], top[:, 1])) < 2.5 * h)
        near_s = (~part) & (np.hypot(cen[:, 0] - a, cen[:, 1] - np.interp(a, top[:, 0], top[:, 1])) < 2.5 * h)
        out.append({"t": fr["time"], "a": a, "ep_edge_particle": float(ep[near].max()) if near.any() else 0.0,
                    "ep_edge_substrate": float(ep[near_s].max()) if near_s.any() else 0.0,
                    "ep_max_particle": float(ep[part].max()), "ep_max_substrate": float(ep[~part].max())})
    return out


def run_case(work, V, mesh, window=2.0):
    n = MESHES[mesh]
    name = f"A{int(V):04d}{mesh[0].upper()}"
    d = os.path.join(work, name)
    t_ref = 2 * R / V
    h = (R / 2) / n
    dt0_est = 0.9 * 0.5 * h / math.sqrt((70e9 * 0.65 / (1.35 * 0.3)) / 2700)
    t_end = window * t_ref
    info = write(d, name, V, n, t_end=t_end, dt_anim=t_ref / 100, dtmin=dt0_est / 50)
    res = oc.run(d, name)
    reason, t_stop, dt0, dtmin, (head, a) = listing_stop(d, name, t_end)
    zp = a[:, [i for i, x in enumerate(head) if x.startswith("particle") and x.endswith("ZMOM")][0]]
    mp = a[0, [i for i, x in enumerate(head) if x.startswith("particle") and x.endswith("MASS")][0]]
    vp = zp / mp
    up = np.nonzero(vp >= 0)[0]
    t_pen = float(a[up[0], 0]) if len(up) else float("nan")  # particle axial velocity crosses zero
    frames = [vtkread.read(v) for v in oc.convert_anim(d, name)]
    em = edge_metrics(frames, info["n_particle_el"], info) if frames else []
    lastf = em[-1] if em else {}
    row = {"V": V, "mesh": mesh, "h_um": h * 1e6, "particle_el": info["n_particle_el"],
           "substrate_el": info["n_substrate_el"], "stop_reason": reason, "t_stop_ns": t_stop * 1e9,
           "t_stop_over_D_V": t_stop / t_ref, "t_pen_ns": t_pen * 1e9, "t_pen_over_D_V": t_pen / t_ref,
           "t_stop_over_t_pen": t_stop / t_pen if t_pen == t_pen else float("nan"),
           "dt0": dt0, "dt_min": dtmin, "dt_min_over_dt0": dtmin / dt0, "vp_end_over_V": float(vp[-1] / V),
           "frames": len(frames), "t_last_frame_ns": lastf.get("t", float("nan")) * 1e9,
           "a_last_over_R": lastf.get("a", float("nan")) / R,
           "ep_edge_particle_last": lastf.get("ep_edge_particle", float("nan")),
           "ep_edge_substrate_last": lastf.get("ep_edge_substrate", float("nan")),
           "ep_max_particle_last": lastf.get("ep_max_particle", float("nan")),
           "ep_max_substrate_last": lastf.get("ep_max_substrate", float("nan")),
           "engine_s": round(res.get("engine_s", float("nan")), 1)}
    np.save(os.path.join(d, "edge.npy"), em, allow_pickle=True)
    np.save(os.path.join(d, "vp.npy"), np.stack([a[:, 0], vp / V]), allow_pickle=True)
    return row


def main():
    if sys.argv[1] != "run":
        raise SystemExit(__doc__)
    work, out_csv = sys.argv[2], sys.argv[3]
    vs = [float(v) for v in sys.argv[4:]] or [500.0, 750.0, 1000.0]
    meshes = os.environ.get("MESHES", "coarse,medium,fine").split(",")
    rows = []
    for mesh in meshes:
        for V in vs:
            row = run_case(work, V, mesh)
            rows.append(row)
            print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()}, flush=True)
            with open(out_csv, "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(rows[0]))
                w.writeheader()
                w.writerows(rows)


if __name__ == "__main__":
    main()
