# CS-14 rung: fragmentation of a brittle film on a stretched substrate (protocol, frozen before any run)

Frozen 2026-11-05, before any code of the DEM cell has been run. Hunch: [coldspray-hunch-cs14.md](coldspray-hunch-cs14.md).
Code (to follow): `src/schemeforge/research/blanket_dem.py`, our own JAX code. This rung verifies the cell and its
fragment metric (standing rule: a metric gets its own rung). It says nothing about real oxides.

## What the rung checks

Against the classical shear-lag result for a brittle film on a substrate whose interface yields at a constant shear
stress τ_i (Kelly–Tyson type; derived below, not taken from a paper):
- the film stress builds up from a free end as σ(x) = τ_i x / t, so the **transfer length** is L_s = σ_f t / τ_i;
- a fragment of length ℓ breaks only if its peak stress τ_i ℓ / (2t) reaches σ_f, so ℓ ≥ 2 L_s;
- at saturation every fragment therefore lies in **L_s ≤ ℓ < 2 L_s** (a deterministic film halves until it does);
- with no length in the problem other than t, the mean fragment length is **w̄ ∝ t**.

## Model (2D, plane, nondimensional)

- **Film:** grains on a square lattice of spacing a = 1 (the grain size d_g), n_t layers thick, n_x = 64 n_t columns
  long, so the film is 64 t long. Mass 1 per grain.
- **Bonds:** nearest neighbours (horizontal and vertical) and both diagonals, linear springs of stiffness k = 1.
  Brittle: a bond breaks irreversibly when its tensile strain exceeds its threshold ε_b,i = ε_b (1 + 0.05 U), with U
  uniform in [−1, 1], one draw per bond from a fixed seed. ε_b = 0.02. A broken bond keeps a compression-only
  contact (no interpenetration).
- **Substrate:** not resolved. Each grain of the bottom layer is tied to a substrate point that moves as
  X_i = X_i⁰ (1 + ε). Normal direction: stiff spring (k_n = 10), no delamination in this rung. Tangential:
  elastic–perfectly plastic, stiffness k_i = 1, yield force f_y = τ_i · a, with the plastic slip updated by return
  mapping after each converged load step.
- **τ_i** is set so that L_s ≈ 4 t, from the σ_f measured in R0 (one value per thickness, recorded before R1).
- **Loading:** quasi-static. The substrate strain ε rises in steps of 0.05 ε_f (ε_f = σ_f / E_f from R0) up to
  4 ε_f. After each step the energy is minimised (FIRE). Then the most overloaded bond, if any, breaks, the energy
  is minimised again, and so on until no bond exceeds its threshold. Then the slip is updated and the next step
  follows.

## Sub-rung R0: free film in tension (calibration and metric check)

- The same film without substrate, length 8 t, left column held in x, right column displaced; quasi-static as
  above.
- Measured: E_f (initial slope of mean stress against strain) and σ_f (peak mean stress, force divided by t).
  Three seeds per thickness, means recorded.
- **Check:** E_f is the same within 2 % for n_t = 4, 8, 16, since the lattice is uniform. If not, the film is not a
  continuum at these thicknesses, and R1 is not run.

## Sub-rung R1: fragmentation on the substrate

- n_t = 4, 8, 16; three seeds each.
- **Fragment metric:** fragments are the connected components of the graph of unbroken bonds (contacts do not
  connect). Components of fewer than n_t grains are debris and are not counted. Fragments touching either film end
  are excluded from the mean. w̄ = mean x-extent of the remaining fragments at ε = 4 ε_f.
- **Metric unit test (before any run):** a film with all bonds across one or two prescribed vertical cuts removed
  must give exactly two or three fragments of the prescribed lengths.

## Pass criteria (frozen)

| Check | Pass |
|---|---|
| R0 | E_f equal within 2 % across n_t = 4, 8, 16 |
| R1a, the theory window | For each n_t, the seed-mean w̄ / L_s lies in **[0.9, 2.1]** (the window [1, 2] with 10 % tolerance) |
| R1b, the scale check | w̄ / t at n_t = 4, 8, 16 lies within **±10 %** of its mean over the three thicknesses |

R1b is the discretisation check that CS-14 needs: at 5–25 nm with nanometre grains, the oxide is 5–25 grains thick.
If R1b fails at n_t = 4 but holds from 8 on, the CS-14 sweep starts at 8 grains, and the grain size used in CS-14
follows from that. That is recorded, not decided after the fact.

## Not checked here

- Rate effects (the rung is quasi-static; CS-14 targets about 10⁹/s).
- The metal substrate's plasticity length and the oxide–metal cohesive length (both are absent from this rung by
  design; the interface is perfectly plastic and does not delaminate).
- Extrusion of metal through the cracks (p_E). That needs a resolved substrate and its own rung, R2, registered
  before it is run.

## Amendment 1 (2026-11-05, after the first R0 run, before any R1 run)

**Finding (R0, n_t = 4, seed 0, square lattice as frozen above; diagnostic):** E_f = 1.380, peak stress 0.0257 at
strain 0.0185. After the peak, the stress does **not** fall to zero. It stays on a sawtooth plateau of 0.019–0.022 up
to strain 0.03 (1.5 ε_b). When the horizontal bonds of a column break, the two diagonal bonds per cell across the cut
stretch at about half the crack opening divided by their length. Their combined x-capacity is comparable to the
horizontals', so the crack is bridged and the film never separates. **A square lattice with central-force diagonals
is not a brittle film.** The frozen R0 check (E_f equal across thicknesses) would have passed regardless; it was too
weak to detect this.

**Changes (before any R1 run):**
1. **Lattice:** triangular (close-packed), nearest-neighbour bonds only, spacing a = 1, rows √3/2 apart, odd rows
   offset by a/2. Film thickness t = n_t · √3/2; stress = force / t. Everything else as above (k, ε_b, scatter,
   substrate tie, loading, fragment metric with columns as the x index).
2. **R0 gains a brittleness check:** after the peak, the stress must fall below 0.1 σ_f before the imposed strain
   exceeds the peak strain by 0.2 ε_b. If it does not, the film is not brittle and R1 is not run.
3. The R0 E_f check stays (equal within 2 % across n_t = 4, 8, 16).

The square-lattice code path is replaced, not kept as an option; the diagnostic numbers above are its record.
