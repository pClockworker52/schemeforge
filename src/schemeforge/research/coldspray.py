"""Retrospective zoo test for single-impact critical adhesion velocities (cold-spray research track).

This module is NOT a judge and NOT an arena. It implements the frozen rules of
docs/research/coldspray-preregistration.md:

- data:        docs/research/data/vcr_lipit.csv (measured windows) and properties.csv (inputs);
- properties:  matched source first (Hassani2020 Table S1, then the HG2018a preprint table, then handbook
               rows), every value carrying its source id;
- quantity:    single-impact v_cr at room temperature (m/s);
- score:       distance of a prediction outside the measured window, divided by the window midpoint
               (0 inside the window); reported separately for in-domain and out-of-domain rows.

Units: velocities m/s, densities kg/m^3, moduli GPa in the tables (converted to Pa here), diameters um,
temperatures K.
"""

from __future__ import annotations

import csv
import math
import statistics
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

DATA = Path(__file__).resolve().parents[3] / "docs" / "research" / "data"
SOURCE_ORDER = ("P-H20", "P-HG", "P-WP")  # matched first (preregistration rule P1)
SCORED_PREFIXES = ("H20", "DW", "CH", "PA")  # Q rows (conflicting quotes) are not scored (rule S3)


@dataclass(frozen=True)
class Row:
    """One measured window from vcr_lipit.csv."""

    id: str
    particle: str
    substrate: str
    substrate_condition: str
    d_um: float | None
    T_substrate: str
    lo: float | None
    hi: float | None
    mid: float | None
    regime: str

    @property
    def matched(self) -> bool:
        return self.particle == self.substrate

    @property
    def room_temperature(self) -> bool:
        return self.T_substrate == "room"


@dataclass(frozen=True)
class Prediction:
    """A model's output for one row: v (m/s) or None if the model cannot run, plus its domain claim."""

    v: float | None
    in_domain: bool
    note: str = ""
    regime: str = ""


def _f(x: str) -> float | None:
    return float(x) if x not in ("", None) else None


def load_rows(path: Path = DATA / "vcr_lipit.csv") -> list[Row]:
    """Read the measured windows. Returns all rows, including unscored Q rows."""
    out = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            out.append(Row(r["id"], r["particle"], r["substrate"], r["substrate_condition"], _f(r["d_um"]),
                           r["T_substrate_K"], _f(r["vcr_low_mps"]), _f(r["vcr_high_mps"]),
                           _f(r["vcr_mid_mps"]), r["regime"]))
    return out


def load_properties(path: Path = DATA / "properties.csv") -> dict[str, dict[str, tuple[float, str]]]:
    """Merge property rows per material by SOURCE_ORDER. Returns {material: {field: (value, source_id)}}.

    A field is taken from the first source in SOURCE_ORDER that has it; nothing is filled from elsewhere.
    """
    by_src: dict[str, list[dict[str, str]]] = {s: [] for s in SOURCE_ORDER}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            for s in SOURCE_ORDER:
                if r["id"].startswith(s + "-"):
                    by_src[s].append(r)
    merged: dict[str, dict[str, tuple[float, str]]] = {}
    for s in SOURCE_ORDER:
        for r in by_src[s]:
            m = merged.setdefault(r["material"], {})
            for k, v in r.items():
                if k in ("id", "material", "source", "extraction", "notes", "Yd_macro_ref") or v == "":
                    continue
                if k not in m:
                    m[k] = (float(v), r["id"])
    return merged


def bulk_modulus_pa(props: dict[str, tuple[float, str]]) -> tuple[float, str] | None:
    """Bulk modulus in Pa: B from E and nu of the first source that has both (B = E / (3 (1 - 2 nu))),
    else a tabled B. Returns (B, provenance)."""
    if "E_GPa" in props and "nu" in props and props["E_GPa"][1] == props["nu"][1]:
        e, src = props["E_GPa"]
        nu = props["nu"][0]
        return e * 1e9 / (3.0 * (1.0 - 2.0 * nu)), f"{src} (E, nu)"
    if "B_GPa" in props:
        return props["B_GPa"][0] * 1e9, props["B_GPa"][1]
    return None


# ---- domain rule shared by the closed-form single-impact laws (preregistration rule D1) ----
def z6_domain(row: Row) -> bool:
    """Matched pair, room-temperature substrate, polished substrate, 8 <= d <= 16 um."""
    return (row.matched and row.room_temperature and row.substrate_condition.startswith("polished")
            and row.d_um is not None and 8.0 <= row.d_um <= 16.0)


def z6_sound_speed(alpha: float, use_hugoniot_c0: bool = False) -> Callable[[Row, dict], Prediction]:
    """Z6 (HG2018a): v_cr = alpha * sqrt(B / rho); variant: alpha * C0 (Hugoniot intercept)."""

    def model(row: Row, props: dict) -> Prediction:
        if not row.matched:
            return Prediction(None, False, "matched pairs only")
        p = props.get(row.particle)
        if not p or "rho_kg_m3" not in p:
            return Prediction(None, False, "no density")
        if use_hugoniot_c0:
            if "C0_mps" not in p or p["C0_mps"][1] != "P-H20-" + row.particle.replace(" ", ""):
                return Prediction(None, False, "no Hugoniot C0")
            return Prediction(alpha * p["C0_mps"][0], z6_domain(row), p["C0_mps"][1])
        b = bulk_modulus_pa(p)
        if b is None:
            return Prediction(None, False, "no bulk modulus")
        rho, rsrc = p["rho_kg_m3"]
        return Prediction(alpha * math.sqrt(b[0] / rho), z6_domain(row), f"B {b[1]}; rho {rsrc}")

    return model


