---
type: lesson
status: draft
tags: [lesson, foundation, github]
phase: R
---

# F4: GitHub features we use

Previous: [F3 Git as we use it](F3_git.md) | Next: [F5 The documentation system](F5_documentation_system.md)

Repository: https://github.com/TalhaMaaz/agrimon (public). The state below was checked with `gh` on 2026-10-10.

## Map of the features

```
            PLANNING                    CHANGE                      AUTOMATION                     PROTECTION
            --------                    ------                      ----------                     ----------
  Issues (#6..#13, #15)          Pull requests (#1..#5, #14)   Actions workflows:              Ruleset "protect-main"
   + issue forms                  + PR template                 ci, codeql, labeler,            CODEOWNERS
   + labels                       + draft state                 pages, release                  SECURITY.md
   + milestones (R, M0..M5)       + review + merge (you)       Dependabot (bot PRs)
```

## 1. Issues: units of work

An issue is a tracked to-do item with a title, a description, labels, a milestone and comments. Analogy: a **ticket in a bug tracker** (Jira, Trello card).

- **Issue forms** (`.github/ISSUE_TEMPLATE/`): task, bug report, feature request, dataset candidate, experiment. They give each new issue a structured body.
- **Labels** classify issues: `type:` (feature, bug, docs, chore, experiment, dataset), `module:` (A, B, C, platform, infra), `priority:`, `status:` (blocked, needs-decision), `learning`. GitHub's default labels (`bug`, `enhancement`, ...) also still exist.
- **Milestones** group issues by roadmap step: `R Research and architecture`, `M0 Scaffolding`, `M1 Module A pipeline and map`, ..., `M5 Integration and thesis`.

Open issues today: #6 Phase R, #7 scaffold, #8 CI setup, #9 charter, #10 dataset audit, #11 label adapter, #12 imagery pilot, #13 baselines, #15 this guide.

Rule: an issue is a unit of work, not a diary. The diary is the lab notebook (F5).

## 2. Pull requests: proposed changes

A PR says "please merge branch X into `main`". It shows the **diff** (exactly what changed), runs the checks, and holds the review discussion. Analogy: a **code review request** at a software company.

```
 branch pushed --> draft PR --> CI runs --> ready for review --> you review --> you squash-merge --> branch deleted
                    (#14)        (F4.3)                          comments,       (only when
                                                                 questions       CI is green)
```

- **Draft** means "not ready to merge yet". Claude always opens PRs as drafts; you mark them ready.
- **PR template** (`.github/pull_request_template.md`): summary, linked issue, type, testing, documentation, hygiene checklist, risk and rollback, **AI-assistance disclosure** (what the AI produced and what you checked).
- `Closes #6` in a PR body closes issue #6 automatically when the PR is merged. `Refs #6` only links them.
- **CODEOWNERS** names you as owner of every path, so GitHub requests your review automatically.

## 3. GitHub Actions: automatic checks

A workflow is a YAML file in `.github/workflows/` that says "on event X, run these steps on a fresh GitHub Linux machine". Analogy: a **CI server / cron job hosted by GitHub**. Results show as green ticks or red crosses on PRs and commits.

| Workflow | Trigger | What it does | State today |
|---|---|---|---|
| `ci.yml` job **ci** | every PR, push to `main` | Set up Python 3.11, install, `ruff` lint + format, `pytest`, block files >5 MB, block data/secrets | **Fails**: `setup-python` with `cache: pip` needs a `pyproject.toml`/`requirements.txt`, which don't exist yet |
| `ci.yml` job **pr-title** | every PR | Checks the PR title is a Conventional Commit | Passes |
| `codeql.yml` | PR, push, weekly | GitHub's security scanner, for Python and JavaScript | Python passes; **JavaScript fails** (no JS code to analyse yet) |
| `labeler.yml` | every PR | Adds labels from changed paths (`docs/**` gives `type:docs`, `.github/**` gives `module:infra`) | Passes |
| `pages.yml` | push to `main` touching `apps/web/**` | Publishes the web map to GitHub Pages | Hasn't run (no web app yet) |
| `release.yml` | pushing a tag `v*` | Creates a GitHub Release with notes from merged PRs | Hasn't run |

## 4. Dependabot: the dependency robot

`.github/dependabot.yml` tells GitHub's bot to check weekly for newer versions of pip packages, npm packages (in `apps/web`) and the Actions used in workflows, and to open a PR for each update. PRs #1 to #5 are its work: for example "bump actions/checkout from 4 to 7". Its pip and npm runs currently fail because there's no `pyproject.toml` or `apps/web/` yet.

Why it exists: outdated dependencies carry known security holes. Cost: a stream of PRs you have to review. Each bump can break something, so CI must be green before you merge one.

## 5. The ruleset "protect-main" (important)

A ruleset is a set of server-side rules that GitHub enforces for **everyone**, including you, on the `main` branch. This is the only protection that also covers your own terminal (Claude's hooks only cover Claude). It was created by `scripts/bootstrap_github.sh`. The active rules:

| Rule | Effect |
|---|---|
| deletion | `main` can't be deleted |
| non_fast_forward | No force-pushes to `main` |
| required_linear_history | No merge commits; squash or rebase only |
| pull_request (0 approvals, threads resolved) | Changes reach `main` only via a PR; all review comments must be resolved |
| required_status_checks: **ci**, strict | The `ci` check must **pass**, and the branch must be up to date with `main` |

Consequence for today: **no PR can be merged right now**, because `ci` fails on every branch. PR #14 and this guide's PR are blocked until CI is fixed. Options are in [F6](F6_a_working_day_and_gaps.md#gaps-between-the-kit-and-reality).

Approvals are set to 0 because GitHub doesn't let you approve your own PR, and you're the only human. The real gate is your own review.

## 6. Not used or not set up (yet)

- **Discussions**: off.
- **Licence**: none (`licenseInfo: null`). Without a licence, the code is "all rights reserved" by default, even in a public repo. To be chosen.
- **Project board**: unknown. `gh` lacks the `read:project` permission to check. You can see it at github.com/TalhaMaaz?tab=projects.
- **Secret scanning, push protection, private vulnerability reporting**: settings toggles that the setup guide lists. Not verified.
- **Releases and tags**: none yet (the first planned is `v0.1.0` at Milestone M1).

## What goes wrong?

- Merging with red CI "just once": the ruleset prevents it, which is the point.
- Merging Dependabot PRs blindly: a major version bump (4 to 7) can change behaviour.
- Treating a green tick as proof of correctness: CI only checks what the tests check.

## Check yourself

1. What is the difference between Claude's hooks and the GitHub ruleset in **who** they protect against?
2. Why can't PR #14 be merged today, even though it contains only Markdown?
3. What does Dependabot do, and what is the risk of merging its PRs without reading them?
