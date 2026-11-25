# Arena 2 promo zoo run in WSL (Peter; needed for Target D and the tag)

The promo suite draws its held-out instances from `~/.schemeforge/heldout_seed`. That file exists only on Peter's
machine, and the cloud session never reads it (CLAUDE.md iron rule 3), so this step runs in WSL. The last promo run
of the contact zoo was neo_hooke only, on contact-v0.6.dev (r-20261103-123550-7e5a). Judge contact-v0.10.dev changes
GF leak_pre and GF newton_iters, so every member is rerun.

## Steps (WSL, in the repository folder)

1. `git pull` on branch `claude/exciting-fermi-qy077p`. WSL git has no GitHub credentials, so pull via Windows git
   if needed.
2. `uv sync --extra contact` (felupe 11.3.0, tensortrax 0.30.0).
3. `uv run --extra contact sforge judge version --arena contact`: expect `contact-v0.10.dev` and `integrity: ok`.
4. `uv run --extra contact sforge judge verify --arena contact`: expect 12 of 12.
5. `uv run --extra contact sforge zoo eval --arena contact --suite promo`. Four members, at about 70 s each on the
   step-4 machine (neo_hooke).
6. Paste back the printed table and the four run ids. The reports carry family aggregates and the seed fingerprint
   only; the instances stay in `~/.schemeforge/heldout_runs/`.

## Not yet

- The γ-sweep promo runs (Target D draft, item 1). They wait for Peter's decision on the sweep.
- The tag `contact-v1.0`. It waits for the Target D commit and Gate 6.
