# Closest literature for round 3 (2026-10-22)

A quick search for the hunch-generator and, later, the analyst and referee: what is already known near the likely
round-3 directions (sharp reconstruction plus pseudo-time memory, PLAN §11.5 step 3d) and near the A1/A7 trade-off
that round 2 ended on. Web search only, in a cloud session where arxiv.org could not be fetched: entries marked
**(snippet)** were read from search results only and must be checked before any dossier cites them. Absence of a
hit is not evidence of novelty; only the referee assigns "plausibly new" (CLAUDE.md rule 6).

## 1. Steady-state convergence with limiters (the ratchet's family)

- **Limiter freezing.** Venkatakrishnan, "On the accuracy of limiters and convergence to steady state solutions"
  (AIAA 93-0880, 1993) and the 1995 J. Comput. Phys. paper on unstructured-grid convergence with limiters are the
  standard references for both the smooth Venkatakrishnan limiter and freezing; the zoo's `*_frozen` members
  implement freezing. Round 2's ratchet (H-0006) is labelled "variant of limiter freezing".
- **Practitioners report that freezing can fail.** An SU2 user froze the limiter after the coefficients settled and
  the run crashed (CFD Online, SU2 forum) **(snippet)**. This matches round 2's finding that freezing φ is unstable
  and freezing ψ = 2φ/(1+r) is not; the ψ form is worth stating clearly in any dossier.
- **Differentiable limiters as the usual cure.** ANSYS Fluent documents that non-differentiable limiters stall
  residuals after a few orders and offers a modified Venkatakrishnan limiter **(snippet)**; OpenFOAM recommends its
  `cubic` limiter after Michalak and Ollivier-Gooch (AIAA 2008, "Limiters for unstructured higher-order accurate
  solutions of the Euler equations"), which is differentiable where Venkatakrishnan's clipped form is not
  **(snippet)**. Neither is in the Arena 1 zoo. The cubic limiter is a smooth function of a ratio in the
  Barth-Jespersen framework; a 1D φ(r) form would be a fair zoo addition before any smooth-limiter claim.
- **Recent comparison** of Venkatakrishnan, Wang's modification and Nishikawa's R3 limiter for steady RANS
  (arXiv 2601.16291, 2026) **(snippet)**: similar results with suitable constants.
- **Residual vs. solution stall.** A positivity limiter applied outside the residual can freeze the solution while
  the residual stays nonzero (arXiv 1811.08666) **(snippet)**. The judge measures the residual of the scheme it
  runs, so this cannot fake convergence there, but it is a known way for a "converged" claim to mislead.

## 2. THINC/BVD and other sharp reconstructions

- **BVD principle:** Sun, Inaba, Xiao, J. Comput. Phys. 322 (2016) (arXiv 1602.00814): choose per cell the
  candidate reconstruction with the smallest boundary variation; MUSCL-THINC-BVD is the zoo's `thinc_bvd`.
  Variants: fifth-order and cascade BVD (Deng et al., arXiv 1811.01379), practical versions (arXiv 1708.01148),
  symmetry-preserving P4T2-BVD with two THINC steepnesses (arXiv 2106.01872), unstructured grids (arXiv
  2003.09223), multiphase (arXiv 1704.08041).
- **No hit on steady-state or implicit convergence of THINC/BVD**, in two searches (nozzle, airfoil, residual,
  implicit). The papers report accuracy on unsteady problems. Our dev run shows the gap (THINC/BVD stalls on N5/N6;
  cloud run r-20261022-054308-f275), so "a BVD-type reconstruction that converges in pseudo-time" is the obvious
  round-3 direction, and the search for its relatives must be repeated properly (Scopus/Google Scholar, "BVD"
  with "steady", "implicit", "LU-SGS", "Newton") before any label other than "variant of".

## 3. Sharpness vs. overshoot (A1 vs. A7, hunch H-0011)

- **"On the numerical overshoots of shock-capturing schemes"** (arXiv 2102.09876) compares superbee and minmod on
  the origin of post-shock overshoots **(snippet; not read)**. Most directly relevant source for H-0011; read it
  before closing the hunch.
- Linear stability of second-order MUSCL schemes on strong shocks: superbee has the largest unstable eigenvalue of
  the limiters tested (arXiv 2305.03281) **(snippet)**; superbee "temperamental" on strong shocks, MC with spurious
  oscillations on strong shocks (arXiv 1703.01241, 1704.00724) **(snippet)**. Consistent with round 2: every
  candidate sharp enough for A1/A2 overshot 2–3× van Leer on held-out shocks.
- A minbee/superbee blend with smaller pre-shock oscillations (arXiv 0812.2938) **(snippet)**: a known relative for
  blended-base candidates like c-b5cb82a0ef.

## Suggested uses

1. Hunch-generator (round 3): the open question in §2 is the most promising gap; hunches that claim a convergence
   mechanism for a sharp reconstruction must list limiter freezing and differentiable limiters as relatives.
2. Before 3e: consider a 1D form of the Michalak–Ollivier-Gooch cubic limiter as a zoo member (judge change).
3. Before closing H-0011: read arXiv 2102.09876.

## Sources

- https://arxiv.org/pdf/1602.00814 · https://arxiv.org/pdf/1811.01379 · https://ar5iv.arxiv.org/html/1708.01148
- https://arxiv.org/pdf/2106.01872 · https://ar5iv.labs.arxiv.org/html/2003.09223 · https://arxiv.org/pdf/1704.08041
- https://arxiv.org/pdf/2102.09876 · https://arxiv.org/pdf/2305.03281 · https://arxiv.org/pdf/1703.01241
- https://arxiv.org/pdf/1704.00724 · https://arxiv.org/pdf/0812.2938 · https://arxiv.org/pdf/1811.08666
- https://arxiv.org/pdf/2601.16291 · https://arxiv.org/pdf/1710.07187
- https://cpp.openfoam.org/dev/VenkatakrishnanGradientLimiter_8H_source.html
- https://git.frytea.com/songtianlun/openfoam/commit/ab49eaf9831dc151c3c24f124b88c294fef04be1
- https://wwwafs.portici.enea.it/project/neptunius/docs/fluent/html/th/node369.htm
- https://cfd-online.com/Forums/su2/240689-upwind-scheme-steady-state-problem.html
