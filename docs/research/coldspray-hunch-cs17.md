# Cold spray: hunch CS-17 (substrate strain-hardening capacity, not hardness), registration (frozen)

Registered and frozen 2026-11-07 on Peter's instruction, after B02 was scored. Research track, not a ledger arena.
**It may not be tested on B02 or on any seen row**; B02 inspired it.

## Why

CS-16 (substrate hardness raises v_cr) was refuted on B02. The same Cu powder bonded at 566 m/s on a cold-rolled
full-hard Cu plate (105 HV) and at 641 m/s on an annealed plate (63 HV). Lucas (B02, read only after scoring)
explains it by the cold-worked plate's low remaining strain-hardening capacity: at equal velocity the particle jets
around almost the whole rim on the hard plate. Lienhard (B14, read after scoring) reports that the jet comes mostly
from the substrate side. CS-17 turns that explanation into a test on data not yet seen.

## Hunch

```yaml
- id: CS-17
  registered: 2026-11-07 (frozen)
  assumption_broken: >-
    Hardness or strength as the substrate descriptor (Hassani's impact ratio Z9 uses Y_d; CS-16 used hardness) and
    H2 in part (the substrate's state does not matter).
  statement: >-
    For one particle powder on substrates of the same metal, the substrate with the lower remaining
    strain-hardening capacity gives the lower v_cr, whatever its hardness. Hardening by cold work lowers v_cr;
    hardening that keeps the hardening capacity (precipitation, solid solution) does not lower it.
  mechanism: >-
    The rim of the crater is where the substrate jets. A substrate that cannot harden further localises its
    deformation at the rim earlier, so the substrate-side jet, and the interface stretch that comes with it, form at
    a lower impact velocity. In the blanket picture (CS-12), the interface reaches its dissolution state sooner.
  inputs: >-
    Remaining strain-hardening capacity H_c of each substrate, ranked by the first measure the paper reports:
    (1) Hollomon exponent n; (2) uniform elongation; (3) UTS / yield - 1; (4) prior cold work (reduction or prior
    plastic strain), higher meaning lower H_c. Pairs are compared only on one measure. If no measure is reported,
    no prediction.
  domain: >-
    Matched metal (particle and substrate the same base metal), polished, room temperature, normal incidence,
    **wrought monolithic substrates only** (plate, sheet, bar). Deposited substrates (cold-sprayed or otherwise
    built from particles) are excluded.
  predicted_effect:
    - {metric: "Delta = v(lower H_c) - v(higher H_c) per substrate pair", direction: down, size: "< -w"}
    - {metric: "same, for pairs hardened without loss of H_c (precipitation, solid solution)", direction: same,
       size: "|Delta| <= w (reported, no verdict)"}
  kill_criterion: >-
    On unseen pairs (two or more substrate states of one metal, one powder) with H_c ranked by the input rule and w
    the median window width (rule B6 where not printed): refuted if any pair with clearly different H_c shows
    Delta > +w. Supported if at least two pairs, from at least two papers or two metals, show Delta < -w and none
    is refuted. Inconclusive otherwise.
  magnitude: >-
    Not predicted. The only seen pair (B02, prior plastic strain 0.17 against 0.83) gave -75 m/s (-12 %); it is
    calibration context, not a prediction.
  known_relatives:
    - Lucas 2025 (B02): the authors' own explanation; CS-17 is a variant of it
    - Considere criterion (necking at a strain equal to n); Lucas's Eq. 19 uses a failure strain of about n
    - Hassani2020 impact ratio (Z9); CS-16 (refuted)
    - Lienhard 2020 (B14): jet mostly from the substrate side
  tension_with_seen_data: >-
    Panova2026b PA-02: the same 19 um Cu powder on polished cold-sprayed Cu (142 HV, heavily cold-worked, so low
    H_c) bonded HIGHER (653 m/s) than on a plate of 98 HV (567 m/s, PA-01). Without the domain restriction, CS-17
    would already be contradicted there. The restriction to wrought monolithic substrates is post hoc, added for
    this row. A plausible reason (prior-particle boundaries with oxide and porosity in a deposit change the
    interface) is a separate idea and is not part of CS-17.
  label: variant of Lucas 2025 (referee to confirm)
  status: open
  author: claude (with Peter)
```

## Where a test can come from

None of the pending blind papers (B03, B05, B06, B07, B12, B16) is known to contain a substrate series. Their inputs
will show it. A dedicated test would be one powder on two or three tempers of one wrought alloy, for example:
- annealed, cold-rolled and peak-aged Al 6061, where peak-aged is hard but keeps its hardening capacity;
- or Cu O-temper against H04 against a solution-strengthened Cu alloy.

That is a candidate second item for the measurement request, if the campaign trigger is met.
