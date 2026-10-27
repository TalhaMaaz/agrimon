---
type: architecture
status: draft
tags: [architecture, phase-r, audit, roadmap]
phase: R
---

# Kit audit (2026-10-27)

Purpose: re-evaluate everything the kit preloaded (plans, module files, design questions, hypotheses, issues, milestones, reading list, lessons) against the project's bigger plan, before Phase R step 2 starts. Requested by the user on 2026-10-27.

The bigger plan, as the user restated it on 2026-10-27:

```
 Stage 1: one country + dataset that carries the WHOLE project
          (every phase, every module, the demo) and matches the
          interface of the eventual end product
              |
              v
 Stage 2: move to Pakistan with what Stage 1 taught us
```

Method: every file in `docs/agent/`, `docs/architecture/`, `docs/learning/` (MAP, L00, F6), the open issues and the milestones were read. Facts the plan depends on were checked at the source on 2026-10-27. Severity: **high** changes the plan; **medium** is an inconsistency to fix while re-planning; **low** is cosmetic.

## 1. Verdict in one picture

```
 KEEP (sound)                          CHANGE (conflicts with the bigger plan)
 ------------                          ----------------------------------------
 Phase R method, evidence rules        no definition of the end-product interface
 hypothesis register discipline        dataset chosen for module A only
 spatial validation emphasis           sugarcane treated as an annual crop
 stream-don't-cache rule               module A detail written for France
 GEE behind an interface               yield (C) demoted without a product reason
 honest "health" framing (module B)    bridge/second dataset placed mid-stage
 anti-pattern lists                    issues #10-#13 assume the old plan
 git/GitHub workflow, hooks, CI        Pakistan dataset status out of date
```

The kit's method is good. Its content was planned around one module (crop classification) and one candidate dataset (Brazil-Crop), not around "one dataset that carries the whole application". That is the main thing to fix.

## 2. Findings

### F-01 (high): the end-product interface is never defined

The kit defines modules (A classify, B health, C yield) but not what the finished application shows its user. MODULE_A section 0b and A-Phase 8 describe a replay map of crop colours; MODULE_B section 2 leaves "what decisions would a user make" for Gate B0, after Module A is built. So the modules are planned bottom-up, from the data, rather than from the product.

Why it matters: the user wants Stage 1 to match the interface of the end product. Without a written target interface, the dataset search can't test "does this dataset support the product?", and the roadmap can't be ordered by what the product needs.

Fix: write a short Stage 1 product specification (screens, per-field and per-region outputs, refresh rate, who uses it) before the dataset search, and derive the data requirements from it. This stays FYP-scoped: it describes the Stage 1 application, not a startup plan.

### F-02 (high): the dataset rubric checks Module A only

DATASET_DISCOVERY section 4 scores relevance, provenance, geometry, size, licence and so on, but not whether one dataset can carry **all** modules and the demo. What each part needs:

| Part | Needs from the data |
|---|---|
| A classification | field polygons, per-field crop labels, enough fields per class |
| A honest evaluation | more than one year or region, for held-out splits |
| A Tier 2 demo, B near-real-time | polygons for a **current** season, so live imagery can be read per field |
| B health baselines | several years of history per crop and region |
| B validation | documented events (drought, flood) in the region and years |
| C yield | yield statistics at some level (field, farm, or district) for the same region |

Brazil-Crop, the kit's first choice, was verified at the source on 2026-10-27. It has 5,477 fields in 30 classes including sugarcane, CC BY 4.0, from four campaigns between Jan 2020 and Jun 2021 in two regions. Its vectors are only 16 MB of the 10.4 GB; the rest is photos. It fits A, but has two seasons per region and no current-season polygons. So it can't carry B's near-real-time path, the Tier 2 demo or multi-year baselines on its own. The kit's hedge, EuroCrops France, has many years but no sugarcane.

Fix: add a criterion "module and demo coverage" to the rubric, and allow a dataset **stack**: one region where labels, multi-year polygons, statistics and events overlap. Don't require a single file to do everything.

### F-03 (high): sugarcane breaks the annual-crop assumption

Module A assumes one crop per field per season: in-season truncation, "which crop is planted today", season-year splits. Sugarcane is semi-perennial. It grows for roughly a year or more, is ratooned (regrown from the stubble) for several cycles, and is harvested over a long window. The kit only mentions this at the end of A-Phase 9, as a question for later.

Why it matters: the label ("is this cane, and which cycle?"), the time window, the health baseline ("expected curve since planting or since the last harvest") and any harvest or yield output all depend on it. Sugarcane is the crop the project ultimately cares about.

Fix: new design question (proposed DQ-21), answered in Phase R from the literature on sugarcane remote sensing.

### F-04 (high): yield (Module C) is demoted without a product reason

CLAUDE.md and MODULE_C call yield "not important" and default it to a feasibility note. For a sugar-mill-style user, supply forecasting (expected tonnage, harvest timing) is plausibly a central output, not a side note. That is a product question, not a data question.

Fix: decide C's priority from the Stage 1 product specification (F-01). Option kept open: "harvest timing or maturity" as a Module B output, which needs less ground truth than yield.

### F-05 (medium): Module A's operational detail is written for France

