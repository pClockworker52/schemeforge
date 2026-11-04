"""CS-11 prerequisite rungs F0 and W0: elastic SPH sphere on an elastic substrate of the same material at 20 m/s,
against two-body Hertz (E* = E / (2 (1 - nu^2)), same sphere mass). Rung-1 material and radius (R = 10 um,
E = 70 GPa, nu = 0.35, rho = 2700). Quarter symmetry; substrate block 3R x 3R x 2R, bottom fixed.

  F0: substrate of bricks, /INTER/TYPE7 friction 0 (sph_interface.py). Pass (frozen, coldspray-hunch-cs11.md):
      at R/32 peak force and maximum approach within 5 % of Hertz, and rebound > 0.9 V.
  W0: SPH substrate (kernel-welded). Loading phase only: pass at R/32 if peak force and maximum approach are
      within 5 % of Hertz. Rebound reported without a threshold.

Metrics as in sph_rung1.py: peak = max F / F_Hertz; approach = max centre-of-mass approach / d_Hertz (from t = 0,
the geometric first contact: lowest particle centre at the TYPE7 gap (F) or one spacing above the top substrate
particle layer (W)); contact end at 1e-2 F_Hertz; rebound = final centre-of-mass velocity / V.

Usage: [THREADS=n] python sph_f0w0.py <work_dir> <out_csv> <F|W> <n_r> [isolid gap_over_s stfac]
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
import sph_interface as si  # noqa: E402
import sph_rung0 as s0  # noqa: E402
import sph_rung1 as s1  # noqa: E402
import sphdeck as sd  # noqa: E402

V = 20.0


def hertz2(V=V):
    """Two-body Hertz for identical materials: rung1.hertz with E replaced so that E* = E / (2 (1 - nu^2))."""
    old = r1.E, r1.V
    r1.E, r1.V = r1.E / 2, V
    try:
        return r1.hertz()
    finally:
        r1.E, r1.V = old


def run_case(work, setup, n_r, fs=None, threads=1, t_fac=None, tag=None, w_dist=1.0):
    fs = fs or si.FSettings()
    H = hertz2()
    t_fac = t_fac or (1.6 if setup == "F" else 0.8)
    mat = oc.Elastic(r1.E, r1.NU, r1.RHO)
    name = tag or (f"F0i{fs.isolid:02d}g{int(round(fs.gap_over_s * 100)):03d}k{int(round(fs.stfac * 10)):03d}"
                   f"n{n_r:03d}" if setup == "F" else f"W0n{n_r:03d}" + (f"d{int(round(w_dist * 10)):02d}" if w_dist != 1.0 else ""))
    d = os.path.join(work, name)
    t_flight = (w_dist - 1.0) * r1.R / n_r / V if setup == "W" else 0.0  # free flight before lattice contact
    info = si.write_case(d, name, setup, mat, r1.R, n_r, V, t_end=t_fac * H["t_contact"] + t_flight,
                         dt_th=H["t_contact"] / 2000, fs=fs, w_dist_over_s=w_dist)
    t0 = time.perf_counter()
    res = sd.run(d, name, threads=threads)
    row = {"name": name, "setup": setup, "n_r": n_r, "isolid": fs.isolid if setup == "F" else "",
           "gap_over_s": fs.gap_over_s if setup == "F" else "", "stfac": fs.stfac if setup == "F" else "",
           "particles": info["n_particles"], "substrate_particles": info["n_sub_particles"],
           "bricks": info.get("n_bricks", 0), "threads": threads}
    if not res.get("normal"):
        row["failed"] = " ".join(res.get("engine_tail", res.get("starter_tail", "")).split())[-300:]
        return row
    t, vz, f, appr, _, _ = si.sphere_trace(d, name, info["m_particle"])
    if setup == "W" and w_dist != 1.0:  # approach from the geometric contact (lowest particle one spacing above)
        appr = np.interp(t, t, appr) - (w_dist - 1.0) * info["s"]
        row["w_dist_over_s"] = w_dist
    t = t - t_flight  # time from the geometric contact
    tn = t[1:] / H["t_contact"]
    fn = f / H["F_max"]
    ncyc = s0.read_cycles(d, name)
    row.update({"t_end_over_tc": t_fac, "peak": float(fn.max()), "t_peak": float(tn[np.argmax(fn)]),
                "approach": float(appr.max() / H["d_max"]),
                "contact_1pct": s1.contact_end(tn, fn, 1e-2), "rebound": float(vz[-1] / V),
                "a_hertz_over_s": math.sqrt(r1.R * H["d_max"]) / info["s"], "d_hertz_over_s": H["d_max"] / info["s"],
                "cycles": ncyc, "engine_s": res["engine_s"], "wall_s": time.perf_counter() - t0})
    np.save(os.path.join(d, "trace.npy"), {"t": tn, "f": fn, "tv": t / H["t_contact"], "v": vz / V,
                                           "appr": appr / H["d_max"]}, allow_pickle=True)
    return row


def main():
    work, out_csv, setup, n_r = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    fs = si.FSettings()
    if len(sys.argv) > 5:
        fs = si.FSettings(isolid=int(sys.argv[5]), gap_over_s=float(sys.argv[6]), stfac=float(sys.argv[7]))
    threads = int(os.environ.get("THREADS", "1"))
    w_dist = float(os.environ.get("W_DIST", "1.0"))  # W: initial distance lowest particle - top layer, in s
    row = run_case(work, setup, n_r, fs, threads=threads, w_dist=w_dist)
    print({k: (round(x, 5) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
    rows = list(csv.DictReader(open(out_csv))) if os.path.exists(out_csv) else []
    rows.append(row)
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
