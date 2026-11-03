"""Write, run and read OpenCourant decks for the axisymmetric plate-on-rigid-wall cases (verification rungs).

Geometry (SI units, /BEGIN kg m s): /ANALY N2D3D = 1, quads in the YZ plane, Y = radius r, Z = axis.
Plate 0 <= r <= radius, 0 <= z <= thickness; frictionless rigid plane wall at z = 0 (/RWALL/PLANE, Slide = 0),
normal +z, all nodes as secondary nodes; initial velocity -V along z (the plate starts in contact).
Optional u_r = 0 on all nodes (uniaxial strain), as in the JAX rung 0 (impact_axisym.confined_plate_on_rigid_wall).

Material blocks:
    Elastic(E, nu, rho)                                         /MAT/LAW1
    PlasticLinear(E, nu, rho, sigma_y, E_t)                     /MAT/LAW2 with n = 1, c = 0, m = 0
    JohnsonCookGruneisen(...)                                   /MAT/LAW4 + /EOS/GRUNEISEN (+ /HEAT/MAT)

Bulk viscosity: OpenCourant replaces q_a = q_b = 0 by its defaults 1.10 and 0.05 (Reference Guide 2022,
/PROP/TYPE14). `q=None` keeps those defaults; `q=(qa, qb)` sets them (use a tiny value such as 1e-30 for "off").
"""

from __future__ import annotations

import csv
import os
import subprocess
import time
from dataclasses import dataclass

import numpy as np

OC_ROOT = os.path.expanduser("~/opt/opencourant/latest-20261011/OpenCourant")


@dataclass(frozen=True)
class Elastic:
    E: float  # Pa
    nu: float
    rho: float  # kg/m^3


@dataclass(frozen=True)
class PlasticLinear:
    """Bilinear elastic-plastic von Mises solid (LAW2 with n = 1, no rate or temperature terms)."""

    E: float
    nu: float
    rho: float
    sigma_y: float  # Pa
    hardening: float  # Pa, LAW2 'b' with n = 1: sigma = sigma_y + b * eps_p


@dataclass(frozen=True)
class JohnsonCookGruneisen:
    """LAW4 (Johnson-Cook) with /EOS/GRUNEISEN and optional /HEAT/MAT (adiabatic heating)."""

    E: float
    nu: float
    rho: float
    A: float  # Pa
    B: float  # Pa
    n: float
    C: float
    eps_dot0: float  # 1/s
    m: float
    T_melt: float  # K
    rho_cp: float  # J/(m^3 K)
    T_r: float  # K
    c0: float  # m/s, Us = c0 + S1 up
    S1: float
    gamma0: float
    a: float = 0.0
    heat_efrac: float | None = None  # Taylor-Quinney fraction for /HEAT/MAT; None = no /HEAT/MAT card


def _f(x: float) -> str:
    return f"{x:20.12g}"


def _i(x: int) -> str:
    return f"{x:10d}"


def _material_cards(mat) -> list[str]:
    if isinstance(mat, Elastic):
        return ["/MAT/LAW1/1", "plate", _f(mat.rho), _f(mat.E) + _f(mat.nu)]
    if isinstance(mat, PlasticLinear):
        return [
            "/MAT/LAW2/1", "plate", _f(mat.rho),
            _f(mat.E) + _f(mat.nu) + _i(0),
            _f(mat.sigma_y) + _f(mat.hardening) + _f(1.0) + _f(0.0) + _f(0.0),
            _f(0.0) + _f(0.0) + _i(0) + _i(0) + _f(0.0) + _f(0.0),
            _f(0.0) + _f(0.0) + _f(0.0) + _f(0.0),
        ]
    if isinstance(mat, JohnsonCookGruneisen):
        cards = [
            "/MAT/LAW4/1", "plate", _f(mat.rho),
            _f(mat.E) + _f(mat.nu),
            _f(mat.A) + _f(mat.B) + _f(mat.n) + _f(0.0) + _f(0.0),
            _f(-1e30),
            _f(mat.C) + _f(mat.eps_dot0) + _f(mat.m) + _f(mat.T_melt) + _f(0.0),
            _f(mat.rho_cp) + " " * 40 + _f(mat.T_r),
            "/EOS/GRUNEISEN/1", "plate eos",
            _f(mat.c0) + _f(mat.S1) + _f(0.0) + _f(0.0),
            _f(mat.gamma0) + _f(mat.a) + _f(0.0),
            _f(0.0) + _f(0.0),
        ]
        if mat.heat_efrac is not None:
            cards += [
                "/HEAT/MAT/1",
                _f(mat.T_r) + _f(mat.rho_cp) + _f(0.0) + _f(0.0),
                _f(0.0) + _f(0.0) + _f(0.0) + _f(mat.heat_efrac),
            ]
        return cards
    raise TypeError(mat)


