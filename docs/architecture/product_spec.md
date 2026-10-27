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

## 4. Capabilities to data requirements

What a Stage 1 region must offer for each capability. The dataset search (DQ-01) scores candidates against this table; a "stack" of sources for one region is allowed (kit audit F-02).

| Capability | Data it needs | Minimum to build it | Best case | Design questions |
|---|---|---|---|---|
| P-1 field polygons | field boundaries for the labelled seasons **and** for a recent season (for the live health layer) | polygons for the labelled seasons; recent boundaries assumed unchanged | annual parcel polygons up to the current year | DQ-01, DQ-05, DQ-23 |
| P-2 crop type | per-field crop labels with known date; enough fields per class; more than one season or region for honest splits | a few thousand fields, sugarcane or not, two seasons or regions | many fields over several years, sugarcane as a class | DQ-01, DQ-10, DQ-14, DQ-21 |
| P-3 health | Sentinel-2 (and possibly Sentinel-1) time series per field; several years of history per crop for an expected curve; weather and soil-moisture context; documented events (drought, flood) for validation | 2+ years of imagery history over the labelled fields; one documented event | 5+ years of history; field-level stress reports | DQ-03, DQ-06, DQ-18, DQ-21 |
| P-4 yield | yield statistics for the same region and years, at field, farm or district level; harvest dates | district or municipal statistics over several years | field- or farm-level yields | DQ-22 |
| all | licence that allows thesis use and publication of figures; imagery coverage; tolerable cloud | open licence, recorded | permissive licence (CC BY or public domain) | DQ-04 |

```
 one region, several sources:

   polygons + labels ----+
   (P-1, P-2)            |
   imagery history ------+---> same fields, same years ---> P-1..P-4
   (P-3)                 |
   weather, events ------+
   yield statistics -----+
   (P-4)
```

## 5. Constraint

- The FYP introductory presentation is about two weeks after 2026-10-27. It must say clearly: the plan, the deliverables, what can and cannot be done. The user did not share other dates; don't ask for them.
