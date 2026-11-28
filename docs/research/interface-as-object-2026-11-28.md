# The contact as an object with a model of its partners (working note, 2026-11-28)

**Status: working note, not a hunch.** It is the brief for drafting the next hunch (working name **CS-25**) in a fresh
session (Peter, chat 2026-11-28: "Write it as a hunch. This will need a bit of reasoning and a fresh session.").
Everything below is the modeller's reasoning unless a source is named. Nothing here has been tested.

## 1. How this came about

1. **Peter's partner-aware contact idea** (fork `cs12` 210d98d4, note §1): a body should "see" its contact partner,
   not only the force.
2. **Two readings were tried and closed:**
   - kernel completion across a TLSPH contact (§43: both forms fail in the static model);
   - the substrate as a heat sink, CS-24. Refuted post hoc: none of the 4 resolved mismatched pairs followed the
     effusivity sign. Item B was supported post hoc, but at 2.6–5× the predicted size.
3. **The modeller's reasoning on the formalism** (chat 2026-11-28): in the continuum, momentum needs nothing beyond
   the traction. So a body gains nothing from more information about its partner. Partner information can only
   repair the discretisation, supply a closure for an unresolved two-body process, or compress information into a
   criterion.
4. **Peter's reframing** (chat 2026-11-28): "Perhaps it's not partner awareness that lacks, [but] the contact's
   awareness of its partners … perhaps it's the contact/interface that lacks a model of its partners."

## 2. What the contact is in the model today (problem-formalism.md §1)

- **Eq. 10:** a stateless penalty. It reads the current gap only.
- **Eq. 11:** frictionless.
- **Eq. 12 (cs12):** state D, δ_t and the frozen σ_B.
  - Activation reads pair minima of the partners' **point values at this instant**: Y, p_n and σ_flow.
  - The strength follows the local σ_flow(T).
  - The elastic part d₀ = σ_B s²/k shrinks with the mesh, since k ∝ s.

So the contact already reads both partners, but only instantaneously and pointwise.

**Missing:**
1. A length and thickness of its own.
2. A memory of what each partner has supplied to it.
3. Knowledge of where it sits in the patch and when the edge passed it.
4. A model of how its partners will respond.

## 3. Why the interface is the right home (against the formalism)

- **§2(a), the length.** The bulk has no length below R. Every small physical length in cold spray sits at the
  interface: oxide thickness, the jetted or mixed layer, roughness, a process zone. The length path (stopped
  2026-11-24) tried to put a length into the bulk (σ_y, T); the interface was never the carrier.
- **§2(c), the singularity.** The bond front's singularity belongs to a *sharp* interface. A finite-strength interface
  with its own length (a cohesive process zone) removes it in fracture mechanics. The mesh must then resolve the
  interface's length, not the singularity.
  - cs12 defeats this in three ways: its thresholds read singular point values, its strength follows the local
    σ_flow, and its elastic opening scales with the penalty.
- **The partners as feeds: the third body** (tribology: Godet 1984; Berthier's tribological circuit; from memory, not
  read). The interface layer is a body with its own rheology, fed and drained by both partners; in cold spray the
  jet is its sink.
  - Cross-link, not a claim: Arena 2's third-medium contact is the numerical counterpart.

## 4. What the CS-24 data observations suggest (exposed; readings, not evidence)

- **H20 mismatched pairs** (`scripts/cs24_score.py` output):
  - every resolved mismatched pair needs a **higher** v_cr than its matched pair: Al on Ni +34 %, Al on Ti +26 %,
    Cu on Al +12 %, Cu on Ti +40 %;
  - Ti on Cu was −17 %, but unresolved.

  An interface that needs fresh surface from **both** partners (co-exposure) is limited by the weaker supplier,
  whichever side that is. Hardness alone does not order the pairs (Cu on Al).
- **CH heated substrates, matched:** Al −11 %, Sn −18 %, against −2.3 % and −7.1 % from heat partition. The
  substrate's state reaches the interface through what the substrate *supplies* (it softens, deforms and jets more),
  not through heat flow.

## 5. Limits any CS-25 must face (all from this track)

1. **This is near the interface-state route closed on 2026-11-17** (DECISIONS "Track B interface-state route closed;
   reduced route adopted"). That route was closed because solver interface states do not converge.
   - Driver check (driver-check-2026-11-17.md; solver-facts §1): annulus plastic work, pressure–slip history,
     ring-averaged stretch, raw v_edge and ring Y do not converge. Only the contact radius a(t) does.
   - So an interface fed by solver-local fluxes inherits non-convergence. The hunch must either take converged
     inputs, or regularise through its own length and show that this length is resolved.
2. **Identifiability (§2(e)).** Each interface state variable adds parameters: supply rates, expulsion, strength. One
   v_cr per condition cannot fix them; a ring map (a function of r per impact) can.
   - No unseen ring-map source exists. That is why CS-20 is parked (DECISIONS 2026-11-24).
   - All single-impact v_cr data is exposed (`data/vcr_lipit.csv`).
3. **It cannot fix the bulk band** (§2(b)): the interface decides bonding, not edge convergence.
4. **What has been tried and must not be re-proposed unknowingly** (multi-particle-tried.md):
   - CS-12, Bay stretch activation: retired; its in-solver form bonds the pole first (§26);
   - CS-20, the switch radius: parked;
   - CS-22b / CS-23, the forked bond response with and without stick;
   - the pressure–slip driver (§27): does not converge.

## 6. The one feasible form the modeller sees (to be reasoned through in the fresh session)

**An interface model driven by a(t), the only converged quantity, not by solver interface fields:**
- **Birth:** the interface element at radius r is born when the edge passes r, at t(r) from a(t) (rigid kinematics or
  the fitted a(t) of the switch check). It knows v_edge(r) = RV/r, and therefore whether the edge was supersonic,
  plus both partners' properties.
- **State:** a film-coverage state φ(r, t), fed by both partners' supply and drained by expulsion. Supply could come
  from each partner's flow stress and its jetting tendency (e.g. Z7/Z9 quantities); expulsion from the subsonic,
  jetting phase.
- **Bond rule:** bonding where 1 − φ at the end of contact exceeds a threshold. The particle bonds if the bonded area
  is large enough.
- **What it has to reproduce (exposed):** a weak centre, and v_cr raised by any mismatch.
- **First unseen predictions:**
  - ring-map changes: a narrower or shifted ring for mismatched pairs, a wider ring on a heated substrate;
  - v_cr for unmeasured pairs.

**What the fresh session must settle before drafting:**
1. How it differs from R3 and CS-20, which are a threshold on a kinematic switch.
2. How many parameters it has, and what fixes each one.
3. Which zoo members (Z6, Z7, Z9) it must beat, and on what.
4. A kill criterion that is not post hoc; if none exists, say so and ask Peter for a waiver.
5. Its closest relatives: the third-body literature, Bay-type film models, and Hassani 2020's impact modes.
