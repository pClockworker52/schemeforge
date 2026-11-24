# Arena 2 case format (for `sforge judge exact --arena contact`)

A case is a YAML mapping with `kind` and `id`. Omitted fields take the defaults below. Unknown fields are an error.
A YAML list of mappings is a batch. Units, geometry and meaning are in docs/judge/contact_spec.md.

## `kind: gap_closure` (C0a; C1 when `distort` > 0)

| Field | Default | Meaning |
|---|---|---|
| gap | 0.1 | medium thickness g |
| height | 1.0 | body height h |
| width | 0.2 | width w |
| push | 0.15 | top displacement at full push |
| steps | 6 | equal load steps |
| nx, ny_body, ny_medium | 1, 2, 2 | cells across, in the body, in the medium |
| E, nu | 1.0, 0.3 | body Young's modulus and Poisson's ratio |
| gamma | 1e-6 | medium stiffness scale γ |
| distort | 0.0 | corner-node moves as a fraction of the cell size (C1) |
| seed | 0 | seed of the distortion (the medium layer uses seed + 1) |

Admissible: g, h, w, E and γ > 0; 0 ≤ ν < 0.5; g < push < g + h/2; 0 ≤ distort < 0.5; steps ≥ 2; at least one cell
in each direction.

## `kind: simple_shear` (C0b)

| Field | Default | Meaning |
|---|---|---|
| shear | 0.5 | s in F = [[1, s, 0], [0, 1, 0], [0, 0, 1]] |
| E, nu | 1.0, 0.3 | moduli defining μ and λ |
| gamma | 1e-5 | γ |

Admissible: s, E and γ > 0; 0 ≤ ν < 0.5.

## `kind: hertz` (C2)

| Field | Default | Meaning |
|---|---|---|
| R, W, H | 1.0, 1.0, 1.0 | radius of the parabolic profile, half width, height |
| gap | 0.002 | initial gap at x = 0 |
| push | 0.006 | top displacement at full push |
| steps | 12 | equal load steps |
| nx, ny, ny_medium | 32, 16, 4 | columns, body rows, medium rows |
| E, nu | 1.0, 0.3 | body moduli |
| gamma | 1e-6 | γ (not used by the classical reference) |
| kr | 5e-7 | regularization strength (not used by the classical reference) |

Admissible: R, W, H, gap, E, γ and kr > 0; 0 ≤ ν < 0.5; gap < push < H/10; steps ≥ 2. The spec's Hertz conditions
(a/R ≤ 0.1, a flat at least 20 a wide) hold for the defaults. The held-out Hertz family stays within these ranges,
and every instance there converged (spec §Step 4): R 0.5–2 with W = H = R; gap 0.15–0.3 % of R; indentation
beyond the gap 0.3–0.5 % of R; 28–36 columns.
