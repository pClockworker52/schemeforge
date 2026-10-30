"""The sforge MCP server: tool list, guards, and the tools that do not need a full evaluation."""

import asyncio

import pytest
import yaml

from schemeforge import mcp_server as ms
from schemeforge.core import ledger, quarantine


def test_tool_list() -> None:
    names = {t.name for t in asyncio.run(ms.server.list_tools())}
    assert names == {"eval", "submit", "leaderboard", "hunch_list", "hunch_show", "hunch_add", "case_propose",
                     "judge_version"}


def test_eval_guards() -> None:
    with pytest.raises(ms.ToolError, match="promo"):
        ms.eval_tool("src/schemeforge/arenas/euler1d/zoo/limiter/minmod.py", "euler1d", "limiter", suite="promo")
    with pytest.raises(ms.ToolError, match="outside the repository"):
        ms.eval_tool("/etc/passwd", "euler1d", "limiter", suite="smoke")
    with pytest.raises(ms.ToolError, match="outside the repository"):
        ms.eval_tool("../../../etc/passwd", "euler1d", "limiter", suite="smoke")


def test_hunch_and_case_tools(tmp_path, monkeypatch) -> None:
    lp = tmp_path / "hunches.yaml"
    lp.write_text("[]\n")
    monkeypatch.setattr(ledger, "LEDGER", lp)
    monkeypatch.setattr(quarantine, "QUARANTINE", tmp_path / "quarantine")
    monkeypatch.chdir(tmp_path)
    draft = ms.REPO_ROOT / "ledger" / "drafts" / "_test_mcp_draft.yaml"
    case = ms.REPO_ROOT / "cases" / "quarantine" / "_test_mcp_case.yaml"
    draft.write_text(yaml.safe_dump({
        "arena": "euler1d", "slot": "limiter", "lens": "contrarian", "statement": "s", "mechanism": "m",
        "predicted_effect": [{"metric": "shock_width", "direction": "down", "size": "0.3 cells"}],
        "kill_criterion": "k", "known_relatives": [], "author": "hunch-generator/contrarian"}))
    case.write_text(yaml.safe_dump({"kind": "riemann", "id": "draft", "left": [1.0, 0.0, 1.0],
                                    "right": [0.2, 0.0, 0.05], "t_end": 0.1, "n": 100}))
    try:
        hid = ms.hunch_add_tool(str(draft.relative_to(ms.REPO_ROOT)))["id"]
        assert hid == "H-0001" and ms.hunch_list_tool()[0]["lens"] == "contrarian"
        assert ms.hunch_show_tool(hid)["status"] == "open"
        cid = ms.case_propose_tool(str(case.relative_to(ms.REPO_ROOT)), "euler1d")["case_id"]
        assert cid == "B-0001" and (tmp_path / "quarantine" / "B-0001.yaml").exists()
    finally:
        draft.unlink()
        case.unlink()


def test_inadmissible_case_is_refused(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(quarantine, "QUARANTINE", tmp_path / "quarantine")
    monkeypatch.chdir(tmp_path)
    bad = ms.REPO_ROOT / "cases" / "quarantine" / "_test_mcp_bad.yaml"
    bad.write_text(yaml.safe_dump({"kind": "riemann", "id": "x", "left": [1, -20, 0.4], "right": [1, 20, 0.4],
                                   "t_end": 0.1, "n": 100}))
    try:
        with pytest.raises(ValueError):
            ms.case_propose_tool(str(bad.relative_to(ms.REPO_ROOT)), "euler1d")
    finally:
        bad.unlink()


def test_judge_version_tool() -> None:
    v = ms.judge_version_tool("euler1d")
    assert v["version"].startswith("euler1d-v") and len(v["hash"]) == 64
