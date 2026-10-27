---
type: handoff
status: living
tags: [handoff]
---

# Handoff (overwritten at every /handoff; history is in Git)

Last updated: 2026-10-27, Photon (laptop)
Branch: `docs/6-kit-audit` (draft PR #27)
Last commit: see `git log -1` on that branch

## What I was doing and why
Re-planning Phase R from the end-product interface after auditing the preloaded kit. The user chose the US stack (CSB + CDL), starting with Louisiana. The intro presentation is about two weeks after 2026-10-27.

## State of the work
- Done: kit audit, product spec, revised DQs/hypotheses, dataset round 1, CDL accuracy table.
- In progress: PR #27, waiting for the user.
- Not started: Louisiana data check, literature pass, roadmap rewrite, presentation.

## Commands to resume (copy-paste)
```
git switch main && git pull --ff-only && git fetch --prune   # after #27 is merged
claude   # then /session-start
```

## Open decisions and questions for the user
- Approve the small Louisiana CSB sample download (under 500 MB) when proposed.
- DQ-14: cane vs non-cane design (decided with evidence).
- Code licence (MIT or Apache-2.0), before #7.

## Things that are only on the old machine (data, caches, env) and how to recreate them
- Nothing. No data downloaded, no environment created yet.

## Gotchas learned (things a fresh session would trip over)
- The shell is zsh: `set -- $var` doesn't split words. Use `bash -c '...'` for word-splitting loops.
- Don't click *Update branch* on Dependabot PRs; comment `@dependabot rebase`. If the rebase is slow, resolve by hand only when the PR is merged straight after.
- A squash-merged branch shows as "diverged" from `main`; compare content (`git diff <squash-commit> <branch>`) before deleting it.
- `ruff format <dir>` formats every file in it; pass single files to keep diffs focused.
- The local network sometimes drops (curl returns `000`); WebFetch still works. Retry rather than conclude a service is down.
- `gh` uses its own login; git pushes over HTTPS need `gh auth setup-git` (done on Photon 2026-10-27).
- NASS CDL metadata URLs: `.../Cropland/metadata/metadata_<st><yy>.htm`; 2024 and 2025 returned 404.
- The Obsidian vault is `docs/`; Obsidian rewrites `MAP.canvas` and `.obsidian/*.json` in its own format. Those diffs are harmless.
