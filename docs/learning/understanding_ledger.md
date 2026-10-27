---
type: ledger
status: living
tags: [ledger]
---

# Understanding ledger

One row per concept. Result is one of: not yet, shaky, solid. The agent updates it after lessons, teach-backs and viva drills; you may disagree with a rating by writing it in the notes column. Before every checkpoint the agent re-teaches the shaky items.

| Concept | Introduced | Lesson | Last check | Result | Notes |
|---|---|---|---|---|---|
| How to read a research paper | 2026-10-10 | [L00](lessons/L00_how_to_read_a_paper.md) | | not yet | Check questions at the end of the lesson |
| Git working tree, staging, commits, branches as pointers | 2026-10-10 | [F3](foundation/F3_git.md), practice run | 2026-10-10 | solid (self-reported) | Practice run on #17; no viva check yet |
| Issue → branch → PR chain and `Closes #N` | 2026-10-10 | [F4](foundation/F4_github.md), practice run | 2026-10-10 | solid (self-reported) | |
| CI workflows, required checks, ruleset | 2026-10-10 | [F4](foundation/F4_github.md), practice run | 2026-10-10 | solid (self-reported) | Fixed the `cache: pip` failure in #18 |
| Claude Code hooks vs server-side guards | 2026-10-10 | [F2](foundation/F2_claude_code_kit.md), practice run | 2026-10-10 | solid (self-reported) | Saw a hook false positive live |
| Merge conflicts (adjacent-line edits) and resolving them | 2026-10-10 | [Notebook](../lab_notebook/2026-10-10.md), PR #3 | | not yet | Seen live on #3; resolved by the agent. Check: why did #2 and #3 conflict? |
| Squash merge and why the branch then looks "diverged" | 2026-10-10 | [F4](foundation/F4_github.md), notebook | | not yet | |
| Product spec drives data needs (top-down planning) | 2026-10-27 | [Product spec](../architecture/product_spec.md), [kit audit](../architecture/kit_audit.md) | | not yet | Check: why did the kit's dataset choice not fit the whole application? |
| Producer's vs user's accuracy (omission vs commission) | 2026-10-27 | [Catalogue S-US](../research/dataset_catalogue.md) | | not yet | CDL sugarcane: 94 to 97 % / 95 to 96 % |
| Model-derived labels and circularity | 2026-10-27 | [DATASET_DISCOVERY rubric](../agent/DATASET_DISCOVERY.md), H-24 | | not yet | |
| Sugarcane as a semi-perennial crop (ratoons) | 2026-10-27 | [Kit audit F-03](../architecture/kit_audit.md) | | not yet | Lesson to come with DQ-21 |
