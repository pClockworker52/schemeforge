"""GIF for CS-13c (setup B, brick particle on brick substrate): one impact run to the dt-collapse stop with many
frames. Section y = 0 (the faces of the elements touching the symmetry plane y = 0, mirrored to negative x),
left: equivalent plastic strain, right: element temperature. The element that stops the run is outlined.
Diagnostic visualisation, outside the protocol.

Usage: python plot_cs13c_gif.py <work_dir> <twin k237|k0|noheat> <n_r> <V> <out_gif> [threads] [frames]
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.collections import PolyCollection

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import cs13c as cc  # noqa: E402
import ocdeck as oc  # noqa: E402
import sphdeck as sd  # noqa: E402
import vtkread  # noqa: E402

SURF, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"


def section(fr, s):
    """Polygons (x, z) of the y = 0 faces of elements touching y = 0, with their element values."""
    X = fr["xyz"]
    c8 = np.array([list(c) for c in fr["cells"]])
    on = np.abs(X[c8, 1]) < 1e-3 * s  # (e, 8)
    keep = on.sum(1) == 4
    polys = []
    for c, m in zip(c8[keep], on[keep], strict=True):
        q = X[c[m]][:, [0, 2]] / cc.R
        cen = q.mean(0)
        q = q[np.argsort(np.arctan2(q[:, 1] - cen[1], q[:, 0] - cen[0]))]
        polys.append(q)
    return polys, keep


def main(work, twin, n_r, V, out_gif, threads=2, n_frames=40):
    n_r, V, threads, n_frames = int(n_r), float(V), int(threads), int(n_frames)
    R, D = cc.R, cc.D
    t_e = 0.25 * D / V
    s = R / n_r
    name = f"G{twin}{n_r:02d}v{int(V):04d}"
    d = os.path.join(work, name)
    dtmin = cc.dt0(work, twin, n_r, threads) / 50
    cc._write(d, name, twin, n_r, V, t_e, dtmin, None)
    # frames every t_e / n_frames (cc._write puts one frame at t_end; rewrite the engine deck's /ANIM/DT)
    eng = os.path.join(d, f"{name}_0001.rad")
    txt = open(eng).read().split("\n")
    txt += ["/ANIM/DT", f"{0.0:>20.6g}{t_e / n_frames:>20.6g}"] + [f"/ANIM/ELEM/{f}" for f in cc.ANIM]
    open(eng, "w").write("\n".join(txt) + "\n")
    res = sd.run(d, name, threads=threads, vmem_gb=8, timeout_s=3600)
    assert res.get("engine_s"), res
    kind, ids, body = cc.stop_info(d, name)
    frames = [vtkread.read(v) for v in oc.convert_anim(d, name)]
    plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                         "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
                         "font.size": 8, "axes.spines.top": False, "axes.spines.right": False})
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), constrained_layout=True)
    ep_max = 1.5
    t_lo, t_hi = 293.0, max(400.0, float(max(f["cell"]["3DELEM_Temperature"].max() for f in frames)))
    cmaps = (plt.cm.viridis, plt.cm.inferno)
    sms = [plt.cm.ScalarMappable(norm=plt.Normalize(0, ep_max), cmap=cmaps[0]),
           plt.cm.ScalarMappable(norm=plt.Normalize(t_lo, t_hi), cmap=cmaps[1])]
    for ax, sm, lab in zip(axs, sms, ("equivalent plastic strain", "element temperature (K)"), strict=True):
        cb = fig.colorbar(sm, ax=ax, shrink=0.8)
        cb.set_label(lab, color=INK2)
        cb.outline.set_visible(False)
    stop_ids = {int(x) for x in ids.split()} if ids else set()

    def draw(i):
        fr = frames[i]
        polys, keep = section(fr, s)
        eid = fr["cell"]["ELEMENT_ID"].astype(int)[keep]
        vals = (fr["cell"]["3DELEM_Plastic_Strain"][keep], fr["cell"]["3DELEM_Temperature"][keep])
        mir = [p * np.array([-1.0, 1.0]) for p in polys]
        last = i == len(frames) - 1
        for ax, v, sm in zip(axs, vals, sms, strict=True):
            ax.clear()
            for pp in (polys, mir):
                ax.add_collection(PolyCollection(pp, array=np.asarray(v), cmap=sm.cmap, norm=sm.norm,
                                                 edgecolors=MUTED, linewidths=0.1))
            if last and stop_ids:
                hit = [p for p, e in zip(polys, eid, strict=True) if e in stop_ids]
                ax.add_collection(PolyCollection(hit, facecolors="none", edgecolors="#e34948", linewidths=1.2))
            ax.set_xlim(-1.3, 1.3)
            ax.set_ylim(-0.45, 0.75)
            ax.set_aspect("equal")
            ax.set_xlabel("x / R (section y = 0, mirrored)")
            ax.set_ylabel("z / R")
        tt = fr["time"] / (D / V)
        in_sec = bool(stop_ids & set(eid.tolist()))
        stop = (f"\nstop: {body} element" + ("" if in_sec else " (not in section)")
                if last and body else "\n")
        axs[0].set_title(f"plastic strain, t = {tt:.3f} D/V{stop}", loc="left", fontsize=8.5)
        axs[1].set_title("temperature", loc="left", fontsize=8.5)
        fig.suptitle(f"CS-13c setup B (brick particle on brick substrate), twin {twin}, s = R/{n_r}, {V:.0f} m/s",
                     x=0.01, ha="left", fontsize=9.5)
        return []

    FuncAnimation(fig, draw, frames=len(frames), blit=False).save(out_gif, writer=PillowWriter(fps=6), dpi=72)
    print(out_gif, len(frames), "frames, stop", kind, ids, body, f"t_stop/(D/V) = {frames[-1]['time'] / (D / V):.4f}")


if __name__ == "__main__":
    main(*sys.argv[1:8])
