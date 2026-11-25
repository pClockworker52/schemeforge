"""Zoo γ-sweep for Target D (DECISIONS 2026-11-25): every contact zoo medium with its stiffness scale γ multiplied
by fixed factors, evaluated as zoo references, not as candidates.

Rule (Target D draft, item 1): a candidate counts only if no zoo member at any of these scale factors meets
the D thresholds together. This guards against a candidate that only rescales γ, since ψ = c γ ψ_zoo passes every
constraint.

Each sweep point is a candidate-style file: the zoo member's source with `psi_medium` renamed, plus a wrapper that
calls it with γ × FACTOR. The import rules still hold, because nothing is imported from the zoo at run time. The
files go to candidates/gamma_sweep/ (gitignored). They are registered with origin "zoo" and the id
zoo-medium-<member>-g<factor>.

Usage (promo needs the held-out seed, so it runs on Peter's machine):
    uv run --extra contact python scripts/contact_gamma_sweep.py --suite promo
    uv run --extra contact python scripts/contact_gamma_sweep.py --suite dev --members faltus2026 --factors 0.1
"""

from __future__ import annotations

import argparse
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

FACTORS = (0.01, 0.1, 10.0, 100.0)  # factor 1 is the plain zoo run (`sforge zoo eval`)
OUT = Path("candidates") / "gamma_sweep"


def factor_tag(c: float) -> str:
    return f"{c:g}"


def wrapper_source(zoo_source: str, factor: float, member: str) -> str:
    """The zoo source with psi_medium renamed, plus a wrapper that scales gamma by `factor`."""
    src, n = re.subn(r"^def psi_medium\(", "def _zoo_psi_medium(", zoo_source, flags=re.M)
    if n != 1:
        raise ValueError(f"{member}: expected exactly one top-level psi_medium, found {n}")
    return (f"{src.rstrip()}\n\n\nFACTOR = {factor!r}  # gamma-sweep point (scripts/contact_gamma_sweep.py)\n\n\n"
            f"def psi_medium(C, p):\n"
            f'    """{member} with the stiffness scale gamma multiplied by FACTOR."""\n'
            f"    q = dict(p)\n"
            f'    q["gamma"] = FACTOR * p["gamma"]\n'
            f"    return _zoo_psi_medium(C, q)\n")


def write_points(members: list[str], factors: tuple[float, ...]) -> list[tuple[str, float, Path]]:
    from schemeforge.arenas.contact import zoo

    OUT.mkdir(parents=True, exist_ok=True)
    paths = zoo.members("medium")
    points = []
    for m in members:
        for c in factors:
            path = OUT / f"{m}_g{factor_tag(c)}.py"
            path.write_text(wrapper_source(paths[m].read_text(encoding="utf-8"), c, m), encoding="utf-8")
            points.append((m, c, path))
    return points


def main() -> None:
    from schemeforge.arenas.contact import zoo
    from schemeforge.core import evaluation, integrity
    from schemeforge.core.locks import max_parallel

    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--suite", choices=("dev", "promo"), default="promo")
    ap.add_argument("--members", default=",".join(sorted(zoo.members("medium"))))
    ap.add_argument("--factors", default=",".join(factor_tag(c) for c in FACTORS))
    args = ap.parse_args()
    problems = integrity.integrity_problems("contact")
    if problems:
        raise SystemExit("refusing to score: " + "; ".join(problems))
    points = write_points(args.members.split(","), tuple(float(c) for c in args.factors.split(",")))

    def one(point):
        m, c, path = point
        res = evaluation.evaluate_file(path, "contact", "medium", args.suite, origin="zoo",
                                       candidate_id=f"zoo-medium-{m}-g{factor_tag(c)}")
        return m, c, res

    with ThreadPoolExecutor(max_workers=max_parallel()) as pool:
        for m, c, res in pool.map(one, points):
            r = res.report
            print(f"{m:14s} x{factor_tag(c):6s} {r.get('status'):9s} {res.run_id}  {r.get('seconds', 0):.0f} s"
                  + ("  " + "; ".join(r.get("violations", [])) if r.get("violations") else ""))


if __name__ == "__main__":
    main()
