# START HERE

This kit sets up Claude Code to build your FYP (classification, health monitoring, optional yield prediction) in one repository, with no rigid schedule, to teach you along the way, and to run the repository like a professional software team.

Vision (added 2026-10-10): Stage 1 builds the full application on a country with good open data; Stage 2, at the end of the FYP, adapts Pakistani datasets. The aim is to learn the standards for building such a system end to end. See `docs/agent/PROJECT_CONTEXT.md` section 1a and `docs/playbook/`.

## What is in the kit

```
CLAUDE.md                          loaded every session; short rules and map
SETUP_GUIDE.md                     read this first: install and first session
SECURITY.md  CONTRIBUTING.md  CODE_OF_CONDUCT.md
.github/                           issue forms, PR template, CODEOWNERS, workflows
                                   (ci, codeql, release, labeler, pages), dependabot, labeler, release notes config
.devcontainer/devcontainer.json    reproducible Codespaces / VS Code environment
scripts/bootstrap_github.sh        labels, milestones, main-branch ruleset, seed issues (you run it)
.claude/
  settings.json                    permissions allow/ask/deny and hook registration
  hooks/                           guard_bash.py, guard_files.py, post_edit_check.py (need only python3)
  commands/                        /handoff /lit-review /session-start /phase-brief /session-end /weekly-review /teach-back /viva-drill /open-pr
  agents/                          reviewer, dataset-scout, examiner (read-only subagents)
docs/learning/                      MAP.md, MAP.canvas, WEEKLY_RHYTHM.md, OBSIDIAN_GUIDE.md, understanding_ledger.md
docs/_templates/  docs/.obsidian/     note templates and starter Obsidian config
docs/agent/
  PROJECT_CONTEXT.md               long background formerly in CLAUDE.md
  MULTI_MACHINE.md                 laptop, lab PC, cloud: how to keep sessions in sync
  TEACHING_PROTOCOL.md             how the agent teaches you, incl. plain-language maths
  DOCUMENTATION_PROTOCOL.md        what gets documented, for thesis and viva
  DATASET_DISCOVERY.md             dataset mandate, rubric, verified Brazil candidates
  READING_LIST.md                  ranked papers and resources with verification status
  PLATFORM_AND_COMPUTE.md          laptop, lab PC, cloud, GEE terms, GitHub plan limits
  GITHUB_WORKFLOW.md               the full git and GitHub process
  ROADMAP.md                       stages and gates, no week numbers
  RESEARCH_AND_ARCHITECTURE.md     Phase R: research, papers, notes, validate the architecture
  MODULE_A_CLASSIFICATION.md       crop classification (Brazil-Crop recommended first)
  MODULE_B_HEALTH.md               health monitoring
  MODULE_C_YIELD.md                yield prediction (conditional)
```

Placeholders to replace: `OWNER` and `REPO` in `.github/CODEOWNERS` and `.github/ISSUE_TEMPLATE/config.yml`. The workflows assume a Python project with `pip install -e ".[dev]"`, `ruff` and `pytest`; the agent adapts them in Phase 0 once tooling is chosen.

## Setup

Follow `SETUP_GUIDE.md` (Part 1 explains how Claude Code, Git, GitHub and Obsidian fit together; Part 2 is the step-by-step install and first session). It replaces the short setup list that used to be here.

## First message to paste

> Read CLAUDE.md and every file in docs/agent/. Treat the architecture in the kit as hypotheses. Start with Phase R: give me a Phase R Brief (design questions, research plan, first papers to read, assumptions, clarifying questions). State your assumptions first, ask me clarifying questions, and do not write code until I approve. I have no maths background and have read no papers, so teach me in plain words and start with the reading list.

## Decisions recorded so far (Oct 2026)

Module B important, Module C not (feasibility note only). Demo: replay on old fields is the must-have; running on present-day fields is a stretch goal. No "you try first" exercises; Claude Code is the primary developer. Reading plus video, courses on the side. Lab PC reachable remotely; Kaggle and Colab accounts; Claude Pro plan. Word thesis accepted by the university. Public repo allowed, comments in code, free GitHub features only.

## What you need to decide or provide at Checkpoint 0

1. Public or private repository, licence for the code (the agent will present options; do not let it choose silently).
2. Your university's thesis template, citation style, page limits, deadlines, supervisor milestones, weekly hours.
3. (Decided) University allows full AI use; you must be able to explain everything built.
5. Your git experience (so the agent teaches the right amount).
6. Lab PC hardware report (the agent will give you a command to run).
7. (Decided) Comments in code: yes. Public repo: yes. Student Pack: none. The agent runs the git and gh commands.

## Obsidian (your learning cockpit)

Open the `docs/` folder as an Obsidian vault and read `docs/learning/OBSIDIAN_GUIDE.md`. Start every day at `docs/learning/MAP.md`; the visual map is `MAP.canvas`; the weekly structure is `WEEKLY_RHYTHM.md`. A starter `docs/.obsidian/` config is included (untested in Obsidian; check Settings, Files and links, and make sure "Use [[Wikilinks]]" is off). `.gitignore` keeps device-specific Obsidian state out of Git.

## Claude Code features in this kit

- Daily loop: `/session-start`, work, `/open-pr`, `/session-end`. Weekly: `/weekly-review`. Fortnightly: `/viva-drill <phase>`. Any time: `/teach-back <concept>`. Before a phase: `/phase-brief <phase>`.
- Hooks block pushes to `main`, force pushes, `gh pr merge`, commits on `main`, commits of data/rasters/weights/secrets, and writes to `.env` and `data/raw`. They run `ruff` after Python edits once ruff is installed. They were tested with sample inputs in a scratch repository; they have not been run inside a live Claude Code session.
- Permissions: read-only git and `gh` commands, `make`, `pytest` and `ruff` are allowed; `git push`, `gh api`, `gh repo` and package installs ask first; force pushes, hard resets, `rm -rf`, `gh pr merge` and `.env` access are denied. Personal overrides go in `.claude/settings.local.json` (add it to `.gitignore`).
- Custom commands still work, but Anthropic's docs now prefer the skills format (`.claude/skills/<name>/SKILL.md`). Converting later is mechanical.
- After copying the kit, restart Claude Code once so it loads `.claude/agents/`. Run `/hooks` and `/agents` to confirm they registered.

## Working habits

- End each session with the agent updating `docs/STATUS.md` and the lab notebook.
- You review and merge every PR. If you cannot explain the diff, do not merge it.
- Read each walkthrough; write a few lines in `docs/learning/my_understanding/` in your own words.
- Review the roadmap monthly; cut scope early in the order given in ROADMAP.md.
- Never commit data, credentials or model weights.

## Known limits

- Written without running anything on your machine. Endpoints, file names and package behaviour must be verified by the agent.
- Brazil-Crop (the recommended first dataset) was read from its landing page only. Its geometry type, per-field label dates and class counts are unverified; Checkpoint A1 decides.
- The reading list marks each item's verification level. Several Pakistan papers and all Tier 4 items are not verified.
- GitHub free-plan feature availability for private repositories is not fully verified.
- Google Earth Engine noncommercial terms matter for a future startup; do not build the product on that tier.
