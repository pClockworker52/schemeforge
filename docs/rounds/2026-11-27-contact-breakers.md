# Breakers on the Arena 2 zoo (contact / medium), review, 2026-11-27

Judge **contact-v0.12.dev** (735b69e; registry hash 2a407e09ef5a). Plan §4, DECISIONS 2026-11-25 item 4. Breaker run in
WSL (Peter): ten cases in quarantine, **B-0057 … B-0066** (e572add). The breaker's final message did not reach the cloud
session, so the modeller re-ran every case on all four zoo members in the cloud: `sforge eval <member> --arena contact
--slot medium --suite smoke --case cases/quarantine/<id>.yaml`. The run ids below are from the cloud registry
(`runs/`, not committed). **No case is accepted** (Peter decides).

Members: F = faltus2026, N = neo_hooke, IV = neo_hooke_iv, W = wriggers2013. "nc" = Newton did not converge.
Held-out ranges (families.py, spec §Step 4): GF, SF, HF and SL draw ν from 0.15–0.45. SF draws s from 0.1–3.0. HF and SL
draw the indentation beyond the gap from 0.3–0.5 % of R. SL draws the slide from 0.2–0.9 % of R (about 0.05–0.2 a).

## 1. Weaknesses: some members fail, others pass

| Case | Set-up | F | N | IV | W | Inside a held-out range? |
|---|---|---|---|---|---|---|
| B-0057 | hertz, **ν = 0** | nc (r-20261127-193723-bc05) | nc (r-20261127-193649-0f42, -193723-44fb) | a_err 0.5 %, p0_err 1.4 % (r-20261127-193723-ce2b) | a_err 11.4 %, p0_err −1.1 % (r-20261127-193723-7e30) | no (ν < 0.15) |
| B-0058 | sliding, **ν = 0** | nc (r-20261127-193754-372b) | nc (r-20261127-193857-cfc9) | shear_parasitic 2.8·10⁻³, fn_rise −1.0·10⁻³ (r-20261127-193742-94d5) | nc (r-20261127-193951-c3f5) | no (ν < 0.15) |
| B-0062 | hertz, **ν = 0.15** | a_err 2.0 %, p0_err −0.5 % (r-20261127-194111-eff4) | nc (r-20261127-194326-4e2f) | a_err −1.0 %, p0_err 1.2 % (r-20261127-194229-004e) | a_err 9.0 %, p0_err −1.1 % (r-20261127-194219-27f5) | yes (HF lower edge) |
| B-0063 | simple shear, **s = 3**, ν 0.45, γ 10⁻³ | shear_parasitic **0.174** (r-20261127-194154-e410) | 1.0·10⁻³ (r-20261127-194448-38b1) | 1.0·10⁻³ (r-20261127-194343-8638) | 4.1·10⁻³ (r-20261127-194251-0e5b) | yes (SF upper edge) |
| B-0060 | simple shear, **s = 10**, ν 0.45, γ 10⁻³ | shear_parasitic **1.93**, normal_parasitic −6.44 (r-20261127-193915-0636) | 1.0·10⁻³ (r-20261127-194137-6be8) | 1.0·10⁻³ (r-20261127-193831-d682) | 0.0195 (r-20261127-194047-7922) | no (s > 3) |

Mechanisms, as read by the modeller:
- **Low ν: Newton fails on N and F; W loses contact-radius accuracy.** IV converges and is accurate. At ν = 0.15,
  inside the HF range, N already fails. The held-out HF and SL families sample ν = 0.15. ν = 0 is outside the
  declared range.
- **Large homogeneous shear stiffens faltus2026.** At s = 3 its parasitic shear is about 170 × γ; the neo-Hookean
  members stay at γ, and W at about 4 γ. At s = 3, inside the SF range, the held-out SF family already samples the
  regime.

## 2. Hard cases: every member fails

| Case | Set-up | Result on all four members | Reading |
|---|---|---|---|
| B-0059 | sliding, **slide 0.099** (validator bound W/10 = 0.1), 5 steps | N, IV, W nc; F converges with shear_parasitic 0.37, fn_rise 2.76 (F r-20261127-193843-027c; N -193928-9be5; IV -193813-d24e; W -194023-3829) | **Large sliding.** a ≈ √(R δ) ≈ 0.06, so the slide is about 1.6 a. C4 is small sliding (0.05–0.2 a); large sliding (C5, ironing) is not in this phase (Gate 6 report, limits). The validator admits it. |
| B-0061 | gap closure, push = gap + 10⁻⁴ | force_err 34.8 / 4.62 / 6.81 / 40.9, gap_res 0.035 / 0.0046 / 0.0068 / 0.041 (F r-20261127-193959-1a49; N -194202-e4c9; IV -194119-b592; W -194100-2edd) | **Grazing gap closure.** The body force from a 10⁻⁴ overlap is of the order of the medium's own resistance at its residual gap: the third-medium floor, not a medium-specific weakness. |
| B-0064 | hertz, indentation 10⁻⁴ beyond the gap | a_err −1 (no contact radius found), p0_err −0.35 … −0.47 (F r-20261127-194303-ec24; N -194503-8b2f; IV -194456-e9e7; W -194316-fe8e) | **Under-resolved.** a ≈ 0.01 is a third of one column (1/32). Outside the HF indentation range (0.3–0.5 % of R); the validator admits it. |
| B-0065 | hertz, **ν = 0.49** | a_err −1 on all, p0_err −0.04 … −0.10, leak_out 0.21–0.25 (F r-20261127-194358-0d88; N -194612-b096; IV -194538-4df7; W -194418-afe2) | Near-incompressible body, outside the ν range. a_err = −1 with nonzero pressure: no contact radius found. Not checked whether this is the body discretisation (locking) or the a-detection rule. |
| B-0066 | hertz, **ν = 0.45** | a_err −7.9 / −19.0 / −20.5 / −11.9 %, p0_err −4.4 / −0.8 / −0.6 / −2.8 %, leak_out 0.05–0.07 (F r-20261127-194435-7a67; N -194717-ac00; IV -194644-63cf; W -194525-b6de) | **Inside the HF range (upper edge)**, and every member misses D4's 2 % on a. The held-out HF family samples it, so it is already in the promo references behind D4. |

## 3. What this means for Gate 6

- **Inside the declared ranges, nothing new escapes the judge.** Every regime that breaks a member at a declared
  parameter (ν = 0.15, s = 3, ν = 0.45) lies in a held-out family that promo already samples. Target D's thresholds
  were set on those promo references.
- **Outside them** (ν = 0, s = 10, ν = 0.49, grazing, large sliding), the breaks are real, but they lie outside the
  arena's declared scope.
- **The validator admits more than the spec intends.** Slides up to W/10 (C4 covers up to about 0.2 a) and indentations
  below one column (the spec's Hertz conditions assume a resolved contact) are admissible. A stricter validator is a
  judge change. It would not change any score.
- **Cost of accepting into dev:** each case adds 3–11 s per member (above). Dev is now 41–52 s against the 60 s budget
  (Gate 6 item 6). One case is about the most that fits. Any acceptance bumps the judge version. The promo
  references and the γ-sweep check are then rerun in WSL before D.md (DECISIONS 2026-11-25 "Target D thresholds
  accepted").

**Modeller's recommendation:** accept none. Record the out-of-scope regimes as limits. Commit docs/targets/D.md on
contact-v0.12.dev and tag that version contact-v1.0. If Peter wants the low-ν failure visible in dev, B-0057 is the one
case to take: two members fail Newton, W is off by 11 %, IV passes. It costs one judge version and the WSL promo rerun.
