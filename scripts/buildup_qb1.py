"""Q-B1 (build-up track): is deposit fracture set by the striking shot or by the stack's history?

Exploratory, post hoc, on seen data (docs/research/data/buildup_reiser2024.csv, digitized from
Reiser2024 Figs. 3b and 5b). Nothing here is a test of a registered hunch.

Comparisons (fixed before computing, 2026-11-07):
(a)  striker: v, v/v_cr and within-stack rank of each fracturing shot; permutation test of the
     mean rank against a random shot of the same stack;
(a') the shot before each fracture, same measures;
(b)  history: mean v of the shots before each fracture, against the intact stacks over the same
     number of shots; sub-v_cr shots before the event;
(c)  stack means over the common window (shots 1-7), intact vs fractured, exact Mann-Whitney.

v_cr = 253 m/s (Au, 16 +- 4 um, HG2019b as quoted by Reiser2024); size-scaled
v_cr(d) = 253 (d/16)^-0.2 (Dowding2020 exponent, as Reiser2024 uses).

Usage: python scripts/buildup_qb1.py [csv]
"""

from __future__ import annotations

import csv
import itertools
import random
import statistics as st
import sys

VCR = 253.0
N_PERM = 20000


def vcr_d(d_um: float) -> float:
    """Size-scaled critical velocity [m/s] for an Au particle of diameter d_um [um]."""
    return VCR * (d_um / 16.0) ** -0.2


def prank(vals: list[float], x: float) -> float:
    """Rank of x among vals, 0 = slowest, 1 = fastest, ties averaged (x must be in vals)."""
    return (sum(v < x for v in vals) + 0.5 * (sum(v == x for v in vals) - 1)) / (len(vals) - 1)


def mann_whitney_exact(a: list[float], b: list[float]) -> tuple[float, float]:
    """U of a over b and the exact one-sided p (P(U >= observed) under random labels)."""
    def u(x, y):
        return sum((i > j) + 0.5 * (i == j) for i in x for j in y)
    obs = u(a, b)
    allv = a + b
    n = len(allv)
    combos = list(itertools.combinations(range(n), len(a)))
    hits = sum(u([allv[i] for i in c], [allv[j] for j in range(n) if j not in c]) >= obs for c in combos)
    return obs, hits / len(combos)


def load(path: str) -> dict[str, list[dict]]:
    stacks: dict[str, list[dict]] = {}
    for r in csv.DictReader(open(path)):
        r = dict(r, v=float(r["v_mps"]), d=float(r["d_um"]), shot=int(r["shot"]), fe=int(r["fracture_event"]))
        stacks.setdefault(r["stack"], []).append(r)
    for s in stacks.values():
        s.sort(key=lambda r: r["shot"])
    return stacks


def main(path: str) -> None:
    S = load(path)
    F = sorted(s for s in S if s.startswith("F"))
    I_ = sorted(s for s in S if s.startswith("I"))
    ev = [(s, r["shot"]) for s in F for r in S[s] if r["fe"]]
    rng = random.Random(1)

    print("(a) striker")
    for s, k in ev:
        r = S[s][k - 1]
        print(f"  {s} shot {k}: v={r['v']:.0f}  v/vcr={r['v'] / VCR:.2f}  v/vcr(d)={r['v'] / vcr_d(r['d']):.2f}"
              f"  d={r['d']}  rank={prank([q['v'] for q in S[s]], r['v']):.2f}")
    evv = [S[s][k - 1]["v"] for s, k in ev]
    other = [r["v"] for s in F for r in S[s] if not r["fe"]]
    print(f"  fracturing shots: mean {st.mean(evv):.0f} m/s (n={len(evv)}); other shots of fractured stacks "
          f"{st.mean(other):.0f} (n={len(other)}); intact-stack shots {st.mean(r['v'] for s in I_ for r in S[s]):.0f}")
    print(f"  fracturing shots below 253 m/s: {sum(v < VCR for v in evv)} of {len(evv)}")
    obs = st.mean(prank([q["v"] for q in S[s]], S[s][k - 1]["v"]) for s, k in ev)
    hits = sum(st.mean(prank([q["v"] for q in S[s]], rng.choice(S[s])["v"]) for s, _ in ev) <= obs
               for _ in range(N_PERM))
    print(f"  mean rank {obs:.2f}; P(random shot rank <= observed) = {hits / N_PERM:.3f}")

    print("(a') preceding shot")
    for s, k in ev:
        p = S[s][k - 2]
        print(f"  {s} shot {k - 1}: v={p['v']:.0f}  v/vcr={p['v'] / VCR:.2f}  d={p['d']}"
              f"  rank={prank([q['v'] for q in S[s]], p['v']):.2f}")
    obs2 = st.mean(prank([q["v"] for q in S[s]], S[s][k - 2]["v"]) for s, k in ev)
    hits = sum(st.mean(prank([q["v"] for q in S[s]], rng.choice(S[s])["v"]) for s, _ in ev) <= obs2
               for _ in range(N_PERM))
    print(f"  mean rank {obs2:.2f}; P(random shot rank <= observed) = {hits / N_PERM:.3f}")

    print("(b) history before each fracture vs intact stacks over the same number of shots")
    for s, k in ev:
        h = S[s][:k - 1]
        ih = [st.mean(q["v"] for q in S[i][:k - 1]) for i in I_]
        print(f"  {s} before shot {k}: mean {st.mean(q['v'] for q in h):.0f} (n={len(h)}), "
              f"below 253: {sum(q['v'] < VCR for q in h)}, below vcr(d): {sum(q['v'] < vcr_d(q['d']) for q in h)};"
              f" intact: {', '.join(f'{x:.0f}' for x in ih)}")

    print("(c) stack means over shots 1-7")
    a = [st.mean(q["v"] for q in S[s][:7]) for s in I_]
    b = [st.mean(q["v"] for q in S[s][:7]) for s in F]
    print("  intact " + ", ".join(f"{s} {x:.0f}" for s, x in zip(I_, a, strict=True)))
    print("  fractured " + ", ".join(f"{s} {x:.0f}" for s, x in zip(F, b, strict=True)))
    u, p = mann_whitney_exact(a, b)
    print(f"  U = {u:.1f} of {len(a) * len(b)}, exact one-sided p = {p:.3f}")
    a = [st.mean(q["v"] for q in S[s]) for s in I_]
    b = [st.mean(q["v"] for q in S[s]) for s in F]
    u, p = mann_whitney_exact(a, b)
    print(f"  (all shots, for comparison: U = {u:.1f}, p = {p:.3f})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "docs/research/data/buildup_reiser2024.csv")
