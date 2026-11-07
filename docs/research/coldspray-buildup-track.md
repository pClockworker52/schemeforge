# Cold spray: build-up track (opened 2026-11-07)

Opened on Peter's decision (DECISIONS 2026-11-07 "Build-up track opened"). Same discipline as the single-impact
track. **It opens with questions and a data audit, not with hunches.** Peter's application is multi-particle build-up;
the single-impact track stays open in parallel, mostly waiting for data.

## Why now

The single-impact track waits for unseen oxide data (pending blind papers, possibly the T3 measurement request).
Build-up has seen literature of its own, and one sharp contradiction already sits in the seen data (below).

## What is already known (seen sources only; evidence levels as in coldspray-data-and-zoo.md)

| Source | What it shows | Level |
|---|---|---|
| Panova2026b | Cu, 19 µm: polished plate 567 m/s; polished cold-sprayed Cu (harder) 653 m/s; rough cold-sprayed Cu about 727 m/s; hardness and roughness each +10–15 %, together about +30 % | F |
| Panova2026a | Two-particle stacks, Cu: bonded fraction at the particle–particle interface ≤ 18 % | A |
| Reiser2024 | Au stacks of more than 20 particles, each impact's size and velocity recorded; build-up needs a higher critical velocity than single bonding (single v_cr 253 ± 7 m/s) | F |
| Process side | process v_cr is lower than single-impact v_cr (Panova2026b attributes it to heating); DE curves (Alkimov1990, Gilmore1999) integrate over distributions and cannot separate mechanisms | S / F |
| B02 (scored) | cold-rolled wrought Cu substrate: v_cr **lower** than on annealed Cu (566 against 641 m/s) | blind, scored |

## The first sharp question

