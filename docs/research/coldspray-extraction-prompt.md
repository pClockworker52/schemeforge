# Prompt for the input-extraction agent (literature-blind step 1)

Give the text below to a separate agent session (for example a second WSL session). It must not be run by the
session that builds the models. Rule B2 of [coldspray-blind-literature.md](coldspray-blind-literature.md).

---

You are the **input extractor** for a blind test in the schemeforge repository (`docs/research/`). Another agent
will predict critical adhesion velocities for experiments described in a set of papers, **without** having seen
the papers' results. Your job is to hand that agent the experimental **inputs** and nothing that reveals the
**outcomes**. If you leak an outcome, the test for that paper is spoiled.

**Papers:** the 16 rows B01–B16 in `docs/research/coldspray-blind-literature.md` (DOIs given there). Get each
paper from OSTI (Schuh-group accepted manuscripts are often there), from the publisher if it is open access
(J. Mater. Res. Technol., Results in Surfaces and Interfaces), or from Peter. Note the access route per paper.

**For every distinct experimental condition** in a paper (one particle material, substrate, preparation and
temperature combination for which the paper reports impact experiments), write one row to
`docs/research/data/blind_inputs.csv` with these columns:

`cond_id` (B01-c1, B01-c2, …), `doi`, `particle` (material, alloy, temper), `substrate` (material, alloy, temper),
`particle_condition` (powder production route, heat treatment, storage), `substrate_condition` (polishing,
roughness Ra/Rz, hardness), `oxide_state` (oxide/hydroxide thickness or type, oxygen content, as reported),
`d_um` and `d_um_spread` (particle diameter used in the impact experiments), `T_particle_K`, `T_substrate_K`,
`impact_angle_deg`, `properties_reported` (any density, moduli, hardness, yield or tensile strength, failure
strain, grain size the paper reports for these materials, with units and where in the paper),
`apparatus` (LIPIT / gas gun / wipe test / other), `measures_vcr` (yes / no / unclear: does the paper report a
critical adhesion or bonding velocity for this condition?), `source_location` (section, table or page of
each input), `access`, `notes`.

**Never write, say, paraphrase or hint at any of the following**, in the CSV, in commit messages, in any file, or
in your messages:
- critical, adhesion, bonding, erosion or threshold velocities, or their ranges or uncertainties;
- impact or rebound velocities of individual particles, coefficients of restitution, or whether particles bonded
  or rebounded at any velocity;
- the range of impact velocities tested, or the number of impacts (both can hint at the answer);
- comparisons such as "higher than", "lower than", "shifted", "reduced", or any qualitative result about bonding;
- figure captions or text that contain such information.
- **anything observed at the particle–substrate interface after impact** (added 2026-11-05 for CS-12 and CS-14):
  oxide fracture mode (cracking, fragmentation, delamination, ductile thinning), fragment size, spacing or
  geometry, oxide left in the contact or in the jet, bonded-area, bonded-fraction or oxide-residue maps, and
  interface micrographs (FIB, TEM, lift-off). The **initial** oxide state of the powder and the substrate (thickness,
  structure, composition before impact) remains an input and should be extracted.

If an input can only be stated together with an outcome (for example a table mixing both), leave the input blank
and write `withheld: mixed with outcome` in `notes`. If a paper has no metal-on-metal single-particle impact
experiments, give it one row with `measures_vcr = no` and nothing else. Do not explain why.

**Rules for you:**
- Do not edit any other file in the repository.
- Work on a new branch `coldspray/blind-inputs` from `claude/exciting-fermi-qy077p`. Commit only
  `docs/research/data/blind_inputs.csv`, push that branch, and stop. Do not merge.
- Keep a private scratch file outside the repository if you need one, and delete it when you finish.
- Your final message to Peter: the number of papers processed, the number of condition rows, the papers you
  could not access, and nothing about results.
