---
type: status
status: living
tags: [status]
---

# STATUS

Last updated: 2026-10-10, machine Photon (laptop). Branch `docs/6-phase-r-plan`.

## Current position

- Stage 1, step R (Research and architecture), issue #6.
- Phase R step 1 (design questions) drafted; step 2 (literature search) not started.

## Done

- Project kit imported (`bda08a0`); labels, milestones, seed issues #6 to #13 exist on GitHub.
- First session: STATUS, lab notebook, machine record, [design questions](architecture/design_questions.md), [hypothesis register](architecture/hypothesis_register.md), search log stub, lesson L00 (how to read a paper).

## In progress

- Phase R (#6): user review of design questions and hypothesis register.

## Next

1. User reviews DQ and hypothesis drafts; answers the L00 check questions.
2. Lesson L01: Sentinel-2 basics (curriculum item 1), then read Drusch et al. 2012 together (verify at source first).
3. First literature search round for P1 questions (DQ-01, DQ-04, DQ-05, DQ-10); log in `research/search_log.md`.
4. After Phase R decides the tooling: issue #7 (scaffold), which also turns CI green.

## Open decisions (user)

- DQ-01: the kit is inconsistent on the first dataset (Brazil-Crop in MODULE_A section 0, France in its section 8). Resolve at Checkpoint R after the audit.
- Code licence (MIT or Apache-2.0): not yet asked; needed before scaffolding.

## Blockers and known issues

- CI (`ci`) fails on `main` and on Dependabot PRs #1 to #5: `setup-python` finds no `requirements.txt`/`pyproject.toml`. CodeQL JavaScript fails because there is no JS code yet. Both expected until issue #7. Dependabot PRs left open until then.
- Dependabot pip and npm update jobs fail for the same reason (`/apps/web` does not exist yet).
- NVIDIA driver not working on Photon (`nvidia-smi` fails). Not needed until deep models.
- Obsidian vault was opened at `docs/learning/` instead of `docs/`; `.gitignore` expects `docs/.obsidian/`. User to reopen `docs/` as the vault.

## Compute and disk

- No data downloaded. Project disk use: about 0 GB of the 60 GB budget.
