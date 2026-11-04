"""Does /HEAT/MAT give a temperature on 3D bricks? Confined column of bricks (uniaxial strain) on a rigid wall.

Column 1 x 1 x n_z bricks of edge h, lateral (x, y) motion fixed on all nodes, moving at -V onto /RWALL/PLANE
z = 0. LAW4 + /EOS/GRUNEISEN (nominal copper-like values, feature check only), with and without
/HEAT/MAT (EFRAC) + engine /THERMAL. Prints element temperatures from the animation output.

Usage: python heat3d.py <work_dir>
"""

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import ocdeck as oc  # noqa: E402
import vtkread  # noqa: E402
from ocdeck import _f, _group, _i, _material_cards  # noqa: E402

CU = dict(E=124e9, nu=0.34, rho=8930.0, A=90e6, B=292e6, n=0.31, C=0.025, eps_dot0=1.0, m=1.09, T_melt=1356.0,
          rho_cp=8930 * 385.0, T_r=293.0, c0=3940.0, S1=1.49, gamma0=1.99)


def write(d, name, mat, *, h, n_z, V, t_end, dt_anim, thermal, q=None, dt_scale=None):
    nodes = [(x * h, y * h, k * h) for k in range(n_z + 1) for y in (0, 1) for x in (0, 1)]
    nid = {p: i + 1 for i, p in enumerate(nodes)}

    def n(x, y, k):
        return nid[(x * h, y * h, k * h)]

    bricks = [[n(0, 0, k), n(1, 0, k), n(1, 1, k), n(0, 1, k), n(0, 0, k + 1), n(1, 0, k + 1), n(1, 1, k + 1),
               n(0, 1, k + 1)] for k in range(n_z)]
    s = ["#RADIOSS STARTER", "/BEGIN", name, _i(2026) + _i(0), f"{'kg':>20}{'m':>20}{'s':>20}",
         f"{'kg':>20}{'m':>20}{'s':>20}", "/NODE"]
    s += [_i(i + 1) + _f(x) + _f(y) + _f(z) for i, (x, y, z) in enumerate(nodes)]
    s += ["/BRICK/1"] + ["".join(_i(v) for v in [e + 1, *b]) for e, b in enumerate(bricks)]
    s += ["/PART/1", "column", _i(1) + _i(1) + _i(0)]
    qa, qb = (0.0, 0.0) if q is None else q
    s += ["/PROP/TYPE14/1", "solid", _i(0) * 8 + _f(0.0), _f(qa) + _f(qb) + _f(0.0) * 3, _f(0.0) * 5, _i(0) * 3]
    s += _material_cards(mat)
    s += _group(1, "all", range(1, len(nodes) + 1))
    s += ["/INIVEL/TRA/1", "v", _f(0.0) + _f(0.0) + _f(-V) + _i(1) + _i(0), _f(0.0) + _i(0)]
    s += ["/BCS/1", "uniaxial strain", "   110 000" + _i(0) + _i(1)]
    s += ["/RWALL/PLANE/1", "wall", _i(0) * 2 + _i(1) + _i(0) * 2, _f(0.0) * 4 + _i(0), _f(0.0) * 3,
          _f(0.0) * 2 + _f(1.0)]
    s += ["/TH/PART/1", "part", "DEF", _i(1), "/END"]
    e = ["#RADIOSS ENGINE", f"/RUN/{name}/1", _f(t_end), "/TFILE/4", _f(t_end / 500), "/TH/TITLE",
         "/ANIM/DT", _f(0.0) + _f(dt_anim), "/ANIM/ELEM/TEMP", "/ANIM/ELEM/EPSP", "/ANIM/ELEM/P"]
    if thermal:
        e += ["/THERMAL", _f(1.0)]
    if dt_scale is not None:
        e += ["/DT", _f(dt_scale) + _f(0.0)]
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f"{name}_0000.rad"), "w").write("\n".join(s) + "\n")
    open(os.path.join(d, f"{name}_0001.rad"), "w").write("\n".join(e) + "\n")


def main(work):
    h, n_z, V = 0.5e-6, 20, 500.0
    t_end = 1.5 * n_z * h / CU["c0"]
    for name, efrac, thermal in (("H3A", None, False), ("H3B", 0.9, True), ("H3C", 0.9, False)):
        d = os.path.join(work, name)
        write(d, name, oc.JohnsonCookGruneisen(**CU, heat_efrac=efrac), h=h, n_z=n_z, V=V, t_end=t_end,
              dt_anim=t_end / 6, thermal=thermal)
        info = oc.run(d, name)
        print(name, "/HEAT/MAT" if efrac else "built-in", "+/THERMAL" if thermal else "", "normal", info.get("normal"))
        if not info.get("normal"):
            print("  ", " ".join((info.get("engine_tail") or info.get("starter_tail", "")).split())[-300:])
            continue
        for v in oc.convert_anim(d, name)[1::2]:
            fr = vtkread.read(v)
            keys = {k: fr["cell"][k] for k in fr["cell"] if "Temp" in k or "Plastic" in k}
            txt = "  ".join(f"{k.split('_', 1)[1]}: min {x.min():.4g} med {np.median(x):.4g} max {x.max():.4g}"
                            for k, x in keys.items())
            print(f"   t = {fr['time'] * 1e9:5.2f} ns  {txt}")


if __name__ == "__main__":
    main(sys.argv[1])
