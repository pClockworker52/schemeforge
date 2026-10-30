"""Arena 2 cases (PLAN §14.2): C0a gap closure and C0b simple shear (step 2); Hertz and the patch test follow in step 3.

Units are consistent but arbitrary: lengths [L], moduli and energies per volume [F/L^2] in plane strain.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any


@dataclass(frozen=True)
class GapClosureCase:
    """C0a: an elastic column of height `height` and width `width` sits on a medium layer of thickness `gap`, whose
    bottom is fixed to a rigid wall. The column's top is pushed down by `push` (> gap) in `steps` equal steps. Both
    are laterally confined (u_x = 0 everywhere), so each layer deforms homogeneously and the case is exact for any
    medium (reference.exact_gap_closure). Ideal contact: no force until the gap closes, then the confined body
    alone (reference.ideal_gap_force), and no residual medium thickness."""

    id: str
    gap: float = 0.1
    height: float = 1.0
    width: float = 0.2
    push: float = 0.15
    steps: int = 6
    nx: int = 1
    ny_body: int = 2
    ny_medium: int = 2
    E: float = 1.0
    nu: float = 0.3
    gamma: float = 1e-6


@dataclass(frozen=True)
class SimpleShearCase:
    """C0b: the medium alone in homogeneous simple shear F = [[1, shear], [0, 1]] (plane strain). Ideal: no shear
    stress. Evaluated exactly from the energy (reference.shear_stress), so no FE solve is needed."""

    id: str
    shear: float = 0.5
    E: float = 1.0
    nu: float = 0.3
    gamma: float = 1e-5


Case = GapClosureCase | SimpleShearCase
KINDS = {"gap_closure": GapClosureCase, "simple_shear": SimpleShearCase}


def smoke_suite() -> list[Case]:
    return [GapClosureCase("smoke-C0a", gamma=1e-3)]


def dev_suite() -> list[Case]:
    """C0a over three decades of medium stiffness (the trade-off of PLAN §14.7), C0b at a small and a large shear."""
    return [GapClosureCase("C0a-g3", gamma=1e-3), GapClosureCase("C0a-g5", gamma=1e-5),
            GapClosureCase("C0a-g6", gamma=1e-6), SimpleShearCase("C0b-s05", shear=0.5),
            SimpleShearCase("C0b-s2", shear=2.0)]


def case_from_dict(d: dict[str, Any]) -> Case:
    d = dict(d)
    kind = d.pop("kind")
    if kind not in KINDS:
        raise ValueError(f"unknown case kind {kind!r}; known: {sorted(KINDS)}")
    cls = KINDS[kind]
    names = {f.name for f in fields(cls)}
    unknown = set(d) - names
    if unknown:
        raise ValueError(f"unknown fields for {kind}: {sorted(unknown)}")
    return cls(**d)


def validate_case(case: Case) -> None:
    """Admissibility: positive sizes and moduli, 0 <= nu < 0.5, a push that closes the gap and spares the body."""
    if isinstance(case, GapClosureCase):
        sizes = (case.gap, case.height, case.width, case.E, case.gamma)
        if min(sizes) <= 0 or not 0.0 <= case.nu < 0.5:
            raise ValueError(f"{case.id}: sizes, E and gamma must be positive and 0 <= nu < 0.5")
        if not case.gap < case.push < case.gap + 0.5 * case.height:
            raise ValueError(f"{case.id}: push must close the gap and compress the column by less than half")
        if case.steps < 2 or min(case.nx, case.ny_body, case.ny_medium) < 1:
            raise ValueError(f"{case.id}: at least 2 steps and one cell per direction")
        return
    if isinstance(case, SimpleShearCase):
        if case.shear <= 0 or case.E <= 0 or case.gamma <= 0 or not 0.0 <= case.nu < 0.5:
            raise ValueError(f"{case.id}: shear, E and gamma must be positive and 0 <= nu < 0.5")
        return
    raise TypeError(type(case).__name__)
