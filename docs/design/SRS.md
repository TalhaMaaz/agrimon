---
type: requirements
status: draft
tags: [requirements, srs, phase-r]
phase: R
---

# Software Requirements Specification: AgriMon

Satellite and AI-Based Crop Monitoring and Decision-Support System for Sugarcane

| Item | Detail |
|---|---|
| Version | 0.2 (draft) |
| Date | 2026-11-10 |
| Author | Muhammad Talha Maaz (student), drafted with Claude Code |
| Supervisor | Dr. Aneela Zameer, DCIS |
| Status | Draft for supervisor review. Requirements are "proposed" until the architecture sign-off (Checkpoint R). |
| Structure | IEEE 830 / ISO/IEC/IEEE 29148 style |

## Contents

1. Introduction
2. Overall description
3. External interface requirements
4. System features (use cases and functional requirements)
5. Non-functional requirements
6. Data requirements
7. Stage 2: the Pakistan system
8. Verification and traceability
9. Open issues

Appendix A: change history

---

## 1. Introduction

### 1.1 Purpose
This document states what AgriMon must do and how well, so that the supervisor, the examiners and the developer agree on the product before it is built. It is the reference for design, testing and the thesis. It does not describe the internal design in detail; that is the architecture dossier's job.

### 1.2 Scope
AgriMon is a web-map application that shows, for each field in a study area:

- whether it is sugarcane (with a confidence value),
- how healthy it is compared with the expected growth curve for its stage in the cane cycle,
- an indicative yield, or a documented reason why yield cannot be estimated at field level.

It is built from free satellite imagery (Sentinel-2) and open field and crop data. The target system is for Pakistan. The work has two stages:

- **Stage 1 (pipeline practice):** build and prove the complete pipeline on Louisiana, USA (Iberia parish), where open field boundaries and sugarcane labels exist. Stage 1 is a proving ground: it tests the methods and the engineering on data good enough to check them, before they are applied where data is scarce.
- **Stage 2 (the real build):** build the Pakistan system, as far as the available Pakistani data allows (section 7).

Requirements in sections 3 to 6 apply to the system in both stages; their acceptance tests run first on Louisiana, where ground data exists to check them.

AgriMon is a prototype for a final-year project. It is not a commercial product, it has no user accounts, and it does not diagnose pests or diseases.

### 1.3 Definitions, acronyms and abbreviations

| Term | Meaning |
|---|---|
| CDL | USDA Cropland Data Layer: a yearly 30 m crop map of the USA, produced by a model |
| CSB | USDA Crop Sequence Boundaries: field polygons with the CDL crop for each year |
| NASS | USDA National Agricultural Statistics Service (official yield statistics) |
| Sentinel-2 | ESA satellites giving free 10 m multispectral images every few days |
| STAC | SpatioTemporal Asset Catalog, a standard way to search satellite imagery |
| Field / parcel | One agricultural field, stored as a polygon |
| Plant cane / ratoon | First crop after planting / regrowth crops after each harvest |
| Cane cycle | Plant cane followed by several ratoon crops, then replanting |
| Vegetation index | A number computed from image bands that tracks plant greenness (for example NDVI) |
| Health flag | A mark that a field departs from its expected curve and from its neighbours. It is not a diagnosis |
| Hold-out (spatial, temporal) | Test data from areas or years the model never saw in training |
| GeoParquet | A columnar file format for tables with geometry |
| FR, NFR | Functional requirement, non-functional requirement |
| TBD | To be decided; listed in section 9 |

### 1.4 References

- `docs/design/requirements_register.md`: the requirement register this SRS expands (same IDs).
- `docs/design/product_spec.md`: the Stage 1 product specification.
- `docs/research/datasets/usda_csb.md`, `docs/research/datasets/usda_cdl.md`: dataset notes and licences.
- `docs/research/dataset_catalogue.md`: candidate datasets and why the US stack was chosen.
- `docs/research/existing_systems_review.md`: existing systems.
- Mid-semester presentation (slides 9 to 11: architecture, use cases, data design).
- IEEE Std 830-1998 and ISO/IEC/IEEE 29148:2018 (structure only).

### 1.5 Overview
Section 2 gives the context and constraints. Section 3 covers interfaces. Section 4 lists the features as use cases with their functional requirements. Section 5 lists quality requirements. Section 6 defines the data. Section 7 covers Pakistan. Section 8 maps every requirement to how it will be checked. Section 9 lists what is still open.

---

