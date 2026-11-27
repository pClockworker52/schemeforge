"""Objective vectors per arena and slot for leaderboards and selection (PLAN §5.8): dev-suite metrics, each with its
direction. This is search policy, not scoring, so it lives outside the judge tree. Promotion uses the held-out
targets in docs/targets/, not these."""

from __future__ import annotations

MIN, MAX, ABSMIN = "min", "max", "absmin"  # absmin: minimise |v| (signed errors such as a_err)

_SHOCK_CAPTURING = [
    ("R1", "shock_width", MIN),
    ("R1", "contact_width", MIN),
    ("N1", "res_orders_expl", MAX),
    ("N1", "newton_iters", MIN),
    ("N4", "roughness_J", MIN),
    ("S1", "order_smooth", MAX),
    ("R7", "l1_ref", MIN),
    # since judge v1.4 (accepted breaker cases): strong slow shock, the dev proxy for Target A's A7b overshoot,
    # and the smooth wave run past ~1000 steps, which exposes state that acts late (round-2 ratchets)
    ("B-0010", "overshoot", MIN),
    ("B-0002", "order_smooth", MAX),
]

OBJECTIVES: dict[str, dict[str, list[tuple[str, str, str]]]] = {
    "euler1d": {
        "limiter": _SHOCK_CAPTURING,
        "limiter_stateful": _SHOCK_CAPTURING,
        "reconstruction": _SHOCK_CAPTURING,
        "reconstruction_stateful": _SHOCK_CAPTURING,
        "flux": [
            ("R1", "contact_width", MIN),
            ("R5", "l1_smooth", MIN),
            ("R2", "l1_smooth", MIN),
            ("N1", "res_orders_expl", MAX),
            ("N1", "newton_iters", MIN),
            ("R7", "l1_ref", MIN),
        ],
    },
    # Arena 2: the dev stand-ins of Target D's axes (docs/targets/D.md). p_l2 and leak_out are mesh-sensitive
    # (spec §mesh_sens) and stay out; max_step exists on promo only.
    "contact": {
        "medium": [
            ("C0a-g5", "gap_res", MIN),          # D1 tight
            ("C0a-g5", "leak_pre", MIN),         # D6 no force before contact
            ("C0b-s2", "shear_parasitic", MIN),  # D7
            ("C2-g5", "a_err", ABSMIN),          # D4
            ("C2-g6", "a_err", ABSMIN),
            ("C2-g6", "p0_err", ABSMIN),         # D5
            ("C2-g6", "newton_iters", MIN),      # robustness (B2 compares HF newton_iters)
            ("C4-g6", "shear_parasitic", MIN),   # D8
        ],
    },
}


# Target A screen on dev (round-4 plan, step 2.3): the dev stand-ins for docs/targets/A.md, (case, metric, op,
# threshold). Selection ranks by the number of failed checks first, then by Pareto rank and score, so that a candidate
# cannot climb by trading A1 for a contact gain the scalar score rewards (round 3, lesson 1). Thresholds: A1 2.6 + 0.1
# (dev R1 runs ~0.1 cell above the RF1 median); overshoot 1.1 x van Leer's dev values (judge v1.4,
# r-20261022-164139-960f: B-0010 0.0249, R6 0.0151); A8a 1.5 x van Leer's B-0004 contact (12.7).
_TARGET_A_DEV = [
    ("R1", "shock_width", "<=", 2.7),            # A1
    ("R1", "contact_width", "<=", 6.5),          # A2
    ("N1", "converged_expl", ">=", 1.0),         # A3
    ("N5", "converged_expl", ">=", 1.0),
    ("N6", "converged_expl", ">=", 1.0),
    ("N1", "converged_impl", ">=", 1.0),         # A4
    ("N4", "converged_impl", ">=", 1.0),
    ("N4", "roughness_J", "<=", 0.002),          # A5
    ("S1", "order_smooth", ">=", 1.9),           # A6
    ("R6", "overshoot", "<=", 0.0166),           # A7a stand-in
    ("B-0010", "overshoot", "<=", 0.0274),       # A7b stand-in
    ("B-0004", "contact_width", "<=", 19.0),     # A8a stand-in
    ("B-0002", "order_smooth", ">=", 1.8),       # A8b
]

# Target D screen on dev (step 7, 2026-11-27): dev stand-ins for docs/targets/D.md, built like D from the zoo, on the
# dev runs of contact-v1.0 (faltus2026 r-20261127-201026-a6a1). D1: 0.1 x faltus2026's C0a-g5 gap_res (0.0290);
# D6, D7, D8: <= faltus2026's dev value, rounded up (C0a-g5 leak_pre 3.771e-4, C0b-s2 shear_parasitic 1.733e-4,
# C4-g6 0.0622); D2/D8 converged on the C2 and C4 cases; D4, D5: |a_err|, |p0_err| <= 0.02 on C2-g5 and C2-g6
# (the HF gamma range 1e-6..1e-5 lies between them). D3 (max_step) has no dev stand-in. Every zoo member fails
# 4-5 checks (faltus2026 5, neo_hooke 4, neo_hooke_iv 4, wriggers2013 5).
_TARGET_D_DEV = [
    ("C0a-g5", "gap_res", "<=", 0.0029),         # D1
    ("C2-g5", "converged", ">=", 1.0),           # D2
    ("C2-g6", "converged", ">=", 1.0),
    ("C2-g5", "a_err", "abs<=", 0.02),           # D4
    ("C2-g6", "a_err", "abs<=", 0.02),
    ("C2-g5", "p0_err", "abs<=", 0.02),          # D5
    ("C2-g6", "p0_err", "abs<=", 0.02),
    ("C0a-g5", "leak_pre", "<=", 3.78e-4),       # D6
    ("C0b-s2", "shear_parasitic", "<=", 1.74e-4),  # D7
    ("C4-g6", "converged", ">=", 1.0),           # D8
    ("C4-g6", "shear_parasitic", "<=", 0.0622),
]

SCREENS: dict[str, dict[str, list[tuple[str, str, str, float]]]] = {
    "euler1d": {s: _TARGET_A_DEV for s in ("limiter", "limiter_stateful", "reconstruction", "reconstruction_stateful")},
    "contact": {"medium": _TARGET_D_DEV},
}


def screen_fails(arena: str, slot: str, values: dict[str, float]) -> int:
    """Number of failed screen checks (a missing or non-finite value fails); 0 for slots without a screen."""
    import math

    fails = 0
    for case, metric, op, thr in SCREENS.get(arena, {}).get(slot, []):
        v = values.get(f"{case}.{metric}")
        if v is None or not math.isfinite(v):
            ok = False
        elif op == "abs<=":
            ok = abs(v) <= thr
        else:
            ok = v <= thr if op == "<=" else v >= thr
        fails += not ok
    return fails

