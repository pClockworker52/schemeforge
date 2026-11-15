# Boundary integration and patch tests in corrected particle methods (WSL B task 2026-11-15-b11)

**Status 2026-11-15 (second part):**
- **Read:** task papers 3, 4 and 6 (Hillman 2013, Ganzenmüller 2015, Tang 2021) and three sweep sources (B, C, F),
  plus one further review (D) and one extra source added at Peter's request (H, Vignjevic et al. 2006).
- **References to §n:** §21 and §22 are sections of `docs/research/opencourant-verification.md` (§21 BCT under
  non-uniform and curved loads; §22 BCT off at the 0.5 µm scale).
- **Not obtained:** task papers 1 and 2 (Chen et al. 2001; Chen, Hillman & Rüter 2013), which are closed.
  Hillman 2013 (E) is the dissertation behind paper 2 and restates paper 1's integration constraint, so the claim
  table no longer depends on them.
- **Page numbers:** printed page numbers for B (journal), E, F and G (theses); PDF page numbers for A, C and D; journal pages for H (CMES 181–198; PDF page n = journal page 180 + n).
- **Labelling:** my own reading is marked **[reading]**.

**Blind screen:**
- **Search:** each source's text was searched for the names, journals, DOIs and article numbers of B06, B07 and B16
  (and of B03, B05, B12), and for "cold spray".
- **A–F and H:** no hits on the blind papers. Same-surname hits are unrelated authors (Y. Wu and W.K. Liu in E;
  W.K. Liu in F).
- **G (Tang 2021):** a cold-spray thesis completed in 2021, before B16 (2024), B07 (2025) and B06 (2026) appeared,
  so it cannot contain their numbers.
  - **B03, B05, B12:** searched by name and journal: no Tiamiyu and no Chen 2022.
  - **Author-name hits:** "Hassani", "Schuh" and "Ichikawa" hit earlier work: Hassani-Gangaraj et al. (its refs.
    [9], [12], [16]), Sun et al. 2020 (ref. [60]), Xie et al. (ref. [30]) and Guetta et al. (ref. [43]), none on the
    blind list.
  - **Journal hit:** ref. [64], J. Wu et al., Scripta Mater. 54 (2006), shares surname and journal with B06 but is
    not B06.
- **Withheld:** nothing. No velocities are reported in this note.

## Sources read

