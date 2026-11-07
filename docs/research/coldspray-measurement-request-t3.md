# Measurement request: v_cr against oxide thickness at a fixed oxide type (CS-12 test T3)

Draft 2026-11-07, for Peter. **Not to be sent before the trigger** (DECISIONS 2026-11-05 "Campaign trigger"): B14,
B06 and B05 must be scored and T3 still undecided. As of this draft B14 is frozen (no T3 series in it: under 5 nm
span at one oxide type), and B06 and B05 are pending. Template: [coldspray-campaign-proposal.md](coldspray-campaign-proposal.md)
(parked), of which this is the narrow form: one series, one question.

## 1. The question

Does v_cr of a single particle depend on the **thickness** of its oxide when the oxide **type** stays the same? Four
frozen models give four different answers. A single series of three or more thicknesses separates them.

## 2. The frozen predictions

For Al 6061 at 15 µm, oxide from 17 to 25 nm, same oxide type, same particle strength (the B10 powder state):

| Model | What it says | Δv_cr, 17 → 25 nm | Frozen in |
|---|---|---|---|
| Z18_Yd (Na et al. 2025, Eq. 6; Lienhard jet model, as published) | the oxide stiffens the jet in proportion to t_ox / t_jet | about +127 m/s | coldspray-zoo-z18.md |
| Z18_static (the same, with static strength, k refitted) | as above | about +92 m/s | coldspray-zoo-z18.md |
| CS-10 (energy balance: jetting + plastic work + shell work) | shell work grows with t_ox / d | about +37 m/s | coldspray-hunch-cs10.md, cs10-fit.md |
| CS-12 minimal (Bay-type threshold stretch; blanket idea) | the threshold depends on oxide type, not thickness | 0 within one window | coldspray-hunch-cs12.md |

Typical window widths are 45–50 m/s, so the steps between the predictions (35–55 m/s) are about one window each.
**For the partner's own powder,** the predictions are recomputed from the frozen models with the partner's stage-1
inputs and committed before any v_cr is shared (section 4). The numbers above are illustrative.

## 3. What to measure

1. **One powder,** Al or an Al alloy, narrow size selection (for example 15 ± 1 µm), as used in LIPIT.
2. **At least three oxide thicknesses of one type, spanning at least 5 nm** (for example about 5, 10 and 15 nm, or
   17, 21 and 25 nm on an alloy).
   - The oxide must stay one type: same structure (amorphous or the same crystalline phase) and no hydroxide
     change. Humid storage changes the type (Lienhard 2020) and does not qualify.
   - **Growing the oxide must not change the particle's strength** (B10 showed that heat treatment changes both).
     One route that may do this: atomic layer deposition of Al₂O₃ on the powder at low temperature (fluidized-bed
     ALD). The deposited oxide differs from the native one, but it is the same type at every thickness, which is
     what the test needs. Low-temperature dry oxidation is an alternative if its temperature leaves the strength
     unchanged. The partner's choice.
3. **Per batch, before any impact:**
   - oxide thickness (XPS and/or TEM, with spread);
   - oxide structure (TEM diffraction, FTIR for OH);
   - particle strength (micro-compression or nanoindentation), to show it is unchanged; the models also need it;
   - size distribution.
4. **Impacts:** LIPIT, matched polished substrate (Al on Al, or alloy on the same alloy), room temperature, normal
   incidence.
   - v_cr by the equal-count window (smallest window with equal numbers of bonded and rebounded impacts), with its
     bounds and the number of impacts;
   - velocity uncertainty stated.
5. **Optional, very useful:** for one thickness at and just above v_cr, FIB sections or lift-off maps of the
   bonded area and of oxide left in the contact (inputs for the interface law, CS-12 and CS-14).

## 4. Protocol (blind by design)

1. The partner sends the stage-1 data only (section 3, items 1–3).
2. We compute the predictions of every frozen model from those inputs and commit them to the public repository
   (git timestamp). The partner receives the commit link.
3. The partner sends the v_cr windows (and optional maps).
4. We score them by a script committed before the windows arrive, and publish the result, whatever it is. Data and
   credit go to the partner; co-authorship is open.

## 5. Cover mail (draft, in Peter's style; English; recipient to be chosen)

Subject: Measurement request: LIPIT critical velocity against oxide thickness

```
Hello Prof. [Name],

I would like to ask whether your group could measure the critical velocity of one Al powder at three or more oxide thicknesses of the same oxide type, spanning at least 5 nm, with the particle strength unchanged.

Four published or registered models give clearly different answers for this case: for Al 6061 at 15 µm going from 17 to 25 nm, about +127, +92, +37 and 0 m/s. The predictions are frozen in a public repository, and for your powder they would be recomputed from your characterisation data and committed before you send any velocities. Details are in the attached two-page request.

Could you let me know if this fits your setup, and what it would take in time and cost?

Best regards,
Peter Scholz
[Contact details]
```
