# Arena 2 WSL steps (Peter): promo zoo, γ-sweep, breakers (before Target D and the tag)

The promo suite draws its held-out instances from `~/.schemeforge/heldout_seed`. That file exists only on Peter's
machine, and the cloud session never reads it (CLAUDE.md iron rule 3). The breakers need the sforge MCP server, which
connects in WSL Claude Code but not in the cloud session; this is the Arena 1 precedent. Judge: **contact-v0.12.dev**
(735b69e). Decisions: DECISIONS 2026-11-25.

## 1. Set-up (WSL, in the repository folder)

1. `git pull` on branch `claude/exciting-fermi-qy077p`. WSL git has no GitHub credentials, so pull via Windows git
   if needed.
2. `uv sync --extra contact` (felupe 11.3.0, tensortrax 0.30.0).
3. `uv run --extra contact sforge judge version --arena contact`: expect `contact-v0.12.dev` and `integrity: ok`.
4. `uv run --extra contact sforge judge verify --arena contact`: expect 13 of 13.

## 2. Promo: plain zoo, then the γ-sweep

1. `uv run --extra contact sforge zoo eval --arena contact --suite promo`. Four members: GF 10, SF 10, HF 6 (each
   with max_step), HX 1, SL 4. The modeller's estimate is 2–8 min per member; robust media are at the low end.
2. `uv run --extra contact python scripts/contact_gamma_sweep.py --suite promo`. This is 16 runs: 4 members ×
   factors 0.01, 0.1, 10 and 100, where factor 1 is step 1. They are registered as zoo-medium-<member>-g<factor>.
3. Paste back both printed tables. They contain the run ids, status and seconds. The reports in `runs/reports/`
   carry family aggregates and the seed fingerprint only; the instances stay in `~/.schemeforge/heldout_runs/`.

## 3. Breakers on the zoo (plan §4, before the tag)

In WSL Claude Code, in this folder (the sforge MCP server must show as connected), paste:

```text
Use the breaker subagent on Arena 2 (arena contact, slot medium), judge contact-v0.12.dev.
Targets: the zoo members faltus2026, wriggers2013 and neo_hooke
(src/schemeforge/arenas/contact/zoo/medium/<name>.py). There are no candidates yet: break the zoo.
Case format: docs/judge/contact_cases.md (kinds gap_closure, simple_shear, hertz, sliding); every case must be
admissible (validate rules there) and have the judge's exact or classical reference. Suggested lines of attack:
grazing contact (tiny indentation), thin medium layers, strong E or nu contrast inside the stated ranges, element
distortion near 0.5, sliding at the upper slide bound, steps near the minimum.
Run all four zoo members on every draft case; a case that breaks every member is a hard case, not a weakness.
Quarantine every breaking case with case_propose. Final message: per target, the quarantine ids, the failure
signature, and which zoo members fail too.
```

Then tell the cloud session the quarantine ids. It reviews them, and Peter decides which are accepted into the judge
(`sforge case accept`, which bumps the judge version).

## Not yet

- **Target D:** committed only after the promo numbers are in and Peter accepts them.
- **The tag `contact-v1.0`:** after Target D and Gate 6.
