"""Driver 1 of docs/research/driver-check-2026-11-17.md: contact radius a(t) and edge speed v_edge = da/dt.

Input: docs/research/opencourant/results/tl_cal6_p3_series.csv (§25 rows; a in µm, t in ns, per speed V in m/s,
one row per output frame). Applies the spec's §25 rule to outputs from the third onward and prints one line per
driver and speed plus the per-output values. Usage: python scripts/driver_check_a.py
"""

import csv
from pathlib import Path

ROWS = Path(__file__).resolve().parents[1] / "docs/research/opencourant/results/tl_cal6_p3_series.csv"
C0 = 5305.5  # m/s, P-HG-Al (§8.3); constant divisor for the edge Mach number
MESHES = ("R64", "R128", "R256")


def converges(q64: float, q128: float, q256: float) -> bool:
    """§25 rule: |q256-q128| <= 3.5 % |q256| and (|q256-q128| <= 0.8 |q128-q64| or |q128-q64| <= 3.5 % |q128|)."""
    d2 = abs(q256 - q128)
    d1 = abs(q128 - q64)
    return d2 <= 0.035 * abs(q256) and (d2 <= 0.8 * d1 or d1 <= 0.035 * abs(q128))


def main() -> None:
    by_v: dict[float, list[dict[str, str]]] = {}
    with ROWS.open() as fh:
        for row in csv.DictReader(fh):
            by_v.setdefault(float(row["V"]), []).append(row)
    for v, rows in sorted(by_v.items()):
        rows.sort(key=lambda r: float(r["t_ns"]))
        t = [float(r["t_ns"]) for r in rows]
        a = {m: [float(r[f"a_{m}_um"]) for r in rows] for m in MESHES}
        # v_edge in m/s: central differences (µm/ns = 1000 m/s); one-sided at the ends
        ve = {}
        for m in MESHES:
            x = a[m]
            d = []
            for i in range(len(x)):
                lo, hi = max(i - 1, 0), min(i + 1, len(x) - 1)
                d.append((x[hi] - x[lo]) / (t[hi] - t[lo]) * 1000.0)
            ve[m] = d
        judged = range(2, len(rows))  # outputs from the third onward
        for name, q in (("a", a), ("v_edge", ve)):
            flags = [converges(q["R64"][i], q["R128"][i], q["R256"][i]) for i in judged]
            frac = sum(flags) / len(flags)
            print(f"V={v:.0f} {name}: {sum(flags)}/{len(flags)} converge ({frac:.2f}); usable={frac >= 0.8}")
            for i, ok in zip(judged, flags, strict=True):
                extra = f" Mach256={q['R256'][i] / C0:.3f}" if name == "v_edge" else ""
                print(f"   t={t[i]:.4f} ns  R64={q['R64'][i]:.4g}  R128={q['R128'][i]:.4g}  "
                      f"R256={q['R256'][i]:.4g}  {'ok' if ok else 'no'}{extra}")


if __name__ == "__main__":
    main()
