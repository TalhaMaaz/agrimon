---
type: lesson
status: draft
tags: [lesson, foundation, git]
phase: R
---

# F3: Git as we use it

Previous: [F2 Claude Code in this kit](F2_claude_code_kit.md) | Next: [F4 GitHub features](F4_github.md)

## What is it?

Git is a program that records **snapshots** of a folder over time. Each snapshot is a **commit**: the full state of the tracked files plus a message, an author, a date and a pointer to the previous commit. Commits form a chain (a graph), and the chain is the project's history.

Analogy: a **linked list of immutable snapshots**. Each commit has an ID (a hash such as `bda08a0`) computed from its contents and its parent, so history can't be changed silently.

## The five places your work can be

```
  working folder  --git add-->  staging area  --git commit-->  local repo  --git push-->  remote (GitHub)
  (files you edit)              (what goes into                (your commits)               (origin)
                                 the next commit)                    ^                          |
                                                                     +------ git fetch / pull --+
```

| Command | Meaning |
|---|---|
| `git status` | What changed, what's staged, which branch, ahead/behind the remote |
| `git add <file>` | Put a change into the staging area |
| `git commit -m "..."` | Make a snapshot of the staging area |
| `git push` | Send your commits to GitHub |
| `git fetch` | Download others' commits (here: Dependabot's) without changing your files |
| `git pull --ff-only` | Fetch, then move your branch forward, only if no merge is needed |
| `git log --oneline` | Show the history |
| `git switch -c <name>` | Create a branch and move onto it |

## Branches

A branch is just a **movable name pointing at a commit**, like a variable holding a pointer. Making a branch is cheap. New commits move the branch you're on forward.

Our repository right now (2026-10-10):

```
                      docs/6-phase-r-plan     (PR #14, waiting)
                    /
 bda08a0 ----------+
 "import project   |\
  kit"   (main)    | docs/15-foundation-guide (this guide)
                   |
                    \ dependabot/...  (5 branches, PRs #1..#5, made by GitHub's bot)
```

`main` is the **trunk**: the official, working version. Work never happens on `main` directly.

## Our branch flow (trunk-based, short-lived branches)

```
 1 issue #N exists          "what and why, acceptance criteria"
 2 git switch -c docs/N-slug   branch from latest main
 3 commits on the branch    small, Conventional Commit messages
 4 git push -u origin docs/N-slug
 5 draft PR on GitHub       "Closes #N" or "Refs #N"
 6 CI runs, you review      F4
 7 YOU squash-merge         all branch commits become ONE commit on main
 8 branch deleted           history on main stays a straight line
```

Branch names: `feat/`, `fix/`, `docs/`, `chore/`, `exp/` followed by `<issue>-<slug>`, for example `docs/6-phase-r-plan`.

**Squash merge** and **linear history**: when you merge, the branch's commits are combined into one commit on `main`, so `main` reads as one commit per PR. The ruleset on GitHub requires linear history (no merge bubbles).

## Conventional Commits

Commit messages and PR titles follow a fixed shape: `type(scope): summary`.

```
 docs(research): start Phase R with design questions and hypothesis register
 ^^^^ ^^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 type  scope     what the change does, imperative mood
```

Types: `feat` (new feature), `fix` (bug fix), `docs`, `chore` (maintenance), `test`, `refactor`, `perf`, `build`, `ci`. Why: the history can be read and searched by type, release notes can be generated automatically, and a CI check (F4) rejects PR titles that don't follow the shape.

Commits made by Claude end with a `Co-Authored-By: Claude ...` line. That keeps the AI involvement visible in the history, which supports the PR's AI-disclosure section.

## Remote, ahead and behind

`origin` is the name of the GitHub copy (`https://github.com/TalhaMaaz/agrimon.git`). `git status` compares your branch with its remote counterpart:

```
 "up to date"   same commit on both
 "ahead 2"      you have 2 commits not yet pushed      -> push
 "behind 3"     GitHub has 3 commits you don't have   -> pull --ff-only
 "diverged"     both have new commits                  -> needs a rebase or merge; ask before doing it
```

## What git must never hold

Data, rasters, model weights, `.env` (secrets). They are blocked in three places: `.gitignore` (git doesn't see them), the Claude hook (refuses to commit them) and CI (fails if they appear). Why: git keeps every version forever, so one committed 2 GB file or one leaked token stays in the history even after you "delete" it.

## What goes wrong?

- Committing on `main`: your `main` and GitHub's `main` diverge. The hook blocks Claude from doing it; be careful in your own terminal.
- Long-lived branches drift from `main` and conflict. Keep PRs small (under about 400 changed lines).
- Two branches editing the same file (for example `understanding_ledger.md` in PR #14 and in another PR) conflict at merge. Merge one, then update the other.
- Force-pushing rewrites history others rely on. It's denied for Claude and blocked on `main` by the ruleset.

## Check yourself

1. What is a branch, technically, and why is creating one cheap?
2. PR #14 has one commit; if it had five, how many commits would land on `main` after a squash merge?
3. Your laptop says "behind 1" after a fetch. What happened, and what command fixes it safely?
