"""Objective vectors per arena and slot for leaderboards and selection (PLAN §5.8): dev-suite metrics, each with its
direction. This is search policy, not scoring, so it lives outside the judge tree. Promotion uses the held-out
targets in docs/targets/, not these."""

from __future__ import annotations

MIN, MAX = "min", "max"

_SHOCK_CAPTURING = [
    ("R1", "shock_width", MIN),
    ("R1", "contact_width", MIN),
    ("N1", "res_orders_expl", MAX),
    ("N1", "newton_iters", MIN),
    ("N4", "roughness_J", MIN),
    ("S1", "order_smooth", MAX),
    ("R7", "l1_ref", MIN),
]

OBJECTIVES: dict[str, dict[str, list[tuple[str, str, str]]]] = {
    "euler1d": {
        "limiter": _SHOCK_CAPTURING,
        "limiter_stateful": _SHOCK_CAPTURING,
        "reconstruction": _SHOCK_CAPTURING,
        "flux": [
            ("R1", "contact_width", MIN),
            ("R5", "l1_smooth", MIN),
            ("R2", "l1_smooth", MIN),
            ("N1", "res_orders_expl", MAX),
            ("N1", "newton_iters", MIN),
            ("R7", "l1_ref", MIN),
        ],
    },
}