## 2. Overall description

### 2.1 Product perspective
AgriMon is a new, self-contained system. It has two parts: an offline pipeline in Python that prepares the data and runs the models, and a web map in the browser that shows the results. There is no database server; results are files.

```
   EXTERNAL SOURCES                  AGRIMON                                    USERS
 +--------------------+   +-----------------------------------------------+
 | Sentinel-2 (STAC)  |-->|  OFFLINE PIPELINE (Python)                    |
 | Earth Engine (opt.)|-->|  ingestion -> per-field feature store         |
 | USDA CSB + CDL     |-->|            -> models A, B, C -> result files  |   developer
 | USDA NASS yields   |-->|                                               |<- runs, evaluates
 +--------------------+   +-----------------------+-----------------------+
                                                  | map tiles + tables
                                                  v
                          +-----------------------------------------------+
                          |  WEB MAP (browser)                            |<- mill officer /
                          |  layers, date slider, field pop-up            |   agronomist
                          +-----------------------------------------------+
```

### 2.2 Product functions (summary)

- F1. Ingest open field polygons, crop labels, satellite imagery and yield statistics for a region.
- F2. Build a cloud-masked vegetation-index time series for every field.
- F3. Classify each field per season as sugarcane or not, with confidence (Module A).
- F4. Flag fields whose growth departs from the expected cane-cycle curve (Module B).
- F5. Estimate yield, or document why it is not feasible (Module C).
- F6. Show all of this per field on an interactive web map with a date slider.
- F7. Evaluate the models honestly on held-out years and areas.

### 2.3 User classes and characteristics

| User class | Description | Technical skill | Main use cases |
|---|---|---|---|
| Mill officer / agronomist (primary) | Plans cane supply or advises farmers; reads the map | Non-specialist; no GIS or ML knowledge assumed | UC-01 to UC-06 |
| Developer (primary) | Runs the pipeline for a region and evaluates models (in the FYP, the student) | Python, GIS, ML | UC-07 to UC-09 |
| Supervisor / examiner (secondary) | Reviews results, demo and reports | Academic | Demo, reports |

Supporting actors (external systems): the Sentinel-2 catalogue and the USDA data sources.

### 2.4 Operating environment

- **Pipeline:** Python 3.12 on Ubuntu; runs on a laptop (RTX 3060 6 GB, 16 GB RAM), a lab PC (large RAM, no GPU), or Colab / Kaggle.
- **Web map:** a current desktop browser (Chrome, Firefox or Edge). Mobile is not a target.
- **Network:** internet access is needed to fetch imagery; the web map can be served locally for the demo.

### 2.5 Design and implementation constraints

- C-1. Open, free data only; each dataset's licence recorded before use.
- C-2. Earth Engine is used only under its noncommercial terms, for university work, and only behind an interface so it can be replaced by the open STAC catalogue.
- C-3. Never store whole satellite scenes; stream imagery and keep per-field features.
- C-4. Must run on the hardware in 2.4.
- C-5. Reproducible: pinned environment, configuration files, fixed seeds, versioned data manifests.
- C-6. Git workflow: issue, branch, pull request, automatic checks; no direct pushes to `main`.
- C-7. No credentials, data, rasters or model weights in the repository.
- C-8. Proposed stack (confirmed with evidence before building): geopandas, rasterio, xarray; Planetary Computer STAC; GeoParquet + DuckDB; LightGBM, then TempCNN and attention models in PyTorch; MapLibre GL JS + PMTiles.

### 2.6 User documentation

- A short user guide for the web map (layers, legend, what a health flag means and does not mean).
- A developer README: setup, configuration, running the pipeline, reproducing results.
- The thesis and experiment reports.

### 2.7 Assumptions and dependencies

- A-1. CSB polygons and CDL labels are accurate enough to train and test on. CDL is model-derived, not ground truth; its published sugarcane accuracy for Louisiana is about 94 to 95 % producer's and 96 % user's accuracy (spike S02).
- A-2. Field boundaries for the newest season are assumed unchanged from the latest CSB edition (DQ-23).
- A-3. Enough cloud-free Sentinel-2 observations exist per field per season. Radar (Sentinel-1) is a fallback if not.
- A-4. NASS yield statistics exist at state level (confirmed) and possibly parish level (still being checked).
- A-5. The Planetary Computer STAC catalogue stays free and available during the FYP.
- A-6. Stage 2 depends on what Pakistani data can be obtained (SUPARCO has been contacted).

---

