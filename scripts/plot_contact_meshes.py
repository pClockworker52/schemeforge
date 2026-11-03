"""Plots of the Arena 2 (contact) meshes as the judge builds them: C0a gap closure and C2 Hertz, undeformed and
deformed, plus the Hertz pressure profiles. Uses the judge's own mesh functions; reads nothing from the registry.

    uv run python scripts/plot_contact_meshes.py [outdir]     (default docs/judge/figures)
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import felupe as fem  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402

from schemeforge.arenas.contact import evaluate as ev  # noqa: E402
from schemeforge.arenas.contact import solve, zoo  # noqa: E402
from schemeforge.arenas.contact.cases import GapClosureCase, HertzCase  # noqa: E402
from schemeforge.arenas.contact.metrics import edge_traction  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/judge/figures")
NEO = zoo.load("medium", "neo_hooke")
BODY, MEDIUM, EDGE = "#c9d9ec", "#f3c98b", "#30475e"
OUTLINE = [0, 4, 1, 5, 2, 6, 3, 7]  # quad9: corner, mid, corner, ... (felupe/VTK order)


def polys(mesh: fem.Mesh, disp: np.ndarray | None = None) -> np.ndarray:
    """(ncells, 8, 2) element outlines through corner and mid-edge nodes, so curved edges show as used."""
    pts = mesh.points + (0.0 if disp is None else disp)
    return pts[mesh.cells[:, OUTLINE]]


def draw(ax, meshes_colors, disp_of=None, nodes=False):
    for mesh, color in meshes_colors:
        d = None if disp_of is None else disp_of(mesh)
        ax.add_collection(PolyCollection(polys(mesh, d), facecolors=color, edgecolors=EDGE, linewidths=0.4))
        if nodes:
            p = mesh.points + (0.0 if d is None else d)
            ax.plot(p[:, 0], p[:, 1], ".", ms=2.0, color=EDGE)
    ax.set_aspect("auto")


class Capture:
    """Keeps the solution field of the next felupe Job (the judge's solvers do not return it)."""

    def __enter__(self):
        self.orig = fem.Job.evaluate
        cap = self

        def evaluate(job, *args, **kwargs):
            cap.field = kwargs.get("x0")
            return cap.orig(job, *args, **kwargs)

        fem.Job.evaluate = evaluate
        return self

    def __exit__(self, *exc):
        fem.Job.evaluate = self.orig


def displacement_lookup(field):
    """Map a sub-mesh's points to the solved displacement on the stacked mesh (points matched by coordinates)."""
    pts, u = field.region.mesh.points, field[0].values
    table = {tuple(np.round(p, 10)): ui for p, ui in zip(pts, u, strict=True)}
    return lambda mesh: np.array([table[tuple(np.round(p, 10))] for p in mesh.points])


def legend(ax):
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, fc=BODY, ec=EDGE, label="body (neo-Hooke)"),
                       plt.Rectangle((0, 0), 1, 1, fc=MEDIUM, ec=EDGE, label="third medium (candidate)")],
              loc="upper right", fontsize=8)


def gap_closure_figure():
    c = GapClosureCase("C0a-g3", gamma=1e-3, nx=2)
    body = solve._column(c.width, c.gap, c.gap + c.height, c.nx, c.ny_body)
    medium = solve._column(c.width, 0.0, c.gap, c.nx, c.ny_medium)
    with Capture() as cap:
        res = solve.gap_closure(NEO, c)
    disp = displacement_lookup(cap.field)
    fig, axes = plt.subplots(1, 2, figsize=(6, 6), sharey=True)
    for ax, title, d in ((axes[0], "C0a undeformed", None), (axes[1], f"pushed {c.push} (gap {c.gap})", disp)):
        draw(ax, [(body, BODY), (medium, MEDIUM)], d, nodes=True)
        ax.axhline(0.0, color="k", lw=2)
        ax.set_xlim(-0.05, c.width + 0.05)
        ax.set_ylim(-0.05, c.gap + c.height + 0.05)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("x")
    axes[0].set_ylabel("y")
    legend(axes[0])
    fig.suptitle(f"C0a gap closure, laterally confined, gamma = 1e-3: medium left {res.medium_thickness:.4f}",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "contact_c0a_mesh.png", dpi=150)
    plt.close(fig)


