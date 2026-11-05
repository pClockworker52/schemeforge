# Prompt: literature search for the interface agenda, for an external AI (no repository access)

Self-contained version of [coldspray-literature-prompt-2026-11.md](coldspray-literature-prompt-2026-11.md),
written 2026-11-05. Paste everything below the line. **Before the answer reaches the modelling session,** run the
leak-scan at the end of this file on it.

---

I am a researcher working on a mechanistic model of **bonding in cold spray**: metal microparticles (about 10–30 µm)
hit a metal substrate at 300–1200 m/s and either bond or rebound. The quantity of interest is the **critical
velocity v_cr** above which a single particle bonds, as measured one impact at a time with the laser-induced
particle impact test (LIPIT). I need a careful literature search on a few specific ideas. Accuracy matters more than
breadth.

## The ideas to check for prior art

**Idea A: bonding as local "dissolution" of the interface.**
- Before impact, particle and substrate are two systems, and the interface (native oxide plus contact gap) separates
  them. A metallurgical bond is the local disappearance of that interface: the two bodies become one there.
- The claim is that bulk fields affect bonding only through a few interface states: normal pressure, surface
  expansion (stretch) of the interface, slip, temperature, and oxide type. In probabilistic terms, the interface
  acts like a Markov blanket (Pearl's sense, conditional independence), not in the free-energy sense.
- **The local bonding criterion,** borrowed from cold pressure welding (Bay's theory as I remember it): a point on the
  interface bonds if its surface expansion Y = (A − A₀)/A exceeds a threshold Y', and the contact pressure exceeds an
  extrusion pressure of order the flow stress, so that fresh metal is pushed through cracks in the oxide. The bonded
  share of the area is (Y − Y')/(1 − Y').
- **A specific claim:** Y' depends on the oxide **type** (chemistry and structure), not on its **thickness**, as long
  as the oxide layer is continuous.

**Idea B: heat conduction regularises impact simulations at the contact edge.** Lagrangian finite-element impact
simulations of cold spray fail at the contact edge, and they fail earlier as the mesh is refined. The edge plastic
strain does not converge. The claim: this is adiabatic localisation without a physical length scale, as in adiabatic
shear bands. Heat conduction, with the thermal diffusion length √(κt) of order 0.5–1 µm at a few nanoseconds, would
set that length, and the edge fields would converge once the mesh is finer than it.

**Idea C: explosive-welding windows applied to a sphere impact.** In explosive welding, bonding is governed by the
speed and angle of the collision point, not by the impact speed itself. In a sphere impact, the collision point sweeps
outward and slows, so bonding should be possible only where its conditions are inside the welding window. That would
predict a bonded ring with an unbonded centre.

**Idea D: rebound as a measure of interface work.** Below v_cr, the coefficient of restitution falls as the velocity
approaches v_cr. Part of that energy deficit may be interface work, so restitution data could be used to infer an
interface law without simulating the jet.

## Rules: please follow them strictly

These protect data I will use later as an independent test. Breaking them makes that data useless to me.

1. **Do not open, summarise or quote the papers in the "excluded" list below,** not even their abstracts. You may
   name them if another paper cites them. The one exception is Na et al. 2025, which you may read in full.
2. **Do not report any measured critical velocity,** from any paper. That includes differences, ratios, percentages
   and statements such as "v_cr rose by X". If a paper you read quotes a value from an excluded paper, write only
   "quotes [excluded paper]" in an "Exposures" list at the end.
3. **Oxide series are protected.** If you find measurements of single-particle bonding or v_cr against oxide
   thickness or oxide type, report **only** the citation, the material, the number of oxide states and the thickness
   range. Do not report the result, its direction, or the authors' conclusion about it.
4. **Bonded-area maps are protected too.** For maps of bonded area, bonded fraction or oxide residue at the interface
   (FIB sections, lift-off scans, TEM), report only the citation, material, method and number of conditions. Do not
   report the pattern found.
5. **No values from memory, and no invented references.** Give a DOI or a stable link for every source. Mark each
   claim with how you checked it:
   - **F**: you read the full text;
   - **A**: abstract only;
   - **S**: second-hand, cited by another paper or from a search snippet;
   - **M**: title and metadata only.

   If you are unsure a paper exists, leave it out.
6. **Do not judge novelty.** If an idea above already exists in the literature, say so plainly and cite it. That is
   the most useful thing you can tell me.

### Excluded papers (do not open)

| Key | Paper | DOI |
|---|---|---|
| B01 | Lucas 2024, microstructure effects on high-velocity microparticle impacts of copper, Acta Mater. 280 | 10.1016/j.actamat.2024.120329 |
| B02 | Lucas 2025, single particle impact study on substrate strength and ductility, Int. J. Mech. Sci. 303 | 10.1016/j.ijmecsci.2025.110676 |
| B03 | Tiamiyu 2021, site-specific study of jetting, bonding and local deformation, Acta Mater. 202 | 10.1016/j.actamat.2020.10.057 |
| B04 | Lienhard 2022, tin and zinc microparticle impacts above the critical adhesion velocity, Surf. Coat. Technol. 432 | 10.1016/j.surfcoat.2021.128053 |
| B05 | Chen 2022, additional hindrances to metallurgical bonding from impurities, Surf. Coat. Technol. | 10.1016/j.surfcoat.2022.128114 |
| B06 | Wu 2026, mechanisms of oxide layer fracture during microparticle impact bonding, Scripta Mater. | 10.1016/j.scriptamat.2026.117444 |
| B07 | Liu 2025, impact bonding between titanium particle and substrate, Surf. Interfaces | 10.1016/j.surfin.2025.107537 |
| B08 | Chen 2026, substrate surface roughness and single-particle impact, Results Surf. Interfaces | 10.1016/j.rsurfi.2026.100939 |
| B09 | Ağır 2025, single-particle impact of Ti6Al4V and Ti-5553, J. Therm. Spray Technol. | 10.1007/s11666-025-02063-8 |
| B11 | Imbriglio 2019, adhesion strength of titanium particles to alumina substrates, Surf. Coat. Technol. 361 | 10.1016/j.surfcoat.2019.01.071 |
| B12 | Tiamiyu 2020, particle flattening during cold spray: single particle impact tests, Surf. Coat. Technol. | 10.1016/j.surfcoat.2020.126386 |
| B13 | 2024, surface oxide and impact ratio dictate interfacial adhesion of cold spray bulk metallic glass single particles, Surf. Coat. Technol. | 10.1016/j.surfcoat.2024.131057 |
| B14 | Lienhard 2020, surface oxide and hydroxide effects on aluminum microparticle impact bonding, Acta Mater. 197 | 10.1016/j.actamat.2020.07.011 |
| B15 | Khan 2025, eutectic melting of alloy microparticles upon low velocity impact, Scripta Mater. 265 | 10.1016/j.scriptamat.2025.116763 |
| B16 | Kajihara 2024, velocity measurement method for a microparticle projectile and high-speed impact testing, Acta Mater. | 10.1016/j.actamat.2023.119467 |
| X1 | Palodhi 2020, J. Therm. Spray Technol. | 10.1007/s11666-020-01105-7 |
| X2 | Wiehler 2024, J. Therm. Spray Technol. | 10.1007/s11666-024-01892-3 |
| X3 | Moonga 2024, engrXiv | 10.31224/3491 |
| X4 | Hirmand 2024, J. Therm. Spray Technol. | 10.1007/s11666-024-01803-6 |
| X5 | Suresh 2020, Acta Mater. | 10.1016/j.actamat.2019.10.039 |
| X6 | Zhang 2025, J. Therm. Spray Technol. | 10.1007/s11666-025-02097-y |
| X7 | Sandhu 2026, preprint | 10.21203/rs.3.rs-8930301/v1 |

Allowed in full: Na et al. 2025, single particle impact explorations on powder heat treatments, J. Mater. Res.
Technol. 36.

## Questions, in priority order

**Q1, Idea A (most important).**
1. Bay's theory of cold pressure welding: the original papers, and the exact formulas for the threshold Y', the
   extrusion pressure and the bond strength. Does Y' depend on the thickness of the cover layer, or only on its type
   and surface preparation? Cite the passage.
2. Has a surface-expansion, interfacial-stretch or oxide-break-up criterion been used for cold-spray bonding, for
   single impacts or coatings? For each paper: the criterion, its parameters and how it was validated.
3. Cold-spray or impact-welding simulations whose interface switches from sliding contact to tied (or cohesive)
   when a criterion is met. Which solver, which criterion, and was the switch verified?
4. Has anyone described a material interface as a Markov blanket, or stated a conditional-independence
   (sufficient-statistic) principle for interface states? A short answer is enough.

**Q2, Idea B.**
1. Thermal-conduction and viscous regularisation of adiabatic shear bands in finite-element simulations: key
   papers, the length scale they give, and how they show mesh convergence.
2. Cold-spray impact simulations (Lagrangian, ALE, CEL, Eulerian, SPH) that include heat conduction. Did any compare
   mesh convergence at the contact edge with and without conduction? What did they find? (Simulation findings may
   be reported; measured v_cr may not.)
3. The thermal-diffusion explanation of the size dependence of v_cr in LIPIT experiments (Hassani-Gangaraj et al.
   2018, "Adiabatic shear instability is not necessary for adhesion in cold spray", and later work), and whether
   anyone has tested it. Report the mechanism and the tests, not measured velocities.

**Q3, Idea C.** Weldability windows from collision-point kinematics (Walsh, Cowan, Deribas, later reviews), with the
criteria as formulas. Has anyone applied them to a sphere impact or to cold spray, and predicted a bonded ring with
an unbonded centre?

**Q4, Idea D.** Papers that extract adhesion or interface energy from LIPIT or other restitution data below v_cr. Is
raw restitution data openly available (supplementary files, data repositories)? Give the citation and the data
location, not the values.

**Q5, Na et al. 2025** (allowed in full). Report its equation for the combined strength + oxide model, said to be a
rule-of-mixtures form following Lienhard, exactly as printed, with its fitted constant and the reference it builds
on. Then compare it in one paragraph with this form, without judging which is better:
v_cr² = (0.15 c)² + β σ_p/ρ + γ (t_ox/d)/ρ,
where c = √(B/ρ), σ_p is particle strength, t_ox the oxide thickness, d the particle diameter, and β, γ fitted
constants.

## Output

One Markdown document with these sections:
1. **Summary:** one paragraph each for Ideas A, B, C and D. Does prior art contain the idea, partly or fully? Name the
   closest relative.
2. **Q1 to Q5:** one subsection each. Every source with its full citation, DOI or link, evidence level (F/A/S/M) and
   what you checked.
3. **Protected data found:** oxide series and bonded-area maps, as citation, material, number of states and method
   only.
4. **Exposures:** anything from an excluded paper that reached you indirectly, and where.
5. **Not accessible:** papers you could not open (paywall), so that I can obtain them.

---

## Leak-scan before the answer reaches the modelling session (for Peter)

Search the answer for: "m/s", "v_cr", "critical velocity", "%", "increase", "decrease", "higher", "lower", and the
excluded keys B01–B16 and X1–X7. Remove any measured velocity, any outcome of an oxide series or bonded-area map,
and any summary of an excluded paper. Note what was removed, without the values, under "Exposures". Then commit the
cleaned answer as `docs/research/coldspray-literature-interface.md` on branch `coldspray/lit-interface`.
