# Arena 2 hunch preview for Target D (step 7), 2026-11-27

Plan step 7: the hunch-generator drafts six hunches for Target D, with lenses as in Arena 1 (including transfer from
other fields), and a literature check naming each hunch's closest published relative and how it differs. **Drafts
only: none is registered, implemented or tested.** Files: `ledger/drafts/d7_*.yaml`. All six pass `ledger.validate`.
Every run id they cite (13) was checked to exist in docs/targets/D.md, docs/rounds/2026-11-27-contact-breakers.md or
docs/judge/2026-11-27-contact-v10-check.md. The sforge MCP tools were not connected, so the agent was given the
dev and promo numbers with their run ids. The literature check is web search. Most entries come from abstracts or
snippets and are marked so in the files. The agent read in full only the Faltus et al. 2024 energy section and the
IPC barrier formula.

| # | File | Lens | Mechanism (short) | Closest published relative | Differs by | Label |
|---|---|---|---|---|---|---|
| 1 | d7_contact_null_biaxial | structure preservation | neo_hooke_iv + 100 γK ⟨2 − I1 + I3⟩₊³; zero on closure and on slip | Wriggers, Schröder, Schwarz 2013 (smallest-stretch term) | acts on the product of both stretch deficits, not on the closing stretch | variant of the Wriggers 2013 family |
| 2 | d7_gamma_free_floor | approximation theory | neo_hooke + a steep J⁻⁶ wall at a γ-independent position (~2e-3 of the gap) | thickness offset in C-IPC (Li, Kaufman, Jiang 2021) | a smooth power wall on J of a continuum medium, not a distance offset | variant of an offset barrier |
| 3 | d7_faltus_conformal | practitioner | faltus2026 with the isochoric invariant replaced by the in-plane conformal distortion (λ1 − λ2)² | Faltus et al. 2024 (arXiv 2405.01185), 2026 (arXiv 2603.13063) | removes the isochoric term's contact role along closure; the same in simple shear | variant of faltus2026 |
| 4 | d7_stiff_then_soft | contrarian (non-convex on purpose) | neo_hooke + a saturating bump in ln J: stiff at small strain, plain neo beyond ~5 % | Xu–Needleman exponential law; non-convex foam energies (Gioia 2001; Pampolini, Del Piero 2008) | used in compression on top of a monotone barrier | variant of non-convex foam energies |
| 5 | d7_ipc_stretch_barrier | transfer (interior-point / IPC) | neo_hooke + IPC's clamped log barrier on each principal stretch below 0.25 | Li et al. 2020 (IPC) | argument is a principal stretch at a quadrature point; no line search, so IPC's guarantee does not transfer | variant of Wriggers 2013 with the IPC barrier |
| 6 | d7_tension_only_fibres | transfer (cartilage) | neo_hooke_iv + 5 γμ Σ⟨λᵢ − 1⟩₊² | Ateshian et al. 2009; Curnier, He, Zysset 1995 | a stabiliser of a fictitious medium; in-plane, tension only | variant of tension-only fibre elasticity |

**Agent's own reading.** No hunch reaches all of Target D on its own. Most claim robustness (D3, D8) at a
neo-Hookean residual gap. Only hunch 3 has a plausible route to every threshold except D4, and it meets D7 at zero
margin. D4 is open in all six. The agent's hypothesis that the small-γ negative a_err bias comes from the judge's
fixed regularization is unmeasured, and it touches the "fixed kr" trap.

**Modeller's check (one, not a review).** Hunch 1 states that its term stiffens only biaxial compression. In plane
strain (C₃₃ = 1), 2 − I1 + I3 = (1 − λ1²)(1 − λ2²). So the ⟨·⟩₊ term vanishes on closure and on slip, as claimed,
but it is also positive in biaxial tension. To be corrected before any registration.

Labels are at most "variant of"; none is "plausibly new" (only the referee assigns that).
