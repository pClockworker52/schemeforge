# Prompt: literature search for the interface agenda (CS-12, CS-13, CS-10 referee input)

For a separate session (cloud or WSL), not the modelling session. Written 2026-11-05. Paste everything below the
line.

---

You are doing a literature search for the schemeforge cold-spray research track. Repository: pClockworker52/schemeforge.
Work on a new branch `coldspray/lit-interface`, created from `claude/exciting-fermi-qy077p`. Write one note,
`docs/research/coldspray-literature-interface.md`, and push it. Do not edit any other file.

## Read first (in the repository)

- docs/research/coldspray-hunch-cs12.md: bonding as local dissolution of the interface "blanket"; criterion =
  surface expansion Y above a threshold Y' plus an extrusion pressure (cold pressure welding).
- docs/research/coldspray-hunch-cs13.md: heat conduction as the length scale that regularises the contact edge in
  impact simulations.
- docs/research/coldspray-hunch-cs10.md: closed-form strength + oxide energy balance.
- docs/research/coldspray-data-and-zoo.md: source register and evidence levels (F, A, S, M). Use the same levels and
  the same source-key style.
- docs/research/coldspray-blind-literature.md: **the blind list. Its rules bind you.**

## Hard rules (blind-test protection)

1. **Do not open any paper on the blind list** (B01–B16, by DOI or title), not even its abstract. Also do not open
   the "Model and simulation papers, unread" listed there (Palodhi 2020, Wiehler 2024, Moonga 2024, Hirmand 2024,
   Suresh 2020, Zhang 2025, Sandhu 2026). Crossref metadata (title, venue, year, DOI) is allowed.
2. **Do not report measured critical velocities, and do not report them as differences or ratios either.** That
   covers any paper. If a paper you read quotes a value from a blind-list paper, write only "quotes B0x" and log it
   under "Exposures".
3. **Oxide series are protected.** If you find a measurement of single-particle v_cr (or bonding) against oxide
   thickness or oxide type, report **only** the citation, the material, the number of states and the thickness
   range. Do not report the outcome, the direction, or what the authors conclude about it. These papers may become
   a new blind list (rule B5).
4. **The same applies to bonded-area, oxide-residue or bonded-fraction maps:** citation, material, method, number
   of conditions only, no outcome. CS-12's test T1 is scored on such data.
5. **No values from memory.** Every claim cites a source with its evidence level. A claim you could not check is
   marked S or M, or left out.
6. Never call anything novel. If a source already contains a CS-hunch's idea, say so plainly. That is the most
   useful thing you can find.

## Questions, in priority order

**Q1. Prior art for CS-12 (the core question).**
- Bay's theory of cold pressure welding: the surface-expansion threshold Y', extrusion through cover-layer cracks,
  bond strength against (Y − Y')/(1 − Y'). Give the original papers and their exact formulas. Does Y' depend on the
  thickness of the cover layer, or only on its type and preparation?
- Has a surface-expansion, interfacial-stretch or oxide-break-up criterion been used for cold-spray bonding
  (single impact or coating)? List every paper, with its criterion, its parameters and how it was validated.
- Cold-spray or impact-welding simulations whose interface switches from contact to tied (or cohesive) by a
  criterion. Which solver, which criterion, was the switch verified?
- Has anyone described an interface in materials or contact mechanics as a Markov blanket, or stated a
  conditional-independence (sufficient-statistic) principle for interface states? A short answer is enough.

**Q2. Prior art for CS-13.**
- Thermal (conduction) and viscous regularisation of adiabatic shear bands in finite-element simulations: key
  papers, the length scale they give, how they show convergence.
- Cold-spray impact simulations (Lagrangian, ALE, CEL, Eulerian, SPH) that include heat conduction. Did any test
  mesh convergence at the contact edge with and without conduction? What did they find?
- The thermal-diffusion explanation of the LIPIT size effect (HG2018a and later), and any test of it.

**Q3. Explosive-welding lens.**
- Weldability windows from collision-point kinematics (Walsh, Cowan, Deribas, later reviews): the criteria as
  formulas. Has anyone applied them to a sphere impact or to cold spray, including a prediction of a bonded ring
  with an unbonded centre?

**Q4. Rebound as a measure of interface work.**
- Papers that extract adhesion or interface energy from LIPIT or other restitution data below v_cr. Is raw
  restitution data openly available (supplementary files, repositories)? Give the citation and the data location,
  not the values.

**Q5. Referee input for CS-10.**
- Na et al. 2025 (J. Mater. Res. Technol. 36, B10) is unblinded and may be read in full. Report its Eq. 6 exactly
  (the combined strength + oxide model, described as a Lienhard rule of mixtures), its fitted constant, and the
  Lienhard reference it builds on. Compare its form with CS-10's form in one paragraph, without judging which is
  better.

**Q6. Input for CS-13 (only if quick).**
- Primary or authoritative sources for the thermal conductivity of pure Al and of Al 6061, 2024 and 7075, near
  room temperature. Give the source and the value as printed, with its condition (temper, temperature). Do not
  edit properties.csv; the WSL session enters the values.

## Output

`docs/research/coldspray-literature-interface.md`, with these sections:
1. **Summary:** for each of CS-12, CS-13 and the explosive-welding lens, one paragraph: does prior art contain the
   idea, partly or fully? Name the closest relative.
2. **Q1 to Q6:** one subsection each. Every row gives source key, full citation, DOI, evidence level, and what was
   checked.
3. **Protected data found:** oxide series and bonded-area maps, as citation, material, states, method only.
4. **Exposures:** anything from a blind-list paper that reached you indirectly, and where.
5. **Register:** new source keys in the style of coldspray-data-and-zoo.md.

Commit with a clear message and push to `coldspray/lit-interface`. Report what you could not access (publisher
blocks), so Peter can supply PDFs.
