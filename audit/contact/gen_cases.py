"""Random admissible instances for the contact judge audit (format: docs/judge/contact_cases.md).

Seed 20261124 (numpy default_rng). Writes audit/contact/cases/batch_XX.yaml, at most 200 cases each:
  250 gap_closure with distort = 0 (C0a), 200 with distort > 0 (C1), 450 simple_shear, 100 hertz.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import yaml

SEED = 20261124
HERE = Path(__file__).resolve().parent
OUT = HERE / "cases"


def logu(rng, lo, hi):
    return float(math.exp(rng.uniform(math.log(lo), math.log(hi))))


def gap_case(rng, i, distorted):
    g = logu(rng, 0.01, 0.5)
    h = logu(rng, 0.3, 3.0)
    w = logu(rng, 0.05, 1.0)
    delta = h * logu(rng, 0.005, 0.45)  # indentation beyond the gap; admissible: g < push < g + h/2
    return dict(
        kind="gap_closure", id=f"{'C1' if distorted else 'C0a'}-{i:04d}",
        gap=g, height=h, width=w, push=g + delta,
        steps=int(rng.integers(2, 13)),
        nx=int(rng.integers(1, 5)), ny_body=int(rng.integers(1, 5)), ny_medium=int(rng.integers(1, 5)),
        E=logu(rng, 0.01, 100.0), nu=float(rng.uniform(0.0, 0.49)),
        gamma=logu(rng, 1e-7, 1e-2),
        distort=float(rng.uniform(0.01, 0.45)) if distorted else 0.0,
        seed=int(rng.integers(0, 1_000_000)),
    )


def shear_case(rng, i):
    return dict(
        kind="simple_shear", id=f"C0b-{i:04d}",
        shear=logu(rng, 0.01, 5.0), E=logu(rng, 0.01, 100.0), nu=float(rng.uniform(0.0, 0.49)),
        gamma=logu(rng, 1e-7, 1e-2),
    )


def hertz_case(rng, i):
    # Inside the case file's stated ranges (held-out family, every instance converged there).
    R = logu(rng, 0.5, 2.0)
    gap = R * float(rng.uniform(0.0015, 0.003))
    push = gap + R * float(rng.uniform(0.003, 0.005))
    return dict(
        kind="hertz", id=f"C2-{i:04d}",
        R=R, W=R, H=R, gap=gap, push=push, steps=12,
        nx=int(rng.integers(28, 37)), ny=16, ny_medium=4,
        E=logu(rng, 0.1, 10.0), nu=float(rng.uniform(0.15, 0.45)),
        gamma=logu(rng, 1e-6, 1e-5),
    )


def main():
    rng = np.random.default_rng(SEED)
    gap = [gap_case(rng, i, False) for i in range(250)] + [gap_case(rng, 250 + i, True) for i in range(200)]
    shear = [shear_case(rng, i) for i in range(450)]
    hz = [hertz_case(rng, i) for i in range(100)]
    OUT.mkdir(exist_ok=True)
    batches = [gap[0:150], gap[150:300], gap[300:450], shear[0:150], shear[150:300], shear[300:450],
               hz[0:50], hz[50:100]]
    for k, b in enumerate(batches):
        assert len(b) <= 200
        (OUT / f"batch_{k:02d}.yaml").write_text(yaml.safe_dump(b, sort_keys=False))
    print(len(gap), len(shear), len(hz))


if __name__ == "__main__":
    main()
