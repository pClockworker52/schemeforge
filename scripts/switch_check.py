"""Switch-radius check of docs/research/switch-check-2026-11-18.md (calibration; spec fixed in 7465e0f).

Fits a(t') = A t'^p to the §25 contact radius (2D quads, Al-Al, R/64, R/128, R/256) over the judged frames,
extrapolates to the time where the fitted edge speed p A t'^(p-1) equals C0, and applies the §25 rule to the
switch radius a_c = A t_c^p.

Input: docs/research/opencourant/results/tl_cal6_p3_series.csv, columns V (m/s), frame, t_ns (ns),
a_R{64,128,256}_um (µm) only. Units inside: µm, ns (1 µm/ns = 1000 m/s).
Usage: python scripts/switch_check.py
"""

import csv
import math
from pathlib import Path

ROWS = Path(__file__).resolve().parents[1] / "docs/research/opencourant/results/tl_cal6_p3_series.csv"
C0 = 5.3055  # µm/ns, P-HG-Al bulk sound speed sqrt(B/rho) (§8.3)
R = 10.0  # µm, particle radius (§8.3 deck)
GAP = 0.001 * R  # µm, initial gap of the §8.3 deck
MESHES = ("R64", "R128", "R256")
JUDGED = {600.0: range(3, 10), 500.0: range(3, 9)}  # frames, driver-check §2
SENSITIVITY = range(3, 7)  # frames 3-6, reported only


def converges(q64: float, q128: float, q256: float) -> bool:
    """§25 rule: |q256-q128| <= 3.5 % |q256| and (|q256-q128| <= 0.8 |q128-q64| or |q128-q64| <= 3.5 % |q128|)."""
    d2 = abs(q256 - q128)
    d1 = abs(q128 - q64)
    return d2 <= 0.035 * abs(q256) and (d2 <= 0.8 * d1 or d1 <= 0.035 * abs(q128))


def fit_power(t: list[float], a: list[float]) -> tuple[float, float]:
    """Unweighted least squares of ln a = ln A + p ln t. Returns (A in µm ns^-p, p)."""
    x = [math.log(v) for v in t]
    y = [math.log(v) for v in a]
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    p = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y, strict=True)) / sum((xi - mx) ** 2 for xi in x)
    return math.exp(my - p * mx), p


def switch(big_a: float, p: float) -> tuple[float, float]:
    """Time t_c (ns) and radius a_c (µm) where p A t^(p-1) = C0; NaN if p >= 1."""
    if p >= 1.0:
        return math.nan, math.nan
    t_c = (p * big_a / C0) ** (1.0 / (1.0 - p))
    return t_c, big_a * t_c**p


def a_rigid(v_ms: float) -> float:
    """Rigid-sphere switch radius R V / sqrt(V^2 + C0^2), µm."""
    v = v_ms / 1000.0
    return R * v / math.sqrt(v * v + C0 * C0)


def main() -> None:
    by_v: dict[float, dict[int, dict[str, str]]] = {}
    with ROWS.open() as fh:
        for row in csv.DictReader(fh):
            by_v.setdefault(float(row["V"]), {})[int(row["frame"])] = row
    ac_judged: dict[float, float] = {}
    overall = True
    for v in sorted(by_v, reverse=True):
        rows = by_v[v]
        t0 = GAP / (v / 1000.0)  # ns
        print(f"\nV = {v:.0f} m/s, t0 = {t0:.4f} ns, a_c,rigid = {a_rigid(v):.4f} um, "
              f"t(frame 3) = {float(rows[3]['t_ns']):.4f} ns")
        res: dict[str, dict[str, tuple[float, float, float, float]]] = {}
        for label, frames in (("judged", JUDGED[v]), ("frames 3-6", SENSITIVITY)):
            res[label] = {}
            for m in MESHES:
                t = [float(rows[f]["t_ns"]) - t0 for f in frames]
                a = [float(rows[f][f"a_{m}_um"]) for f in frames]
                big_a, p = fit_power(t, a)
                t_c, a_c = switch(big_a, p)
                res[label][m] = (big_a, p, t_c, a_c)
                resid = max(abs(big_a * ti**p / ai - 1.0) for ti, ai in zip(t, a, strict=True))
                print(f"  {label:10s} {m:5s} A = {big_a:.4f}  p = {p:.4f}  t_c = {t_c:.4f} ns  "
                      f"a_c = {a_c:.4f} um  a_c/rigid = {a_c / a_rigid(v):.3f}  "
                      f"t_c/t3 = {t_c / float(rows[3]['t_ns']):.3f}  max fit resid = {resid:.3%}")
        q = [res["judged"][m][3] for m in MESHES]
        ok = all(math.isfinite(x) for x in q) and converges(*q)
        overall = overall and ok
        ac_judged[v] = q[2]
        d2 = abs(q[2] - q[1]) / abs(q[2])
        d1 = abs(q[1] - q[0]) / abs(q[1])
        print(f"  rule on a_c: |256-128|/256 = {d2:.2%}, |128-64|/128 = {d1:.2%} -> "
              f"{'converges' if ok else 'does not converge'}")
        for m in MESHES:
            change = res["frames 3-6"][m][3] / res["judged"][m][3] - 1.0
            print(f"  sensitivity {m}: a_c(3-6)/a_c(judged) - 1 = {change:+.2%}")
    if 600.0 in ac_judged and 500.0 in ac_judged:
        ratio = ac_judged[600.0] / ac_judged[500.0]
        print(f"\nR/256 a_c(600)/a_c(500) = {ratio:.4f}; CS-20 ratio sin(beta_c) = "
              f"{a_rigid(600.0) / a_rigid(500.0):.4f} (post hoc, simulation, not a CS-20 test)")
    print(f"\nVERDICT (switch-check §3): {'PASS' if overall else 'FAIL'}")


if __name__ == "__main__":
    main()
