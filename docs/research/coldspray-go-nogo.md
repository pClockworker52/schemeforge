# Cold spray: go / no-go for schemeforge (Q4)

One page, 2026-11-03. Evidence: [coldspray-data-and-zoo.md](coldspray-data-and-zoo.md),
[coldspray-questions.md](coldspray-questions.md). For Peter to read before any STATUS or DECISIONS entry.

## Recommendation: **go: discipline only**, with a defined upgrade path to a component arena

schemeforge needs a trusted reference that is exact or provably reliable (README "Where the method fits"). For
cold-spray bonding the best references available today are measured, not exact. They are mechanistic, and a
held-out split by material is possible in principle, but they are too few and too narrow to discriminate
between candidates found by a search. A swarm searching on them would be fitting about 20 numbers.

## Candidate components and their judges

| Component (pure function in a fixed harness) | Reference it would be judged against | Held-out by material? | Honest judge today? |
|---|---|---|---|
| **C1. Single-impact v_cr(particle, substrate, d, T)** from material properties | LIPIT v_cr: ~8 matched metals; 20 particle/substrate combinations in Hassani2020; size series (Al, Ti), substrate-temperature series (Al, Sn, Ti), oxide series (Al), growth surface (Cu) | Yes: leave-one-material-out | **Not yet.** n ≈ 20–40 values (my estimate from the studies listed), mostly one lab, extracted from figures, ±3–4 % per shot velocity. The zoo has a one-parameter law fitting within that noise (0.15·sqrt(B/ρ), Z6) and a two-parameter spall law (Z7). The judge cannot separate candidates any better than that, so a search would overfit. |
| **C2. DE map**: DE from velocity and size distributions plus a bonding probability p(v/v_cr, d) | Bulk DE runs with **measured** per-run particle velocity and size distributions (Gilmore1999 Cu, Zhang2025 Al, Raletz2006) | Barely: the validated work found covers Cu and Al | **No.** The convolution is near-trivial. The unknown is the width of p (C3 in Q1), and no dataset constrains it across materials. HUGO-CS may hold the DE values, but whether it records particle velocity is unchecked. |
| **C3. Validity-domain predicate**: does the v_cr model apply (regime: rebound / bond / erosion-melt; splat / co-deform / penetrate)? | LIPIT regime observations (Hassani2020 map, melting and erosion studies); zoo baseline: Vlcek2003's qualitative eligibility ranking (Z17) | Partly | **Not alone**: the labels are few and coupled to C1. Peter's position 5 is best realised as part of C1's output, scored on both in-domain error and declared-out-of-domain failures. |
| **C4. Bond criterion from local interface fields at impact** (pressure, strain, temperature, oxide state → bonded or not) | Would need fields from simulations, but simulation interpretation is exactly what the ASI-against-jetting dispute is about | — | **No.** The reference would be a model, not a measurement. |
| **C5. Bond strength or bonded fraction against velocity** | Tang2024/2025 (Al), Panova FIB tomography (Cu) | No: one material each | **No.** |

## Why not no-go

The process discipline transfers directly, and the literature already contains the mechanistic structure Peter
proposes: v_cr/C₀, T*, d/d₀, an impact-mode ratio and a spall group (Z6–Z9). The questions where
pre-registration and held-out tests add most are untested: B6 (single-particle to process), C3 (threshold width)
and E1 (new materials). The data situation is fixable by specific experiments. It is not a matter of missing
physics.

## What "discipline only" means in practice

1. Build an **open v_cr table** from the LIPIT literature (C1's inputs and outputs, uncertainty brackets,
   source figure for each row). Ask the Schuh, Hassani and Ichikawa groups for the raw restitution data where
   possible. No search runs on it.
2. **Pre-register** the zoo predictions (Z1, Z2, Z6, Z7, and a property-free baseline) for materials not yet
   measured. Each needs a hunch with mechanism, predicted value and kill criterion, as in the ledger.
3. Test against **blind measurements**. This is the judge that would make C1 honest: a LIPIT campaign on
   materials chosen after the predictions are frozen (e.g. alloys, refractory metals, dissimilar pairs off the
   current map). The Cornell, Tohoku or Sandia LIPIT systems are possible partners; the Schuh report counts 12+
   systems. Five to ten new materials would double the cross-material base.
4. For C2, the bridging experiment is a process run that measures per-particle velocity, size and bond
   outcome together, on powders also tested by LIPIT. Without it, B6 and C3 stay unanswerable.

## Upgrade trigger to "go: component arena" (C1, later C1 + C3)

All three must hold:
- An open table of at least ~15 matched metals plus dissimilar pairs, each value with an uncertainty bracket.
- A held-out set frozen before measurement, owned by someone other than the searcher, as with the euler1d
  seed.
- A judge-noise check showing the reference separates the existing zoo members, i.e. Z6 and Z7 differ by more
  than the measurement brackets on the held-out set.

Then the slot would be `v_cr(props_p, props_s, d, T) -> (v_cr, in_domain)`. The judge scores the error on
in-domain held-out materials, plus a penalty for confident predictions on materials later found out of domain.
The zoo is Z1, Z2, Z6, Z7 and a constant baseline. The first target: beat Z6 on held-out materials while
declaring the domain.

## Open checks before Peter decides

- Done 2026-11-03: Assadi2003, Vlcek2003 and Dykhuizen1998 read in full (PDFs from Peter). Assadi's Eq. 3 is
  a linearisation around Cu, limited by its authors to small changes, and its process v_cr values are inferred
  through CFD rather than measured. This confirms that Z1 is not an extrapolating model and changes nothing
  in the recommendation.
- Still needed: Schmidt2006 and Assadi2011 in full (Z2 coefficients F₁, F₂; the η-map). They are S-level here.
- Confirm the Hassani2020 table of 20 combinations and its uncertainties (Elsevier; the accepted manuscript may
  be on OSTI or DSpace, but DSpace returned 429).
- Inspect the HUGO-CS files for particle velocity and DE coverage (raw.githubusercontent.com works; needs file
  names, or github.com allowed).
