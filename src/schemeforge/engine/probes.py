"""Behaviour descriptors and novelty fingerprints (PLAN §5.8). Search policy, not scoring: this runs inside the
sandboxed worker (the candidate is untrusted code) but lives outside the judge tree.

probe(fn, arena, slot) -> {"descriptors": {...}, "fingerprint": [...]} (JSON-serializable)
"""

from __future__ import annotations

from typing import Any

import numpy as np

# limiter: descriptors on r in [0, 3]; fingerprint = phi at 64 fixed slope ratios
LIMITER_R = np.linspace(0.0, 3.0, 301)
LIMITER_FINGERPRINT_R = np.concatenate(
    [np.linspace(-1.0, 0.0, 8), np.linspace(0.05, 3.0, 48), np.geomspace(3.5, 50, 8)]
)


def probe(fn, arena: str, slot: str) -> dict[str, Any]:
    if arena == "euler1d" and slot == "limiter":
        return _limiter(fn)
    if arena == "euler1d" and slot == "limiter_stateful":
        return _limiter_stateful(fn)
    if arena == "euler1d" and slot == "flux":
        return _flux(fn)
    if arena == "euler1d" and slot == "reconstruction":
        return _reconstruction(lambda W: fn(W, 1.4))
    if arena == "euler1d" and slot == "reconstruction_stateful":
        return _reconstruction_stateful(fn)
    return {"descriptors": {}, "fingerprint": []}


def _limiter(phi) -> dict[str, Any]:
    import jax.numpy as jnp

    v = np.asarray(phi(jnp.asarray(LIMITER_R)), dtype=float)
    h = LIMITER_R[1] - LIMITER_R[0]
    second = np.abs(np.diff(v, 2)) / h**2
    inner = LIMITER_R[1:-1] >= 0.05  # skip the kink every TVD limiter has at r = 0
    return {
        "descriptors": {
            "compressiveness": float(np.mean(v)),  # mean phi on [0, 3]
            "smoothness": float(np.max(second[inner])),  # max |phi''| on [0.05, 3] (large = kinked)
        },
        "fingerprint": np.asarray(phi(jnp.asarray(LIMITER_FINGERPRINT_R)), dtype=float).tolist(),
    }


def _limiter_stateful(phi_s) -> dict[str, Any]:
    """Descriptors of phi at the initial state 0; the fingerprint adds the new state at 0 and phi at a later state
    (s = 1e4), so a frozen limiter differs from its plain version."""
    import jax.numpy as jnp

    def at(s):
        return lambda r: phi_s(r, jnp.full_like(r, s))

    out = _limiter(lambda r: at(0.0)(r)[0])
    rf = jnp.asarray(LIMITER_FINGERPRINT_R)
    out["fingerprint"] += [*np.asarray(at(0.0)(rf)[1], dtype=float).tolist(),
                           *np.asarray(at(1e4)(rf)[0], dtype=float).tolist()]
    return out


def _flux(flux) -> dict[str, Any]:
    import jax.numpy as jnp

    from schemeforge.arenas.euler1d.constraints import flux_probes
    from schemeforge.arenas.euler1d.numerics import physical_flux

    UL, UR = flux_probes(m=64, seed=7)
    F = np.asarray(flux(jnp.asarray(UL), jnp.asarray(UR), 1.4), dtype=float)
    central = 0.5 * np.asarray(physical_flux(jnp.asarray(UL), 1.4) + physical_flux(jnp.asarray(UR), 1.4))
    jump = np.abs(UR - UL) + 1e-300
    diss = np.abs(central - F) / jump  # effective dissipation coefficient per component
    # a stationary contact: zero dissipation keeps it exactly
    rho = np.array([[1.4, 0.0, 1.0 / 0.4]]), np.array([[1.0, 0.0, 1.0 / 0.4]])
    Fc = np.asarray(flux(jnp.asarray(rho[0]), jnp.asarray(rho[1]), 1.4), dtype=float)
    return {
        "descriptors": {
            "dissipation": float(np.median(diss)),
            "contact_dissipation": float(abs(Fc[0, 0])),
        },
        "fingerprint": (F / (np.abs(central) + 1.0)).ravel()[:192].tolist(),
    }


