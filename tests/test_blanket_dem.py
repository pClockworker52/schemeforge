"""Tests for the CS-14 blanket cell (rung R0/R1 helpers): lattice, fragment metric, a small free-film run."""

import numpy as np
import pytest

from schemeforge.research import blanket_dem as bd


def test_lattice_bond_counts():
    f = bd.build_film(3, 5, seed=0)
    # triangular lattice: along rows 4*3; between rows 2 interfaces x (5 + 4) inclined bonds
    assert len(f.bi) == 12 + 2 * 9
    assert np.allclose(f.r0, 1.0)  # nearest neighbours only, all of length a


def _cut(film, cols):
    """Remove every bond that crosses the vertical cut between column c-1 and c, for each c in cols."""
    alive = np.ones(len(film.bi), dtype=bool)
    ci, cj = film.bi // film.n_t, film.bj // film.n_t
    for c in cols:
        alive &= ~((np.minimum(ci, cj) < c) & (np.maximum(ci, cj) >= c))
    return alive


def test_fragment_metric_prescribed_cuts():
    # protocol: one or two prescribed cuts give exactly two or three fragments of the prescribed lengths
    f = bd.build_film(4, 40, seed=0)
    one = bd.fragments(f, _cut(f, [15]))
    assert [x["length"] for x in one] == [15, 25]
    two = bd.fragments(f, _cut(f, [10, 28]))
    assert [x["length"] for x in two] == [10, 18, 12]
    assert [x["touches_end"] for x in two] == [True, False, True]


def test_free_film_small_run():
    r = bd.run_r0(2, seed=0, length_over_t=4, n_steps=15)
    assert r["E_f"] > 0
    # a film must eventually fail: peak stress below E_f times the imposed strain range
    assert 0 < r["sigma_f"] < r["E_f"] * 1.5 * bd.EPS_B
