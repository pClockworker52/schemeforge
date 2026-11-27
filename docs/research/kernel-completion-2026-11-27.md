# Kernel completion across a TLSPH contact: does it remove the face-layer deficit? (spec and prediction, frozen)

**Frozen 2026-11-27, approved by Peter ("Freeze it as drafted"), as drafted in eae3ed5, before any number was
computed.** WSL A task 2026-11-27-b. Drafted 2026-11-27 (cloud, modeller). Peter asked for it (DECISIONS 2026-11-27, "Cold-spray track
unpaused"). `kind = check`; no hunch, no budget. **Stage A only: a static model in Python, no solver run, no build, no
existing solver output read.** A solver stage (B) is outlined at the end. It needs its own frozen spec, after Peter has
reviewed Stage A.

## Why

- **The defect.** When a normal load is applied as point forces on the outermost TL particles, the first two layers
  carry the wrong stress:
  - 0.655 / 0.845 of the traction against a rigid wall (§17.2);
  - 0.619 / 0.856 when one TL column strikes another through the hvi contact (§22 item 2).
- **Its cause is known and static** (SPEC-TL-b §4.2). The TL force sum for a uniform stress does not vanish where the
  kernel is truncated. Each end layer k receives P · B_k, with B_k = Σ_j V_k V_j (K_k + K_j) ∇W_kj. On the cubic net,
  B = +1.4854, −0.4710, −0.0143 per unit area on layers 1–3. The contact puts the whole load on layer 1, so the face
  layers deform until the forces balance.
  - `hvi/scripts/tl_endlayer.py` reproduces the measured layers to 0.0011 with no fitted parameter (α = 10).
- **The idea** (Peter's partner-aware contact; fork `cs12` 210d98d4, note §4). At a contact, the particles missing from
  a body's truncated kernel are the partner's particles. Completing the kernel with them, in compression only, lets the
  interface see a near-bulk neighbourhood.
  - For identical aligned lattices it is trivially exact: the two bodies become one bulk.
  - The question is whether it stays near-exact when the partner is **not** a continuation of the lattice. That is the
    case in every real contact: the lattices are offset or finer on one side, the interface spacing is not s, the
    materials differ.
- **Why not BCT.** BCT (SPEC-TL-b §4.3) is exact on flat uniform loads in this same model and failed on small or
  changing patches (§21, §22). So Stage A **cannot show an advantage over BCT**. It can only show that kernel
  completion is consistent where BCT also is, and how it degrades under mismatch. Stage A is a gate against building a
  broken formulation. The comparison that matters (curved, changing patches) is Stage B's.

## Definitions (fixed now)

**Model.** Two TL bodies A (below) and B (above), each a column of n = 40 layers, statically loaded in uniaxial strain.
- Lateral periodic cell, with explicit particles and images (not the 1D layer reduction of `tl_endlayer.py`), so that
  offsets and spacing ratios can be represented.
- As `tl_endlayer.py`:
  - cubic net; cubic-spline kernel, h = 2^(1/6) s of each body;
  - first-order reference correction K;
  - force f_i = Σ_j V_i V_j (P_i K_i + P_j K_j) ∇W_ij;
  - linear elasticity with ν = 0.35, P = M (F − 1) in the axial direction;
  - hourglass force linearised with α = 10;
  - linear, small strain, solved by least squares with the rigid translation removed.
- The far ends of A and B carry the consistent load (distributed in proportion to B_k), so the far ends are exact and
  any error is the interface's.
- The interface spacing d is the distance between A's top layer and B's bottom layer.

**Cross pairs.** Particles i ∈ A and j ∈ B with |X_i − X_j| < h_i + h_j, using h_ij = (h_i + h_j)/2 in W and ∇W. In
statics the current positions are the reference positions.

**Load-transfer laws.**
- **L0 (today):** no cross pairs. The interface force acts as point forces, +t on every particle of A's top layer and
  −t on every particle of B's bottom layer (as the hvi contact applies it).
- **KC-f (completion in the force only):** the cross pairs add V_i V_j (P_i K_i + P_j K_j) ∇W_ij to f_i and the
  opposite to f_j. K_i and F_i come from each body's own neighbours. No point force: the cross pairs carry the
  interface load.
- **KC-full (completion in force, deformation gradient and correction):** as KC-f, and the cross pairs also enter
  K_i and F_i, with F_i − 1 = Σ_j V_j (u_j − u_i) ⊗ K_i ∇W_ij over own and cross neighbours.
- **BCT (reference row):** the Shepard-weighted BCT of SPEC-TL-b §4.3, applied on both faces.

"Compression only" cannot be tested in a linear static model: every cross pair here is compressive. Stage B tests it.

**Cases.**

| Case | What differs at the interface | Set-up |
|---|---|---|
| K1 | nothing (control) | identical lattices, aligned, d = s |
| K2a | lateral offset | B shifted by (s/2, 0) |
| K2b | lateral offset | B shifted by (s/2, s/2) |
| K3a | interface spacing | d = 0.8 s |
| K3b | interface spacing | d = 1.2 s |
| K4 | stiffness | E_B / E_A = 3, aligned, d = s |
| K5 | spacing | s_B = s_A / 2 (B finer, layer planes aligned), d = (s_A + s_B)/2 |

**Quantities.**
- p_k = P_k / t for the first three layers on each side of the interface (A's top three, B's bottom three).
- e_face = max |p_k − 1| over layers 1–2 on both sides.
- e_bulk = |P / t − 1| at mid-height of each body.
- The force transmitted by the cross pairs, Σ over cross pairs acting on A, divided by t · area: momentum, to 1e-9.
- The equilibrium residual.
- Reported only: the full layer profiles, and B_k of the face layers with and without the cross pairs.

## Rule (fixed now)

**Model checks (stop if either fails; nothing else is read).**
1. L0 on K1 gives the rigid-wall static values of `tl_endlayer.py` (0.6515 / 0.8397) to 0.002 on both sides.
2. KC-full on K1 gives p_k = 1 to 1e-9 on every layer, transmitted force 1 to 1e-9, residual ≤ 1e-10.

**Outcome, separately for KC-f and KC-full, over K2a–K5:**
- **consistent:** e_face ≤ 0.035 and e_bulk ≤ 0.001 in every case. 0.035 is the project's reading band (§25 rule).
- **partial:** e_face ≤ 0.175 in every case but not consistent. 0.175 is half of L0's deficit on K1, 1 − 0.65.
- **fails:** otherwise, or if the transmitted force misses 1 by more than 1e-9 in any case. A completion that loses
  momentum is not a contact law.

BCT is reported on every case and not judged.

## Facts checked (coldspray-procedure.md)

- No solver output, parser key or engine placeholder is read in Stage A.
- The model's only link to the solver is its check against `tl_endlayer.py`, which matched the measured layers
  (SPEC-TL-b §4.2). The static values differ from the dynamic two-body measurement by about 0.03 (0.6515 vs 0.619,
  §22 item 2). Stage A judges the static model, not the solver.
- solver-facts §2: native SPH kernel-welds two SPH parts, in tension and shear as well. KC is a compression-only
  version of that coupling for TLSPH. The welding is why native SPH has no separable contact (§9.8).
- Not covered: none for Stage A.

## Prediction (judgment, before any number)

- Model checks pass: 0.95. (KC-full on K1 is a bulk by construction; the risk is an implementation error.)
- **KC-full:** consistent 0.15, partial 0.45, fails 0.40.
  - K2 offsets: e_face ≤ 0.035 with probability 0.6. The first-order correction keeps uniform F exact; the residual
    B_k of an offset neighbourhood is small.
  - K3 spacing: 0.45.
  - K4 stiffness 3:1: 0.3. F_i of a face particle mixes the two materials' displacements, so the strain jump is
    smeared over about 2h while each particle uses its own modulus.
  - K5 finer side: 0.35.
- **KC-f:** consistent 0.20, partial 0.45, fails 0.35. With F and K from the own body, the face particles' K differs
  from the bulk's, so even K1 is not exact. K1 is reported, not judged, for KC-f.
- BCT on K1, K2 and K4: e_face ≤ 1e-3 (flat uniform loads), probability 0.8. On K5: 0.5.
- **Label before any literature check:** expected "variant of kernel-interaction SPH contact"; to be checked:
  - Campbell, Vignjevic and Libersky 2000, a contact algorithm for SPH (CMAME 184), from memory, not read;
  - native SPH part interaction in OpenRadioss.

  Never "novel".

## What follows (stated now; Peter decides after the result)

- **KC-full or KC-f consistent:** a Stage B spec, drafted for Peter, a cs12 build behind a switch with compression-only
  gating of cross pairs. Its runs:
  - §22 item 2 (TL column on TL column; there today 0.619 / 0.856);
  - T-B2 sphere on block at R/32, the curved, changing patch on which BCT failed;
  - T-A0 neutrality with the switch off.

  Judged against the quads as in §22.
- **Partial:** report, with the case that limits it; Peter decides whether Stage B is worth it.
- **Fails:** kernel completion is recorded as a negative result in this form, and no Stage B. The face-layer deficit
  stays a known limit (solver-facts §3).
- None of these outcomes bears on bonding or on the edge singularity.

## Who runs it

WSL A, Python only, minutes of CPU. A new script `hvi/scripts/tl_kc_static.py` in the fork, built on `tl_endlayer.py`;
the model checks are committed with the script before any K2–K5 number is computed. Rows
`opencourant/results/tl_kc_static.csv` (`kind = check`), and a verification section (§43) on `coldspray/opencourant-sph`,
recreated from `claude/exciting-fermi-qy077p`. Cost: none beyond WSL A time; no solver build.
