"""FElupe models for Arena 2 (felupe 11.3, plane strain, bi-quadratic quads). The candidate medium enters as a
JAX-differentiated strain energy of C (`felupe.constitution.jax.Hyperelastic`), evaluated per quadrature point."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import jax

jax.config.update("jax_enable_x64", True)

import felupe as fem  # noqa: E402
import felupe.constitution.jax as fjax  # noqa: E402
import numpy as np  # noqa: E402

from .cases import GapClosureCase  # noqa: E402


def lame(E: float, nu: float) -> tuple[float, float]:
    """(mu, lmbda) of an isotropic body from Young's modulus and Poisson's ratio."""
    return E / (2.0 * (1.0 + nu)), E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))


def medium_material(psi: Callable, mu: float, lmbda: float, gamma: float):
    """The candidate energy psi(C, p) as a FElupe material; p = {mu, lmbda, gamma} of the body and the medium scale."""

    def fun(C, mu, lmbda, gamma):
        return psi(C, {"mu": mu, "lmbda": lmbda, "gamma": gamma})

    return fjax.Hyperelastic(fun, mu=mu, lmbda=lmbda, gamma=gamma)


@dataclass
class GapClosureResult:
    push: np.ndarray  # (steps + 1,) prescribed top displacement [L]
    force: np.ndarray  # (steps + 1,) reaction on the top edge, per unit thickness [F/L]
    medium_thickness: float  # at full push, at the symmetry line [L]
    newton_iters: list[int]
    min_j_medium: float


def _column(x1: float, y0: float, y1: float, nx: int, ny: int) -> fem.Mesh:
    m = fem.Rectangle(a=(0.0, y0), b=(x1, y1), n=(nx + 1, ny + 1))
    return m.add_midpoints_edges().add_midpoints_faces()


def gap_closure(psi: Callable, case: GapClosureCase) -> GapClosureResult:
    """Run C0a and return the force-push curve. Raises if Newton fails (the evaluator records it as a violation)."""
    g, h, w = case.gap, case.height, case.width
    mu, lmbda = lame(case.E, case.nu)
    body = _column(w, g, g + h, case.nx, case.ny_body)
    medium = _column(w, 0.0, g, case.nx, case.ny_medium)
    container = fem.MeshContainer([body, medium], merge=True, decimals=10)
    regions = [fem.RegionBiQuadraticQuad(m) for m in container.meshes]
    sub = [fem.FieldPlaneStrain(r, dim=2).as_container() for r in regions]
    umats = [fem.NeoHookeCompressible(mu=mu, lmbda=lmbda), medium_material(psi, mu, lmbda, case.gamma)]
    solids = [fem.SolidBody(u, f) for u, f in zip(umats, sub, strict=True)]

    region = fem.RegionBiQuadraticQuad(container.stack())
    field = fem.FieldPlaneStrain(region, dim=2).as_container()
    pts = region.mesh.points
    top = np.isclose(pts[:, 1], g + h)
    bounds = fem.BoundaryDict(
        symmetry=fem.Boundary(field[0], fx=0.0, skip=(0, 1)),
        wall=fem.Boundary(field[0], fy=0.0),
        top=fem.Boundary(field[0], mask=top, skip=(1, 0)),
    )
    ramp = fem.math.linsteps([0.0, 1.0], num=case.steps) * case.push
    step = fem.Step(items=solids, ramp={bounds["top"]: -ramp}, boundaries=bounds)

    force, iters = [], []

    def record(context, state):
        iters.append(int(context.substep.iterations or 0))
        r = np.asarray(context.substep.fun).ravel()[: field[0].values.size].reshape(-1, 2)
        force.append(-float(r[bounds["top"].points, 1].sum()))

    fem.Job([step], plugins=[record, fem.LinesearchPlugin()]).evaluate(x0=field, verbose=0, tol=1e-10)

    u = field[0].values
    axis = np.isclose(pts[:, 0], 0.0)
    y_axis = pts[axis, 1] + u[axis, 1]
    medium_top = np.isclose(pts[axis, 1], g)
    F = sub[1][0].extract(grad=True, sym=False, add_identity=True)
    j = np.linalg.det(np.moveaxis(F[:2, :2], (0, 1), (-2, -1)))
    return GapClosureResult(push=ramp, force=np.asarray(force), medium_thickness=float(y_axis[medium_top][0]),
                            newton_iters=iters, min_j_medium=float(j.min()))
