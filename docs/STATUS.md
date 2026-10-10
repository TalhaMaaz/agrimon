---
type: status
status: living
tags: [status]
---

# STATUS

Last updated: 2026-10-10 (end of second session), machine Photon (laptop). Branch `fix/21-hook-false-positives`.

## Current position

- Stage 1, step R (Research and architecture), issue #6.
- Phase R step 1 (design questions, hypothesis register) drafted and merged (#14), waiting for the user's review; step 2 (literature search and dataset search) not started.
- Pre-Phase-R setup is complete once PR #22 and the Dependabot PRs are merged.
- Project vision recorded (PR #20, issue #19): two stages inside the FYP; Stage 1, the full application on a country with good open data, is the only focus; the motivation is to learn the standards for building such a system end to end. See `agent/PROJECT_CONTEXT.md` section 1a and `playbook/`.

## Done

- Project kit imported (`bda08a0`); labels, milestones, seed issues #6 to #13 exist on GitHub.
- First session: STATUS, lab notebook, machine record, [design questions](architecture/design_questions.md), [hypothesis register](architecture/hypothesis_register.md), search log stub, lesson L00 (how to read a paper).
- Second session: foundation guide read (PR #16); practice run of the full workflow; CI fix (PR #18); vision carried through the kit (PR #20); DQ-01 restated (PR #14). All four merged by the user; branches deleted; laptop synced. Hook false positives fixed with tests (PR #22); glossary created; Dependabot PRs reviewed (all safe).

## Waiting for the user (merge order)

1. **PR #22** (hook fix, glossary, session docs): review, merge.
2. **Dependabot #4, #5, #3, #2, #1**, one at a time. All reviewed as safe (see the 2026-10-10 notebook). If one shows a conflict or "out of date" after the previous merge, comment `@dependabot rebase` on it instead of clicking *Update branch* (a human commit makes Dependabot stop maintaining the PR).

## Next

1. User answers the L00 check questions (how to read a paper).
2. Lesson L01: Sentinel-2 basics, then read Drusch et al. 2012 together (verify at source first).
3. First literature and dataset search round for the P1 questions (DQ-01, DQ-04, DQ-05, DQ-10); dataset search uses the two-stage targets in `agent/DATASET_DISCOVERY.md` section 2.
4. After Phase R decides the tooling: issue #7 (scaffold), which re-adds `cache: pip`.

## Open decisions (user)

- DQ-01: the Stage 1 country and dataset, decided at Checkpoint R after the search and audit.
- Code licence (MIT or Apache-2.0): needed before scaffolding.

## Blockers and known issues

- None blocking. CI fixed in #18 (deviation: session 1 planned to leave it red until #7). Hook false positives fixed in #22.
- Dependabot pip and npm update jobs fail (`/apps/web` and `pyproject.toml` don't exist yet). Harmless until #7.
- NVIDIA driver not working on Photon (`nvidia-smi` fails). Not needed until deep models.

## Compute and disk

- No data downloaded. Project disk use: about 0 GB of the 60 GB budget.
