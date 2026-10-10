#!/usr/bin/env python3
"""PreToolUse hook for Bash commands.

Reads the hook JSON from stdin and blocks (exit code 2, reason on stderr)
commands that break the repository rules in CLAUDE.md:

* pushing to main / master, or force-pushing anything
* merging pull requests from the command line
* committing files that must never be in git (data, rasters, model weights,
  secrets), checked against the staged file list at commit time

Everything else is allowed through; the normal permission rules in
.claude/settings.json still apply afterwards.
"""
import json
import re
import subprocess
import sys

# File patterns that must never be committed (CLAUDE.md rule 10).
FORBIDDEN_STAGED = re.compile(
    r"(^|/)(data/(raw|interim|processed|external)/"
    r"|\.env(\..*)?$"
    r"|.*\.(tif|tiff|jp2|nc|zarr|pt|pth|ckpt|safetensors|onnx|pkl|pmtiles)$)"
)


def block(reason: str) -> None:
    # Exit code 2 on PreToolUse blocks the call and shows stderr to Claude.
    print(reason, file=sys.stderr)
    sys.exit(2)


def current_branch() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip()
    except Exception:
        return ""


def staged_files() -> list[str]:
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, timeout=10,
        )
        return [line for line in out.stdout.splitlines() if line]
    except Exception:
        return []


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    command = payload.get("tool_input", {}).get("command", "") or ""

    if re.search(r"\bgit\s+push\b", command):
        if re.search(r"(--force|--force-with-lease|\s-f\b)", command):
            block("Blocked: force push. Rewrite history only with the user's explicit approval.")
        # Match main/master only as a whole token, so "feat/main-menu" is not blocked.
        if re.search(r"(?<![\w/.-])(main|master)(?![\w/.-])", command):
            block("Blocked: pushing to main. Push a feature branch and open a draft PR.")
        if current_branch() in ("main", "master") and "origin" in command:
            block("Blocked: you are on main. Create a branch (git switch -c feat/<issue>-<slug>) first.")

    if re.search(r"\bgh\s+pr\s+merge\b", command):
        block("Blocked: the user merges pull requests, not the agent.")

    if re.search(r"\bgit\s+commit\b", command):
        if current_branch() in ("main", "master"):
            block("Blocked: committing on main. Use a feature branch.")
        bad = [f for f in staged_files() if FORBIDDEN_STAGED.search(f)]
        if bad:
            block(
                "Blocked: staged files must never be committed (data, rasters, weights, secrets): "
                + ", ".join(bad[:10])
            )

    sys.exit(0)


if __name__ == "__main__":
    main()
