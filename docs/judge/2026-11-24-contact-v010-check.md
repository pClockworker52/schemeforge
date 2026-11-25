# contact-v0.10.dev acceptance check (2026-11-25, cloud)

Judge change 910ecdd, the two blind-audit fixes (docs/judge/contact_audit.md "Result"):
- g/2 is a load step of C0a and C1;
- the Newton test is scale-aware, with ε = 1e-3 · E · L.

Both are designed to leave the dev cases unchanged: E = L = 1 there, and g/2 is already step 2 of 6.

| Member | contact-v0.9.dev | contact-v0.10.dev | seconds (v0.10) |
|---|---|---|---|
| faltus2026 | r-20261124-101155-78d7 | r-20261125-070226-c01e | 34.1 |
| neo_hooke | r-20261124-101236-bc74 | r-20261125-070301-76ac | 34.3 |
| neo_hooke_iv | r-20261124-101314-ab36 | r-20261125-070336-4be8 | 36.1 |
| wriggers2013 | r-20261124-101352-eafc | r-20261125-070413-0c74 | 42.6 |

**Result:**
- **Dev:** all `ok`; **192 of 192 metric values are bitwise identical** to v0.9 (wall time excluded).
- **Self-check:** `sforge judge verify --arena contact` passes 12 of 12.
- **Promo:** values are expected to change for GF leak_pre and GF newton_iters. No promo run exists on v0.10 yet;
  docs/judge/contact_promo_wsl.md gives the steps.
- **Archive:** there are no contact candidates and no search archive to rescore (iron rule 2); the zoo is the only
  scored set.
