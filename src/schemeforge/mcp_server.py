"""`sforge` as an MCP server (PLAN §5.10), so that proposer, breaker and hunch-generator need no Bash.

Tools mirror the CLI: eval (smoke/dev only), submit, leaderboard, hunch_list, hunch_show, hunch_add,
case_propose, judge_version. Not exposed: promo, case accept, reveal, evolve (Peter / orchestrator only).
File arguments must lie inside the repository. Run: `uv run sforge-mcp` (stdio); configured in .mcp.json.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mcp.server.mcpserver import MCPServer

from schemeforge.core.integrity import REPO_ROOT

server = MCPServer("sforge", instructions="Evaluate and register schemeforge candidates. The judge decides: cite "
                                          "run ids for every claim about a candidate.")


class ToolError(ValueError):
    pass


def _repo_file(path: str) -> Path:
    p = (REPO_ROOT / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    if REPO_ROOT.resolve() not in p.parents:
        raise ToolError(f"{path} is outside the repository")
    if not p.is_file():
        raise ToolError(f"{path} does not exist")
    return p


def eval_tool(file: str, arena: str, slot: str, suite: str = "dev",
              case: str | None = None) -> dict[str, Any]:
    from schemeforge.core import evaluation
    from schemeforge.core.integrity import integrity_problems

    if suite not in ("smoke", "dev"):
        raise ToolError("only the smoke and dev suites are available here (promo is Peter's)")
    problems = integrity_problems(arena)
    if problems:
        raise ToolError("refusing to score: " + "; ".join(problems))
    extra = []
    if case:
        import importlib

        import yaml

        cases = importlib.import_module(f"schemeforge.arenas.{arena}.cases")
        d = yaml.safe_load(_repo_file(case).read_text(encoding="utf-8"))
        cases.validate_case(cases.case_from_dict(d))
        extra = [d]
    res = evaluation.evaluate_file(_repo_file(file), arena, slot, suite, extra)
    r = res.report
    return {"run_id": res.run_id, "candidate_id": res.candidate_id, "status": r["status"],
            "violations": r.get("violations", []), "cases": r.get("cases", {}),
            "metamorphic": r.get("metamorphic", {}), "cost_ns_per_cell_update": r.get("cost"),
            "judge_version": r.get("judge_version")}


def submit_tool(file: str, hunch: str, parents: list[str] | None = None) -> dict[str, Any]:
    from schemeforge.core import evaluation

    cid = evaluation.submit_candidate(_repo_file(file), hunch, parents or [])
    return {"candidate_id": cid, "hunch": hunch, "parents": parents or []}


def leaderboard_tool(arena: str, slot: str, pareto: bool = False, vs_zoo: bool = True,
                     top: int | None = 20) -> list[dict[str, Any]]:
    from schemeforge.core import leaderboard, registry

    rows = leaderboard.build(registry.connect(), arena, slot)
    if pareto:
        rows = [r for r in rows if r.rank == 0]
    keys = [f"{c}.{m}" for c, m, _ in leaderboard.objectives(arena, slot)]
    rows = [r for r in rows if r.duplicate_of is None]
    return [{"candidate_id": r.candidate_id, "zoo": r.is_zoo, "hunch": r.hunch_id, "run_id": r.run_id,
             "screen_fails": r.fails, "pareto_rank": r.rank, "score_vs_zoo": r.score,
             "values": {k: r.values.get(k) for k in keys},
             **({"vs_zoo": r.vs_zoo} if vs_zoo else {})} for r in rows[: top or None]]


def hunch_list_tool(open_only: bool = False) -> list[dict[str, Any]]:
    from schemeforge.core import ledger

    return [{"id": h["id"], "arena": h["arena"], "slot": h["slot"], "status": h.get("status"),
             "lens": h["lens"], "statement": " ".join(str(h["statement"]).split())}
            for h in ledger.load() if not open_only or h.get("status") in ("open", "testing")]


def hunch_show_tool(hunch_id: str) -> dict[str, Any]:
    from schemeforge.core import ledger

    return ledger.get(hunch_id)


def hunch_add_tool(file: str) -> dict[str, Any]:
    import yaml

    from schemeforge.core import ledger

    return {"id": ledger.add(yaml.safe_load(_repo_file(file).read_text(encoding="utf-8")) or {})}


def case_propose_tool(file: str, arena: str) -> dict[str, Any]:
    from schemeforge.core import quarantine

    return {"case_id": quarantine.propose(_repo_file(file), arena)}


def judge_version_tool(arena: str) -> dict[str, Any]:
    from schemeforge.core import integrity

    return {"version": integrity.judge_version(arena), "hash": integrity.tree_hash(arena=arena),
            "problems": integrity.integrity_problems(arena)}


TOOLS = {
    "eval": (eval_tool, "Sandboxed evaluation of a candidate file (suite smoke or dev); stores scores, returns the "
                        "report and run id. Optional `case`: an extra case YAML (breakers)."),
    "submit": (submit_tool, "Register a candidate file under a hunch, with parent candidate ids."),
    "leaderboard": (leaderboard_tool, "Rankings for arena/slot: fewest failed target-screen checks, then Pareto "
                                      "rank and ratio to the best zoo member; duplicates left out."),
    "hunch_list": (hunch_list_tool, "List hunches in the ledger (open_only for open and testing)."),
    "hunch_show": (hunch_show_tool, "Show one hunch."),
    "hunch_add": (hunch_add_tool, "Register a hunch draft (YAML file in ledger/drafts/); returns its id."),
    "case_propose": (case_propose_tool, "Validate a case YAML and put it into cases/quarantine/ under a new id."),
    "judge_version": (judge_version_tool, "Judge version, content hash and integrity state."),
}
for _name, (_fn, _desc) in TOOLS.items():
    server.tool(name=_name, description=_desc)(_fn)


def main() -> None:
    server.run("stdio")


if __name__ == "__main__":
    main()
