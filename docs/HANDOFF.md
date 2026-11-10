---
type: handoff
status: living
tags: [handoff]
---

# Handoff (overwritten at every /handoff; history is in Git)

Last updated: 2026-11-10, laptop
Branch: `docs/presentation-final-touches`

## What I was doing and why
Finishing the mid-semester presentation. Designed deck (16 slides): https://claude.ai/artifact/N6e6SsWzupuPcMasPJ46eX. Plain black-and-white copy: https://claude.ai/artifact/KnVFM1Q13BiS3nwUiY3WfB. Details in `docs/lab_notebook/2026-11-10.md`.

## State of the work
- Done: spike env, S01, S02, B02, B03, existing-systems review, requirements, deck (with use-case diagram and ERD), plain copy.
- Next: Talha sends their own presenter-notes document; review it against the slides, sources and the 10-minute limit (do not edit deck notes until then).
- Pending doc updates: see the open list in the 2026-11-10 notebook entry.
- Not started: S03 Sentinel-2, S04 yields, literature round 2, Checkpoint R.

## Commands to resume (copy-paste)
```
cd ~/Documents/University/FYP\ -\ AgriMon/agrimon
git switch main && git pull --ff-only && git fetch --prune
~/miniforge3/envs/agrimon-spikes/bin/jupyter lab     # spikes; kernel "Python (agrimon-spikes)"
claude   # start from INSIDE agrimon/ so the repo agents load; then /session-start
```

## Gotchas
- PROJ/GDAL need `PROJ_DATA`/`GDAL_DATA` unless the env is activated (the kernel sets them).
- MDPI and ScienceDirect block automated fetches; the user downloads PDFs into `Presentations/`.
- The national CSB/CDL files live in `data/raw/` (git-ignored, kept).

## Open decisions and questions for the user
- Earth Engine Cloud project ID (to finish the GEE setup).
- Four PDFs (Hu 2022, sugarcane review 2021, Punjab 2024, Weiss 2020).
- Supervisor meetings and feedback, Gantt dates for the deck.
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
