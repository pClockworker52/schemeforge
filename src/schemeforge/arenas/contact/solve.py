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

from .cases import GapClosureCase, HertzCase  # noqa: E402
from .metrics import edge_traction  # noqa: E402
from .reference import lame  # noqa: E402


def medium_material(psi: Callable, mu: float, lmbda: float, gamma: float):
    """The candidate energy psi(C, p) as a FElupe material; p = {mu, lmbda, gamma} of the body and the medium scale."""

    def fun(C, mu, lmbda, gamma):
        return psi(C, {"mu": mu, "lmbda": lmbda, "gamma": gamma})

    return fjax.Hyperelastic(fun, mu=mu, lmbda=lmbda, gamma=gamma)


@dataclass
class GapClosureResult:
    push: np.ndarray  # (steps + 1,) prescribed top displacement [L]
    force: np.ndarray  # (steps + 1,) reaction on the top edge, per unit thickness, compressive positive [F/L]
    wall_pressure: np.ndarray  # (n_wall,) contact pressure on the rigid wall at full push, from the reactions [F/L^2]
    medium_thickness: float  # at full push, at the symmetry line [L]
    newton_iters: list[int]
    min_j_medium: float


def _column(x1: float, y0: float, y1: float, nx: int, ny: int) -> fem.Mesh:
    m = fem.Rectangle(a=(0.0, y0), b=(x1, y1), n=(nx + 1, ny + 1))
    return m.add_midpoints_edges().add_midpoints_faces()


def gap_closure(psi: Callable, case: GapClosureCase) -> GapClosureResult:
    """Run C0a (laterally confined) and return the force-push curve. Raises felupe's NewtonConvergenceError if Newton
    fails (the evaluator records converged = 0)."""
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
        lateral=fem.Boundary(field[0], mask=np.ones(len(pts), bool), skip=(0, 1)),
        wall=fem.Boundary(field[0], fy=0.0),
        top=fem.Boundary(field[0], mask=top, skip=(1, 0)),
    )
    ramp = fem.math.linsteps([0.0, 1.0], num=case.steps) * case.push
    step = fem.Step(items=solids, ramp={bounds["top"]: -ramp}, boundaries=bounds)

    force, iters, last = [], [], {}

    def record(context, state):
        iters.append(int(context.substep.iterations or 0))
        r = np.asarray(context.substep.fun).ravel()[: field[0].values.size].reshape(-1, 2)
        force.append(-float(r[bounds["top"].points, 1].sum()))
        last["r"] = r

    fem.Job([step], plugins=[record, fem.LinesearchPlugin()]).evaluate(x0=field, verbose=0, tol=1e-10)

    u = field[0].values
    axis = np.isclose(pts[:, 0], 0.0)
    y_axis = pts[axis, 1] + u[axis, 1]
    medium_top = np.isclose(pts[axis, 1], g)
    F = sub[1][0].extract(grad=True, sym=False, add_identity=True)
    j = np.linalg.det(np.moveaxis(F[:2, :2], (0, 1), (-2, -1)))
    wall = np.isclose(pts[:, 1], 0.0)
    order = np.argsort(pts[wall, 0])
    pressure = edge_traction(pts[wall, 0][order], last["r"][wall, 1][order])
    return GapClosureResult(push=ramp, force=np.asarray(force), wall_pressure=pressure,
                            medium_thickness=float(y_axis[medium_top][0]), newton_iters=iters,
                            min_j_medium=float(j.min()))


def gap_closure_classical(case: GapClosureCase, multiplier: float) -> tuple[np.ndarray, np.ndarray]:
    """C0a with classical frictionless contact instead of a medium: the confined body alone above a rigid plane at
    y = 0 (felupe.ContactRigidPlane, penalty scaled by the body's mean stiffness times `multiplier`). Returns (push,
    force). The penalty error falls like 1/multiplier; `classical_extrapolated` removes it."""
    g, h, w = case.gap, case.height, case.width
    mu, lmbda = lame(case.E, case.nu)
    mesh = _column(w, g, g + h, case.nx, case.ny_body)
    mesh.update(points=np.vstack([mesh.points, [0.0, 0.0]]))  # the plane's centre point, held fixed
    region = fem.RegionBiQuadraticQuad(mesh)
    field = fem.FieldPlaneStrain(region, dim=2).as_container()
    solid = fem.SolidBody(fem.NeoHookeCompressible(mu=mu, lmbda=lmbda), field)
    pts = mesh.points
    n = len(pts)
    bottom = np.arange(n)[np.isclose(pts[:, 1], g)]
    contact = fem.ContactRigidPlane(field, points=bottom, centerpoint=n - 1, normal=[0.0, 1.0], multiplier=multiplier,
                                    items=[solid])
    centre = np.zeros(n, bool)
    centre[-1] = True
    bounds = fem.BoundaryDict(
        lateral=fem.Boundary(field[0], mask=np.ones(n, bool), skip=(0, 1)),
        centre=fem.Boundary(field[0], mask=centre),
        top=fem.Boundary(field[0], mask=np.isclose(pts[:, 1], g + h), skip=(1, 0)),
    )
    ramp = fem.math.linsteps([0.0, 1.0], num=case.steps) * case.push
    force = []

    def record(context, state):
        r = np.asarray(context.substep.fun).ravel()[: field[0].values.size].reshape(-1, 2)
        force.append(-float(r[bounds["top"].points, 1].sum()))

    step = fem.Step(items=[solid, contact], ramp={bounds["top"]: -ramp}, boundaries=bounds)
    fem.Job([step], plugins=[record]).evaluate(x0=field, verbose=0, tol=1e-10)
    return ramp, np.asarray(force)


