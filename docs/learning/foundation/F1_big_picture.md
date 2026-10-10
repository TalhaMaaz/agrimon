---
type: lesson
status: draft
tags: [lesson, foundation]
phase: R
---

# F1: The big picture

Previous: [index](F0_index.md) | Next: [F2 Claude Code in this kit](F2_claude_code_kit.md)

## What is it?

The project is **one folder** (`~/Documents/UNI/fyp/agrimon`). Four tools work on that folder. None of them talk to each other directly; they share the files.

```
                         +-------------------------------+
   you  --- type ---->   |  Claude Code (terminal)       |
                         |  reads rules, edits files,    |
                         |  runs git / gh / python       |
                         +---------------+---------------+
                                         | reads and writes
                                         v
 +-------------+  opens docs/   +------------------------------+   push/pull   +-------------------+
 |  Obsidian   | <------------> |  the repository (a folder)   | <-----------> |  GitHub (cloud)   |
 |  notes app  |                |  code + docs + kit           |    via git    |  issues, PRs, CI, |
 +-------------+                |  history kept by git         |               |  rules on main    |
                                +------------------------------+               +-------------------+
```

| Tool | What it is | What it does for us |
|---|---|---|
| **Git** | A version-control program on your laptop | Records every change as a commit; lets work happen on branches |
| **GitHub** | A website that hosts a copy of the git repository | Issues (to-do items), pull requests (proposed changes), Actions (automatic checks), rules that protect `main` |
| **Claude Code** | An AI agent in the terminal | Reads the rules in `CLAUDE.md`, writes code and docs, runs commands, asks permission for risky ones |
| **Obsidian** | A Markdown notes app | A comfortable way for you to read and link the notes in `docs/` |

## How does it work? The one idea that matters most

**The repository is the memory.** A Claude Code conversation is saved only on the machine where it ran, and each new session starts with an empty context. So anything that must survive (decisions, progress, what to do next) goes into a file in git, not into the chat.

Coding analogy: a Claude session is like a **stateless web server process**. It can be killed at any time. The **database** is the repository. If a fact lives only in process memory (the chat), it's lost on restart. That's why every session starts by reading `STATUS.md` and `HANDOFF.md` (loading state) and ends by writing them (saving state).

```
 session 1                     repo (persistent)               session 2 (any machine)
 ---------                     -----------------               -----------------------
 /session-start  <-- read --   STATUS, HANDOFF, notebook  -- read -->  /session-start
 work                                                               work
 /session-end    -- write -->  STATUS, HANDOFF, notebook  <-- write -- /session-end
```

## What is "the kit"?

The kit is a set of files someone (a previous Claude conversation, with you) prepared so Claude Code works in a particular way on this project. It has three layers:

```
 LAYER 1: instructions for Claude            LAYER 2: automation and guard rails         LAYER 3: for you (human-facing)
 ------------------------------              -----------------------------------         ------------------------------
 CLAUDE.md          (always loaded)          .claude/settings.json (permissions)          START_HERE.md, SETUP_GUIDE.md
 docs/agent/*.md    (read on demand)         .claude/hooks/*.py    (safety checks)        docs/learning/ (MAP, lessons, ledger)
 .claude/commands/  (your slash commands)    .github/ (CI, Dependabot, forms, rules)      docs/_templates/ (note templates)
 .claude/agents/    (helper subagents)       scripts/bootstrap_github.sh (one-off setup)  CONTRIBUTING, SECURITY, CODE_OF_CONDUCT
```

## Tour of the repository as it is today

There is no code yet. Today the repository is only the kit plus the first session's notes (77 tracked files on `main`).

```
agrimon/
  CLAUDE.md                 the rules Claude reads every session
  START_HERE.md             kit overview (for you)
  SETUP_GUIDE.md            how the kit was installed (for you; already done)
  CONTRIBUTING.md  SECURITY.md  CODE_OF_CONDUCT.md   standard open-source files
  .claude/                  Claude Code configuration (F2)
    settings.json             permissions + hook registration
    hooks/                    3 Python safety scripts
    commands/                 9 slash commands (/session-start, ...)
    agents/                   3 read-only helpers (reviewer, dataset-scout, examiner)
  .github/                  GitHub configuration (F4)
    workflows/                5 automatic jobs (ci, codeql, labeler, pages, release)
    ISSUE_TEMPLATE/           forms for new issues
    pull_request_template.md  the checklist every PR body starts from
    dependabot.yml  labeler.yml  CODEOWNERS  release.yml
  .devcontainer/            recipe for a cloud dev environment (Codespaces); unused so far
  scripts/bootstrap_github.sh   already run once: created labels, milestones, issues, ruleset
  docs/                     the Obsidian vault and the project's written memory (F5)
    agent/                    detailed protocols for Claude
    learning/                 your learning area
    _templates/               note templates
    .obsidian/                shared Obsidian settings
```

Later, Phase 0 (issue #7) adds `src/`, `tests/`, `configs/`, `pyproject.toml`, a `Makefile` and so on. The planned layout is itself a hypothesis (H-09).

## Who does what

| You (product owner, reviewer) | Claude (contributor) |
|---|---|
| Decide scope and priorities | Propose plans (Phase Briefs), research, write code and docs |
| Approve Phase Briefs | Teach each new concept, then build |
| Review and **merge** every PR | Open issues, branches, draft PRs; never merges, never pushes to `main` |
| Answer check questions; write your own notes in `my_understanding/` | Keep STATUS, notebook, ledger, MAP current |

## What goes wrong?

- Trusting the chat as memory: switch machines or start a new session, and it's gone.
- Treating the kit as truth. Its architecture and tool choices are hypotheses (that's what Phase R is for), and some of its claims about itself are wrong (see F6).
- Merging what you can't explain. Your university requires you to understand everything, so the merge button is your understanding gate.

## Check yourself

1. Why does every session start by reading `STATUS.md` instead of relying on what was said yesterday?
2. Name the three layers of the kit and one file from each.
3. Which actions are reserved for you and never done by Claude?
