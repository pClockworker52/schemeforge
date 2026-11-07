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
| **C2. DE map**: DE from velocity and size distributions plus a bonding probability p(v/v_cr, d) | Bulk DE runs with **measured** per-run particle velocity and size distributions (Gilmore1999 Cu, Zhang2025 Al, Raletz2006) | Barely: the validated work found covers Cu and Al | **No.** The convolution is near-trivial. The unknown is the width of p (C3 in Q1), and no dataset constrains it across materials. HUGO-CS has DE with a particle velocity in 147 experiments from 32 articles, but only a single mean velocity, not marked as measured or computed, and a size spread in only 32 of them. |
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
   possible. No search runs on it. *v0.1 done 2026-11-03: [data/vcr_lipit.csv](data/vcr_lipit.csv), 41 rows,
   11 matched materials; conflicting secondary quotes flagged; primaries HG2018b and HG2019b still needed.*
2. **Pre-register** the zoo predictions (Z1, Z2, Z6, Z7, and a property-free baseline) for materials not yet
   measured. Each needs a hunch with mechanism, predicted value and kill criterion, as in the ledger.
3. Test against **blind measurements**. This is the judge that would make C1 honest: a LIPIT campaign on
   materials chosen after the predictions are frozen (e.g. alloys, refractory metals, dissimilar pairs off the
   current map). The Cornell, Tohoku or Sandia LIPIT systems are possible partners; the Schuh report counts 12+
   systems. Five to ten new materials would double the cross-material base.
4. For C2, the bridging experiment is a process run that measures per-particle velocity, size and bond
   outcome together, on powders also tested by LIPIT. Without it, B6 and C3 stay unanswerable.

## Local-first order, revision 2 (DECISIONS 2026-11-04 "Cold-spray plan revision: the interface law is the core")

**Why the order changed.** The original step 1 ended in "v_cr with setups frozen in advance". That is not
reachable as written. A simulated v_cr is always "simulation plus interface law", and no affordable simulation
resolves the interface (5–20 nm oxide against particle spacings of about 0.2 µm). OpenCourant made this explicit:
two SPH bodies are welded by the kernel; bricks with `/INTER/TYPE7` never weld (opencourant-verification.md §9.8).
The evidence so far points the same way:
- strength alone was refuted on B10 (CS-08);
- the oxide term carries most of CS-10's excess over Z6, in-sample;
- oxide-free Au and lightly oxidised Ag lie below Z6.

So the core of the single-impact problem is the **interface law**: oxide fracture, fresh-metal contact, bond or
separation. It is a closure the simulation needs, not something the simulation can supply.

**Order:**
1. **Interface bracket, CS-11** ([coldspray-hunch-cs11.md](coldspray-hunch-cs11.md)): welded against frictionless
   interface for simulated jetting onset, after the prerequisite rungs F0 and W0. It decides whether the simulation
   path needs an interface law at all, and how large the law's effect is compared with measured oxide effects.
2. **Interface-law hunches.** At most one or two parameters each, mechanism first, registered with a kill
   criterion against oxide-series data the law has not seen. First candidate: an oxide interphase of SPH particles
   (option C of §9.8), after a check of how OpenCourant handles SPH material failure (the no-erosion rule
   applies). A simulated v_cr is quoted only with a stated interface law, or with both bracket bounds.
3. **Closed-form track in parallel.** CS-07 and CS-10 are scored on every blind paper. CS-10's γ term is a
   closed-form interface law, so closed form and simulation should agree on the oxide effect. That agreement is
   itself a test.
4. **Blind papers ordered by oxide content.** B14 (Al oxide/hydroxide; partly exposed), B06 (oxide fracture), and
   B05 (impurities) if they carry thickness values come first. The others follow as before
   ([coldspray-blind-literature.md](coldspray-blind-literature.md)).
