"""Post-hoc check of the spall law Z7 on B02 (Cu powder on soft and hard Cu C110), 2026-11-07.

Z7 (Lucas thesis Eq. 19; form also in Panova2026b): v_cr = (2/k) (2 Y_d eps_c / B)^(1/2) C0.
k is unknown, so only the ratio v_cr(soft) / v_cr(hard) is testable. C0 and B are equal for the two plates
(3950 m/s, 137 GPa) and cancel.

Inputs (all exposed: B02 is scored; vcr_lipit.csv rows B-B02-c1/c2, blind_inputs.csv):
- plates (Lucas ch. 4 Table 2): soft Y_d 351 MPa, eps_c 0.29; hard Y_d 562 MPa, eps_c 0.16;
- particle: Y_d 383 +- 65 MPa (Lucas ch. 3); particle eps_c not reported;
- measured: v_cr 641 (soft), 566 (hard) m/s, each +-2 % (no window bounds printed).

Variants:
- substrate only (Lucas's own evaluation): ratio = sqrt(Y_s eps_s / Y_h eps_h);
- arithmetic-mean mixing (Panova2026b form): Y and eps each averaged over particle and substrate; the ratio then
  depends on the unknown particle eps_p, so the script solves for the eps_p that reproduces the measurement.

Usage: python scripts/z7_cu_posthoc.py
"""

from __future__ import annotations

import math

Y_SOFT, EPS_SOFT = 351.0, 0.29
Y_HARD, EPS_HARD = 562.0, 0.16
Y_P, Y_P_ERR = 383.0, 65.0
V_SOFT, V_HARD, REL_ERR = 641.0, 566.0, 0.02


def ratio_mixed(eps_p: float, y_p: float = Y_P) -> float:
    """v_soft / v_hard under arithmetic-mean mixing of Y_d and eps_c (dimensionless)."""
    soft = 0.25 * (y_p + Y_SOFT) * (eps_p + EPS_SOFT)
    hard = 0.25 * (y_p + Y_HARD) * (eps_p + EPS_HARD)
    return math.sqrt(soft / hard)


def eps_p_for(ratio: float, y_p: float = Y_P) -> float:
    """Particle failure strain that makes ratio_mixed equal `ratio` (solves the linear equation in eps_p)."""
    a = (y_p + Y_SOFT) / (y_p + Y_HARD)
    r2 = ratio * ratio
    return (a * EPS_SOFT - r2 * EPS_HARD) / (r2 - a)


def main() -> None:
    meas = V_SOFT / V_HARD
    err = meas * math.hypot(REL_ERR, REL_ERR)
    print(f"measured ratio soft/hard: {meas:.4f} +- {err:.3f} (2 % per v_cr, combined)")
    sub = math.sqrt(Y_SOFT * EPS_SOFT / (Y_HARD * EPS_HARD))
    print(f"Z7 substrate only: {sub:.4f}  (predicts hard = {V_SOFT / sub:.0f} m/s from soft; measured {V_HARD:.0f})")
    for eps in (0.0, 0.05, 0.1, 0.16, 0.29, 0.5):
        print(f"Z7 mixed, eps_p = {eps:4.2f}: ratio {ratio_mixed(eps):.4f}")
    for y in (Y_P - Y_P_ERR, Y_P, Y_P + Y_P_ERR):
        lo, mid, hi = eps_p_for(meas + err, y), eps_p_for(meas, y), eps_p_for(meas - err, y)
        # sign of the contrast flips where ratio_mixed = 1
        a = (y + Y_SOFT) / (y + Y_HARD)
        flip = (a * EPS_SOFT - EPS_HARD) / (1 - a)
        print(f"Y_p = {y:.0f} MPa: eps_p to match {mid:.3f} (range {lo:.3f}-{hi:.3f}); "
              f"soft > hard only if eps_p < {flip:.3f}")


if __name__ == "__main__":
    main()
