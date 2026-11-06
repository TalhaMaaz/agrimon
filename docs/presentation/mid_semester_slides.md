---
type: presentation
status: draft
tags: [presentation, mid-semester, slides]
phase: R
date: 2026-11-06
---

# Mid-semester presentation: slide notes

Rules from the guidelines (`Presentations/FYP Presentation Instructions (Mid-Semester-7).pdf`):
- **10–12 slides, strictly 10 minutes.** Plan about 50 seconds per slide.
- **Bring the weekly attendance or progress sheet.** The slides must match it.
- **Separate completed work from planned work clearly.** The guidelines mark this in red.

How to read each slide below:
- **On the slide:** short text to put on the slide.
- **Say:** speaker notes. Don't put these on the slide.
- **Visual:** the figure or diagram to use. Figures are in `docs/research/spikes/figures/`.
- **Status:** `[READY]` means you can build it now. `[NEEDS WORK]` means something is still missing; the current content is still given.

| # | Slide | Guideline section | Status |
|---|---|---|---|
| 1 | Introduction | 1 | READY (your full name to add) |
| 2 | Background and motivation | 2 | READY |
| 3 | Problem statement | 3 | NEEDS WORK (confirm the mill and agronomist claim) |
| 4 | Aim, objectives and scope | 4 | READY |
| 5 | Existing systems | 5 | READY |
| 6 | Literature and the gap | 5 | NEEDS WORK (papers still to read) |
| 7 | Proposed solution and methodology | 6 | READY |
| 8 | Architecture and use cases | 6 | READY |
| 9 | Technologies and tools | 7 | READY (marked "proposed") |
| 10 | Initial progress | 8 | NEEDS WORK (supervisor meetings; Earth Engine project) |
| 11 | Timeline and future plan | 9 | NEEDS WORK (your dates) |
| 12 | Thank you and questions | – | READY |

---

## Slide 1: Project introduction `[READY]`

**On the slide**
- **Title:** Satellite and AI-Based Crop Monitoring and Decision-Support System for Sugarcane (working name: AgriMon)
- **Student:** Talha (*add your full name and registration number*). Solo project.
- **Supervisor:** Dr. Aneela Zameer Jaafery, DCIS
- **Domain:** machine learning and geospatial data science (agritech)
- **Overview, in one line:** a web map that shows, for each field, whether it is sugarcane, how healthy it is over time and an indicative yield, built from free satellite data.

**Say** (about 30 s): "My project uses free satellite images and machine learning to monitor sugarcane field by field. I build and test it first where open data is rich, in Louisiana, USA, and then adapt it to Pakistan."

**Visual:** one S01 map as a background or side image: `S01_iberia_crop2023.png`.

The title, supervisor and domain are from your Form 1A.

---

## Slide 2: Background and motivation `[READY]`

**On the slide**
- **What:** satellites (Sentinel-2, free, every few days at 10 m) can see crop type and plant condition.
- **Why sugarcane:** Pakistan, 2025-26 (provisional):
  - **1.22 million ha**, **89.45 million tonnes**, **73,200 kg/ha**;
  - **0.8 % of GDP** and **3.2 % of agricultural value addition**;
  - raw material for the **2nd largest agro-based industry**, sugar.
- **Why me:** direct field experience with sugarcane farmers in Rahim Yar Khan, and a link with an agritech venture interested in this kind of tool for sugar mills.
- **Who benefits:** sugar mills (cane supply planning), agronomists and extension staff, and farmers.

**Say:** "Sugarcane is a big crop in Pakistan, and mills depend on knowing what is growing where and in what condition. Satellite data that could tell them this is free, but it doesn't reach them as field-level information."

**Visual:** a small infographic of the four numbers.

**Source:** Pakistan Economic Survey 2025-26, Chapter 2 (finance.gov.pk). Write "provisional" next to the 2025-26 figures.

---

## Slide 3: Problem statement `[NEEDS WORK]`

**Needs:** your confirmation of the claim about what mills and agronomists lack. It rests on your Rahim Yar Khan experience and the startup contact; no source states it directly.

**On the slide (draft)**
> Pakistan grows sugarcane on 1.22 million ha, yet available satellite-based information is mainly **aggregate statistics for government** or **pixel maps** with no field view. A mill or agronomist has **no openly available tool** that shows, per field, where cane is, how healthy it is against the expected cane cycle, and what it may yield.

- **Why the problem exists:**
  - field-level labelled data is scarce in Pakistan;
  - sugarcane is semi-perennial (plant cane, then ratoons), so tools built for yearly crops don't fit;
  - clouds during the monsoon.
