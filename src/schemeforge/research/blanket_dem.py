"""CS-14 blanket cell, rung R0/R1: brittle bonded-grain film on a stretched substrate (2D, quasi-static).

Protocol (frozen before any run): docs/research/coldspray-cs14-rung.md. Not a judge.

Nondimensional units: grain spacing a = 1, bond stiffness k = 1, grain mass 1. Arrays: positions (N, 2);
bonds (M,) index pairs with rest length r0 and threshold strain eps_b. Stresses are forces per unit length (2D).
"""

from __future__ import annotations

from dataclasses import dataclass

import jax
import jax.numpy as jnp
import numpy as np

jax.config.update("jax_enable_x64", True)

K_BOND = 1.0
K_NORMAL = 10.0  # substrate tie, normal direction
K_TANG = 1.0  # substrate tie, tangential elastic stiffness
K_PEN = 100.0  # R0 end grips
EPS_B = 0.02
SCATTER = 0.05


@dataclass
class Film:
    """Triangular-lattice film of n_t rows and n_x columns, centred on x = 0, bottom row at y = 0."""

    n_t: int
    n_x: int
    x0: np.ndarray  # (N, 2)
    bi: np.ndarray  # (M,)
    bj: np.ndarray  # (M,)
    r0: np.ndarray  # (M,)
    eps_b: np.ndarray  # (M,)
    bottom: np.ndarray  # indices of the bottom layer, left to right
    left: np.ndarray
    right: np.ndarray


ROW = np.sqrt(3.0) / 2.0  # triangular lattice: row spacing (amendment 1)


def thickness(n_t: int) -> float:
    """Film thickness t = n_t * sqrt(3)/2 (grain spacing a = 1)."""
    return n_t * ROW


def build_film(n_t: int, n_x: int, seed: int) -> Film:
    """Triangular (close-packed) lattice, nearest-neighbour bonds only; odd rows offset by a/2 (amendment 1)."""
    ix, iy = np.meshgrid(np.arange(n_x), np.arange(n_t), indexing="ij")
    idx = (ix * n_t + iy)
    x0 = np.stack([ix.ravel() + 0.5 * (iy.ravel() % 2) - 0.5 * (n_x - 1), iy.ravel() * ROW], axis=1)
    pairs = []
    jx, jy = ix + 1, iy  # along the row
    ok = jx < n_x
    pairs.append(np.stack([idx[ok], (jx * n_t + jy)[ok]], axis=1))
    for side in (0, 1):  # to the row above: even rows reach columns i-1, i; odd rows i, i+1
        jx = ix + np.where(iy % 2 == 0, side - 1, side)
        jy = iy + 1
        ok = (jx >= 0) & (jx < n_x) & (jy < n_t)
        pairs.append(np.stack([idx[ok], (jx * n_t + jy)[ok]], axis=1))
    p = np.concatenate(pairs)
    bi, bj = p[:, 0], p[:, 1]
    r0 = np.linalg.norm(x0[bj] - x0[bi], axis=1)
    rng = np.random.default_rng(seed)
    eps_b = EPS_B * (1.0 + SCATTER * rng.uniform(-1.0, 1.0, size=len(bi)))
    return Film(n_t, n_x, x0, bi, bj, r0, eps_b, idx[:, 0].copy(), idx[0, :].copy(), idx[-1, :].copy())


def _bond_energy(x, alive, bi, bj, r0):
    d = jnp.linalg.norm(x[bj] - x[bi], axis=1) - r0
    comp = jnp.minimum(d, 0.0)
    return 0.5 * K_BOND * jnp.sum(jnp.where(alive, d * d, comp * comp))


def _huber(delta, f_y):
    dy = f_y / K_TANG
    a = jnp.abs(delta)
    return jnp.where(a <= dy, 0.5 * K_TANG * delta * delta, f_y * a - 0.5 * f_y * dy)


def energy_substrate(x, alive, eps, slip, bi, bj, r0, bottom, xb0, f_y):
    """R1: bonds + bottom layer tied to a substrate stretched to strain eps (elastic-perfectly plastic shear)."""
    xb = x[bottom]
    delta = xb[:, 0] - xb0 * (1.0 + eps) - slip
    return (_bond_energy(x, alive, bi, bj, r0) + jnp.sum(_huber(delta, f_y))
            + 0.5 * K_NORMAL * jnp.sum(xb[:, 1] ** 2))


