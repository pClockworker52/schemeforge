"""Explicit 2D-axisymmetric impact solver in JAX (cold-spray research track, rung 1 of the verification ladder).

Status: rung 1 only. Small-strain linear elasticity, frictionless rigid wall. Later rungs add finite strain,
Johnson-Cook plasticity, Mie-Grueneisen EOS, artificial viscosity and deformable substrates. Not a judge.

Discretisation
- Coordinates (r, z); axis r = 0; the sphere moves in -z onto a rigid wall z = z_wall.
- 4-node quadrilaterals, 2x2 Gauss points, B-bar (volumetric strain taken at the element centre) so that the
  element does not lock for nearly incompressible flow later.
- Lumped (row-sum) mass with the axisymmetric weight 2 pi r; nodal forces are ring forces (N).
- Central differences; kinematic wall contact: a node predicted to cross the wall lands exactly on it, and the
  momentum removed is the contact reaction.

Units: SI (m, s, kg, Pa). Arrays: X (n_nodes, 2) reference coordinates; conn (n_elem, 4) node ids,
counter-clockwise in (r, z).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import jax
import jax.numpy as jnp
import numpy as np

jax.config.update("jax_enable_x64", True)

_GP = 1.0 / math.sqrt(3.0)
GAUSS = np.array([[-_GP, -_GP], [_GP, -_GP], [_GP, _GP], [-_GP, _GP]])


@dataclass(frozen=True)
class Mesh:
    X: np.ndarray  # (n_nodes, 2) reference (r, z), m
    conn: np.ndarray  # (n_elem, 4) int


def sphere_mesh(radius: float, n_u: int, n_v: int, grade: float = 2.0) -> Mesh:
    """Half-disk (r >= 0) meshed by the elliptical square-to-disk map, centred at z = 0.

    u in [0, 1] (u = 0 is the axis), v in [-1, 1]; the edges u = 1 and v = +-1 lie on the circle. Nodes are
    graded towards u = 0 and v = -1 (the contact point at the south pole) with exponent `grade`.
    """
    u = (np.arange(n_u + 1) / n_u) ** grade
    s = np.arange(n_v + 1) / n_v
    v = -1.0 + 2.0 * s**grade
    uu, vv = np.meshgrid(u, v, indexing="ij")  # (n_u+1, n_v+1)
    r = radius * uu * np.sqrt(1.0 - vv**2 / 2.0)
    z = radius * vv * np.sqrt(1.0 - uu**2 / 2.0)
    X = np.stack([r.ravel(), z.ravel()], axis=1)
    idx = np.arange((n_u + 1) * (n_v + 1)).reshape(n_u + 1, n_v + 1)
    a, b = idx[:-1, :-1], idx[1:, :-1]
    c, d = idx[1:, 1:], idx[:-1, 1:]
    conn = np.stack([a.ravel(), b.ravel(), c.ravel(), d.ravel()], axis=1)  # ccw in (r, z)
    return Mesh(X=X, conn=conn)


def characteristic_length(mesh: Mesh) -> float:
    """Smallest element 'thickness' area / longest diagonal (m); governs the stable time step of distorted
    quadrilaterals better than the shortest edge."""
    xe = mesh.X[mesh.conn]
    d1, d2 = xe[:, 2] - xe[:, 0], xe[:, 3] - xe[:, 1]
    area = 0.5 * np.abs(d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0])
    diag = np.maximum(np.linalg.norm(d1, axis=1), np.linalg.norm(d2, axis=1))
    return float(np.min(area / diag))


def _shape(xi: float, eta: float) -> tuple[np.ndarray, np.ndarray]:
    N = 0.25 * np.array([(1 - xi) * (1 - eta), (1 + xi) * (1 - eta), (1 + xi) * (1 + eta), (1 - xi) * (1 + eta)])
    dN = 0.25 * np.array([[-(1 - eta), -(1 - xi)], [(1 - eta), -(1 + xi)], [(1 + eta), (1 + xi)],
                          [-(1 + eta), (1 - xi)]])  # (4, 2): d/dxi, d/deta
    return N, dN


def _element_operators(X: jnp.ndarray, conn: jnp.ndarray):
    """B-bar matrices and integration weights at the 4 Gauss points of every element (reference config).

    Returns Bbar (n_elem, 4, 4, 8) mapping element dofs (r1, z1, ..., r4, z4) to (e_rr, e_zz, e_tt, g_rz), and
    w (n_elem, 4) = 2 pi r detJ (Gauss weights 1), and Nw (n_elem, 4, 4) = N_i * w for mass lumping.
    """
    xe = X[conn]  # (E, 4, 2)

    def at(xi, eta):
        N, dN = _shape(xi, eta)
        J = jnp.einsum("eai,aj->eij", xe, dN)  # (E, 2, 2): dx_i/dxi_j
        detJ = J[:, 0, 0] * J[:, 1, 1] - J[:, 0, 1] * J[:, 1, 0]
        Jinv = jnp.stack([jnp.stack([J[:, 1, 1], -J[:, 0, 1]], -1), jnp.stack([-J[:, 1, 0], J[:, 0, 0]], -1)],
                         -2) / detJ[:, None, None]
        dNdx = jnp.einsum("aj,eji->eai", dN, Jinv)  # (E, 4, 2): dN_a/dr, dN_a/dz
        r = jnp.einsum("a,ea->e", N, xe[..., 0])
        B = jnp.zeros((xe.shape[0], 4, 8))
        B = B.at[:, 0, 0::2].set(dNdx[..., 0])
        B = B.at[:, 1, 1::2].set(dNdx[..., 1])
        B = B.at[:, 2, 0::2].set(jnp.asarray(N)[None, :] / r[:, None])
        B = B.at[:, 3, 0::2].set(dNdx[..., 1])
        B = B.at[:, 3, 1::2].set(dNdx[..., 0])
        return B, 2.0 * jnp.pi * r * detJ, jnp.asarray(N)

    Bs, ws, Ns = zip(*[at(*g) for g in GAUSS], strict=True)
    B = jnp.stack(Bs, 1)  # (E, 4gp, 4, 8)
    w = jnp.stack(ws, 1)  # (E, 4gp)
    # B-bar: volumetric part replaced by its volume-weighted element average
    bvol = B[:, :, 0, :] + B[:, :, 1, :] + B[:, :, 2, :]  # (E, 4gp, 8)
    bvol_avg = jnp.einsum("eg,egk->ek", w, bvol) / w.sum(1)[:, None]
    m = jnp.array([1.0, 1.0, 1.0, 0.0])
    Bbar = B + (m[None, None, :, None] / 3.0) * (bvol_avg[:, None, None, :] - bvol[:, :, None, :])
    Nw = jnp.stack(Ns, 0)[None, :, :] * w[:, :, None]  # (E, 4gp, 4)
    return Bbar, w, Nw


def elastic_D(E: float, nu: float) -> jnp.ndarray:
    """Isotropic elasticity for (e_rr, e_zz, e_tt, g_rz), Pa."""
    lam = E * nu / ((1 + nu) * (1 - 2 * nu))
    mu = E / (2 * (1 + nu))
    return jnp.array([[lam + 2 * mu, lam, lam, 0.0], [lam, lam + 2 * mu, lam, 0.0],
                      [lam, lam, lam + 2 * mu, 0.0], [0.0, 0.0, 0.0, mu]])


@dataclass(frozen=True)
class ImpactResult:
    t: np.ndarray  # (n_steps,) s
    force: np.ndarray  # (n_steps,) total wall reaction, N (positive = pushing the sphere up)
    z_cm: np.ndarray  # (n_steps,) centre-of-mass height, m
    v_cm: np.ndarray  # (n_steps,) centre-of-mass velocity, m/s


def elastic_sphere_on_rigid_wall(radius: float, velocity: float, E: float, nu: float, rho: float,
                                 n_u: int = 30, n_v: int = 60, cfl: float = 0.4,
                                 t_end_factor: float = 1.6) -> ImpactResult:
    """Rung 1: elastic sphere (initially touching) hits a rigid frictionless wall at `velocity` (m/s, > 0).

    t_end = t_end_factor * Hertz contact time (from hertz_reference) so that the rebound is captured.
    """
    mesh = sphere_mesh(radius, n_u, n_v)
    X = jnp.asarray(mesh.X)
    conn = jnp.asarray(mesh.conn)
    Bbar, w, Nw = _element_operators(X, conn)
    D = elastic_D(E, nu)
    n = X.shape[0]
    mass = jax.ops.segment_sum((rho * Nw.sum(1)).ravel(), conn.ravel(), n)  # (n,) ring masses, kg
    axis = jnp.isclose(X[:, 0], 0.0)
    z_wall = -radius

    h_min = characteristic_length(mesh)
    c_d = math.sqrt(float(D[0, 0]) / rho)
    dt = cfl * h_min / c_d
    t_end = t_end_factor * hertz_reference(radius, velocity, E, nu, rho)["t_contact"]
    n_steps = int(math.ceil(t_end / dt))

    def f_int(u):
        ue = u[conn].reshape(conn.shape[0], 8)  # (E, 8) dofs r1 z1 ... r4 z4
        eps = jnp.einsum("egij,ej->egi", Bbar, ue)
        sig = jnp.einsum("ij,egj->egi", D, eps)
        fe = jnp.einsum("egij,egi,eg->ej", Bbar, sig, w).reshape(-1, 4, 2)
        return jax.ops.segment_sum(fe.reshape(-1, 2), conn.ravel(), n)

    def step(state, _):
        u, v = state
        a = -f_int(u) / mass[:, None]
        v_pred = v + dt * a
        v_pred = v_pred.at[:, 0].set(jnp.where(axis, 0.0, v_pred[:, 0]))
        z_pred = X[:, 1] + u[:, 1] + dt * v_pred[:, 1]
        hit = z_pred < z_wall
        vz_new = jnp.where(hit, (z_wall - X[:, 1] - u[:, 1]) / dt, v_pred[:, 1])
        force = jnp.sum(mass * (vz_new - v_pred[:, 1])) / dt
        v_new = v_pred.at[:, 1].set(vz_new)
        u_new = u + dt * v_new
        z_cm = jnp.sum(mass * (X[:, 1] + u_new[:, 1])) / mass.sum()
        v_cm = jnp.sum(mass * v_new[:, 1]) / mass.sum()
        return (u_new, v_new), (force, z_cm, v_cm)

    u0 = jnp.zeros_like(X)
    v0 = jnp.zeros_like(X).at[:, 1].set(-velocity)
    _, (force, z_cm, v_cm) = jax.lax.scan(jax.jit(step), (u0, v0), None, length=n_steps)
    t = dt * (np.arange(n_steps) + 1)
    return ImpactResult(t=t, force=np.asarray(force), z_cm=np.asarray(z_cm), v_cm=np.asarray(v_cm))


def hertz_reference(radius: float, velocity: float, E: float, nu: float, rho: float) -> dict[str, float]:
    """Hertz impact of an elastic sphere on a rigid flat, from the force law F = (4/3) E* sqrt(R) d^(3/2).

    m d'' = -F(d), d(0) = 0, d'(0) = v. d_max follows from energy; the contact time and peak force are obtained
    by integrating the ODE (RK4, fine step), so no tabulated constants are used. E* = E / (1 - nu^2).
    """
    E_star = E / (1.0 - nu**2)
    m = rho * 4.0 / 3.0 * math.pi * radius**3
    k = 4.0 / 3.0 * E_star * math.sqrt(radius)
    d_max = (15.0 * m * velocity**2 / (16.0 * E_star * math.sqrt(radius))) ** 0.4

    def rhs(y):
        d, dd = y
        return np.array([dd, -k * max(d, 0.0) ** 1.5 / m])

    h = (d_max / velocity) / 20000.0
    y, t = np.array([0.0, velocity]), 0.0
    while True:
        k1 = rhs(y)
        k2 = rhs(y + 0.5 * h * k1)
        k3 = rhs(y + 0.5 * h * k2)
        k4 = rhs(y + h * k3)
        y_new = y + h / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        if y_new[0] < 0.0:  # left contact: linear interpolation of the crossing
            t += h * y[0] / (y[0] - y_new[0])
            break
        y, t = y_new, t + h
    return {"d_max": d_max, "t_contact": t, "F_max": k * d_max**1.5}
