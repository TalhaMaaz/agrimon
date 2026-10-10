---
type: lesson
status: draft
tags: [lesson, foundation, claude-code]
phase: R
---

# F2: Claude Code in this kit

Previous: [F1 The big picture](F1_big_picture.md) | Next: [F3 Git as we use it](F3_git.md)

## What is it?

Claude Code is an agent that runs in your terminal inside the project folder. It can read and edit files and run shell commands. A project shapes its behaviour with five mechanisms, and this kit uses all five:

```
 mechanism          file(s)                          when it acts                       who triggers it
 ---------          -------                          ------------                       ---------------
 1 memory file      CLAUDE.md                        loaded at the start of every session automatic
 2 slash commands   .claude/commands/*.md            when you type /name                you
 3 subagents        .claude/agents/*.md              when Claude delegates a task       Claude (or you, by asking)
 4 permissions      .claude/settings.json            before every tool call             automatic
 5 hooks            .claude/hooks/*.py (+ settings)  before/after specific tool calls   automatic
```

## 1. CLAUDE.md: the always-on rules

Claude Code reads `CLAUDE.md` into context at the start of every session. Analogy: it's the **system config every process loads at boot**. Because it costs context on every turn, it's kept short (rules and pointers only). The long protocols sit in `docs/agent/` and are read **on demand**, like lazy-loaded modules: CLAUDE.md says "read `GITHUB_WORKFLOW.md` for any git action", and Claude opens it when needed.

```
 CLAUDE.md (always)  ---> points to --->  docs/agent/TEACHING_PROTOCOL.md   (every session)
                                          docs/agent/RESEARCH_AND_ARCHITECTURE.md (Phase R)
                                          docs/agent/GITHUB_WORKFLOW.md     (git work)
                                          docs/agent/MODULE_A_...md          (only the current module)
```

The files in `docs/agent/`, and what each one governs:

| File | Governs |
|---|---|
| PROJECT_CONTEXT | Long background: modules, you, hardware, standing rules, planned repo layout |
| TEACHING_PROTOCOL | How Claude teaches you: lesson formats, plain-language maths, ledger |
| DOCUMENTATION_PROTOCOL | What gets written where; the "phase exit rule"; thesis structure |
| RESEARCH_AND_ARCHITECTURE | Phase R: questions, literature, hypotheses, dossier, Checkpoint R |
| ROADMAP | Stages, steps and gates (no dates) |
| GITHUB_WORKFLOW | Branches, commits, PRs, CI, releases |
| MULTI_MACHINE | Working across laptop, lab PC and cloud |
| PLATFORM_AND_COMPUTE | Hardware, cloud options, Earth Engine terms, GitHub plan limits |
| DATASET_DISCOVERY | How datasets are found and scored |
| READING_LIST | Papers and courses, with honest verification status |
| MODULE_A / B / C | The plan for each module |

## 2. Slash commands: your buttons

A slash command is a saved prompt. Typing `/session-start` sends the text of `.claude/commands/session-start.md` to Claude as if you'd typed it. Some take an argument (`/teach-back calibration`), which is inserted where the file says `$ARGUMENTS`. Analogy: **shell aliases or Makefile targets** for prompts.

| Command | Use it when | What it does |
|---|---|---|
| `/session-start` | Start of every session | Fetch, read STATUS/HANDOFF/notebook, summarise, propose a plan, ask about priorities |
| `/session-end` | End of every session | Write notebook, STATUS, ledger, HANDOFF; commit on a branch; three questions for you |
| `/handoff` | Switching machine | Like session-end, focused on HANDOFF; commits and pushes |
| `/phase-brief A-1` | Before a new phase | Writes the Phase Brief and waits for your "go" |
| `/lit-review <question>` | Phase R research | Searches literature for a design question, writes paper notes |
| `/open-pr` | Work is ready to show | Opens or updates a draft PR with the template |
| `/teach-back <concept>` | You want to test yourself | You explain; Claude grades and fills gaps |
| `/viva-drill <topic>` | Every two weeks or before a gate | Mock examiner, one question at a time |
| `/weekly-review` | Once a week | Plan versus reality, risks, open work, understanding |

