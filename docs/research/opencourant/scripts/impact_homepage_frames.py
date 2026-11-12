"""Particle on a like substrate (Ta or Ti-6Al-4V), two impact velocities (He/N2 vs H2/N2), as playback frames for prallwerk.de.

Not a verification rung and not a cold-spray result: an illustration for the homepage.

Set-up: setup W of sph_interface.py (opencourant-verification.md section 10), reused unchanged: surface-conforming
quarter SPH sphere on an SPH block (cubic net, same spacing s, 3R x 3R x 2R quarter, bottom fixed), symmetry planes
x = 0 and y = 0, h = 2^(1/6) s, dt scale 0.3. Only change: the block is 4R x 4R x 3.5R (BLOCK_LX, BLOCK_LZ below).

KNOWN DEFECT, accepted only for this illustration: SPH particles of different parts interact through the kernel as
one body (sphdeck.py; section 9). The interface cannot separate and carries tension and shear, so the particle
sticks wherever it touches. This is the open epistemic hole of the SPH route (W0 fails), not a bonding model.
For the homepage, Peter decided (2026-11-07) to assume adhesion on impact, and the defect is accepted for that
reason only. Nothing here says whether, where or how a Ta particle bonds.

Other limits: adiabatic (no /HEAT/MAT: an SPH part with /HEAT/MAT overheats, section 12); no verification of plastic
SPH impacts at about 1 km/s exists in this ladder; R/16 only.

Particle and substrate: Ta, particle diameter D_UM (default 10 um).
Material P-HG-Ta (docs/research/data/properties.csv; HG2018a preprint, arXiv 1612.08081, Extended Data Table 1,
printed values): rho = 16690 kg/m^3, T_m = 3290 K, c_p = 140.2 J/(kg K), G = 69 GPa, nu = 0.34, C0 = 3461.7 m/s
(sqrt(B/rho), as the preprint uses it), s = 1.2, gamma0 = 1.61, JC A = 684.5 MPa, B = 205.3 MPa, n = 0.78,
C = 0.043, m = 0.344, reference strain rate 3500 1/s, T_ref = 298 K. E = 2 G (1 + nu) = 184.9 GPa (the table gives
B, G and nu, not E). LAW4 + /EOS/GRUNEISEN.

Velocities: nozzle exit velocities of a Ta particle from the 1D model in VCS-H2-Nozzle-Designer
(pr/generate_plots.py::solve_nozzle: T0 = 673 K, P0 = 60 bar, throat radius 0.9 mm, divergent length 250 mm,
80/20 by mass), table VEL below.

Output JSON (compact, for inline embedding): per run two point sets fixed at t = 0, the particle slice 0 < y < s and
the substrate slice 0 < y < s cut to x < SUB_X, z > -SUB_Z (x > 0 only; the page mirrors it). Positions quantised
to uint8 over [0, XMAX] x [ZMIN, ZMAX] in units of R, equivalent plastic strain to uint8 over [0, EPS_MAX];
frames base64-encoded, bytes per point (x, z, eps).

Materials: MAT=ta (default, P-HG-Ta below) or MAT=ti64 (Ti-6Al-4V, Khamsepour et al. 2022, see TI64).

Usage (WSL): [MAT=ta|ti64] [D_UM=10] [PACK_ONLY=1] python impact_homepage_frames.py <work_dir> <out_json> [n_r] [threads]
PACK_ONLY=1 re-packs the frames of an earlier run in <work_dir> without running the engine again.
"""

import base64
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import ocdeck as oc  # noqa: E402
import sph_interface as si  # noqa: E402
import sphdeck as sd  # noqa: E402
import vtkread  # noqa: E402

# 1D-model nozzle exit velocities (m/s) by material and diameter (um): (He/N2, H2/N2), same set-up as above
VEL = {"ta": {10: (1211.0, 1384.0), 20: (949.0, 1046.0), 30: (825.0, 896.0), 45: (722.0, 776.0)},
       "ti64": {10: (1618.0, 1996.0), 20: (1347.0, 1584.0), 30: (1200.0, 1382.0), 45: (1071.0, 1215.0)}}
