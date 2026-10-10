---
description: Save everything a fresh session on another machine needs, commit and push the branch
---

Prepare a machine switch (or a clean stopping point).

1. Make sure we are on a feature branch, not `main`. If there are uncommitted changes, review them with `git status` and `git diff --stat` and tell me anything unexpected (data files, secrets).
2. Overwrite `docs/HANDOFF.md` using its template: what we were doing and why, exact stopping point (file, function, command), commands to resume, open decisions, things that exist only on this machine and how to recreate them, gotchas.
3. Append today's lab-notebook entry (include machine name and hardware), update `docs/STATUS.md` and the "Right now" part of `docs/learning/MAP.md`, and the understanding ledger if we taught anything.
4. Commit with a Conventional Commit message (a work-in-progress commit on a feature branch is fine) and push the branch (this asks my permission).
5. Verify: `git status` clean and nothing unpushed. Reply with the exact commands I should run on the other machine, and what to expect.
