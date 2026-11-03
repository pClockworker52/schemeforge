# Prompt for the OpenRadioss setup session (WSL)

Give the text below to an agent session on Peter's WSL machine. DECISIONS 2026-11-03 "Cold-spray track: local
first": OpenRadioss is the main impact solver; a small JAX code (src/schemeforge/research/impact_axisym.py) is the
independent cross-check.

---

You are setting up **OpenRadioss** for the cold-spray simulation track of the schemeforge repository
(`~/schemeforge` or wherever Peter's clone lives; read `CLAUDE.md` and `docs/research/coldspray-go-nogo.md`,
section "Local-first order", first). Goal of this session: a verified, reproducible OpenRadioss installation and
one smoke run. Not in scope: any cold-spray result, any critical velocity, any change to the models or data in
`docs/research/`.

1. **Verify the facts before acting.** From the official OpenRadioss sources (GitHub `OpenRadioss/OpenRadioss`,
   openradioss.org documentation), confirm and write down:
   - licence (expected AGPL-3.0; confirm), latest release tag and date;
   - supported Linux platforms and prerequisites;
   - how to install: a prebuilt Linux release or a build from source;
   - which features exist for: explicit dynamics, Johnson–Cook plasticity, Mie–Grüneisen equation of state,
     ALE and/or SPH, contact, thermal coupling (adiabatic heating), and axisymmetric 2D analysis.
   
   Do not rely on memory for any of these; cite the page or file for each.
2. **Install** under `~/opt/openradioss/<release-tag>` (no system-wide changes without asking Peter). Prefer the
   official prebuilt release; build from source only if no Linux binary exists. Record exact commands, compiler
   and MPI versions, and the binary paths (starter and engine).
3. **Smoke test:** run one example or QA deck shipped with OpenRadioss that uses Johnson–Cook (or, failing that,
   any explicit elastic-plastic impact example). Check that it completes, and note run time, core count and
   output files. Convert results with the shipped tools if needed (e.g. anim/th to VTK or CSV), and record how.
4. **Write `docs/research/openradioss-setup.md`** with the verified facts (with sources), the install
   commands, versions, the smoke-test deck, its run time and outputs, and anything that did not work. Add a
   short "what we still need to check" list: axisymmetric support, a rigid-wall contact option, element types
   suitable for extreme distortion at the jet, the mesh-convergence options, and how to script parameter sweeps
   (impact velocity) from Python.
5. **Git:** work on a new branch `coldspray/openradioss-setup` from `claude/exciting-fermi-qy077p`. Commit only
   `docs/research/openradioss-setup.md` (and, if small and licence-compatible, the smoke-test input deck under
   `docs/research/openradioss/`). Never commit binaries or large result files. Push the branch and stop.

Stop and ask Peter before: installing system packages with sudo, downloading more than ~2 GB, or changing any
file outside the new doc and the optional deck folder.
