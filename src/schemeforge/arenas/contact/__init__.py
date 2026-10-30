"""Arena 2: third-medium contact (PLAN §14, docs/plans/2026-10-30-phase6.md).

The candidate is the strain energy of the fictitious medium that fills the gap between contacting bodies. The judge
runs it inside fixed FElupe models (plane strain, bi-quadratic quads) and measures how close the medium comes to
ideal contact: no force before the gap closes, no residual gap after, no shear resistance, robust Newton steps.

JUDGE_VERSION names the git tag of this judge; ".dev" means untagged development. Bump it in the same commit as any
judge change (PLAN §2 rule 2). This arena is its own judge: its version and hash cover only this directory and
arenas/__init__.py (core/integrity.py).
"""

JUDGE_VERSION = "contact-v0.1.dev"
