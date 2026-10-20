"""Dossier skeleton from the registry (temporary registry; a zoo member as the subject)."""

import pytest

from schemeforge.arenas.euler1d import zoo
from schemeforge.core import dossier, evaluation


def test_dossier_for_a_smoke_evaluated_candidate(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SFORGE_MAX_PARALLEL", "2")
    monkeypatch.setattr(dossier, "DOSSIERS", tmp_path / "dossiers")
    res = evaluation.evaluate_file(zoo.members("limiter")["van_albada"], "euler1d", "limiter", "smoke")
    readme = dossier.build(res.candidate_id)
    text = readme.read_text()
    assert text.startswith(f"# {res.candidate_id} — Van Albada limiter")
    assert "No promo run under" in text and "## Mechanism" in text and "def phi(r):" in text
    assert (tmp_path / "dossiers" / res.candidate_id / "candidate.py").exists()
    with pytest.raises(KeyError):
        dossier.build("c-does-not-exist")
