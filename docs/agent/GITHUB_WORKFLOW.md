# GITHUB WORKFLOW (run the project like a small software company)

Goal: the user learns how real teams ship and maintain code, using GitHub features end to end, on a solo project. The user plays every role (product owner, developer, reviewer, release manager) deliberately; the agent works as a contributor who never merges its own work.

Facts about what a free GitHub account allows are in PLATFORM_AND_COMPUTE.md section 4. Several features below depend on the repository being public or on a paid or student plan; each is tagged.

## 1. Roles

| Role | Who | Responsibility |
|---|---|---|
| Product owner / maintainer | User | Decides scope, accepts work, merges PRs, cuts releases |
| Contributor | Agent | Opens issues, works on branches, opens PRs, responds to review |
| Reviewer | User first; agent may do a separate "review pass" in a new session, labelled as AI review | Reads diffs, requests changes |

The agent never pushes to `main`, never merges and never approves its own PR. The user has authorised the agent to run all git and `gh` commands, including bootstrap and settings changes; it announces each settings change first and logs it. The university allows full AI use but requires the user to understand everything, so the understanding check on every PR is the real gate. The user merges after CI is green and after a real read of the diff. If the user cannot explain the diff, the PR waits (rule 1 of CLAUDE.md applies to code review too).

## 2. Branching and commits

- Trunk-based with short-lived branches from `main`. Names: `feat/<issue>-<slug>`, `fix/<issue>-<slug>`, `docs/<issue>-<slug>`, `exp/<issue>-<slug>` for experiments, `chore/<issue>-<slug>`.
- One issue, one branch, one PR. PRs stay small (aim under 400 changed lines excluding generated files); large work is split.
- Conventional Commits: `feat(classification): add TempCNN model`, `fix(imagery): handle empty STAC result`, `docs(adr): record dataset decision`, `chore(ci): pin action versions`, `test:`, `refactor:`, `perf:`, `build:`. Breaking change marked `!` and explained in the body.
- Squash-merge into `main` with the PR title as the commit message (so PR titles are conventional commits). Linear history.
- Commit trailers from the harness (for example Co-Authored-By) are kept. Do not strip them.
- Tags: `cp-A0`, `cp-A1` for checkpoints (annotated tags). SemVer tags `v0.1.0` for releases.

## 3. Issues and planning

- **Issue forms** in `.github/ISSUE_TEMPLATE/`: task, bug report, feature request, dataset candidate, experiment. Every piece of work starts as an issue with acceptance criteria that match a requirement ID (R-A-01 and so on).
- **Labels** (created by the bootstrap script): `type:feature`, `type:bug`, `type:docs`, `type:chore`, `type:experiment`, `type:dataset`, `module:A`, `module:B`, `module:C`, `module:platform`, `module:infra`, `priority:high`, `priority:normal`, `priority:low`, `status:blocked`, `status:needs-decision`, `good-first-task`, `learning`.
- **Milestones** mirror the roadmap: `R Research and architecture`, `M0 Scaffolding`, `M1 Module A pipeline and map`, `M2 Second dataset and Pakistan bridge`, `M3 Health monitoring prototype`, `M4 Yield prototype or feasibility`, `M5 Integration and thesis`. Stage 2 (Pakistan) gets its own milestone(s) when the Bridge Report plans it; don't create them earlier.
- **Projects (v2 board)**: columns Backlog, Ready, In progress, In review, Done; fields: Module, Priority, Estimate, Milestone. Automation: items move to Done when the issue closes. Created manually in the web UI (the CLI can create projects but field and view setup is easier in the UI; verify current `gh project` support).
- **Discussions** (public repos): categories Ideas, Q&A, Decisions (links to ADRs), Show and tell. Use them as the design-notes log before an ADR.
- **Sub-issues / task lists** break epics (a phase) into issues. One epic issue per phase with a checklist.

## 4. Pull requests

- PR template: summary, linked issue (`Closes #n`), type of change, what was tested, screenshots or metrics, docs updated, ADR needed, risk and rollback, checklist (tests, lint, no data or secrets committed, understanding check done), AI-assistance disclosure.
- Draft PRs while work is in progress. Ready for review only when CI is green.
- Review comments are resolved before merge. The user practises writing real review comments (what, why, suggestion).
- CODEOWNERS routes review requests (with a solo owner it still documents ownership by area and triggers the review request flow).
- Auto-labeling by changed paths through `.github/labeler.yml`.
- Semantic PR title check in CI.

## 5. Continuous integration (GitHub Actions)

Workflows live in `.github/workflows/`:
- `ci.yml`: on PR and push to `main`: lint (ruff), format check, type check (optional), unit tests (pytest) with coverage, contract tests, a docs build check, a "no large files, no secrets" check. Matrix only if useful. Cache dependencies. Tests must run without network or GPU (use tiny fixtures).
- `codeql.yml`: static security analysis for Python and JavaScript (free for public repos; private repos need GitHub Code Security: UNVERIFIED for this account).
- `release.yml`: on tag `v*`: build artifacts, generate release notes from merged PRs (categories in `.github/release.yml`), create a GitHub Release.
- `docs.yml`: build documentation and the static web demo and deploy to GitHub Pages (public repos only on Free).
- Dependabot (`.github/dependabot.yml`): weekly updates for pip, npm, and GitHub Actions.
- Rules: pin third-party actions to a major version at least (full commit SHA is stronger; trade-off is maintenance effort); set `permissions:` to read-only by default; never print secrets; heavy jobs (extraction, training) are NOT run in CI.

