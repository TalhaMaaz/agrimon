---
type: handoff
status: living
tags: [handoff]
---

# Handoff (overwritten at every /handoff; history is in Git)

Last updated: 2026-10-27, Photon (laptop)
Branch: `docs/6-close-session-2` (session-end PR); everything else is on `main`
Last commit: see `git log -1` on that branch

## What I was doing and why
Setup before Phase R, now complete: CI fixed (#18), vision carried through the kit (#20), foundation guide (#16) and Phase R plan (#14) merged, hook false positives fixed (#22), glossary created, Dependabot #1 to #5 merged.

## State of the work
- Done: everything above; Photon synced with `main` (only branch).
- In progress: the session-end PR #23 and Dependabot PRs #24 to #26, waiting for the user to merge.
- Not started: Phase R step 2 (literature and dataset search).

## Commands to resume (copy-paste)
```
git switch main && git pull --ff-only && git fetch --prune
claude   # then /session-start
```

## Open decisions and questions for the user
- Review the design questions and hypothesis register (`docs/architecture/`).
- L00 check questions (how to read a paper).
- Code licence: MIT or Apache-2.0 (needed before #7).

## Things that are only on the old machine (data, caches, env) and how to recreate them
- Nothing. No data downloaded, no environment created yet.

## Gotchas learned (things a fresh session would trip over)
- The shell is zsh: `set -- $var` doesn't split words. Use `bash -c '...'` for word-splitting loops.
- Don't click *Update branch* on Dependabot PRs; comment `@dependabot rebase`. If the rebase is slow, resolve by hand only when the PR is merged straight after.
- A squash-merged branch shows as "diverged" from `main`; compare content (`git diff <squash-commit> <branch>`) before deleting it.
- `ruff format <dir>` formats every file in it; pass single files to keep diffs focused.
- The Obsidian vault is `docs/`; Obsidian rewrites `MAP.canvas` and `.obsidian/*.json` in its own format. Those diffs are harmless.
