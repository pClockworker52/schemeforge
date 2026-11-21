# Slip check: why do 30× bonds hold and 3× / 10× bonds tear? (spec and prediction, frozen)

Frozen 2026-11-22 (Peter: "Freeze"), as drafted in 1237591, before any slip number was read.

Written 2026-11-22 (cloud, modeller) at Peter's request. `kind = check`; no hunch, no budget.

## Why

CS-22b is supported at δ_c 30× (opencourant-verification.md §31, DECISIONS 2026-11-22). **Its verdict stands
whatever this check finds:** its frozen rule (coldspray-hunch-cs22b.md, c8a6c5c) does not use slip.

Before building on that result (a confirmatory test, or part 2, the bistable band in V), it matters which mechanism
decides whether a bond tears or holds:
- **Slip decides (a property of this bond law).** A bonded pair carries no cohesive traction while compressed
  (g ≤ 0). Its tangential opening δ_t keeps accumulating and counts in δ = √(g² + |δ_t|²) once the pair reopens
  (§35; problem-formalism.md §2(g)). Then the tear/hold threshold is roughly "slip ≈ δ_c", and part 2 would measure
  that rather than the impact.
- **Normal opening decides (bond behaviour).** Bonds tear because the pair pulls apart, with little tangential
  opening, and further work can build on this law.

## Facts checked (coldspray-procedure.md)

solver-facts.md §3 and §4 (cs12 activation, no traction while g ≤ 0, δ_t accumulation, candidate-list release at
r > 2.51 s, the lost-bond check as a lower bound). **Not covered:** the interface-file field `slip` has never been
read. Its meaning is Q1 and is settled first.

## Q1: source (reading only)

With file and line references in the fork (engine `27e53d5f0`):
1. What is `slip` in the interface file: per facet or per particle, accumulated over what (all contact or bonded
   only), and how it relates to a bonded pair's δ_t?
2. Can per-pair δ_t, g and D at each record be read from the existing CS-22b output (interface file v6, any other
   file)?
3. If neither δ_t nor a proxy whose relation to δ_t is stated in Q1 can be read from existing files: stop and report
   "not determinable without a new output". A rerun with more output is decided later, not here.

## Q2: data (existing files only; no run, no build)

CS-22b on-runs: 3× and 10× at R/8 and R/16; 30× at R/8, R/16 and R/32 (engine `27e53d5f0`, §31).
- For every bond that tears (D reaches 1): δ_t at the last record before D = 1, divided by δ_c (or the Q1 proxy).
- For every bond that holds to t_end: δ_t / δ_c at t_end.
- Per run: the count, median, 10th and 90th percentile of δ_t / δ_c, for torn and held bonds separately; the record
  interval (time resolution); the unit of analysis (pair, facet or particle, as Q1 allows).

## Rule (fixed now)

Pooled over all torn bonds of all runs (also reported per run):
- **slip decides** if at least 80 % of torn bonds have δ_t ≥ δ_c before tearing;
- **opening decides** if at least 80 % have δ_t ≤ 0.2 δ_c;
- **mixed** otherwise;
- **not determinable** if Q1 stops.

Held bonds (30× at R/16 and R/32) are reported, not judged.

## Prediction (judgment, before any number)

slip decides 0.40; mixed 0.35; opening decides 0.25.

## What follows (stated now; Peter decides after the result)

- **slip decides:** change the bond law to stick under compression before a confirmatory test or part 2.
- **opening decides:** a confirmatory test or part 2 can go ahead on this law.
- **mixed:** report and decide.
- **not determinable:** decide whether a rerun with pair-level output is worth it.