- **Who is affected:** sugar mills, agronomists, farmers.
- **Why existing solutions fall short:**
  - SUPARCO produces statistics for government;
  - commercial platforms we checked don't mention sugarcane on their product pages;
  - the best global sugarcane map finds only **43 %** of Pakistani cane in point validation (recall 0.43, F1 0.6; Di Tommaso et al. 2024).

**Say:** keep it to one specific problem: "no field-level, sugarcane-aware view". Don't describe the whole field of agritech (the guidelines warn against this).

**Visual:** three boxes: what exists (district statistics, pixel maps, generic platforms) → the gap → what's needed (a per-field, sugarcane-aware map).

---

## Slide 4: Aim, objectives and scope `[READY]`

**On the slide**
- **Aim:** build and evaluate a web-map application that shows each field's crop type, health over time and indicative yield. Develop it on open US data, designed to be adapted to Pakistan.
- **Objectives:**
  1. A reproducible pipeline from open field polygons, labels and Sentinel-2 to per-field time series.
  2. Classify fields as sugarcane or non-sugarcane, evaluated on held-out years and areas.
  3. Monitor field health against the expected cane-cycle curve; validate on documented events (hurricanes, freezes).
  4. Assess yield estimation against official statistics (a model, or a documented feasibility study).
  5. An interactive web map showing these layers per field.
- **Functional requirements (main ones):**
  - show field polygons;
  - a crop label with a confidence value;
  - a health flag and a history chart per field;
  - a date slider;
  - an indicative yield.
- **Non-functional requirements:**
  - reproducible (pinned environment, seeds);
  - honest evaluation (spatial and temporal hold-outs);
  - runs on student hardware (6 GB GPU, 16 GB RAM);
  - usable by non-specialists;
  - no secrets in the code;
  - licences recorded.
