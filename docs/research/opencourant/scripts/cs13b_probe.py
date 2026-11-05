"""CS-13b, step before the 24 runs: can setup F run with conduction in the bricks and an adiabatic SPH particle?

Setup F as frozen (§10.2, cs11_sweep.py), R = 7.5 um, s = R/16, 800 m/s, to t_e = 0.25 D/V with the dt-collapse
stop dt0/50. Variants (all engine runs capped, sphdeck.run):
  adi        no /HEAT/MAT, no /THERMAL (the adiabatic twin: LAW4 temperature from the element internal energy)
  cond_pk0   /THERMAL; bricks /HEAT/MAT k = 237 W/(m K), EFRAC 1; particle /HEAT/MAT k = 0, EFRAC 1 (no conduction)
  cond_pe0   as cond_pk0, particle EFRAC = 0 (no heat source in the particle)
The variant the protocol literally asks for (/HEAT/MAT on the bricks only) is not run: the engine then grows past
15 GB within seconds and the WSL VM is OOM-killed (2026-11-05, bisected in a separate session).

Reported per variant: stop time / (D/V), the element type named in the dt-collapse message, max particle and brick
temperature and plastic strain in the last frame, and the particle temperature percentiles.

Usage: python cs13b_probe.py <work_dir> <out_csv>
"""

import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import cs11_sweep as cs  # noqa: E402
import h0_sph  # noqa: E402
import ocdeck as oc  # noqa: E402
import sph_interface as si  # noqa: E402
import sphdeck as sd  # noqa: E402
import vtkread  # noqa: E402
from ocdeck import _f  # noqa: E402

THERMAL = ["/THERMAL", _f(1.0), "/ANIM/NODA/TEMP"]


def heat(mat_id, k, efrac):
    c = h0_sph.heat_cards(mat_id, k=k)
    c[2] = c[2][:60] + _f(efrac)
    return c


VARIANTS = {"adi": ([], []),
            "cond_pk0": (heat(si.BRICK_PART, h0_sph.K_AL, 1.0) + heat(1, 0.0, 1.0), THERMAL),
            "cond_pe0": (heat(si.BRICK_PART, h0_sph.K_AL, 1.0) + heat(1, 0.0, 0.0), THERMAL)}


def run(work, variant, n_r=16, V=800.0):
    R, D = cs.R, cs.D
    s, t_e = R / n_r, 0.25 * D / V
    name = f"P{n_r:02d}{variant.replace('_', '')}"
    d = os.path.join(work, name)
    starter, engine = VARIANTS[variant]
    si.write_case(d, name, "F", cs.AL, R, n_r, V, t_end=t_e, dt_th=t_e / 100, fs=cs.F_FROZEN, dt_anim=t_e / 10,
                  anim=("EPSP", "TEMP"), dt_min=cs.DT_SPH_PER_M * s / 50, extra_starter=starter,
                  extra_engine=engine)
    res = sd.run(d, name, threads=8, vmem_gb=6, timeout_s=900)
    f = vtkread.read(oc.convert_anim(d, name)[-1])
    c = f["cell"]
    sph = c["PART_ID"] == 1
    msg = [ln.split("FOR", 1)[1].split() for ln in open(os.path.join(d, f"{name}_0001.out"), errors="replace")
           if "DTMIN FOR" in ln]
    Tp = c["SPHELEM_Temperature"][sph]
    return {"variant": variant, "n_r": n_r, "V": V, "normal": res.get("normal"), "engine_s": res.get("engine_s"),
            "t_stop_over_D_V": f["time"] / (D / V), "stop_element": msg[0][0] if msg else "",
            "stop_ids": " ".join(sorted({m[-1] for m in msg})),
            "T_particle_max": float(Tp.max()), "T_particle_p50": float(np.percentile(Tp, 50)),
            "T_particle_p99": float(np.percentile(Tp, 99)), "n_particle_above_Tmelt": int((Tp > 933.0).sum()),
            "n_particle": int(sph.sum()), "epsp_particle_max": float(c["SPHELEM_Plastic_Strain"][sph].max()),
            "T_brick_max": float(c["3DELEM_Temperature"][~sph].max()),
            "epsp_brick_max": float(c["3DELEM_Plastic_Strain"][~sph].max())}


def main():
    work, out_csv = sys.argv[1:3]
    rows = [run(work, v) for v in VARIANTS]
    for r in rows:
        print({k: (round(x, 4) if isinstance(x, float) else x) for k, x in r.items()}, flush=True)
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
