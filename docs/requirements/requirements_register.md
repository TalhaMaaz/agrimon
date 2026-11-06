---
type: requirements
status: draft
tags: [requirements, phase-r, presentation]
phase: R
---

# Requirements register (draft, 2026-11-06)

Derived from the [Stage 1 product spec](../architecture/product_spec.md) (P-1 to P-4). Format from `docs/agent/DOCUMENTATION_PROTOCOL.md`.
- **Priority:** must, should or could.
- **Verification:** T = test, E = experiment, D = demo, R = review.
- **Numbers:** numeric performance targets are agreed after baselines exist, so they are written as "target set after baseline" rather than invented.
- **Status** is "proposed" until Checkpoint R.

## 1. Aim and objectives (slide 4)

**Aim:** build and evaluate a web-map application that shows, for each sugarcane-area field, its crop type, its health over time and an indicative yield. Develop it on open US data (Louisiana) and design it to be adapted to Pakistan.

| # | Objective | Evidence it is met |
|---|---|---|
| O1 | Build a reproducible pipeline that turns open field polygons, labels and Sentinel-2 imagery into per-field time series | Pipeline runs end to end from a clean checkout (T, D) |
| O2 | Classify fields as sugarcane or non-sugarcane and evaluate honestly (held-out years and areas) | Experiment report with a spatial and temporal split (E) |
| O3 | Monitor field health against the expected sugarcane-cycle curve, and validate on documented stress events | Event case studies (hurricane, freeze) (E) |
| O4 | Assess field- or parish-level yield estimation, as a model or a documented feasibility study | Report comparing against NASS statistics (E, R) |
| O5 | Deliver an interactive web map that shows these layers per field | Demo with replay of held-out data (D) |

## 2. Functional requirements

| ID | Requirement | Priority | Acceptance criterion | Verify | Product |
|---|---|---|---|---|---|
| R-F-01 | Show field polygons for the study area on an interactive map (pan, zoom, click) | must | Polygons for the study parish render and a click shows attributes | D, T | P-1 |
| R-F-02 | Classify each field per season as sugarcane or non-sugarcane, with a confidence value | must | Predictions exist for every field in the test set; metrics reported on held-out data; target set after baseline | E | P-2 |
| R-F-03 | Show the crop layer with a legend and a filter for low-confidence fields | should | The map toggles low-confidence fields | D | P-2 |
| R-F-04 | Compute per-field vegetation indices over time from Sentinel-2, with clouds masked | must | A time series per field, with cloudy observations removed and flagged | T, E | P-3 |
| R-F-05 | Flag a field when its index departs from the expected curve for its cane-cycle stage and from its neighbours | must | Flags are produced; evaluated on at least one documented event | E | P-3 |
| R-F-06 | Show a field's health history (time-series chart) in the map pop-up | must | Clicking a field shows its curve and its expected range | D | P-3 |
| R-F-07 | Update the health layer when new imagery arrives (near real time), with the data date shown | should | A run on recent imagery updates the layer; the latency is measured and reported | D, E | P-3 |
| R-F-08 | Estimate yield per field or parish, or document why it is not feasible | could | A model compared with NASS statistics, or a feasibility note | E, R | P-4 |
| R-F-09 | Pick a date or season on the map (time slider) | should | Changing the date recolours fields | D | P-1..P-3 |
| R-F-10 | Load a new region through the same pipeline steps (configuration, not code changes) | should | A second parish runs by changing configuration only | T | Stage 2 |

## 3. Non-functional requirements

| ID | Requirement | Priority | Acceptance criterion | Verify |
|---|---|---|---|---|
| R-N-01 | **Reproducibility:** pinned environment, configuration files, fixed random seeds, versioned data manifests | must | Re-running an experiment gives the same metrics | T |
| R-N-02 | **Honest evaluation:** spatial and temporal hold-outs; uncertainty reported | must | Each reported metric names its split and its spread | R |
| R-N-03 | **Runs on project hardware:** laptop (RTX 3060 6 GB, 16 GB RAM), lab PC, Colab or Kaggle | must | The full pipeline for one parish completes on the laptop | T |
| R-N-04 | **Storage discipline:** stream imagery and store per-field features, never whole scenes | must | No scene files in the data folders | R |
| R-N-05 | **Usability:** a non-specialist can read the map (legend, units, colour-blind-safe palette, plain-language pop-ups) | should | Review by the supervisor or a test user | R, D |
| R-N-06 | **Transparency:** every result traces to data version, code version and configuration | must | Each experiment record has a commit hash and data hash | R |
| R-N-07 | **Licensing:** only data and imagery whose licence allows thesis use; licences recorded | must | Each dataset note lists its licence | R |
| R-N-08 | **Security:** no credentials or tokens in the repository; secrets only in local `.env` files | must | CI secret scan and commit hooks pass | T |
| R-N-09 | **Performance:** map interactions stay responsive for one parish (about 5,600 fields) | should | Target set when the web stack is chosen | T |
| R-N-10 | **Maintainability:** code tested (pytest), linted (ruff), documented | should | CI green | T |

## 4. Limitations and boundaries (what is NOT included)

- **Not disease or pest diagnosis.** Health means departure from expected growth; the cause needs field checking.
- **No ground truth of our own.** Labels are model-derived (CDL); this is stated with its accuracy (S01, S02).
- **No field-level yield validation.** Only parish or state statistics exist.
- **Not a commercial product.** Earth Engine is used under noncommercial terms and is optional behind an interface.
- **Not region-wide field segmentation.** Field polygons come from CSB in Stage 1. Pakistan field boundaries are a Stage 2 question.
- **Only one study region in depth** (Louisiana: Iberia, plus possibly a second, more mixed parish). Pakistan is adapted at the end, with whatever data exists.
- **Not a mobile app,** and no user accounts.

## 5. Open points

- Targets for R-F-02, R-F-05 and R-N-09 are set after baselines (Checkpoint R and Module A).
- Whether R-F-08 is a model or a note depends on S04 (parish yields) and DQ-22.