# reconstruction: smeared steps (tanh, widths 0.5-2 cells, sub-cell offsets) and a smooth wave, 16 interfaces each
RECON_CELLS = 21  # padded cells: 16 interfaces
RECON_STEPS = [(w, x0) for w in (0.5, 1.0, 2.0) for x0 in (0.0, 0.25, 0.5)]
RECON_WAVE = 16.0  # cells per wavelength


def _recon_profiles() -> tuple[list[np.ndarray], np.ndarray, np.ndarray]:
    """Padded grids (RECON_CELLS, 3), the same profile in rho, u and p (offset to stay positive): the smeared steps,
    then the wave as cell averages, plus the wave's exact values at the 16 interfaces."""
    i = np.arange(RECON_CELLS) - RECON_CELLS / 2 + 0.5  # cell centres, the middle interface at 0
    grids = [np.repeat((1.0 + 0.5 * (1.0 + np.tanh((i - x0) / w)))[:, None], 3, axis=1) for w, x0 in RECON_STEPS]
    k = 2.0 * np.pi / RECON_WAVE
    avg = 1.0 + 0.2 * np.sin(k * i) * np.sin(k / 2) / (k / 2)  # exact cell averages
    faces = i[2:-3] + 0.5  # interfaces between padded cells j + 2 and j + 3
    return grids, np.repeat(avg[:, None], 3, axis=1), 1.0 + 0.2 * np.sin(k * faces)


def _reconstruction(rec) -> dict[str, Any]:
    """rec(W) -> (WL, WR). compressiveness: on the steps of width <= 1 cell, the share of the jump between
    neighbouring cells that the faces take up, sum((WL - W_left) + (W_right - WR)) / sum(W_right - W_left) over the
    interfaces (first order 0; THINC/BVD 0.85, WENO5-Z 0.78, MUSCL-superbee 0.76, MUSCL-minmod 0.47).
    smooth_error: log10 of the mean face error on the wave (WENO5-Z -4.7, MUSCL -2.3 to -2.8, first order -1.6)."""
    import jax.numpy as jnp

    steps, wave, exact = _recon_profiles()
    taken, total, prints = 0.0, 0.0, []
    for (width, _), W in zip(RECON_STEPS, steps, strict=True):
        WL, WR = (np.asarray(x, dtype=float)[:, 0] for x in rec(jnp.asarray(W)))
        left, right = W[2:-3, 0], W[3:-2, 0]
        if width <= 1.0:
            taken += float(np.sum((WL - left) + (right - WR)))
            total += float(np.sum(right - left))
        prints += [*WL, *WR]
    WL, WR = (np.asarray(x, dtype=float)[:, 0] for x in rec(jnp.asarray(wave)))
    err = 0.5 * (np.mean(np.abs(WL - exact)) + np.mean(np.abs(WR - exact)))
    return {
        "descriptors": {"compressiveness": taken / total, "smooth_error": float(np.log10(err + 1e-16))},
        "fingerprint": [*prints, *WL, *WR],
    }


def _reconstruction_stateful(rec_s) -> dict[str, Any]:
    """Descriptors at the initial state 0; the fingerprint adds the new state at 0 and the faces at a late state
    (s = 1e4), as for limiter_stateful."""
    import jax.numpy as jnp

    def at(s):
        return lambda W: rec_s(W, 1.4, jnp.full((W.shape[0] - 2, 3), s))

    out = _reconstruction(lambda W: at(0.0)(W)[:2])
    late = _reconstruction(lambda W: at(1e4)(W)[:2])
    W = jnp.asarray(_recon_profiles()[0][4])
    out["fingerprint"] += [*np.asarray(at(0.0)(W)[2], dtype=float)[:, 0].tolist(), *late["fingerprint"]]
    return out


def fingerprint_distance(a: list[float], b: list[float]) -> float:
    """Max absolute difference, scaled by the larger magnitude (inf if the shapes differ)."""
    x, y = np.asarray(a, float), np.asarray(b, float)
    if x.shape != y.shape or x.size == 0:
        return float("inf")
    return float(np.max(np.abs(x - y)) / max(1.0, float(np.max(np.abs(x))), float(np.max(np.abs(y)))))
