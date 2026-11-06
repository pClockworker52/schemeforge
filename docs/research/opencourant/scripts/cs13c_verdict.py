"""CS-13c: apply the frozen verdict rule (coldspray-hunch-cs13c.md) to the pass-1 and pass-2 CSVs of cs13c.py, print
the tables for opencourant-verification.md §13 and draw the figure.

Rule (tolerance 6 % for R/32 -> R/48):
  Supported if at >= 2 of 3 velocities: conductive t_f changes <= 6 % (or neither run fails), conductive P2 changes
    <= 6 % in both bodies, and the k0 twin fails at least one of these two.
  Refuted if (a) at all three velocities conductive t_f falls by > 6 % and P2 changes by > 6 % in either body, or
    (b) conductive and k0 twins agree within 6 % in t_f and P2 (both bodies) at every velocity and spacing.
  Inconclusive otherwise, or if a rung failed, or if a run needed for the verdict failed check E.

Usage: python cs13c_verdict.py <pass1.csv> <pass2.csv> <out_png>
"""

import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

TOL = 0.06
VS = (500.0, 800.0, 1100.0)
NS = (16, 24, 32, 48)
SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
COL = {"k237": "#2a78d6", "k0": "#eb6834", "noheat": "#52514e"}


def rel(a, b):
    return (b - a) / a


def load(p1, p2):
    r1 = {(r["twin"], int(r["n_r"]), float(r["V"])): r for r in csv.DictReader(open(p1))}
    r2 = {(r["twin"], int(r["n_r"]), float(r["V"])): r for r in csv.DictReader(open(p2))}
    return r1, r2


def conv(r1, r2, twin, V):
    a, b = r1[(twin, 32, V)], r1[(twin, 48, V)]
    fa, fb = a["failed_collapse"] == "True", b["failed_collapse"] == "True"
    dt = rel(float(a["t_stop_ns"]), float(b["t_stop_ns"]))
    dp = rel(float(r2[(twin, 32, V)]["P2_particle"]), float(r2[(twin, 48, V)]["P2_particle"]))
    ds = rel(float(r2[(twin, 32, V)]["P2_substrate"]), float(r2[(twin, 48, V)]["P2_substrate"]))
    tf_ok = (not fa and not fb) or abs(dt) <= TOL
    p2_ok = abs(dp) <= TOL and abs(ds) <= TOL
    return {"dt": dt, "dp": dp, "ds": ds, "tf_ok": tf_ok, "p2_ok": p2_ok, "falls": dt < -TOL,
            "p2_moves": abs(dp) > TOL or abs(ds) > TOL}


def main(p1, p2, out):
    r1, r2 = load(p1, p2)
    e_ok = all(r["E1_pass"] == "True" and r["E2_pass"] in ("True", "") for r in list(r1.values()) + list(r2.values())
               if r["twin"] in ("k237", "k0"))
    print("check E passed in every twin run:", e_ok)
    print("\nR/32 -> R/48 per velocity (conductive | k0):")
    sup = 0
    ref_a = True
    for V in VS:
        c, z = conv(r1, r2, "k237", V), conv(r1, r2, "k0", V)
        ctrl = not (z["tf_ok"] and z["p2_ok"])
        ok = c["tf_ok"] and c["p2_ok"] and ctrl
        sup += ok
        ref_a &= c["falls"] and c["p2_moves"]
        print(f"  {V:.0f} m/s: t_f {c['dt']:+.1%} | {z['dt']:+.1%};  P2 particle {c['dp']:+.1%} | {z['dp']:+.1%};"
              f"  P2 substrate {c['ds']:+.1%} | {z['ds']:+.1%};  supported-clauses met: {ok}")
    agree = []
    for V in VS:
        for n in NS:
            a, b = r1[("k237", n, V)], r1[("k0", n, V)]
            q, w = r2[("k237", n, V)], r2[("k0", n, V)]
            d = (rel(float(b["t_stop_ns"]), float(a["t_stop_ns"])),
                 rel(float(w["P2_particle"]), float(q["P2_particle"])),
                 rel(float(w["P2_substrate"]), float(q["P2_substrate"])))
            agree.append(max(abs(x) for x in d))
            print(f"  twins {V:.0f} m/s R/{n}: t_f {d[0]:+.2%}, P2 particle {d[1]:+.2%}, P2 substrate {d[2]:+.2%}")
    ref_b = max(agree) <= TOL
    print(f"\nlargest twin difference: {max(agree):.2%}")
    print(f"supported at {sup} of 3 velocities; refuted (a): {ref_a}; refuted (b): {ref_b}")
    verdict = ("inconclusive (check E)" if not e_ok else "supported" if sup >= 2 else
               "refuted" if (ref_a or ref_b) else "inconclusive")
    print("VERDICT:", verdict)

    plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                         "text.color": INK, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
                         "font.size": 8, "axes.spines.top": False, "axes.spines.right": False})
    fig, axs = plt.subplots(3, 3, figsize=(11, 8.2), constrained_layout=True, sharex=True)
    for j, V in enumerate(VS):
        D_V = 15e-6 / V
        for twin, mk, ls in (("k237", "o", "-"), ("k0", "s", "--")):
            x = [1 / n for n in NS]
            axs[0, j].plot(x, [float(r1[(twin, n, V)]["t_stop_ns"]) * 1e-9 / D_V for n in NS], color=COL[twin],
                           marker=mk, ms=5, lw=1.4, ls=ls, label=f"{twin}")
            axs[1, j].plot(x, [float(r2[(twin, n, V)]["P2_particle"]) for n in NS], color=COL[twin], marker=mk,
                           ms=5, lw=1.4, ls=ls, label=twin)
            axs[2, j].plot(x, [float(r2[(twin, n, V)]["P2_substrate"]) for n in NS], color=COL[twin], marker=mk,
                           ms=5, lw=1.4, ls=ls, label=twin)
        nh = r1.get(("noheat", 16, V))
        if nh:
            axs[0, j].scatter([1 / 16], [float(nh["t_stop_ns"]) * 1e-9 / D_V], color=COL["noheat"], marker="x", s=40,
                              zorder=4, label="no /HEAT/MAT (reported only)")
        axs[0, j].set_title(f"{V:.0f} m/s", loc="left")
        for i in range(3):
            axs[i, j].grid(color=GRID, lw=0.6)
            axs[i, j].set_ylim(bottom=0)
        axs[2, j].set_xlabel("spacing s / R")
        axs[2, j].set_xticks([1 / n for n in NS], [f"1/{n}" for n in NS])
        axs[2, j].set_xlim(0, 0.07)
    axs[0, 0].set_ylabel("P1: failure time t_f / (D/V)")
    axs[1, 0].set_ylabel("P2 particle: edge ε_p at t_c")
    axs[2, 0].set_ylabel("P2 substrate: edge ε_p at t_c")
    axs[0, 0].legend(frameon=False, fontsize=7)
    fig.suptitle(f"CS-13c, setup B (brick particle on brick substrate), Al–Al R = 7.5 µm: conductive (k = 237) vs "
                 f"k = 0 twin. Verdict: {verdict}", x=0.01, ha="left", fontsize=9.5)
    fig.savefig(out, dpi=130)


if __name__ == "__main__":
    main(*sys.argv[1:4])
