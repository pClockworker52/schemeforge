# Literature check of the fork analysis §3 (TLSPH outlook), 2026-11-12

**Checked:** the outlook in the fork's `hvi/ANALYSIS-2026-11-12.md` (§3), written by WSL A from memory. **Checked by**
the cloud modeller, with web searches (standard mode), on 2026-11-12. **Not** an independent referee check.

**Evidence levels, as elsewhere in the track:**
- **F:** full text read;
- **A:** abstract or publisher page;
- **S:** search-result summary or secondary description only.

**Nothing here is F.** Two full texts could not be fetched because their hosts are not allowed in the cloud
session's network: `comptes-rendus.academie-sciences.fr` and `lamcos.insa-lyon.fr`. Reading them needs either
those hosts allowed, or WSL B (standing fetch rule).

**Blind list:** coldspray-blind-literature.md contains no TLSPH paper and no SPH-method paper (grep for "Lagrangian",
"SPH", "Vignjevic", "Ganzenm"). Nothing here is restricted.

## Claims

| # | Claim in the analysis | Finding | Level | Sources |
|---|---|---|---|---|
| 1 | TLSPH removes the tensile instability by construction | **Confirmed, with a qualifier:** the instability is avoided when kernels are evaluated in the initial (reference) configuration. Bonet & Kulasegaram report that a Lagrangian formulation removes it, while zero-energy modes remain. The Vignjevic, Reveles & Campbell 2006 abstract claims first-order consistency and relief of kernel-support deficiency at surfaces | S (A for the 2006 abstract) | Vignjevic, Reveles & Campbell, "SPH in a Total Lagrangian Formalism", CMES 14(3) 181–198 (2006), doi:10.3970/cmes.2006.014.181; Reveles PhD thesis, Cranfield 2007 |
| 2 | TLSPH needs its own control of zero-energy (hourglass) modes | **Confirmed.** Ganzenmüller 2015 gives a penalty-type hourglass control for TLSPH (amplitude α). A 2016 companion paper reports that it also removes tensile instability. Later reviews call the zero-energy modes the persistent problem of TLSPH | S (A for 2015) | Ganzenmüller, CMAME 2015, doi:10.1016/j.cma.2014.12.005, arXiv:1410.7221; EPJ ST 2016 |
| 3 | At cold-spray strains the reference configuration must be updated, which brings part of the problem back | **Confirmed.** Original TLSPH cannot handle large shear and distortion. Updating the reference configuration tends to activate zero-energy modes, and an updated (current-configuration) kernel brings the tensile instability back. Proposed remedies: updated-reference Lagrangian formulations (Gil, Lee and co-workers 2022; de Campos), and a stabilised TLSPH with configuration update (arXiv:1907.06990). **No standard scheme found** | S | arXiv:1907.06990; Gil/Lee et al., CMAME 2022 (not opened); de Campos thesis (Swansea; not opened) |
| 4 | Contact between TLSPH bodies needs a separate contact law, because bodies do not interact through the kernel | **Confirmed for LAMMPS SMD/MACHDYN:** `smd/tlsph` allows no cross-type interaction; contact between bodies goes through `smd/hertz` (particle overlap with a contact radius, stiffness about half of E) or `smd/tri_surface` (rigid triangulated walls). This is the same structure as our hvi contact. **For us:** the hvi contact and bond laws can in principle be carried over | S (documentation) | LAMMPS docs `pair_style smd/tlsph`, `smd/hertz`, `smd/tri_surface` |
| 5 | (not in the analysis) TLSPH has already been applied to cold spray | **Found, and important; now read at F level by WSL A** ([data/profizi2016_reading.md](data/profizi2016_reading.md)). Corrections from the full text: no hourglass control, no reference update, pinball contact with Lagrange multipliers between SPH bodies, an energy-limited cohesive pair law with a yield-drop activation criterion; no test against an exact reference; cold-spray runs at R/5; finer meshes failed at 600–900 m/s, and the author recommends updated Lagrangian (thesis p. 70, p. 87). Search-level summary, as first recorded: Profizi, Combescure & Ogawa (2016) model adhesion in fast-dynamics SPH, applied to an Al particle on an Al substrate. They correct the tensile instability by "an appropriate renormalization of the kernel functions, a total Lagrangian formulation of the solid mechanics equations and some artificial stabilization", and study cohesive-zone interaction laws (Dugdale in a 2015 conference paper). Profizi's PhD thesis (INSA Lyon 2016): *Development of a Numerical Model of Single Particle Impact with Adhesion* | S | Profizi, Combescure, Ogawa, C. R. Mécanique 344(4-5) 211–224 (2016), doi:10.1016/j.crme.2016.02.001; Profizi thesis, INSA Lyon 2016 (both not opened: hosts blocked) |
| 6 | Eulerian FE / CEL is the usual cold-spray choice; two materials in one cell are bonded by construction | **Partly confirmed:** CEL is widely used and called more robust at high deformation (INSA Lyon thesis 2014; Materials & Design 2022: Lagrangian for single, CEL for multi-particle). Some CEL studies add a cohesive zone at the particle–substrate interface. One review says Lagrangian FE stays the most popular where bonding and interface tracking matter. **Not found:** a source that states the bonded-in-mixed-cells limitation directly; it remains our inference | S | INSA Lyon thesis 2014 (873); Materials & Design 2022; CEL multi-particle 2024 (journal.mmi.kpi.ua); ECCOMAS 2024 |
| 7 | (not in the analysis) Peridynamics is used for cold spray with oxide | **Found:** "Effect of particle oxidation, size and material on deformation, bonding and deposition during cold spray: a peridynamic investigation", arXiv:2403.01311. It is relevant to the oxide/interface agenda (CS-12) and is an alternative host. Not opened | S | arXiv:2403.01311 |

