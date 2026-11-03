"""Option 1 feature check: LAW4 (Johnson-Cook) + /EOS/GRUNEISEN on axisymmetric quads, unconfined plate at 500 m/s.

Material values are nominal copper-like numbers for a feature check only (not verified, not for results).
Temperature comes from LAW4's built-in adiabatic update (no /HEAT/MAT; see opencourant-verification.md).
Writes a GIF of plastic strain and temperature on the deformed mesh (mirrored about the axis).

Usage: python opt1_jc_gruneisen.py <work_dir> <out_gif>
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import ocdeck as oc  # noqa: E402
import vtkread  # noqa: E402

CU = dict(E=124e9, nu=0.34, rho=8930.0, A=90e6, B=292e6, n=0.31, C=0.025, eps_dot0=1.0, m=1.09, T_melt=1356.0,
          rho_cp=8930 * 385.0, T_r=293.0, c0=3940.0, S1=1.49, gamma0=1.99)
L, V = 10e-6, 500.0
SURF, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
BLUE_SEQ = LinearSegmentedColormap.from_list("b", ["#cde2fb", "#6da7ec", "#256abf", "#0d366b"])
ORANGE_SEQ = LinearSegmentedColormap.from_list("o", ["#fbe3d6", "#f2a27f", "#eb6834", "#a23a12"])


def main(work, out_gif):
    name = "J7"
    d = os.path.join(work, name)
    oc.write_plate_deck(d, name, oc.JohnsonCookGruneisen(**CU, heat_efrac=None), thickness=L, radius=L, n_z=50,
                        n_r=50, velocity=V, t_end=5 * L / CU["c0"], dt_th=1e-11, dt_anim=0.25e-9, confine_r=False,
                        q=None, anim_fields=("P", "EPSP", "TEMP", "VONM"))
    info = oc.run(d, name)
    print({k: v for k, v in info.items() if "tail" not in k})
    frames = [vtkread.read(v) for v in oc.convert_anim(d, name)]
    n_el = 50 * 50
    ep_max = max(f["cell"]["2DELEM_Plastic_Strain"][:n_el].max() for f in frames)
    t_max = max(f["cell"]["2DELEM_Temperature"][:n_el].max() for f in frames)
    print("frames", len(frames), "eps_p max", ep_max, "T max", t_max)
    plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                         "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
                         "font.size": 8})
    r_ext = 1e6 * max(f["xyz"][:, 1].max() for f in frames)
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 4.6), constrained_layout=True)
    norms = (Normalize(0, np.ceil(ep_max)), Normalize(293, 100 * np.ceil(t_max / 100)))
    fields = ("2DELEM_Plastic_Strain", "2DELEM_Temperature")
    for ax, nm, cm, lab in zip(axs, norms, (BLUE_SEQ, ORANGE_SEQ), ("equiv. plastic strain (–)", "temperature (K)"),
                               strict=True):
        cb = fig.colorbar(plt.cm.ScalarMappable(norm=nm, cmap=cm), ax=ax, shrink=0.9, pad=0.01, aspect=12)
        cb.set_label(lab, color=INK2)

    def draw(i):
        fr = frames[i]
        for ax, f, nm, cm in zip(axs, fields, norms, (BLUE_SEQ, ORANGE_SEQ), strict=True):
            ax.clear()
            rz = fr["xyz"][:, 1:3] * 1e6
            for s in (1.0, -1.0):
                polys = [rz[c] * np.array([s, 1.0]) for c in fr["cells"][:n_el]]
                ax.add_collection(PolyCollection(polys, array=fr["cell"][f][:n_el], cmap=cm, norm=nm,
                                                 edgecolors="none"))
            ax.axhline(0, color=INK2, lw=1.2)
            ax.set_xlim(-1.05 * r_ext, 1.05 * r_ext)
            ax.set_ylim(-0.5, 10.5)
            ax.set_aspect("equal")
            ax.set_xlabel("r (µm)")
        for ax in axs:
            ax.set_ylabel("z (µm)")
        axs[0].set_title(f"Cu-like JC + Grüneisen plate, {V:.0f} m/s, t = {fr['time'] * 1e9:4.1f} ns", loc="left",
                         fontsize=8.5)
        return []

    FuncAnimation(fig, draw, frames=range(0, len(frames), 2), blit=False).save(out_gif, writer=PillowWriter(fps=6),
                                                                              dpi=72)


if __name__ == "__main__":
    main(*sys.argv[1:3])