**A growing coating is a heavily cold-worked surface, yet it raises v_cr** (Panova2026b: 653 against 567 m/s). A
heavily cold-worked **wrought** plate lowers it (B02: 566 against 641 m/s). Cold work alone cannot explain both.
Whatever distinguishes a deposit from a cold-worked plate decides how build-up continues once the first layer is
down. Candidates:
- prior-particle boundaries with oxide;
- roughness at the scale of the particle;
- porosity;
- ultrafine grains;
- a second oxide (the deposit's own surface).

## Questions (not hunches)

1. What makes a deposit surface different from a wrought surface of the same metal and hardness, for the next
   particle?
2. Does the 1.3× particle-on-particle factor (Panova2026b, Reiser2024 for Au) hold across metals, or does it scale
   with something measurable (oxide, roughness, hardness)?
3. How does single-particle v_cr map onto a process deposition-efficiency curve (velocity and size distributions,
   particle heating)? This is C2/C3 of the go/no-go note.
4. What does the bonded fraction (≤ 18 % in stacks) mean for coating strength and porosity?

## First steps

1. **Data audit:** for each build-up source (seen, and anything new found under the blind rules), record what is
   measured, in which variables, and with what uncertainty. Output: a table in this file.
2. **Choose one question** that the audited data can actually answer, before any hunch is registered.
3. **Hunches only after that,** under the hunch budget if Peter adopts it (HANDOFF, Open for Peter).

## Data audit (2026-11-07, cloud)

Seen sources only. No paper of the blind list (coldspray-blind-literature.md) or the proposed blind list 2
(Tiamiyu 2022; Panova & Schuh 2024 ×2) was opened. Reiser2024 was re-read in full for this audit (arXiv:2404.05601v1,
the only version, read 2026-11-07); the other rows rest on earlier full-text reads, as recorded in
coldspray-data-and-zoo.md, unless stated.

### Audit table

| Source | Level | Material, set-up | What is measured (variables) | n | Uncertainty as printed | Outcome variable for build-up | Usable for |
|---|---|---|---|---|---|---|---|
| **Reiser2024** | F | Au powder, 9–22 µm (99.9 %, 200 mesh); targets Si wafers with 100 nm sputtered or 3 µm electroplated Au; LIPIT, same spot, minutes between shots (isothermal) | per shot: diameter (before launch), impact velocity, rebound if inside the camera window; per stack: survival or fracture (optical, after each shot), shot number of each fracture; cross-sections: flaw length, three microstructure classes, splat height | 9 stacks in the figures: 4 intact (Fig. 3; 14–24 shots), 5 fractured (Fig. 5; 7–15 shots; 7 fracture events). Flaw regression N = 67 (3 stacks); microstructure N = 47 (2 stacks) | velocity ±5 % per shot; stack means ± s.d. printed | stack survival (binary); flaw length per height slice; recrystallized area fraction | stack survival against the impact history (per-shot data exist only as bar charts, to be digitized); flaw density against v/v_cr |
| **Panova2026b** | F | Cu, sieved 17–21 µm; polished H02 plate (98 HV), polished cold-sprayed Cu (142 HV), rough cold-sprayed Cu (Ra 8 µm, Rz 45 µm) | v_cr per surface (PA-01…03); surface hardness; roughness | 3 surfaces; 39–48 impacts each | window = mean of last 2 rebounds and first 2 bonds (563–571, 651–655, 717–737 m/s) | v_cr of a particle on a deposit-like surface | the deposit-vs-plate contrast (one powder, one metal); not the cause of it |
| **Panova2026a** | A (abstract; full text not opened) | Cu, two-particle stacks around the optimal velocity | bonded fraction of the particle–particle interface (FIB tomography) | not known from the abstract | not known | bonded fraction | nothing quantitative until the full text is read |
| **B02** (Lucas thesis ch. 4, blind, scored) | blind F | Cu powder on annealed and cold-rolled full-hard wrought Cu | v_cr per substrate | 2 substrates | coldspray-results-b02-b14.md | v_cr on a cold-worked, non-deposit surface | the other side of the deposit-vs-plate contrast |
| **Gilmore1999** | S (via Dowding2020) | Cu, ~19 µm (11–26 µm), process | DE against mean particle velocity | a few points (53 % at 640, 95 % at 725 m/s) | not seen | DE | nothing mechanistic: integrates size, velocity, temperature and erosion |
| **Alkimov1990** | S (figure via Hall2015) | Cu, Ni, Al, process | DE against particle velocity | S-curves | not seen | DE | as Gilmore1999 |
| **HUGO-CS** | F (data file) | 147 runs with DE and one particle velocity, 32 with a size spread | DE, one mean velocity (measured or computed not recorded) | 147 | 16 % of DE values carry one | DE | not a test of any build-up mechanism (no distributions) |

### What the audit changes

1. **Reiser's "build-up critical velocity" is not a particle-on-particle bonding velocity.** It is the stack-mean
   velocity above which a free-standing stack survived (about ≥ 330 m/s). Particles did bond on the stack near
   the single-impact v_cr: the slowest bonded particle was 249 m/s at 20 µm, against v_cr = 253 ± 7 m/s at
   16 ± 4 µm (Reiser2024 §3). So Question 2 above ("the 1.3× particle-on-particle factor … Reiser2024 for Au")
   mixes two quantities. Only Panova2026b measures a particle-on-deposit v_cr, and only for Cu. **Question 2 cannot
   be answered with seen data:** one metal.
2. **The ≥ 330 m/s boundary is not sharp.** Printed stack means: intact 328 ± 45, 329 ± 56, 342 ± 20,
   354 ± 37 m/s; fractured 274 ± 31, 288 ± 33, 297 ± 43, 326 ± 28, 329 ± 68 m/s. Means of 326–329 m/s sit on both
   sides. The ranks separate the groups (my arithmetic, post hoc, on the printed means: Mann–Whitney U = 18.5 of
   20, exact one-sided p = 3/126 = 0.024 with n = 4 and 5), but the stack means overlap within their spreads.
   Confounds named by the authors: no lateral constraint (stacks are free-standing columns), possible organic
   contamination from the launch pad. Not named: fractured stacks stop early (7–15 shots), so their means come from
   the first shots only, while intact means include shots 12–24.
3. **The fracturing impacts look like ordinary shots.** Visual reading of Fig. 5b (300 dpi, not digitized): the
   7 shots marked as fracture events lie near their own stack's mean, and none is clearly below v_cr. Erosion here
   is not obviously caused by a slow, rebounding striker (grit blasting). It looks like a property of the stack
   built so far. **This is a reading, not a measurement.** It must be digitized before it supports anything, and
   any hunch drawn from it cannot be tested on Reiser2024.
4. **The deposit-vs-plate contrast** (Panova2026b against B02) has two data points per side and differs in
   several candidate variables at once (prior-particle boundaries, oxide, grain size, residual stress, surface
   preparation; the rough row also adds roughness). None of the five candidates in "The first sharp question"
   varies on its own in seen data. **Question 1 cannot be answered with seen data.**
5. **Questions 3 and 4 cannot be answered with seen data.** Question 3: no run with measured velocity and size
   distributions (go/no-go C2). Question 4: only the Au flaw-length regression, which is weak (R² = 0.06,
   p = 0.046, N = 67, with the sampling bias the authors name).

### Proposed question (step 2; awaiting Peter)

**Q-B1. In a growing deposit, is erosion set by the striking particle or by the deposit's history?** Concretely,
on Reiser2024's nine stacks: does fracture at shot k depend on (a) the velocity and size of shot k, or (b) the
impacts before it (mean v/v_cr of shots 1…k−1, stack height or aspect ratio at k)?

Why this one:
- **The seen data can answer it.** Per-shot diameter and velocity (±5 %) and the shot number of each fracture event
  are printed for all nine stacks (Figs. 3 and 5). That gives about 150 shots and 7 events, enough for a
  descriptive answer.
- **It bears on Peter's application.** It decides whether erosion during build-up can be modelled per impact (a
  per-particle removal law, the simple route to DE) or needs a state variable for the deposit (the bond quality of
  buried interfaces).
- **It is not a hunch.** Answering it is exploratory and post hoc. Any hunch it suggests must be tested on unseen
  stacks (a later multi-particle LIPIT paper, or a request).

What answering it takes: digitizing Figs. 3b and 5b (velocity bars, size bars, fracture arrows) into
`docs/research/data/buildup_reiser2024.csv`, with reading error stated, and a one-page analysis. Limits to state
up front: one metal (Au), free-standing stacks, 7 events, survivorship (fractured stacks stop early), and the
possible launch-pad contamination.

Not proposed: a question on the deposit-vs-plate contrast. It is the sharpest contradiction, but the seen data
cannot separate its candidates. It goes into the measurement request if the campaign trigger is met (one powder on
a deposit, an annealed deposit, and a cold-rolled plate of matched hardness).
