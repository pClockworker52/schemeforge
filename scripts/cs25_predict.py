"""CS-25 (draft): predictions of the co-exposure law from material properties only.

Reads properties.csv only (rule P1 via schemeforge.research.coldspray.load_properties). Reads NO v_cr value.

Model (docs/research/coldspray-hunch-cs25.md):
- planar acoustic contact of particle p and substrate s, impedances Z_i = sqrt(B_i rho_i) [kg m^-2 s^-1], B_i the bulk
  modulus [Pa] from E and nu (rule P1), c_i = sqrt(B_i / rho_i) [m/s];
- shared interface pressure p = V Z_p Z_s / (Z_p + Z_s) [Pa]; each face's compression mu_i = p / B_i [-];
- face i is cleaned iff mu_i >= mu_star = alpha / 2, alpha = 0.15 from zoo Z6 (not fitted here);
- the particle bonds iff BOTH faces are cleaned (co-exposure), so
  v_cr(p on s) = (alpha / 2) * max(B_p, B_s) * (1 / Z_p + 1 / Z_s) [m/s];
- matched pairs: v_cr = alpha * c (Z6 exactly);
- inner radius of the bonded ring at V (rigid kinematics): r_in / R = V / sqrt(V^2 + min(c_p, c_s)^2).

Comparators (for mismatched pairs): Z6 with the particle's c (ratio to the particle's matched pair = 1), and Z6 with
the arithmetic mean of B and rho of both bodies (Z7's mismatched-pair rule applied to Z6).

Run: uv run python scripts/cs25_predict.py
"""

from __future__ import annotations

import math

from schemeforge.research.coldspray import bulk_modulus_pa, load_properties

ALPHA = 0.15  # zoo Z6 (HG2018a, experiments); fixed, not fitted
MU_STAR = ALPHA / 2.0

# H20 mismatched pairs (particle, substrate). The first six are CS-24's item A (ratios in the record: calibration
# context); the last three are the judged item of the draft (rows not quoted in the record).
CONTEXT = [("Al", "Cu"), ("Al", "Ni"), ("Al", "Ti"), ("Cu", "Al"), ("Cu", "Ti"), ("Ti", "Cu")]
JUDGED = [("Cu", "W"), ("Sn", "Cu"), ("W", "Cu")]
# Not measured in H20 (unseen predictions).
# Observed ratios of the context pairs, size-corrected, copied from the CS-24 result section
# (docs/research/coldspray-hunch-cs24.md, "Result", item A table; output of scripts/cs24_score.py). Exposed;
# they decide nothing for CS-25. True = resolved by CS-24's rule.
CONTEXT_OBS = {("Al", "Cu"): (1.082, False), ("Al", "Ni"): (1.344, True), ("Al", "Ti"): (1.260, True),
               ("Cu", "Al"): (1.120, True), ("Cu", "Ti"): (1.400, True), ("Ti", "Cu"): (0.825, False)}
UNSEEN = [("Ni", "Al"), ("Ti", "Al"), ("Cu", "Sn"), ("Al", "W"), ("W", "Al"), ("Ni", "Cu"), ("Cu", "Ni"),
          ("Sn", "Al"), ("Al", "Sn"), ("Ti", "Ni"), ("Ni", "Ti")]


def mat(props: dict, m: str) -> dict[str, float]:
    """B [Pa], rho [kg/m^3], c [m/s], Z [kg m^-2 s^-1] of material m by rule P1."""
    p = props[m]
    b = bulk_modulus_pa(p)
    if b is None:
        raise ValueError(f"no bulk modulus for {m}")
    rho = p["rho_kg_m3"][0]
    return {"B": b[0], "rho": rho, "c": math.sqrt(b[0] / rho), "Z": math.sqrt(b[0] * rho)}


def vcr(pp: dict[str, float], ss: dict[str, float]) -> float:
    """Co-exposure v_cr [m/s] of particle pp on substrate ss."""
    return MU_STAR * max(pp["B"], ss["B"]) * (1.0 / pp["Z"] + 1.0 / ss["Z"])


def limiting_face(pp: dict[str, float], ss: dict[str, float]) -> str:
    """The face that reaches mu_star last (the larger bulk modulus)."""
    return "particle" if pp["B"] >= ss["B"] else "substrate"


