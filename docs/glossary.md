---
type: register
status: living
tags: [glossary]
---

# Glossary

One line per term, with a link to where it is taught. New terms are added when they are first used (TEACHING_PROTOCOL section 7). Sorted alphabetically within each group.

## Workflow and tooling

| Term | Definition | Lesson |
|---|---|---|
| Branch | A movable name that points at a commit; new commits on it move the name forward. | [F3](learning/foundation/F3_git.md) |
| CI (continuous integration) | Automated checks GitHub runs on a fresh machine for every PR and push. | [F4](learning/foundation/F4_github.md) |
| Commit | An immutable snapshot of the repository with a message and a parent. | [F3](learning/foundation/F3_git.md) |
| Conventional Commits | Message format `type(scope): subject` (fix, feat, docs, chore...) that tools read. | [F3](learning/foundation/F3_git.md) |
| Dependabot | GitHub bot that opens PRs to update dependencies, here the versions of GitHub Actions. | [F4](learning/foundation/F4_github.md) |
| Draft PR | A pull request marked "not ready"; it can't be merged until marked ready for review. | [F4](learning/foundation/F4_github.md) |
| Hook (Claude Code) | A script Claude Code runs before or after a tool call; it can block the call. Guards the agent only. | [F2](learning/foundation/F2_claude_code_kit.md) |
| Pull request (PR) | A proposal to merge a branch into `main`, with diff, discussion and checks. | [F4](learning/foundation/F4_github.md) |
| Refspec | The `source:destination` part of `git push` that says which branch goes where. | [Practice run, 2026-10-10](lab_notebook/2026-10-10.md) |
| Ruleset | Server-side rules on `main` (PR required, `ci` must pass, no force push). Guards everyone. | [F4](learning/foundation/F4_github.md) |
| Squash merge | Merging a PR as one new commit on `main` containing all its changes. | [F4](learning/foundation/F4_github.md) |
| Working tree | The files on disk, including changes not yet committed. | [Practice run, 2026-10-10](lab_notebook/2026-10-10.md) |

## Project

| Term | Definition | Lesson |
|---|---|---|
| Playbook | `docs/playbook/`: the standard practices learned in Stage 1 and whether they transfer to Pakistan. | [Playbook](playbook/README.md) |
| Stage 1 / Stage 2 | Stage 1: full application on a country with good open data. Stage 2: adapt Pakistani datasets (end of the FYP). | [PROJECT_CONTEXT 1a](agent/PROJECT_CONTEXT.md) |
