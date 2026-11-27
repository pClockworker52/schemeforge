# contact-v1.0 acceptance check (2026-11-27)

Judge **contact-v1.0** (6eef4c9, git tag `contact-v1.0`; judge hash b33dd8e82d68). It is the tag of contact-v0.12.dev
(735b69e): `git diff 735b69e 6eef4c9 -- src/schemeforge/arenas` changes only `JUDGE_VERSION`. No breaker case was
accepted (DECISIONS 2026-11-27 "Arena 2 breakers").

- `sforge judge version --arena contact`: contact-v1.0, integrity ok. `sforge judge verify --arena contact`: 13 of 13.
- `pytest -q -k "contact or integrity or version"`: 35 passed.
- Zoo dev, cloud, before and after the bump. Cases, metamorphic checks, violations and status are identical on every
  member; only wall times differ.

| Member | contact-v0.12.dev | contact-v1.0 | dev wall time (v1.0) |
|---|---|---|---|
| faltus2026 | r-20261127-200445-d245 | r-20261127-201026-a6a1 | 41.4 s |
| neo_hooke | r-20261127-200524-6a65 | r-20261127-201108-122e | 41.5 s |
| neo_hooke_iv | r-20261127-200603-8e92 | r-20261127-201150-ea67 | 43.9 s |
| wriggers2013 | r-20261127-200646-f095 | r-20261127-201235-b2b2 | 49.2 s |

The promo references of docs/targets/D.md (contact-v0.12.dev, 2026-11-25) therefore stand for contact-v1.0. A
non-.dev version is scored only where the tag exists locally (core/integrity.py), so WSL needs `git fetch --tags`
before its next contact eval.
