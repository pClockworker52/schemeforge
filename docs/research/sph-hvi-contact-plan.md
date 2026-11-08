<!-- Approved by Peter 2026-11-08. Copy of the plan for the private fork repo sph-hvi-contact (place it there as hvi/PLAN.md). The frozen judge is docs/research/sph-contact-ladder.md in schemeforge. -->

# sph-hvi-contact: plan, milestone 1

**Repo:** `sph-hvi-contact` (private). Description: *SPH–SPH contact and bonding interface for high-velocity impact
(cold spray). Fork of OpenCourant (AGPL-3.0).*
**Who:** Peter's local WSL session executes Part A. The schemeforge cloud session does Part B.
**Decided (Peter, 2026-11-08):**
- no-fork is dropped;
- the contact lives in a separate private repo;
- it is configured through a sidecar file, and the Siemens-licensed files stay byte-identical;
- milestone 1 contains contact, cohesive bond and Bay activation in the solver.

## Context

Every interface route we tried in OpenCourant fails for a known reason (schemeforge
`docs/research/opencourant-verification.md`):
- **SPH–SPH is welded through the kernel.** There is no part filter in the neighbour search or in `spforcp.F`
  (§9.2 item 4). In the two-column test the striker is pulled back to −0.93 V where the exact answer is 0 (§9.8).
- **W0 fails.** The contact is 19–37 % too stiff, and its result depends on where the sphere starts (§10.3).
- **SPH on TYPE7 bricks** never bonds, and the edge bricks collapse at 0.07–0.17 D/V, earlier as the mesh is refined
  (§10.5, §13).

