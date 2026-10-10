#!/usr/bin/env python3
"""PreToolUse hook for Bash commands.

Reads the hook JSON from stdin and blocks (exit code 2, reason on stderr)
commands that break the repository rules in CLAUDE.md:

* pushing to main / master, or force-pushing anything
* merging pull requests from the command line
* committing on main, or committing files that must never be in git (data,
  rasters, model weights, secrets), checked against the staged file list

The command is split into shell segments and only the arguments of real
`git push`, `git commit` and `gh pr merge` invocations are inspected. Text that
merely mentions them (heredocs, commit messages, PR bodies, other commands'
flags such as `gh pr create --base main`) is ignored. Issue #21.

This is the local guard for the agent only. The GitHub ruleset on main is the
server-side guard for everyone. Everything else is allowed through; the normal
permission rules in .claude/settings.json still apply afterwards.
"""

import json
import re
import shlex
import subprocess
import sys
from collections.abc import Callable

# File patterns that must never be committed (CLAUDE.md rule 10).
FORBIDDEN_STAGED = re.compile(
    r"(^|/)(data/(raw|interim|processed|external)/"
    r"|\.env(\..*)?$"
    r"|.*\.(tif|tiff|jp2|nc|zarr|pt|pth|ckpt|safetensors|onnx|pkl|pmtiles)$)"
)

PROTECTED = {"main", "master"}
SEPARATORS = {"&&", "||", ";", "|", "&", "(", ")", ";;", "|&"}
# Wrappers that run another command given as a single string argument.
SHELLS = {"bash", "sh", "zsh", "dash"}
# Words that can precede a command in a segment: wrappers, and shell keywords
# so `for ...; do git push origin main; done` is still seen.
PREFIX_WORDS = {"env", "command", "time", "nohup", "sudo", "exec", "!", "{"}
PREFIX_WORDS |= {"do", "then", "else", "elif", "if", "while", "until"}
# git global options that take a separate value (`git -C path push`).
GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
# `git push` options that take a separate value; their value is not a refspec.
PUSH_OPTS_WITH_VALUE = {"-o", "--push-option", "--repo", "--receive-pack", "--exec"}


def block(reason: str) -> None:
    # Exit code 2 on PreToolUse blocks the call and shows stderr to Claude.
    print(reason, file=sys.stderr)
    sys.exit(2)


def current_branch() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return out.stdout.strip()
    except Exception:
        return ""


def staged_files() -> list[str]:
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return [line for line in out.stdout.splitlines() if line]
    except Exception:
        return []


def tokenize(line: str) -> list[str]:
    """Split one line into shell tokens, keeping && ; | etc. as separate tokens.

    Heredoc bodies are not valid shell, so shlex can fail on them (an
    apostrophe in "doesn't"). Falling back to a whitespace split is safe: such
    a line almost never starts with `git`, so it is ignored either way.
    """
    try:
        lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        return list(lexer)
    except ValueError:
        return line.split()


def segments(command: str) -> list[list[str]]:
    """Return the command as a list of simple commands (lists of tokens).

    Lines are tokenized separately so heredoc text can't swallow real commands.
    A quoted string spanning lines is split too; that can only cause a block
    (safe side), never let a dangerous command through unseen.
    """
    out: list[list[str]] = []
    for line in command.splitlines():
        current: list[str] = []
        for tok in tokenize(line):
            if tok in SEPARATORS:
                if current:
                    out.append(current)
                current = []
            else:
                current.append(tok)
        if current:
            out.append(current)
    return out


def strip_prefix(seg: list[str]) -> list[str]:
    """Drop leading VAR=value assignments, wrappers and shell keywords."""
    i = 0
    while i < len(seg) and (
        re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", seg[i]) or seg[i] in PREFIX_WORDS
    ):
        i += 1
    return seg[i:]