def plate_mesh(radius: float, thickness: float, n_r: int, n_z: int):
    """Nodes (n, 2) as (r, z) and quads (e, 4) 1-based ids, counter-clockwise in (r, z) (normal +x)."""
    r = np.linspace(0.0, radius, n_r + 1)
    z = np.linspace(0.0, thickness, n_z + 1)
    rr, zz = np.meshgrid(r, z, indexing="ij")
    rz = np.stack([rr.ravel(), zz.ravel()], axis=1)
    idx = np.arange(1, (n_r + 1) * (n_z + 1) + 1).reshape(n_r + 1, n_z + 1)
    quads = np.stack([idx[:-1, :-1].ravel(), idx[1:, :-1].ravel(), idx[1:, 1:].ravel(), idx[:-1, 1:].ravel()], 1)
    return rz, quads


def _group(gid: int, title: str, ids) -> list[str]:
    out = [f"/GRNOD/NODE/{gid}", title]
    ids = list(ids)
    for k in range(0, len(ids), 10):
        out.append("".join(_i(int(x)) for x in ids[k : k + 10]))
    return out


def write_plate_deck(path_root: str, name: str, mat, *, thickness: float, radius: float, n_z: int, n_r: int,
                     velocity: float, t_end: float, dt_th: float, dt_anim: float | None = None,
                     confine_r: bool = True, q: tuple[float, float] | None = (1e-30, 1e-30),
                     anim_fields: tuple[str, ...] = ("P", "EPSP", "VONM"),
                     dt_scale: float | None = None, ismstr: int = 0,
                     thermal: bool = False) -> tuple[str, str]:
    """Write <name>_0000.rad and <name>_0001.rad into directory path_root; return both paths."""
    rz, quads = plate_mesh(radius, thickness, n_r, n_z)
    nn = len(rz)
    s = ["#RADIOSS STARTER", f"# schemeforge rung deck, written by ocdeck.py: {name}",
         "/BEGIN", name, _i(2026) + _i(0),
         f"{'kg':>20}{'m':>20}{'s':>20}", f"{'kg':>20}{'m':>20}{'s':>20}",
         "/ANALY", _i(1) + _i(0) + _i(0),
         "/NODE"]
    s += [_i(k + 1) + _f(0.0) + _f(r) + _f(z) for k, (r, z) in enumerate(rz)]
    s += ["/QUAD/1"] + ["".join(_i(x) for x in [e + 1, *q4]) for e, q4 in enumerate(quads)]
    s += ["/PART/1", "plate", _i(1) + _i(1) + _i(0)]
    qa, qb = (0.0, 0.0) if q is None else q
    s += ["/PROP/TYPE14/1", "plate solid", _i(0) + _i(ismstr) + _i(0) * 6 + _f(0.0), _f(qa) + _f(qb) + _f(0.0) + _f(0.0) + _f(0.0),
          _f(0.0) + _f(0.0) + _f(0.0) + _f(0.0) + _f(0.0), _i(0) + _i(0) + _i(0)]
    s += _material_cards(mat)
    s += _group(1, "all nodes", range(1, nn + 1))
    s += ["/INIVEL/TRA/1", "impact velocity", _f(0.0) + _f(0.0) + _f(-velocity) + _i(1) + _i(0),
          _f(0.0) + _i(0)]
    axis = [k + 1 for k, (r, _) in enumerate(rz) if r == 0.0]
    s += _group(2, "axis nodes", axis)
    s += ["/BCS/1", "axis: u_r = 0", "   110 000" + _i(0) + _i(2)]
    if confine_r:
        others = [k + 1 for k, (r, _) in enumerate(rz) if r != 0.0]
        s += _group(3, "confined nodes", others)
        s += ["/BCS/2", "confinement: u_r = 0", "   110 000" + _i(0) + _i(3)]
    else:
        s += _group(3, "off-axis nodes", [k + 1 for k, (r, _) in enumerate(rz) if r != 0.0])
        s += ["/BCS/2", "out-of-plane x fixed", "   100 000" + _i(0) + _i(3)]
    s += ["/RWALL/PLANE/1", "rigid wall z=0", _i(0) + _i(0) + _i(1) + _i(0) + _i(0),
          _f(0.0) + _f(0.0) + _f(0.0) + _f(0.0) + _i(0),
          _f(0.0) + _f(0.0) + _f(0.0),
          _f(0.0) + _f(0.0) + _f(1.0)]
    s += ["/TH/PART/1", "part", "DEF", _i(1)]
    s += ["/TH/RWALL/2", "wall", "DEF", _i(1)]
    s += ["/END"]
    e = ["#RADIOSS ENGINE", f"/RUN/{name}/1", _f(t_end), "/TFILE/4", _f(dt_th), "/TH/TITLE", "/PRINT/-100",
         "/PARITH/ON"]
    if thermal:  # engine /THERMAL: switches on the thermal analysis that /HEAT/MAT needs
        e += ["/THERMAL", _f(1.0)]
    if dt_scale is not None:  # /DT: scale factor on the critical time step (default 0.9)
        e += ["/DT", _f(dt_scale) + _f(0.0)]
    if dt_anim:
        e += ["/ANIM/DT", _f(0.0) + _f(dt_anim)]
        e += [f"/ANIM/ELEM/{f}" for f in anim_fields]
        e += ["/ANIM/VECT/VEL"]
    os.makedirs(path_root, exist_ok=True)
    p0, p1 = os.path.join(path_root, f"{name}_0000.rad"), os.path.join(path_root, f"{name}_0001.rad")
    with open(p0, "w") as fh:
        fh.write("\n".join(s) + "\n")
    with open(p1, "w") as fh:
        fh.write("\n".join(e) + "\n")
    return p0, p1


