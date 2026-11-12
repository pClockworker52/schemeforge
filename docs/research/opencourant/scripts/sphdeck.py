"""Write and run 3D SPH decks for OpenCourant (verification ladder of opencourant-verification.md section 9).

Geometry: SI units (/BEGIN kg m s, deck version 2026), 3D (/ANALY N2D3D = 0), particles on a cubic net of
spacing s (particle mass rho s^3, one particle per cube of side s, centred in it). The impact direction is -z.

Cards used (Reference Guide 2022, card layouts from the shipped hm_cfg_files):
  /SPHCEL/part   one line per particle: node id, flag 0; no mass on this card (radioss110 sphcel.cfg). A mass
                 here sets the particle type to "mass input" and the starter then ignores the property's h and
                 uses the close-packed default (sqrt(2) m / rho)^(1/3) (starter spinih.F lines 88-93).
  /PROP/TYPE34   mp, qa (quadratic, "beta"), qb (linear, "alpha"), alpha_cs, skew, h_1D / order, h, xi_stab
                 (radioss2026 prop_p34_sph.cfg). OpenCourant replaces qa = 0 by 2 and qb = 0 by 1
                 (hm_read_prop34.F), so "off" needs a tiny value such as 1e-30.
  /SPHBCS/SLIDE  symmetry plane through the origin of a fixed frame, normal to the frame's local X; particles
                 must lie on the positive side. Ghosts are single reflections (spsym.F): one per particle per
                 plane, none across two planes (no corner ghosts).
  /FRAME/FIX     origin, Y' axis, Z' axis (X' = Y' x Z').
  /RWALL/PLANE   frictionless (Slide = 0) rigid plane z = z_wall, normal +z, all particle nodes secondary.

Set-up switch: the environment variable SPH_STAB="xi_stab,alpha_cs,order" overrides these three /PROP/TYPE34
fields for every SPH part of every deck written here, whatever the calling script passes. Unset = the script's own
values (the frozen set-up of section 9.1: 0, 0, 0). SPH_STAB=0.3,0,1 is set-up S' of the sph-contact ladder,
Addendum 1 (artificial stress 0.3, kernel-correction order 1, on all particles).

SPH particles of different parts interact through the kernel like one body (no part filter in the neighbour
search or in spforcp.F); a particle-substrate contact therefore needs a separate method (section 9).
"""

from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass, field

import numpy as np
from ocdeck import OC_ROOT, _env, _f, _group, _i, _material_cards


@dataclass(frozen=True)
class SphProp:
    """/PROP/TYPE34 settings. h is the smoothing length (m); the kernel support radius is 2h."""

    h: float
    qa: float = 2.0  # quadratic artificial viscosity (Monaghan beta); OpenCourant default 2
    qb: float = 1.0  # linear artificial viscosity (Monaghan alpha); OpenCourant default 1
    alpha_cs: float = 0.0  # conservative smoothing of velocities
    order: int = 0  # kernel correction order: -1 none, 0 (default), 1 (not in SPMD)
    xi_stab: float = 0.0  # Monaghan (2000) artificial stress coefficient, n = 4 (spstab.F)
    h_1d: int = 0  # 0: h follows 3D volume change (default)


@dataclass(frozen=True)
class SymPlane:
    """Symmetry plane through `origin` with unit normal `normal` pointing into the particles."""

    origin: tuple[float, float, float]
    normal: tuple[float, float, float]
    kind: str = "SLIDE"


@dataclass
class Body:
    xyz: np.ndarray  # (n, 3) particle positions, m
    mass: float  # kg per particle
    mat: object  # ocdeck material dataclass
    prop: SphProp
    velocity: tuple[float, float, float] = (0.0, 0.0, 0.0)
    title: str = "body"
    fix: str = "000"  # /BCS translations x y z fixed on all particles of the body ('110' = lateral blocked)
    extra: dict = field(default_factory=dict)


def cubic_net(lo, hi, s):
    """Particle centres of a cubic net of spacing s filling the box lo..hi (cells of side s, centred)."""
    ax = [np.arange(lo[k] + 0.5 * s, hi[k] - 0.49 * s, s) for k in range(3)]
    g = np.stack(np.meshgrid(*ax, indexing="ij"), -1).reshape(-1, 3)
    return g