## 3. External interface requirements

### 3.1 User interface
One screen: a map with a left panel and a field panel. Wireframe (illustrative):

```
 +------------------------------------------------------------------------------+
 | AgriMon . Iberia parish, Louisiana                                           |
 +--------------+-----------------------------------------+---------------------+
 | Layer        |                                         | Selected field      |
 | (o) Crop     |        field polygons coloured          | Sugarcane, ratoon 2 |
 | ( ) Health   |        by the chosen layer              | Confidence: high    |
 | ( ) Yield    |                                         | Below expected      |
 | Date         |                                         | since May           |
 | [----o----]  |                                         | [health chart]      |
 | Legend       |                                         | Yield vs NASS       |
 +--------------+-----------------------------------------+---------------------+
```

- UI-1. Pan, zoom and click on fields.
- UI-2. A layer selector (crop type, health, yield).
- UI-3. A date or season slider; the data date is always shown.
- UI-4. A legend for every layer, using a colour-blind-safe palette and words, not colour alone.
- UI-5. A field panel with crop, confidence, health status, health chart (field curve against expected range) and yield.
- UI-6. Plain-language labels; "health flag" is explained as "behaving differently from expected", not as a diagnosis.

### 3.2 Hardware interfaces
None beyond a standard computer. GPU use is optional for training (NFR R-N-03).

### 3.3 Software interfaces

| ID | Interface | Direction | Notes |
|---|---|---|---|
| SI-1 | Sentinel-2 L2A via a STAC API (Planetary Computer) | in | Search by area and date; read only the pixels inside fields |
| SI-2 | Google Earth Engine | in (optional) | Noncommercial only; behind the same ingestion interface as SI-1 |
| SI-3 | USDA CSB files | in | Downloaded once; field polygons and yearly CDL crop codes |
| SI-4 | USDA CDL | in | Crop labels and accuracy metadata |
| SI-5 | USDA NASS statistics | in | Official yields per state, and per parish where available |
| SI-6 | Result files (GeoParquet, PMTiles) | out | Read by the web map |

### 3.4 Communications interfaces
HTTPS to the data sources above. The web map reads static files over HTTP; there is no backend API in Stage 1.

---

## 4. System features

Use-case diagram (slide 10 of the mid-semester deck), in text:

```
 Mill officer / agronomist --- UC-01 View field map <--<<extend>>-- UC-02 Select a date
                           \-- UC-03 View field details --<<include>>--> UC-04 View crop type and confidence
                                                       \--<<include>>--> UC-05 View health history
                                                       <--<<extend>>---- UC-06 View indicative yield
 Developer ----------------+-- UC-07 Run pipeline for a region --<<include>>--> UC-08 Ingest open data
                           \-- UC-09 Evaluate models                              |
                                                     Sentinel-2 catalogue, USDA data sources
```

Each feature below lists its use cases and functional requirements. Priority: must, should, could. IDs match the requirements register.

### 4.1 Field map (P-1)
**UC-01 View field map.** Actor: mill officer / agronomist. The user opens the map; the study area's fields are drawn as polygons coloured by the chosen layer. Extended by UC-02.

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| R-F-01 | Show field polygons for the study area on an interactive map (pan, zoom, click) | must | Polygons for the study parish render and a click shows attributes |
| R-F-09 | Pick a date or season on the map (time slider) | should | Changing the date recolours fields |

**UC-02 Select a date** (extends UC-01): the user moves the slider; the map shows that date's layer and the data date.

### 4.2 Crop type (P-2, Module A)
**UC-03 View field details** and **UC-04 View crop type and confidence** (included). The user clicks a field; the panel shows whether it is sugarcane and how confident the model is.

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| R-F-02 | Classify each field per season as sugarcane or non-sugarcane, with a confidence value | must | Predictions exist for every field in the test set; metrics reported on held-out data; target set after baseline |
| R-F-03 | Show the crop layer with a legend and a filter for low-confidence fields | should | The map toggles low-confidence fields |

### 4.3 Field health (P-3, Module B)
**UC-05 View health history** (included in UC-03): the panel shows the field's vegetation-index curve against the expected range for its cane-cycle stage, and when it started to depart.

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| R-F-04 | Compute per-field vegetation indices over time from Sentinel-2, with clouds masked | must | A time series per field, with cloudy observations removed and flagged |
| R-F-05 | Flag a field when its index departs from the expected curve for its cane-cycle stage and from its neighbours | must | Flags are produced; evaluated on at least one documented event |
| R-F-06 | Show a field's health history (time-series chart) in the map pop-up | must | Clicking a field shows its curve and its expected range |
| R-F-07 | Update the health layer when new imagery arrives (near real time), with the data date shown | should | A run on recent imagery updates the layer; the latency is measured and reported |