## 6. Branch protection with rulesets (repository settings)

Target ruleset for `main` (script in `scripts/bootstrap_github.sh`): require a pull request before merging, require status checks `ci` to pass and branches to be up to date, block force pushes and deletions, require linear history, require conversation resolution, require signed commits optional. With one account the user cannot get a second human approval, so "required approvals" is set to 0 and the discipline is the user's own review; record this in an ADR as a known limitation. Availability: rulesets on public repos on Free; on private repos probably need a paid or student plan (UNVERIFIED).

## 7. Releases and versioning

- Semantic Versioning: `0.y.z` while prototyping. `v0.1.0` = first end-to-end Module A pipeline and map (Milestone M1). `v0.2.0` second dataset, and so on. `v1.0.0` = FYP submission.
- `CHANGELOG.md` kept by hand or generated; GitHub Release notes are generated from PR labels.
- Each release attaches: the web demo bundle, the metrics report, and a reproducibility note (commit, config hashes, data manifest versions). Model weights go in Release assets only if small and licence-clean; otherwise document how to regenerate (never commit weights to git).
- Hotfix flow: branch from the tag, fix, PR, patch release.

## 8. Security and hygiene

- `SECURITY.md` with a private reporting route (enable private vulnerability reporting in settings, public repos).
- Secret scanning and push protection (free for public repos; settings toggle). `.env` never committed; `.env.example` is.
- Dependabot alerts and security updates on. `pip-audit` or similar in CI (verify).
- Pre-commit hooks locally mirror CI (ruff, end-of-file, large-file check, detect-secrets or gitleaks; verify tools).
- Licence file: ASK the user (MIT or Apache-2.0 are typical for code; datasets keep their own licences; thesis text has its own terms). Do not choose silently.
- Data licences recorded in `docs/data/licences.md`. Notice that CC BY-NC data (for example the São Paulo yield set) affects a future startup.

## 9. If the repository must be private on a Free plan

Expect to lose: rulesets/branch protection, Pages, possibly CodeQL and secret scanning. Mitigations: pre-commit hooks and a local `make check` target as the gate; deploy the demo from a separate public repo containing only the static demo bundle; keep the same PR-and-review discipline voluntarily. Ask whether the user has the GitHub Student Developer Pack and check what it unlocks.

## 10. Other features to use deliberately (tag: Free/public unless noted)

- **Codespaces** and `.devcontainer/` for a reproducible environment (120 core-hours per month on Free; GPU not available there, so use it for docs, web and light tests).
- **GitHub Pages** for the web demo and the documentation site.
- **Packages (ghcr.io)** for a Docker image of the pipeline (500 MB storage on Free).
- **Wiki** not used (docs live in the repo, reviewed through PRs).
- **Insights**: pulse, contributors, dependency graph, traffic; the user screenshots these for the thesis "process" chapter.
- **gh CLI**: the agent uses `gh issue create`, `gh pr create --draft`, `gh pr checks`, `gh run watch`; the agent runs the bootstrap script after explaining it. Prerequisite: the session must have a linked GitHub account (`gh auth status`); if not, stop and ask the user to connect it.
- **Saved replies, notifications, mobile app** optional.
- **Autolinks, issue/PR references, CITATION.cff** (so GitHub shows "Cite this repository"; useful for the thesis).

## 11. How the agent works on this workflow

1. Before any code: create or find the issue; confirm it has acceptance criteria and a milestone; branch from latest `main`.
2. Work in small commits with conventional messages; push the branch; open a DRAFT PR early using the template.
3. Run `make check` locally before marking ready; check CI with `gh pr checks`.
4. Fill the AI-assistance disclosure in the PR body honestly (what the agent generated; what the user reviewed).
5. Explain the diff to the user in plain language (TEACHING_PROTOCOL walkthrough) and ask the user to review. Never merge.
6. After merge: delete the branch, update `docs/STATUS.md` and the lab notebook, close or update the issue, update the Project board.
7. Teach each GitHub concept the first time it appears (branches, PRs, CI, rulesets, releases), in the same Q&A format, with a tiny example.

## 12. Bootstrap order (Phase 0; the agent runs the commands)

1. The user links GitHub to the session; the agent confirms with `gh auth status` and `gh api user --jq .login`.
2. Create the repository (public, decided by the user; a private repo is possible for drafts) and ask the user for the code licence.
3. Run `scripts/bootstrap_github.sh OWNER/REPO` (labels, milestones, seed issues, ruleset). The agent explains each call first.
4. Enable in Settings: Discussions, private vulnerability reporting, secret scanning, push protection, Dependabot alerts and updates, Pages (source: GitHub Actions).
5. Create the Project board in the UI and add the seeded issues.
6. Open the first PR (scaffolding) through the normal flow so the pipeline is exercised from day one.

## 13. Anti-patterns

- Committing to `main` directly "just this once".
- Giant PRs mixing refactors, features and data changes.
- Merging with red CI, or disabling a failing test instead of fixing it.
- Committing datasets, rasters, model weights, notebooks with large outputs, or `.env`.
- Running training or extraction in CI.
- Treating AI-generated diffs as reviewed because the AI wrote them.
- Using issues as a diary; a lab notebook entry is the diary, an issue is a unit of work.
- Over-engineering the process so it slows learning. If a ceremony costs more than it teaches, say so and trim it, but record the decision.
