---
description: Close the session cleanly (lab notebook, STATUS, ledger, commit on a branch)
---

End the working session.

1. Write `docs/lab_notebook/<today>.md`: what we did, why, commands run, outputs, surprises, mistakes, next step.
2. Update `docs/STATUS.md`: done, in progress, next, open decisions, blockers, disk and compute used.
3. Update `docs/learning/understanding_ledger.md` with concepts taught today and the result of any understanding check (not yet, shaky, solid).
4. Update affected registers only if something changed (assumptions, risks, claims).
5. Also refresh `docs/HANDOFF.md` so a fresh session on any machine can resume (see `docs/agent/MULTI_MACHINE.md`).
6. Make sure work is on a feature branch (never `main`). Commit with a Conventional Commit message. If the work is reviewable, push the branch and open or update a draft PR with /open-pr.
7. Reply tersely: what was done, what is waiting for me to review or merge, what you need from me next time, and three questions I should be able to answer about today's work.
