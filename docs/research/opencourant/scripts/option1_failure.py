"""Where and why do the option-1 runs stop? For each run: the element that controls the time step at the last
printed cycle, its part, its distance to the contact edge, and its shape (smallest interior angle, aspect ratio)
in the last animation frame.

Also writes the evaluation table: edge plastic strain at t_eval = min(t_stop, t_pen) (at failure if the run
fails during penetration, else at the end of penetration) and its maximum over [0, t_eval].

Usage: python option1_failure.py <work_dir> <option1_csv> [<eval_csv>]
"""

import csv
import glob
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "openradioss", "scripts"))
import vtkread  # noqa: E402

R = 10e-6


def last_controlling(out_path):
    rows = []
    for ln in open(out_path, errors="replace"):
        w = ln.split()
        try:
            if len(w) >= 10 and w[0].isdigit() and "E" in w[2].upper() and w[3].isalpha():
                rows.append((int(w[0]), float(w[1]), float(w[2]), w[3], int(w[4])))
        except ValueError:
            pass
    return rows


def shape(p):
    """Smallest interior angle (deg) and aspect ratio (longest / shortest edge) of a quad p (4, 2)."""
    angs, edges = [], []
    for k in range(4):
        a, b, c = p[k - 1], p[k], p[(k + 1) % 4]
        u, v = a - b, c - b
        angs.append(np.degrees(np.arccos(np.clip(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)), -1, 1))))
        edges.append(np.linalg.norm(c - b))
    return min(angs), max(edges) / max(min(edges), 1e-30)


def evaluate(work, csv_path, out_csv):
    out = []
    rows = list(csv.DictReader(open(csv_path)))
    # reference penetration time per velocity: from the coarsest run that reached the end of penetration
    t_ref = {}
    for mesh in ("coarse", "medium", "fine"):
        for r in rows:
            if r["mesh"] == mesh and r["t_pen_ns"] not in ("", "nan") and float(r["t_pen_ns"]) == float(r["t_pen_ns"]):
                t_ref.setdefault(r["V"], float(r["t_pen_ns"]) * 1e-9)
    for r in rows:
        name = f"A{int(float(r['V'])):04d}{r['mesh'][0].upper()}"
        em = np.load(os.path.join(work, name, "edge.npy"), allow_pickle=True)
        t = np.array([e["t"] for e in em])
        t_stop, t_pen = float(r["t_stop_ns"]) * 1e-9, t_ref[r["V"]]
        failed = not r["stop_reason"].startswith("reached")
        t_eval = min(t_stop, t_pen)
        k = int(np.nonzero(t <= t_eval + 1e-15)[0][-1])
        sel = slice(0, k + 1)
        out.append({"V": r["V"], "mesh": r["mesh"], "h_um": r["h_um"], "failed": failed,
                    "t_pen_ref_over_D_V": t_pen * float(r["V"]) / (2 * R),
                    "t_stop_over_t_pen_ref": min(t_stop / t_pen, 99.0) if failed else float("nan"), "t_eval_over_D_V": t[k] * float(r["V"]) / (2 * R),
                    "a_over_R": em[k]["a"] / R, "ep_edge_particle": em[k]["ep_edge_particle"],
                    "ep_edge_substrate": em[k]["ep_edge_substrate"],
                    "ep_edge_particle_max": max(e["ep_edge_particle"] for e in em[sel]),
                    "ep_edge_substrate_max": max(e["ep_edge_substrate"] for e in em[sel])})
        print({kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in out[-1].items()})
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)


def main(work, csv_path, eval_csv=None):
    if eval_csv:
        evaluate(work, csv_path, eval_csv)
    for r in csv.DictReader(open(csv_path)):
        name = f"A{int(float(r['V'])):04d}{r['mesh'][0].upper()}"
        d = os.path.join(work, name)
        rows = last_controlling(os.path.join(d, f"{name}_0001.out"))
        if not rows:
            continue
        cyc, t, dt, etype, eid = rows[-1]
        fr = vtkread.read(sorted(glob.glob(os.path.join(d, f"{name}A*.vtk")))[-1])
        ids = fr["cell"]["ELEMENT_ID"].astype(int)
        k = int(np.nonzero(ids == eid)[0][0]) if (ids == eid).any() else None
        n_p = int(r["particle_el"])
        em = np.load(os.path.join(d, "edge.npy"), allow_pickle=True)
        a = em[-1]["a"]
        if k is not None:
            p = fr["xyz"][fr["cells"][k], 1:3]
            c = p.mean(0)
            ang, ar = shape(p)
            where = f"{'particle' if eid <= n_p else 'substrate'} el {eid}: centroid r = {c[0] / R:.3f} R, " \
                    f"z = {c[1] / R:+.3f} R, distance to contact edge {np.hypot(c[0] - a, c[1]) / R:.3f} R, " \
                    f"min angle {ang:.1f} deg, aspect {ar:.1f}"
        else:
            where = f"{etype} {eid} (not in the last frame)"
        print(f"{name}: {r['stop_reason']}, t_stop = {float(r['t_stop_over_D_V']):.3f} D/V; last printed cycle {cyc} "
              f"(t = {t * float(r['V']) / (2 * R):.3f} D/V), dt = {dt:.3g} (dt0 = {float(r['dt0']):.3g}); "
              f"controlling {where}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
