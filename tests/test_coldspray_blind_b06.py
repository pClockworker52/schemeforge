"""B06 predictions follow the frozen input rules (docs/research/coldspray-preregistration-b06.md)."""

from schemeforge.research import coldspray_blind_b06 as b06


def _by_model() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for p in b06.predict():
        out.setdefault(p["model"], []).append(p)
    return out


def test_two_conditions_seven_models() -> None:
    preds = b06.predict()
    assert {p["row"] for p in preds} == {"B06-c1", "B06-c2"}
    assert len(preds) == 14


def test_zoo_values_equal_across_conditions_and_out_of_domain() -> None:
    m = _by_model()
    for name in ("Z6_a015", "Z6_a015_C0", "baseline_LOMO"):
        vals = {p["v_pred_mps"] for p in m[name]}
        assert len(vals) == 1 and vals != {""}, name
        assert all(p["in_domain"] == "False" for p in m[name]), name


def test_models_without_inputs_give_no_prediction_with_reason() -> None:
    m = _by_model()
    for name in ("DW_size", "CS-10", "Z18_static", "Z18_Yd"):
        assert all(p["v_pred_mps"] == "" and p["note"] for p in m[name]), name


def test_written_file_matches_predict() -> None:
    import csv

    with open(b06.OUT, newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert rows == b06.predict()