def energy_free(x, alive, eps, x0, bi, bj, r0, left, right, pin):
    """R0: bonds + end grips (left column held, right column displaced to strain eps) + one y pin."""
    length = x0[right[0], 0] - x0[left[0], 0]
    e_l = jnp.sum((x[left, 0] - x0[left, 0]) ** 2)
    e_r = jnp.sum((x[right, 0] - (x0[right, 0] + eps * length)) ** 2)
    return _bond_energy(x, alive, bi, bj, r0) + 0.5 * K_PEN * (e_l + e_r) + 0.5 * K_PEN * x[pin, 1] ** 2


def make_fire(energy, dt_max: float, tol: float = 1e-7, max_iter: int = 200_000):
    """FIRE minimiser for energy(x, *args); returns (x, iterations, max force)."""
    grad = jax.grad(energy)

    @jax.jit
    def relax(x, *args):
        def force(y):
            return -grad(y, *args)

        def cond(s):
            _, _, _, _, _, it, fmax = s
            return (fmax > tol) & (it < max_iter)

        def body(s):
            y, v, dt, alpha, npos, it, _ = s
            f = force(y)
            v = v + dt * f
            p = jnp.sum(f * v)
            fn = jnp.linalg.norm(f) + 1e-30
            vn = jnp.linalg.norm(v)
            v = (1 - alpha) * v + alpha * vn * f / fn
            up = (p > 0) & (npos > 5)
            dt = jnp.where(p > 0, jnp.where(up, jnp.minimum(dt * 1.1, dt_max), dt), dt * 0.5)
            alpha = jnp.where(p > 0, jnp.where(up, alpha * 0.99, alpha), 0.1)
            npos = jnp.where(p > 0, npos + 1, 0)
            v = jnp.where(p > 0, v, 0.0 * v)
            y = y + dt * v
            return y, v, dt, alpha, npos, it + 1, jnp.max(jnp.abs(f))

        s0 = (x, jnp.zeros_like(x), dt_max * 0.1, 0.1, 0, 0, jnp.inf)
        y, _, _, _, _, it, fmax = jax.lax.while_loop(cond, body, s0)
        return y, it, fmax

    return relax


@jax.jit
def overload(x, alive, bi, bj, r0, eps_b):
    """Ratio of tensile bond strain to threshold for unbroken bonds; returns (max ratio, argmax)."""
    strain = jnp.linalg.norm(x[bj] - x[bi], axis=1) / r0 - 1.0
    ratio = jnp.where(alive, strain / eps_b, -jnp.inf)
    i = jnp.argmax(ratio)
    return ratio[i], i


def _break_until_stable(x, alive, film, relax, args_fn, max_breaks=100_000):
    bi, bj, r0, eb = (jnp.asarray(a) for a in (film.bi, film.bj, film.r0, film.eps_b))
    n = 0
    while n < max_breaks:
        r, i = overload(x, alive, bi, bj, r0, eb)
        if float(r) <= 1.0:
            break
        alive = alive.at[int(i)].set(False)
        x, _, _ = relax(x, *args_fn(alive))
        n += 1
    return x, alive, n


def run_r0(n_t: int, seed: int, length_over_t: int = 8, n_steps: int = 60, record: bool = False) -> dict:
    """Free film in tension. Returns E_f (initial slope) and sigma_f (peak mean stress), force per unit length."""
    film = build_film(n_t, length_over_t * n_t, seed)
    x0 = jnp.asarray(film.x0)
    bi, bj, r0 = (jnp.asarray(a) for a in (film.bi, film.bj, film.r0))
    left, right = jnp.asarray(film.left), jnp.asarray(film.right)
    pin = int(film.left[0])
    relax = make_fire(energy_free, dt_max=0.08)
    alive = jnp.ones(len(film.bi), dtype=bool)
    x = x0
    length = float(film.x0[film.right[0], 0] - film.x0[film.left[0], 0])
    curve = []
    frames = []
    for k in range(1, n_steps + 1):
        eps = 1.5 * EPS_B * k / n_steps
        args = lambda a, e=eps: (a, e, x0, bi, bj, r0, left, right, pin)  # noqa: E731
        x, _, _ = relax(x, *args(alive))
        x, alive, _ = _break_until_stable(x, alive, film, relax, args)
        force = K_PEN * float(jnp.sum((x0[right, 0] + eps * length) - x[right, 0]))
        strain = float(jnp.mean(x[right, 0]) - jnp.mean(x[left, 0])) / length - 1.0
        curve.append((strain, force / thickness(n_t)))
        if record:
            frames.append((eps, np.asarray(x), np.asarray(alive)))
    c = np.array(curve)
    e_f = c[0, 1] / c[0, 0]
    ip = int(c[:, 1].argmax())
    sigma_f = float(c[ip, 1])
    # amendment 1: brittle if the stress falls below 0.1 sigma_f before strain exceeds the peak strain + 0.2 eps_b
    after = c[(c[:, 0] > c[ip, 0]) & (c[:, 0] <= c[ip, 0] + 0.2 * EPS_B)]
    brittle = bool(len(after) and after[:, 1].min() < 0.1 * sigma_f)
    out = {"n_t": n_t, "seed": seed, "E_f": e_f, "sigma_f": sigma_f, "brittle": brittle, "curve": c}
    if record:
        out["frames"], out["film"] = frames, film
    return out


