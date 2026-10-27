---
type: status
status: living
tags: [status]
---

# STATUS

Last updated: 2026-10-27 (end of session 3), machine Photon (laptop). Branch `docs/6-kit-audit` (draft PR #27).

## Current position

- Stage 1, step R (Research and architecture), issue #6. Re-planning after the kit audit.
- Re-plan step 1 done: [kit audit](architecture/kit_audit.md), [product spec](architecture/product_spec.md), revised design questions and hypotheses.
- Re-plan step 2 started: dataset round 1 ([catalogue](research/dataset_catalogue.md)). **User decision 2026-10-27: US stack (USDA CSB boundaries + CDL labels), starting with Louisiana.** ADR at Checkpoint R.

## Near-term goal

- FYP introductory presentation, about two weeks after 2026-10-27: plan, deliverables, what can and cannot be done, plus slides. Drives the Phase R order (see `architecture/product_spec.md`).
- Kit audit done 2026-10-27 (`architecture/kit_audit.md`): the kit plans bottom-up from one module and one dataset; re-plan from the product spec.

## Done

- Sessions 1 and 2 (2026-10-10): kit imported, foundation guide, workflow practice, CI and hook fixes, vision recorded, Dependabot #1 to #5. See the notebook for 2026-10-10.
- Session 3 (2026-10-27): #23 to #26 merged by the user; kit audit; product spec; DQ-21 to DQ-23 and H-19 to H-24; rubric criterion 11; dataset round 1; CDL sugarcane accuracy recorded (producer's 94.1 to 97.2 %, user's 94.8 to 96.4 %).

## Waiting for the user

1. Review and merge draft PR #27 (audit, product spec, questions, catalogue, session docs).
2. Close issue #8 (CI setup is done) and delete the merged branches (`docs/6-close-session-2`, `dependabot/.../labeler-7`, `dependabot/.../codeql-action-4`).

## Next

1. Louisiana data check: CSB attributes; a small CSB sample for one cane parish (under 500 MB, ask first); field counts and sizes; NASS parish yields (DQ-22); whether Crop Progress rates sugarcane.
2. Retest the imagery source (Planetary Computer STAC; Earth Search fallback).
3. Re-plan step 3: survey-depth literature on crop type, health signals and sugarcane yield.
4. Re-plan step 4: rewrite ROADMAP, MODULE_A/B/C (dataset-neutral), milestones, issues #10 to #13.
5. Presentation content and deck; `/viva-drill` rehearsal.

## Open decisions (user)

- DQ-01: US stack chosen (Louisiana); years and the exact study area still open.
- DQ-14: binary cane vs non-cane, or multi-class shown as cane vs non-cane (H-19).
- P-4 yield priority: decided once the yield data level is known (DQ-22).
- Code licence (MIT or Apache-2.0): needed before scaffolding.

## Blockers and known issues

- None blocking. CI fixed in #18 (deviation: session 1 planned to leave it red until #7). Hook false positives fixed in #22.
- Dependabot pip and npm update jobs fail (`/apps/web` and `pyproject.toml` don't exist yet). Harmless until #7.
- NVIDIA driver not working on Photon (`nvidia-smi` fails). Not needed until deep models.

## Compute and disk

- No data downloaded. Project disk use: about 0 GB of the 60 GB budget.
