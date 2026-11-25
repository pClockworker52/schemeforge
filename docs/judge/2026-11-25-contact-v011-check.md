# contact-v0.11.dev acceptance check (2026-11-25, cloud)

Judge change 9086db7: C4, frictionless sliding (dev case C4-g6; held-out family SL). DECISIONS 2026-11-25.

| Member | contact-v0.10.dev | contact-v0.11.dev | seconds | C4-g6 shear_parasitic | fn_rise | converged |
|---|---|---|---|---|---|---|
| faltus2026 | r-20261125-070226-c01e | r-20261125-072326-18cb | 43.8 | 0.0622 | 0.0188 | 1 |
| neo_hooke | r-20261125-070301-76ac | r-20261125-072411-bef5 | 41.7 | — | — | 0 |
| neo_hooke_iv | r-20261125-070336-4be8 | r-20261125-072454-5cec | 44.9 | — | — | 0 |
| wriggers2013 | r-20261125-070413-0c74 | r-20261125-072540-6c9e | 52.9 | 0.0399 | 0.0176 | 1 |

**Result:**
- **Unchanged cases:** all eight runs are `ok`. **192 of 192 pre-existing metric values are bitwise identical**
  to v0.10.
- **C4 is new and discriminates.**
  - The robust media (faltus2026, wriggers2013) slide, but their medium resists: 4–6 % of the normal force is
    needed to slide, against 0 for classical frictionless contact, with 2 % ploughing.
  - The neo-Hookean media fail Newton on the slide. This is a result (converged 0), not a violation.
- **Dev budget:** 42–53 s per member, within 60 s. Memory was not remeasured; C4's mesh is smaller than C2's
  (16 × 10 per half against 32 × 16).
- **Self-check:** judge verify passes 13 of 13 (C4 classical shear_parasitic 9.2e-15, fn_rise 1.7e-10).