| Id | Source | Copy (URL, version) | sha256 |
|---|---|---|---|
| A | G.C. Ganzenmüller, "An hourglass control algorithm for Lagrangian Smooth Particle Hydrodynamics", Comput. Methods Appl. Mech. Eng. (2015), doi:10.1016/j.cma.2014.12.005 (DOI from a search result, not checked against the journal) | https://arxiv.org/pdf/1410.7221v1, arXiv v1 of 27 Oct 2014 ("preprint submitted"), 38 pp. Journal version not seen | `47d1992695370aefc26458492ab04607683949885f80ff29b902c68ceb0a5974` |
| B | S.-W. Chi, J.-S. Chen, H.-Y. Hu, J.P. Yang, "A gradient reproducing kernel collocation method for boundary value problems", Int. J. Numer. Meth. Engng 93 (2013) 1381–1402, doi:10.1002/nme.4432 | NYCU institutional repository, handle 11536/21169 (bitstream via its DSpace API, https://ir.lib.nycu.edu.tw/server/api/core/bitstreams/00cc2aa0-eaca-47bc-b9ec-baadd1f40f43/content); publisher version, 22 pp. | `7ee15f4a14cd2209a2e25e0b9ae787f564f8df2bde205c24881f525344bab571` |
| C | I.M. Wiragunarsa, L.R. Zuhal, T. Dirgantara, I.S. Putra, E. Febrianto, "Total Lagrangian SPH with an improved bond-based deformation gradient for large strain solid dynamics" | https://arxiv.org/pdf/2407.04021v2, arXiv v2 of 4 Sep 2024 ("preprint submitted to Elsevier"), 33 pp. | `ac270b92e3ded364e48d70d2a44dbfc0fe7eb9966efd32c711b078e80e59b653` |
| D | T. Halada, S. Yaskovets, A. Singh, L. Beneš, P. Suchde, I.F. Sbalzarini, "An overview of meshfree collocation methods" | https://arxiv.org/pdf/2509.20056v2, arXiv v2 of 2 Oct 2025, 92 pp. (including Supplementary Material) | `7b3535366a6266dc069cce3dcf0cca64de29d5ccee5f22cbed74dfe054655fe6` |
| E | M.C. Hillman, *An arbitrary order variationally consistent integration method for Galerkin meshfree methods*, PhD dissertation, UCLA 2013 (chair J.-S. Chen), https://escholarship.org/uc/item/2s8848b6 | eScholarship PDF, downloaded by Peter in a browser, filed as `coldspray-papers/notlisted_Hillman_PhD-thesis_2013.pdf`; 154 pp. | `3907421c168f71ff7b158fc706d64955ae02835e4ec278b7c5e62037d9a6c84a` |
| F | J.R. Reveles, *Development of a Total Lagrangian SPH code for the simulation of solids under dynamic loading*, PhD thesis, Cranfield University 2007 (dspace.lib.cranfield.ac.uk 1826/3916) | Cranfield DSpace PDF, downloaded by Peter in a browser, filed as `coldspray-papers/notlisted_Reveles_PhD-thesis_2007.pdf`; 231 pp. (scanned, OCR text) | `268c06aae484f60068d032f34781d350e02135494845cc4af64d43a3d66f1886` |
| G | J. Tang, *Predictive model of impact-induced bonding in cold spray using the Material Point Method*, MASc thesis, University of Waterloo 2021, http://hdl.handle.net/10012/17030 | UWSpace PDF, downloaded by Peter in a browser, filed as `coldspray-papers/notlisted_Tang_MASc-thesis_2021.pdf`; 110 pp. | `4d5ff0e9c027279eb594f84d042185c48b4071c90845951d1b412b1e81a0109a` |
| H | R. Vignjevic, J.R. Reveles, J. Campbell, "SPH in a Total Lagrangian Formalism", CMES 14(3) (2006) 181–198 | Tech Science Press journal version, supplied by Peter, filed as `coldspray-papers/notlisted_Vignjevic_CMES2006.pdf`; 18 pp. | `5fb047168f48fe891e3fb6af6abe3d187d85264e6d3e952606d0086acae8b892` |

**Roles:**
- **Task papers:** A is paper 4, E is paper 3 and G is paper 6.
- **Task paper 5 (sweep), three sources:** B (Neumann conditions in RK collocation), C (TLSPH boundaries) and F (a
  TLSPH thesis with a section on boundary conditions).
- **D:** a review of collocation methods read during the sweep. It adds nothing on traction patch tests and is not
  counted as one of the three.
- **H:** an extra source added at Peter's request (journal pages), outside the three.

## Not obtained

| Task # | Paper | What happened | How to get it |
|---|---|---|---|
| 1 | Chen, Wu, Yoon, You 2001, SCNI, IJNME 50:435–466 | No open copy found (OSTI, arXiv and author pages searched). One copy is on Scribd; not used, under the fetch rule. A copy at repository.hku.hk (10722/54308) did not resolve from here. Its integration constraint and SCNI are restated in E (§3.1, citing it as [23]) | Peter or Alex (Wiley), if the original is wanted |
| 2 | Chen, Hillman, Rüter 2013, VCI, IJNME, doi:10.1002/nme.4512 | No open copy found. E is the dissertation the paper comes from (same method, chs. 3–4) | Peter or Alex (Wiley), if the original is wanted |
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
   - **Our engine:** its force, f_i = Σ_j V_i V_j (P_i K_i + P_j K_j) ∇W_ij (SPEC-TL-b 4.2, `tl_mod.F90`), is eq. 24. In
     SPEC-TL-b 4.2's formulas K stands for L⁻¹ (`kinv` in `tl_mod.F90`). The engine uses h̄ = ½(h_i + h_j), so
     ∇W_ji = −∇W_ij.
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

## D. Halada et al. 2025 review of meshfree collocation (also read; not one of the three sweep sources), arXiv v2

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


## E. Hillman 2013 (task paper 3), dissertation

1. **Formulation.** Galerkin meshfree methods (reproducing kernel shape functions, RKPM) under numerical domain
   integration:
   - Gauss integration (GI);
   - direct nodal integration (DNI);
   - stabilized conforming nodal integration (SCNI, of task paper 1);
   - stabilized non-conforming nodal integration (SNNI);
   - variationally consistent integration (VCI, of task paper 2).

   Chapter 7 compares these with strong-form RK collocation. Chapter 6 extends VCI to Total and Updated Lagrangian
   RKPM.
2. **Loaded boundaries.**
   - **The linear integration constraint (§3.1.1, p. 13, eq. 3.1):** ⟨∇Ψ_I⟩_Ω = ⟨Ψ_I n⟩_∂Ω for all I, "the
     condition to numerically integrate the divergence equality" for first-order Galerkin exactness (citing [23] =
     Chen et al. 2001).
   - **Necessary and sufficient, both stated:**
     - Sufficient: "the exactness in the Galerkin approximation is guaranteed provided additional integration
       constraints are met" (p. 13); "Domain integration that meets (3.28) yields Galerkin exactness" (p. 26).
     - Necessary: Remark 3.3 (§3.2.2, p. 26), numerical integration "of the domain and boundary integrals … has to
       be consistent with the test functions … for an nth order complete numerical method to achieve the nth order
       exactness … (passing the nth order patch test)". The §3.2.2 derivation inserts the exact solution into the
       discrete equations.
     - Sufficiency also assumes a stable, uniquely solvable discrete system (§4.2).
   - **Elasticity (§3.2.4, pp. 28–31):** the general constraint is eq. 3.41. For a linear displacement field
     (constant stress) it reduces to ⟨Ψ̂_I,1⟩_Ω = ⟨Ψ̂_I n_1⟩_∂Ω and ⟨Ψ̂_I,2⟩_Ω = ⟨Ψ̂_I n_2⟩_∂Ω (eq. 3.45, p. 31).
     The traction boundary ∂Ω_h enters through the boundary integral.
   - **Linear patch test with a natural (flux) boundary, Poisson problem (§3.1.1, pp. 14–15, Table 3.1):** the
     set-up has a Neumann edge ∂Ω_h (eq. 3.2b).
     - "Because both Gauss integration and direct nodal integration fail to meet the linear integration constraint,
       they fail the patch test." The DNI error is 0.0237 on a uniform node set and 0.72 and 0.68 on perturbed sets.
     - "meeting the linear completeness requirement alone is not sufficient for passing linear patch test" (p. 15).
   - **Bulk nodes meet the constraint (pp. 16–17):** in the convergence study with a pure essential boundary
     (eq. 3.4), on uniform nodes "the integration constraint is met for nodes with kernel functions that do not cover
     the boundary of the domain, since Gauss and direct integration points are symmetric with respect to the shape
     functions".
   - **Linear patch test for elasticity with a traction edge (§4.3.3, pp. 45–46, Table 4.3):** plane strain on
     (−1, 1)², 25 nodes.
     - Boundaries: a traction edge ∂Ω_h on 0 ≤ x ≤ 1, y = 1, the "same" decomposition as §4.3.2. The rest of ∂Ω is
       essential, imposed by Nitsche's method with penalty 10³E/h (§4.3, p. 41).
     - L2 error: DNI 0.0648, SNNI 0.0532, 1×1 GI 0.0810; SCNI 8.66 × 10⁻¹⁴; DNI with VCI 3.42 × 10⁻¹⁴.
     - "spurious deformations are seen to take place for methods without VCI" (Fig. 4.4), and the constant shear
       stress is reproduced only with VCI (Fig. 4.5).
     - Eq. 3.45 integrates over all of ∂Ω, so E does not separate the traction edge's share of the error from the
       Nitsche edges' share.
   - **Strong-form collocation (§7.1.2, pp. 89–90):** "Assuming nth order completeness, the collocation method
     (7.1) will give the exact solution for BVPs with nth order solutions. This is in contrast to the Galerkin method
     where additional constraints exist on the choice of numerical integration and test function."
     - The argument includes the natural-boundary collocation equations (eqs. 7.1b, 7.9b).
     - E's numerical collocation patch tests (Tables 7.1–7.2) use a pure Dirichlet boundary. The numerical support
       for traction boundaries in collocation comes from B.
     - Convergence needs "reproducing degree of at least 2" (§7.1.3, p. 91).
