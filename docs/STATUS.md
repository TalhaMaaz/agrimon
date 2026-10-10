---
type: status
status: living
tags: [status]
phase: R
---

# Status

Last updated: 2026-10-10 (Photon, laptop)

## Where we are
- Stage 1, before Phase R. Kit imported; the foundation guide is read (PR #16); a practice run of the full git/GitHub workflow is done (issue #17, PR #18).
- Project vision recorded: two stages inside the FYP, Stage 1 is the only focus, and Stage 1 also produces transferable standards (`docs/playbook/`). See [PROJECT_CONTEXT 1a](agent/PROJECT_CONTEXT.md).
- No code yet.

## Done
- CI unblocked (PR #18, draft): `ci` passes without `pyproject.toml`; CodeQL scans Python only.
- Vision, STATUS, lab notebook, playbook index (this PR, issue #19).

## In progress / waiting for the user
Merge order (the user merges; each must show green `ci`):
1. **PR #18** (CI fix). Mark ready, squash-merge, delete branch.
2. **PR #19's PR** (this one: vision and status). Click *Update branch* first if GitHub asks.
3. **PR #16** (foundation guide) and **PR #14** (Phase R plan): *Update branch*, wait for green, review, merge.
4. **Dependabot #1 to #5**: review one at a time (next practice: reviewing someone else's PR).

## Next
- **Phase R** (issue #6, PR #14): research plan, design questions, hypothesis register, then a dataset search for the Stage 1 country (polygons + crop labels, sugarcane preferred) and the reading list papers with notes.

## Open decisions
- Licence for the code (gap G5: MIT or Apache-2.0).
- Python version for the project (gap G9, decided in #7).

## Blockers
- None once #18 is merged.

## Known issues
- `guard_bash.py` blocks any command that contains both `git push` and the word `main`, even `gh pr create --base main` in the same command. Workaround: run push and PR creation as separate commands. Fix later (small hook change).
- NVIDIA driver not loaded on Photon (gap G11); needed before deep models, not for Phase R.

## Disk and compute used
- Nothing beyond the repo.