def v_clean(face: dict[str, float], pp: dict[str, float], ss: dict[str, float]) -> float:
    """Impact speed [m/s] at which this face reaches mu_star."""
    return MU_STAR * face["B"] * (1.0 / pp["Z"] + 1.0 / ss["Z"])


def r_in(v: float, pp: dict[str, float], ss: dict[str, float]) -> float:
    """r_in / R at impact speed v (rigid kinematics, switch of the lower-sound-speed face)."""
    c = min(pp["c"], ss["c"])
    return v / math.sqrt(v * v + c * c)


def z6_mean(pp: dict[str, float], ss: dict[str, float]) -> float:
    """Z6 with arithmetic means of B and rho (Z7's mismatched-pair rule)."""
    return ALPHA * math.sqrt(0.5 * (pp["B"] + ss["B"]) / (0.5 * (pp["rho"] + ss["rho"])))


def row(props: dict, x: str, y: str, denom: str) -> str:
    """One table row. denom: the matched pair the ratio is taken against ('particle' or 'substrate')."""
    pp, ss = mat(props, x), mat(props, y)
    v = vcr(pp, ss)
    ref = pp if denom == "particle" else ss
    v0 = ALPHA * ref["c"]
    return (f"| {x} on {y} | {pp['B'] / 1e9:.1f} / {ss['B'] / 1e9:.1f} | {pp['Z'] / 1e6:.2f} / {ss['Z'] / 1e6:.2f} "
            f"| {v:.0f} | {limiting_face(pp, ss)} | {denom} | {v / v0:.3f} | {ALPHA * pp['c'] / v0:.3f} "
            f"| {z6_mean(pp, ss) / v0:.3f} | {r_in(v, pp, ss):.3f} "
            f"| {v_clean(pp, pp, ss):.0f} / {v_clean(ss, pp, ss):.0f} |")


def main() -> None:
    props = load_properties()
    print(f"alpha = {ALPHA}, mu_star = {MU_STAR}")
    print("\nMatched pairs (v_cr = alpha c; r_in / R at v_cr = alpha / sqrt(1 + alpha^2) = "
          f"{ALPHA / math.sqrt(1 + ALPHA ** 2):.3f}):")
    for m in ("Al", "Cu", "Ni", "Ti", "Sn", "W"):
        q = mat(props, m)
        print(f"  {m}: B {q['B'] / 1e9:.1f} GPa, rho {q['rho']:.0f}, c {q['c']:.0f} m/s, Z {q['Z'] / 1e6:.2f} MRayl, "
              f"v_cr {ALPHA * q['c']:.0f} m/s")
    head = ("| Pair | B_p / B_s [GPa] | Z_p / Z_s [MRayl] | v_cr CS-25 [m/s] | limiting face | ratio against "
            "| CS-25 ratio | Z6 particle-only ratio | Z6 mean ratio | r_in / R at v_cr "
            "| face cleaned from, p / s [m/s] |\n" + "|---" * 11 + "|")
    print("\nCalibration context (CS-24 item A pairs; observed ratios in the record):")
    print(head)
    for x, y in CONTEXT:
        print(row(props, x, y, "particle"))
    print("\nContext comparison (post hoc, decides nothing): |ln r_obs - ln r_model|")
    print("| Pair | r_obs (CS-24) | resolved | CS-25 | Z6 particle-only | Z6 mean |\n|---|---|---|---|---|---|")
    for (x, y), (r_obs, res) in CONTEXT_OBS.items():
        pp, ss = mat(props, x), mat(props, y)
        v0 = ALPHA * pp["c"]
        errs = [abs(math.log(r_obs) - math.log(m / v0)) for m in (vcr(pp, ss), v0, z6_mean(pp, ss))]
        print(f"| {x} on {y} | {r_obs:.3f} | {'yes' if res else 'no'} | " + " | ".join(f"{e:.3f}" for e in errs) + " |")
    print("\nJudged item (rows not quoted in the record):")
    print(head)
    print(row(props, "Cu", "W", "particle"))
    print(row(props, "Sn", "Cu", "particle"))
    print(row(props, "W", "Cu", "substrate"))
    print("\nUnseen pairs (not measured in H20):")
    print(head)
    for x, y in UNSEEN:
        print(row(props, x, y, "particle"))


if __name__ == "__main__":
    main()
