"""CS-13c prerequisite rung B0: elastic brick sphere on an elastic brick block, two TYPE7 contacts, friction 0,
20 m/s, against two-body Hertz (E* = E / (2 (1 - nu^2))). The brick analogue of F0 (sph_f0w0.py): rung-1 material
and radius (R = 10 um, E = 70 GPa, nu = 0.35, rho = 2700), quarter symmetry, block 3R x 3R x 2R, bottom fixed,
setup B of brick_particle.py.

Pass (frozen, coldspray-hunch-cs13c.md): at R/32 peak force and maximum approach within 5 % of Hertz, and rebound
> 0.9 V. Gap and Stfac are chosen here and then frozen.

Metrics as F0: force = -d(ZMOM)/dt of the particle x 4, approach = integrated centre-of-mass velocity from t = 0
(lowest node at the gap: contact starts at t = 0), contact end at 1e-2 F_Hertz, rebound = final vz / V.

Usage: [THREADS=n] python b0_rung.py <work_dir> <out_csv> <n_r> <gap_over_s> <stfac>
"""

import csv
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import brick_particle as bp  # noqa: E402
import ocdeck as oc  # noqa: E402
import rung1 as r1  # noqa: E402
import sph_f0w0 as fw  # noqa: E402
import sph_interface as si  # noqa: E402
import sph_rung0 as s0  # noqa: E402
import sph_rung1 as s1  # noqa: E402
import sphdeck as sd  # noqa: E402


def run_case(work, n_r, bs, threads=8, t_fac=1.6):
    H = fw.hertz2()
    mat = oc.Elastic(r1.E, r1.NU, r1.RHO)
    name = f"B0g{int(round(bs.gap_over_s * 100)):03d}k{int(round(bs.stfac * 10)):03d}n{n_r:03d}"
    d = os.path.join(work, name)
    info = bp.write_case(d, name, mat, r1.R, n_r, fw.V, t_end=t_fac * H["t_contact"], dt_th=H["t_contact"] / 2000,
                         bs=bs)
    t0 = time.perf_counter()
    res = sd.run(d, name, threads=threads, vmem_gb=12, timeout_s=3 * 3600)
    row = {"name": name, "n_r": n_r, "isolid": bs.isolid, "gap_over_s": bs.gap_over_s, "stfac": bs.stfac,
           "particle_bricks": info["n_particle_bricks"], "substrate_bricks": info["n_bricks"],
           "vol_ratio": info["vol_ratio"], "threads": threads}
    if not res.get("normal"):
        row["failed"] = " ".join((res.get("engine_tail") or res.get("starter_tail", "")).split())[-300:]
        return row
    t, vz, f, appr, _, _ = si.sphere_trace(d, name, info["m_particle"])
    tn = t[1:] / H["t_contact"]
    fn = f / H["F_max"]
    row.update({"peak": float(fn.max()), "t_peak": float(tn[np.argmax(fn)]), "approach": float(appr.max() / H["d_max"]),
                "contact_1pct": s1.contact_end(tn, fn, 1e-2), "rebound": float(vz[-1] / fw.V),
                "a_hertz_over_s": math.sqrt(r1.R * H["d_max"]) / info["s"], "d_hertz_over_s": H["d_max"] / info["s"],
                "cycles": s0.read_cycles(d, name), "engine_s": res["engine_s"], "wall_s": time.perf_counter() - t0})
    row["pass"] = abs(row["peak"] - 1) <= 0.05 and abs(row["approach"] - 1) <= 0.05 and row["rebound"] > 0.9
    np.save(os.path.join(d, "trace.npy"), {"t": tn, "f": fn, "tv": t / H["t_contact"], "v": vz / fw.V,
                                           "appr": appr / H["d_max"]}, allow_pickle=True)
    return row


def main():
    work, out_csv, n_r, gap, stfac = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    threads = int(os.environ.get("THREADS", "8"))
    row = run_case(work, n_r, bp.BSettings(gap_over_s=gap, stfac=stfac), threads=threads)
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
