"""The hunch ledger (PLAN §6): ledger/hunches.yaml is the only source of truth for hunches."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .integrity import REPO_ROOT

LEDGER = REPO_ROOT / "ledger" / "hunches.yaml"
HEADER = "# The hunch ledger: the only source of truth for hunches (PLAN §6). Edited through `sforge hunch ...` only.\n"
ARENAS = {"euler1d", "euler2d", "contact"}
LENSES = {"steady-convergence", "shock physics", "approximation theory", "structure preservation", "practitioner",
          "contrarian", "transfer", "human"}
STATUSES = {"open", "testing", "supported", "refuted", "inconclusive", "merged"}
VERDICTS = {"supported", "refuted", "inconclusive", "merged"}
REQUIRED = ("arena", "slot", "lens", "statement", "mechanism", "predicted_effect", "kill_criterion",
            "known_relatives", "author")


class LedgerError(ValueError):
    pass


def load(path: Path | None = None) -> list[dict[str, Any]]:
    path = path or LEDGER
    data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else None
    return list(data or [])


def save(hunches: list[dict[str, Any]], path: Path | None = None) -> None:
    path = path or LEDGER
    body = yaml.safe_dump(hunches, sort_keys=False, allow_unicode=True, width=110) if hunches else "[]\n"
    path.write_text(HEADER + body, encoding="utf-8")


def validate(d: dict[str, Any]) -> list[str]:
    """Problems with a hunch draft (empty = valid), following ledger/schema.yaml."""
    errs = [f"missing field {k!r}" for k in REQUIRED if k not in d]
    if d.get("arena") is not None and d["arena"] not in ARENAS:
        errs.append(f"arena must be one of {sorted(ARENAS)}")
    if d.get("lens") is not None and d["lens"] not in LENSES:
        errs.append(f"lens must be one of {sorted(LENSES)}")
    for k in ("slot", "statement", "mechanism", "kill_criterion", "author"):
        if k in d and (not isinstance(d[k], str) or not d[k].strip()):
            errs.append(f"{k!r} must be a non-empty string")
    eff = d.get("predicted_effect")
    if "predicted_effect" in d:
        if not isinstance(eff, list) or not eff:
            errs.append("'predicted_effect' must be a non-empty list")
        else:
            for i, e in enumerate(eff):
                if not isinstance(e, dict) or not {"metric", "direction", "size"} <= set(e):
                    errs.append(f"predicted_effect[{i}] needs metric, direction and size")
                elif e["direction"] not in ("up", "down", "same"):
                    errs.append(f"predicted_effect[{i}].direction must be up, down or same")
    if "known_relatives" in d and not isinstance(d["known_relatives"], list):
        errs.append("'known_relatives' must be a list (empty only if none are known)")
    if d.get("status", "open") not in STATUSES:
        errs.append(f"status must be one of {sorted(STATUSES)}")
    return errs


def add(draft: dict[str, Any], path: Path | None = None) -> str:
    errs = validate(draft)
    if errs:
        raise LedgerError("; ".join(errs))
    hunches = load(path)
    n = max((int(h["id"][2:]) for h in hunches), default=0) + 1
    hid = f"H-{n:04d}"
    entry = {"id": hid, **{k: v for k, v in draft.items() if k != "id"}}
    entry.setdefault("status", "open")
    entry.setdefault("verdict_note", "")
    hunches.append(entry)
    save(hunches, path)
    return hid


def get(hid: str, path: Path | None = None) -> dict[str, Any]:
    for h in load(path):
        if h["id"] == hid:
            return h
    raise LedgerError(f"no hunch {hid}")


def update(hid: str, path: Path | None = None, **fields: Any) -> dict[str, Any]:
    hunches = load(path)
    for h in hunches:
        if h["id"] == hid:
            h.update(fields)
            save(hunches, path)
            return h
    raise LedgerError(f"no hunch {hid}")


def close(hid: str, verdict: str, note: str, path: Path | None = None) -> dict[str, Any]:
    if verdict not in VERDICTS:
        raise LedgerError(f"verdict must be one of {sorted(VERDICTS)}")
    if not note.strip():
        raise LedgerError("a verdict needs a note with evidence (run ids)")
    return update(hid, path, status=verdict, verdict_note=note)
