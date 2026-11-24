# contact-v0.9.dev acceptance check (2026-11-24, cloud)

Judge change eaf87f1: new `arenas/contact/verify.py` (`sforge judge verify` and `sforge judge exact`). The scoring
code is unchanged. Check: the zoo dev runs before and after, compared on every metric of every case.

| Member | contact-v0.8.dev | contact-v0.9.dev | seconds (before / after) |
|---|---|---|---|
| faltus2026 | r-20261124-095229-3338 | r-20261124-101155-78d7 | 38.7 / 39.7 |
| neo_hooke | r-20261124-095309-2957 | r-20261124-101236-bc74 | 36.0 / 36.6 |
| neo_hooke_iv | r-20261124-095346-da9d | r-20261124-101314-ab36 | 38.3 / 36.8 |
| wriggers2013 | r-20261124-095425-7803 | r-20261124-101352-eafc | 45.9 / 46.9 |

**Result:**
- **Scores:** all eight runs are `ok`, with no violations. **192 of 192 metric values are bitwise identical**
  (wall time excluded).
- **Dev budget:** within 60 s for every member (Gate 6 item 6). Memory was not measured in this check.
- **Self-check:** `sforge judge verify --arena contact` passes 12 of 12.
