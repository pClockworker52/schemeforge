# Arena 1 blind audit (PLAN §9.10) — how to run it

The judge-auditor re-implements the exact Riemann and nozzle solutions from `euler1d_spec.md` §1–4 alone and
compares them with the judge on at least 1,000 random admissible instances. Its hook denies every read of
`src/schemeforge/arenas/`, so it must run in a Claude Code session **inside WSL** (the hooks call `python3`;
from the Windows side they would fail open).

## Steps (Peter)

1. In WSL: `cd /mnt/c/Users/peter/schemeforge && claude` (subscription login; the folder must be trusted).
2. Paste the prompt below. It takes roughly 20–40 minutes.
3. When it is done, check that `audit/euler1d/REPORT.md` exists and tell the main session; it will review the
   report, trace any disagreement above 1e-10 and record the result in `docs/STATUS.md`.

## Prompt

```text
Use the judge-auditor subagent for the Arena 1 blind audit (docs/PLAN.md §9.10, docs/judge/euler1d_audit.md).
Task for the subagent:
1. From docs/judge/euler1d_spec.md sections 1-4 and textbook formulas only, implement in audit/euler1d/:
   the exact Riemann solver (star state, wave speeds, sampling) and the exact quasi-1D nozzle solution
   (critical pressures, regimes, shock position, profiles) for the anderson, parabolic and conical geometries.
   Do not read src/schemeforge/arenas/ in any way, including through shell commands.
2. Generate at least 1000 random admissible instances with a fixed seed of your own:
   - 600 Riemann problems: gamma in {1.4, 5/3, 1.405, 1.2}, densities 10^-1..10^1, pressures 10^-3..10^3,
     velocities up to the sound speed, no vacuum, n = 50, t_end small enough that waves stay inside [0, 1];
   - 400 nozzles: anderson, parabolic and conical geometries (area ratio 2..10, length 2..4, inlet ratio
     1.5..3), all three regimes (subsonic, shock, supersonic exit), n = 40.
   Write them as YAML lists in the case format of docs/judge/euler1d_cases.md and get the judge's answers with
   `uv run sforge judge exact --arena euler1d --case <file> --json` (batches of a few hundred cases).
3. Compare p_star, u_star, rho_star_L/R, wave speeds, the sampled rho/u/p (Riemann) and regime, x_shock, M1,
   p0_ratio, mass_flow, p_crit1..3 and the profiles (nozzle). Report the maximum relative difference per
   quantity and trace every disagreement above 1e-10 to its cause (spec ambiguity, judge bug or audit bug).
4. Write audit/euler1d/REPORT.md with the method, the instance generator seed, the table of maximum
   differences and the list of disagreements with causes. Keep the audit code in audit/euler1d/.
```
