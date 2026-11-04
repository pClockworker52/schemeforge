# Cold spray: hunch CS-12 (bonding as local dissolution of the interface blanket), registration draft

Drafted 2026-11-04. Idea: Peter (the interface as a Markov blanket). Criterion: cold pressure welding by surface
expansion (Bay; from memory, not read in this track). **Status: draft.** It is frozen when Peter approves it, and
no test below is run or read before that commit. Research track, not a ledger arena. Background: CS-11 outcome
(opencourant-verification.md §10.6) and plan revision 2 (coldspray-go-nogo.md).

## The picture

- **Before impact,** the particle and the substrate are two systems. The interface is their **Markov blanket** in
  Pearl's sense: the bulk of each body influences the other, and the bonding outcome, only through a small set of
  interface states.
- **A metallurgical bond is the local dissolution of that blanket:** lattice continuity, so that the two bodies
  become one there. Rebound means the blanket survived everywhere.
- **This diagnoses both CS-11 setups.** The kernel weld (W) has no blanket from the first touch. The TYPE7 contact
  (F) has a blanket that can never dissolve. Neither can represent the transition, which is the phenomenon itself.
- **Physically,** the blanket is the native oxide plus the contact gap. It dissolves where the oxide has cracked
  and fresh metal has been pressed through the cracks into contact.

Only the graphical-model meaning is used. The free-energy and active-inference readings of "Markov blanket" make no
prediction here that this one does not, and are not part of the hunch.

## Hunch

```yaml
- id: CS-12
  registered: draft 2026-11-04 (frozen on Peter's approval)
  assumption_broken: >-
    H1 (bonding is a single particle-level velocity threshold): here bonding is a local, area-wise state change of
    the interface. Also the method assumption raised by CS-11 (proposed H8: a solver contact or coupling option
    can represent the interface).
  statement: >-
    (a) Blanket: given the history of the interface states s(r, t) = {normal pressure p_n, surface expansion Y,
    slip, temperature T, oxide type}, the bonding outcome is independent of the bulk fields.
    (b) Dissolution criterion C (cold pressure welding): an interface point bonds if and only if its surface
    expansion Y = (A - A0) / A exceeds a threshold Y', and the normal pressure acting while Y > Y' exceeds an
    extrusion pressure p_E = m * sigma_flow. The bonded share of that point's area is (Y - Y') / (1 - Y').
    (c) Minimal variant: Y' depends on the oxide type (chemistry and structure), not on its thickness, as long as
    the layer is continuous. m is universal.
  mechanism: >-
    A brittle native oxide cannot follow the stretch of the metal beneath it. Beyond a critical expansion it breaks
    into fragments, and fresh metal is extruded through the gaps when the contact pressure exceeds the flow-stress
    level needed to push it through. Where fresh metal meets fresh metal under pressure, the blanket dissolves. The
    stretch and the pressure are kinematic and mechanical states at the boundary, so the oxide never has to be
    resolved. Jetting matters through what it does to Y and p_n at the edge, not as a criterion of its own.
  parameters: "Y' (per oxide type) and m (universal); 2 for one oxide type. Fitting rule registered later (see T2)."
  predicted_effect:
    - {metric: "T1: bonded-area pattern on sectioned or lifted-off splats near v_cr", direction: "ring",
       size: "bonded annulus with an unbonded centre; the unbonded centre shrinks as V rises above v_cr"}
    - {metric: "T3: v_cr across an oxide-thickness series of one oxide type (same powder otherwise)",
       direction: same, size: "max - min <= w"}
    - {metric: "T4: v_cr across oxide types (e.g. oxide vs hydroxide)", direction: "any",
       size: "not predicted (Y' changes); reported"}
  kill_criterion: >-
    T3 (simulation-free, the decisive test available now): on an unseen series of at least three states of one
    oxide type, spanning at least 5 nm of thickness, with w the median window width (rule B6 where not printed):
    refuted if v_cr is monotone in thickness and max - min > 2 w; supported if max - min <= w; inconclusive
    otherwise. T1: refuted if bonded-area maps on unseen material at or just above v_cr show bonding concentrated
    at the centre with an unbonded rim. T2 (after a bulk solver survives the contact, see CS-13): the frozen
    criterion with Y', m fitted once must predict v_cr on unseen oxide series within the S1 rule; kill rule to be
    registered with the fitting rule, before any T2 run.
  known_relatives:
    - Bay (cold pressure welding, surface-expansion threshold and extrusion; from memory, not read)
    - cold-spray papers relating bonding to interfacial stretch or oxide break-up (likely exist; not checked)
    - cohesive-zone interface models with internal variables (the formal structure)
    - Ichikawa2015/2019 (oxide left at the crater centre), Panova2026a (bonded fraction <= 18 %)
    - HG2019b (oxide removal), CS-07, CS-10 (thickness enters; CS-12 minimal says it does not)
  provenance: Peter's Markov-blanket idea after CS-11 (2026-11-04); criterion C from the cold-welding lens.
  label: none yet (referee); expected at most "variant of Bay applied to cold spray"
  status: draft
  author: Peter (idea), claude (formulation)
```

## Why T3 matters: CS-12 and CS-10 disagree

| Hunch | Oxide thickness at fixed oxide type | Al 6061 at 15 µm, 17 → 25 nm |
|---|---|---|
| CS-10 (frozen γ) | raises v_cr through t_ox/d | about +37 m/s |
| CS-12 minimal | no effect while the layer is continuous | 0 within w |

This is the disagreement map of the go/no-go note in miniature: a same-type thickness series decides between them.
Known exposures, which carry no verdict:
- **B10** (seen; thickness and strength co-vary) has a spread of 77 m/s and Δ = −30.5 m/s. That is compatible
  with either hunch.
- **HG2019b** reports large drops in Cu process v_cr below 2–3 nm oxide. CS-12 minimal reads this as the layer no
  longer being continuous. That reading is post hoc, and process data are outside the domain.
- **Lienhard2020** (+14 % for hydroxide) is a change of oxide type, so it falls under T4: no verdict.

**If T3 refutes the minimal variant,** a thickness-dependent Y' is a new hunch with its own registration, not a
rescue of CS-12.

## What the blanket view asks for (data, not verdicts)

- **Bonded-area and oxide-residue maps** (FIB sections, lift-off scans, TEM of interfaces) observe where the blanket
  dissolved. They are judge data besides v_cr. B06 (oxide fracture mechanisms) is the first blind paper to look at
  after its freeze.
- **Interface-state histories** (Y, p_n at each interface point) are needed for T2 and for the conditional-
  independence test (a). Both need a bulk solver that survives the contact. Today F collapses at 0.07–0.17 D/V
  (§10.5). This is why CS-12's simulation part depends on CS-13.

## What CS-12 cannot show

- (a), the conditional independence, is the principle. It is tested only through (b) and (c) until interface
  states can be computed.
- Y' for a given oxide type must be fitted. Without simulation, CS-12 predicts patterns and the absence of a
  thickness effect, not v_cr values.
- The minimal variant ignores temperature in the criterion. Temperature enters only through σ_flow.
