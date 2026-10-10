#!/usr/bin/env python3
"""PreToolUse hook for Edit and Write.

Blocks writes into places where the agent must not put files:
* secrets (.env files) -- credentials never go into the repo
* data/raw -- raw downloads are immutable inputs; processed data goes elsewhere
* the test split definition once frozen (configs/splits/frozen_*), because
  silently changing the test blocks invalidates every reported result
"""
import json
import re
import sys

PROTECTED = [
    (re.compile(r"(^|/)\.env(\..*)?$"), "secrets files are never written by the agent"),
    (re.compile(r"(^|/)data/raw/"), "data/raw is read-only input; write derived data to data/interim or data/processed"),
    (re.compile(r"(^|/)configs/splits/frozen_"), "frozen split files must not change; supersede them with a new ADR and a new file"),
]


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    path = payload.get("tool_input", {}).get("file_path", "") or ""
    for pattern, why in PROTECTED:
        if pattern.search(path):
            print(f"Blocked write to {path}: {why}.", file=sys.stderr)
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