5. **External campaign: only for registered predictions that disagree** (trigger revised 2026-11-05, DECISIONS
   "Campaign trigger"). A campaign is not used to collect data from which a model is then formulated. It is the
   lab's half of theory-first work: the measurement that decides between hunches that are already frozen.
   - **Trigger:** once the pending oxide papers (B14, B06, B05) are scored, if CS-12's test T3 (v_cr against oxide
     thickness at a fixed oxide type) is still undecided for lack of an unseen series, a measurement request goes
     out. It asks for exactly that series, with the frozen CS-10 and CS-12 predictions attached.
   - **Who:** one of the LIPIT groups, as a request for a specific measurement, not a proposal for a programme
     ([coldspray-campaign-proposal.md](coldspray-campaign-proposal.md) item 2 is the template: Cu at three oxygen
     levels; Al at three thicknesses of one oxide type works equally well).
   - **Later requests** follow the same rule: each names the frozen hunches it decides between and their predicted
     values.
   - **Exception:** direct observations of interface states (where the oxide breaks, how far it stretches, what
     stays in the contact) may be asked for to formulate an interface law. They come first from published FIB and
     TEM work.
6. **Multi-particle build-up and deposition efficiency** come after the single-impact interface law. The law
   carries over to them; the second-impact assumption (H2) adds its own problem.

Unchanged: the blind rules B1–B6, pre-registration, the verification ladder before any simulated number, no
erosion as a production method, no OpenCourant fork, local first.

**The guard this revision needs.** One seen oxide series (B10) and one partly exposed series (B14) cannot judge an
interface law with parameters. Fitting it to them would be the trap this note warns about: fitting a handful of
numbers. Hence the limit of one or two parameters, the unseen-series rule, and the campaign trigger in step 5.

*Revision 1 (DECISIONS 2026-11-03, superseded in order, not in method):* simulation pipeline (verification ladder,
mesh convergence at the jet, v_cr with frozen setups) → model hunches → frozen predictions and the literature-blind
set → external campaign only if local evidence cannot decide.

## Steering hunches beyond the zoo

The zoo is the bar to beat, not the source of new ideas. Nothing guarantees creativity. The process can make
exploration explicit and measurable, so that a round shows whether it explored or only rephrased.

**Assumption inventory.** Most zoo members (Z1–Z14) share these assumptions. Each hunch must name the one it
breaks; the ledger records it.

| # | Shared assumption | Evidence against or around it |
|---|---|---|
| H1 | Bonding is a single velocity threshold (binary) | Bond strength peaks near 1.3 v_cr and then falls [Tang2025 A]; threshold "not as sharp" on growth surfaces [Panova2026b F] |
| H2 | The target is a fresh, polished substrate; impact history does not matter | Particle-on-particle v_cr ~1.3× [Panova2026b F]; bonded fraction ≤ 18 % [Panova2026a A]; build-up v_cr above single-bond v_cr [Reiser2024 F]. This is the multi-particle build-up regime of Peter's application. **Post hoc (B02, scored 2026-11-07, coldspray-results-b02-b14.md):** the same Cu powder bonds at 566 m/s on a cold-rolled full-hard Cu plate and at 641 m/s on an annealed plate; the substrate's state matters, but not through its hardness (CS-16 refuted; CS-17 registered for unseen data) |
| H3 | Heating softens the material (temperature terms in Z1, Z2, Z6) | Titles only, not read: "Metals strengthen with increasing temperature at extreme strain rates" [Dowding2024 M]; "Pure metals thermally harden while alloys thermally soften" [Dowding2026 M]. If confirmed, the temperature terms may have the wrong sign for pure metals |
| H4 | Oxide enters as a thickness at most | Hydroxide chemistry and structure shift v_cr [Lienhard2020 S]; oxide form sets local bond strength [Tang2024 S]. **Post hoc (B14, scored 2026-11-07, exposed):** dehydrating the RH-95 powder (OH bands and crystallinity removed, thickness less than 1 nm smaller) lowered v_cr by 68.5 m/s (1.6 window widths): oxide chemistry or structure matters beyond thickness, which thickness-only terms (CS-10, Z18) cannot carry |
| H5 | Bulk handbook properties describe the powder | Microstructure and cold work change bonding [Lucas2025 M, Panova2026b F]; quasi-static properties are the "main inaccuracy" [Vlcek2003 F] |
| H6 | Solid-state only; melting is an upper limit | Restricted nanoscale melting can bond [Khan2026 A] |
| H7 | Normal impact, one particle at a time | Oblique-impact model [Schuh2026 F lists Liu2024]; particle–particle interaction during build-up [Reiser2024 F] |
| H8 | A solver's contact or coupling option can represent the particle–substrate interface (method assumption; added 2026-11-05) | CS-11 (opencourant-verification.md §10): SPH–SPH kernel coupling has no defined contact at reachable spacings (W0 fails); TYPE7 on bricks never bonds and its edge bricks collapse earlier with refinement. Neither bound of the bracket is computable in OpenCourant |