MAT = os.environ.get("MAT", "ta")
D_UM = int(os.environ.get("D_UM", "10"))
R = D_UM * 0.5e-6
G, NU = 69e9, 0.34
TA = oc.JohnsonCookGruneisen(E=2 * G * (1 + NU), nu=NU, rho=16690.0, A=684.5e6, B=205.3e6, n=0.78, C=0.043,
                             eps_dot0=3500.0, m=0.344, T_melt=3290.0, rho_cp=16690.0 * 140.2, T_r=298.0,
                             c0=3461.7, S1=1.2, gamma0=1.61, heat_efrac=None)
# Ti-6Al-4V: Khamsepour, Moreau, Dolatabadi, J. Therm. Spray Technol. 31 (2022) 70-83, Table 1 (their refs 30-31):
# rho = 4430 kg/m^3, G = 41.9 GPa, JC A = 862 MPa, B = 331 MPa, n = 0.34, C = 0.012, m = 1.1, T_m = 1903 K,
# T_r = 298 K, c_p = 536 J/(kg K), c0 = 5130 m/s, s = 1.03, Gamma0 = 1.23.
# Not in that table, ASSUMED: nu = 0.342 (handbook value for Ti-6Al-4V), reference strain rate 1 1/s (standard JC form).
G_TI, NU_TI = 41.9e9, 0.342
TI64 = oc.JohnsonCookGruneisen(E=2 * G_TI * (1 + NU_TI), nu=NU_TI, rho=4430.0, A=862e6, B=331e6, n=0.34, C=0.012,
                               eps_dot0=1.0, m=1.1, T_melt=1903.0, rho_cp=4430.0 * 536.0, T_r=298.0, c0=5130.0,
                               S1=1.03, gamma0=1.23, heat_efrac=None)
MATERIAL = {"ta": TA, "ti64": TI64}[MAT]
RUNS = {"he": VEL[MAT][D_UM][0], "h2": VEL[MAT][D_UM][1]}
T_END = 2.0 * D_UM * 1e-6 / VEL[MAT][D_UM][0]  # s, 2 D/V for He (16.5 ns for Ta 10 um)
N_FRAMES = 20
XMAX, ZMIN, ZMAX, EPS_MAX = 3.2, -1.9, 2.1, 3.0
SUB_X, SUB_Z = 3.1, 1.7  # substrate window shown, units of R
# Larger block than sph_interface's default 3R x 2R: at 10 um the crater reaches -1.65 R and the rim jets 2.9 R,
# too close to the fixed bottom and the free side faces. Same cubic net and settings otherwise.
BLOCK_LX, BLOCK_LZ = 4.0, 3.5
_sph_block = si.sph_block
si.sph_block = lambda mat, R_, s, prop: _sph_block(mat, R_, s, prop, lx_fac=BLOCK_LX, lz_fac=BLOCK_LZ)


def run_one(work, key, v, n_r, threads):
    name = f"{MAT.upper()}W{key.upper()}D{D_UM:02d}N{n_r:03d}"
    d = os.path.join(work, name)
    info = si.write_case(d, name, "W", MATERIAL, R, n_r, v, t_end=T_END, dt_th=T_END / 400, dt_anim=T_END / N_FRAMES,
                         anim=("P", "EPSP"))
    if os.environ.get("PACK_ONLY"):  # re-pack an existing run (deck rewritten identically, results kept)
        res = {"normal": True, "engine_s": None}
    else:
        res = sd.run(d, name, threads=threads)
    print(key, {k: res.get(k) for k in ("starter_rc", "engine_rc", "normal", "engine_s")}, flush=True)
    if not res.get("normal"):
        print(res.get("starter_tail", ""), res.get("engine_tail", ""), sep="\n")
        raise SystemExit(f"{name}: no normal termination")
    frames = [vtkread.read(f) for f in oc.convert_anim(d, name)]
    stats = {"n_particle_quarter": int(info["n_particles"]), "n_substrate_quarter": int(info["n_sub_particles"]),
             "s_over_R": 1 / n_r, "cycles": sd.cycles(d, name), "engine_s": res.get("engine_s")}
    return frames, info, stats