3. **Remedies, and what they need from the code.**
   - **SCNI (§3.1.2, pp. 18–20):**
     - Gradients are smoothed over conforming nodal cells by the divergence theorem, ∇̃Ψ_I(x_L) = (1/A_L)⟨Ψ_I n⟩_∂Ω_L
       (eqs. 3.6–3.9). The constraint then holds by construction (eq. 3.10).
     - "To yield linear exactness … using SCNI, the boundary integration rules used in ⟨Ψ_I n⟩_∂Ω_L in (3.9) should be
       used for natural or essential boundary terms in the weak form" (pp. 19–20).
     - Needs: a conforming cell partition (Voronoi or Delaunay; "cumbersome in problems subjected to topological
       change", p. 20), and boundary quadrature on the cell faces that is also used for the applied traction.
   - **VCI, assumed-strain form (§4.1.2, pp. 35–36):**
     - The test-function gradient of node I gets a constant correction over its support, ∇̃Ψ_I = ∇Ψ_I + R_I ξ_I,
       with ξ_iI = −(⟨Ψ_I,i⟩_Ω − ⟨Ψ_I n_i⟩_∂Ω)/⟨R_I⟩ (eqs. 4.10–4.12). This makes any quadrature meet the constraint.
     - The method is Petrov–Galerkin (test ≠ trial gradients).
     - Needs: the boundary integral ⟨Ψ_I n⟩_∂Ω, that is a boundary quadrature with points, normals, weights and
       shape-function values, plus one correction vector per node.
   - **Lagrangian setting (§6.1.3, p. 78, eqs. 6.7–6.9):** the VCI coefficients are computed in the undeformed
     configuration, ξ_I = (⟨Ψ_I n⟩_∂Ω_X − ⟨Ψ_I,i⟩_Ω_X)/⟨R_I⟩_Ω_X. For a Total Lagrangian code this is a one-off
     reference computation.
   - **Nonlinear tests (§6.2, pp. 81–86):** an elastic-plastic bar and a Taylor bar impact, with VC-SNNI against
     SNNI and SCNI. The J2 examples use the Updated Lagrangian form of §6.1.5. No time integrator is stated and
     momentum conservation is not discussed.
4. **Carry-over to strong-form TLSPH with penalty contact on the outer layer.** **[reading]** It inherits the
   conditions of B item 4: hyperelastic P, fixed reference, symmetric neighbour sets, a symmetric kernel argument
   h̄ = ½(h_i + h_j), and reflected L⁻¹ for images, with hourglass and viscous forces excluded.
   - **TLSPH as DNI.** With the energy-gradient form of the TL force (B, item 4), TLSPH is a direct-nodal-integrated
     Galerkin method with particle volumes V_k as weights. The "shape-function gradient" is the one implied by F_k
     (eq. 17 of A): for node I seen from particle k it is V_I L_k⁻¹∇W_kI for I ≠ k, and −Σ_j V_j L_k⁻¹∇W_kj for
     I = k.
   - **B_I is Hillman's domain integral.** Summing that gradient over k with weights V_k gives
     ⟨∇Ψ_I⟩_Ω = −Σ_j V_I V_j (L_I⁻¹ + L_j⁻¹)∇W_Ij = −B_I. Here B_I is the project's vector (SPEC-TL-b 4.2, with K =
     L⁻¹; `bvec` in `tl_mod.F90`, whose comment, Σ_j V_k V_j (K_k⁻¹ + R K_j⁻¹ R)∇W_kj, uses K for L itself, so
     K⁻¹ = `kinv` = L⁻¹). The internal force is then f_I = σ·B_I,
     as SPEC-TL-b 4.2 states ("each end layer k receives P · B_k"). My algebra, checked by the reviewing agent; not
     from a source.
   - **The §22 finding is a constraint failure.** The linear constraint (eq. 3.45) requires ⟨Ψ_I n⟩_∂Ω = −B_I.
     - In the bulk B_I = 0 and there is no boundary term, so it holds.
     - At the loaded end of the SPEC-TL-b column (B pointing inward, n outward), it requires face weights −B_I·n per
       unit area of 1.485, −0.471 and −0.014 on layers 1–3. The wall and the hvi contact apply 1, 0 and 0.
     - The constraint is violated, the uniform-stress patch test fails, and the face layer carries the wrong stress.
       This is E's DNI failure (Tables 3.1 and 4.3), reached for TLSPH through the project's own static model.
     - The error term is σ·(⟨∇Ψ_I⟩ − ⟨Ψ_I n⟩). On a lattice-aligned free face B_I ∥ n and σ·n = 0, so it vanishes.
       That is why only normally loaded faces fail, consistent with SPEC-TL-b 4.2's free-face paragraph.
     - **Limits:** this explains why the deficit exists. The split without hourglass control is 0.515 / 0.985. The
       measured α = 10 split (0.65 / 0.84) also depends on the hourglass force, which is outside the argument. E's
       evidence is 2D static RKPM with Nitsche boundaries.
   - **BCT is a version of E's SCNI requirement.** BCT spread the load in proportion to B_k·n, making the traction
     quadrature consistent with the operator, as E's SCNI remark requires ("boundary integration rules … should be
     used for natural … boundary terms"). It did that for whichever particles were loaded, so it depended on the
     patch. §21 found it fails on small or changing patches.
   - **VCI turns the correction round.** It fixes the operator once, in the reference configuration, against a
     chosen boundary quadrature. The load then has to be applied through that same quadrature. Concretely:
     - a reference surface quadrature over each body (the measurement skin of D2 is a candidate carrier);
     - per surface particle one correction vector ξ_I, applied in the force as a Petrov–Galerkin term;
     - contact tractions applied through the surface quadrature, not as point forces on layer 1.
   - **Open:**
     - TLSPH has only an implied gradient and no Ψ_I that can be evaluated at surface points. Defining one on the
       surface (Shepard or RK interpolation) is a modelling choice.
     - With the ξ_I R_I term, Σ_I ∇̃Ψ_I(X_k) ≠ 0 in general, so the internal forces no longer sum to zero for
       non-uniform stress. Exact linear momentum is then lost, not merely unshown (my algebra).
     - E covers neither penalty contact nor moving contact patches.

