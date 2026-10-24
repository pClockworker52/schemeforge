"""The inner evolutionary loop (PLAN §5.9): islands keyed by hunches, single-shot LLM mutations, sandboxed
evaluation (smoke, then dev with probes), MAP-Elites archive, Pareto selection from the registry. Resumable.

State: runs/evolve/<run_id>/state.json. Candidates: candidates/<hunch>/<run_id>/. Scores: the registry only.
"""

from __future__ import annotations

import json
import math
import secrets
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

from schemeforge.core import evaluation, leaderboard, ledger, registry
from schemeforge.core.integrity import REPO_ROOT
from schemeforge.core.loader import load_function
from schemeforge.core.locks import max_parallel
from schemeforge.core.sandbox import validate_source

from . import backends, prompts
from .archive import Archive

ISLAND_CAP = 24
TOURNAMENT = 3
STAGNATION_LIMIT = 8
EVOLVE_DIR = Path("runs") / "evolve"
CANDIDATES_DIR = REPO_ROOT / "candidates"


@dataclass
class Config:
    arena: str
    slot: str
    hunches: list[str]
    gens: int = 20
    children: int = 8
    backend: str = "claude-cli"
    model: str = "sonnet"
    budget: int | None = None  # maximum number of children
    seeds: list[str] = field(default_factory=list)  # seed candidate files (default: the slot's zoo)
    stagnation: int = STAGNATION_LIMIT
    rng_seed: int = 0
    suite: str = "dev"  # selection suite after the smoke gate ("smoke" only for fast tests)
    wild_model: str | None = "haiku"  # cheaper model for the "wild" operator (PLAN §5.9); None = same model