def hertz_meshes(c: HertzCase):
    surf = solve._surface(c)
    body = solve._curved_block(c, surf, lambda x: c.H + 0.0 * x, c.ny, grade=True)
    medium = solve._curved_block(c, lambda x: 0.0 * x, surf, c.ny_medium, grade=False)
    return body, medium


def hertz_figures():
    c = HertzCase("C2-g6", gamma=1e-6)
    body, medium = hertz_meshes(c)
    with Capture() as cap:
        res = solve.hertz(NEO, c)
    disp = displacement_lookup(cap.field)
    m, _ = ev.hertz_metrics(c, res)
    es = c.E / (1 - c.nu**2)
    a = float(np.sqrt(4 * res.load * c.R / (np.pi * es)))

    fig, ax = plt.subplots(figsize=(7, 6))
    draw(ax, [(body, BODY), (medium, MEDIUM)])
    ax.axhline(0.0, color="k", lw=2)
    ax.set_xlim(-0.02, c.W + 0.02)
    ax.set_ylim(-0.02, c.H + 0.02)
    ax.set_title(f"C2 Hertz, whole half model: {len(body.cells)} body + {len(medium.cells)} medium Q2 cells, "
                 f"{2 * cap.field.region.mesh.npoints} DOF", fontsize=10)
    ax.set_xlabel("x (symmetry at x = 0)")
    ax.set_ylabel("y (rigid flat at y = 0)")
    legend(ax)
    fig.tight_layout()
    fig.savefig(OUT / "contact_c2_mesh_overview.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    for ax, title, d in ((axes[0], "undeformed (vertical scale stretched)", None),
                         (axes[1], f"pushed {c.push}: deformed, true displacements", disp)):
        draw(ax, [(body, BODY), (medium, MEDIUM)], d, nodes=True)
        ax.axhline(0.0, color="k", lw=1.5)
        ax.axvline(a, color="crimson", lw=1, ls="--")
        ax.set_xlim(0.0, 0.15)
        ax.set_ylim(-0.001, 0.02)
        ax.set_title(title, fontsize=10)
        ax.set_ylabel("y")
    axes[0].text(a, 0.0185, " Hertz a", color="crimson", fontsize=8)
    axes[1].set_xlabel("x")
    legend(axes[0])
    fig.suptitle(f"C2 Hertz near the contact, gamma = 1e-6, judge regularization kr = {c.kr:g}: "
                 f"a_err {m['a_err']:+.1%}, p0_err {m['p0_err']:+.1%}", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "contact_c2_mesh_contact_zone.png", dpi=150)
    plt.close(fig)
    return c


def pressure_figure():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    runs = [("classical contact (reference)", None), ("medium, gamma = 1e-5", 1e-5), ("medium, gamma = 1e-6", 1e-6)]
    for label, gamma in runs:
        c = HertzCase("p", gamma=gamma or 1e-6)
        res = solve.hertz_classical(c) if gamma is None else solve.hertz(NEO, c)
        p = edge_traction(res.x, res.f)
        ax.plot(res.x, p, ".-", ms=3, lw=1, label=label)
    es = c.E / (1 - c.nu**2)
    a = float(np.sqrt(4 * res.load * c.R / (np.pi * es)))
    x = np.linspace(0, a, 200)
    ax.plot(x, 2 * res.load / (np.pi * a) * np.sqrt(1 - (x / a) ** 2), "k--", lw=1.5, label="Hertz (for the load)")
    ax.axhline(0.0, color="0.6", lw=0.8)
    ax.set_xlim(0, 0.2)
    ax.set_xlabel("x")
    ax.set_ylabel("contact pressure on the flat")
    ax.set_title("C2 pressure from the nodal reactions (metrics.edge_traction)", fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "contact_c2_pressure.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    gap_closure_figure()
    hertz_figures()
    pressure_figure()
    print("written:", *sorted(p.name for p in OUT.glob("contact_*.png")))