## F. Reveles 2007 (sweep), thesis

1. **Formulation.** Total Lagrangian SPH, normalised and corrected (Shepard normalisation plus derivative
   correction, §4.3; chs. 4–5), in an explicit code (the MCM SPH code, §5.1). A and our engine use the derivative
   correction only, without normalisation.
2. **Loaded boundaries.**
   - The SPH derivation drops boundary terms "since we assume a kernel with compact support" (§2.1, pp. 16–17; again
     in ch. 7, p. 165).
   - **§3.3, pp. 34–36:**
     - In standard SPH free-surface conditions "have been successfully ignored since the value of stress drops to
       zero at a distance 2h due to the lack of neighbouring particles".
     - "In the normalized SPH case, both free and traction boundaries have to be imposed rigorously at the surface."
     - Ghost particles and repulsive boundary particles are reviewed. Of boundary terms in the SPH equations
       (Campbell), the author writes: "although mathematically rigorous, poses new and unresolved problems. More
       work is required in this area before a general purpose treatment of boundary conditions method is available
       in SPH."
   - **Tests:** Problem 3 (§6.1.3, p. 111 ff.) checks constant and linear gradient fields at boundary particles in
     1D. The conclusion (p. 155) is that the correction makes the scheme first-order consistent and that
     normalisation corrects the particle deficiency at boundaries.
   - **Appended paper:** the thesis appends the paper published as H (PDF p. 227, no printed page). Its claims are
     taken up in H.
   - No traction patch test and no stress error at a loaded face are reported.
