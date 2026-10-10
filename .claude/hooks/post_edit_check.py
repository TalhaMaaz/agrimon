#!/usr/bin/env python3
"""PostToolUse hook for Edit and Write.

After a Python file is changed, run ruff on that single file so style and
obvious bugs are caught immediately. This cannot block (the edit already
happened); on failure it prints the findings to stderr with exit code 2 so
the agent sees them and fixes them in the next step.

If ruff is not installed yet (before Phase 0 tooling exists) the hook does
nothing instead of failing.
"""
import json
import shutil
import subprocess
import sys


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    path = payload.get("tool_input", {}).get("file_path", "") or ""
    if not path.endswith(".py"):
        sys.exit(0)

    ruff = shutil.which("ruff")
    if ruff is None:
        sys.exit(0)

    result = subprocess.run([ruff, "check", path], capture_output=True, text=True, timeout=50)
    if result.returncode != 0:
        print(result.stdout + result.stderr, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