**Lenses from neighbouring fields**, each an explicit input to a hunch round (hunch-generator `lens`):
explosive welding (weldability windows), ultrasonic and wire bonding, cold welding and tribology, adhesion and
contact mechanics, shock physics and spall, rapid solidification and brazing kinetics, and the dynamics of
impact cratering. In Arena 1, agents produced ideas the main session had not, but they drift back to familiar
literature unless the lens forces them away.

**Disagreement map: put the creativity into the experiment.** With 16 measured windows 2–25 % wide, a new
mechanism and a curve fit can score alike. So, before any blind campaign (step 3 above):
1. Evaluate the zoo and the registered hunches over candidate materials and conditions.
2. Rank the conditions by how far the predictions spread, relative to the expected measurement window.
3. Measure where they spread most.

A hunch that wins there wins by evidence. Candidate regions visible now: the Al-alloy series (790–1290 m/s,
Hassani2020), heated targets for pure metals against alloys (H3), and second-layer impacts (H2).

**Guards.** Hunches are pre-registered with a mechanism, predicted value and kill criterion. Negative results go
in the ledger. Breakers attack the leaders. Only the referee assigns "plausibly new", after a literature check.

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

## Upgrade trigger for the interface component (added 2026-11-04, revision 2)

The component is an interface law inside a fixed, verified simulation harness, or its closed-form counterpart
(CS-10's oxide term). Its reference is measured v_cr across oxide states, which is a measurement. That answers the
objection to C4 above, where the reference would have been a model. All three must hold:
- **Oxide series:** at least two held-out series on different metals, each with at least three states, numeric
  oxide thickness, and windows wider apart than their brackets.
- **Harness:** the simulation passes its verification ladder, including the interface rungs (F0, W0 of CS-11).
- **Resolving power:** the CS-11 bracket width is reported against the measured oxide effects, so that the judge's
  resolving power is known.

Even then, each evaluation is a simulation sweep of hours to days. A swarm search stays out of reach;
hand-registered hunches are the expected mode.

## Open checks before Peter decides

- Done 2026-11-03: Assadi2003, Vlcek2003 and Dykhuizen1998 read in full (PDFs from Peter). Assadi's Eq. 3 is
  a linearisation around Cu, limited by its authors to small changes, and its process v_cr values are inferred
  through CFD rather than measured. This confirms that Z1 is not an extrapolating model and changes nothing
  in the recommendation.
- Still needed: Schmidt2006 and Assadi2011 in full (Z2 coefficients F₁, F₂; the η-map). They are S-level here.
- Done: Hassani2020 Table 1 transcribed (16 numeric windows, 11 matched materials, 2 % velocity uncertainty,
  window widths 2–25 % of v_cr). Against the upgrade trigger: 11 matched materials (< ~15 required), so the
  recommendation stands. The Al-alloy rows (790–1290 m/s at similar ρ and B) are the subset that can separate
  Z6 from strength-dependent laws. Running that comparison is a pre-registered hunch, not an estimate here.
- Done: Schmidt2006 read. F₁ = 1.2, F₂ = 0.3, calibrated on 6 materials (Al, Ti, Sn, 316L, Cu, Ta) at 25 µm
  using process v_cr. Held out for Z2 within Hassani2020: Ni, Zn, Au, Ag and the three Al alloys. Z2's
  temperature term assumes thermal softening (Johnson–Cook), which is assumption H3.
  Assadi2011 (η-maps) is process-side and optional.
- Done: HUGO-CS coverage counted (see data note). It cannot judge C2 (no velocity distributions) or C1
  (critical velocities mostly computed with Schmidt's formula; 5 marked as measured).
