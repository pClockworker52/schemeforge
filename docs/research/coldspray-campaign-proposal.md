# Proposal: a blind, pre-registered test of critical-velocity models with single-particle impacts

**Parked (DECISIONS 2026-11-03 "Cold-spray track: local first"): an external campaign is the last resort.**

Draft v0.1, 2026-11-03, for Peter to revise before sending. Intended reader: a group operating a laser-induced
particle impact test (LIPIT), e.g. Cornell (Hassani), Tohoku (Ichikawa), Sandia, or Northwestern/MIT (Schuh).
Background and evidence: [coldspray-go-nogo.md](coldspray-go-nogo.md), [coldspray-results-v1.md](coldspray-results-v1.md),
[data/README.md](data/README.md).

## 1. The question

Can a mechanistic model predict the critical adhesion velocity v_cr of a material it was not calibrated on,
and can it say when it cannot? Published critical-velocity models (Assadi 2003, Schmidt 2006, the
sound-speed law of Hassani-Gangaraj 2018, spall-based variants) have been compared mostly on the materials
they were fitted to. We have found no test on materials measured after the predictions were fixed.

## 2. What we have done so far

- An open table of single-particle critical velocities from the literature: 44 rows, 11 matched materials,
  each with its source, window definition and caveats (`data/vcr_lipit.csv`).
- A matched property table built from Hassani et al. 2020, Table S1 (`data/properties.csv`).
- A pre-registered, explicitly retrospective test (predictions committed before scoring):
  - the sound-speed law beats a property-free baseline on held-out materials;
  - it fails in opposite directions for soft, heavy metals (Au, Ag, Sn: predicted too high) and for
    age-hardened Al alloys (predicted too low);
  - the strength-dependent models could not be run, because tensile strength and failure strain of the tested
    powders are not published.
- The existing windows are narrow enough to separate a property-based law from a constant (8 of 9 held-out
  rows), so a modest blind campaign can decide between models.

## 3. Proposed protocol (two stages, blinded by design)

**Stage 1, characterisation and sub-critical impacts (partner).** For each material:
- powder size distribution, oxygen content, temper or heat-treatment state, and, where possible, native oxide
  thickness and type;
- quasi-static strength and failure strain of the powder (e.g. micro-compression) or of the parent stock;
- ~20 impacts below the expected bonding range on a polished, matched substrate, to fit a dynamic yield
  strength as in Hassani et al. 2020 (Sun et al. 2020 method).

Only the stage-1 data are shared with us.

**Freeze (us).** Within an agreed period, we commit every model's prediction and domain claim (in or out of
its validity domain) for every stage-2 condition, publicly timestamped (git commit hash). No prediction
changes after this point.

**Stage 2, bonding window (partner).** ~20–30 further impacts per condition around the bonding transition,
same setup as stage 1. Raw per-impact data (diameter, impact velocity, rebound velocity) are released, with
the window defined as in Hassani et al. 2020 (smallest range with equal numbers bonded and rebounded).

**Scoring (us, rules frozen in advance).** Distance of each prediction outside the measured window, divided by
the window midpoint, reported separately for in-domain and out-of-domain predictions. Every model is reported,
including the ones that fail.

The held-out data stay with the partner until predictions are frozen. Nobody on the modelling side can see or
tune against them.

## 4. Proposed materials (5–8 conditions, each chosen to separate models)

| # | Condition | Separates | Why |
|---|---|---|---|
| 1 | One Al alloy in two tempers (e.g. 6061-O and 6061-T6) | sound-speed law vs strength-dependent laws | Same density and sound speed, different strength: the cleanest strength test. The published Al grades span 790–1290 m/s at nearly equal C₀ |
| 2 | Cu powders at three controlled oxygen levels | oxide-removal hunch (CS-07) | Process data compiled by Hassani-Gangaraj et al. 2019 suggest a large drop below ~2–3 nm oxide; no single-particle oxide series exists except Lienhard 2020 for Al |
| 3 | A noble metal other than Au (e.g. Pt or Pd; oxide state to be verified) | oxide-removal hunch; sound-speed law for soft, heavy metals | Tests whether the Au/Ag shortfall is oxide or something else |
| 4 | Ta and 316L | single-particle vs process critical velocity | Both are in Schmidt 2006's process calibration set, so this links single-impact and spray values for the same materials |
| 5 | Ti-6Al-4V | transfer to an engineering alloy | Pure Ti is predicted well by the sound-speed law; does that transfer to its main alloy? |
| 6 (optional) | Cu on a sprayed Cu growth surface, after Panova et al. 2026 | coating build-up | The regime that governs multi-particle deposition |
| 7 (optional) | One pure metal and one alloy on a heated stage | sign of the temperature effect | Dowding & Schuh (2024, 2026) report thermal hardening of pure metals at extreme rates; the classic laws assume softening |

Conditions 1–5 bring the open table to at least 15 matched materials, the threshold we set for treating the
problem as a judged benchmark.

## 5. What the partner gets

- A pre-registered model comparison on their data, co-authored.
- All analysis code and tables, open (GPL-3.0-or-later; data under CC-BY if the partner agrees).
- A dataset designed to be reused as an open benchmark, with their group as its source.

## 6. What we ask

- Stages 1 and 2 for the agreed conditions (estimated 40–50 impacts per condition, comparable to
  Panova et al. 2026: N = 39–48).
- Release of raw per-impact data after the freeze.
- Optionally: raw restitution data for already published materials, to replace values we currently read from
  figures.

## 7. Open points for Peter before sending

- Which group to approach first, and whether to offer co-authorship up front.
- Whether to fund or share consumables (powders with controlled oxygen content and tempers).
- Whether to include the optional conditions 6 and 7, which are closest to the application but add effort.
- Who on our side freezes and holds the predictions (the upgrade trigger asks for someone other than the
  searcher to own the held-out set; here the partner holds the data, so this is met).