def _slice_ids(info, n1):
    s = info["s"]
    p = info["particle_xyz0"]
    part = 1 + np.nonzero(p[:, 1] < s)[0]
    q = info["sub_xyz"]
    sub = info["sub_ids"][(q[:, 1] < s) & (q[:, 0] < SUB_X * R) & (q[:, 2] > -SUB_Z * R)]
    return part.astype(int), sub.astype(int)


def _quant(fr, ids):
    pos = {int(k): j for j, k in enumerate(fr["point"]["NODE_ID"].astype(int))}
    cid = {int(k): j for j, k in enumerate(fr["cell"]["ELEMENT_ID"].astype(int))}
    xyz = np.array([fr["xyz"][pos[k]] if k in pos else (np.nan,) * 3 for k in ids]) / R
    e = np.array([fr["cell"]["SPHELEM_Plastic_Strain"][cid[k]] if k in cid else 0.0 for k in ids])
    qx = np.clip(np.nan_to_num(xyz[:, 0] / XMAX * 255, nan=255), 0, 255).astype(np.uint8)
    qz = np.clip(np.nan_to_num((xyz[:, 2] - ZMIN) / (ZMAX - ZMIN) * 255, nan=255), 0, 255).astype(np.uint8)
    qe = np.clip(e / EPS_MAX * 255, 0, 255).astype(np.uint8)
    out_of_box = int(((xyz[:, 0] > XMAX) | (xyz[:, 2] > ZMAX) | (xyz[:, 2] < ZMIN)).sum())
    return np.stack([qx, qz, qe], 1).tobytes(), float(np.nanmax(e)), out_of_box, xyz


def pack(frames, info):
    part, sub = _slice_ids(info, info["n_particles"])
    ids = np.concatenate([part, sub])
    out, eps_max, oob = [], 0.0, 0
    for fr in frames:
        b, em, ob, xyz = _quant(fr, ids)
        eps_max, oob = max(eps_max, em), max(oob, ob)
        out.append({"t_ns": round(fr["time"] * 1e9, 2), "d": base64.b64encode(b).decode()})
    pz = xyz[: len(part)]
    shape = {"particle_x_max_over_R": float(np.nanmax(pz[:, 0])), "particle_z_max_over_R": float(np.nanmax(pz[:, 2])),
             "substrate_z_min_over_R": float(np.nanmin(xyz[len(part):, 2]))}
    return {"n_particle": int(len(part)), "n_substrate": int(len(sub)), "frames": out, "eps_max_seen": eps_max,
            "max_points_out_of_box": oob, "final_shape": shape}


def main(work, out_json, n_r=16, threads=8):
    n_r, threads = int(n_r), int(threads)
    data = {"box": {"xmax": XMAX, "zmin": ZMIN, "zmax": ZMAX, "eps_max": EPS_MAX, "unit_um": R * 1e6},
            "d_um": D_UM, "material": {"ta": "Ta on Ta, P-HG-Ta (HG2018a)",
                                                     "ti64": "Ti-6Al-4V on Ti-6Al-4V (Khamsepour 2022)"}[MAT], "n_r": n_r, "runs": {}}
    for key, v in RUNS.items():
        frames, info, stats = run_one(work, key, v, n_r, threads)
        packed = pack(frames, info)
        packed.update(v=v, stats=stats)
        data["runs"][key] = packed
        print(key, stats, {k: packed[k] for k in ("n_particle", "n_substrate", "eps_max_seen",
                                                  "max_points_out_of_box", "final_shape")}, flush=True)
    with open(out_json, "w") as fo:
        json.dump(data, fo, separators=(",", ":"))
    print("wrote", out_json, os.path.getsize(out_json), "bytes")


if __name__ == "__main__":
    main(*sys.argv[1:5])