The interface law of CS-12 (Bay: surface expansion Y, threshold Y', extrusion pressure p_E) needs a host in which:
1. the two bodies are separate until a criterion says otherwise;
2. Y and p_n at the interface are defined.

Milestone 1 builds that host and verifies it against exact references. It makes **no physics claim**: v_cr, Y' or
p_E for real materials come later, under a registered schemeforge hunch (CS-15).

**Labels** (iron rule 6: rediscovery / variant of X / plausibly new; only the referee assigns "plausibly new"):
- Each component gets its own label.
- Starting point for the referee: Campbell/Vignjevic/Libersky-type SPH contact (from memory, not checked),
  Pontabry 2016 (switch to a cohesive law on activation), Kebriaei 2014 (Bay's law in an interface element).
- Any fix we have to invent for stability, accuracy or speed is logged in `hvi/CHANGELOG.md` with the problem it
  solves and a literature check. Those fixes are the candidates for "plausibly new", assigned by the referee.

---

## Part A: the fork repo (local WSL session)

### A0. Set-up and baseline (no code change)

1. **Location:** the WSL Linux filesystem, `~/sph-hvi-contact`, not `/mnt/c/...`. A Fortran build over the Windows
   mount is several times slower, and file modes and case sensitivity break. From Windows it is reachable at
   `\\wsl$\<distro>\home\<user>\sph-hvi-contact`. Create the private repo `sph-hvi-contact` from the OpenCourant source at the commit behind release
   `latest-20261011`. Record its SHA in `hvi/README.md`. Keep `LICENSE` (AGPL-3.0) and the upstream copyright files
   unchanged.
2. Add an `hvi/` tree:
   - `README.md` (purpose, labels, licence note);
   - `SPEC.md`;
   - `CODEMAP.md`;
   - `CHANGELOG.md`;
   - `decks/`, `scripts/`, `results/`.
3. **Baseline:** build from source (CMake, OpenMP, the same compiler as the release). Then check:
   - the shipped smoke deck reproduces the reference energies exactly;
   - our existing SPH rungs, rerun with decks from schemeforge's `docs/research/opencourant/scripts/`
     (`sphdeck.py`, `sph_rung0.py`, `sph_rung0p.py`, `sph_rung1.py`, `sph_twopart.py`, `sph_f0w0.py`), reproduce
     `results/sph_s0.csv`, `sph_s0p.csv`, `sph_s1.csv`, `sph_twopart.csv`, `cs11_f0w0.csv` to 4 digits.

   If the baseline fails, stop and report. Every later comparison is against this build.
4. **Guard for the Siemens files:** add a script `hvi/scripts/check_untouched.sh` that diffs `hm_reader`,
   `hm_cfg_files`, H3D and the starter reader tree against the base SHA. Run it before every commit; it must print
   nothing.

### A1. Code reading → `hvi/CODEMAP.md` (before any edit)

Map every loop that sums over SPH neighbours, with file and line. Known starting points:
- `engine/.../elements/sph/sphprep.F` (neighbour sort, bucket search);
- `spforcp.F` (forces);
- `spmall3.F` (failure and `KXSP(2,·)`);
- `spsym.F` (symmetry ghosts);
- starter `spinih.F` (h).

Find:
- density and continuity;
- artificial viscosity;
- the ξ tensile correction;
- kernel correction;
- conservative smoothing;
- `/SPHBCS` ghosts;
- the time-step routine;
- the time-history and animation output;
- where the SPH particle's part id is stored at engine level;
- how OpenMP splits the loops;
- how MPI exchanges SPH neighbours (SPMD).

Output: a table of each loop, what it computes, and whether it needs the body filter.

### A2. Design (`hvi/SPEC.md`, committed before the code)

**Sidecar** `hvi_contact.inp`:
- Found through env var `HVI_CONTACT_FILE`, else `<deck>_hvi.inp` next to the deck.
- Read once by new engine code. Plain `key = value` lines, with comments; any unknown key is a fatal error.
- No sidecar means the code paths are untouched (rung A-0 checks bit identity).

```
bodies          = 1:part 1 ; 2:part 2 3          # SPH part ids per body
contact.dc      = 1.0     # contact distance / s (particle spheres touch)
contact.stfac   = 10      # penalty stiffness k = stfac * B * s (as TYPE7 F0)
contact.damp    = 0.05    # fraction of critical
surface.normal  = colour  # colour-function gradient | analytic (rungs only)
bond.model      = none    # none | tie | cs12 | bay83
bond.Yp         = ...     # Y'
bond.pE         = ...     # p_E (Pa)   or bond.m with sigma_flow from the material
bond.alpha      = ...     # bay83 only
cohesive.shape  = bilinear
cohesive.Gc     = ...     # J/m^2   (or cohesive.delta_c)
out.interval    = ...     # s
out.file        = hvi_interface.bin
```

**Mechanics:**
1. **Body filter.**
   - Kernel sums (A1 list) include only pairs from the same body.
   - Cross-body pairs within a distance of 2h go into a separate candidate list. One bucket search is kept; the pair
     is tagged.
   - Symmetry ghosts inherit their parent's body id and surface state.
2. **Contact (frictionless).**
   - Between the surface particles i ∈ body 1 and j ∈ body 2, the gap is g = |x_i − x_j| − d_c·s.
   - The normal is the average of the two bodies' outward normals (colour gradient within each body).
   - Force: F = k⟨−g⟩ n, plus damping, repulsive only. Equal and opposite, so momentum is exact.
   - The stable time step dt ≤ C·√(m/k) enters the global dt.
   - Contact energy and damping work are accumulated.
3. **Surface particles and Y.**
   - A particle is a surface particle if its colour-gradient magnitude exceeds a threshold at t = 0. The initial
     normal N₀ is stored.
   - The deformation gradient is integrated per particle: Ḟ = L F, with the same velocity gradient L as the
     solver.
   - Area ratio A/A₀ = J |F⁻ᵀN₀|. Then **Y = (A − A₀)/A** (Bay's definition, as in CS-12).
   - p_n = (normal contact force) / A, with A = s²·A/A₀.
   - Slip is the accumulated tangential relative displacement of the pair. T is the particle's LAW4 temperature.
4. **Bond.** The state is per pair (i, j), stored on the body-1 particle. Pairs survive re-sorting by partner id.
   - `tie`: the pair bonds on first contact. Used for rungs only.
   - `cs12`: bonds when Y > Y' and p_n > p_E (both particles' Y; use the minimum). Bonded share
     f = (Y − Y')/(1 − Y'). Strength σ_B = f·σ_flow, capped at σ_flow.
   - `bay83`: σ_B = α⟨(Y − Y')/(1 − Y')⟩ p + (1 − α) Y ⟨p − p_E⟩ (as reported via Kebriaei 2014; check the primary
     before coding, step A4.0). σ_B accumulates as the maximum over the history and is capped at σ_flow.
   - **Bonded pair:** a bilinear traction–separation law in the normal and tangential directions. Peak traction is
     σ_B·A. Energy is G_c·A, or δ_c. Damage is irreversible. At full damage the pair returns to frictionless
     contact. Dissipated energy is accumulated.
5. **Output.**
   - Per surface particle, every `out.interval`: id, body, x, Y, p_n, slip, T, bond state, σ_B, damage.
   - Global: contact energy, cohesive dissipation, bonded area.
   - Written as little-endian binary with a header, plus a Python reader in `hvi/scripts/read_interface.py`.
6. **Not supported in M1, fatal error if requested:**
   - MPI ranks > 1 with hvi active (OpenMP only; §9.3 shows threads ≈ MPI);
   - restart;
   - friction;
   - more than 2 bodies;
   - SPH–FE contact changes (TYPE7 untouched).

### A3. Implementation order (small commits; core rung after each, the rest deferred)

New engine files: `hvi_mod.F90` (state, sidecar reader), `hvi_contact.F90`, `hvi_surface.F90` (normals, F, Y),
`hvi_bond.F90`, `hvi_out.F90`. Minimal hooks go into the A1 loops.

1. Sidecar reader and body ids, then the body filter. Core: A-0, A-2.
2. Contact. Core: B-1, B-2, B-3. Then **E-1** (performance pass, A4b).
3. Surface, F and Y. Core: C-1.
4. Tie and cohesive. Core: D-2.
5. cs12 and bay83 activation. Core: D-3. Then **E-2**.

Run `check_untouched.sh` before every commit. **Weighting (Peter):** about 80 % of the effort goes to building the
contact and finding out how it performs on real impacts, about 20 % to verification. The full ladder is completed
only before a result is used for any claim.

### A4. Verification ladder

Exact references wherever one exists. The thresholds are proposed; schemeforge freezes them (B2) before any rung
run. Default set-up: §9.1 settings (cubic net, h = 2^(1/6) s, default q, ξ = 0, dt scale 0.3).

**A4.0 (before D3):** record the Bay/Kebriaei equations in SPEC.md with page references, read from the primary
(Kebriaei 2014 interface paper; Bay 1983 from Peter). Code the form actually printed.

**A: regression**

| Rung | Case | Reference | Pass |
|---|---|---|---|
| A-0 | no sidecar: S0, S0p, S1, twopart | baseline build | bit-identical output |
| A-1 | sidecar with 1 body: S0, S0p, S1 | baseline | ≤ 0.1 % in all rung metrics |
| A-2 | 2 bodies, 10 s apart, opposite velocities, no contact | free flight | velocities exact to 1e-12 relative, no cross force |

**B: contact**

| Rung | Case | Reference | Pass |
|---|---|---|---|
| B-1 | two-column striker/target (§9.8 deck, 50 particles/L) | exact 1D: striker at rest from 2L/c_d; target near end at rest to 4L/c_d, then V; target mean V/2 | striker \|v\|/V ≤ 0.05 for t ≥ 1.1·2L/c_d; target mean within 0.05 V of 0.5 V; interface tension never > 1 % of ρc_dV |
| B-2 | Hertz sphere on SPH block (W0 set-up), R/16, R/32 | two-body Hertz | at R/32 peak and approach within 5 %, rebound > 0.9 V (the F0 thresholds) |
| B-3 | B-2, started at s and at 2.4 s | itself | metrics differ ≤ 1 % (W0 defect gone) |
| B-4 | two equal spheres, head-on | two-body Hertz | as B-2 |
| B-5 | block sliding on block under light normal load | frictionless: tangential momentum per body conserved | ≤ 1 % change |
| B-6 | B-2 quarter vs half model | itself | ≤ 0.5 % (as §9.7) |
| B-7 | B-2 at 1 vs 8 threads | itself | ≤ 0.1 % |
| B-8 | energy in elastic B-2 | KE + contact + strain energy | total drift ≤ 2 % to end of rebound |

**C: surface expansion**

| Rung | Case | Reference | Pass |
|---|---|---|---|
| C-1 | block under prescribed homogeneous equi-biaxial stretch λ (boundary velocities) | Y = 1 − 1/λ² on the free face | ≤ 1 % at λ = 1.5, 2 |
| C-2 | rigid rotation of a block, 90° | Y = 0 | \|Y\| ≤ 1e-3 |
| C-3 | sphere normals at t = 0 (colour) | analytic radial normal | angle ≤ 5° at R/32 |

**D: bond**

| Rung | Case | Reference | Pass |
|---|---|---|---|
| D-1 | B-1 with `tie`, σ_B above the tension amplitude | exact 1D joined bar (one column of length 3L) | striker and target velocities within 0.05 V of exact |
| D-2 | B-1 with `tie`, σ_B below the tension amplitude | exact: separation when the interface stress reaches σ_B | separation time within 5 %; dissipated energy = G_c·A within 5 % |
| D-3 | two blocks pressed (p > p_E), then stretched equi-biaxially to Y > Y' (prescribed), then pulled apart | σ_B from the closed form on the exact Y(t), p(t) | pull-off traction within 2 % (cs12 and bay83) |
| D-4 | D-3 with Y < Y', and separately p < p_E | no bond (cs12); bay83 term-wise | zero bond strength / correct term |
| D-5 | D-3 at dt scale 0.3 and 0.15, s and s/2 | itself | ≤ 2 % |

**Core rungs** (run during M1): A-0, A-2, B-1, B-2, B-3, C-1, D-2, D-3. **Deferred** (the full ladder, before any
claim): A-1, B-4 to B-8, C-2, C-3, D-1, D-4, D-5.

### A4b. Performance pass (exploratory, no claims)

- **E-1, after B-3:** Al–Al quarter-symmetry impact with contact only (`bond.model = none`), at 500 / 800 /
  1100 m/s and R/16, R/24 (R/32 if affordable). Record:
  - whether the run survives past the kinematic switch (0.002–0.019 D/V) and how far beyond it;
  - the time step and cost per particle-cycle compared with §9.3;
  - instabilities (tensile instability at the interface, particle interpenetration, pairing noise);
  - the interface histories Y, p_n and slip at the edge, and whether they change with spacing.
- **E-2, after D-3:** the same runs with `tie` and with `cs12` at placeholder Y' and p_E, chosen to show the
  mechanics (bonded ring, debonding during rebound), not fitted.
- **Labels:** every E result is labelled exploratory. No v_cr is read from it (schemeforge rule: no simulated v_cr
  before the ladder and convergence). It goes to schemeforge as solver diagnostics, like §10.5.
- **Problems found here** (stability, speed, edge) drive the next design iteration. Each fix gets a CHANGELOG entry
  with a literature check (see Labels).

**M1 ends when the core rungs pass and E-1 and E-2 are reported.** Results go in `hvi/results/*.csv` (one row per run: fork SHA, deck hash, metrics) and a
summary in `hvi/VERIFY-RESULTS.md`. Any failing rung: stop, record it, report to schemeforge. Do not tune and rerun
silently.

### A5. Not in M1

- any impact run used for a claim (E runs are diagnostics only);
- fitted Y', p_E;
- friction;
- MPI;
- restart;
- the oxide-interphase option.

The first impact diagnostic needs a schemeforge hunch (CS-15) frozen first: law, parameters, fitting rule, kill
rule.

---

## Part B: schemeforge (cloud session, after Peter approves this plan)

1. **DECISIONS entry**, 2026-11-08 "No-fork dropped; SPH–SPH contact fork `sph-hvi-contact` (Peter)". It reverses
   the 2026-11-04 no-fork clause, and records the separate private repo, the sidecar route, M1 scope, and the
   licence rationale. Regenerate the index (`python scripts/decisions_index.py`).
2. **Freeze the ladder:** `docs/research/sph-contact-ladder.md` holds the A4 tables as the judge for the fork. It
   is committed before any rung run, and the fork cites its commit.
3. **Bookkeeping:**
   - `docs/research/tasks/wsl-a.md`: a task pointing to the fork and this plan;
   - an H8 note in coldspray-go-nogo.md (route reopened);
   - a STATUS line;
   - HANDOFF at session end.
4. **Results path:** WSL A pushes rung results to `coldspray/opencourant-sph` as CSV plus the fork SHA. The cloud
   session merges them and records verdicts against the frozen ladder.

## Verification of this plan's execution

- `hvi/scripts/check_untouched.sh` prints nothing at every commit.
- The A-0 baseline reproduces the existing schemeforge CSVs (A0.3).
- Each rung row in `hvi/results/` carries the fork SHA and is compared with the frozen ladder by a script in
  `hvi/scripts/` (one verdict line per rung).
- schemeforge: `pytest -q` and `ruff check .` stay green on the doc and task commits.
