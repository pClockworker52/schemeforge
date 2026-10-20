"""Breaker cases: proposed into cases/quarantine/, accepted by Peter into the judge tree (PLAN §5.5, §11.3).

Accepting a case changes the judge: it moves into src/schemeforge/arenas/<arena>/cases/accepted/, after which the
judge version must be bumped, committed, tagged and the zoo and archive rescored.
"""

from __future__ import annotations

import importlib
import re
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from . import registry
from .integrity import ARENAS_DIR, REPO_ROOT

QUARANTINE = REPO_ROOT / "cases" / "quarantine"


def _rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(p.resolve())


def _next_id(conn) -> str:
    ids = [r[0] for r in conn.execute("SELECT id FROM cases WHERE id LIKE 'B-%'")]
    ids += [p.stem for p in QUARANTINE.glob("B-*.yaml")]
    n = max((int(m.group(1)) for i in ids if (m := re.fullmatch(r"B-(\d+)", i))), default=0) + 1
    return f"B-{n:04d}"


def propose(path: Path, arena: str, proposed_by: str = "breaker",
            registry_path: Path = registry.DEFAULT_PATH) -> str:
    """Validate a case file and put it into quarantine under a fresh id. Raises ValueError if inadmissible."""
    cases = importlib.import_module(f"schemeforge.arenas.{arena}.cases")
    d: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        raise ValueError("a case file holds one YAML mapping")
    conn = registry.connect(registry_path)
    d["id"] = _next_id(conn)
    cases.validate_case(cases.case_from_dict(d))  # raises on inadmissible cases
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    out = QUARANTINE / f"{d['id']}.yaml"
    out.write_text(yaml.safe_dump(d, sort_keys=False), encoding="utf-8")
    conn.execute("INSERT INTO cases (id, arena, family, status, path, proposed_by, created_at) "
                 "VALUES (?, ?, ?, 'quarantine', ?, ?, ?)",
                 (d["id"], arena, d.get("kind"), _rel(out), proposed_by,
                  datetime.now(UTC).isoformat(timespec="seconds")))
    conn.commit()
    conn.close()
    return d["id"]


def accept(case_id: str, registry_path: Path = registry.DEFAULT_PATH) -> Path:
    """Move a quarantined case into the judge tree (Peter only; the CLI asks for confirmation)."""
    conn = registry.connect(registry_path)
    row = conn.execute("SELECT arena, status, path FROM cases WHERE id = ?", (case_id,)).fetchone()
    if row is None or row["status"] != "quarantine":
        raise ValueError(f"{case_id} is not a quarantined case")
    src = Path(row["path"]) if Path(row["path"]).is_absolute() else REPO_ROOT / row["path"]
    dest_dir = ARENAS_DIR / row["arena"] / "cases" / "accepted"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.move(str(src), dest)
    conn.execute("UPDATE cases SET status = 'accepted', path = ? WHERE id = ?",
                 (_rel(dest), case_id))
    conn.commit()
    conn.close()
    return dest