def classical_extrapolated(values: dict[float, float]) -> float:
    """Richardson extrapolation of penalty results to infinite penalty: fit v(k) = a + b/k + c/k^2 through three
    multipliers k and return a."""
    k = np.array(sorted(values))
    if k.size != 3:
        raise ValueError("needs results for exactly three multipliers")
    A = np.column_stack([np.ones(3), 1.0 / k, 1.0 / k**2])
    return float(np.linalg.solve(A, np.array([values[x] for x in k]))[0])


# --- C2 Hertz ------------------------------------------------------------------------------------------------------
@dataclass
class HertzResult:
    x: np.ndarray  # (n,) reference x of the contact nodes, sorted [L]
    f: np.ndarray  # (n,) consistent nodal contact forces on the flat, half model, compressive positive [F/L]
    load: float  # total load P of the full model [F/L]
    newton_iters: list[int]
    min_j_medium: float


def _curved_block(case: HertzCase, y0: Callable, y1: Callable, ny: int, grade: bool) -> fem.Mesh:
    """Q2 mesh between curves y0(x) and y1(x) over x in [0, W]: mid-nodes are added in reference space before mapping,
    so edge mid-nodes lie on the curves and stay centred in x (columns: corners W s^2, mids their averages); rows are
    graded towards y0 if `grade`."""
    nx = case.nx
    m = fem.Rectangle(a=(0.0, 0.0), b=(1.0, 1.0), n=(nx + 1, ny + 1)).add_midpoints_edges().add_midpoints_faces()
    corners = case.W * np.linspace(0.0, 1.0, nx + 1) ** 2
    xcol = np.empty(2 * nx + 1)
    xcol[0::2] = corners
    xcol[1::2] = 0.5 * (corners[:-1] + corners[1:])
    x = xcol[np.rint(m.points[:, 0] * 2 * nx).astype(int)]
    t = m.points[:, 1] ** 2 if grade else m.points[:, 1]
    m.points = np.column_stack([x, y0(x) + t * (y1(x) - y0(x))])
    return m


def _regularization(field, kr: float) -> fem.FormItem:
    """HuHu-LuLu Hessian regularization of the medium (Frederiksen et al. 2025; felupe example ex20), strength kr."""
    from felupe.math import dddot, dot, hess

    def lap(z):
        return np.einsum("ijj...->i...", z)

    @fem.Form(v=field, u=field, kwargs={"kr": 1.0})
    def bilinearform():
        def a(v, u, kr):
            hu, hv = hess(u), hess(v)
            return kr * (dddot(hu, hv) - dot(lap(hu), lap(hv), mode=(1, 1)) / 2)

        return [a]

    @fem.Form(v=field, kwargs={"kr": 1.0})
    def linearform():
        u = field[0]

        def lin(v, kr):
            hu, hv = hess(u)[:2, :2, :2], hess(v)
            return kr * (dddot(hu, hv) - dot(lap(hu), lap(hv), mode=(1, 1)) / 2)

        return [lin]

    return fem.FormItem(bilinearform=bilinearform, linearform=linearform, kwargs={"kr": kr})


def _surface(case: HertzCase) -> Callable:
    return lambda x: case.gap + x**2 / (2.0 * case.R)


