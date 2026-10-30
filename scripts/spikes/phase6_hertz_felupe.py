"""Spike script, not part of the judge. Needs felupe 11.3 and jax in a separate venv (GPL-3.0 dependency, see
docs/spikes/2026-10-30-phase6-tooling.md).

Phase 6 spike (PLAN §14.1): 2D plane-strain Hertz contact through a third medium, FElupe, Q2 (bi-quadratic) quads.

Half model x in [0, W] (symmetry at x = 0). Lower block y in [-Hb, 0]; medium between y = 0 and the upper body's
surface y = d0 + x^2 / (2R); upper body above it, thickness Ht. Bottom fixed, top pushed down. Elastically identical
bodies, so Hertz gives P = pi E* a^2 / (4R) per unit length, 1/E* = 2 (1 - nu^2) / E.
Usage: python hertz.py nx ny_body ny_medium push nsteps
"""

import sys
import time

import numpy as np

import felupe as fem
from felupe.math import dddot, dot, hess

nx, nyb, nym = (int(a) for a in sys.argv[1:4])
push, nsteps = float(sys.argv[4]), int(sys.argv[5])
W, R, Hb, Ht, d0 = 1.0, 1.0, 1.0, 1.0, 0.002
E, nu = 1.0, 0.3
mu, lmbda = E / (2 * (1 + nu)), E * nu / ((1 + nu) * (1 - 2 * nu))
gamma0, kr = 1e-6, 5e-6

s = np.linspace(0, 1, nx + 1)
xs = W * s**2  # graded towards the contact


def surface(x):
    return d0 + x**2 / (2 * R)


def block(y0, y1, ny, grade_to):
    """Structured quad mesh between curves y0(x) and y1(x); rows graded towards 'lo' / 'hi' / None."""
    m = fem.Rectangle(a=(0, 0), b=(1, 1), n=(nx + 1, ny + 1))
    i = np.rint(m.points[:, 0] * nx).astype(int)
    t = m.points[:, 1]
    t = {"lo": t**2, "hi": 1 - (1 - t) ** 2, None: t}[grade_to]
    x = xs[i]
    m.points = np.column_stack([x, y0(x) + t * (y1(x) - y0(x))])
    return m


lower = block(lambda x: -Hb + 0 * x, lambda x: 0 * x, nyb, "hi")
medium = block(lambda x: 0 * x, surface, nym, None)
upper = block(surface, lambda x: surface(x) + Ht, nyb, "lo")
body = fem.MeshContainer([lower, upper], merge=True, decimals=10).stack()
body = body.add_midpoints_edges().add_midpoints_faces()
medium = medium.add_midpoints_edges().add_midpoints_faces()

container = fem.MeshContainer([body, medium], merge=True, decimals=10)
regions = [fem.RegionBiQuadraticQuad(m, hess=True) for m in container.meshes]
fields = [fem.FieldPlaneStrain(r, dim=2).as_container() for r in regions]
umats = [fem.NeoHookeCompressible(mu=mu, lmbda=lmbda),
         fem.NeoHookeCompressible(mu=mu * gamma0, lmbda=lmbda * gamma0)]
import os  # noqa: E402

if os.environ.get("JAX_MEDIUM"):
    import jax  # noqa: E402

    jax.config.update("jax_enable_x64", True)
    import jax.numpy as jnp  # noqa: E402

    def psi_medium(C, mu, lmbda):  # the candidate: a pure jax.numpy function of C
        lnJ = jnp.log(jnp.linalg.det(C)) / 2
        return mu / 2 * (jnp.trace(C) - 3) - mu * lnJ + lmbda / 2 * lnJ**2

    import felupe.constitution.jax as fjax  # noqa: E402

    umats[1] = fjax.Hyperelastic(psi_medium, mu=mu * gamma0, lmbda=lmbda * gamma0)
solids = [fem.SolidBody(u, f) for u, f in zip(umats, fields)]

region = fem.RegionBiQuadraticQuad(container.stack())
field = fem.FieldPlaneStrain(region, dim=2).as_container()
pts = region.mesh.points
top = np.isclose(pts[:, 1], surface(pts[:, 0]) + Ht)
bounds = fem.BoundaryDict(
    sym=fem.Boundary(field[0], fx=0.0, skip=(0, 1)),
    bottom=fem.Boundary(field[0], fy=-Hb),
    top=fem.Boundary(field[0], mask=top, skip=(1, 0)),
)

lap = lambda x: np.einsum("ijj...->i...", x)  # noqa: E731


@fem.Form(v=fields[1], u=fields[1], kwargs={"kr": 1.0})
def bilinearform():
    def a(v, u, kr):
        Hu, Hv = hess(u), hess(v)
        return kr * (dddot(Hu, Hv) - dot(lap(Hu), lap(Hv), mode=(1, 1)) / 2)
    return [a]


@fem.Form(v=fields[1], kwargs={"kr": 1.0})
def linearform():
    u = fields[1][0]

    def L(v, kr):
        Hu, Hv = hess(u)[:2, :2, :2], hess(v)
        return kr * (dddot(Hu, Hv) - dot(lap(Hu), lap(Hv), mode=(1, 1)) / 2)
    return [L]


reg = fem.FormItem(bilinearform=bilinearform, linearform=linearform, kwargs={"kr": kr * lmbda * W**2})
ramp = -fem.math.linsteps([0, 1], num=nsteps) * (d0 + push)
step = fem.Step(items=[*solids, reg], ramp={bounds["top"]: ramp}, boundaries=bounds)

iters, last = [], {}


def record(c, st):
    iters.append(c.substep.iterations)
    last['fun'] = c.substep.fun


job = fem.Job([step], plugins=[record, fem.LinesearchPlugin()])
t0 = time.perf_counter()
job.evaluate(x0=field, verbose=0, tol=1e-8)
wall = time.perf_counter() - t0

# reaction on the top boundary (per unit length, half model -> x2), and contact half-width from the medium thickness
r = np.asarray(last["fun"]).ravel()[: field[0].values.size].reshape(-1, 2)
force = 2 * r[bounds["top"].points].sum(axis=0)  # full model (x2)
u = field[0].values
y = pts[:, 1] + u[:, 1]
x = pts[:, 0] + u[:, 0]
low_top = np.isclose(pts[:, 1], 0.0)
up_bot = np.isclose(pts[:, 1], surface(pts[:, 0])) & ~low_top
xl, yl = x[low_top], y[low_top]
xu, yu = x[up_bot], y[up_bot]
o = np.argsort(xl)
gap = np.interp(xu, xl[o], yl[o])
thick = yu - gap
a_est = xu[thick < 0.25 * d0].max() if np.any(thick < 0.25 * d0) else 0.0
Es = E / (2 * (1 - nu**2))
import resource
print(f"peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
print(f"DOF {field[0].values.size}  cells {region.mesh.ncells}  steps {nsteps}  Newton iters {iters}  "
      f"total {sum(i or 0 for i in iters)}  wall {wall:.1f} s")
print(f"contact half-width (medium < 25 % of d0) a = {a_est:.4f}; Hertz P for that a = {np.pi * Es * a_est**2 / (4 * R):.4g}")
print(f"min medium thickness {thick.min():.3e} (d0 {d0}), J_min medium check below")
F = fields[1][0].extract(grad=True, sym=False, add_identity=True)
J = np.linalg.det(F.transpose(2, 3, 0, 1))
print(f"J_min medium {J.min():.3e}")
if force is not None:
    print(f"top reaction (full model) Fy = {force[1]:.4g}; Hertz a for that P = {np.sqrt(4 * abs(force[1]) * R / (np.pi * Es)):.4f}")