3. **Remedies named.** Ghost particles mirroring stress, Monaghan-type repulsive boundary particles, and Campbell's
   boundary terms. None is developed for traction in the TL code.
   - Ghost particles need a mirror construction about the surface.
   - Boundary terms need a surface representation and, per the author, raise a density term "of little or no
     physical meaning" (p. 36).
4. **Carry-over.** **[reading]** F states the requirement for a normalised kernel (traction must be imposed
   rigorously) without an analysis or a remedy. Neither F nor C treats a boundary-consistent traction for TLSPH,
   which matches SPEC-TL-b 4.3.

## G. Tang 2021 (task paper 6), MASc thesis; task item 5

1. **Formulation.** MPM (Galerkin on a background grid; "the particles act essentially as integration points within
   the grid element", p. 52), with PTW strength, SCG melt and Mie–Grüneisen EOS. Viscous damping boundaries
   represent the semi-infinite substrate (§3.5.5).
   - **Contact:** grid-based multi-mesh contact. The normal is that of the substrate (maximum volume gradient,
     §3.5.4, pp. 34–35); normals are "a known source of error in MPM".
   - **Bond:** a history variable D_bond; when its grid value reaches 1, the sticking contact force is applied in
     the separation phase (pp. 39, 51).
2. **Loaded boundaries.** Not treated as a patch-test or boundary-integration question. Nothing in G addresses the
   external review's claim.
3. **Remedy.** Not applicable.
4. **Carry-over.** None for the boundary question.
5. **What converges under refinement, against what reference, and which length or regularisation.**
   - **Without a bond (grids 1.5, 1.0 and 0.5 µm, three particle spacings each, 14 µm particle):**
     - Strains "appear to converge to similar values for each grid size and with increasing numbers of material
       points per computational grid", but "strains do vary drastically with grid size refinement" (§4.2.3, p. 48,
       Fig. 4.8). Some runs did not reach the 1000 ns end time (24 h limit, p. 48).
     - Jetting appears "around the perimeter of the contact interface" only as the grid is refined (Fig. 4.5,
       pp. 45, 48).
     - The average plastic strain energy density shows "smaller discrepancies" (§4.2.4, p. 49, Fig. 4.9).
   - **The strain-based bond model is grid-sensitive:** its bonding boundaries are "extremely different" between
     grids (§4.1.3, pp. 44–45, Fig. 4.6).
   - **Regularisation:** the energy-based model adds ΔG_s = σ_vm Δε_p D_Cell, with D_Cell the grid length (eq. 4.17,
     p. 52), after the characteristic-length regularisation of fracture mechanics (eq. 4.16, p. 51). The author:
     "this insensitivity is more as a result of including D_Cell than purely switching to an energy measure" (p. 52).
   - **What converges, with the bond:**
     - The bonding boundaries in the space of the two model parameters (G_c, Ġ_c), found by logistic regression,
       are "similar" across nine grid configurations (grids 1.5, 1.0 and 0.7 µm) for both the 14 µm and the 30 µm
       particle (§5.1.3, pp. 64–65, Fig. 5.7).
     - The PBCP classification tolerances, by grid (Table 5.2, p. 60):

       | Grid | 14 µm particle | 30 µm particle |
       |---|---|---|
       | 1.5 µm | 8.0–8.5 % | 8.1–9.2 % |
       | 1.0 µm | 6.0–6.1 % | 8.1–8.3 % |
       | 0.7 µm | 4.6–4.8 % | 4.9–5.3 % |

       The author reads this as "a clear convergence" (p. 60) and as "appropriately convergent" with particles per
       grid (p. 61). PBCP (eq. 5.1, p. 59) is the count of points with D_bond ≥ 1 over the count with D_bond > 0.
       Taking it as the percent bonded area is the author's assumption (p. 79).
   - **What does not converge:** the particle shape and the jetting change visibly between the 1.0 and 0.7 µm grids
     (Fig. 5.8, pp. 65–66). The author calls the 0.7 µm shape "more accurate … relative to experimental evidence",
     not converged. Grid size matters more than particle spacing.
   - **Not reported:** the surface expansion Y and the contact pressure p_n are not reported or checked under
     refinement.
   - **Reference:** there is no spatial reference, only a time-step one. A 0.05 time-step scaling factor serves as
     "a reference for convergence", and 0.1 gives an "identical" boundary (pp. 66–67, Fig. 5.9). Elsewhere:
     - the calibration targets experimental critical velocities (its ref. [9], Hassani-Gangaraj et al. 2018);
     - the bonded fraction is compared with a theoretical ~5 % (its ref. [60], Sun et al. 2020) and a 15–95 % range
       (its ref. [90], Schmidt et al. 2009) (pp. 79–80).
   - **[reading]**
     - "Discretisation independence" in G means calibrated bonding boundaries and bonded fraction that agree between
       grids under a grid-length regularisation. The finest grid is 0.7 µm, for 14 µm and 30 µm particles.
     - Three grids with PBCP tolerances still falling from 1.0 to 0.7 µm, for a tolerance chosen per grid, do not
       show a limit.
     - It is not verification of the interface state (Y, p_n) against a reference. This matches reviewer-1's
       reading from the abstract.

