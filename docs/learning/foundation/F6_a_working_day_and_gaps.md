---
type: lesson
status: draft
tags: [lesson, foundation, workflow]
phase: R
---

# F6: A working day, and gaps

Previous: [F5 The documentation system](F5_documentation_system.md) | Back to [index](F0_index.md)

## A working day, end to end

```
 YOU                                   CLAUDE                                   GITHUB
 ---                                   ------                                   ------
 open terminal in repo, run `claude`
 /session-start  ───────────────────>  git fetch; read STATUS, HANDOFF,
                                       notebook; summarise; propose plan
 answer: priorities, decisions  ────>
                                       (new phase?) /phase-brief -> wait for "go"
                                       issue exists? branch from main
                                       lesson on the new concept
                                       write code/docs, commit on branch
                                       git push  (you approve the prompt) ───────>  branch appears
                                       /open-pr (draft) ─────────────────────────>  PR; CI, CodeQL,
                                                                                   labeler run
                                       walkthrough of the diff
 read diff + walkthrough;
 ask until you can explain it
 mark ready, squash-merge  ───────────────────────────────────────────────────>  main moves forward
                                                                                   issue closes
 /session-end  ─────────────────────>  notebook, STATUS, ledger, HANDOFF,
                                       MAP; commit; push
```

Rhythm on top of the daily loop (see `learning/WEEKLY_RHYTHM.md`): `/weekly-review` weekly, `/viva-drill` every two weeks, a documentation audit monthly.

### Switching machines (laptop to lab PC)

```
 leaving machine:  /handoff         -> HANDOFF.md updated, branch pushed, git status clean
 arriving machine: git fetch --all --prune && git switch <branch> && git pull --ff-only
                   claude  ->  /session-start
```

### Phase lifecycle (bigger loop)

```
 /phase-brief -> your "go" -> primer lessons -> build in small PRs -> checkpoint report
     -> 3 viva-style questions -> phase report, ADRs, registers updated -> next phase
```

## What you type versus what you click

| You type in Claude Code | You do yourself (browser or terminal) |
|---|---|
| `/session-start`, `/session-end`, `/handoff` | Review the diff on GitHub ("Files changed" tab) |
| `/phase-brief`, `/lit-review`, `/open-pr` | Mark a draft PR ready; squash-merge; delete the branch |
| `/teach-back`, `/viva-drill`, `/weekly-review` | Write your notes in `docs/learning/my_understanding/` |
| Normal questions and requests | Approve or decline permission prompts (read them) |

## Gaps between the kit and reality

Checked on 2026-10-10. Ordered by how much they block work.

| # | Gap | Effect | Proposed fix |
|---|---|---|---|
| G1 | `ci` fails on every branch: `setup-python` uses `cache: pip` but there is no `pyproject.toml`/`requirements.txt` | The ruleset requires `ci` to pass, so **no PR can be merged** (including #14 and this guide) | Small `chore(ci)` PR: drop `cache: pip` until a `pyproject.toml` exists, or make it conditional. Every other `ci` step already skips when there is no `pyproject.toml` |
| G2 | CodeQL JavaScript analysis fails: there is no JS code | Red cross on every PR (not merge-blocking: only `ci` is required) | Same PR: analyse only Python until `apps/web/` exists |
| G3 | Dependabot pip and npm jobs fail; npm points at `/apps/web`, which doesn't exist | Noise; no harm | Leave until #7 creates `pyproject.toml` and the web app exists |
| G4 | Dependabot PRs #1 to #5 (Actions major bumps) | Can't merge (G1); need review | After G1: review each, check the changelog for breaking changes, merge one at a time |
| G5 | No licence | Public code is "all rights reserved" by default | You choose MIT or Apache-2.0; add `LICENSE` via a PR |
| G6 | Obsidian opened at `docs/learning/` instead of `docs/` | Second, untracked `.obsidian/` folder | See F5 |
| G7 | MAP links to `../glossary.md`, which doesn't exist | Broken link in Obsidian | Create the glossary when the first term is defined (Phase R) |
| G8 | Kit inconsistency: MODULE_A section 0 says Brazil-Crop first; section 8 says France pipeline | Unclear target | Design question DQ-01, settled at Checkpoint R |
| G9 | CI pins Python 3.11; laptop system Python is 3.14 | Version choice not made yet | Decide in #7 (hypothesis H-18) |
| G10 | `gh` login lacks the `read:project` scope | Claude can't see the Project board | Optional: `gh auth refresh -s read:project,project` |
| G11 | NVIDIA driver not loaded on Photon | No GPU for deep models | Fix before Module A deep models |
| G12 | Commands use the older `.claude/commands/` format | None today | Convert to skills later if useful |

G1 is the only one that blocks us now. I recommend fixing it next, in its own small PR, so the review-and-merge loop works before any more docs pile up.

## Check yourself

1. Walk through what happens between "Claude pushes a branch" and "the change is on `main`". Who does each step?
2. Why must G1 be fixed before anything else can be merged?
3. You arrive at the lab PC. What are the first three things you run?
