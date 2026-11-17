# Reduced route: plan (adopted 2026-11-17, DECISIONS "Track B interface-state route closed; reduced route adopted")

Drafted 2026-11-16 by the modeller, per DECISIONS 2026-11-16 "After the odds review" item 5. The reduced route is the
named fallback of the route review (D3 (iv)). It becomes the project's main line if the dead-end trigger fires, and
it is prepared now so that no time is lost then.

## What it is

The project's goal stays the same: predict whether and where a particle bonds, from material properties, without
fitting to the outcome. The reduced route drops the 3D in-solver interface state and works at a level the data can
judge:

| Option | What it predicts | Built from | Judged on |
|---|---|---|---|
| R1. Closed-form v_cr law | v_cr per material and state | zoo Z6 (v_cr ≈ 0.15 c), Z18 (Na2025 Eq. 6), and the open hunches CS-10 (particle strength and oxide thickness), CS-12 (Bay-type dissolution, oxide type), CS-17 (substrate hardening capacity) | blind papers (B06 next), data/vcr_lipit.csv, the T3 measurement request |
| R2. Particle-level build-up rule | whether a particle bonds onto a deposit versus a plate; erosion of stacks | coldspray-buildup-track.md (questions 1–4, Q-B1), Reiser2024, Panova2026a/b | build-up data audit; new seen or blind sources |
| R3. Kinematic Bay estimate | where on the interface the Bay criterion is first met, as a function of velocity | the geometric impact kinematics (coldspray-kinematics.md) and the CS-12 criterion, without a solver interface state | bonded-ring data (exposed for CS-12 T1; label any comparison post hoc) |

## What is lost against the full chain

- **No resolved interface state:** p_n and Y are not computed locally, so where bonding starts is at best a
  kinematic estimate (R3).
- **No in-solver bond:** its effect on rebound is not modelled.
- **No 3D shape prediction** beyond the elastic and bulk results already verified (T-S1, T-B2 with BCT off).
- **Claims shrink to v_cr laws and build-up rules.** These are judged on blind data under the existing rules.

## What carries over from Track B

- The verified elastic contact numbers and the TLSPH energy balance (§20–§23) are reported as a negative or partial
  result (ledger).
- The finding that the face-layer deficit is a rediscovery of the Galerkin nodal-integration constraint (b11) is
  recorded as such.
- The P3 probe (task 2026-11-16-b) informs whether any local interface claim is possible at all. If it shows
  convergence in 2D, a 2D axisymmetric one-way interface study, labelled as reduced, becomes an option R4.

## First two steps (if adopted)

1. **B06 pre-registration** (Track A, already pending): freeze predictions from Z6, Z18, CS-10 and CS-12 for the two
   B06 conditions (native Al oxide; ZnO coating) before step 3 of the blind protocol. This is the nearest test any
   reduced-route model can get.
2. **Decide the T3 request** (done 2026-11-17: dropped, DECISIONS "T3 measurement request dropped"): B06 is not a thickness series, so the decisive test of CS-12 still needs one. Send the
   measurement request or drop it (the single-impact end point needs one of the two).

Further steps (R2, R3) are chosen after these, under the hunch budget (3 of 5 open).

## Open for Peter

- Which of R1–R3 is the main line?