DW_FIT = {"Al": (1500.0, 0.19), "Ti": (1280.0, 0.21)}  # Dowding2020 Fig. 6: v_cr = F d^-n (m/s, um)


def dw_size_law(row: Row, props: dict) -> Prediction:
    """Dowding2020 power law, Al and Ti matched pairs only; domain 5-50 um, room temperature, polished."""
    if not row.matched or row.particle not in DW_FIT or row.d_um is None:
        return Prediction(None, False, "Al/Ti matched with a diameter only")
    f, n = DW_FIT[row.particle]
    dom = row.room_temperature and row.substrate_condition.startswith("polished") and 5.0 <= row.d_um <= 50.0
    return Prediction(f * row.d_um ** (-n), dom, "Dowding2020 fit")


ASSADI_FE = {"Cu": 562.5, "Al": 675.0}  # Assadi2003 FE (type-1 simulation entry): Cu 545-580, Al 675 m/s


def assadi_fe_literature(row: Row, props: dict) -> Prediction:
    """Published FE critical velocities (process quantity, 5-100 um): declared out of domain for LIPIT rows."""
    if not row.matched or row.particle not in ASSADI_FE:
        return Prediction(None, False, "Cu/Al matched only")
    return Prediction(ASSADI_FE[row.particle], False, "process-quantity FE value (Assadi2003)")


def make_baseline(rows: list[Row]) -> Callable[[Row, dict], Prediction]:
    """Leave-one-material-out median of the H20 matched-pair midpoints (property-free baseline)."""
    ref = [(r.particle, r.mid) for r in rows if r.id.startswith("H20") and r.matched and r.mid is not None]

    def model(row: Row, props: dict) -> Prediction:
        if not row.matched:
            return Prediction(None, False, "matched pairs only")
        vals = [m for mat, m in ref if mat != row.particle]
        if not vals:
            return Prediction(None, False, "no reference values")
        return Prediction(statistics.median(vals), z6_domain(row), f"median of {len(vals)} other materials")

    return model


def impact_ratio(particle: dict, substrate: dict) -> float | None:
    """Hassani2020 Eq. 3: R = (rho C0^2 Yd)_p / (rho C0^2 Yd)_s, from Table S1 (microscale Yd)."""
    need = ("rho_kg_m3", "C0_mps", "Yd_micro_MPa")
    if not all(k in particle and k in substrate for k in need):
        return None

    def z(p: dict) -> float:
        return p["rho_kg_m3"][0] * p["C0_mps"][0] ** 2 * p["Yd_micro_MPa"][0]

    return z(particle) / z(substrate)


def z9_regime(row: Row, props: dict) -> Prediction:
    """Z9 regime from R: < 1/2 splatting, > 2 penetration, else co-deformation. No velocity prediction."""
    p, s = props.get(row.particle), props.get(row.substrate)
    r = impact_ratio(p or {}, s or {})
    if r is None:
        return Prediction(None, False, "missing rho, C0 or Yd")
    reg = "splatting" if r < 0.5 else "penetration" if r > 2.0 else "co-deformation"
    return Prediction(None, row.room_temperature, f"R = {r:.3g}", regime=reg)


def distance(pred: float, lo: float, hi: float) -> float:
    """Score rule S1: 0 inside [lo, hi], else distance to the nearest bound divided by the midpoint."""
    mid = 0.5 * (lo + hi)
    if lo <= pred <= hi:
        return 0.0
    return (lo - pred) / mid if pred < lo else (pred - hi) / mid


def models(rows: list[Row]) -> dict[str, Callable[[Row, dict], Prediction]]:
    """The frozen zoo of the retrospective test (preregistration section 3)."""
    return {
        "Z6_a015": z6_sound_speed(0.15),
        "Z6_a014_sim": z6_sound_speed(0.14),
        "Z6_a015_C0": z6_sound_speed(0.15, use_hugoniot_c0=True),
        "DW_size": dw_size_law,
        "Assadi2003_FE": assadi_fe_literature,
        "baseline_LOMO": make_baseline(rows),
        "Z9_regime": z9_regime,
    }


def predict(rows: list[Row], props: dict) -> list[dict[str, str]]:
    """All predictions for the scored rows, without looking at the measured windows."""
    out = []
    for name, model in models(rows).items():
        for row in rows:
            if not row.id.startswith(SCORED_PREFIXES):
                continue
            p = model(row, props)
            if p.v is None and not p.regime:
                continue
            out.append({"model": name, "row": row.id, "particle": row.particle, "substrate": row.substrate,
                        "v_pred_mps": "" if p.v is None else f"{p.v:.1f}", "regime_pred": p.regime,
                        "in_domain": str(p.in_domain), "note": p.note})
    return out


def write_predictions(path: Path = DATA / "predictions_v1.csv") -> int:
    """Write predictions_v1.csv (frozen before scoring). Returns the number of rows."""
    rows = load_rows()
    preds = predict(rows, load_properties())
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(preds[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(preds)
    return len(preds)


if __name__ == "__main__":
    print(write_predictions())