def hertz(psi: Callable, case: HertzCase) -> HertzResult:
    """Run C2 with the candidate medium. Contact forces are the nodal reactions on the flat (medium bottom)."""
    mu, lmbda = lame(case.E, case.nu)
    surf = _surface(case)
    body = _curved_block(case, surf, lambda x: case.H + 0.0 * x, case.ny, grade=True)
    medium = _curved_block(case, lambda x: 0.0 * x, surf, case.ny_medium, grade=False)
    container = fem.MeshContainer([body, medium], merge=True, decimals=10)
    regions = [fem.RegionBiQuadraticQuad(m, hess=True) for m in container.meshes]
    sub = [fem.FieldPlaneStrain(r, dim=2).as_container() for r in regions]
    umats = [fem.NeoHookeCompressible(mu=mu, lmbda=lmbda), medium_material(psi, mu, lmbda, case.gamma)]
    items = [*(fem.SolidBody(u, f) for u, f in zip(umats, sub, strict=True)),
             _regularization(sub[1], case.kr * lmbda * case.W**2)]
    region = fem.RegionBiQuadraticQuad(container.stack())
    field = fem.FieldPlaneStrain(region, dim=2).as_container()
    pts = region.mesh.points
    bounds = fem.BoundaryDict(
        symmetry=fem.Boundary(field[0], fx=0.0, skip=(0, 1)),
        flat=fem.Boundary(field[0], fy=0.0),
        top=fem.Boundary(field[0], mask=np.isclose(pts[:, 1], case.H), skip=(1, 0)),
    )
    ramp = fem.math.linsteps([0.0, 1.0], num=case.steps) * case.push
    iters, last = [], {}

    def record(context, state):
        iters.append(int(context.substep.iterations or 0))
        last["r"] = np.asarray(context.substep.fun).ravel()[: field[0].values.size].reshape(-1, 2)

    step = fem.Step(items=items, ramp={bounds["top"]: -ramp}, boundaries=bounds)
    fem.Job([step], plugins=[record, fem.LinesearchPlugin()]).evaluate(x0=field, verbose=0, tol=1e-10)
    r = last["r"]
    flat = np.arange(len(pts))[np.isclose(pts[:, 1], 0.0)]
    order = np.argsort(pts[flat, 0])
    F = sub[1][0].extract(grad=True, sym=False, add_identity=True)
    j = np.linalg.det(np.moveaxis(F[:2, :2], (0, 1), (-2, -1)))
    return HertzResult(x=pts[flat, 0][order], f=r[flat, 1][order], load=-2.0 * float(r[bounds["top"].points, 1].sum()),
                       newton_iters=iters, min_j_medium=float(j.min()))


def hertz_classical(case: HertzCase, multiplier: float = 1e3) -> HertzResult:
    """C2 with classical frictionless contact (felupe.ContactRigidPlane on the cylinder's surface nodes), no medium.
    The judge's reference for the error floor of the Hertz comparison (docs/judge/contact_spec.md)."""
    mu, lmbda = lame(case.E, case.nu)
    surf = _surface(case)
    mesh = _curved_block(case, surf, lambda x: case.H + 0.0 * x, case.ny, grade=True)
    mesh.update(points=np.vstack([mesh.points, [0.0, 0.0]]))  # the plane's centre point, held fixed
    region = fem.RegionBiQuadraticQuad(mesh)
    field = fem.FieldPlaneStrain(region, dim=2).as_container()
    solid = fem.SolidBody(fem.NeoHookeCompressible(mu=mu, lmbda=lmbda), field)
    pts = mesh.points
    n = len(pts)
    surface = np.arange(n - 1)[np.isclose(pts[:-1, 1], surf(pts[:-1, 0]))]
    contact = fem.ContactRigidPlane(field, points=surface, centerpoint=n - 1, normal=[0.0, 1.0],
                                    multiplier=multiplier, items=[solid])
    centre = np.zeros(n, bool)
    centre[-1] = True
    bounds = fem.BoundaryDict(
        symmetry=fem.Boundary(field[0], fx=0.0, skip=(0, 1)),
        centre=fem.Boundary(field[0], mask=centre),
        top=fem.Boundary(field[0], mask=np.isclose(pts[:, 1], case.H), skip=(1, 0)),
    )
    ramp = fem.math.linsteps([0.0, 1.0], num=case.steps) * case.push
    iters, last = [], {}

    def record(context, state):
        iters.append(int(context.substep.iterations or 0))
        last["r"] = np.asarray(context.substep.fun).ravel()[: field[0].values.size].reshape(-1, 2)

    step = fem.Step(items=[solid, contact], ramp={bounds["top"]: -ramp}, boundaries=bounds)
    fem.Job([step], plugins=[record]).evaluate(x0=field, verbose=0, tol=1e-10)
    vec = solid.assemble.vector()
    vec = np.asarray(vec.toarray() if hasattr(vec, "toarray") else vec).ravel()[: field[0].values.size].reshape(-1, 2)
    order = np.argsort(pts[surface, 0])
    return HertzResult(x=pts[surface, 0][order], f=vec[surface, 1][order],
                       load=-2.0 * float(last["r"][bounds["top"].points, 1].sum()), newton_iters=iters,
                       min_j_medium=1.0)
