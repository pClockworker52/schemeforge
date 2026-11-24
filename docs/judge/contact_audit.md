# Arena 2 blind audit (plan step 6, Gate 6 item 2): how it runs

The `judge-auditor` re-implements the exact solutions and the metric definitions of C0a, C0b, C1 and C2 from
`docs/judge/contact_spec.md` and `docs/judge/contact_cases.md` alone. It then compares them with the judge on at
least 1,000 random admissible instances.
- Its hook denies every Read, Grep and Glob of `src/schemeforge/arenas/` and allows writes only under `audit/`.
- Shell reads of the judge, and of git history or diffs, are forbidden by the prompt. The hook does not cover them.
- In the cloud, the hooks run with the container's python3.

The FE solves themselves are not re-implemented. The auditor checks them against its own exact solutions for C0a
and C1, and checks the Hertz metrics by recomputing them from the nodal forces that the judge reports.

## Prompt (verbatim)

```text
Arena 2 blind audit (docs/plans/2026-10-30-phase6.md step 6; Gate 6 item 2).
Read ONLY docs/judge/contact_spec.md and docs/judge/contact_cases.md (and this prompt). Do not read
src/schemeforge/arenas/ in any way, including through shell commands (cat, grep, python -c, inspect, site-packages
copies), and do not read git history, diffs or commit messages (git log, git show, git diff). Textbook formulas are
allowed. Write only under audit/contact/.

1. Implement in audit/contact/, from the spec only, with numpy/scipy (jax only if you need it; float64):
   - the compressible neo-Hookean body and the audit medium psi_m = gamma psi_b, their confined-stretch stresses;
   - C0a/C1: the ideal contact force, the exact homogeneous solution (force and medium thickness at any push), and
     the metrics leak_pre, gap_res and force_err exactly as the spec defines them;
   - C0b: P = 2 F dpsi/dC in simple shear, shear_parasitic and normal_parasitic;
   - C2: Hertz for a rigid flat (a, p0, p(x)) for a given load, the pressure recovery from consistent nodal forces
     on quadratic edges (consistent mass matrix), and a_err (second moment), p0_err, p_l2 and leak_out as defined.
2. Generate at least 1000 random admissible instances with a fixed seed of your own, in the format of
   docs/judge/contact_cases.md: about 450 gap_closure (about 200 of them with distort > 0, i.e. C1; gamma 1e-7..1e-2
   log-uniform; random geometry, moduli, push, steps, cell counts), about 450 simple_shear (shear 0.01..5, gamma
   1e-7..1e-2) and about 100 hertz (stay inside the ranges the case file states). Get the judge's values with
   `uv run --extra contact sforge judge exact --arena contact --case <file> --json`, batches of at most 200 cases
   (Hertz cases take a few seconds each). Record any case the judge answers with an error.
3. Compare:
   - gap_closure: ideal_force, exact_force, exact_thickness, exact_force_half, exact_thickness_half,
     exact_leak_pre, exact_gap_res and exact_force_err against yours; the judge's FE values (fe_force at full push,
     fe_thickness, fe_wall_pressure against F/w, fe_leak_pre, fe_gap_res, fe_force_err) against your exact values;
     classical_force against your ideal force at every load step.
   - simple_shear: P_xy, P_yy, shear_parasitic and normal_parasitic.
   - hertz: from the judge's x and f, recompute load consistency, p, a_hertz, p0_hertz, a_err, p0_err, p_l2 and
     leak_out, and compare them with the judge's values; separately report classical-vs-Hertz a_err and p0_err
     (the spec's error floor, not round-off).
   Report the maximum relative difference per quantity (absolute where the reference is near zero, say which).
   Trace every disagreement above 1e-10 to its cause: spec ambiguity, judge bug, audit bug, or a stated tolerance
   in the spec (e.g. Newton's absolute tolerance). Do not "fix" a disagreement by reading the judge.
4. Write audit/contact/REPORT.md: method, generator seed, instance counts, the table of maximum differences, the
   list of disagreements with causes, and any place where the spec was ambiguous or silent. Keep the audit code in
   audit/contact/. Do not commit.
Final message: the table of maximum differences, and the cause of every disagreement above 1e-10.
```

## After the audit (main session)

1. Review the report and trace every disagreement.
2. Record the result in STATUS and in the Gate 6 report.
3. A spec ambiguity is fixed in the spec. A judge bug is fixed in its own judge commit, with a version bump and a
   zoo check.