def _frame(fid, origin, normal):
    n = np.asarray(normal, float)
    n = n / np.linalg.norm(n)
    a = np.array([1.0, 0.0, 0.0]) if abs(n[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    y = np.cross(n, a)
    y /= np.linalg.norm(y)
    z = np.cross(n, y)  # then y x z = n
    return [f"/FRAME/FIX/{fid}", f"sym frame {fid}", _f(origin[0]) + _f(origin[1]) + _f(origin[2]),
            _f(y[0]) + _f(y[1]) + _f(y[2]), _f(z[0]) + _f(z[1]) + _f(z[2])]


def write_deck(d, name, bodies: list[Body], *, t_end, dt_th, sym=(), z_wall=None, dt_scale=None,
               dt_anim=None, anim=("P", "EPSP", "VONM", "DENS"), sphglo=None, print_every=-200, extra_engine=(),
               extra_starter=(), th_parts=None, dt_min=0.0):
    s = ["#RADIOSS STARTER", f"# schemeforge SPH deck, written by sphdeck.py: {name}", "/BEGIN", name,
         _i(2026) + _i(0), f"{'kg':>20}{'m':>20}{'s':>20}", f"{'kg':>20}{'m':>20}{'s':>20}", "/NODE"]
    nid, ranges = 0, []
    for b in bodies:
        ranges.append((nid + 1, nid + len(b.xyz)))
        s += [_i(nid + k + 1) + _f(x) + _f(y) + _f(z) for k, (x, y, z) in enumerate(b.xyz)]
        nid += len(b.xyz)
    for p, (b, (a0, a1)) in enumerate(zip(bodies, ranges, strict=True), start=1):
        # mass only in /PROP/TYPE34: a mass on /SPHCEL makes the starter replace h by (sqrt2 m/rho)^(1/3) (spinih.F)
        s += [f"/SPHCEL/{p}"] + [_i(k) + _i(0) for k in range(a0, a1 + 1)]
        s += [f"/PART/{p}", b.title, _i(p) + _i(p) + _i(0)]
        pr = b.prop
        acs, order, xi = pr.alpha_cs, pr.order, pr.xi_stab
        if os.environ.get("SPH_STAB"):  # set-up switch for every SPH part of every deck, see module docstring
            xi, acs, order = (float(v) for v in os.environ["SPH_STAB"].split(","))
        s += [f"/PROP/TYPE34/{p}", f"{b.title} sph", _f(b.mass) + _f(pr.qa) + _f(pr.qb) + _f(acs) + _i(0)
              + _i(pr.h_1d), _i(int(order)) + _f(pr.h) + _f(xi), _f(0.0)]
        mc = _material_cards(b.mat)
        mc[0] = mc[0].rsplit("/", 1)[0] + f"/{p}"
        mc = [c if not c.startswith("/EOS/") else c.rsplit("/", 1)[0] + f"/{p}" for c in mc]
        s += mc
        s += _group(10 + p, f"{b.title} nodes", range(a0, a1 + 1))
        if any(b.velocity):
            s += [f"/INIVEL/TRA/{p}", f"{b.title} velocity", _f(b.velocity[0]) + _f(b.velocity[1])
                  + _f(b.velocity[2]) + _i(10 + p) + _i(0), _f(0.0) + _i(0)]
        if b.fix != "000":
            s += [f"/BCS/{p}", f"{b.title} fixed {b.fix}", f"   {b.fix} 000" + _i(0) + _i(10 + p)]
    for k, pl in enumerate(sym, start=1):
        s += _frame(100 + k, pl.origin, pl.normal)
        s += [f"/SPHBCS/{pl.kind}/{k}", f"symmetry {k}", f"{'X':>10}" + _i(100 + k) + _i(0) + " " * 10 + _i(0)]
    if z_wall is not None:
        s += _group(99, "all particles", range(1, nid + 1))
        s += ["/RWALL/PLANE/1", "rigid wall", _i(0) + _i(0) + _i(99) + _i(0) + _i(0),
              _f(0.0) + _f(0.0) + _f(0.0) + _f(0.0) + _i(0), _f(0.0) + _f(0.0) + _f(z_wall),
              _f(0.0) + _f(0.0) + _f(z_wall + 1.0)]
        s += ["/TH/RWALL/2", "wall", "DEF", _i(1)]
    if sphglo is not None:
        s += ["/SPHGLO", _f(sphglo[0]) + _i(0) + _i(sphglo[1]) + _i(sphglo[2])]
    s += list(extra_starter)  # e.g. a brick substrate with /INTER/TYPE7 (sph_interface.py); ids must not clash
    parts = th_parts or range(1, len(bodies) + 1)
    s += ["/TH/PART/1", "parts", "DEF", "".join(_i(p) for p in parts), "/END"]
    e = ["#RADIOSS ENGINE", f"/RUN/{name}/1", _f(t_end), "/TFILE/4", _f(dt_th), "/TH/TITLE", f"/PRINT/{print_every}"]
    if dt_scale is not None:
        e += ["/DT", _f(dt_scale) + _f(dt_min)]  # dt_min > 0: the run stops below it (time-step collapse)
    if dt_anim:
        e += ["/ANIM/DT", _f(0.0) + _f(dt_anim)] + [f"/ANIM/ELEM/{f}" for f in anim] + ["/ANIM/VECT/VEL"]
    e += list(extra_engine)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f"{name}_0000.rad"), "w").write("\n".join(s) + "\n")
    open(os.path.join(d, f"{name}_0001.rad"), "w").write("\n".join(e) + "\n")
    return ranges


