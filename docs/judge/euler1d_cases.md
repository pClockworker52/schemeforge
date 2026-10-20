# Arena 1 case format (euler1d)

Breakers write cases in this format into `cases/quarantine/`; `sforge eval --case FILE` reads it. Every case
must be physically admissible (positive density and pressure, no vacuum, 0 < p_b/p₀ < 1) and have an exact
reference the judge computes itself. Units and conventions: `euler1d_spec.md`.

## Riemann problem (exact)

```yaml
kind: riemann
id: B-0001              # required; breaker cases use B-<number>
left: [1.0, 0.0, 100.0]  # rho, u, p
right: [0.01, 0.0, 0.001]
t_end: 0.01
n: 200                  # cells
gamma: 1.4              # optional, default 1.4
x0: 0.5                 # optional, initial discontinuity, default 0.5
domain: [0.0, 1.0]      # optional, default [0, 1]; transmissive boundaries
```

Waves must not reach the boundaries before `t_end` (the judge checks the exact wave speeds).

## Smooth periodic wave (exact: pure translation)

```yaml
kind: smooth
id: B-0002
ns: [50, 100, 200]      # grids for the observed order
t_end: 1.0
amp: 0.2                # rho = 1 + amp sin(2 pi x)
u0: 1.0
gamma: 1.4
```

## Steady nozzle (exact)

```yaml
kind: nozzle
id: B-0003
pb: 0.6784              # p_b / p0
n: 120
gamma: 1.4
nozzle:                 # optional, default anderson
  type: parabolic       # anderson | parabolic | conical (formulas: euler1d_spec.md §4)
  x_in: 0.0             # optional inlet position, default 0 (ignored for anderson)
  area_ratio: 4.0       # exit area / throat area
  length: 2.0           # divergent length in throat units
  inlet_ratio: 2.0      # inlet area / throat area (convergent length 1)
```

## Back-pressure sweep (exact at every point)

```yaml
kind: nozzle_sweep
id: B-0004
pbs: [0.60, 0.62, 0.64]
n: 120
solvers: [implicit]     # implicit | explicit
nozzle: {type: anderson}
```

Geometry types and formulas: `euler1d_spec.md` §4 (`conical` is also available, `x_in` moves the inlet).

A file holding a YAML list of cases is accepted by `sforge judge exact` (batch mode); `sforge eval --case`
takes a single case.

## Dev suite (fixed, visible)

| ID | Definition |
|---|---|
| R1 | Sod: (1, 0, 1) / (0.125, 0, 0.1), t = 0.2, x0 = 0.5, N = 200 |
| R2 | 123: (1, −2, 0.4) / (1, 2, 0.4), t = 0.15, N = 200 |
| R3 | left blast: (1, 0, 1000) / (1, 0, 0.01), t = 0.012, N = 200 |
| R4 | shock collision (Toro test 5 states), t = 0.035, x0 = 0.4, N = 200 |
| R5 | stationary contact (1.4, 0, 1) / (1, 0, 1), t = 2, N = 100 |
| R6 | shock of Mach 3 into (1, ·, 1), speed 0.05·max(\|u\| + a), from x0 = 0.2, t = 0.95, N = 200 |
| R7 | Shu–Osher: (3.857143, 2.629369, 10.333333) for x < −4, (1 + 0.2 sin 5x, 0, 1) otherwise, on [−5, 5], t = 1.8, N = 400. Reference: WENO5-Z + HLLC + SSP-RK3 (CFL 0.5) at N = 12,800, averaged onto the case grid (`references/`; self-check N = 6,400 vs 12,800: L1 ρ difference 4.3e-4 on 400 cells) |
| S1 | smooth wave, amp 0.2, u = 1, p = 1, N = 50/100/200, t = 1 |
| N1 | Anderson nozzle, p_b = 0.6784, N = 120 |
| N2 | Anderson nozzle, p_b = 0.995 (unchoked, exit Mach 0.085), N = 120 |
| N3 | Anderson nozzle, p_b = 0.01 (supersonic exit), N = 120 |
| N4 | Anderson nozzle, 11 back pressures moving the shock over 30 cells around x = 2.1, implicit only, N = 120 |
