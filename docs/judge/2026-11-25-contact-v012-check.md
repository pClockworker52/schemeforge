# contact-v0.12.dev acceptance check (2026-11-25, cloud)

Judge change 735b69e: max_step is measured on every HF instance in promo, not only on HX (DECISIONS 2026-11-25).
The change is promo only, so dev cannot change.

| Member | contact-v0.11.dev | contact-v0.12.dev | seconds |
|---|---|---|---|
| faltus2026 | r-20261125-072326-18cb | r-20261125-073430-de58 | 41.4 |
| neo_hooke | r-20261125-072411-bef5 | r-20261125-073512-d6f1 | 42.3 |
| neo_hooke_iv | r-20261125-072454-5cec | r-20261125-073555-d420 | 46.7 |
| wriggers2013 | r-20261125-072540-6c9e | r-20261125-073643-b67b | 51.6 |

**Result:**
- **Dev:** all `ok`, and **206 of 206 metric values are bitwise identical** to v0.11 (wall time excluded).
- **Promo:** not run here, because the held-out seed is on Peter's machine (contact_promo_wsl.md).
