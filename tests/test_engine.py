"""Evolution engine: probes, archive, prompts, backends (no real LLM calls) and an end-to-end dummy run."""

import json
import os
import stat

import pytest

from schemeforge.arenas.euler1d import zoo
from schemeforge.core import ledger, registry
from schemeforge.core.sandbox import validate_source
from schemeforge.engine import archive as arch
from schemeforge.engine import backends, evolve, prompts
from schemeforge.engine.probes import fingerprint_distance, probe


def test_limiter_probes_separate_smooth_and_kinked() -> None:
    mm = probe(zoo.load("limiter", "minmod"), "euler1d", "limiter")
    va = probe(zoo.load("limiter", "van_albada"), "euler1d", "limiter")
    sb = probe(zoo.load("limiter", "superbee"), "euler1d", "limiter")
    # a kink seen through finite differences (h = 0.01) gives |phi''| ~ 1/h = 100; van Albada ~1.7
    assert mm["descriptors"]["smoothness"] > 30 * va["descriptors"]["smoothness"]
    assert sb["descriptors"]["compressiveness"] > va["descriptors"]["compressiveness"] > mm["descriptors"][
        "compressiveness"]
    assert len(mm["fingerprint"]) == 64 and fingerprint_distance(mm["fingerprint"], va["fingerprint"]) > 1e-2


def test_reconstruction_probes() -> None:
    from schemeforge.arenas.euler1d.numerics import muscl

    d = {n: probe(f, "euler1d", "reconstruction")["descriptors"] for n, f in [
        ("first", zoo.load("reconstruction", "first_order")), ("weno", zoo.load("reconstruction", "weno5z")),
        ("thinc", zoo.load("reconstruction", "thinc_bvd")), ("minmod", muscl(zoo.load("limiter", "minmod"))),
        ("superbee", muscl(zoo.load("limiter", "superbee")))]}
    assert d["first"]["compressiveness"] == 0.0
    assert d["minmod"]["compressiveness"] < d["superbee"]["compressiveness"] < d["thinc"]["compressiveness"]
    assert d["weno"]["smooth_error"] < -4 < -3 < d["superbee"]["smooth_error"] < d["first"]["smooth_error"]
    # a frozen reconstruction differs from its plain version in the fingerprint, not in the descriptors
    plain, frozen = (probe(zoo.load("reconstruction_stateful", n), "euler1d", "reconstruction_stateful")
                     for n in ("muscl_van_leer", "muscl_van_leer_frozen"))
    assert plain["descriptors"] == frozen["descriptors"]
    assert fingerprint_distance(plain["fingerprint"], frozen["fingerprint"]) > 1e-2


def test_flux_probes() -> None:
    hllc = probe(zoo.load("flux", "hllc"), "euler1d", "flux")
    rus = probe(zoo.load("flux", "rusanov"), "euler1d", "flux")
    assert hllc["descriptors"]["contact_dissipation"] < 1e-12 < rus["descriptors"]["contact_dissipation"]


@pytest.mark.parametrize("slot, names", [
    ("limiter", ["minmod", "van_albada", "van_leer", "venkatakrishnan", "mc", "koren", "superbee"]),
    ("flux", ["rusanov", "hll", "hllc"]),
    ("reconstruction", ["first_order", "weno5z", "thinc_bvd"]),
])
def test_zoo_members_occupy_distinct_cells(slot: str, names: list[str]) -> None:
    # the grid must at least tell the known methods apart, or MAP-Elites has nothing to spread over
    cells = {arch.cell_of("euler1d", slot, probe(zoo.load(slot, n), "euler1d", slot)["descriptors"]) for n in names}
    assert len(cells) == len(names)


def test_stagnation_counts_archive_progress() -> None:
    assert evolve.archive_progress([{"archive": "rejected"}, {"archive": "new cell"}])
    assert evolve.archive_progress([{"archive": "replaced c-1"}])
    assert not evolve.archive_progress([{"archive": "rejected"}, {"archive": "duplicate:zoo:minmod"},
                                        {"status": "llm_error"}])


def test_archive_cells_duplicates_and_replacement() -> None:
    a = arch.Archive("euler1d", "limiter")
    mm = probe(zoo.load("limiter", "minmod"), "euler1d", "limiter")
    a.references["minmod"] = mm["fingerprint"]
    assert a.offer("c-copy", mm, 1.0, lambda c: 1.0) == "duplicate:zoo:minmod"
    va = probe(zoo.load("limiter", "van_albada"), "euler1d", "limiter")
    scores = {"c-1": 1.0, "c-2": 0.5}
    assert a.offer("c-1", va, 1.0, scores.get) == "new cell"
    va2 = {**va, "fingerprint": [v + 0.01 for v in va["fingerprint"]]}
    assert a.offer("c-2", va2, 0.5, scores.get) == "replaced c-1"
    assert a.members() == ["c-2"]
    assert arch.Archive.from_dict(json.loads(json.dumps(a.to_dict()))).elites == a.elites


def test_prompt_contains_contract_hunch_and_task() -> None:
    hunch = {"id": "H-0001", "statement": "s", "mechanism": "m", "predicted_effect": []}
    p = prompts.user_prompt("euler1d", "limiter", hunch, [{"id": "c-1", "code": "def phi(r): ...", "summary": "-"}],
                            ["c-9: rank 0"], "refine")
    assert "def phi(r):" in p and "## `limiter`" in p and "## `flux`" not in p
    assert "## Task: refine" in p and "c-9: rank 0" in p
    # known traps: the shared section and the slot's own, not other slots'
    assert "## Known traps" in p and "### All slots" in p and "soft max breaks the TVD bound" in p
    assert "6-cell window" not in p
    r = prompts.user_prompt("euler1d", "reconstruction", hunch, [], [], "explore")
    assert "6-cell window" in r and "soft max" not in r


