"""MAP-Elites archive over behaviour descriptors, with fingerprint-based duplicate detection (PLAN §5.8).

The archive stores candidate ids and their descriptor cell; scores always come from the registry (leaderboard),
so there is no second source of truth for evaluations. State is JSON-serializable for resumable runs.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from .probes import fingerprint_distance

DUPLICATE_DISTANCE = 1e-3  # fingerprints closer than this are the same method

# per (arena, slot): descriptor name -> (bin edges); values outside fall into the first / last bin
GRIDS: dict[tuple[str, str], dict[str, np.ndarray]] = {
    # Edges fitted to where the zoo and the C1/C2 calibration children actually lie (DECISIONS.md, 2026-10-21):
    # the first grids spread 7 zoo limiters over 5 cells and C2's 48 fluxes over 3.
    ("euler1d", "limiter"): {
        # mean phi on [0, 3]: minmod 0.83, van Albada 0.97, van Leer 1.07, MC 1.22, Koren 1.29, superbee 1.42
        "compressiveness": np.array([0.0, 0.85, 0.95, 1.05, 1.15, 1.25, 1.35, 1.45]),
        # max |phi''| on [0.05, 3] with h = 0.01: a kink of size k shows up as ~k/h, so >= 30 means kinked;
        # the kinked bins separate kink size 1 (minmod, MC: 100), 4/3 (Koren) and 2 (superbee)
        "smoothness": np.array([0.0, 0.3, 1.0, 3.0, 10.0, 30.0, 75.0, 115.0, 150.0]),
    },
    ("euler1d", "limiter_stateful"): {  # descriptors of phi at the initial state, same edges as the limiter
        "compressiveness": np.array([0.0, 0.85, 0.95, 1.05, 1.15, 1.25, 1.35, 1.45]),
        "smoothness": np.array([0.0, 0.3, 1.0, 3.0, 10.0, 30.0, 75.0, 115.0, 150.0]),
    },
    ("euler1d", "reconstruction"): {
        # engine/probes.py _reconstruction: first order 0, MUSCL minmod 0.47, van Albada 0.52, van Leer 0.62,
        # Koren 0.69, MC 0.70, superbee 0.76, WENO5-Z 0.78, THINC/BVD 0.85
        "compressiveness": np.array([0.0, 0.3, 0.5, 0.6, 0.66, 0.72, 0.8, 0.9]),
        # log10 face error on the smooth wave: WENO5-Z -4.7, MUSCL -2.8 to -2.3, THINC/BVD -2.7, first order -1.6
        "smooth_error": np.array([-16.0, -6.0, -5.0, -4.0, -3.0, -2.5, -2.0, -1.0]),
    },
    ("euler1d", "reconstruction_stateful"): {  # descriptors at the initial state, same edges
        "compressiveness": np.array([0.0, 0.3, 0.5, 0.6, 0.66, 0.72, 0.8, 0.9]),
        "smooth_error": np.array([-16.0, -6.0, -5.0, -4.0, -3.0, -2.5, -2.0, -1.0]),
    },
    ("euler1d", "flux"): {
        # median |central - F| / |jump| on the probes: HLLC 2.13, HLL 2.69, Rusanov 4.42
        "dissipation": np.array([0.0, 0.5, 1.0, 1.5, 1.75, 2.0, 2.25, 2.5, 3.0, 3.5, 4.0, 4.5]),
        "contact_dissipation": np.concatenate([[0.0], np.geomspace(1e-12, 1.0, 5)]),
    },
}


def cell_of(arena: str, slot: str, descriptors: dict[str, float]) -> tuple[int, ...]:
    grid = GRIDS.get((arena, slot), {})
    out = []
    for name, edges in grid.items():
        v = descriptors.get(name, math.nan)
        out.append(-1 if not math.isfinite(v) else int(np.clip(np.searchsorted(edges, v, side="right") - 1,
                                                               0, len(edges) - 1)))
    return tuple(out)


@dataclass
class Archive:
    arena: str
    slot: str
    elites: dict[str, str] = field(default_factory=dict)  # "i,j" -> candidate id
    fingerprints: dict[str, list[float]] = field(default_factory=dict)  # candidate id -> fingerprint
    references: dict[str, list[float]] = field(default_factory=dict)  # zoo name -> fingerprint
    duplicates: dict[str, str] = field(default_factory=dict)  # candidate id -> what it duplicates

    def duplicate_of(self, fp: list[float], exclude: str | None = None) -> str | None:
        for name, ref in self.references.items():
            if fingerprint_distance(fp, ref) < DUPLICATE_DISTANCE:
                return f"zoo:{name}"
        for cid, ref in self.fingerprints.items():
            if cid != exclude and fingerprint_distance(fp, ref) < DUPLICATE_DISTANCE:
                return cid
        return None

    def offer(self, cid: str, probe: dict[str, Any], score: float, score_of) -> str:
        """Try to place a candidate. Returns 'duplicate:<x>', 'new cell', 'replaced <old>' or 'rejected'.
        score_of(cid) gives the current score of an incumbent (lower is better)."""
        fp = probe.get("fingerprint") or []
        dup = self.duplicate_of(fp, exclude=cid) if fp else None
        if dup:
            self.duplicates[cid] = dup
            return f"duplicate:{dup}"
        key = ",".join(map(str, cell_of(self.arena, self.slot, probe.get("descriptors", {}))))
        old = self.elites.get(key)
        if old is None or score < score_of(old):
            self.elites[key] = cid
            self.fingerprints[cid] = fp
            if old is not None:
                self.fingerprints.pop(old, None)
            return "new cell" if old is None else f"replaced {old}"
        return "rejected"

    def members(self) -> list[str]:
        return list(self.elites.values())

    def to_dict(self) -> dict[str, Any]:
        return {"arena": self.arena, "slot": self.slot, "elites": self.elites, "fingerprints": self.fingerprints,
                "references": self.references, "duplicates": self.duplicates}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Archive:
        return cls(d["arena"], d["slot"], d.get("elites", {}), d.get("fingerprints", {}),
                   d.get("references", {}), d.get("duplicates", {}))
