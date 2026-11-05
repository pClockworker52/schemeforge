# Reading note: Zhang & Bay 1997, the general cold-welding model (for CS-12)

**Source key ZhangBay1997, evidence level F.** W. Zhang and N. Bay, "Cold welding — theoretical modeling of the weld
formation", Welding Journal 76(10), Welding Research Supplement 417-s to 420-s (October 1997). PDF supplied by Peter
on 2026-11-05 (pp. 1–4 of the file; pp. 5–14 are an unrelated paper). The PDF is not committed (copyright). It is
the later, generalised form of Bay's model; Bay 1983 (*Welding J.* 62(5) 137-s) is its ref. 8 and was **not**
read. Not on the blind list; it contains no cold-spray data.

## The model as printed

| Eq. | Content |
|---|---|
| (1) | Nominal weld strength σ_B = ψ · p_B: ψ is the overlapping surface exposure (fraction of the interface where virgin metal of both sides meets), p_B the effective normal pressure on it. |
| (2) | Cap: (σ_B)max = σ₀ of the weaker base metal. |
| (3) | **Cover layer** (brittle, e.g. scratch-brushed or electroless Ni): exposure ψ_C = (A₁ − A_C)/A₁ = (1 − G) Y. **No threshold**: the layer cracks from the start of expansion. |
| (4) | Surface expansion Y = (A₁ − A₀)/A₁. |
| (5) | G = ductility of the cover layer, G = (Y − ψ_C)/Y. |
| (6) | **Contaminant film** (thin): exposure ψ_F = (A₁ − A')/A₁ = (Y − Y')/(1 − Y'). |
| (7) | Threshold Y' = (A' − A₀)/A'. "The value of Y' for each metal with contaminant films only is determined by pilot welding experiments." |
| (8), (9) | Same surface layers on both sides: ψ = ψ_M. Different layers: ψ = ψ_M1 · ψ_M2. Scratch-brushed surfaces combine both types, with the cover-free fraction γ from SEM. |
| (10) | **Thin contaminant films: p_B = p.** The exposed virgin metal is in contact at once; **no extrusion pressure.** |
| (11) | **Thicker cover layer: p_B = p − p_E**, with p_E the pressure needed to extrude base metal through the cracks. |
| (12) | Critical fragment dimension ratio (t/w)_c = [1/(4 tan α)] · [1/((1 − G) Y) + 1], with t the layer thickness, w the fragment width, α the dead-zone angle. Above it the extrusion is incomplete. |

p_E comes from an energy-method analysis of plane-strain extrusion through the cracks (refs. 11, 14 of the paper,
not given in it). **It depends on the base metal's yield stress with work hardening, Y, the fragments' t/w, and G.**

The fitted inputs printed in the figure legends are G, t/w, Y' and γ. For example, scratch-brushed Al–Al: G 0.050,
t/w 0.100, Y' 0.350, γ 0.632. Scratch-brushed Cu–Cu: G 0.300, t/w 0.050, Y' 0.850, γ 0.813. They are surface-
preparation-specific and taken from pilot experiments and micrographs.

## What this means for CS-12 (frozen 2026-11-05; the file is not edited)

1. **CS-12(b) merges the two mechanisms.** It requires Y > Y' **and** p_n > p_E = m σ_flow, with bonded share
   (Y − Y')/(1 − Y'). In Zhang & Bay these belong to different surface types:
   - a thin film has a threshold Y' and **no** extrusion pressure;
   - a brittle cover layer has **no** threshold and an extrusion pressure p_E(t/w, G, Y, σ).

   CS-12(b) is therefore a hybrid, not Bay's model. It stays frozen as written. If T2 is ever registered, a corrected
   variant (native oxide as film **or** as cover layer, chosen and justified) is a new hunch, not a repair.
2. **On thickness (CS-12's T3):**
   - **Film reading:** thickness does not appear. Y' is empirical per metal and surface, and the paper says nothing
     on how it varies with film thickness. Consistent with CS-12(c), but not support for it.
   - **Cover-layer reading:** thickness enters through t/w in p_E and in (t/w)_c. A thicker layer means a larger
     t/w, unless the fragment width w grows with t.

     Thin brittle films on a stretched substrate commonly fragment with a crack spacing that scales with the film
     thickness. That is a recollection from thin-film mechanics, not sourced here. If it holds, t/w stays roughly
     constant, and thickness drops out again.

   So the paper neither supports nor kills the "no thickness effect" claim. It shows where a thickness effect would
   enter, if there is one: through the extrusion term of a cover layer.
3. **Which mechanism fits a native oxide in cold spray** is an open physical question. A 5–25 nm amorphous or
   semi-crystalline oxide is "thin" in Bay's sense, but brittle, as a cover layer is. Measured fragment geometry (t/w)
   of the oxide at the interface would decide it. That is the kind of interface-state observation the campaign
   exception in plan step 5 allows.

## Checks against the external literature report

| Claim in the report | This paper |
|---|---|
| Formula with weights β / (1 − β) for film and cover layer | Consistent in structure. Here the cover-layer term carries (1 − G) Y, and the weights are γ and the multiplication of exposures (8, 9). |
| "Y' = 0.35 for the non-brushed contaminant film on Al" | The 0.350 printed here is for **scratch-brushed** Al–Al (Fig. 9). Not confirmed as stated. |
| "p_E/σ₀ ≈ 1.85–2.0, constant" | Not here. p_E comes from an energy method and depends on t/w, G, Y and the hardening yield stress. Not confirmed. |
| "Y' varies empirically with film thickness" (summary) versus "property of preparation" (Q1.1) | Here: Y' from pilot welding experiments per metal and surface. Thickness is not discussed. Neither version is confirmed. |
| p_E increases with oxide thickness through channel geometry | Consistent with the dependence on t/w, but stated here only for the cover-layer mechanism. |
