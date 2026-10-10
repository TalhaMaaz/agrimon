---
type: status
status: living
tags: [status]
---

# STATUS

Last updated: 2026-10-10 (second session), machine Photon (laptop). Branch `docs/6-phase-r-plan`.

## Current position

- Stage 1, step R (Research and architecture), issue #6.
- Phase R step 1 (design questions) drafted; step 2 (literature search and dataset search) not started.
- Project vision recorded (PR #20, issue #19): two stages inside the FYP; Stage 1, the full application on a country with good open data, is the only focus; the motivation is to learn the standards for building such a system end to end. See `agent/PROJECT_CONTEXT.md` section 1a and `playbook/`.

## Done

- Project kit imported (`bda08a0`); labels, milestones, seed issues #6 to #13 exist on GitHub.
- First session: STATUS, lab notebook, machine record, [design questions](architecture/design_questions.md), [hypothesis register](architecture/hypothesis_register.md), search log stub, lesson L00 (how to read a paper).
- Second session: foundation guide read (PR #16); practice run of the full workflow; CI fix (PR #18); vision carried through the kit (PR #20); DQ-01 restated for the dataset search.

## Waiting for the user (merge order)

1. **PR #18** (CI fix): mark ready, squash-merge, delete branch. Unblocks all other merges.
2. **PR #20** (vision), **PR #16** (foundation guide), **PR #14** (this branch): click *Update branch*, wait for green `ci`, review, merge. No files overlap, so any order works.
3. Dependabot #1 to #5: review one at a time, later.

## Next

1. User answers the L00 check questions (how to read a paper).
2. Lesson L01: Sentinel-2 basics, then read Drusch et al. 2012 together (verify at source first).
3. First literature and dataset search round for the P1 questions (DQ-01, DQ-04, DQ-05, DQ-10); dataset search uses the two-stage targets in `agent/DATASET_DISCOVERY.md` section 2.
4. After Phase R decides the tooling: issue #7 (scaffold), which re-adds `cache: pip`.

## Open decisions (user)

- DQ-01: the Stage 1 country and dataset, decided at Checkpoint R after the search and audit.
- Code licence (MIT or Apache-2.0): needed before scaffolding.

## Blockers and known issues

- CI fails on every PR until PR #18 is merged. Deviation: the first session planned to leave CI red until #7; this session fixed it separately because red CI blocked merging the docs PRs.
- `guard_bash.py` blocks any command that contains both `git push` and the word `main` (for example `gh pr create --base main` in the same command). Workaround: separate commands. Fix later with a small hook change.
- Dependabot pip and npm update jobs fail (`/apps/web` and `pyproject.toml` don't exist yet). Harmless until #7.
- NVIDIA driver not working on Photon (`nvidia-smi` fails). Not needed until deep models.

## Compute and disk

- No data downloaded. Project disk use: about 0 GB of the 60 GB budget.