@dataclass
class State:
    run_id: str
    config: Config
    generation: int = 0
    children_made: int = 0
    stagnation: int = 0
    islands: dict[str, list[str]] = field(default_factory=dict)  # hunch -> candidate ids
    archive: dict[str, Any] = field(default_factory=dict)
    front: list[str] = field(default_factory=list)  # Pareto rank-0 ids after the last generation
    history: list[dict[str, Any]] = field(default_factory=list)

    @property
    def dir(self) -> Path:
        return EVOLVE_DIR / self.run_id

    def save(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        tmp = self.dir / "state.json.tmp"
        tmp.write_text(json.dumps({**asdict(self), "config": asdict(self.config)}, indent=1), encoding="utf-8")
        tmp.replace(self.dir / "state.json")

    @classmethod
    def load(cls, run_id: str) -> State:
        d = json.loads((EVOLVE_DIR / run_id / "state.json").read_text(encoding="utf-8"))
        d["config"] = Config(**{k: v for k, v in d["config"].items() if k in Config.__dataclass_fields__})
        return cls(**d)


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


# --- evaluation of one file ---------------------------------------------------------------------------------
def evaluate_child(path: Path, cfg: Config, hunch: str, parents: list[str]) -> dict[str, Any]:
    """Smoke, then dev with probes; register under the hunch. Returns a small summary dict."""
    smoke = evaluation.evaluate_file(path, cfg.arena, cfg.slot, "smoke", probe=cfg.suite == "smoke")
    cid = evaluation.submit_candidate(path, hunch, parents, origin="engine")
    if smoke.report["status"] != "ok" or cfg.suite == "smoke":
        if cfg.suite == "smoke":
            return {"id": cid, "status": smoke.report["status"], "stage": "smoke", "run_id": smoke.run_id,
                    "violations": smoke.report.get("violations", [])[:3], "probe": smoke.report.get("probe", {})}
        return {"id": cid, "status": "rejected", "stage": "smoke", "violations": smoke.report["violations"][:3]}
    dev = evaluation.evaluate_file(path, cfg.arena, cfg.slot, cfg.suite, probe=True)
    return {"id": cid, "status": dev.report["status"], "stage": "dev", "run_id": dev.run_id,
            "violations": dev.report.get("violations", [])[:3], "probe": dev.report.get("probe", {})}


# --- one child -------------------------------------------------------------------------------------------------
def _parent_view(cid: str, rows: dict[str, leaderboard.Row], keys: list[str]) -> dict[str, Any]:
    conn = registry.connect()
    path = conn.execute("SELECT path FROM candidates WHERE id = ?", (cid,)).fetchone()["path"]
    conn.close()
    p = Path(path) if Path(path).is_absolute() else REPO_ROOT / path
    r = rows[cid]
    return {"id": cid, "code": p.read_text(encoding="utf-8"),
            "summary": prompts.report_summary(r.values, r.vs_zoo, keys)}


def make_child(state: State, hunch: dict[str, Any], operator: str, parents: list[str],
               rows: dict[str, leaderboard.Row], archive_ctx: list[str], index: int) -> dict[str, Any]:
    cfg = state.config
    keys = [f"{c}.{m}" for c, m, _ in leaderboard.objectives(cfg.arena, cfg.slot)]
    prompt = prompts.user_prompt(cfg.arena, cfg.slot, hunch, [_parent_view(p, rows, keys) for p in parents],
                                 archive_ctx, operator)
    model = cfg.wild_model if operator == "wild" and cfg.wild_model and cfg.backend != "dummy" else cfg.model
    backend = backends.make_backend(cfg.backend, model, seed=cfg.rng_seed * 100003 + index)
    comp = backend.complete(prompt)
    out_dir = CANDIDATES_DIR / hunch["id"] / state.run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"g{state.generation:03d}_{index:03d}_{operator}"
    result: dict[str, Any] = {"operator": operator, "parents": parents, "hunch": hunch["id"]}
    conn = registry.connect()
    try:
        if comp.data is None:
            backends.log_call(conn, backend, prompt, comp, None)
            return {**result, "status": "llm_error", "error": comp.error, "unreached": comp.unreached}
        path = out_dir / f"{stem}.py"
        path.write_text(comp.data["code"], encoding="utf-8")
        (out_dir / f"{stem}.json").write_text(json.dumps({k: comp.data[k] for k in ("rationale", "expected_change")}
                                                         | {"operator": operator, "parents": parents}, indent=1))
        if not validate_source(comp.data["code"]).ok:  # cheap pre-check; the worker validates again
            cid = evaluation.submit_candidate(path, hunch["id"], parents, origin="engine")
            backends.log_call(conn, backend, prompt, comp, cid)
            v = [str(x) for x in validate_source(comp.data["code"]).violations[:3]]
            return {**result, "id": cid, "status": "rejected", "stage": "sandbox", "violations": v}
        summary = evaluate_child(path, cfg, hunch["id"], parents)
        backends.log_call(conn, backend, prompt, comp, summary["id"])
        return {**result, **summary, "cost_usd": comp.cost_usd}
    finally:
        conn.close()


# --- generation ------------------------------------------------------------------------------------------------
def _tournament(rng: np.random.Generator, members: list[str], rows: dict[str, leaderboard.Row]) -> str:
    pool = [m for m in members if m in rows]
    pick = rng.choice(pool, size=min(TOURNAMENT, len(pool)), replace=False)
    return min(pick, key=lambda c: rows[c].key)


def _archive_context(archive: Archive, rows: dict[str, leaderboard.Row], rng: np.random.Generator) -> list[str]:
    elites = [c for c in archive.members() if c in rows]
    pick = rng.choice(elites, size=min(3, len(elites)), replace=False) if elites else []
    return [f"{c}: Pareto rank {rows[c].rank}, score {rows[c].score:.3f} x zoo" for c in pick]


def seed_islands(state: State) -> None:
    """Evaluate the seeds (or take the zoo's latest dev runs) and put them on every island."""
    cfg = state.config
    seeds = [Path(s) for s in cfg.seeds]
    if not seeds:
        import importlib

        zoo = importlib.import_module(f"schemeforge.arenas.{cfg.arena}.zoo")
        seeds = list(zoo.members(cfg.slot).values())
    ids = []
    conn = registry.connect()
    rows = {r.candidate_id: r for r in leaderboard.build(conn, cfg.arena, cfg.slot, suite=cfg.suite)}
    conn.close()
    with ThreadPoolExecutor(max_workers=max_parallel()) as pool:
        futs = []
        for s in seeds:
            futs.append(pool.submit(_seed_one, s, cfg, rows))
        ids = [f.result() for f in futs]
    archive = Archive(cfg.arena, cfg.slot)
    _zoo_references(archive)
    state.archive = archive.to_dict()
    state.islands = {h: [i for i in ids if i] for h in cfg.hunches}


def _seed_one(path: Path, cfg: Config, rows: dict[str, leaderboard.Row]) -> str | None:
    conn = registry.connect()
    cid = evaluation.register_candidate(conn, path, cfg.arena, cfg.slot, origin="seed")
    conn.close()
    if cid in rows:
        return cid
    res = evaluation.evaluate_file(path, cfg.arena, cfg.slot, cfg.suite, probe=True)
    return cid if res.report["status"] == "ok" else None


def _zoo_references(archive: Archive) -> None:
    """Fingerprints of the zoo (trusted judge files, probed in-process)."""
    import importlib

    from .probes import probe

    zoo = importlib.import_module(f"schemeforge.arenas.{archive.arena}.zoo")
    for name, path in zoo.members(archive.slot).items():
        fn = load_function(path, zoo.SLOT_FUNCTIONS[archive.slot])
        archive.references[name] = probe(fn, archive.arena, archive.slot).get("fingerprint", [])


def archive_progress(results: list[dict[str, Any]]) -> bool:
    """True if a child of this generation filled a new archive cell or replaced an elite."""
    return any(str(r.get("archive", "")).startswith(("new cell", "replaced")) for r in results)


def run_generation(state: State, rng: np.random.Generator) -> dict[str, Any]:
    cfg = state.config
    conn = registry.connect()
    rows = {r.candidate_id: r for r in leaderboard.build(conn, cfg.arena, cfg.slot, suite=cfg.suite)}
    conn.close()
    archive = Archive.from_dict(state.archive)
    hunches = {h: ledger.get(h) for h in cfg.hunches}
    ops, weights = zip(*prompts.OPERATOR_WEIGHTS.items(), strict=True)
    jobs = []
    index = 0
    for h in cfg.hunches:
        for _ in range(cfg.children):
            if cfg.budget is not None and state.children_made + len(jobs) >= cfg.budget:
                break
            op = str(rng.choice(ops, p=np.array(weights) / sum(weights)))
            parents = [_tournament(rng, state.islands[h], rows)]
            if op == "crossover":
                other = [c for hh, m in state.islands.items() for c in m if hh != h] or state.islands[h]
                parents.append(_tournament(rng, other, rows))
            jobs.append((hunches[h], op, parents, _archive_context(archive, rows, rng) if op == "explore" else [],
                         index))
            index += 1
    with ThreadPoolExecutor(max_workers=max_parallel()) as pool:
        results = list(pool.map(lambda j: _safe_child(state, rows, *j), jobs))
    # a request that never reached the model (usage limit) did not make a child (round 3: gen 18 lost all 24)
    state.children_made += sum(not r.get("unreached") for r in results)

    conn = registry.connect()
    rows = {r.candidate_id: r for r in leaderboard.build(conn, cfg.arena, cfg.slot, suite=cfg.suite)}
    conn.close()
    placed = 0
    for res in results:
        cid = res.get("id")
        if res.get("status") != "ok" or cid not in rows:
            continue
        outcome = archive.offer(cid, res.get("probe") or {}, rows[cid].score,
                                lambda c: rows[c].score if c in rows else math.inf)
        res["archive"] = outcome
        if not outcome.startswith("duplicate"):
            island = state.islands[res["hunch"]]
            island.append(cid)
            island.sort(key=lambda c: rows[c].key if c in rows else (math.inf, math.inf, math.inf))
            del island[ISLAND_CAP:]
            placed += 1
    front = sorted(c for c, r in rows.items() if r.rank == 0)
    new_front = [c for c in front if c not in state.front and any(r.get("id") == c for r in results)]
    # with 7 objectives nearly every distinct child is non-dominated, so stagnation counts generations without
    # archive progress instead (DECISIONS.md, Gate 2)
    state.stagnation = 0 if archive_progress(results) else state.stagnation + 1
    state.front = front
    state.archive = archive.to_dict()
    summary = {"generation": state.generation, "finished": _now(), "children": len(jobs),
               "ok": sum(r.get("status") == "ok" for r in results),
               "rejected": sum(r.get("status") == "rejected" for r in results),
               "llm_errors": sum(r.get("status") == "llm_error" for r in results),
               "unreached": sum(bool(r.get("unreached")) for r in results),
               "duplicates": sum(str(r.get("archive", "")).startswith("duplicate") for r in results),
               "placed": placed, "new_front": new_front, "cost_usd": sum(r.get("cost_usd") or 0 for r in results)}
    with (state.dir / "children.jsonl").open("a", encoding="utf-8") as fh:
        for r in results:
            fh.write(json.dumps({**r, "generation": state.generation}, default=str) + "\n")
    state.history.append(summary)
    state.generation += 1
    state.save()
    return summary


def _safe_child(state, rows, hunch, op, parents, ctx, index) -> dict[str, Any]:
    try:
        return make_child(state, hunch, op, parents, rows, ctx, index)
    except Exception as exc:  # noqa: BLE001 - one failing child must not end the generation
        return {"status": "error", "error": f"{type(exc).__name__}: {exc}", "operator": op, "hunch": hunch["id"]}


def evolve(cfg: Config | None = None, resume: str | None = None, log=print) -> State:
    if resume:
        state = State.load(resume)
    else:
        assert cfg is not None
        for h in cfg.hunches:
            hh = ledger.get(h)
            if (hh["arena"], hh["slot"]) != (cfg.arena, cfg.slot):
                raise ValueError(f"hunch {h} is for {hh['arena']}/{hh['slot']}, not {cfg.arena}/{cfg.slot}")
        run_id = f"e-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(2)}"
        state = State(run_id, cfg)
        state.dir.mkdir(parents=True, exist_ok=True)
        log(f"evolve {run_id}: seeding {len(cfg.hunches)} island(s)")
        seed_islands(state)
        state.save()
    cfg = state.config
    rng = np.random.default_rng([cfg.rng_seed, state.generation])
    while state.generation < cfg.gens:
        if cfg.budget is not None and state.children_made >= cfg.budget:
            log("budget exhausted")
            break
        if state.stagnation >= cfg.stagnation:
            log(f"no new archive cell or better elite for {state.stagnation} generations")
            break
        s = run_generation(state, rng)
        log(f"gen {s['generation']}: {s['children']} children, {s['ok']} ok, {s['rejected']} rejected, "
            f"{s['llm_errors']} llm errors, {s['duplicates']} duplicates, {s['placed']} placed, "
            f"new front {len(s['new_front'])}, cost ${s['cost_usd']:.3f}")
        if s["children"] and s["unreached"] >= max(1, s["children"] // 2):
            log(f"pausing: {s['unreached']} of {s['children']} requests did not reach the model (usage or rate "
                f"limit). State saved; continue later with --resume {state.run_id}")
            break
        rng = np.random.default_rng([cfg.rng_seed, state.generation])
    return state