- **Not included:**
  - pest or disease **diagnosis** (we flag unusual fields, we don't name the cause);
  - our own ground survey;
  - field-level yield validation;
  - a mobile app;
  - a commercial product.

**Say:** "Health here means 'this field is behaving differently from what's expected'. The cause still needs someone in the field."

**Source:** `docs/requirements/requirements_register.md` (R-F-01 to R-F-10, R-N-01 to R-N-10). If the board asks for accuracy targets: they are set after the first baselines, not guessed now.

---

## Slide 5: Literature review, existing systems `[READY]`

**On the slide:** comparison table.

| System | Type | Field level | Sugarcane | Health | Yield |
|---|---|---|---|---|---|
| SUPARCO crop monitoring | Government statistics (since 2005) | crop layers; field-level support still a project (since 2020) | yes | NDVI reporting | forecasts |
| EOSDA Crop Monitoring | Commercial | user draws fields | not mentioned | yes, plus alerts | yes |
| OneSoil | Commercial | field boundaries map | not mentioned | yes | not stated |
| Cropin | Commercial (enterprise) | not mentioned | not mentioned | yes | yes |
| Di Tommaso et al. 2024 | Research, 10 m global map | no (pixels) | yes | no | no |
| **AgriMon (proposed)** | FYP prototype | **yes** | **yes, cycle-aware** | **yes** | **parish level** |

**Say:**
- "SUPARCO's pilot in 2005 actually covered Rahim Yar Khan, Bahawalpur and Ghotki for wheat, cotton and sugarcane. Its outputs are statistics for government."
- For the vendors, say "their product pages don't mention sugarcane", not "they can't do it". The vendor rows are based only on their marketing pages.

**Sources:** `docs/research/existing_systems_review.md`. The SUPARCO row is from Akhtar, PIDE Discourse 2024.

---

## Slide 6: Literature and the research gap `[NEEDS WORK]`

**Needs:**
- read the Punjab 2024 paper, the 2021 sugarcane review, Hu 2022 and Weiss 2020 (you're downloading these);
- I read Pelletier 2019 and Garnot 2020 (free on arXiv);
- **find 1–2 crop-health papers** (currently a gap).

**On the slide (current content)**

| Topic | Key work | What it shows | Limit for our purpose |
|---|---|---|---|
| Sugarcane mapping | Di Tommaso et al. 2024 (ESSD) | 10 m sugarcane maps, 13 countries, 2019–22 | pixels only; Pakistan recall 0.43 |
| Sugarcane in Punjab | Sentinel-2 deep learning paper, 2024 (RS Applications: Society and Environment, article 101225) | CNN and LSTM on 10 dates × 12 bands + 6 indices; labels from spectral unmixing | pixel level; *abstract only so far* |
| Sugarcane yield | Hu et al. 2022 (Remote Sensing) | regional yield, Florida and Louisiana, from MODIS and weather; SiPAR best | regional, coarse; *abstract only so far* |
| Crop-type models | Pelletier 2019 (TempCNN); Garnot 2020 (attention) | time-series models for crops | *to read* |
| Crop health | *to find* | | |

- **The gap:** the pieces exist separately. We found no openly documented system that combines **field polygons, sugarcane classification, cane-cycle-aware health monitoring and yield** in one pipeline designed to transfer to Pakistan.
- **How AgriMon differs:**
  - per field, not per pixel or per district;
  - follows the sugarcane cycle (S01 shows it in real data);
  - built and validated where open data is rich, then adapted to Pakistan;
  - open and reproducible.

**Say:** "This is what we found; it doesn't prove nothing else exists. Our search is logged with dates and queries." (`docs/research/search_log.md`)

**Don't claim:** better accuracy than anyone. We haven't measured any yet.

---

## Slide 7: Proposed solution and methodology `[READY]`

**On the slide**
- **Two stages:**
  - Stage 1: build the full system on open US data (Louisiana), where field boundaries and sugarcane labels exist.
  - Stage 2: adapt it to Pakistan with the data available there.
- **Development methodology:** iterative and incremental, phase-gated (an Agile style for one developer):

  ```
  Research ─> Module A ─> Module B ─> Module C ─> Pakistan
  (spikes)    crop type   health      yield       adaptation
     each phase: plan (Phase Brief) → approve → build in small tasks → review → checkpoint
  ```

- **Why not Waterfall:** the data and the methods are uncertain. Small experiments settle each design question first, and our first data experiment (S01) already changed the plan.
- **Workflow:** fields and labels plus Sentinel-2 → per-field time series → classify → health flag → yield → web map.

**Visual:** the workflow diagram from `docs/architecture/presentation_diagrams.md` section 2, redrawn as boxes and arrows.

**Say:** "Every change goes through GitHub: an issue, a branch, a pull request and automatic checks. So the history of the project is reviewable."

---

## Slide 8: Architecture and use cases `[READY]`

**On the slide**
- **Left: expected architecture.**
  - ingestion (Sentinel-2 catalogue; Earth Engine optional) → per-field feature store (GeoParquet) → models (A crop type, B health, C yield) → per-field exports → web map;
  - configuration, tests and CI around everything.
- **Right: use-case diagram.**
  - **Agronomist or mill officer:** view fields; see crop type (with low-confidence filter); see a field's health and history; pick a date; see indicative yield.
  - **Developer:** run the pipeline for a region; evaluate models.
  - **External systems:** Sentinel-2 catalogue, Earth Engine, USDA NASS data.

**Visual:**
- both diagrams from `presentation_diagrams.md` sections 3 and 4, redrawn;
- optionally a small **wireframe** of the map screen (from `docs/architecture/product_spec.md` section 1): map, layer toggles, date selector, field pop-up.

**ERD:** a database server isn't planned. If asked, show the per-field table instead:
- field id, geometry, crop label per year (from CSB);
- time series of indices per date;
- prediction, confidence, health flag.

---

## Slide 9: Technologies and tools `[READY]`

**On the slide** (title: "Proposed stack")

| Layer | Choice | Why |
|---|---|---|
| Backend and data | Python 3.12, geopandas, rasterio, xarray | standard geospatial stack; already in use |
| Imagery | Microsoft Planetary Computer (STAC), Sentinel-2 L2A; Google Earth Engine optional | free, open catalogue; Earth Engine for bulk extraction under noncommercial terms |
| Storage | GeoParquet files + DuckDB | per-field tables are small; no server to maintain; reproducible |
| AI/ML | LightGBM baseline → TempCNN / attention models (PyTorch) | the standard model ladder in crop-classification literature; fits a 6 GB GPU |
| Frontend | MapLibre GL JS + PMTiles | open-source web maps, no API key, no backend |
| Tools | Git and GitHub (issues, PRs, CI), conda-forge, Jupyter, VS Code, Obsidian, Claude Code | reviewable history, pinned environment, documented learning |

**Say:**
- "These are proposals. Each will be confirmed with evidence before building."
- **On the database:** "We use files instead of a database server because the data is per-field tables, which are small, and files make results reproducible." Be ready to defend this.
- **On Earth Engine:** "It's behind an interface, because its free tier is noncommercial."

---

## Slide 10: Initial progress `[NEEDS WORK]`

**Needs:**
- the supervisor meetings and the feedback you received (only you know these);
- the Earth Engine project ID, so the connection is fully working before you present;
- check every line against your attendance sheet.

**On the slide: two columns.**

**Completed**
- **Project environment setup:**
  - GitHub repository with CI, protected main branch and commit checks;
  - pinned Python environment (conda-forge; GDAL, geopandas, rasterio).
- **Research agent setup:** AI-assisted research and review workflow (dataset scout, reviewer, examiner agents; literature-review command), with every source logged.
- **Requirements gathering:** product spec, aim, objectives, functional and non-functional requirements.
- **Literature review, first round:** existing-systems comparison; search log.
- **Datasets selected:**
  - USDA Crop Sequence Boundaries (CSB) for fields, and the Cropland Data Layer (CDL) for crop labels, both public domain;
  - Sentinel-2 for imagery.
  - Chosen against three alternatives (Brazil-Crop, La Réunion, EuroCrops).
- **Dataset exploration:**
  - **S01:** Louisiana has 206,389 fields. Iberia parish has 5,632, of which 4,213 were sugarcane in 2023. The median cane field is 4.65 ha (about 465 Sentinel-2 pixels). The multi-year cane cycle is visible in the data.
  - **S02:** a typical cane field is 94.9 % cane pixels, and 100 % one pixel in from the edge. 87.3 % of cane pixels fall inside the field polygons.
  - **Label accuracy check:** USDA's sugarcane accuracy in Louisiana, 2023, is 95.0 % producer's and 96.4 % user's.

**In progress or planned**
- **Cloud and Python Earth Engine setup:** the Python package is installed and the login is done; the project link is pending. *Update this when done.*
- Sentinel-2 access and cloud cover (S03); yield statistics per parish (S04).
- Literature review, second round (papers listed on slide 6).

**Visual:** `S02_cdl_vs_csb.png` (zoom panel) and `S01_iberia_cane_sequences.png`. These are your strongest "real work" images.

**Say:** "Before building any model, I tested whether the data is good enough. Every check had a pass rule written before looking at the data."

---

## Slide 11: Timeline and future plan `[NEEDS WORK]`

**Needs:** your semester dates for the Gantt chart. I've left them out, as you asked. The order and the dependencies below are fixed; put the dates on the bars.

**On the slide**

| Period | Work | Deliverable |
|---|---|---|
| **Semester 7: done** | environment, repository, dataset search and selection, S01, S02, literature round 1 | spike reports, requirements |
| **Semester 7: remaining** | S03 Sentinel-2, S04 yield statistics, literature round 2, architecture approval (Checkpoint R), Module A baselines started | architecture document, first classification results |
| **Semester 8** | Module A (crop type), Module B (health), Module C (yield or feasibility), web map; then Pakistan adaptation (Stage 2); testing, thesis, defence | working prototype, thesis |

**Gantt chart:** one bar per row above. Module B depends on A; the web map runs alongside A and B; Stage 2 comes last.

**Risks and challenges**

| Risk | Mitigation |
|---|---|
| Labels come from a model (CDL), partly made from Sentinel-2 itself (circularity) | state it openly; test on held-out years and areas; compare with an independent sugarcane map |
| Cloud cover gaps the imagery | cloud masking; consider Sentinel-1 radar (decided by S03) |
| Pakistan lacks open field polygons and labels | the pipeline is designed so the data source is swappable; Stage 2 scope is set by what exists |
| Yield data only at parish or state level | yield is a model only if the data allows, otherwise a feasibility study |
| Student hardware (6 GB GPU) | simple models first; Colab or Kaggle for heavier training |
| Earth Engine is noncommercial | kept optional behind an interface; Planetary Computer is the default |
| Solo project, broad scope | phase gates; health (B) prioritised over yield (C) |

---

## Slide 12: Thank you and questions `[READY]`

**On the slide:** "Thank you. Questions?" plus the repository link, if you want to show it.

**Prepare for likely questions** (I can drill you with `/viva-drill`):
1. Why the US and not Pakistan first?
2. Your labels come from a model; how do you know they're right?
3. How is this different from SUPARCO or EOSDA?
4. What does "health" mean if you can't diagnose disease?
5. Why no database?
6. Why does the plan differ from your Form 1A? (You said you'll handle this one.)

---

## Before presenting: checklist

- [ ] Every progress item matches the attendance sheet
- [ ] Earth Engine project linked, so slide 10 can say "done"
- [ ] Slide 3 problem claim confirmed by you
- [ ] Slide 6 updated after the papers are read
- [ ] Gantt dates filled in
- [ ] Timed run-through under 10 minutes (aim for 9)
- [ ] One `/viva-drill` rehearsal
