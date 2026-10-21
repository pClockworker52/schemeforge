"""Hard constraints on Arena 1 slot functions (PLAN §5.8, §9.7), checked on fixed probe sets before any case runs.

A non-empty list of violations rejects the candidate. Run-level constraints (finite output, positive density and
pressure, solver failure) are checked by the evaluator on every case result.
"""

from __future__ import annotations

from collections.abc import Callable

import jax.numpy as jnp
import numpy as np

from .numerics import elementwise, physical_flux, prim_to_cons, rowwise

CONSISTENCY_TOL = 1e-12  # relative to max |F|
MIRROR_TOL = 1e-12
BATCH_TOL = 1e-13  # batch vs one-at-a-time evaluation, relative (rounding only; a case switch differs by O(1))
R_MIRROR = np.array([1.0, -1.0, 1.0])
# run-like batch sizes: interfaces/cells of the dev and held-out grids (N = 50 ... 400) and a single item
BATCH_ROWS = (1, 54, 101, 104, 121, 124, 201, 204, 404)


def limiter_probes() -> np.ndarray:
    """Slope ratios covering negative, zero, tiny, order-one and huge values (and the clipping bound)."""
    special = [0.0, 1.0, -1.0, 1e-300, -1e-300, 1e-12, -1e-12, 1e5, -1e5, 1e10, -1e10, 0.5, 2.0, 3.0]
    return np.concatenate([np.linspace(-5.0, 5.0, 201), np.logspace(-8, 10, 73), -np.logspace(-8, 10, 73), special])


def flux_probes(m: int = 256, seed: int = 20261020, gamma: float = 1.4) -> tuple[np.ndarray, np.ndarray]:
    """Fixed pairs of conserved states (m, 3): log-uniform rho in [1e-2, 1e2], p in [1e-3, 1e3], u in [-5, 5]."""
    rng = np.random.default_rng(seed)

    def states():
        rho = 10.0 ** rng.uniform(-2, 2, m)
        u = rng.uniform(-5, 5, m)
        p = 10.0 ** rng.uniform(-3, 3, m)
        return np.asarray(prim_to_cons(jnp.asarray(np.stack([rho, u, p], axis=1)), gamma))

    return states(), states()


def _close(a, b) -> bool:
    a, b = np.asarray(a), np.asarray(b)
    if a.shape != b.shape:
        return False
    both_nan = np.isnan(a) & np.isnan(b)
    with np.errstate(invalid="ignore"):
        ok = np.abs(a - b) <= BATCH_TOL * np.maximum(1.0, np.abs(b))
    return bool(np.all(ok | both_nan | (a == b)))


def _batch_independent_limiter(phi: Callable, r: np.ndarray) -> bool:
    """phi on run-shaped (rows, 3) batches equals phi applied one ratio at a time, also on zero-heavy batches."""
    one = elementwise(phi)
    for rows in BATCH_ROWS:
        a = np.resize(r, (rows, 3))
        for batch in (a, np.where(np.arange(a.size).reshape(a.shape) % 2 == 0, 0.0, a)):
            if not _close(np.asarray(phi(jnp.asarray(batch))), np.asarray(one(jnp.asarray(batch)))):
                return False
    return True


def _batch_independent_flux(flux: Callable, UL: np.ndarray, UR: np.ndarray, gamma: float) -> bool:
    one = rowwise(flux)
    for rows in BATCH_ROWS:
        a, b = np.resize(UL, (rows, 3)), np.resize(UR, (rows, 3))
        if not _close(np.asarray(flux(jnp.asarray(a), jnp.asarray(b), gamma)),
                      np.asarray(one(jnp.asarray(a), jnp.asarray(b), gamma))):
            return False
    return True


def _bitwise_equal(a, b) -> bool:
    a, b = np.asarray(a), np.asarray(b)
    return a.shape == b.shape and a.dtype == b.dtype and bool(np.all((a == b) | (np.isnan(a) & np.isnan(b))))