Note: Anthropic now prefers the "skills" format (`.claude/skills/<name>/SKILL.md`) over `.claude/commands/`. The old format still works; this session showed all nine commands as available.

## 3. Subagents: helpers with their own context

A subagent is a separate Claude instance that Claude can hand a task to. It starts with an **empty context**, gets only the tools listed in its file, and returns a report. Analogy: a **worker process with restricted permissions** (a sandboxed child process that returns a result over a pipe).

| Agent | Tools | Purpose |
|---|---|---|
| reviewer | Read, Grep, Glob (read-only) | Reviews code for bugs, leakage, reproducibility, comments, tests |
| dataset-scout | Read, Grep, Glob, WebSearch, WebFetch | Finds and verifies candidate datasets; returns a report |
| examiner | Read, Grep, Glob | Asks viva questions from the repo's contents; used by `/viva-drill` |

All three are set to the `sonnet` model and are read-only, so they can't change files. Why separate agents? (a) A fresh context gives an independent view (a reviewer who didn't write the code). (b) A long web search doesn't fill the main conversation. Cost: each one starts cold and uses Pro-plan usage, so they're used deliberately, not by reflex.

## 4. Permissions: allow, ask, deny

Before running a tool, Claude Code checks `.claude/settings.json`:

```
 tool call ──> matches deny?  ──yes──> refused
                  │no
                  v
              matches ask?   ──yes──> you get a prompt (approve/decline)
                  │no
                  v
              matches allow? ──yes──> runs silently
                  │no
                  v
              default: you get a prompt
```

What this kit sets:

| List | Examples |
|---|---|
| allow | Reading files; `git status/diff/log/add/commit/switch/fetch`; `gh issue *`; `gh pr create --draft`; `make`, `pytest`, `ruff` |
| ask | `git push`, `gh api`, `gh repo`, `pip install`, `uv add`, `npm install` |
| deny | Reading or writing `.env`; `git push --force`; `git reset --hard`; `gh pr merge`; `gh repo delete`; `rm -rf` |

Personal overrides go in `.claude/settings.local.json`, which is git-ignored, so they never reach the other machine or GitHub.

## 5. Hooks: code that runs around Claude's actions

A hook is a script that Claude Code runs automatically at a given moment. **PreToolUse** runs before a tool call and can **block** it (exit code 2; the script's message is shown to Claude). **PostToolUse** runs after it and can report problems. Analogy: **git hooks or middleware**. Permissions match command patterns; hooks run real code, so they can check things a pattern can't, such as "which branch am I on?" or "which files are staged?".

| Hook | When | Blocks or reports |
|---|---|---|
| `guard_bash.py` | Before every Bash command | Blocks: force push; any push naming `main`/`master`; pushing while on `main`; `gh pr merge`; `git commit` on `main`; committing staged data/rasters/weights/`.env` |
| `guard_files.py` | Before Edit/Write | Blocks writes to `.env*`, `data/raw/`, frozen split files `configs/splits/frozen_*` |
| `post_edit_check.py` | After Edit/Write of a `.py` file | Runs `ruff check` on that file and reports findings (does nothing if ruff isn't installed, which is the case today) |

Why both permissions and hooks? Defence in depth: two independent layers, so one mistake doesn't get through.

Limit worth knowing: hooks only guard **Claude's** actions. Commands you type in your own terminal don't go through them. On GitHub, the ruleset (F4) is what protects `main` from everyone.

## 6. What Claude Code doesn't do here

- **Auto memory** (`~/.claude/projects/.../memory/`) exists but is machine-local, so the rules say not to rely on it for project facts. Repository files are the memory (F1).
- Claude doesn't merge PRs. Both the deny list and a hook enforce this.

## What goes wrong?

- A long CLAUDE.md wastes context in every session. Keep rules there and detail in `docs/agent/`.
- Approving permission prompts without reading them defeats the "ask" list.
- Editing `.claude/settings.json` changes the guard rails for every machine. That's a reviewable change, so it goes through a PR.

## Check yourself

1. What is the difference between `CLAUDE.md` and `docs/agent/GITHUB_WORKFLOW.md` in when they're loaded, and why is it split that way?
2. Claude tries `git push origin main`. Which two mechanisms stop it?
3. Why are the subagents read-only, and why might the reviewer find bugs that the main session missed?
