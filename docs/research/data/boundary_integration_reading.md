# Boundary integration and patch tests in corrected particle methods (WSL B task 2026-11-15-b11; first part)

**Status 2026-11-15: partial.** Four open sources read (sections A–D below). The task's papers 1, 2, 3 and 6 are not
obtained (table "Not obtained"), so the claim table at the end is provisional. Statements from a source carry its
page: PDF page numbers for A, C and D, journal pages for B. My own reading is marked **[reading]**.

**Blind screen:** each source's text was searched for the names, journals, DOIs and article numbers of B06, B07 and
B16 (and of B03, B05, B12), and for "cold spray". There were no hits, so no number from a blind paper can appear in
these four methods papers, and nothing is withheld.

## Sources read

| Id | Source | Copy (URL, version) | sha256 |
|---|---|---|---|
| A | G.C. Ganzenmüller, "An hourglass control algorithm for Lagrangian Smooth Particle Hydrodynamics", Comput. Methods Appl. Mech. Eng. (2015), doi:10.1016/j.cma.2014.12.005 (DOI from a search result, not checked against the journal) | https://arxiv.org/pdf/1410.7221v1, arXiv v1 of 27 Oct 2014 ("preprint submitted"), 38 pp. Journal version not seen | `47d1992695370aefc26458492ab04607683949885f80ff29b902c68ceb0a5974` |
| B | S.-W. Chi, J.-S. Chen, H.-Y. Hu, J.P. Yang, "A gradient reproducing kernel collocation method for boundary value problems", Int. J. Numer. Meth. Engng 93 (2013) 1381–1402, doi:10.1002/nme.4432 | NYCU institutional repository, handle 11536/21169 (bitstream via its DSpace API, https://ir.lib.nycu.edu.tw/server/api/core/bitstreams/00cc2aa0-eaca-47bc-b9ec-baadd1f40f43/content); publisher version, 22 pp. | `7ee15f4a14cd2209a2e25e0b9ae787f564f8df2bde205c24881f525344bab571` |
| C | I.M. Wiragunarsa, L.R. Zuhal, T. Dirgantara, I.S. Putra, E. Febrianto, "Total Lagrangian SPH with an improved bond-based deformation gradient for large strain solid dynamics" | https://arxiv.org/pdf/2407.04021v2, arXiv v2 of 4 Sep 2024 ("preprint submitted to Elsevier"), 33 pp. | `ac270b92e3ded364e48d70d2a44dbfc0fe7eb9966efd32c711b078e80e59b653` |
| D | T. Halada, S. Yaskovets, A. Singh, L. Beneš, P. Suchde, I.F. Sbalzarini, "An overview of meshfree collocation methods" | https://arxiv.org/pdf/2509.20056v2, arXiv v2 of 2 Oct 2025, 92 pp. (including Supplementary Material) | `7b3535366a6266dc069cce3dcf0cca64de29d5ccee5f22cbed74dfe054655fe6` |

A is task paper 4. B, C and D come from the sweep (task item 5): B covers Neumann conditions in RK collocation,
C covers TLSPH boundaries, and D is a review of collocation methods.

## Not obtained

| Task # | Paper | What happened | How to get it |
|---|---|---|---|
| 1 | Chen, Wu, Yoon, You 2001, SCNI, IJNME 50:435–466 | No open copy found (OSTI, arXiv and author pages searched). One copy is on Scribd; not used, under the fetch rule. A copy at repository.hku.hk (10722/54308) did not resolve from here. Its abstract is known only second-hand, from a web-search summary of bibliographic listings (manuscript.isc.ac/inventory/10/424203.htm, 2026-11-15) | Peter or Alex (Wiley) |
| 2 | Chen, Hillman, Rüter 2013, VCI, IJNME, doi:10.1002/nme.4512 | No open copy found | Peter or Alex (Wiley); task 3 covers the same method |
| 3 | Hillman 2013, PhD dissertation, UCLA | Open, but eScholarship's CDN answers scripted downloads with 403 (CloudFront). Not bypassed | browser: https://escholarship.org/content/qt2s8848b6/qt2s8848b6.pdf into `coldspray-papers/` |
| 6 | Tang 2021, MASc thesis, Waterloo, 10012/17030 | UWSpace bot challenge (Anubis), as in b9. Not bypassed | browser: http://hdl.handle.net/10012/17030 |
| 5 (candidate) | J.R. Reveles, PhD thesis, Cranfield 2007 (TLSPH; has a section "Boundary conditions in SPH") | Open, but Cranfield DSpace answers with a Cloudflare challenge. Not bypassed | browser: https://dspace.lib.cranfield.ac.uk/bitstream/1826/3916/1/Reveles-Thesis_2007.pdf |
| 5 (candidate) | "Development of stress boundary conditions in SPH for the modeling of solids deformation" (2025), ScienceDirect pii S2196438625007478 | 403; access status unknown. Only a search-result summary seen: offset dummy particles; errors below 1 % need at least 10 particles along the characteristic length (second-hand, not used below) | browser, if open |
| — | Puso, Chen, Zywicz, Elmer 2008, IJNME 74:416–446 (nodal integration) | CORE copy behind a JavaScript check. Not bypassed | browser (core.ac.uk/download/71316876.pdf) |
| — | Belytschko, Chen, Hillman 2024, *Meshfree and particle methods* (book; cited in D, p. 12, as comparing nodally integrated Galerkin and collocation meshfree methods) | Not searched for (book) | library |

## A. Ganzenmüller 2015 (task paper 4), arXiv v1

1. **Formulation.** Total Lagrangian SPH with first-order corrected kernel gradients: L_i = Σ_j V⁰_j ∇W_i(X_ij) ⊗
   (X_j − X_i), ∇̃W = L_i⁻¹ ∇W (p. 8, eqs. 13–16).
   - **Deformation gradient (p. 8, eq. 17):** the symmetrised SPH derivative (eq. 12), with the corrected gradients
     inserted.
   - **Uncorrected force (p. 10, eq. 21):** f_i = Σ_j V⁰_i V⁰_j (P_j + P_i) ∇W_i(X_ij) "is variationally consistent
     in the sense that it minimizes elastic energy [20]".
   - **Corrected force used (p. 10, eq. 24):** the antisymmetric f_i = Σ_j V⁰_i V⁰_j (P_i L_i⁻¹ ∇W_i(X_ij) − P_j
     L_j⁻¹ ∇W_j(X_ji)). Inserting the corrected gradient directly into eq. 21, as "seems to be customary", "destroys
     the local conservation of linear momentum".
   - **How the paper classes the method:** it calls SPH a meshless *collocation* method (abstract; pp. 3–4, 31) and
     relates it "directly … to the nodal integration approach, which is a piecewise constant integration technique"
     (p. 11). On p. 20 it compares its result with other "nodal integration" schemes.
   - **Our engine:** its force, f_i = Σ_j V_i V_j (P_i K_i + P_j K_j) ∇W_ij (SPEC-TL-b 4.2, `tl_mod.F90`; K = L,
     with h̄ = ½(h_i + h_j), so ∇W_ji = −∇W_ij), is eq. 24.
2. **Loaded boundaries.** The paper does not analyse them.
   - **Patch test (pp. 16–17):** "a uniform strain field … the stress should be uniform everywhere. SPH with
     first-order corrected kernel gradients is well-known to pass this test." The test then run is a square patch
     stretched 10 % and integrated in time, for stability. No load is applied after the initial stretch (it is
     unconstrained: my reading of the set-up).
   - **Simply supported beam (p. 19):** loaded by a displacement condition on one particle, with the reaction force
     measured there; the clamp is three columns of fixed particles.
   - **Beam convergence (p. 20):** without stabilisation it converges at about −1.45. "It is not clear how to
     understand this odd rate", and "only computationally expensive cell integration methods have been reported to
     perform in this manner [15]". With α = 50 the rate is about −1.97 (Table 1, p. 21).
   - **Punch test (p. 23):** the tool acts through "a repulsive Hertzian potential" between tool and rubber
     particles. No stress at the contact face is reported.
   - **Rubber pull (p. 25):** velocity conditions on the top and bottom rows. The unstabilised run "exhibits particle
     disorder, in particular near the boundaries of the domain". This is the only boundary-related observation in A.
   - **Taylor impact (Sec. 4.5) and 3D tensile test with failure (Sec. 4.6, pp. 28–30):** loads are an impact and
     prescribed end velocities.

   No traction-boundary accuracy is reported anywhere.
3. **Remedy.** None for boundaries. The paper's subject is hourglass control.
4. **Carry-over to our set-up.** Directly applicable to the formulation, since it is our force form. Nothing in the
   paper speaks to the traction at a penalty-loaded outer layer.
   **[reading]** "Passes the patch test" here means a uniform F is reproduced and gives uniform stress. It does
   not mean that a traction applied to the outer particles is in discrete equilibrium with that stress, which is
   the §22 situation.

## B. Chi, Chen, Hu, Yang 2013 (sweep), publisher version

1. **Formulation.** Strong-form collocation with reproducing kernel (RK) approximation (RKCM), and a gradient RK
   variant (G-RKCM). It is not SPH.
   - **Problem set-up (p. 1382, eq. 1):** the boundary value problem has an explicit Neumann boundary ∂Ω_h with
     operator B_h u = h.
   - **Collocation (pp. 1383–1384, eqs. 8, 12–13):** the PDE is collocated at interior points and the boundary
     operators at boundary points. This is a weighted least-squares system, with weights √α_h = 1 and √α_g = κ N_s
     for RKCM.
2. **Loaded boundaries.**
   - **RKCM error bound (p. 1384, eq. 14):** "for RKCM to converge, the RK approximation of degree p > 2 needs to be
     used" (as extracted; ≥ is meant, from the a^{p−1} in eq. 14 and from p. 1394, "at least second-order bases …
     similar to the convergence requirement for RKCM [30]").
   - **G-RKCM error split (pp. 1389–1390, eqs. 42–45):** the error splits into domain, Neumann and Dirichlet parts
     E1, E2 and E3. "E1 and E2 are in balance without the weight in E2", so α_h = O(1) (eq. 47).
   - **G-RKCM rates (eqs. 50–51):** H¹ error O(a^{q−1}), L² error O(a^q). Remark 5.1 (p. 1391) says q ≥ 2 is
     needed for convergence (extracted as "q > 2"). The same holds for elasticity (eqs. 52–53).
   - **Cylinder under internal pressure (Sec. 7.3, pp. 1395–1396):** a traction-boundary example.
   - **Cantilever (Sec. 7.4, pp. 1396–1398, eq. 75, Fig. 10):** tractions are prescribed at x = L (tip shear), on
     the free faces y = ±D/2, and at x = 0 away from the pinned points. G-RKCM with q = 2 "achieves the similar rate
     of convergence as the RKCM with quadratic basis".
   - **No patch-test failure is reported.**
3. **Remedy, and what it needs from the code.** The traction condition is a collocation equation of its own,
   weighted against the domain residual. That needs:
   - explicit boundary points with normals;
   - an RK basis of degree ≥ 2;
   - a global (over-determined) least-squares solve for the coefficients.

   No special boundary integration is used. **[reading]** None of these maps onto explicit TLSPH with penalty
   contact, which has no system solve and no boundary equation.
4. **Carry-over.** **[reading]**
   - **Not the same class of method.** TLSPH is not this kind of strong-form collocation: it has no boundary
     equation; the traction enters only as a force on outer particles; and its correction is first order.
   - **TLSPH as an energy gradient.**
     - A calls eq. 21 variationally consistent (p. 10). That the corrected eq. 24 is also an energy gradient, f_i =
       −∂/∂x_i Σ_k V_k Ψ(F_k) with F_k from eq. 17, is my derivation; the algebra was checked by the reviewing agent
       on 2026-11-15, but not against a source.
     - It holds for hyperelastic P = ∂Ψ/∂F, for L and V fixed in the reference configuration, and for symmetric
       neighbour sets. A's own patch test adjusts h per particle (p. 17), which breaks the last condition.
     - It excludes the hourglass and viscous forces. The §22 layer split depends on α.
   - **Consequence.** Within those conditions, TLSPH behaves like a nodally integrated Galerkin method, the setting
     of task papers 1–3, although A labels it collocation.
   - **What B does and does not support.** B does not support the claim that strong-form methods need surface
     integrals. It shows that genuine strong-form collocation handles traction boundaries by boundary equations,
     provided the basis order is high enough.

## C. Wiragunarsa et al. 2024 (sweep), arXiv v2

1. **Formulation.** TLSPH with a bond-based deformation gradient, compared with JST-stabilised TLSPH.
   - It uses a mixed formulation in linear momentum and F.
   - Its correction is a first-order corrected kernel, whose gradient ∇W̃¹ is used (kernel correction, not A's
     corrected gradient) (pp. 3, 8).
   - Its force is eq. 22 = B.11 (p. 30): (P_i + P_j)·½(∇W̃¹_j(X_i) − ∇W̃¹_i(X_j)). That is the sum of the stresses
     times a symmetrised corrected gradient, not A's eq. 24.
2. **Loaded boundaries.**
   - Kernel consistency is worse "in the region near the boundaries" (p. 1).
   - With correction the gradient "is no longer anti-symmetric, impacting the local momentum and energy
     preservation" (p. 2).
   - At a boundary point all gradient variants lose antisymmetry (p. 5, Fig. 2c, d).
   - The bond-based F "significantly improves accuracy, especially in proximity to the boundary" (p. 11, eq. 36
     context).
   - The tests use a normal constraint on the swinging plate (p. 13), fixed ends, a prescribed top velocity and
     initial velocities (pp. 17, 21–22).
   - No traction-boundary accuracy is reported.
3. **The boundary term in the derivation (Appendix B, p. 30).** The momentum equation is derived from a weighted
   residual over a small control volume at i (eq. B.2). The surface term ∮∂V_o ψ_i ψ_j n appears in eq. B.7, and
   "Following the consistency condition, the surface integration on the right-hand side will naturally vanish". The
   result is eq. B.11.
   - **What it needs from the code:** nothing; the term is dropped.
4. **Carry-over.** **[reading]** This is a corrected TLSPH force (not the eq. 24 form) derived with a surface term
   dropped by assumption. The surface in C is that of a small control volume, not the body surface.
   - **Where the assumption fails:** near a free or loaded surface, where the support is truncated, the dropped term
     is what I take to correspond to the project's B_k (SPEC-TL-b 4.2: "the discrete counterpart of the boundary
     integral ∫ N_k n dA"). That identification is mine, not C's.
   - **What C does not do:** analyse the consequence of the omission.

## D. Halada et al. 2025 review of meshfree collocation (sweep), arXiv v2

1. **Formulation.** A review of strong-form collocation operators. It covers GFDM, MLS variants including Compact
   MLS (CMLS), the Finite Point Method (FPM), the Finite Pointset Method (FPsM), RBF-FD and others.
2. **Loaded boundaries.** Boundary conditions are imposed as constraints in the local reconstruction. Examples:
   - the hard constraint L_∂Ω q_i = g_i at boundary points in CMLS (p. 25, eq. 69, after Trask et al. [232]);
   - Neumann conditions as added constraint rows in FPsM (Supplementary Material, p. 77, its eqs. 74–76).

   A search of the text found no "patch test", no traction condition (the only hit is inside "abstraction") and no
   surface or boundary integrals.
3. **Remedy, and what it needs from the code.** Boundary conditions enter the local operator construction at
   boundary points. That needs boundary points with normals and a constrained local least-squares problem per
   point.
4. **Carry-over.** **[reading]** The same as for B: collocation imposes traction at boundary points, while TLSPH
   does not.

## Tang 2021 (task paper 6, task item 5)

Not obtained (see above). Reviewer-1 and reviewer-2 of the route review read only the abstract and the record.

## Claim table (provisional): external review, inputs.md input 2, point 4

| Claim (input 2, point 4) | What the sources read show | Still open |
|---|---|---|
| Where the verification literature lives: "(e.g., Ganzenmüller 2015 on TLSPH; Chen, Belytschko, and Puso on stabilized conforming nodal integration)" | A has no boundary or traction analysis. Its patch test is a uniform-stretch stability test, and its loads are displacement or velocity conditions, an impact and a Hertzian contact potential (pp. 16–30) | SCNI papers (1, Puso 2008) not read |
| That literature "proves mathematically that strong-form corrected particle methods fail the linear patch test on traction boundaries" | None of A–D proves or shows this. B shows strong-form RK collocation converging with traction boundaries (cylinder, Sec. 7.3; cantilever, Sec. 7.4), given a basis of degree ≥ 2 and boundary equations. A states that corrected TLSPH passes the uniform-strain patch test. Chen 2001 is known here only second-hand, from its abstract: an integration constraint as a necessary condition for linear exactness in *Galerkin* meshfree methods. **[reading]** That concerns Galerkin with numerical integration, not strong form | 1, 2, 3: whether the integration constraint gives a proven traction patch-test failure for direct nodal integration |
| "… unless boundary integrals are evaluated over stabilized surface cells" | For collocation (B, D) the remedy is boundary equations, not surface cells. For SCNI, smoothing over nodal cells by the divergence theorem is known only from the abstract (second-hand) | 1, 3 |
| "… confirming that your §22 finding (the face-layer deficit is structural) is a known mathematical property of the discretization" | No source read shows it for TLSPH. C drops a surface term by assumption (App. B, p. 30). **[reading, conditional]** The project's own result (SPEC-TL-b 4.2: a uniform stress is not a discrete equilibrium when the load goes to layer 1 only; B_k is the implied boundary integral) looks like the TLSPH analogue of the Galerkin integration constraint, because the elastic TL force of eq. 24 is a nodal energy gradient (B, item 4). *If* papers 1–3 confirm this, the mechanism is known in Galerkin meshfree methods, and BCT was a version of its remedy (the traction distributed to match the discrete boundary term) | 1–3 for the integration constraint and its remedy; whether any source treats it for TLSPH (SPEC-TL-b 4.3 found none) |

## Change log

- 2026-11-15: first part. Sources A–D read; papers 1, 2, 3, 6 and two sweep candidates not obtained (bot challenges
  not bypassed, or no open copy). Reviewed by a separate agent; its findings applied (page ranges, quote fixes,
  CMLS/FPsM names, A §4.4–4.6, C formulation and force form, code requirements, derivation conditions).
