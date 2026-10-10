---
type: architecture
status: living
tags: [architecture, phase-r, hypotheses]
phase: R
---

# Hypothesis register

One row per architecture hypothesis. Status is one of **hypothesis** (written down, not tested), **validated** (supported by read papers and/or our own spike), **provisional** (partly supported; validation plan exists), **rejected** (with reasons). A status changes only when evidence is recorded in the Evidence column. Questions they answer are in [design questions](design_questions.md).

Rows H-01 to H-09 come from `docs/agent/RESEARCH_AND_ARCHITECTURE.md` section 3. Rows H-10 onward were added on 2026-10-10 from the kit's module files, where they appear as unstated assumptions.

| ID | Hypothesis | Answers | Source | Status | Evidence | Pakistan relevance |
|---|---|---|---|---|---|---|
| H-01 | Classify at parcel level using per-parcel aggregated time series | DQ-05 | Starting kit | hypothesis | | Weak point: open parcel polygons are scarce in Pakistan; a boundary-extraction step or pixel-level fallback may be needed |
| H-02 | Sentinel-2 L2A through STAC (Microsoft Planetary Computer) is the primary imagery source | DQ-02, DQ-04 | Starting kit | hypothesis | | Global coverage, so transfers; terms of use to check for commercial use |
| H-03 | Spatial block validation plus a held-out region/year is needed for honest scores | DQ-10, DQ-11 | Starting kit | hypothesis | Roberts et al. 2017 (to be read) | Transfers directly; even more important with clustered smallholder labels |
| H-04 | LightGBM baseline, then TempCNN and attention models, is the right model ladder | DQ-13 | Starting kit | hypothesis | Pelletier et al. 2019; Garnot et al. 2020 (to be read) | Small label sets in Pakistan may favour simpler or pretrained models |
| H-05 | Radar (Sentinel-1) is needed under cloud | DQ-03 | Starting kit | hypothesis | | Probably high: monsoon (kharif) season is cloudy |
| H-06 | Health is best expressed as deviation from an expected crop curve | DQ-18 | Starting kit | hypothesis | | Needs crop calendars for rabi/kharif crops |
| H-07 | A static web map (MapLibre GL JS and PMTiles) suffices for the demo | DQ-15, DQ-16 | Starting kit | hypothesis | | A startup product would likely need a backend; acceptable for a prototype |
| H-08 | Brazil-Crop is a suitable first dataset | DQ-01, DQ-14 | Web research | hypothesis | Landing page read during kit preparation; audit not done (issue #10) | Low direct transfer (different crops, fields, calendars); the pipeline transfers |
| H-09 | The repository layout in PROJECT_CONTEXT section 8 is adequate | DQ-20 | Starting kit | hypothesis | | Neutral |
| H-10 | Planetary Computer is preferable to Google Earth Engine as the main imagery path | DQ-02, DQ-04 | MODULE_A section 1 (implied) | hypothesis | Earth Engine is noncommercial for this user (CLAUDE.md); other factors to compare | High: a startup cannot depend on noncommercial terms |
| H-10b | Fixed 10-day median composites are a good temporal grid | DQ-07 | MODULE_A section A-Phase 3 | hypothesis | | Cloudier regions may need longer intervals or radar fill |
| H-11 | The Sentinel-2 Scene Classification Layer (SCL) is a good enough cloud mask | DQ-06 | MODULE_A section A-Phase 3 | hypothesis | | Monsoon haze and small fields may need a stronger mask |
| H-12 | A large declared-label dataset (EuroCrops France) is needed to prove the pipeline before trusting small Brazilian results | DQ-01 | MODULE_A section 0 | hypothesis | Conflicts with MODULE_A section 8 wording; resolve at Checkpoint R | Neutral |
| H-13 | Per-parcel mean and standard deviation of 10 bands plus a few indices are sufficient features | DQ-08 | MODULE_A section A-Phase 3 | hypothesis | | Small parcels give few interior pixels; statistics become noisy |
| H-14 | Streaming windowed extraction with zonal statistics fits the laptop, lab PC and 60 GB disk budget | DQ-09 | MODULE_A section A-Phase 3, CLAUDE.md rule 9 | hypothesis | To be checked by a pilot (issue #12) | Larger areas in Stage 2 increase the cost |
| H-15 | Temperature scaling gives adequately calibrated probabilities | DQ-12 | MODULE_A section A-Phase 5 | hypothesis | Guo et al. 2017 (not yet verified) | Transfers |
| H-16 | Truncation-augmented training gives usable in-season predictions | DQ-17 | MODULE_A section A-Phase 6 | hypothesis | | Important: farmers and buyers want early answers |
| H-17 | A present-day run (demo Tier 2) is feasible on the dataset's polygons despite year-to-year change and domain shift | DQ-17 | MODULE_A section 0b | hypothesis | Gated after Checkpoint A5 | Same present-day data path as Module B |
| H-18 | A pinned Python environment (one lockfile) on Ubuntu laptop, CPU lab PC and Kaggle/Colab is workable | DQ-20 | PROJECT_CONTEXT | hypothesis | System Python on the laptop is 3.14 (2026-10-10); geospatial wheels may lag, so the project Python version needs checking | Neutral |
