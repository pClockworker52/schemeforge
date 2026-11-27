# Repository clean-up, 2026-11-27

Step 2 of DECISIONS 2026-11-27 (finish Gate 6, clean the repository, then unpause cold spray). Scope proposed in chat
by the modeller and confirmed by Peter ("go ahead") on 2026-11-27. Record only; nothing here changes a result.

## Done

1. **Merged `coldspray/bonding-methods-reading`** (cbe2d88). Its one unmerged commit 2a8ad14 (WSL B task b9 completed
   except the closed Dai 2025) adds to docs/research/data/bonding_methods_reading.md only. Leak scan: the commit carries
   its own blind screen (no B06, B07 or B16 material); blind list 1 is used up (DECISIONS 2026-11-23); no PDF.
2. **`main` fast-forwarded** from c029897 (2026-11-03) to cbe2d88. Fast-forward only, no history rewritten.
3. **STATUS:** the dated entries 2026-11-18 to 2026-11-23 (40 lines) moved verbatim to docs/status-archive.md.
4. **HANDOFF:** reduced to the current order; the cold-spray track state at the pause moved verbatim to
   docs/handoff-archive.md (section "2026-11-27").
5. Checks before the clean-up commits: `pytest -q` 333 passed; `ruff check .` clean.

## Not done: remote branch deletion (blocked in the cloud)

The cloud session's permission classifier refused `git push origin --delete` for the branches below. Each is fully
contained in `claude/exciting-fermi-qy077p` (checked with `git merge-base --is-ancestor` on 2026-11-27), so deleting
them loses no commit. Tips, for recovery:

| Branch | Tip | Last commit |
|---|---|---|
| `coldspray/b02-b14-outcomes` | add80b840 | 2026-11-07 |
| `coldspray/b03-b12-outcomes` | 5ec37363e | 2026-11-08 |
| `coldspray/b03-b12-provenance` | 2ba00a2df | 2026-11-08 |
| `coldspray/b06-outcomes` | da1900b26 | 2026-11-18 |
| `coldspray/b10-outcomes` | 94fd1739c | 2026-11-04 |
| `coldspray/blind-inputs` | c9de45f70 | 2026-11-07 |
| `coldspray/blind-inputs-b03-b05-b12` | fca79c9b8 | 2026-11-07 |
| `coldspray/blind-inputs-b06-b07-b16` | d58c3450e | 2026-11-15 |
| `coldspray/blind-list2-count` | e49345588 | 2026-11-21 |
| `coldspray/bonding-methods-reading` | 2a8ad14eb | 2026-11-15 |
| `coldspray/boundary-integration-reading` | e865660b8 | 2026-11-15 |
| `coldspray/lit-interface` | 2b45c66be | 2026-11-05 |
| `coldspray/opencourant-verification` | 01a1f6b75 | 2026-11-04 |
| `coldspray/openradioss-setup` | f5b91a1ee | 2026-11-03 |
| `coldspray/panova-thesis` | 29798bebd | 2026-11-07 |
| `coldspray/panova2024-ch2` | a33742c9e | 2026-11-08 |
| `coldspray/powder-properties` | 9e2c28dc9 | 2026-11-07 |
| `coldspray/profizi2016-reading` | 370ac9146 | 2026-11-12 |

To delete them from WSL (after `git fetch origin`):

```bash
git push origin --delete \
  coldspray/b02-b14-outcomes \
  coldspray/b03-b12-outcomes \
  coldspray/b03-b12-provenance \
  coldspray/b06-outcomes \
  coldspray/b10-outcomes \
  coldspray/blind-inputs \
  coldspray/blind-inputs-b03-b05-b12 \
  coldspray/blind-inputs-b06-b07-b16 \
  coldspray/blind-list2-count \
  coldspray/bonding-methods-reading \
  coldspray/boundary-integration-reading \
  coldspray/lit-interface \
  coldspray/opencourant-verification \
  coldspray/openradioss-setup \
  coldspray/panova-thesis \
  coldspray/panova2024-ch2 \
  coldspray/powder-properties \
  coldspray/profizi2016-reading
```

Kept: `main` and the working branch. `coldspray/opencourant-sph` (tip 87a1d4e) was kept for §42; §42 is merged since
5208b15, so it can be deleted too: `git push origin --delete coldspray/opencourant-sph`.
