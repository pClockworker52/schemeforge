# Secondary target A-c: contact sharpening without regression

Pre-registered on 2026-10-24 in docs/plans/2026-10-24-round4.md §3.2, before any round-4 work. Implemented as target
`Ac` in `src/schemeforge/core/promotion.py`: `sforge promote <id> --target Ac`. All checks run on the candidate's
held-out promo run under judge v1.5 or later. References are the limiter zoo's van Leer (as for Target A).

| # | Check | Threshold |
|---|---|---|
| C1 | RF1 contact_width median | ≤ 0.6 × van Leer's |
| C2 | RF1 shock_width median | ≤ 1.1 × van Leer's |
| C3–C8 | Target A's A3, A4, A5, A6, A7a/b, A8a/b | as in docs/targets/A.md |
| C9 | promo run status | ok (holds whenever `promote` runs: it needs an ok promo run) |
| B2 | paired bootstrap of RF1 contact_width vs van Leer | 95 % CI of the log ratio < 0 |

`promote` prints C3–C8 under their Target A ids (A3 … A8b). A candidate meeting A-c is labelled at most "variant of
characteristic THINC" unless the referee decides otherwise; A-c is a practical result, not a Target A promotion.
