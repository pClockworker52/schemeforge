#!/usr/bin/env python3
"""PreToolUse guard for schemeforge subagents.

  guard_paths.py PREFIX [PREFIX ...]   allow file tools only inside these repo-relative prefixes
  guard_paths.py --deny PREFIX [...]   block file tools that touch these prefixes

Reads the hook JSON from stdin. Exit code 2 blocks the call and shows stderr to the agent.
"""
import json
import os
import sys


def inside(rel: str, prefix: str) -> bool:
    prefix = prefix.rstrip("/")
    return rel == prefix or rel.startswith(prefix + "/")


def main() -> int:
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())
    raw = ti.get("file_path") or ti.get("notebook_path") or ti.get("path") or "."
    path = os.path.realpath(os.path.join(root, os.path.expanduser(raw)))
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    args = sys.argv[1:]

    if args[:1] == ["--deny"]:
        for p in args[1:]:
            # A Grep/Glob rooted above the denied folder would read it too.
            above = tool in ("Grep", "Glob") and (rel == "." or inside(p.rstrip("/"), rel))
            if inside(rel, p) or above:
                print(f"Blocked: {rel} is off-limits for this agent ({p}).", file=sys.stderr)
                return 2
        return 0

    if rel.startswith("..") or not any(inside(rel, p) for p in args):
        print(f"Blocked: this agent may only write under {', '.join(args)} (tried {rel}).", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
