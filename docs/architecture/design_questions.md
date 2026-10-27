---
type: architecture
status: draft
tags: [architecture, phase-r, design-questions]
phase: R
---

# Design questions (Phase R, step 1)

Purpose: the list of questions the architecture must answer before anything is built. Each question is answered in the [architecture dossier](architecture_dossier.md) (not yet written) with evidence from papers and spikes, and each answer is tracked as one or more rows in the [hypothesis register](hypothesis_register.md).

Status values: **open** (not researched), **researching**, **answered** (evidence recorded, ADR exists).
Priority: **P1** blocks the first build steps of Module A; **P2** needed before Module A finishes; **P3** needed later (Module B, demo Tier 2, Stage 2).

Source: `docs/agent/RESEARCH_AND_ARCHITECTURE.md` step 1, `MODULE_A_CLASSIFICATION.md`, `MODULE_B_HEALTH.md`. Drafted 2026-10-10 by the agent. Revised 2026-10-27 after the [kit audit](kit_audit.md) to follow the [Stage 1 product spec](product_spec.md) (capabilities P-1 to P-4): DQ-01, DQ-14 and DQ-18 reworded; DQ-21 to DQ-23 added; DQ-18 raised to P2. To be reviewed by the user.

```
 data in                     processing                    evaluation              product
 -------                     ----------                    ----------              -------
 DQ-01 dataset               DQ-05 unit of analysis        DQ-10 splits            DQ-15 web stack
 DQ-02 imagery source        DQ-06 clouds and gaps         DQ-11 metrics           DQ-16 serving
 DQ-03 sensors (S1?)         DQ-07 temporal grid           DQ-12 calibration       DQ-17 in-season
 DQ-04 licences/terms        DQ-08 features                DQ-13 model ladder      DQ-18 health (B)
 DQ-22 yield data            DQ-09 compute and storage     DQ-14 class list        DQ-19 Pakistan carry-over
 DQ-23 current polygons      DQ-21 sugarcane cycle                                 DQ-20 repo shape
```

## Data in

| ID | Question | Why it matters | Linked hypotheses | Priority | Status |
|---|---|---|---|---|---|
| DQ-01 | Which country, and which stack of open sources in one region, covers all four product capabilities (polygons, crop labels, health history and events, yield statistics; [product spec](product_spec.md) section 4)? Is a second (pipeline-proving) dataset needed? | Everything downstream depends on label quality, class counts and geography. Kit audit F-02: the kit chose for Module A only; the search now scores module and demo coverage. Chosen by dataset search (user, 2026-10-10): proper field polygons with reliable labels first, sugarcane second, closeness to Pakistani conditions as tiebreaker (DATASET_DISCOVERY section 2). The kit was inconsistent (Brazil-Crop in MODULE_A section 0, France in section 8); PR #20 makes section 8 neutral, so this question now decides it. | H-08, H-12, H-23, H-24 | P1 | researching (user chose the US stack, S-US, on 2026-10-27; still open: Louisiana or Florida, and the years; ADR at Checkpoint R) |
| DQ-02 | Where does Sentinel-2 imagery come from (Planetary Computer STAC, AWS Earth Search, Copernicus Data Space, Google Earth Engine), and through which client? | Determines speed, reliability, cost, and whether the pipeline can be used commercially later. | H-02, H-10 | P1 | open |
| DQ-03 | Is optical imagery alone enough, or is Sentinel-1 radar needed (for Module A, Module B, or both)? | Tropical Brazil and monsoon Pakistan are cloudy; radar sees through cloud but adds a second data path and new concepts. | H-05 | P2 | open |
| DQ-04 | What do the licences and platform terms of each dataset and service allow, now (university) and later (startup)? | Earth Engine is noncommercial for us; some datasets are CC BY-NC. A choice that blocks the startup should be known early. | H-02, H-08, H-10 | P1 | open |

## Processing

| ID | Question | Why it matters | Linked hypotheses | Priority | Status |
|---|---|---|---|---|---|
| DQ-05 | What is the unit of classification: pixel, parcel (polygon aggregate), or image patch? | Sets the data model, the features, the model families and the map. Parcels require polygons, which Pakistan lacks. | H-01 | P1 | open |
| DQ-06 | How are clouds, cloud shadows and missing observations handled (scene filter, per-pixel mask, gap filling, validity mask)? | Wrong masking puts clouds into the features; aggressive masking leaves empty time series. | H-11 | P1 | open |
| DQ-07 | What temporal grid is used (raw acquisitions, fixed-interval composites; which interval)? | Trades noise and gaps against temporal detail; also affects in-season prediction. | H-10b | P2 | open |
| DQ-08 | Which inputs: which bands, which vegetation indices, which per-parcel statistics? | Feature choice drives baseline quality and the size of the stored data. | H-13 | P2 | open |
| DQ-09 | How does extraction run within the hardware and the 60 GB disk budget (streaming, windowing, where to run it)? | Never caching scenes is a rule; the extraction design must make it practical. | H-14 | P1 | open |

