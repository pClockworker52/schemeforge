# Research brief: cold spray, deposition efficiency and bonding (written 2026-11-03)

For a fresh session. Research only: no code, no new arena, no repository changes beyond the deliverables below. Read
docs/DECISIONS.md "2026-11-03 — Arena 2 paused; cold-spray question opened" first.

## Why this brief exists

Peter's application is multi-particle cold spray with coating buildup, and specifically **deposition efficiency and
bonding**. The assessment of 2026-11-03 found that third-medium contact (Arena 2) does not address what limits
cold-spray modelling (extreme distortion, impact dynamics, bonding, material behaviour), so Arena 2 was paused. Before
anything is built, this brief asks whether and how schemeforge's method can serve the cold-spray question.

## Peter's positions (take them as the starting point; challenge them with evidence, not opinion)

1. Current cold-spray models of deposition efficiency and bonding are not satisfactory: they answer few of the
   questions the domain actually has.
2. Much existing data was obtained with the wrong mindset (bulk outcomes without mechanistic information), so it may not
   discriminate between bonding mechanisms.
3. The goal is prediction for **new materials**, or **extended parameter ranges** for known ones: extrapolation.
4. A **mechanistic, multi-physics** perspective is likely necessary. (Counter-argument recorded in the session: fitted
   formulas win inside dense data; mechanistic models risk too many uncertain parameters. Compromise to examine: a
   mechanistic structure with few dimensionless groups, falsifiable on held-out materials.)
5. The model should **state for which materials it can predict**: its validity domain is part of the output, and a judge
   can check both the predictions inside the domain and the failures outside it.

## Questions

**Q1. What must a deposition-efficiency and bonding model answer?** Draft the list of domain questions (e.g. will this
powder/substrate pair bond at all, at what particle velocity and temperature, how does deposition efficiency depend on
the velocity and size distribution, which mechanism dominates: adiabatic shear instability, jetting, oxide-film
breakup, interfacial heating and diffusion), and mark which of them today's models answer, partly answer, or do not
answer. Peter corrects this list; it defines what "better" means.

**Q2. Which experiments carry mechanistic information, and are they usable as a judge?** Survey:
- single-particle impact experiments with in-situ observation (to be verified: laser-launched microparticle impacts
  from the group of C. Schuh, MIT, from about 2017, measuring critical bonding velocities particle by particle);
- bulk deposition-efficiency measurements against velocity, temperature, particle size, material;
- bond-strength and adhesion tests, cross-section and interface analyses, oxide characterisation.
For each source: what is measured, for which materials and ranges, how many data points, uncertainty, public
availability and licence, and whether a held-out split by material is possible.

**Q3. What exists as the zoo?** The existing models (to be verified from sources: critical-velocity correlations, e.g.
the line of work of Assadi and of Schmidt; adiabatic-shear-instability criteria from impact simulations; anything
newer), each with its inputs, assumptions, claimed validity range and reported accuracy.

**Q4. Can a mechanistic model be split into judgeable components?** schemeforge searches for a small component inside a
fixed harness, judged by a trusted reference (README "Where the method fits"). Identify candidate components (e.g. a
bonding criterion given local interface fields at impact; a deposition-efficiency map from the particle velocity
distribution and a critical velocity; a validity-domain predicate) and, for each, the reference it would be judged
against. Where no honest judge exists, say so.

## Method and rules

- **Every claim cites a source** (paper, dataset, DOI). Items marked "to be verified" above come from memory and must
  not be repeated as facts until checked. No invented formulas, values or datasets.
- Network: in the cloud session arxiv.org and en.wikipedia.org were blocked (DECISIONS 2026-11-03 context). Before
  starting, either allow the needed hosts in the environment settings (Network access → Allowed domains) or ask Peter
  for the PDFs, as he provided them for Arena 2.
- Time-box: one session. Breadth first (what exists), depth only where it decides the go/no-go.
- Never call a modelling idea novel; label sources and gaps.

## Deliverables

1. `docs/research/coldspray-questions.md`: Q1's list of domain questions and which models answer them (for Peter to
   correct).
2. `docs/research/coldspray-data-and-zoo.md`: Q2 and Q3 as tables with sources.
3. `docs/research/coldspray-go-nogo.md` (one page): the answer to Q4 and a recommendation:
   - **go: component arena** — at least one component with an honest judge on mechanistic data with a held-out split;
     sketch the slot, the judge, the zoo and the first target;
   - **go: discipline only** — no judgeable component yet, but schemeforge's process (hunches with kill criteria,
     pre-registration, held-out tests) structures the model development; propose what experiment or data would make a
     judge possible;
   - **no-go** — say why, and what would have to change.
4. One line in docs/STATUS.md and a DECISIONS entry only after Peter has read the go/no-go note.

## Not in scope

Building a model, writing a judge, running simulations, choosing a solver (Peter wants to stay tool-agnostic as long
as possible), resuming Arena 2.