## What this changes

1. **CS-18 is at best a "variant of Profizi et al. 2016".** They already combine TLSPH (with renormalisation and
   stabilisation) with an adhesion model for Al-on-Al cold spray. The pairing of TLSPH and an SPH adhesion model is
   not ours. What could differ: a Bay-type activation (CS-12) in place of a cohesive zone, verification against
   exact references, and the frozen ladder.
   - **It is also probably related to "Pontabry et al. 2016"** in our external literature report (an SPH adhesion
     model in a cold-spray context, IOP conference). It may be the same group. Not verified.
2. **Read Profizi 2016 and the thesis before any TLSPH code** (F level). They answer, from experience:
   - which renormalisation and stabilisation they use;
   - whether they update the reference configuration at jetting strains, and how;
   - how contact between bodies is done;
   - what verification they show.

   Route: allow the two hosts in the environment, or WSL B fetches them.
3. **The reference-update problem (claim 3) is the main technical risk** for cold spray. The ladder must test it
   directly (rung T-large-strain). A TLSPH that never updates will fail at jetting strains, and one that updates
   reintroduces the modes it was chosen to avoid.
4. **Hourglass control is not optional** (claim 2). The ladder needs a zero-energy rung, and the set-up must fix the
   hourglass coefficient before the freeze.
5. **LAMMPS SMD/MACHDYN is an existing open TLSPH implementation with body-to-body contact** (claim 4). It is a
   possible independent cross-check code for the host rungs. It is GPL, separate from the fork, and not examined.

Sources: [Vignjevic et al. 2006](https://www.techscience.com/doi/10.3970/cmes.2006.014.181.html) ·
[Reveles thesis 2007](https://dspace.lib.cranfield.ac.uk/bitstream/1826/3916/1/Reveles-Thesis_2007.pdf) ·
[Ganzenmüller 2015 (arXiv)](https://ar5iv.labs.arxiv.org/html/1410.7221) ·
[EPJ ST 2016](https://epjst.epj.org/articles/epjst/abs/2016/02/epjst162016/epjst162016.html) ·
[stabilised TLSPH, arXiv:1907.06990](https://arxiv.org/pdf/1907.06990) ·
[updated Lagrangian SPH, arXiv:2409.11474](https://arxiv.org/html/2409.11474v1) ·
[LAMMPS smd/hertz](https://docs.lammps.org/pair_smd_hertz.html) ·
[LAMMPS smd/tlsph](https://guriang.unpad.ac.id/lammpsdoc/pair_smd_tlsph.html) ·
[Profizi et al. 2016](https://comptes-rendus.academie-sciences.fr/mecanique/articles/10.1016/j.crme.2016.02.001/) ·
[Profizi thesis 2016](https://lamcos.insa-lyon.fr/files/theses/1123-thesepdf.pdf) ·
[INSA Lyon thesis 2014](https://lamcos.insa-lyon.fr/files/theses/873-thesepdf.pdf) ·
[CEL multi-particle 2024](https://journal.mmi.kpi.ua/article/view/295144) ·
[peridynamics cold spray, arXiv:2403.01311](https://arxiv.org/pdf/2403.01311)
