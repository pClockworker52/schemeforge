# Prompt for output extraction (literature-blind step 3)

Use only for papers whose predictions are frozen and committed (for B10: commit 060fff8,
`docs/research/coldspray-preregistration-b10.md`). Any session may do this, including the modelling session.

---

You are extracting the **measured outcomes** of blind paper **B10** (Na et al. 2025, J. Mater. Res. Technol. 36,
7026, "Single particle impact explorations on the role of powder heat treatments in cold spray"). Predictions are
already frozen (commit 060fff8); do not edit `docs/research/coldspray-preregistration-b10.md`,
`docs/research/data/predictions_b10.csv` or any code.

For each condition B10-c1 … B10-c5 (as in `docs/research/data/blind_inputs.csv`), add one row to
`docs/research/data/vcr_lipit.csv` with id `B-B10-c1` … `B-B10-c5`, using the existing columns:
particle, substrate, conditions, oxide_state (copy from blind_inputs.csv), d_um, T_substrate_K ("room" unless
stated), `vcr_low_mps`, `vcr_high_mps`, `vcr_mid_mps`, `vcr_definition` (exactly how the paper defines the
critical velocity and its range or uncertainty), `n_impacts` if stated, `regime` (co-deformation),
`read_from` (table, figure or page), `primary_source` (Na2025), `extraction` (printed / digitized ±x m/s), `notes`.

Also record, in `notes` of each row, the paper's dynamic yield strength for that condition (it was withheld in
step 1) and anything the paper says about why the conditions differ. If values exist only in a figure, digitize
them and say so. Commit only `docs/research/data/vcr_lipit.csv` on a new branch `coldspray/b10-outcomes` from
`claude/exciting-fermi-qy077p`, push, and stop.
