---
description: Orient at the start of a working session (state, plan, open decisions)
---

Start a working session.

0. Run `git fetch --all --prune` and tell me if my branch is behind or ahead of its remote, and which machine this seems to be (ask if unclear).
1. Read `docs/HANDOFF.md`, `docs/STATUS.md`, the most recent file in `docs/lab_notebook/`, and `docs/agent/TEACHING_PROTOCOL.md`. If any is missing, say so instead of guessing.
2. Run `git status` and `git log --oneline -10`, and `gh pr list` and `gh issue list --limit 10` if GitHub is linked.
3. Reply, assumptions first, with: where we are in three lines; what is open (PRs waiting for my review, failing CI, blocked issues); today's proposed plan as a short task list; any decision you need from me.
4. Ask whether priorities changed. Do not start building until I answer.