MODULE_A section 0 prefers Brazil-Crop, but sections 1, 4 and A-Phases 1 to 3 give France-specific steps: HCAT4 classes, "tile within France", EuroCrops column names, train 2021 / validate 2022 / test 2023, and "winter cereals peak before maize". The class-size rules also conflict: section 0 asks for 200 or more fields per class, while section 4 asks for at least 500 training parcels per class. With 5,477 fields across 30 classes, Brazil-Crop can't meet 500 per class for most classes.

Fix: rewrite MODULE_A to be dataset-neutral, with dataset-specific details in the dataset's own file (`docs/research/datasets/<id>.md`) once it is chosen.

### F-06 (medium): the order of milestones conflicts with the roadmap

The second dataset and the Pakistan bridge are A-Phase 9 and milestone M2, placed **before** Module B (M3). ROADMAP section 2 places the Bridge last, after the thesis work. MODULE_B also says "plan for week 12", and the READING_LIST reading order uses weeks, both against the "no weeks" rule in ROADMAP.

Fix: re-order the milestones in the new roadmap; remove week references.

### F-07 (medium): the Pakistan dataset now exists and is verified

The kit lists "Pakistan Sentinel-2 field time series (Zenodo record 22806700)" as "not verified; record ID and claims may be wrong". Checked at the source on 2026-10-27, the record is real:

- **Title:** "Sentinel-2 Field-Level Crop Phenology Time Series in Pakistan (85,618 Fields, 79 Districts, Rabi & Kharif)". Contact: Saeed Ali, NUST. Published 2026-09-17, version 1, CC BY 4.0.
- **Rabi 2022:** 26,428 fields, 5 crops (wheat, rapeseed and mustard, barseem, maize, sugarcane).
- **Kharif 2023:** 59,190 fields, 7 crops (rice, cotton, sugarcane, maize, sorghum, jantar, sesame).
- **Format:** one 51.4 MB archive of per-field time series with district and province identifiers. The page does **not** mention field polygons.

Why it matters: Stage 2 starts from a real dataset. If it holds only time series (no polygons), the Stage 1 pipeline should accept "per-field time series" as an input, separate from "polygons plus imagery". That is a design choice to make now, cheaply (affects H-01 and the label-adapter interface, issue #11). It does **not** change the Stage 1 focus.

User decision (2026-10-27): not now. Focus on Stage 1; Pakistan data is revisited in Stage 2. The record stays in the catalogue as a Stage 2 lead; no download.

### F-08 (medium): issues #10 to #13 assume the old plan

#10 (audit first dataset), #11 (label adapter), #12 (imagery pilot for 1,000 parcels) and #13 (baselines with spatial blocks) were created before Phase R, from the kit's Module A plan. They may still be right, but their scope should follow the new roadmap. #8 (CI setup) is done and should be closed. #7 (scaffold) still waits for DQ-20.

### F-09 (medium): the roadmap can't be made "seamless" without dates

No thesis or defence deadline, university template or requirement is recorded (Checkpoint 0 asks for them, but Checkpoint 0 comes after Phase R). The kit also says "there are no research questions". Some universities require objectives or research questions in an FYP thesis; worth checking.

### F-10 (low): facts to re-verify before relying on them

| Claim in the kit | Status on 2026-10-27 |
|---|---|
| Planetary Computer STAC (`sentinel-2-l2a`) is the default imagery path | Not verified. The live test failed because the local network was down. Web search found no retirement notice, but no 2026 status either. Re-test when the network is back |
| Sentinel-2 "two-satellite constellation, about 5-day revisit" | The constellation changed after the kit's sources: Sentinel-2C launched in 2024. Re-verify the current configuration |
| READING_LIST tiers 3 and 4 | Mostly "title only" or "not yet verified". Expected; verify as phases approach |
| MAP's system picture labels the dataset "Brazil-Crop" | A hypothesis drawn as a fact; update after DQ-01 |

### F-11 (low): what was checked and is fine

The L00 and F1–F6 check questions are about method, not kit facts, so they stay valid. TEACHING_PROTOCOL, DOCUMENTATION_PROTOCOL, GITHUB_WORKFLOW, the hooks and CI are unaffected. MODULE_B's honesty rules (no disease diagnosis, measured latency, neighbour comparison, no invented labels) are sound and should stay.

## 3. Proposed re-planning sequence (for the user's approval)

```
 1. user answers the product and constraint questions (F-01, F-04, F-09)
 2. Stage 1 product spec          docs/architecture/product_spec.md
    (screens, outputs, refresh, user) -> capability list
 3. capability -> data requirements matrix (F-02)
 4. revise design questions + hypothesis register
    (new: DQ-21 sugarcane cycle, DQ-22 yield data,
     DQ-23 current-season polygons; H-08/H-12 re-framed)
 5. dataset search round with the coverage criterion (DQ-01)
 6. rewrite ROADMAP, MODULE_A/B/C (dataset-neutral), milestones, issues
 7. Checkpoint R as before
```

Steps 1 to 4 and 6 are documents; step 5 is the research the kit already planned, with a better rubric.

## 4. Sources checked on 2026-10-27

- Brazil-Crop record: https://zenodo.org/records/18461147
- Pakistan field time series record: https://zenodo.org/records/22806700
- Fields of The World (field boundaries, 24 countries): https://arxiv.org/abs/2409.16252 (seen in search results only)
