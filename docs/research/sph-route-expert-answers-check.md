# Literature check of the critique's expert answers (sph-route-review-2026-11-critique.md §5)

2026-11-13, cloud modeller, prompted by the meta-review (point 5).
- **Method:** web searches, standard mode. **Every finding is S level** (search-result summaries and abstracts). No
  full text was read.
- **Use:** these are pointers for decisions, not evidence for claims. A finding that would carry a decision has to be
  read at F level first.

| # | Critique's answer (from memory) | Finding | Status |
|---|---|---|---|
| 1 | No particle-method demonstration of deformable–deformable Hertz within 5 % at about 5 spacings; MPM contact (Bardenhagen type) about 10 % | **MPM:** Bardenhagen et al. 2001 validated against rigid-body analytical problems, not Hertz. Recent MPM papers use Hertz as a standard benchmark with grid refinement: two equal disks at three resolutions (arXiv:2403.13534, 2024); a cylinder on a rigid plane with pointwise pressure error (arXiv:2604.18917); refinement sequences (arXiv:2605.09097). Their error levels were not visible in the summaries. **SPH:** one SPH-DEM paper (Comp. Part. Mech. 2023, doi:10.1007/s40571-023-00616-8) reports convergence to Hertz in a simple contact problem; no error-against-spacing table seen. **No source found** for the "about 10 %" figure | **Partly confirmed:** Hertz is a standard MPM benchmark, and no particle-method result at our accuracy and resolution was found. The 10 % figure is not found |
| 2 | Point values of Y and p_n at a moving edge: unrealistic in any method; quantities averaged over a fixed length may be achievable | Not checked directly. Indirectly, see #3 and #5 | **Not checked** |
| 3 | FE with remeshing for a first claim: flattening and crater depth converge; edge strain and jetting onset stay mesh-dependent (Li et al. 2006 and later) | **Wen-Ya Li et al. 2006** (Appl. Surf. Sci., "On high velocity impact of micro-sized metallic particles in cold spraying", Lagrangian and ALE, Cu): the mesh size significantly influences the localised shear instability at the interface; with a finer mesh, the onset velocity of interface shear instability **decreases**. A later Eulerian study: Lagrangian models cannot avoid the dependence on element distortion. **Ge et al. 2026** (Politecnico di Milano, Int. J. Mech. Sci.): mesh size about D/50 is the usual rule, yet particle profiles still vary strongly with mesh size; remapping near high strain gradients can produce unrealistic deformation | **Confirmed** for edge mesh dependence. **Corrected in part:** Ge et al. 2026 report that even *profiles* vary with mesh size at D/50, so "flattening converges" is not safe as stated |
| 4 | Thresholds should be calibrated against a method known to pass, references corrected for finite strain, impact references incl. LIPIT rebound data | **Finite strain:** confirmed in this project (§17). **LIPIT restitution data exist:** Hassani-Gangaraj et al., Scripta Mater. 145 (2018) 9–13 (coefficient of restitution against impact velocity), cited as such by Reiser & Schuh; an α-LIPIT Al-on-sapphire study (PMC5505959) reports ≥ 85 % of the kinetic energy dissipated and a transition in the coefficient of restitution near 500 m/s | **Confirmed** that LIPIT rebound data exist and are used for validation. Their suitability as a judge for this solver is not assessed |
| 5 | Edge quantities do not converge without a length scale (conduction or a gradient model) | **Found:** Ge et al. 2026, "High-Fidelity modeling of cold spray: improved constitutive material model and **nonlocal mesh sensitivity mitigation**". A nonlocal regularisation aimed at exactly this problem exists in recent cold-spray work. Its formulation was not visible (abstract level). Conduction does not do it at the spacings reached in this project (§13, CS-13c) | **Confirmed in direction:** a nonlocal length scale is the current remedy in the literature. Read Ge et al. 2026 at F level before using it |
| 6 | One-way coupling for the oxide scale | A design judgment, not a literature claim. Not checked | **n/a** |

## What this changes

1. **Ge et al. 2026 (Politecnico di Milano) is the most relevant new source.**
   - It is a cold-spray FE study with nonlocal regularisation against mesh sensitivity, plus a multi-particle framework
     from the same group (2026).
   - It bears directly on the question of whether edge quantities exist (review §4 item 4) and on the FE option
     (review §7).
   - **Recommended:** an F-level reading by WSL B or WSL A. The PDFs are on `re.public.polimi.it`, which this session
     has not tested.
2. **Edge quantities depend on the mesh in Lagrangian and ALE FE as well** (Li et al. 2006). This supports the
   critique's main point: the edge problem belongs to the physics or the mathematics of the problem, not to SPH.
3. **No particle-method result was found** that meets our Hertz thresholds at our resolution. This is not evidence
   that none exists.

## Sources (all S level)

- [arXiv:2403.13534](https://arxiv.org/pdf/2403.13534) · [arXiv:2604.18917](https://arxiv.org/pdf/2604.18917) ·
  [arXiv:2605.09097](https://arxiv.org/pdf/2605.09097) (MPM contact and Hertz benchmarks)
- [SPH-DEM, Comp. Part. Mech. 2023](https://link.springer.com/article/10.1007/s40571-023-00616-8)
- [Li et al. 2006 record](https://search.isc.ac/Inventory/10/1003260.htm)
- [Ge et al. 2026, Int. J. Mech. Sci.](https://re.public.polimi.it/retrieve/45d0d1af-830d-464c-8cb5-e44b886085b9/1-s2.0-S0020740326005084-main.pdf) ·
  [Politecnico record](https://re.public.polimi.it/handle/11311/1314673) ·
  [multi-particle framework 2026](https://re.public.polimi.it/retrieve/e5d7048e-0e0c-4049-b157-cc9b35dcee5c/1-s2.0-S2214860426002113-main.pdf)
- [α-LIPIT Al restitution (PMC5505959)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5505959) ·
  [Reiser & Schuh, CSC 2024 slides](https://coldsprayclub.minesparis.psl.eu/wp-content/uploads/2024/06/CSC2024_AReiser.pdf)
