"""Gate 2 end-to-end engine run in an isolated working directory (own registry, ledger and candidates), so
calibration runs never mix with the project's ledger and registry.

    uv run python scripts/e2e_evolve.py start  WORKDIR --backend dummy --gens 13 --children 8 --budget 208
    uv run python scripts/e2e_evolve.py resume WORKDIR RUN_ID
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

def calibration_hunch(k: int) -> dict:
    return {"arena": "euler1d", "slot": "limiter", "lens": "human",
            "statement": f"Calibration island {k + 1}: find a good MUSCL slope limiter (engine calibration C1, "
                         "not a research hunch).",
            "mechanism": "Engine calibration only: textbook limiters are expected to reappear.",
            "predicted_effect": [{"metric": "R1.shock_width", "direction": "down", "size": "towards the zoo"}],
            "kill_criterion": "n/a (calibration)", "known_relatives": ["all zoo limiters"],
            "author": "orchestrator"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["start", "resume"])
    ap.add_argument("workdir")
    ap.add_argument("run_id", nargs="?")
    ap.add_argument("--backend", default="dummy")
    ap.add_argument("--model", default="dummy")
    ap.add_argument("--gens", type=int, default=13)
    ap.add_argument("--children", type=int, default=8)
    ap.add_argument("--budget", type=int, default=208)
    ap.add_argument("--seed", action="append", default=[])
    ap.add_argument("--islands", type=int, default=2)
    a = ap.parse_args()

    work = Path(a.workdir).resolve()
    work.mkdir(parents=True, exist_ok=True)
    os.chdir(work)  # registry, reports and evolve state live under WORKDIR/runs/
    from schemeforge.core import ledger
    from schemeforge.engine import evolve

    ledger.LEDGER = work / "hunches.yaml"
    evolve.CANDIDATES_DIR = work / "candidates"
    if a.mode == "start":
        if not ledger.LEDGER.exists():
            ledger.LEDGER.write_text("[]\n")
            for k in range(a.islands):
                ledger.add(calibration_hunch(k))
        ids = [h["id"] for h in ledger.load()]
        cfg = evolve.Config("euler1d", "limiter", ids, gens=a.gens, children=a.children, backend=a.backend,
                            model=a.model, budget=a.budget, seeds=[str(Path(s).resolve()) for s in a.seed])
        state = evolve.evolve(cfg, log=lambda m: print(m, flush=True))
    else:
        state = evolve.evolve(resume=a.run_id, log=lambda m: print(m, flush=True))
    print(f"{state.run_id}: generation {state.generation}, children {state.children_made}, front {len(state.front)}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(REPO / "src"))
    sys.exit(main())
