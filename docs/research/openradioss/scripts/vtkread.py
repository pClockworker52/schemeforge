"""Minimal reader for the legacy ASCII VTK files written by OpenCourant's anim_to_vtk.

Returns a dict with
    time  : float, simulation time (deck units)
    xyz   : (n_points, 3) node coordinates (deck units)
    cells : list of int arrays, node indices per cell
    types : (n_cells,) VTK cell types (9 = quad)
    point : {name: (n_points,) or (n_points, 3) array}
    cell  : {name: (n_cells,) array}
"""

import numpy as np


def _parse_cells(tok, i):
    m = int(tok[i + 2])
    flat = np.array(tok[i + 3 : i + 3 + m], int)
    cells, j = [], 0
    while j < m:
        k = flat[j]
        cells.append(flat[j + 1 : j + 1 + k])
        j += k + 1
    return cells, i + 3 + m


def read(path):
    tok = open(path).read().split()
    out = {"cell": {}, "point": {}}
    where = None
    i = 0
    while i < len(tok):
        t = tok[i]
        if t == "TIME":  # FieldData entry: TIME 1 1 double <value>
            out["time"] = float(tok[i + 4])
            i += 5
        elif t == "POINTS":
            n = int(tok[i + 1])
            out["xyz"] = np.array(tok[i + 3 : i + 3 + 3 * n], float).reshape(n, 3)
            i += 3 + 3 * n
        elif t == "CELLS":
            out["cells"], i = _parse_cells(tok, i)
        elif t == "CELL_TYPES":
            n = int(tok[i + 1])
            out["types"] = np.array(tok[i + 2 : i + 2 + n], int)
            i += 2 + n
        elif t in ("CELL_DATA", "POINT_DATA"):
            where = "cell" if t == "CELL_DATA" else "point"
            out["n" + where] = int(tok[i + 1])
            i += 2
        elif t == "SCALARS":  # SCALARS name type ncomp [LOOKUP_TABLE default] values...
            name, n = tok[i + 1], out["n" + where]
            j = i + 6 if tok[i + 4] == "LOOKUP_TABLE" else i + 4
            out[where][name] = np.array(tok[j : j + n], float)
            i = j + n
        elif t == "VECTORS":
            name, n = tok[i + 1], out["n" + where]
            out[where][name] = np.array(tok[i + 3 : i + 3 + 3 * n], float).reshape(n, 3)
            i += 3 + 3 * n
        else:
            i += 1
    return out