def fragments(film: Film, alive: np.ndarray, min_size: int | None = None) -> list[dict]:
    """Connected components of unbroken bonds. Returns fragments (debris below min_size grains dropped)."""
    n = len(film.x0)
    parent = np.arange(n)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i, j in zip(film.bi[alive], film.bj[alive], strict=True):
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
    roots = np.array([find(i) for i in range(n)])
    min_size = film.n_t if min_size is None else min_size
    col = np.arange(n) // film.n_t
    out = []
    for r in np.unique(roots):
        members = np.flatnonzero(roots == r)
        if len(members) < min_size:
            continue
        c = col[members]
        out.append({"size": len(members), "c_min": int(c.min()), "c_max": int(c.max()),
                    "length": int(c.max() - c.min() + 1),
                    "touches_end": bool(c.min() == 0 or c.max() == film.n_x - 1)})
    return sorted(out, key=lambda f: f["c_min"])


def run_r1(n_t: int, seed: int, sigma_f: float, e_f: float, ls_over_t: float = 4.0,
           length_over_t: int = 64, n_steps: int = 80, eps_max_over_ef: float = 4.0) -> dict:
    """Fragmentation on the stretched substrate. tau_i = sigma_f / ls_over_t, so L_s = sigma_f t / tau_i = ls_over_t t.

    The film is length_over_t * n_t columns long (about 1.15 * length_over_t * t on the triangular lattice).
    """
    film = build_film(n_t, length_over_t * n_t, seed)
    tau_i = sigma_f / ls_over_t
    f_y = tau_i * 1.0
    eps_f = sigma_f / e_f
    x0 = jnp.asarray(film.x0)
    bi, bj, r0 = (jnp.asarray(a) for a in (film.bi, film.bj, film.r0))
    bottom = jnp.asarray(film.bottom)
    xb0 = x0[bottom, 0]
    relax = make_fire(energy_substrate, dt_max=0.15)
    alive = jnp.ones(len(film.bi), dtype=bool)
    slip = jnp.zeros(len(film.bottom))
    x = x0
    n_breaks = 0
    for k in range(1, n_steps + 1):
        eps = eps_max_over_ef * eps_f * k / n_steps
        args = lambda a, e=eps, s=slip: (a, e, s, bi, bj, r0, bottom, xb0, f_y)  # noqa: E731
        x, _, _ = relax(x, *args(alive))
        x, alive, nb = _break_until_stable(x, alive, film, relax, args)
        n_breaks += nb
        delta = x[bottom, 0] - xb0 * (1.0 + eps) - slip
        excess = jnp.abs(delta) - f_y / K_TANG
        slip = slip + jnp.where(excess > 0, jnp.sign(delta) * excess, 0.0)
    frs = fragments(film, np.asarray(alive))
    inner = [f["length"] for f in frs if not f["touches_end"]]
    ls = ls_over_t * thickness(n_t)
    return {"n_t": n_t, "seed": seed, "L_s": ls, "n_fragments": len(frs), "n_inner": len(inner),
            "w_mean": float(np.mean(inner)) if inner else float("nan"),
            "w_min": min(inner) if inner else None, "w_max": max(inner) if inner else None,
            "n_breaks": n_breaks, "tau_i": tau_i}