### 4.4 Yield (P-4, Module C)
**UC-06 View indicative yield** (extends UC-03): where a yield estimate exists, the panel shows it next to the official statistic.

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| R-F-08 | Estimate yield per field or parish, or document why it is not feasible | could | A model compared with NASS statistics, or a feasibility note |

### 4.5 Pipeline and evaluation (developer)
**UC-07 Run pipeline for a region**, including **UC-08 Ingest open data** from the supporting actors. **UC-09 Evaluate models** on held-out data and produce a report.

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| R-F-10 | Load a new region through the same pipeline steps (configuration, not code changes) | should | A second parish runs by changing configuration only |
| R-F-11 (new, proposed) | Produce an evaluation report per model with metrics on spatial and temporal hold-outs | must | The report names the split, the metrics and their spread (links to R-N-02) |
| R-F-12 (new, proposed) | Resume a long pipeline run after an interruption without redoing finished chunks | should | Killing and restarting a run finishes with the same output |

R-F-11 and R-F-12 are new in this SRS (they come from objective O2 and constraint C-3) and still need the student's approval before they enter the register.

---

## 5. Non-functional requirements

| ID | Category | Requirement | Priority | Acceptance criterion |
|---|---|---|---|---|
| R-N-01 | Reproducibility | Pinned environment, configuration files, fixed random seeds, versioned data manifests | must | Re-running an experiment gives the same metrics |
| R-N-02 | Evaluation quality | Spatial and temporal hold-outs; uncertainty reported | must | Each reported metric names its split and its spread |
| R-N-03 | Portability / resources | Runs on project hardware (laptop, lab PC, Colab or Kaggle) | must | The full pipeline for one parish completes on the laptop |
| R-N-04 | Storage | Stream imagery and store per-field features, never whole scenes | must | No scene files in the data folders |
| R-N-05 | Usability | A non-specialist can read the map (legend, units, colour-blind-safe palette, plain-language pop-ups) | should | Review by the supervisor or a test user |
| R-N-06 | Traceability | Every result traces to data version, code version and configuration | must | Each experiment record has a commit hash and data hash |
| R-N-07 | Legal | Only data whose licence allows thesis use; licences recorded | must | Each dataset note lists its licence |
| R-N-08 | Security | No credentials or tokens in the repository; secrets only in local `.env` files | must | CI secret scan and commit hooks pass |
| R-N-09 | Performance | Map interactions stay responsive for one parish (about 5,600 fields) | should | Target set when the web stack is chosen |
| R-N-10 | Maintainability | Code tested (pytest), linted (ruff), documented | should | CI green |

Numeric targets (accuracy, latency, response time) are deliberately not invented here. They are set after the first baselines and recorded in section 9.

---

## 6. Data requirements

### 6.1 Data sources and licences

| Source | Use | Licence (as recorded) |
|---|---|---|
| USDA NASS CSB 2018-2025 | Field polygons, yearly crop per field | "considered public domain and free to redistribute" (metadata file in the download) |
| USDA NASS CDL | Crop labels and accuracy | "considered public domain and free to redistribute" (metadata file in the download) |
| Sentinel-2 L2A (Copernicus) | Imagery for indices | TBD: to be recorded in a dataset note before use |
| USDA NASS yield statistics | Yield comparison | TBD: to be recorded in a dataset note before use |
| Google Earth Engine (optional) | Alternative imagery access | Noncommercial terms, university work only |