## Evaluation

| ID | Question | Why it matters | Linked hypotheses | Priority | Status |
|---|---|---|---|---|---|
| DQ-10 | How are data split so scores are honest (random, spatial blocks, held-out region, held-out year or campaign; block size)? | Spatially close fields resemble each other; random splits can inflate scores. Likely the most-asked viva question. | H-03 | P1 | open |
| DQ-11 | Which metrics are headline metrics (accuracy, macro-F1, per-class scores), and how is uncertainty in them reported (seeds, block bootstrap)? | Class imbalance makes plain accuracy misleading. | H-03 | P2 | open |
| DQ-12 | Are calibrated probabilities needed, and with which method? | The map shows confidence; Module B may use it. | H-15 | P2 | open |
| DQ-13 | Which model ladder: majority and rule baselines, gradient boosting, temporal CNN, attention models? Is a pretrained foundation model worth it? | Defines the experiments; needs to fit a 6 GB GPU or CPU-only lab PC. | H-04 | P2 | open |
| DQ-14 | Which class list and what policy for rare classes? Binary (sugarcane vs non-sugarcane), multi-class, or multi-class trained and shown as cane vs non-cane? | Depends on the dataset audit; affects every metric. The user prefers cane vs non-cane only if it makes the work easier (product spec P-2); "non-cane" is a mixed, varied class, so it may not. | H-08, H-19 | P2 | open |

## Product and later modules

| ID | Question | Why it matters | Linked hypotheses | Priority | Status |
|---|---|---|---|---|---|
| DQ-15 | Which web stack shows parcels with a date slider and popups (static tiles versus a backend)? | Simplicity versus the needs of Module B's near-real-time layer. | H-07 | P2 | open |
| DQ-16 | How are predictions exported and served (GeoParquet, PMTiles, API)? | Contract between the pipeline and the map. | H-07 | P2 | open |
| DQ-17 | How does in-season prediction work ("as of date"), and is a present-day run (demo Tier 2) feasible? | Drives the demo and shares a data path with Module B. | H-16, H-17 | P2 | open |
| DQ-18 | What does "crop health" mean operationally, which satellite signals carry health information (optical indices, red-edge, SWIR moisture, radar, thermal, weather), and how can it be validated without our own ground truth? | Health is a must-have layer (product spec P-3), and the user wants to learn the techniques. Gate B0 requires an answer. | H-06, H-21 | P2 | open |
| DQ-19 | Which choices survive the move to Pakistan (no open polygons, smallholder fields, monsoon cloud, scarce labels)? | Stage 1 exists to make Stage 2 cheaper. Asked of every other question. | all | P1 (as a lens) | open |
| DQ-20 | What repository layout, environment management and tooling should be used? | Must be settled before scaffolding (issue #7). | H-09, H-18 | P1 | open |

## Added 2026-10-27 (kit audit)

| ID | Question | Why it matters | Linked hypotheses | Priority | Status |
|---|---|---|---|---|---|
| DQ-21 | How is sugarcane's semi-perennial cycle (about a year or more per cycle, ratoon regrowth, long harvest window) handled in labels, time windows, health baselines and yield? | The kit assumes one crop per field per season (audit F-03). Sugarcane is the crop the project cares about most. | H-20 | P1 (if the chosen data contain sugarcane) | open |
| DQ-22 | What yield data exist for the candidate regions, at what level (field, farm, district or municipality), and what claim does each level support? | Decides whether P-4 is a model or a feasibility note (audit F-04; Module C). Affects the dataset choice. | H-22 | P1 | open |
| DQ-23 | How are field polygons obtained for a recent season, so the health layer can run on current imagery: reuse the labelled polygons, an annual parcel registry, or boundary extraction? | Near-real-time health and the present-day demo need current fields (audit F-02). | H-17, H-23 | P1 | open |

## Notes

- Questions will be added as research raises them. Do not delete a question; mark it answered or merged and link where.
- Order of research (revised 2026-10-27, aimed at the introductory presentation): DQ-01 with DQ-22 and DQ-23 (the dataset stack), DQ-04, then DQ-21, DQ-18 and DQ-14 at survey depth (enough to state the approach and its limits), then DQ-05, DQ-10, DQ-02, DQ-06, DQ-09, DQ-20, then the rest.
