"""Tests for guard_bash.py (issue #21).

Run with `python3 .claude/hooks/test_guard_bash.py` (no dependencies) or with
pytest once the project has it. Each case is (command, current branch, staged
files, expected): expected is None for "allowed", or a word that must appear
in the block reason.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from guard_bash import check_command  # noqa: E402

HEREDOC_THEN_PUSH = """cat >> docs/lab_notebook/x.md <<'EOF'
- The hook blocks pushes to main; it doesn't stop the user.
EOF
git push"""

CASES = [
    # --- false positives hit on 2026-10-10: must be allowed ---
    (
        "git push -u origin fix/17-ci && gh pr create --base main --title x",
        "fix/17-ci",
        [],
        None,
    ),
    (HEREDOC_THEN_PUSH, "docs/6-phase-r-plan", [], None),
    (
        "git push origin --delete docs/6-phase-r-plan fix/17-ci-no-python-yet",
        "main",
        [],
        None,
    ),
    (
        'gh issue create --title t --body "mentions git push --force and main"',
        "main",
        [],
        None,
    ),
    # --- other things that must stay allowed ---
    ("git push", "feat/1-x", [], None),
    ("git push -u origin feat/1-x", "feat/1-x", [], None),
    ("git push origin feat/main-menu", "feat/main-menu", [], None),
    ("git -C /repo push origin feat/1-x", "main", [], None),
    ("git pull --ff-only && git switch main", "main", [], None),
    ('echo "git commit later" > notes.txt', "main", [], None),
    ("git commit -m 'fix: x'", "feat/1-x", ["src/a.py"], None),
    ("gh pr create --draft --base main", "feat/1-x", [], None),
    # --- pushing to main: blocked ---
    ("git push origin main", "feat/1-x", [], "main"),
    ("git push origin HEAD:main", "feat/1-x", [], "main"),
    ("git push origin feat/1-x:refs/heads/main", "feat/1-x", [], "main"),
    ("git push origin master", "feat/1-x", [], "main"),
    ("git push origin --delete main", "feat/1-x", [], "main"),
    ("git push", "main", [], "main"),
    ("git push -u origin", "main", [], "main"),
    ("git push --all origin", "feat/1-x", [], "all branches"),
    ("git push --mirror origin", "feat/1-x", [], "all branches"),
    ("cd /repo && git push origin main", "feat/1-x", [], "main"),
    ("git -C /repo push origin main", "feat/1-x", [], "main"),
    ('bash -c "git push origin main"', "feat/1-x", [], "main"),
    ("eval git push origin main", "feat/1-x", [], "main"),
    ("GIT_TRACE=1 git push origin main", "feat/1-x", [], "main"),
    ("for r in a b; do git push origin main; done", "feat/1-x", [], "main"),
    ("if true; then git push origin main; fi", "feat/1-x", [], "main"),
    ("sudo git push origin main", "feat/1-x", [], "main"),
    # --- force: blocked ---
    ("git push --force origin feat/1-x", "feat/1-x", [], "force"),
    ("git push -f", "feat/1-x", [], "force"),
    ("git push --force-with-lease origin feat/1-x", "feat/1-x", [], "force"),
    ("git push origin +feat/1-x", "feat/1-x", [], "force"),
    # --- merging: blocked ---
    ("gh pr merge 5 --squash", "feat/1-x", [], "merges"),
    ("git status && gh pr merge 5", "feat/1-x", [], "merges"),
    # --- commits: blocked on main or with forbidden files ---
    ("git commit -m x", "main", [], "committing on main"),
    (
        "git add -A && git commit -m x",
        "feat/1-x",
        ["data/raw/a.csv"],
        "never be committed",
    ),
    ("git commit -m x", "feat/1-x", ["weights/model.pt"], "never be committed"),
    ("git commit -m x", "feat/1-x", [".env"], "never be committed"),
]


def run() -> int:
    failures = 0
    for command, branch, staged, expected in CASES:
        reason = check_command(command, lambda b=branch: b, lambda s=staged: s)
        ok = (
            reason is None
            if expected is None
            else (reason is not None and expected in reason)
        )
        if not ok:
            failures += 1
            print(
                f"FAIL  branch={branch!r}  expected={expected!r}  got={reason!r}\n      {command!r}"
            )
    print(f"{len(CASES) - failures}/{len(CASES)} passed")
    return 1 if failures else 0


def test_cases() -> None:
    """pytest entry point."""
    assert run() == 0


if __name__ == "__main__":
    sys.exit(run())
