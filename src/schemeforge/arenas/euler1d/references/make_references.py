"""Regenerate the cached fine-grid references (a judge change: commit, bump the judge version, rescore).

    uv run python -m schemeforge.arenas.euler1d.references.make_references
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from schemeforge.arenas.euler1d import zoo
from schemeforge.arenas.euler1d.cases import INITS, REFERENCES_DIR
from schemeforge.arenas.euler1d.unsteady import solve_unsteady

REFERENCES = {
    # file: (init, n, t_end, domain, reconstruction, flux, cfl)
    "shu_osher_weno5z_hllc_N12800.npz": ("shu_osher", 12800, 1.8, (-5.0, 5.0), "weno5z", "hllc", 0.5),
}


def make(name: str) -> Path:
    init, n, t_end, (a, b), rec, flux, cfl = REFERENCES[name]
    dx = (b - a) / n
    x = a + (np.arange(n) + 0.5) * dx
    t0 = time.perf_counter()
    res = solve_unsteady(INITS[init](x), dx, t_end, 1.4, zoo.load("reconstruction", rec),
                         flux=zoo.load("flux", flux), cfl=cfl)
    path = REFERENCES_DIR / name
    np.savez_compressed(path, W=np.asarray(res.W), x=x, t_end=t_end, steps=res.steps,
                        method=f"{rec}+{flux}+ssprk3 cfl={cfl}")
    print(f"{name}: {res.steps} steps in {time.perf_counter() - t0:.1f} s")
    return path


if __name__ == "__main__":
    for name in REFERENCES:
        make(name)