def _capped(cmd, vmem_gb, timeout_s):
    """cmd under a virtual-memory cap, no core dumps and a hard time limit. An OpenCourant engine that runs away
    (e.g. /THERMAL with /HEAT/MAT on the bricks but not on the SPH material: >15 GB in seconds) otherwise gets the
    whole WSL VM OOM-killed; core dumps of GB-sized processes go through Windows' crash capture and take minutes."""
    q = " ".join(f"'{c}'" for c in cmd)
    lim = f"ulimit -c 0; ulimit -v {int(vmem_gb * 1024 * 1024)}"
    return ["bash", "-c", f"{lim}; exec timeout -s KILL {int(timeout_s)} {q}"]


def run(d, name, threads=1, np_mpi=1, vmem_gb=10.0, timeout_s=4 * 3600):
    """Starter + engine. threads = OpenMP threads per process (-nt), np_mpi > 1 uses the MPI engine.
    Both run under a virtual-memory cap of vmem_gb (per process) and a hard limit of timeout_s (_capped)."""
    env, exe = _env(), f"{OC_ROOT}/exec"
    env["OMP_NUM_THREADS"] = str(threads)
    out = {}
    t0 = time.perf_counter()
    r = subprocess.run(_capped([f"{exe}/starter_linux64_gf", "-i", f"{name}_0000.rad", "-np", str(np_mpi)], vmem_gb,
                               timeout_s), cwd=d, env=env,
                       capture_output=True, text=True)
    out["starter_rc"], out["starter_s"], out["starter_tail"] = r.returncode, time.perf_counter() - t0, r.stdout[-800:]
    if r.returncode != 0:
        return out
    t0 = time.perf_counter()
    if np_mpi > 1:
        cmd = ["mpirun", "-np", str(np_mpi), "--bind-to", "none", f"{exe}/engine_linux64_gf_ompi", "-i",
               f"{name}_0001.rad", "-nt", str(threads)]
    else:
        cmd = [f"{exe}/engine_linux64_gf", "-i", f"{name}_0001.rad", "-nt", str(threads)]
    r = subprocess.run(_capped(cmd, vmem_gb, timeout_s), cwd=d, env=env, capture_output=True, text=True)
    out["engine_rc"], out["engine_s"], out["engine_tail"] = r.returncode, time.perf_counter() - t0, r.stdout[-800:]
    out["normal"] = "NORMAL TERMINATION" in r.stdout
    subprocess.run([f"{exe}/th_to_csv_linux64_gf", f"{name}T01"], cwd=d, env=env, capture_output=True)
    return out


def cycles(d, name):
    """Number of cycles from the engine listing (last 'CYCLE' summary line)."""
    txt = open(os.path.join(d, f"{name}_0001.out"), errors="replace").read()
    for ln in txt.splitlines()[::-1]:
        if "NUMBER OF CYCLES" in ln.upper() or "CYCLES" in ln.upper() and ":" in ln:
            digits = [w for w in ln.replace(":", " ").split() if w.isdigit()]
            if digits:
                return int(digits[-1])
    return None
