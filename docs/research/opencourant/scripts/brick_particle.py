"""Setup B of hunch CS-13c (docs/research/coldspray-hunch-cs13c.md): a brick particle on a brick substrate, quarter
symmetry, normal impact along -z, two /INTER/TYPE7 contacts (each body's nodes secondary on the other's surface),
friction 0, no heat transfer across the contact.

Particle mesh (quarter O-grid, ogrid_quarter_sphere): index lattice i, j in [0, N], k in [-N, N] with N = Nc + M.
For a lattice point p (index units) let rho = |p|_inf / N and u = p / |p|_inf (a point of the unit cube surface).
The tangential components of u are mapped equiangularly (u_t -> tan(pi/4 u_t)), so the cells along the sphere
surface subtend equal angles. The point is placed on the ray through u at radius
    r = (rho / rho_c) r_in(u)                                    for rho <= rho_c = Nc / N (core)
    r = r_in(u) + (rho - rho_c) / (1 - rho_c) (R - r_in(u))      for rho > rho_c (M shell layers)
with the core boundary r_in(u) = c |u|^(1/2) (c = CORE R: a rounded cube, so the shell is not thin at the cube
corners). The lowest point (the pole, contact point) is a face centre of the -z shell, where cells are regular:
tangential edge (pi/2) R / (2 Nc) and radial edge (R - c) / M, both set to about s.
Substrate: si.brick_block (edge s for x, y <= 1.5 R and z >= -1.5 R, graded 1.2 outside, bottom fixed).

Both bodies: /PROP/TYPE14 Isolid (17, as frozen in §10.2). The lowest particle node starts at z = gap, so contact
starts at t = 0. TYPE7 as in sph_interface (Istf = 1000, Igap = 1000 constant gap, friction 0), gap and Stfac set by
rung B0.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sph_interface as si  # noqa: E402
import sphdeck as sd  # noqa: E402
from ocdeck import _f, _group, _i, _material_cards  # noqa: E402

CORE = 0.5  # core half-size c / R
P_PART, P_ELEM0 = 1, 5_000_000  # particle part / material / property id; particle brick ids start above this
SUB_SURF, SUB_INTER = 70, 71  # from si.brick_block
P_SURF, P_INTER = 75, 76


@dataclass(frozen=True)
class BSettings:
    """Brick element and TYPE7 contacts of setup B (frozen by rung B0)."""

    isolid: int = 17
    gap_over_s: float = 0.1
    stfac: float = 10.0


def ogrid_quarter_sphere(R, s):
    """Quarter sphere x, y >= 0 of radius R centred at the origin. Returns (xyz (n, 3), conn (e, 8) node indices
    0-based, outer faces (f, 4) node indices oriented outward, lattice info)."""
    nc = max(2, int(round(math.pi / 2 * R / s / 2)))  # half the cells across a cube face: (pi/2) R / (2 nc) = s
    m = max(2, int(round((1 - CORE) * R / s)))
    n = nc + m
    ii = np.arange(0, n + 1)
    kk = np.arange(-n, n + 1)
    gi, gj, gk = np.meshgrid(ii, ii, kk, indexing="ij")
    p = np.stack([gi, gj, gk], -1).reshape(-1, 3).astype(float)
    inf = np.abs(p).max(axis=1)
    xyz = np.zeros_like(p)
    nz = inf > 0
    u = p[nz] / inf[nz, None]
    dom = np.abs(u) >= 1 - 1e-12  # dominant component(s): stay at +-1
    u = np.where(dom, u, np.tan(math.pi / 4 * u))
    un = np.linalg.norm(u, axis=1)
    r_in = CORE * R * np.sqrt(un)
    rho = inf[nz] / n
    rc = nc / n
    r = np.where(rho <= rc, rho / rc * r_in, r_in + (rho - rc) / (1 - rc) * (R - r_in))
    xyz[nz] = u / un[:, None] * r[:, None]
    nid = np.arange(len(p)).reshape(n + 1, n + 1, 2 * n + 1)
    a, b, c = np.meshgrid(np.arange(n), np.arange(n), np.arange(2 * n), indexing="ij")
    a, b, c = a.ravel(), b.ravel(), c.ravel()
    conn = np.stack([nid[a, b, c], nid[a + 1, b, c], nid[a + 1, b + 1, c], nid[a, b + 1, c],
                     nid[a, b, c + 1], nid[a + 1, b, c + 1], nid[a + 1, b + 1, c + 1], nid[a, b + 1, c + 1]], 1)
    faces = []
    q = np.arange(n)
    A, B = np.meshgrid(q, q, indexing="ij")
    A, B = A.ravel(), B.ravel()
    # outer faces: i = n (normal +x), j = n (+y), k = -n (-z), k = +n (+z); oriented counter-clockwise seen from out
    A2, C = np.meshgrid(q, np.arange(2 * n), indexing="ij")
    A2, C = A2.ravel(), C.ravel()
    faces += list(np.stack([nid[n, A2, C], nid[n, A2 + 1, C], nid[n, A2 + 1, C + 1], nid[n, A2, C + 1]], 1))
    faces += list(np.stack([nid[A2, n, C], nid[A2, n, C + 1], nid[A2 + 1, n, C + 1], nid[A2 + 1, n, C]], 1))
    faces += list(np.stack([nid[A, B, 0], nid[A, B + 1, 0], nid[A + 1, B + 1, 0], nid[A + 1, B, 0]], 1))
    faces += list(np.stack([nid[A, B, 2 * n], nid[A + 1, B, 2 * n], nid[A + 1, B + 1, 2 * n], nid[A, B + 1, 2 * n]], 1))
    return xyz, conn, np.array(faces), {"nc": nc, "m": m, "n": n}


def hex_volumes(xyz, conn):
    """Signed hexahedron volumes (5-tetrahedron split is not exact for warped hexes; use the 6-tet split)."""
    x = xyz[conn]
    tets = [(0, 1, 3, 4), (1, 2, 3, 6), (1, 4, 5, 6), (3, 4, 6, 7), (1, 3, 4, 6)]
    v = np.zeros(len(conn))
    for t in tets:
        a, b, c, d = (x[:, k] for k in t)
        v += np.einsum("ij,ij->i", b - a, np.cross(c - a, d - a)) / 6
    return v


def write_case(d, name, mat, R, n_r, V, *, t_end, dt_th, bs: BSettings | None = None, dt_anim=None,
               anim=("EPSP",), dt_scale=0.3, dt_min=0.0, extra_starter=(), extra_engine=(), heat=None):
    """Deck of one setup-B case. heat = callable(mat_id) -> /HEAT/MAT cards, applied to both bodies (or None)."""
    bs = bs or BSettings()
    s = R / n_r
    gap = bs.gap_over_s * s
    xyz, conn, faces, lat = ogrid_quarter_sphere(R, s)
    vol = hex_volumes(xyz, conn)
    assert vol.min() > 0, f"inverted particle brick: min volume {vol.min()}"
    xyz = xyz + np.array([0.0, 0.0, R + gap])
    ids = np.arange(1, len(xyz) + 1)
    c = ["/NODE"] + [_i(int(k)) + _f(x) + _f(y) + _f(z) for k, (x, y, z) in zip(ids, xyz, strict=True)]
    c += [f"/BRICK/{P_PART}"] + ["".join(_i(int(x)) for x in (P_ELEM0 + e + 1, *(row + 1)))
                                 for e, row in enumerate(conn)]
    c += [f"/PART/{P_PART}", "particle", _i(P_PART) + _i(P_PART) + _i(0)]
    c += [f"/PROP/TYPE14/{P_PART}", "particle solid", _i(bs.isolid) + _i(0) * 7 + _f(0.0), _f(0.0) * 5,
          _f(0.0) * 5, _i(0) * 3]
    mc = _material_cards(mat)
    mc[0] = mc[0].rsplit("/", 1)[0] + f"/{P_PART}"
    mc = [x if not x.startswith("/EOS/") else x.rsplit("/", 1)[0] + f"/{P_PART}" for x in mc]
    c += mc
    c += _group(11, "particle nodes", ids)
    c += [f"/INIVEL/TRA/{P_PART}", "particle velocity", _f(0.0) + _f(0.0) + _f(-V) + _i(11) + _i(0), _f(0.0) + _i(0)]
    # symmetry: u_x = 0 on x = 0, u_y = 0 on y = 0 (particle)
    for k, (axis, code) in enumerate(((0, "100"), (1, "010")), start=0):
        on = ids[np.abs(xyz[:, axis]) < 1e-6 * s]
        both = ids[(np.abs(xyz[:, 0]) < 1e-6 * s) & (np.abs(xyz[:, 1]) < 1e-6 * s)]
        sel = np.setdiff1d(on, both)
        c += _group(12 + k, f"particle sym {code}", sel) + [f"/BCS/{12 + k}", f"particle {code}",
                                                             f"   {code} 000" + _i(0) + _i(12 + k)]
    both = ids[(np.abs(xyz[:, 0]) < 1e-6 * s) & (np.abs(xyz[:, 1]) < 1e-6 * s)]
    c += _group(14, "particle axis", both) + ["/BCS/14", "particle 110", "   110 000" + _i(0) + _i(14)]
    c += [f"/SURF/SEG/{P_SURF}", "particle outer surface"] + ["".join(_i(int(x)) for x in (e + 1, *(f + 1)))
                                                             for e, f in enumerate(faces)]
    fs = si.FSettings(isolid=bs.isolid, gap_over_s=bs.gap_over_s, stfac=bs.stfac)
    sub, info = si.brick_block(mat, R, s, fs, sec_group=11)
    c += sub
    top = info["sub_ids"][np.abs(info["sub_xyz"][:, 2]) < 1e-6 * s]
    c += _group(15, "substrate top nodes", top)
    c += [f"/INTER/TYPE7/{P_INTER}", "substrate on particle frictionless",
          _i(15) + _i(P_SURF) + _i(1000) + _i(0) + _i(1000) + " " * 10 + _i(0) + _i(1000) + _i(0) + _i(0),
          _f(0.0) + _f(0.0) + _f(0.0) + " " * 20 + _i(0) + _i(0),
          _f(0.0) + _f(0.0) + _f(0.0) + _f(0.0) + _i(0) + _i(0),
          _f(bs.stfac) + _f(0.0) + _f(gap) + _f(0.0) + _f(0.0),
          " " * 7 + "000" + " " * 20 + _i(1000) + _f(0.0) + _f(0.0) + _f(0.0),
          _i(0) + _i(0) + _f(0.0) + _i(0) + _i(0) + _i(0) + _f(0.0) + _i(0)]
    c += ["/TH/INTER/77", "contact 2", "DEF", _i(P_INTER)]
    if heat is not None:
        c += heat(P_PART) + heat(si.BRICK_PART)
    c += list(extra_starter)
    eng = list(extra_engine) + (["/THERMAL", _f(1.0)] if heat is not None else [])
    sd.write_deck(d, name, [], t_end=t_end, dt_th=dt_th, dt_scale=dt_scale, dt_anim=dt_anim, anim=anim,
                  extra_starter=c, extra_engine=eng, th_parts=(P_PART, si.BRICK_PART), dt_min=dt_min)
    m_q = float(vol.sum() * mat.rho)
    return {"s": s, "gap": gap, "n_particle_bricks": len(conn), "n_particle_nodes": len(xyz),
            "n_bricks": info["n_bricks"], "m_particle": m_q, "lattice": lat, "vol_ratio": float(vol.sum() /
            (math.pi / 3 * R**3)), "particle_xyz0": xyz, "sub_xyz": info["sub_xyz"], "sub_ids": info["sub_ids"],
            "particle_faces": faces + 1}
