---
type: log
status: living
tags: [log]
---

# LOG

Claude's running log of the project, newest entry at the bottom. Each entry: what was done, decisions and why, numbers, problems, next. Sessions before kit v2 are in the archived [lab notebook](archive/kit-v1/lab_notebook/) and [HANDOFF](archive/kit-v1/HANDOFF.md).

## Before kit v2 (2026-10-10 to 2026-11-10), summary

- **2026-10-10:** kit v1 imported; foundation guides; CI and hook fixes; project vision recorded (Stage 1 on good open data, Stage 2 Pakistan).
- **2026-10-27:** kit audit and re-plan from a product spec. Dataset round 1. **Decision (user): US stack, Louisiana** (CSB boundaries + CDL labels). CDL sugarcane accuracy recorded (producer's 94.1–97.2 %, user's 94.8–96.4 %).
- **2026-10-28 to 2026-11-06:** spike environment pinned. S01 (CSB fields, Iberia): 206,389 field polygons in Louisiana; 4,213 cane fields in Iberia 2023 (threshold ≥ 1,000); median cane field 11.5 acres ≈ 465 Sentinel-2 pixels. S02 (CDL labels): a typical cane field is 94.9 % cane pixels (threshold ≥ 90 %). Existing-systems review, requirements register, briefings B01–B03.
- **2026-11-06 to 2026-11-10:** mid-semester deck built (16 slides, https://claude.ai/artifact/N6e6SsWzupuPcMasPJ46eX), speaker notes, cue cards, full-text literature reading.

## 2026-11-11 · final deck changes

- Deck edits (user-directed): use-case diagram lost its external actors; Datasets slide moved after Method; slide 5 mockup now shows real Iberia fields; three non-functional requirements added as chips; slide 3 problem statement made concrete; final review fixed three typos and a leftover note. Slide 13 baseline changed to Random Forest by the user.
- White-background copy of the deck made: https://claude.ai/artifact/1ggypDcMBre3ofJZwRtuwA. The user chose the coloured deck.
- Regenerated one-page cue cards and wrote a full English speaker script (`docs/presentations/`).
- Problem found: slide 13 speaker notes still say LightGBM while the slide says Random Forest. Not fixed in the deck.

## 2026-11-12 · presentation given; kit v2

- **Presentation:** given; on 2026-11-12 the user reported that it went well. Panel questions and feedback not recorded yet.
- **Decision (user): kit v2.** Reason: kit v1 was too complex for a solo project. Claude keeps this log; teaching, summaries and defence prep happen only on request; git becomes one branch and one PR per milestone.
- **Done:**
  - Removed all kit v1 slash commands (9) and subagents (3); kit v1 is kept at git tag `kit-v1`.
  - GitHub slimmed: kept CI, a 3-line PR template and bug/task issue templates; removed CodeQL, labeler, Pages, release, Dependabot, CODEOWNERS, the PR-title check and the bootstrap script. Labels 29 → 5. Closed finished issues #6, #7, #9, #10, #30; #11–#13 stay open.
  - GitHub settings: `main` protected (PR required, no force push, no deletion); merge commits only; branches auto-delete after merge.
  - Branches: deleted those already merged; folded `docs/presentation-final-touches` and `docs/srs-draft` into `chore/kit-v2`.
  - Docs restructured into `research/`, `design/`, `presentations/`, `learning/` and `archive/kit-v1/` (73 files moved with git mv, all links rewritten and checked). Old team-policy and onboarding files archived.
  - New short CLAUDE.md, five-line STATUS and this LOG. Old versions kept as `archive/kit-v1/CLAUDE_v1.md` and `STATUS_v1.md`.
- **Problems:** the first push of `chore/kit-v2` was refused (token lacked the `workflow` scope); the user re-authenticated and it went through. Merging PR #35 was then blocked: an older GitHub ruleset `protect-main` (from kit v1's bootstrap script) required linear history, which forbids merge commits. Fixed by removing that one rule and limiting the ruleset to merge commits; the ruleset still blocks deletion and force pushes, and requires a PR and a passing `ci` check. The classic branch protection added earlier today duplicated the ruleset and was removed.
- **Decision (user), after the merge of PR #35:** learning is entirely the user's responsibility. No lessons, reminders or milestone pointers; teach only when asked. CLAUDE.md rule 11 rewritten (branch `chore/kit-v2-rules`).
- **Next (written before the merge):** user merges PR #35. Then decide the new kit's commands and helpers, the build timeline (layers 1 + 2 or 1 + 2 + 3) and the milestone pointer; then Stage 1 preprocessing.