def test_dummy_backend_writes_valid_candidates() -> None:
    b = backends.Dummy(seed=3)
    for _ in range(5):
        c = b.complete("x")
        assert validate_source(c.data["code"]).ok


def test_claude_cli_backend_parses_structured_output(tmp_path) -> None:
    fake = tmp_path / "fake-claude"
    # Claude Code 2.1.x prints the session's messages as a list; the last "result" item carries the output
    payload = [{"type": "system", "subtype": "init"},
               {"type": "result", "subtype": "success", "total_cost_usd": 0.0123,
                "structured_output": {"code": "def phi(r):\n    return r\n", "rationale": "r", "expected_change": "e"},
                "usage": {"input_tokens": 2, "cache_creation_input_tokens": 98, "output_tokens": 20}}]
    fake.write_text(f"#!/bin/sh\ncat > /dev/null\nprintf '%s\\n' '{json.dumps(payload)}'\n")  # echo expands \n
    fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
    b = backends.ClaudeCLI("sonnet", executable=str(fake))
    assert "--json-schema" in b.command() and "--model" in b.command()
    c = b.complete("prompt")
    assert c.data["code"].startswith("def phi") and c.cost_usd == 0.0123 and c.input_tokens == 100
    # C1 finding: at the usage limit the CLI returns a result with zero API time and no structured output
    limited = tmp_path / "limited-claude"
    lim = [{"type": "result", "subtype": "success", "duration_api_ms": 0, "is_error": True,
            "result": "usage limit reached", "usage": {}}]
    limited.write_text(f"#!/bin/sh\ncat > /dev/null\nprintf '%s\\n' '{json.dumps(lim)}'\n")
    limited.chmod(limited.stat().st_mode | stat.S_IEXEC)
    c = backends.ClaudeCLI(executable=str(limited)).complete("p")
    assert c.data is None and c.unreached and "usage limit reached" in c.error
    broken = tmp_path / "broken-claude"
    broken.write_text("#!/bin/sh\necho 'not json'\nexit 1\n")
    broken.chmod(broken.stat().st_mode | stat.S_IEXEC)
    assert backends.ClaudeCLI(executable=str(broken)).complete("p").data is None


@pytest.fixture
def sandbox_env(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SFORGE_MAX_PARALLEL", "4")
    lp = tmp_path / "hunches.yaml"
    lp.write_text("[]\n")
    monkeypatch.setattr(ledger, "LEDGER", lp)
    monkeypatch.setattr(evolve, "CANDIDATES_DIR", tmp_path / "candidates")
    hid = ledger.add({"arena": "euler1d", "slot": "limiter", "lens": "human", "statement": "smooth rational limiters",
                      "mechanism": "no kinks", "predicted_effect": [{"metric": "newton_iters", "direction": "down",
                                                                     "size": "2x"}],
                      "kill_criterion": "none in 2 rounds", "known_relatives": ["van Albada"], "author": "peter"})
    return tmp_path, hid


def test_evolve_end_to_end_with_dummy_backend_and_resume(sandbox_env) -> None:
    tmp_path, hid = sandbox_env
    seeds = [str(zoo.members("limiter")[n]) for n in ("minmod", "van_leer")]
    cfg = evolve.Config("euler1d", "limiter", [hid], gens=1, children=3, backend="dummy", seeds=seeds,
                        suite="smoke", rng_seed=1)
    state = evolve.evolve(cfg, log=lambda *_: None)
    assert state.generation == 1 and state.children_made == 3
    assert (state.dir / "state.json").exists() and len(state.islands[hid]) >= 2
    lines = (state.dir / "children.jsonl").read_text().splitlines()
    assert len(lines) == 3 and all(json.loads(x)["status"] == "ok" for x in lines)
    # resume: extend the run by one generation
    saved = json.loads((state.dir / "state.json").read_text())
    saved["config"]["gens"] = 2
    (state.dir / "state.json").write_text(json.dumps(saved))
    resumed = evolve.evolve(resume=state.run_id, log=lambda *_: None)
    assert resumed.generation == 2 and resumed.children_made == 6
    conn = registry.connect(tmp_path / "runs" / "registry.sqlite")
    rows = conn.execute("SELECT hunch_id, origin, parents FROM candidates WHERE origin = 'engine'").fetchall()
    assert len(rows) >= 1 and all(r["hunch_id"] == hid and json.loads(r["parents"]) for r in rows)
    assert conn.execute("SELECT COUNT(*) FROM llm_calls WHERE backend = 'dummy'").fetchone()[0] == 6
    assert os.path.isdir(tmp_path / "candidates" / hid / state.run_id)


def test_unreached_requests_do_not_use_the_budget(sandbox_env, monkeypatch) -> None:
    # round 3, gen 18: all 24 requests hit the usage limit and still counted against --budget
    tmp_path, hid = sandbox_env
    seeds = [str(zoo.members("limiter")[n]) for n in ("minmod", "van_leer")]
    cfg = evolve.Config("euler1d", "limiter", [hid], gens=1, children=3, backend="dummy", seeds=seeds,
                        suite="smoke", rng_seed=1)
    monkeypatch.setattr(evolve, "make_child", lambda state, hunch, op, *a, **k: {
        "status": "llm_error", "unreached": True, "error": "usage limit", "operator": op, "hunch": hunch["id"]})
    state = evolve.evolve(cfg, log=lambda *_: None)
    assert state.history[-1]["unreached"] == 3 and state.children_made == 0
