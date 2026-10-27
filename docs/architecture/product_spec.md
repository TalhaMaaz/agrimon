---
type: architecture
status: draft
tags: [architecture, phase-r, product, requirements]
phase: R
---

# Stage 1 product specification (draft)

The interface the Stage 1 application must have, as stated by the user on 2026-10-27 (answers to the [kit audit](kit_audit.md) finding F-01). Everything else (datasets, design questions, roadmap) is derived from this. It describes the FYP application only, not a startup product.

## 1. The interface

```
 +--------------------------------------------------------------+
 |  web map                                    [date / season]  |
 |                                                              |
 |   +------+   +-----+        layers:                          |
 |   | cane |   | non |        [x] crop type (field polygons)   |
 |   +------+   +-----+        [x] health (per field)           |
 |        +---------+          [ ] yield estimate               |
 |        |  cane   |                                           |
 |        +---------+          click a field ->                 |
 |                               crop + confidence              |
 |                               health status + history        |
 |                               yield estimate (if built)      |
 +--------------------------------------------------------------+
```

| # | Capability | User's words (2026-10-27) | Priority |
|---|---|---|---|
| P-1 | Field polygons on a map | "properly mapped polygons of fields" | must |
| P-2 | Crop type per field | "showing which crop they are"; preferred as **sugarcane vs non-sugarcane**, "but only if this would make our work easier and can be done easily" | must |
| P-3 | Health layer per field | "a health layer on top of each field"; learn which satellite data are useful for health monitoring | must |
| P-4 | Yield estimation | "and then a yield estimation"; priority decided after this spec and data availability (Module C) | open |

## 2. Data preferences

- Sugarcane in the Stage 1 dataset is the best case, but only if that dataset is strong enough for all modules. A cane-free dataset that covers the modules better wins over a weak cane dataset (user, 2026-10-27).

## 3. Open questions this spec raises (to become design questions)

- **Binary versus multi-class (P-2).**
  - **Why binary might be easier:** fewer classes, less class imbalance, and it matches the product.
  - **Why it might not be:** "non-cane" mixes many crops, so it is a hard, varied class. A binary model also shows less about what the model confuses. And Stage 2's Pakistan data are multi-crop.
  - **A middle option:** train multi-class and show cane versus non-cane on the map.
  - Decide in Phase R with evidence.
- **Health for a semi-perennial crop (P-3):** the expected curve must be measured from planting or the last harvest, not from a calendar season (kit audit F-03).
- **Yield (P-4):** what level of yield data exists (field, farm, district) for the chosen region decides whether this is a model or a feasibility note.

## 4. Constraint

- The FYP introductory presentation is about two weeks after 2026-10-27. It must say clearly: the plan, the deliverables, what can and cannot be done. The user did not share other dates; don't ask for them.