def check_limiter(phi: Callable) -> list[str]:
    r = limiter_probes()
    v: list[str] = []
    try:
        out = np.asarray(phi(jnp.asarray(r)))
    except Exception as exc:  # noqa: BLE001 - any failure of candidate code is a violation
        return [f"phi raised {type(exc).__name__}: {exc}"]
    if out.shape != r.shape:
        return [f"phi returned shape {out.shape}, expected {r.shape}"]
    if out.dtype != np.float64:
        v.append(f"phi returned dtype {out.dtype}, expected float64")
    if not np.all(np.isfinite(out)):
        bad = r[~np.isfinite(out)][:3]
        v.append(f"phi is not finite for r = {bad.tolist()}")
    if not _bitwise_equal(out, np.asarray(phi(jnp.asarray(r)))):
        v.append("phi is not deterministic")
    perm = np.random.default_rng(1).permutation(r.size)
    if not _bitwise_equal(np.asarray(phi(jnp.asarray(r[perm]))), out[perm]):
        v.append("phi is not pointwise (a permuted input does not give the permuted output)")
    r2 = r.reshape(-1, 3) if r.size % 3 == 0 else r[: r.size - r.size % 3].reshape(-1, 3)
    out2 = np.asarray(phi(jnp.asarray(r2)))
    if out2.shape != r2.shape or not _bitwise_equal(out2.reshape(-1), np.asarray(phi(jnp.asarray(r2.reshape(-1))))):
        v.append("phi depends on the input shape")
    try:
        if not _batch_independent_limiter(phi, r):
            v.append("phi is not elementwise (on a run-sized batch it differs from phi applied to one ratio at a "
                     "time: it depends on the batch size or statistics)")
    except Exception as exc:  # noqa: BLE001
        v.append(f"phi fails on a single slope ratio: {type(exc).__name__}: {exc}")
    return v


def check_flux(flux: Callable, gamma: float = 1.4) -> list[str]:
    UL, UR = flux_probes(gamma=gamma)
    v: list[str] = []
    try:
        F = np.asarray(flux(jnp.asarray(UL), jnp.asarray(UR), gamma))
    except Exception as exc:  # noqa: BLE001
        return [f"flux raised {type(exc).__name__}: {exc}"]
    if F.shape != UL.shape:
        return [f"flux returned shape {F.shape}, expected {UL.shape}"]
    if not np.all(np.isfinite(F)):
        v.append("flux is not finite on admissible states")
    # consistency on equal states
    Fc = np.asarray(flux(jnp.asarray(UL), jnp.asarray(UL), gamma))
    Fe = np.asarray(physical_flux(jnp.asarray(UL), gamma))
    scale = np.max(np.abs(Fe), axis=1, keepdims=True)
    err = np.max(np.abs(Fc - Fe) / scale)
    if not err <= CONSISTENCY_TOL:
        v.append(f"consistency flux(U, U) = F(U) violated: max relative error {err:.2e}")
    # mirror symmetry flux(R UR, R UL) = -R flux(UL, UR), relative to the largest flux magnitude involved
    Fm = np.asarray(flux(jnp.asarray(UR * R_MIRROR), jnp.asarray(UL * R_MIRROR), gamma))
    FR = np.asarray(physical_flux(jnp.asarray(UR), gamma))
    scale = np.max(np.abs(np.concatenate([F, Fe, FR], axis=1)), axis=1, keepdims=True)
    err = np.max(np.abs(Fm + F * R_MIRROR) / scale)
    if not err <= MIRROR_TOL:
        v.append(f"mirror symmetry violated: max relative error {err:.2e}")
    if not _bitwise_equal(F, np.asarray(flux(jnp.asarray(UL), jnp.asarray(UR), gamma))):
        v.append("flux is not deterministic")
    perm = np.random.default_rng(2).permutation(UL.shape[0])
    if not _bitwise_equal(np.asarray(flux(jnp.asarray(UL[perm]), jnp.asarray(UR[perm]), gamma)), F[perm]):
        v.append("flux is not row-wise (a permuted batch does not give the permuted output)")
    try:
        if not _batch_independent_flux(flux, UL, UR, gamma):
            v.append("flux is not row-wise (on a run-sized batch it differs from flux applied to one interface at "
                     "a time: it depends on the batch size or statistics)")
    except Exception as exc:  # noqa: BLE001
        v.append(f"flux fails on a single interface: {type(exc).__name__}: {exc}")
    return v


def check_run(W: np.ndarray) -> list[str]:
    """Run-level hard constraints on a final primitive state (n, 3)."""
    W = np.asarray(W)
    if not np.all(np.isfinite(W)):
        return ["non-finite state (NaN or Inf)"]
    v = []
    if np.any(W[:, 0] <= 0.0):
        v.append("negative or zero density")
    if np.any(W[:, 2] <= 0.0):
        v.append("negative or zero pressure")
    return v
