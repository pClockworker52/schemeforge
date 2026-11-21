"""Checks for docs/research/problem-formalism.md (2026-11-22).

1. Symbolic adiabatic hardening modulus h_eff of the Johnson-Cook law with LAW4's plastic-work heating
   (beta = 1, no compression or q heating), and its sign along an adiabatic path for P-HG-Al.
2. Dimensional analysis of the impact problem: the parameters and their units, to list the lengths.
3. HRR exponents (textbook form) for the JC hardening exponent n.

Units: SI (Pa, K, m, s, kg). Run: `uv run python scripts/formalism_check.py`.
"""

from __future__ import annotations

import math

import sympy as sp
from scipy.integrate import solve_ivp

# P-HG-Al (opencourant-verification.md section 8.3; data/properties.csv)
RHO = 2700.0  # kg/m^3
CP = 896.9  # J/(kg K)
A, B, N, C, M = 148.4e6, 345.5e6, 0.183, 0.001, 0.895  # Pa, Pa, -, -, -
T_R, T_M = 293.0, 933.0  # K
RATE0 = 1.0  # 1/s, reference strain rate


def symbolic_heff() -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Return sigma_y, dT/deps (plastic work, beta = 1) and h_eff = d sigma_y / d eps_p along an adiabat."""
    eps, temp, rate = sp.symbols("epsilon_p T rate", positive=True)
    a, b, n, c, m, tr, tm, rho, cp, r0 = sp.symbols("A B n C m T_r T_m rho c_p rate0", positive=True)
    tstar = (temp - tr) / (tm - tr)
    sigma0 = (a + b * eps**n) * (1 + c * sp.log(rate / r0))  # athermal part
    sigma_y = sigma0 * (1 - tstar**m)
    dtdeps = sigma_y / (rho * cp)  # LAW4 plastic-work heating, beta = 1
    heff = sp.diff(sigma_y, eps) + sp.diff(sigma_y, temp) * dtdeps
    return sigma_y, dtdeps, sp.simplify(heff)


def adiabat(rate: float, eps_end: float = 3.0) -> list[tuple[float, float, float, float]]:
    """Integrate dT/deps = sigma_y/(rho c_p) from T_r; return (eps, T, sigma_y, h_eff) samples (h_eff in Pa)."""
    rf = 1.0 + C * math.log(rate / RATE0)

    def sig(eps: float, temp: float) -> float:
        ts = max(0.0, (temp - T_R) / (T_M - T_R))
        return 0.0 if ts >= 1.0 else (A + B * eps**N) * rf * (1.0 - ts**M)

    def heff(eps: float, temp: float) -> float:
        ts = (temp - T_R) / (T_M - T_R)
        if ts >= 1.0:
            return 0.0
        hard = B * N * eps ** (N - 1.0) * rf * (1.0 - ts**M)
        soft = -(A + B * eps**N) * rf * M * ts ** (M - 1.0) / (T_M - T_R) if ts > 0 else -math.inf
        return hard + soft * sig(eps, temp) / (RHO * CP)

    sol = solve_ivp(lambda e, y: [sig(e, y[0]) / (RHO * CP)], (1e-6, eps_end), [T_R], dense_output=True,
                    max_step=1e-3, rtol=1e-9, atol=1e-9)
    out = []
    for eps in (0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0):
        temp = float(sol.sol(eps)[0])
        out.append((eps, temp, sig(eps, temp), heff(eps, temp)))
    return out


def onset(rate: float) -> float:
    """Smallest eps_p (grid 1e-4) on the adiabat where h_eff <= 0."""
    samples = adiabat(rate)  # warm-up for the solver settings
    del samples
    rf = 1.0 + C * math.log(rate / RATE0)
    eps, temp, d = 1e-6, T_R, 1e-4
    while eps < 5.0:
        ts = max(0.0, (temp - T_R) / (T_M - T_R))
        s0 = (A + B * eps**N) * rf
        sy = s0 * (1.0 - ts**M)
        hard = B * N * eps ** (N - 1.0) * rf * (1.0 - ts**M)
        soft = -s0 * M * ts ** (M - 1.0) / (T_M - T_R) * sy / (RHO * CP) if ts > 0 else 0.0
        if eps > 1e-3 and hard + soft <= 0.0:
            return eps
        temp += sy / (RHO * CP) * d
        eps += d
    return math.nan


def main() -> None:
    sigma_y, dtdeps, heff = symbolic_heff()
    print("sigma_y =", sigma_y)
    print("dT/deps =", dtdeps)
    print("h_eff  =", heff)
    for rate in (1e6, 1e8):
        print(f"\nAdiabat at rate {rate:.0e} 1/s (rate factor {1 + C * math.log(rate):.4f}):")
        print(" eps_p     T [K]   T/T_m  sigma_y [MPa]  h_eff [MPa]")
        for eps, temp, sy, h in adiabat(rate):
            print(f"{eps:6.3f} {temp:9.1f} {temp / T_M:6.3f} {sy / 1e6:13.1f} {h / 1e6:12.1f}")
        print(f"h_eff <= 0 from eps_p = {onset(rate):.3f}")
    print("\nDimensional analysis (SI): parameters and units")
    params = {
        "R": "m", "s (spacing)": "m", "V": "m/s", "rho0": "kg/m^3", "G, K (moduli)": "Pa",
        "C0 (EOS)": "m/s", "S, gamma0, n, m, C": "-", "A, B": "Pa", "rate0": "1/s", "T_r, T_m": "K",
        "c_p": "J/(kg K)", "kappa (only with conduction)": "m^2/s",
    }
    for k, v in params.items():
        print(f"  {k:32s} {v}")
    print("  lengths: R, s; with conduction also sqrt(kappa t); rate0 with V gives V/rate0 = 600 m (not a"
          " small-scale length)")
    nn = N
    print(f"\nHRR (textbook): sigma ~ r^(-1/(N+1)), eps ~ r^(-N/(N+1)) with N = 1/n = {1 / nn:.3f}:"
          f" sigma ~ r^{-nn / (1 + nn):.3f}, eps ~ r^{-1 / (1 + nn):.3f}")


if __name__ == "__main__":
    main()