## H. Vignjevic, Reveles, Campbell 2006 (extra source, added at Peter's request), journal version

1. **Formulation.** Total Lagrangian SPH with the "mixed correction": Shepard-normalised kernel plus corrected
   derivatives (abstract; §3, §4.2, pp. 183–189). It is the journal paper of the TL code in F.
2. **Loaded boundaries.**
   - **Abstract (p. 181):** "The Total Lagrangian framework is combined with the mixed correction which ensures
     linear completeness and compliance with the patch test, R. Vignjevic, J. Campbell, L. Libersky (2000)." The
     patch-test claim is cited from the 2000 paper, not shown here. Also: "In corrected SPH, the domain boundaries
     and field variables at boundaries are approximated with the default accuracy of the method."
   - **Introduction (p. 181):** "the lack of rigorous treatment of boundary conditions still hamper the full
     exploitation of the method". Of the MLPG alternative, it "requires additional effort and care in the treatment
     of boundary conditions" (p. 182).
   - **The only boundary test (§5.1, pp. 189–191, Tables 2–4):** a 1D gradient of a constant and a linear velocity
     field, at particles with incomplete support (particles 1, 2) and complete support (Tables 3–4 in Appendix A, p. 192). The TL scheme reproduces the
     linear gradient only with the symmetrisation term.
   - **Other examples (§5.2–5.4):** plate impact, normal impact of a prism on a plate, spall. Loads are impacts; no
     traction patch test, no stress at a loaded face.
   - **Conclusions (p. 197):** "The corrections introduced render the method 1st order consistent and the
     normalization of the smoothing function ensures the particle deficiency problem at the boundaries gets
     corrected."