### 6.2 Logical data model
Entity-relationship diagram (slide 11 of the deck; crow's foot in the slide, text here). This is a proposed logical design, stored as GeoParquet files joined on keys; it is not a database schema yet.

```
 CROP_LABEL >|------|| FIELD ||------|< REGION ... (many fields in one region)
                        ||                 ||
                        |o<                |o<
              INDEX_OBSERVATION         YIELD_STATISTIC
                        ^
 FIELD ||------o< PREDICTION
```

| Entity | Key | Attributes | Relationship |
|---|---|---|---|
| FIELD | field_id (PK) | region_id (FK), geometry (polygon), area_acres | Belongs to one REGION |
| CROP_LABEL | field_id + year (PK) | crop_code (CDL code) | One or more per FIELD |
| INDEX_OBSERVATION | field_id + obs_date + index_name (PK) | value, cloud_flag | Zero or more per FIELD |
| PREDICTION | field_id + pred_date (PK) | crop_class, confidence, health_flag, est_yield | Zero or more per FIELD |
| REGION | region_id (PK) | name, level (parish or state) | Has many FIELDs |
| YIELD_STATISTIC | region_id + year (PK) | official_yield | Zero or more per REGION |

### 6.3 Data quality requirements

- DQ-R1. Every field kept for training has a crop label for the season used, and a pass rule is written before the data is checked (as in spikes S01 and S02).
- DQ-R2. Cloudy observations are removed and flagged, not silently dropped.
- DQ-R3. Every dataset has a manifest (source, version, date fetched, licence, checksum).

---

## 7. Stage 2: the Pakistan system

Stage 2 is the real build: the system for Pakistani sugarcane. Stage 1 exists so that this stage starts from a pipeline that is already proven and tested.

**What carries over from Stage 1:** the pipeline, the per-field feature store, the models' interfaces and the web map. R-F-10 (new region by configuration) is the requirement that makes this possible.

**What changes, and what is unknown:**

| Topic | Stage 1 (Louisiana) | Stage 2 (Pakistan) | Status |
|---|---|---|---|
| Field boundaries | CSB polygons | SUPARCO data if available; otherwise boundaries drawn from satellite images | SUPARCO contacted; outcome pending |
| Crop labels | CDL, 18 seasons with sugarcane | Whatever labelled data exists | TBD |
| Clouds | Moderate | Monsoon cloud; radar more likely needed | Risk |
| Field size | Median cane field about 4.65 ha | Smaller smallholder fields | Risk to 10 m pixels |
| Yield data | NASS state (and maybe parish) | District statistics, if available | TBD |

**Stage 2 requirements (proposed, to be refined when the data is known):**

- R-F-S2-01. Run the pipeline on a Pakistani study area using the same configuration mechanism (must).
- R-F-S2-02. If no field boundaries are available, produce field polygons from satellite images for a test area and report their quality (could).
- R-F-S2-03. Report how the Stage 1 models perform on Pakistani data, and what retraining was needed (must).
- R-F-S2-04. Show the Pakistani study area on the web map with every layer the available data supports, and state plainly which layers are missing and why (must).

---

## 8. Verification and traceability

Verification methods: T = test, E = experiment, D = demo, R = review.

| Objective | Requirements | Use cases | Verified by |
|---|---|---|---|
| O1 Pipeline | R-F-04, R-F-10, R-F-12, R-N-01, R-N-03, R-N-04, R-N-06 | UC-07, UC-08 | T, D |
| O2 Crop type | R-F-02, R-F-03, R-F-11, R-N-02 | UC-04, UC-09 | E |
| O3 Health | R-F-04 to R-F-07 | UC-05 | E, D |
| O4 Yield | R-F-08 | UC-06 | E, R |
| O5 Web map | R-F-01, R-F-06, R-F-09, R-N-05, R-N-09 | UC-01 to UC-03 | D, T |
| Stage 2 Pakistan system | R-F-S2-01 to R-F-S2-04, R-F-10 | UC-01 to UC-08 on Pakistani data | D, E |
| All | R-N-07, R-N-08, R-N-10 | | R, T |

---

## 9. Open issues (TBD)

| # | Issue | Decided when |
|---|---|---|
| 1 | Accuracy target for R-F-02 | After the Module A baseline |
| 2 | How health flags are scored for R-F-05 (which events, which metric) | Module B design |
| 3 | Response-time target for R-N-09 | When the web stack is chosen |
| 4 | Yield as a model or a feasibility note (R-F-08) | After parish-level NASS data is checked |
| 5 | Binary or multi-class crop model (DQ-14) | Phase R, with evidence |
| 6 | Licences for Sentinel-2 and NASS statistics recorded in dataset notes | Before first use |
| 7 | Whether R-F-11 and R-F-12 join the register | Student's review of this draft |
| 8 | Stage 2 data (SUPARCO) | When SUPARCO replies |

---

## Appendix A: change history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-10 | First draft from the requirements register, product spec and mid-semester deck |
| 0.2 | 2026-11-10 | Reframed: Louisiana is pipeline practice (Stage 1); Pakistan is the real build (Stage 2). Stage 2 requirements raised to must where the data allows; R-F-S2-04 added |