def _env() -> dict:
    env = dict(os.environ)
    env.update(OPENCOURANT_PATH=OC_ROOT, RAD_CFG_PATH=f"{OC_ROOT}/hm_cfg_files",
               RAD_H3D_PATH=f"{OC_ROOT}/extlib/h3d/lib/linux64", OMP_STACKSIZE="400m", OMP_NUM_THREADS="1",
               LD_LIBRARY_PATH=f"{OC_ROOT}/extlib/hm_reader/linux64/:" + env.get("LD_LIBRARY_PATH", ""))
    return env


def run(run_dir: str, name: str) -> dict:
    """Run starter + engine (1 process, 1 thread) in run_dir; convert the time history to CSV."""
    env, exe = _env(), f"{OC_ROOT}/exec"
    out = {}
    t0 = time.perf_counter()
    r = subprocess.run([f"{exe}/starter_linux64_gf", "-i", f"{name}_0000.rad", "-np", "1"], cwd=run_dir, env=env,
                       capture_output=True, text=True)
    out["starter_rc"], out["starter_s"] = r.returncode, time.perf_counter() - t0
    out["starter_tail"] = r.stdout[-600:]
    if r.returncode != 0:
        return out
    t0 = time.perf_counter()
    r = subprocess.run([f"{exe}/engine_linux64_gf", "-i", f"{name}_0001.rad"], cwd=run_dir, env=env,
                       capture_output=True, text=True)
    out["engine_rc"], out["engine_s"] = r.returncode, time.perf_counter() - t0
    out["engine_tail"] = r.stdout[-600:]
    out["normal"] = "NORMAL TERMINATION" in r.stdout
    subprocess.run([f"{exe}/th_to_csv_linux64_gf", f"{name}T01"], cwd=run_dir, env=env, capture_output=True)
    return out


def read_th(run_dir: str, name: str) -> tuple[list[str], np.ndarray]:
    rows = list(csv.reader(open(os.path.join(run_dir, f"{name}T01.csv"))))
    return [h.strip() for h in rows[0]], np.array(rows[1:], float)


def convert_anim(run_dir: str, name: str) -> list[str]:
    """gunzip + anim_to_vtk for every animation file; returns VTK paths in time order."""
    import glob
    import gzip
    import shutil

    env, exe = _env(), f"{OC_ROOT}/exec"
    paths = []
    for g in sorted(glob.glob(os.path.join(run_dir, f"{name}A[0-9][0-9][0-9]*"))):
        plain = g[:-3] if g.endswith(".gz") else g
        if g.endswith(".gz"):
            with gzip.open(g, "rb") as fi, open(plain, "wb") as fo:
                shutil.copyfileobj(fi, fo)
        vtk = plain + ".vtk"
        with open(vtk, "w") as fo:
            subprocess.run([f"{exe}/anim_to_vtk_linux64_gf", plain], cwd=run_dir, env=env, stdout=fo)
        paths.append(vtk)
    return sorted(set(paths))