3. **Remedy.** Kernel normalisation and derivative correction, for the approximation at boundary particles. Nothing
   for traction application.
4. **Carry-over.** **[reading]**
   - "Patch test" here means reproducing linear fields and their gradients (completeness). E shows that for a
     Galerkin-type method under nodal integration, completeness alone does not pass the linear patch test with a
     traction boundary (E, p. 15: "meeting the linear completeness requirement alone is not sufficient"). So H's
     claim does not cover the §22 case. It is the same distinction as for A, item 4.
   - The 2000 paper it cites was not read: Vignjevic, Campbell, Libersky, "A treatment of zero-energy modes in the
     smoothed particle hydrodynamics method", Comput. Methods Appl. Mech. Eng. 184 (2000) 67–85, per H's reference
     list.

## Claim table: external review, inputs.md input 2, point 4

| Claim (input 2, point 4) | What the sources show | Still open |
|---|---|---|
| Where the verification literature lives: "(e.g., Ganzenmüller 2015 on TLSPH; Chen, Belytschko, and Puso on stabilized conforming nodal integration)" | Half right. A has no boundary or traction analysis (pp. 16–30). The SCNI/VCI literature (E, restating paper 1) is where the relevant result lives. (Belytschko is not an author of the SCNI and VCI sources read) | — |
| That literature "proves mathematically that strong-form corrected particle methods fail the linear patch test on traction boundaries" | **Proved for Galerkin, wrong for strong form.** For *Galerkin* methods under numerical integration, E derives the integration constraint as necessary and (given a stable system) sufficient for patch-test exactness (pp. 13, 26; Remark 3.3). It shows the failure numerically for DNI, including elasticity with a traction edge (Table 4.3; the other edges by Nitsche). For *strong-form collocation* E states the opposite: completeness alone gives exactness (§7.1.2, argued including natural boundaries; its numerical tests use Dirichlet boundaries only), and B shows convergence with traction boundaries. **[reading]** TLSPH with the eq. 24 force is a nodally integrated Galerkin method (B, item 4; E, item 4), so the failure applies to it, not because it is strong form | — |
| "… unless boundary integrals are evaluated over stabilized surface cells" | Partly. SCNI meets the constraint by smoothing over conforming nodal cells, and the same boundary integration must be used for the applied traction (E, pp. 18–20). VCI meets it for any quadrature by correcting the test-function gradients against a boundary integral (E, §4.1.2, §6.1.3). Both need a boundary quadrature; neither needs "surface cells" in a stabilised sense beyond that | — |
| "… confirming that your §22 finding (the face-layer deficit is structural) is a known mathematical property of the discretization" | **[reading]** Yes, in substance, under the energy-gradient conditions (E, item 4).<br>• The project's B_I is −⟨∇Ψ_I⟩_Ω for TLSPH (my algebra, checked).<br>• Applying the load to layer 1 only violates eq. 3.45, which is E's DNI patch-test failure.<br>• It explains why the deficit exists, not the hourglass-dependent α = 10 split.<br>• E's evidence is 2D static RKPM with Nitsche boundaries.<br>• The project found the mechanism again (SPEC-TL-b 4.2). SPEC-TL-b 4.3 found no TLSPH source, and neither F, C nor H treats it.<br>• BCT was a patch-dependent form of the consistent-traction requirement. VCI is the known remedy, with a fixed reference correction | Whether VCI carries over to explicit TLSPH with penalty contact: a surface Ψ_I must be defined, and the Petrov–Galerkin force loses exact linear momentum (E, item 4, Open) |

## Change log

- 2026-11-15: first part. Sources A–D read; papers 1, 2, 3, 6 and two sweep candidates not obtained (bot challenges
  not bypassed, or no open copy). Reviewed by a separate agent; its findings applied (page ranges, quote fixes,
  CMLS/FPsM names, A §4.4–4.6, C formulation and force form, code requirements, derivation conditions).
- 2026-11-15: second part. E (Hillman 2013), F (Reveles 2007) and G (Tang 2021) read from Peter's browser downloads;
  H (Vignjevic et al. 2006) added at Peter's request. D moved out of the three sweep sources. Papers 1 and 2 stay
  closed and are covered through E. Claim table finalised. Reviewed by a separate agent; its findings applied:
  - the sign of the boundary weights (⟨Ψ_I n⟩ = −B_I);
  - K = L⁻¹ in SPEC-TL-b;
  - necessity and sufficiency;
  - the Nitsche edges in Table 4.3;
  - Tang Table 5.2 and the time-step reference;
  - the normalised (not corrected) wording in F;
  - the blind-screen detail.
