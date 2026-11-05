"""Interface bracket of hunch CS-11 (docs/research/coldspray-hunch-cs11.md): an SPH sphere on a substrate, quarter
symmetry, normal impact along -z, two setups:

  W (welded)       SPH sphere on an SPH block (cubic net, same spacing s); the bodies couple through the kernel.
  F (frictionless) SPH sphere on a 3D brick block, /INTER/TYPE7, friction 0, the sphere's particles as secondary
                   nodes, the block's top face (z = 0) as the main surface.

Geometry (quarter): block 0 <= x, y <= Lx (Lx = 3R), -Lz <= z <= 0 (Lz = 2R), bottom fixed; symmetry planes x = 0 and
y = 0 (SPH: /SPHBCS/SLIDE at the cell boundaries; bricks: u_x = 0 on x = 0, u_y = 0 on y = 0). Sphere: the
surface-conforming SPH sphere of §9.1 (sph_rung1.sphere), particle mass = sphere mass / N.
  W: block particles at the cell centres of the net, top layer at z = -s/2; lowest sphere particle at z = +s/2,
     so the two lattices are one spacing apart ("touching") at t = 0.
  F: bricks of edge s for x, y <= 1.5R and z >= -1.5R, graded (ratio <= 1.2) outside; lowest sphere particle at
     z = gap, so contact starts at t = 0.

TYPE7 settings (fixed in rung F0): Istf = 1000 (stiffness from the main side, K = Stfac B A^2 / V per segment),
Igap = 1000 (constant gap = Gapmin), Ibag = 0 (default: no closure), Idel = 1000, Inacti = 1000, VIS_S = 0.05 (default critical damping
of the penalty spring), Fric = 0, Ifric = 0.

Reads: sphere centre-of-mass history from /TH/PART (ZMOM), contact force = -d(ZMOM)/dt of the sphere x 4.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ocdeck as oc  # noqa: E402
import sph_rung1 as s1  # noqa: E402
import sphdeck as sd  # noqa: E402
from ocdeck import _f, _group, _i, _material_cards  # noqa: E402

BRICK_NODE0 = 2_000_000  # brick node ids start above this (SPH nodes are 1..N)
BRICK_PART = 50


@dataclass(frozen=True)
class FSettings:
    """Brick element and TYPE7 contact of setup F. Defaults = the values frozen by rung F0 (§10.2)."""

    isolid: int = 17  # /PROP/TYPE14 Isolid: 17 H8C (2x2x2); 24 HEPH and 1 run at a 30x smaller nodal time step
    gap_over_s: float = 0.5  # constant TYPE7 gap / particle spacing (particle surface s/2 outside its centre)
    stfac: float = 10.0  # TYPE7 stiffness scale on the main-side stiffness (Istf = 1000); 1 adds 8 % approach
    q: tuple[float, float] | None = None  # brick bulk viscosity (None = OpenCourant defaults 1.10, 0.05)


def graded(l_uniform, l_total, s, ratio=1.2):
    """Coordinates 0 .. l_total: cells of size s up to l_uniform, then growing by `ratio` (last cell trimmed)."""
    n_u = int(round(l_uniform / s))
    x = list(np.arange(n_u + 1) * s)
    h = s
    while x[-1] < l_total - 1e-12 * l_total:
        h *= ratio
        nxt = x[-1] + h
        if nxt > l_total or l_total - nxt < 0.5 * h:
            nxt = l_total
        x.append(nxt)
    return np.array(x)


def sphere_body(mat, R, n_r, V, z_low, prop):
    """Quarter conforming SPH sphere of radius R, spacing R/n_r, lowest particle centre at z_low."""
    old = s1.r1.R
    s1.r1.R = R
    try:
        s, p = s1.sphere(n_r, "quarter", conform=True)
    finally:
        s1.r1.R = old
    p = p + np.array([0.0, 0.0, z_low])
    m_p = mat.rho * 4 / 3 * math.pi * R**3 / 4 / len(p)
    return s, sd.Body(xyz=p, mass=m_p, mat=mat, prop=prop, velocity=(0.0, 0.0, -V), title="particle")


def _bcs_groups(xyz, ids, lx_tol, fixed_bottom_z, gid0, bcs_id0):
    """/BCS cards: u_x = 0 on x = 0, u_y = 0 on y = 0, all fixed on z = fixed_bottom_z (combined per node)."""
    code = np.zeros((len(xyz), 3), bool)
    code[:, 0] |= np.abs(xyz[:, 0]) < lx_tol
    code[:, 1] |= np.abs(xyz[:, 1]) < lx_tol
    code[np.abs(xyz[:, 2] - fixed_bottom_z) < lx_tol] = True
    cards, k = [], 0
    for c in sorted({tuple(r) for r in code if r.any()}):
        sel = ids[np.all(code == np.array(c), axis=1)]
        txt = "".join("1" if b else "0" for b in c)
        cards += _group(gid0 + k, f"bcs {txt}", sel)
        cards += [f"/BCS/{bcs_id0 + k}", f"block {txt}", f"   {txt} 000" + _i(0) + _i(gid0 + k)]
        k += 1
    return cards


def brick_block(mat, R, s, fs: FSettings, lx_fac=3.0, lz_fac=2.0, sec_group=11):
    """Starter cards of the brick substrate + the TYPE7 interface (secondary = node group `sec_group`)."""
    xs = graded(1.5 * R, lx_fac * R, s)
    zs = -graded(1.5 * R, lz_fac * R, s)[::-1]
    X, Y, Z = np.meshgrid(xs, xs, zs, indexing="ij")
    xyz = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    nx, nz = len(xs), len(zs)
    nid = BRICK_NODE0 + np.arange(len(xyz)).reshape(nx, nx, nz)
    c = ["/NODE"] + [_i(int(k)) + _f(x) + _f(y) + _f(z) for k, (x, y, z) in zip(nid.ravel(), xyz, strict=True)]
    i, j, k = np.meshgrid(np.arange(nx - 1), np.arange(nx - 1), np.arange(nz - 1), indexing="ij")
    i, j, k = i.ravel(), j.ravel(), k.ravel()
    conn = np.stack([nid[i, j, k], nid[i + 1, j, k], nid[i + 1, j + 1, k], nid[i, j + 1, k],
                     nid[i, j, k + 1], nid[i + 1, j, k + 1], nid[i + 1, j + 1, k + 1], nid[i, j + 1, k + 1]], 1)
    c += [f"/BRICK/{BRICK_PART}"] + ["".join(_i(int(x)) for x in (e + 1, *row)) for e, row in enumerate(conn)]
    c += [f"/PART/{BRICK_PART}", "substrate", _i(BRICK_PART) + _i(BRICK_PART) + _i(0)]
    qa, qb = fs.q if fs.q is not None else (0.0, 0.0)
    c += [f"/PROP/TYPE14/{BRICK_PART}", "substrate solid", _i(fs.isolid) + _i(0) * 7 + _f(0.0),
          _f(qa) + _f(qb) + _f(0.0) + _f(0.0) + _f(0.0), _f(0.0) + _f(0.0) + _f(0.0) + _f(0.0) + _f(0.0),
          _i(0) + _i(0) + _i(0)]
    mc = _material_cards(mat)
    mc[0] = mc[0].rsplit("/", 1)[0] + f"/{BRICK_PART}"
    mc = [x if not x.startswith("/EOS/") else x.rsplit("/", 1)[0] + f"/{BRICK_PART}" for x in mc]
    c += mc
    c += _bcs_groups(xyz, nid.ravel(), 1e-3 * s, zs[0], 60, 60)
    # main surface: top faces (z = 0), counter-clockwise seen from +z (outward normal +z)
    it, jt = np.meshgrid(np.arange(nx - 1), np.arange(nx - 1), indexing="ij")
    it, jt, kt = it.ravel(), jt.ravel(), nz - 1
    segs = np.stack([nid[it, jt, kt], nid[it + 1, jt, kt], nid[it + 1, jt + 1, kt], nid[it, jt + 1, kt]], 1)
    c += ["/SURF/SEG/70", "substrate top"] + ["".join(_i(int(x)) for x in (e + 1, *row)) for e, row in enumerate(segs)]
    gap = fs.gap_over_s * s
    c += ["/INTER/TYPE7/71", "particle on substrate frictionless",
          _i(sec_group) + _i(70) + _i(1000) + _i(0) + _i(1000) + " " * 10 + _i(0) + _i(1000) + _i(0) + _i(0),
          _f(0.0) + _f(0.0) + _f(0.0) + " " * 20 + _i(0) + _i(0),
          _f(0.0) + _f(0.0) + _f(0.0) + _f(0.0) + _i(0) + _i(0),
          _f(fs.stfac) + _f(0.0) + _f(gap) + _f(0.0) + _f(0.0),
          " " * 7 + "000" + " " * 20 + _i(1000) + _f(0.0) + _f(0.0) + _f(0.0),
          _i(0) + _i(0) + _f(0.0) + _i(0) + _i(0) + _i(0) + _f(0.0) + _i(0)]
    c += ["/TH/INTER/72", "contact", "DEF", _i(71)]
    info = {"n_bricks": len(conn), "n_brick_nodes": len(xyz), "nx": nx, "nz": nz, "gap": gap,
            "top_z": float(zs[-1]), "sub_xyz": xyz, "sub_ids": nid.ravel()}
    return c, info


def sph_block(mat, R, s, prop, lx_fac=3.0, lz_fac=2.0):
    """SPH substrate body (cubic net) and the starter cards fixing its bottom layer (added after the bodies)."""
    p = sd.cubic_net((0.0, 0.0, -lz_fac * R), (lx_fac * R, lx_fac * R, 0.0), s)
    return sd.Body(xyz=p, mass=mat.rho * s**3, mat=mat, prop=prop, title="substrate")


def th_nodes(tid, title, ids, var=("X", "Y", "VX", "VY")):
    """/TH/NODE card for the node ids (one line per node)."""
    return [f"/TH/NODE/{tid}", title, "".join(f"{v:<10}" for v in var)] + [_i(int(k)) + _i(0) for k in ids]


def write_case(d, name, setup, mat, R, n_r, V, *, t_end, dt_th, fs: FSettings | None = None, dt_anim=None,
               anim=("P", "EPSP", "VONM"), dt_scale=0.3, dt_min=0.0, th_sub=None, w_dist_over_s=1.0,
               extra_starter=(), extra_engine=()):
    """Write the deck of one W or F case; returns a dict of geometry facts.

    extra_starter / extra_engine: cards appended to the starter (after the bodies and the substrate) and engine decks.
    th_sub = (depth, radius): also write a /TH/NODE (X, Y, VX, VY) for every particle node and for the substrate
    nodes with z >= -depth and sqrt(x^2 + y^2) <= radius (jetting metric J of CS-11)."""
    fs = fs or FSettings()
    s = R / n_r
    prop = sd.SphProp(h=2 ** (1 / 6) * s)
    planes = [sd.SymPlane((0, 0, 0), (1, 0, 0)), sd.SymPlane((0, 0, 0), (0, 1, 0))]
    if setup == "F":
        s_, sph = sphere_body(mat, R, n_r, V, fs.gap_over_s * s, prop)
        extra, info = brick_block(mat, R, s, fs)
        bodies, th_parts = [sph], (1, BRICK_PART)
        info.update(n_particles=len(sph.xyz), n_sub_particles=0, m_particle=sph.mass * len(sph.xyz))
    elif setup == "W":
        # lowest sphere particle w_dist_over_s * s above the top substrate layer (z = -s/2); 1 = lattice contact
        s_, sph = sphere_body(mat, R, n_r, V, (w_dist_over_s - 0.5) * s, prop)
        blk = sph_block(mat, R, s, prop)
        n1 = len(sph.xyz)
        bottom = n1 + 1 + np.nonzero(blk.xyz[:, 2] < blk.xyz[:, 2].min() + 0.1 * s)[0]
        extra = _group(60, "substrate bottom", bottom) + ["/BCS/60", "substrate bottom fixed",
                                                          "   111 000" + _i(0) + _i(60)]
        bodies, th_parts = [sph, blk], None
        info = {"n_particles": n1, "n_sub_particles": len(blk.xyz), "m_particle": sph.mass * n1, "gap": 0.0,
                "sub_xyz": blk.xyz, "sub_ids": n1 + 1 + np.arange(len(blk.xyz))}
    else:
        raise ValueError(setup)
    if th_sub is not None:
        depth, rad = th_sub
        sx = info["sub_xyz"]
        sel = (sx[:, 2] >= -depth) & (np.hypot(sx[:, 0], sx[:, 1]) <= rad)
        info["th_sub_ids"] = info["sub_ids"][sel]
        extra = list(extra) + th_nodes(81, "particle nodes", range(1, len(sph.xyz) + 1))
        extra += th_nodes(82, "substrate nodes near the surface", info["th_sub_ids"])
    sd.write_deck(d, name, bodies, t_end=t_end, dt_th=dt_th, sym=planes, dt_scale=dt_scale, dt_anim=dt_anim,
                  anim=anim, extra_starter=list(extra) + list(extra_starter), th_parts=th_parts, dt_min=dt_min,
                  extra_engine=extra_engine)
    info["s"] = s
    info["particle_xyz0"] = sph.xyz
    return info


def sphere_trace(d, name, m_particle, sym_factor=4.0):
    """t (s), sphere centre-of-mass velocity vz (m/s), contact force F (N, full sphere), approach (m) from t = 0."""
    head, a = oc.read_th(d, name)
    t = a[:, 0]
    zm = [i for i, h in enumerate(head) if h.endswith("ZMOM")][0]  # first part = the sphere
    zmom = a[:, zm] * sym_factor
    vz = zmom / (m_particle * sym_factor)
    f = np.diff(zmom) / np.diff(t)
    appr = -np.concatenate([[0.0], np.cumsum(0.5 * (vz[1:] + vz[:-1]) * np.diff(t))])
    return t, vz, f, appr, head, a
