---
description: Open or update a draft pull request with the project template and disclosure
allowed-tools: Bash(git status *), Bash(git diff *), Bash(git log *), Bash(gh pr create --draft *), Bash(gh pr view *), Bash(gh pr checks *)
---

Prepare a draft pull request for the current branch.

1. Confirm the branch is not `main` and that the work links to an issue. If there is no issue, create one first with the matching issue form fields.
2. Run `make check` if it exists and report the result honestly. Do not open the PR as ready if checks fail.
3. Fill `.github/pull_request_template.md` fully: summary, `Closes #n`, type, how it was tested, documentation updated, hygiene checks, risk and rollback, and the AI-assistance disclosure (what you produced; what I still need to read, run and understand).
4. Use a Conventional Commit style PR title.
5. Create it with `gh pr create --draft`. Never merge.
6. Reply with: the PR title, what changed in plain language, the three parts of the diff I should read first, and two questions I should be able to answer before I merge.
