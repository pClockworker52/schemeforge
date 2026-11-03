# Cold spray: retrospective zoo test v1, results

Scored 2026-11-03 under [coldspray-preregistration.md](coldspray-preregistration.md). Commit order:
pre-registration and predictions abce3f6, scoring script 045409d, then these results with
`data/scores_v1.csv`. Retrospective, not blind (I had seen the data). Not a judge run: no sforge run ids exist
for this track; the evidence is the committed CSV files and `python -m schemeforge.research.coldspray_score`.

d = distance outside the measured window divided by its midpoint (0 inside the window).

## Summary per model

| Model | In-domain rows | Median d in domain | Out-of-domain rows | Median d out of domain |
|---|---|---|---|---|
| Z6_a015 (0.15 sqrt(B/ρ)) | 15 | 0.080 | 11 | 0.084 |
| Z6_a014_sim (0.14, simulation fit) | 15 | 0.088 | 11 | 0.040 |
| Z6_a015_C0 (0.15 C₀, Hugoniot) | 15 | 0.053 | 11 | 0.080 |
| DW_size (Dowding power law) | 11 | 0.000 | 2 | 0.115 |
| Assadi2003_FE (process FE values) | 0 | — | 11 | 0.136 |
| baseline_LOMO (property-free median) | 15 | 0.249 | 11 | 0.150 |

The in-domain medians mix in-sample materials (Al, Cu, Ni, Zn for Z6; Al, Ti for DW_size) with held-out ones,
so only the hunch rows below speak to transfer.

## Hunch verdicts (by the frozen kill criteria)

| Hunch | Result | Verdict |
|---|---|---|
| CS-01: Z6 transfers to held-out pure metals | d: Ti 0.000 (H20-12), 0.000 and 0.023 (DW-07, DW-08); Sn 0.171; Ag 0.320; Au 0.437; median 0.097 | **Inconclusive** (median ≤ 0.10, but > 0.05 and three rows > 0.15) |
| CS-02: sound speed alone cannot rank the Al alloys | d: 6061 0.161, 2024 0.293, 7075 0.360 | **Supported** (all > 0.10; foreseeable from Table S1) |
| CS-03: Z6 beats the property-free baseline on held-out rows | median d 0.171 against 0.418 | **Supported** |
| CS-04: impact-mode ratio reproduces the 20 Hassani2020 regimes | 20 of 20 | **Passed** (in-sample consistency of the transcription) |
| CS-05: Dowding size law transfers to other Al/Ti batches | Ti H20-12: 0.000; Al H20-17: 0.090 | **Inconclusive** (none > 0.10, Al > 0.05) |
| CS-06: process FE values lie below single-impact windows | Below for every room-temperature Al row; but Cu 562.5 lies inside the Cu window 560–590 (H20-10), and Al 675 equals the lower bound of the heated-substrate row CH-01 | **Refuted** |

Judge-noise check: Z6_a015 and the baseline differ by more than the window width on **8 of 9** held-out rows.
The existing data can separate a property-based law from a constant. Whether they can separate one
property-based law from another (e.g. Z6 against a strength-dependent law) is not shown, because no
strength-dependent law was runnable.

## What this says

1. **Sound speed carries real signal** (CS-03, judge-noise check), and transfers well to Ti, but not to the
   soft, heavy metals Au, Ag and Sn. There Z6 lies above the windows (d 0.17–0.44), and it lies below for the Al
   alloys. Both failures point to a missing strength-like term, in opposite directions. This is an observation
   from retrospective data, not a tested claim; a hunch with a mechanism and kill criterion should precede any
   model built on it.
2. **The Hugoniot-C₀ variant scores better in domain** (median 0.053 against 0.080). It was a sensitivity
   variant, not a hunch, so this is a lead, not a result.
3. **The single-particle/process gap is not universal** (CS-06 refuted). For Cu, Assadi's FE process value
   (and their measured process value, 570 m/s) sits inside the LIPIT window. The ~40 % gap Panova2026b reports
   is for Al, Ni and Zn against other process sources. B6 in the questions note is therefore partly a
   source-by-source question, not a constant offset.
4. **The strength-dependent models could not be run.** Z1, Z2 and Z7 need tensile strength or failure strain
   for the impact-tested powders, which no source in hand provides. That is now the main gap for a fair
   comparison.

## Caveat found after scoring (2026-11-03)

The primary HG2019b gives Au 253 ± 7 and Ag 353 ± 2.5 m/s. The v1 scores used the Hassani2020 quotes (H20-14
Au 260–275, H20-15 Ag 340–365). For Au the primary window is lower, so Z6's over-prediction would be larger,
not smaller. The verdicts of CS-01 do not change (it stays inconclusive), but v1 is not rescored; a v2 would
use primaries where available.

## Next

- Source the tensile strength and failure strain of the Hassani2020 powders (ask the authors; check the
  primaries HG2018b and HG2019).
- Register a strength-term hunch only after naming its mechanism (assumption inventory H5), then test it on the
  blind set, not on these rows.
- Blind-campaign proposal: the disagreement map now has a concrete axis, soft/heavy metals and age-hardened
  alloys, where Z6 fails in opposite directions.
