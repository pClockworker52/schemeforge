"""SPH rung S1: elastic sphere on a frictionless rigid wall (Hertz), 3D SPH, quarter (or half) symmetry.

Same physics and metrics as rung1.py (R = 10 um, E = 70 GPa, nu = 0.35, rho = 2700, V = 20 m/s or 2 m/s; contact =
first time after the force peak with F < 1e-3 F_Hertz; peak; max approach; rebound). Compared with Hertz, the
JAX code and OpenCourant Isolid = 17 (rung 1).

Sphere: cubic net of spacing s = R / n_r (optionally with the surface layer moved onto the sphere, SURFACE=conform), particle centres at ((i + 1/2) s, (j + 1/2) s, z) with the sphere
centre on the z axis, keeping centres with |x - c| <= R. The lattice is shifted in z so that the lowest layer
holds only the particle(s) nearest the axis (0.6 s^2/R above the true pole); total mass is
set to the exact sphere mass (particle mass = sphere mass / N; reported against rho s^3).

Symmetry: "quarter" = /SPHBCS/SLIDE planes x = 0 and y = 0 (cell boundaries); "half" = plane x = 0 only, y full.
Wall: "rwall" = /RWALL/PLANE (frictionless) through the lowest particle centre; "mirror" = /SPHBCS/SLIDE plane
half a spacing below the lowest particle centre (kernel contact with the sphere's mirror image; can carry tension).
Force = d(momentum)/dt of the sphere (only the wall acts), scaled by the symmetry factor.

Usage: [THREADS=n] [SURFACE=conform] [XI=0.3] python sph_rung1.py <work_dir> <out_csv> <V> <wall> <sym> <hf> [n_r ...]
       python sph_rung1.py recompute <work_dir> <csv_in> <csv_out>      (adds contact_1pct from saved traces)
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
import rung1 as r1  # noqa: E402
import sph_rung0 as s0  # noqa: E402
import sphdeck as sd  # noqa: E402


def sphere(n_r, sym, conform=False):
    """Particle centres of the sphere (cubic net, spacing s = R / n_r) touching z = 0 at the lowest centre.

    conform=False: plain lattice; the lowest layer holds only the particle(s) next to the axis.
    conform=True: lattice interior, and every particle whose centre lies within s of the surface is moved
    radially onto the sphere of radius R - s/2 (the SPH surface is about s/2 outside the centres), so particle
    heights near the pole follow r^2 / 2R instead of steps of s.
    """
    R = r1.R
    s = R / n_r
    delta0 = 0.6 * s * s / R  # plain lattice: lowest layer 0.6 s^2/R above the pole, only the axis particle(s)
    zc = R - delta0
    xs = (np.arange(-n_r, n_r) + 0.5) * s
    zs = np.arange(0, 2 * n_r + 2) * s
    X, Y, Z = np.meshgrid(xs, xs, zs, indexing="ij")
    p = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    c = np.array([0.0, 0.0, zc])
    dist = np.linalg.norm(p - c, axis=1)
    keep = dist <= R
    if sym == "quarter":
        keep &= (p[:, 0] > 0) & (p[:, 1] > 0)
    elif sym == "half":
        keep &= p[:, 0] > 0
    p, dist = p[keep], dist[keep]
    if conform:
        outer = dist > R - s
        p[outer] = c + (p[outer] - c) * ((R - 0.5 * s) / dist[outer])[:, None]
        # merge surface pairs closer than s/2 (about 0.5 % of the particles): keep one at the pair's mean
        # direction on the surface sphere; the particle mass is set from the sphere mass in run_case
        idx = np.nonzero(outer)[0]
        q = p[idx]
        dd = np.linalg.norm(q[:, None, :] - q[None, :, :], axis=2)
        np.fill_diagonal(dd, np.inf)
        drop = set()
        for i, j in zip(*np.nonzero(dd < 0.5 * s), strict=True):
            if i < j and i not in drop and j not in drop:
                m_ = 0.5 * (q[i] + q[j]) - c
                p[idx[i]] = c + m_ * (R - 0.5 * s) / np.linalg.norm(m_)
                drop.add(j)
        p = np.delete(p, [idx[j] for j in drop], axis=0)
    p[:, 2] -= p[:, 2].min()  # lowest particle centre at z = 0
    return s, p


def min_spacing(p):
    """Smallest distance between two particles (brute force in chunks), m."""
    best = np.inf
    for k in range(0, len(p), 2000):
        d = np.linalg.norm(p[k:k + 2000, None, :] - p[None, :, :], axis=2)
        d[d == 0] = np.inf
        best = min(best, float(d.min()))
    return best


def run_case(work, V, wall, sym, hf, n_r, threads=1, dts=0.3, q=(2.0, 1.0), t_fac=1.6, tag=None, conform=False,
             xi=0.0):
    H = hertz_v(V)
    s, p = sphere(n_r, sym, conform)
    factor = {"quarter": 4.0, "half": 2.0, "full": 1.0}[sym]
    m_lattice = r1.RHO * s**3
    z_shift = 0.5 * s if wall == "mirror" else 0.0
    p = p + np.array([0.0, 0.0, z_shift])
    prop = sd.SphProp(h=hf * s, qa=q[0], qb=q[1], xi_stab=xi)
    m_p = r1.RHO * 4 / 3 * math.pi * r1.R**3 / factor / len(p)  # exact sphere mass, shared equally
    body = sd.Body(xyz=p, mass=m_p, mat=oc.Elastic(r1.E, r1.NU, r1.RHO), prop=prop,
                   velocity=(0.0, 0.0, -V), title="sphere")
    planes = []
    if sym in ("quarter", "half"):
        planes.append(sd.SymPlane((0, 0, 0), (1, 0, 0)))
    if sym == "quarter":
        planes.append(sd.SymPlane((0, 0, 0), (0, 1, 0)))
    if wall == "mirror":
        planes.append(sd.SymPlane((0, 0, 0), (0, 0, 1)))
    name = tag or (f"H{wall[0]}{sym[0]}{'c' if conform else 'l'}{int(V):02d}{int(round(hf * 100)):03d}{n_r:03d}"
                   + (f"x{int(round(xi * 10))}" if xi else ""))
    d = os.path.join(work, name)
    sd.write_deck(d, name, [body], t_end=t_fac * H["t_contact"], dt_th=H["t_contact"] / 2000, sym=planes,
                  z_wall=0.0 if wall == "rwall" else None, dt_scale=dts)
    t0 = time.perf_counter()
    res = sd.run(d, name, threads=threads)
    if not res.get("normal"):
        return {"name": name, "failed": " ".join(res.get("engine_tail", res.get("starter_tail", "")).split())[-300:]}
    head, a = oc.read_th(d, name)
    t = a[:, 0]
    col = {h_: i for i, h_ in enumerate(head)}
    zmom = a[:, [i for h_, i in col.items() if h_.endswith("ZMOM")][0]] * factor
    mass = len(p) * body.mass * factor
    vz = zmom / mass
    f = np.diff(zmom) / np.diff(t)
    appr = -np.concatenate([[0.0], np.cumsum(0.5 * (vz[1:] + vz[:-1]) * np.diff(t))])
    m = metrics_v(t[1:], f, vz, appr, H, V)
    ncyc = s0.read_cycles(d, name)
    row = {"name": name, "V": V, "wall": wall, "sym": sym, "surface": "conform" if conform else "lattice",
           "h_over_s": hf, "xi_stab": xi, "n_r": n_r, "s_um": s * 1e6,
           "particles": len(p), "mass_over_lattice_mass": m_p / m_lattice,
           "a_hertz_over_s": math.sqrt(r1.R * H["d_max"]) / s, "d_hertz_over_s": H["d_max"] / s, **m,
           "cycles": ncyc, "threads": threads, "engine_s": res["engine_s"],
           "us_per_particle_cycle": res["engine_s"] * threads / (len(p) * ncyc) * 1e6 if ncyc else float("nan"),
           "wall_s": time.perf_counter() - t0}
    np.save(os.path.join(d, "trace.npy"), {"t": t[1:] / H["t_contact"], "f": f / H["F_max"],
                                           "tv": t / H["t_contact"], "v": vz / V}, allow_pickle=True)
    return row


def hertz_v(V):
    old = r1.V
    r1.V = V
    try:
        return r1.hertz()
    finally:
        r1.V = old


def contact_end(t, f, thresh):
    """First time after the force peak with f < thresh (same rule as rung1.contact_end)."""
    k = int(np.argmax(f))
    below = np.nonzero(f[k:] < thresh)[0]
    return float(t[k + below[0]]) if len(below) else float("nan")


def metrics_v(t, f, v, appr, H, V):
    """Rung-1 metrics; contact also at a 1e-2 F_Hertz threshold, because SPH force tails (a few edge particles
    leaving the wall late, < 1 % F_Hertz) move the 1e-3 end of contact."""
    return {"contact": contact_end(t, f, 1e-3 * H["F_max"]) / H["t_contact"],
            "contact_1pct": contact_end(t, f, 1e-2 * H["F_max"]) / H["t_contact"],
            "peak": float(f.max() / H["F_max"]), "approach": float(appr.max() / H["d_max"]),
            "rebound": float(v[-1] / V)}


def recompute(work, csv_in, csv_out):
    """Add contact_1pct to rows of an existing CSV from the saved traces (normalised t and f)."""
    rows = list(csv.DictReader(open(csv_in)))
    for r in rows:
        if r.get("name") and os.path.exists(os.path.join(work, r["name"], "trace.npy")):
            d = np.load(os.path.join(work, r["name"], "trace.npy"), allow_pickle=True).item()
            r["contact_1pct"] = contact_end(d["t"], d["f"], 1e-2)
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(csv_out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def main():
    if sys.argv[1] == "recompute":
        recompute(*sys.argv[2:5])
        return
    work, out_csv, V, wall, sym, hf = sys.argv[1:7]
    ns = [int(x) for x in sys.argv[7:]] or [16, 24, 32]
    threads = int(os.environ.get("THREADS", "1"))
    conform = os.environ.get("SURFACE", "lattice") == "conform"
    xi = float(os.environ.get("XI", "0"))
    rows = list(csv.DictReader(open(out_csv))) if os.path.exists(out_csv) else []
    for n in ns:
        row = run_case(work, float(V), wall, sym, float(hf), n, threads=threads, conform=conform, xi=xi)
        rows.append(row)
        print({k: (round(x, 5) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with open(out_csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    main()