def git_subcommand(seg: list[str]) -> tuple[str, list[str]] | None:
    """For `git [global opts] <sub> args...` return (sub, args); otherwise None."""
    if not seg or seg[0] != "git":
        return None
    i = 1
    while i < len(seg) and seg[i].startswith("-"):
        i += 2 if seg[i] in GIT_OPTS_WITH_VALUE else 1
    if i >= len(seg):
        return None
    return seg[i], seg[i + 1 :]


def refspec_destination(spec: str) -> str:
    """`+src:refs/heads/dst` -> `dst`; `main` -> `main`."""
    dst = spec.lstrip("+").split(":")[-1]
    return dst.removeprefix("refs/heads/")


def check_push(args: list[str], branch: Callable[[], str]) -> str | None:
    positional: list[str] = []
    skip = False
    for a in args:
        if skip:
            skip = False
            continue
        if (
            a in {"--force", "-f"}
            or a.startswith("--force-with-lease")
            or a.startswith("--force-if-includes")
        ):
            return "Blocked: force push. Rewrite history only with the user's explicit approval."
        if a in {"--all", "--mirror", "--branches"}:
            return "Blocked: pushing all branches would include main. Push one feature branch."
        if a in PUSH_OPTS_WITH_VALUE:
            skip = True
            continue
        if a.startswith("-"):
            continue
        positional.append(a)
    # positional[0] is the remote, the rest are refspecs.
    refspecs = positional[1:]
    for spec in refspecs:
        if spec.startswith("+"):
            return "Blocked: force push (+refspec). Rewrite history only with the user's explicit approval."
        if refspec_destination(spec) in PROTECTED:
            return (
                "Blocked: pushing to main. Push a feature branch and open a draft PR."
            )
    if not refspecs and branch() in PROTECTED:
        # No refspec: git pushes the current branch, which is main.
        return "Blocked: you are on main. Create a branch (git switch -c feat/<issue>-<slug>) first."
    return None


def check_segment(
    seg: list[str],
    branch: Callable[[], str],
    staged: Callable[[], list[str]],
    depth: int = 0,
) -> str | None:
    seg = strip_prefix(seg)
    if not seg:
        return None

    # Look inside `bash -c "..."`, `sh -c '...'` and `eval ...` (one level is enough).
    if depth < 2:
        if seg[0] in SHELLS and "-c" in seg:
            i = seg.index("-c")
            if i + 1 < len(seg):
                return check_command(seg[i + 1], branch, staged, depth + 1)
        if seg[0] == "eval":
            return check_command(" ".join(seg[1:]), branch, staged, depth + 1)

    if seg[:3] == ["gh", "pr", "merge"]:
        return "Blocked: the user merges pull requests, not the agent."

    parsed = git_subcommand(seg)
    if parsed is None:
        return None
    sub, args = parsed
    if sub == "push":
        return check_push(args, branch)
    if sub == "commit":
        if branch() in PROTECTED:
            return "Blocked: committing on main. Use a feature branch."
        bad = [f for f in staged() if FORBIDDEN_STAGED.search(f)]
        if bad:
            return (
                "Blocked: staged files must never be committed (data, rasters, weights, secrets): "
                + ", ".join(bad[:10])
            )
    return None


def check_command(
    command: str,
    branch: Callable[[], str],
    staged: Callable[[], list[str]],
    depth: int = 0,
) -> str | None:
    """Return the reason to block `command`, or None to allow it.

    `branch` and `staged` return the current branch and the staged file list.
    They are callables so git only runs when a push or commit is actually found
    (this hook runs before every Bash command), and so tests can pass stubs.
    """
    for seg in segments(command):
        reason = check_segment(seg, branch, staged, depth)
        if reason:
            return reason
    return None


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    command = payload.get("tool_input", {}).get("command", "") or ""
    reason = check_command(command, current_branch(), staged_files)
    if reason:
        block(reason)
    sys.exit(0)


if __name__ == "__main__":
    main()
