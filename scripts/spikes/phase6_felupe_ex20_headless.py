r"""
Third Medium Contact
--------------------

.. topic:: Frictionless contact method simulated by a third medium [1]_.

   * create a mesh container with multiple meshes

   * define multiple solid bodies and create a top-level field

   * plot the deformed solid

This contact method uses a third medium for two solid contact bodies with a a Hessian-
based regularization [2]_. First, let's create sub meshes with bi-quadratic quad cells
for the solid body. All sub meshes are merged by stacking the meshes of the
:class:`mesh container <felupe.MeshContainer>` into a :class:`mesh <felupe.Mesh>`.
"""

import numpy as np

import felupe as fem

t = 0.1
L = 1
H = 0.5

nt, nL, nH = (2, 10, 4)

a = fem.Rectangle(a=(0, 0), b=(t, t), n=nt)
b = a.translate(move=H - t, axis=1)
c = fem.Rectangle(a=(t, 0), b=(L, t), n=(nL, nt))
d = c.translate(move=H - t, axis=1)
e = fem.Rectangle(a=(0, t), b=(t, H - t), n=(nt, nH))
body = fem.MeshContainer([a, b, c, d, e], merge=True).stack()
body = body.add_midpoints_edges().add_midpoints_faces()

# %%
# This is repeated for the medium, where two meshes are added to a mesh container. Extra
# cells are added on the right edge to improve convergence.
f = fem.Rectangle(a=(t, t), b=(L, H - t), n=(nL, nH))
g = fem.Rectangle(a=(L, 0), b=(L + t / (nt - 1), H), n=(2, 2 * (nt - 1) + nH))
medium = fem.MeshContainer([f, g], merge=True).stack()
medium = medium.add_midpoints_edges().add_midpoints_faces()

# %%
# Both stacked meshes are added to a top-level mesh container. For each mesh of the
# container, quad regions and plane-strain vector-fields for the displacements are
# created. The Neo-Hookean isotropic hyperelastic material formulation from the solid
# body is also used for the isotropic part of the background material but with scaled
# down material parameters.
G = 5 / 14
K = 5 / 3
kr = 5e-6
gamma0 = 5e-6

container = fem.MeshContainer([body, medium], merge=True, decimals=6)
regions = [fem.RegionBiQuadraticQuad(m, hess=True) for m in container.meshes]
fields = [fem.FieldPlaneStrain(r, dim=2).as_container() for r in regions]
umats = [
    fem.NeoHookeCompressible(mu=G, lmbda=K),
    fem.NeoHookeCompressible(mu=G * gamma0, lmbda=K * gamma0),
]
solids = [fem.SolidBody(umat, f) for umat, f in zip(umats, fields)]

# %%
# A top-level plane-strain field is created on a stacked mesh. This field includes all
# unknowns and is required for the selection of prescribed degrees of freedom as well
# as for Newton's method. The left end edge is fixed and the vertical displacement is
# prescribed on the outermost top-right point.
region = fem.RegionBiQuadraticQuad(container.stack())
field = fem.FieldPlaneStrain(region, dim=2).as_container()

bounds = fem.BoundaryDict(
    fixed=fem.Boundary(field[0], fx=0),
    move=fem.Boundary(field[0], fx=L, fy=H, mode="and", skip=(1, 0)),
)

# %%
# The so-called HuHu-regularization [3]_, here enhanced by the HuHu-LuLu-regularization
# [4]_, is created by two weak-:func:`forms <felupe.Form>`, which are derived from the
# regularization potential, see Eq. :eq:`huhu-lulu-regularization` [4]_.
#
# .. math::
#    :label: huhu-lulu-regularization
#
#    \Psi(\boldsymbol{u}) = W(\boldsymbol{u}) + \frac{k_r}{2} \left (
#        \mathbb{H}(\boldsymbol{u})~\vdots~\mathbb{H}(\boldsymbol{u})
#        - \frac{1}{\text{tr}(\boldsymbol{1})}
#          \mathbb{L}(\boldsymbol{u}) \cdot \mathbb{L}(\boldsymbol{u})
#    \right )
#
from felupe.math import dddot, dot, hess

laplacian = lambda x: np.einsum("ijj...->i...", x)


@fem.Form(v=fields[1], u=fields[1], kwargs={"kr": 1.0})
def bilinearform():
    def a(v, u, kr):
        Hu = hess(u)
        Hv = hess(v)
        Lu = laplacian(Hu)
        Lv = laplacian(Hv)
        return kr * (dddot(Hu, Hv) - dot(Lu, Lv, mode=(1, 1)) / 2)

    return [a]


@fem.Form(v=fields[1], kwargs={"kr": 1.0})
def linearform():
    u = fields[1][0]

    def L(v, kr):
        Hu = hess(u)[:2, :2, :2]
        Hv = hess(v)
        Lu = laplacian(Hu)
        Lv = laplacian(Hv)
        return kr * (dddot(Hu, Hv) - dot(Lu, Lv, mode=(1, 1)) / 2)

    return [L]


regularization = fem.FormItem(
    bilinearform=bilinearform,
    linearform=linearform,
    kwargs={"kr": kr * K * L**2},
)

# %%
# The prescribed displacement is ramped up to the maximum value.
move = fem.math.linsteps([0, 1], num=5)
step = fem.Step(
    items=[*solids, regularization],
    ramp={bounds["move"]: -0.62 * move * L},
    boundaries=bounds,
)

# %%
# The top-level field has to be passed as the ``x0``-argument of the job.
# The deformation configuration is plotted.
#
# ..  note::
#     For larger load increments, a full Newton step may lead to inadmissible
#     deformations of the third medium (:math:`\det \boldsymbol{F} \le 0`). An
#     optional backtracking line search (:class:`~felupe.LinesearchPlugin`) scales down
#     such Newton increments. By alternative, an incremental cutback strategy
#     (:class:`~felupe.CutbackPlugin`) can be used.
linesearch = fem.LinesearchPlugin()
job = fem.Job([step], plugins=[linesearch]).evaluate(x0=field)

print("DOF", field.values().size, "cells", region.mesh.ncells)
print("max top-right y-displacement", field[0].values[:, 1].min())
