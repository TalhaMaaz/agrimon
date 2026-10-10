# MODULE A: CROP CLASSIFICATION

Goal: classify the crop growing in each field (parcel) from Sentinel-2 time series, show parcels on a web map coloured by the crop predicted as of a chosen date. This is a prototype built entirely from open data, with the focus on software engineering and pipelines. There is no ground truth of our own and none is required. Pakistan-specific work comes after the pipeline exists and the user understands it.

Each phase starts with a Phase Brief and a Primer (see TEACHING_PROTOCOL), and ends with the Phase Exit Rule (see DOCUMENTATION_PROTOCOL).

## 0. Dataset strategy (Turn-10 update; decided at Checkpoint A1 from the audit, recorded as ADR)

The user's preference is Brazil because of sugarcane, and the immediate goal is a good-looking, good-performing demo from any suitable open dataset. Candidates, in recommended order (all details must be re-verified by the agent in Phase A-1):

1. **Brazil-Crop (Zenodo, DOI 10.5281/zenodo.18461147, CC BY 4.0, published 2 Feb 2026).** Read from the landing page: 5,477 unique field geometries (1,769 in Campo Verde, Mato Grosso; 3,708 in Paraná), about 30 land-use classes including sugarcane, soybean, corn, cotton, wheat, pasture, eucalyptus; four field campaigns between Jan 2020 and Jun 2021; Shapefile and GeoPackage vectors; 2,242 geotagged photos; about 10 GB mostly photos; field boundaries delimited on Sentinel-2 imagery, labels checked with MODIS NDVI. It contains no imagery or time series, which fits our own streaming pipeline. Recommended PRIMARY dataset because it is Brazilian, has sugarcane, is surveyed on the ground (best label provenance), and is open. NOT verified yet: exact geometry type, per-campaign attributes, label date per field, class counts after cleaning, whether fields repeat across campaigns, and spatial overlap. Expect heavy class imbalance and many rare classes among 30; merging to a smaller class list is likely.
2. **EuroCrops France (v2.0, gpqtv202).** Large, clean, polygon-based, multi-year declared labels. Kept as a PIPELINE-PROVING benchmark: 100,000s of parcels let the spatial-validation and model-comparison machinery be tested properly before trusting small Brazilian results. No sugarcane. Optional, decided at Checkpoint A1.
3. **Campo Verde database (IEEE DataPort, DOI 10.21227/H2804B).** 513 reference fields, 14 classes, 2015/16 crop year, Shapefile; includes Sentinel-1 and Landsat-8 imagery; no sugarcane in the class list as read; login required, licence unclear. Supporting or backup only.
4. **Goiatuba early-season reference dataset (Zenodo DOI 10.5281/zenodo.17612590, MDPI Data 2025, CC BY 4.0).** 580 plots in Goiás, polygons in a GeoPackage, fieldwork 3 to 7 Nov 2025 at the start of the 2025/26 season, includes sugarcane, soybean, maize, pasture, centre-pivot cropland. A single-date snapshot at the very start of a season, so labels may describe what is planned or just sown rather than what grows through the season. Useful as an out-of-region, out-of-year test set for Brazil-Crop models if the label meaning is compatible. Needs careful reading.
5. **Zheng et al. 2022 sugarcane map (ESSD 14:2065, Figshare DOI 10.6084/m9.figshare.14213909).** 30 m raster, 2016 to 2019, 91.47 percent overall accuracy for 2018. Not field polygons and model-derived, so never used as training truth. Use as an independent cross-check of sugarcane areas.
6. **Sugarcane yield dataset, NE São Paulo (Data in Brief, 2026; Hugging Face 10.57967/hf/6862).** 12 plots on 6 farms; licence CC BY-NC 4.0. Far too small to train yield models; at most a toy example for Module C. Non-commercial licence matters for a future startup.

Decision rules for Checkpoint A1: (a) if Brazil-Crop audit passes (valid polygons, usable labels, at least 3 to 5 classes with 200+ fields each after cleaning, sugarcane among them), adopt it as primary; (b) if it fails, fall back to EuroCrops France for stage 1 and keep Brazil as the extension; (c) in both cases keep the label-adapter interface so the second dataset is a configuration change. Record scores from the DATASET_DISCOVERY rubric. Ask the user before final choice.

Honest note to teach the user: Brazil-Crop labels are field-survey snapshots from specific campaigns in two regions, so the demo will be strong for those areas and years, and will not automatically transfer to Pakistan (irrigated smallholder wheat-rice, cotton and sugarcane systems, very different field sizes and calendars). The transferable asset is the pipeline and the evaluation discipline.

## 0b. Demo tiers ("which field is planted today")

The user wants the final demo to run the trained model on present-day fields, with a safe fallback to old fields. Plan both:

- **Tier 1 (must, safe): replay.** Held-out fields and dates; the map shows what the model would have predicted as of each date. Fully verifiable against labels.
- **Tier 2 (stretch, high value): present-day.** Run `predict_as_of(today)` on current-season Sentinel-2 over a chosen set of field polygons and show the result with a clear "unverified prediction" label.

What Tier 2 needs, and why it is harder: (1) polygons for present fields (reuse the dataset's polygons if boundaries are unchanged, accept that boundaries and crops change between years; extracting new boundaries is a separate problem, see Fields of The World); (2) fresh imagery through STAC with measured latency; (3) an in-season model that works with partial seasons (design study DS-A-07), because "today" is mid-season or earlier; (4) a model trained on 2020 to 2021 labels applied to a later year, which is temporal domain shift, so expect weaker results and the L2A processing-baseline offset from early 2022 must be harmonised; (5) no labels exist for the present season, so accuracy cannot be reported for Tier 2, only plausibility checks (agreement with neighbours, phenology sanity, confidence) and honest wording. Module B's near-real-time pipeline shares the same present-day data path, so build it once and use it for both.

Decision gate after Checkpoint A5: Tier 2 goes ahead only if a pilot on a few hundred polygons works end to end. Record the outcome in an ADR.

## 1. Starting hypotheses (NOT locked: validate or replace each in Phase R, then record the outcome as an ADR with evidence; items marked EC apply only if EuroCrops France is used)

- (EC) Dataset: EuroCrops v2.0 (JRC), France only for stage 1. Download root: https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/DRLL/EuroCropsV2/ . Use the latest corrected folder `gpqtv202` (older: `gpqt` initial, `gpqtv201` stack-layer fix). Confirm that it contains the France files you need via `all_gpqt_files.csv` and the folder listing. Read `copyright.txt` and `README.html` in the root first.
- (EC) File naming `<nuts>_<year>.parquet` (France is `fr`); `<nuts>_stack.parquet` also exists. Years span 2008 to 2023 but not every year exists everywhere: verify.
- (EC) Columns: `cropfield`, `original_code`, `off_area` (when present), `area_ha`, `geom`. CRS EPSG:3035. Codes of 10000 or above are synthetic and have no semantic mapping.
- (EC) Crop-code mapping tables: GitHub repo Martincccc/EuroCropsV2, folder `data/cropcodemapping/` (`Eurocrops.csv`, `hcat4.csv`, others). The README's example mapping URL appears malformed; use the raw-content URL or clone. Join on `nuts` (lower case) and `original_code` (as string).
- Imagery: Sentinel-2 L2A from a free STAC catalogue. Preferred: Microsoft Planetary Computer (collection `sentinel-2-l2a`, signing via `planetary-computer`). Fallback: AWS Earth Search. Verify endpoints and asset names by querying; do not rely on memory.
- Unit of classification: the parcel. Polygons are given, so this is not a segmentation task. Aggregate pixels inside each parcel into a time series.
- Scope: the Sentinel-2 tile(s) covering the chosen dataset's region (Campo Verde and Paraná are about 1,000 km apart, so expect at least two separate tiles or regions; treat them as a spatial generalisation test), chosen from the audit. Tropical cloud cover is heavy in the Brazilian summer wet season: expect large gaps, plan gap handling early, and evaluate Sentinel-1 radar as an input in a design study.
- Previous-year labels and the stack layer are NOT used as input features (keeps the task as classification rather than rotation forecasting).
- The web map is a replay of held-out past dates, not a live product: current-season declarations do not exist and parcel boundaries change between years.
- Known data limitations to document, not hide (EuroCrops): labels are farmer declarations, not ground truth; only declared parcels exist; one code per parcel; French vineyard declarations were incomplete in some years; centred on European crops. (Brazil-Crop): survey snapshots per campaign, two distant regions, many rare classes, geometry and label dates unverified until the audit.

## 2. Requirements seed (finalise at Checkpoint 0; numeric targets after baselines)

- R-A-01: classify each parcel in the tile into the approved class list.
- R-A-02: headline evaluation uses spatial-block splits and a held-out year.
- R-A-03: produce calibrated class probabilities.
- R-A-04: provide `predict_as_of(date)` that uses only data up to that date.
- R-A-05: export predictions and serve them in a web map with a date selector and parcel popups.
- R-A-06: pipeline is reproducible from raw data with documented commands within the disk budget.
- R-A-07: new label sources can be added through the label-adapter interface without changing model code.

## 3. Design studies seed

DS-A-01 validation strategy (random vs spatial block, and the size of the gap); DS-A-02 model family (majority, rule, gradient boosting, TempCNN, attention); DS-A-03 temporal resolution; DS-A-04 inputs (bands, indices); DS-A-05 parcel buffer and minimum area; DS-A-06 class granularity and rare-class policy; DS-A-07 in-season truncation training; DS-A-08 calibration method.
Use at least 3 seeds for headline numbers (mean and spread). Use bootstrap confidence intervals that resample spatial blocks, not parcels. Compare models on identical splits. Do not over-claim significance.

## 4. Starting defaults (hypotheses; validate in Phase R and revise at Checkpoint A1)

- Label granularity: about 8 to 15 broad crop classes from the HCAT4 hierarchy.
- Years: for EuroCrops France, train 2021, validate 2022, test 2023 if available. For Brazil-Crop, labels cover four campaigns (Jan 2020, Aug 2020, Feb 2021, Jun 2021); a held-out-year split may be impossible, so use spatial-block splits plus a held-out campaign or held-out region (for example train on Paraná, test on Campo Verde) and state clearly what each split proves.
- Compute: develop on the laptop (RTX 3060 6 GB, 16 GB RAM) with small batches and mixed precision; heavy extraction on the lab PC (large RAM and SSD, CPU only) or on a cloud notebook; GPU-heavy runs on Kaggle or Colab if the laptop is too slow. See PLATFORM_AND_COMPUTE.md.
- Web stack: static MapLibre GL JS plus PMTiles; no backend.
- Minimum parcel area 0.5 ha (confirm from the audit); inward buffer 10 to 20 m; minimum 500 training parcels per class; 10 km spatial blocks.

## 5. Phases

### A-Phase 0: Scaffolding and charter
Create the repository layout from CLAUDE.md, pinned environment (verify installs), Makefile, pre-commit, experiment tracker, figure and table scaffolding, thesis skeleton and build target. Write charter, requirements, assumptions and risk registers, seed ADRs, learning curriculum and understanding ledger, and the initial dataset catalogue (see DATASET_DISCOVERY). Prefer packages: geopandas, pyarrow, duckdb, shapely, pyproj, rasterio, rioxarray, xarray, odc-stac or stackstac, pystac-client, planetary-computer, dask, pandas, scikit-learn, lightgbm, torch, an experiment tracker, matplotlib, pytest, ruff. Verify and adjust.
Teaching: Primer on satellite imagery and GIS basics.
**Checkpoint 0** (see CLAUDE.md section 9).

### A-Phase 1: Environment, hardware and data audit
Hardware report (laptop, then ask the user to run the same report on the lab PC). Read licences. Download the Brazil-Crop vector files only (not the 6 GB photo archives unless needed; verify file list and sizes first, and ask before any download above 500 MB) and, if EuroCrops is kept, the mapping tables and France yearly files for candidate years. Audit Brazil-Crop first: geometry type and validity, CRS, attribute schema, label dates, class counts per campaign and region, duplicates and overlaps, field size distribution, minimum size versus 10 m pixels, sugarcane share. Score it with the rubric and recommend per section 0. Use DuckDB or pyarrow to avoid loading everything. Audit report: per-year parcel counts, total area, parcel-size distribution, geometry validity, class counts and area per HCAT4 class, share of synthetic and unmapped codes, lineage table. Propose the Sentinel-2 tile (MGRS): crop-class richness, enough parcels per class, tile within France, plausible cloud-free coverage; show the top 3 with numbers.
Teaching: vector vs raster, CRS, label provenance.
**Checkpoint A1:** audit summary, hardware, tile, class list, years.

### A-Phase 2: Label curation
Define the label-adapter interface (parcel id, geometry in any CRS, crop label, year, source metadata) and implement the EuroCrops France adapter. Clip to the tile. Cleaning rules: drop synthetic and unmapped codes, "not known or other" classes, landscape-feature classes, invalid or empty geometries (repair where safe), parcels under the minimum area. Apply the inward buffer. Map to the approved classes via HCAT4; merge rare classes upward. Assign each parcel to a 10 km spatial block; fix train, validation and test blocks once and never change them silently. Outputs: processed label parquet, split table, class-distribution plot, lineage with counts dropped at each step, updated data dictionary, tests for each cleaning rule.
Teaching: leakage and spatial autocorrelation (include a notebook that demonstrates it).
**Checkpoint A2.**

### A-Phase 3: Imagery and per-parcel features
Query STAC for scenes over the tile for the target years; scene-level cloud cover only as a coarse filter. Bands B02, B03, B04, B05, B06, B07, B08, B8A, B11, B12; resample 20 m bands to 10 m consistently and record the method. Mask with the scene classification layer (drop no data, saturated, cloud shadow, cloud medium and high, cirrus, snow; verify class codes against product documentation).
IMPORTANT: the L2A processing baseline change in early 2022 introduced a reflectance offset. Verify the date and the correct scale and offset from the STAC metadata per scene, harmonise, and add a test showing a 2021 scene and a 2023 scene give comparable reflectance on a stable target. Write an ADR and a concept note: likely viva question.
Composites on a fixed grid (default 10-day median; configurable). Document the missing-data policy (limited forward fill plus validity mask). Features per parcel and time step: mean and standard deviation of each band, NDVI, NDWI, NDMI and one red-edge index on interior pixels; parcel area as a static feature.
Implementation: process in spatial windows; rasterise parcel ids once per window and compute zonal statistics with vectorised reductions instead of per-polygon masking; lazy time steps so memory stays flat; resumable at window level; retries with exponential backoff; incremental parquet writes; throughput logging.
Run a pilot first (about 1,000 parcels, a few time steps). Measure time per window, network volume, disk growth; extrapolate.
**Checkpoint A3:** pilot numbers and extrapolated cost. Wait for go-ahead, then run the full extraction in the background. Verify: no all-NaN parcels beyond an agreed threshold, mean NDVI per class over time looks agronomically sensible (for example winter cereals peak before maize), counts match the label table. Record plot and interpretation.
Teaching: reflectance, clouds, indices, phenology (Deep Dives).

### A-Phase 4: Baselines
Majority class; NDVI-threshold rule; LightGBM (or random forest) on flattened series with class weights. DS-A-01: compare random splits with spatial-block validation on the training year. Then train on the training year and evaluate on the validation year. Test year and blocks stay untouched. Metrics: accuracy, macro-F1, per-class precision, recall, F1, confusion matrix; JSON and plots to `reports/`. Per-fold scaling fitted on training data only. Register every run.
Teaching: metrics, imbalance, gradient boosting.
**Checkpoint A4:** numeric targets for deep models are agreed with the user here.

### A-Phase 5: Deep models
TempCNN and a small Transformer or L-TAE-style encoder in PyTorch; handle missing steps with the validity mask. Mixed precision, class-balanced loss, early stopping on validation, fixed seeds, tracked. Size batch and model to the detected GPU. Compare against baselines on identical splits; at least 3 seeds. Temperature-scaling calibration fitted on validation; report calibration error.
**Checkpoint A5:** comparison table, per-class results, confusion matrix, error analysis, recommendation. After approval, evaluate ONCE on the test year and blocks and record it as the single official test result, including failure classes.
Teaching: TempCNN, attention (Deep Dives), seeds and variance, calibration.

### A-Phase 6: Ablations and in-season behaviour
Run prioritised design studies. Evaluate truncated series at several cut-off dates and plot macro-F1 versus date. Train a truncation-augmented variant and compare. Implement `predict_as_of(date)` and a test proving no future information is used.

### A-Phase 7: Inference and export
Run `predict_as_of` for dates through the test year (default every 2 weeks). Output parcel id, geometry, top-1 class and probability, top-3 classes with probabilities. Reproject to EPSG:4326, write GeoParquet, convert to PMTiles (verify the tooling). Record the layout choice in an ADR.

### A-Phase 8: Web application
Static MapLibre GL JS site with PMTiles, open basemap without API key. Parcels coloured by predicted crop, legend, date selector, popup with top-3 and probabilities, opacity control, low-confidence toggle, clear note that this is a replay of held-out data. Verify in a headless browser (map loads, parcels render, date change recolours, popups work); save screenshots. Colour-blind-safe palette. Prepare an offline demo bundle and a recorded fallback.
**Milestone M1** (see ROADMAP).

### A-Phase 9: Second dataset and the Pakistan bridge
Dataset discovery round 2 (DATASET_DISCOVERY). Add the second dataset (Brazil-Crop if France was first, or EuroCrops France if Brazil was first) through the label-adapter interface and report what changes. Then write a Pakistan Bridge Report: what would be needed to run this pipeline on Pakistan (open labels, which are scarce; crop calendars for rabi wheat and kharif rice, cotton, sugarcane; field-boundary extraction because open polygons are scarce; radar for monsoon cloud; ground-truth collection), using verified Pakistan references from READING_LIST tier 3. Sugarcane is long-cycle with plant and ratoon crops, so the "planted today" idea needs rethinking: define the label with the user. Update threats to validity.
**Milestone M2.**

## 6. Anti-patterns (do not do these)

- Random pixel or random parcel splits for headline results (neighbours leak). Random splits appear only in DS-A-01, labelled as such.
- Fitting scalers or selecting classes using validation or test data.
- Touching the test year or blocks before the approved final evaluation, or tuning after it.
- Using the stack layer or previous-year labels as features.
- Mixing pre- and post-2022 reflectance without harmonisation.
- Caching whole scenes or tiles; committing data or weights.
- Mixing datasets or countries in one training set without an explicit ADR and a design study.
- Reporting a single-seed score as the result.
- Claiming the web map shows live "today" predictions.
- Undocumented decisions. If it was worth deciding, it is worth an ADR.

## 7. Seed viva questions (answer each with evidence pointers in `docs/defence/viva_questions.md`)

Why this first dataset when the long-term interest is Pakistan? What are the weaknesses of its labels as ground truth? How do Brazilian conditions differ from Pakistani ones? Why parcel-level rather than pixel-level? Why spatial validation and what would random splits have shown? How were clouds and missing data handled? What is the reflectance offset issue? Why these classes and what about rare ones? Why macro-F1? How do you know the model is not memorising local patterns? Why did the deep model beat or fail to beat gradient boosting? How well does it generalise to a new year? How early in the season can it decide? How calibrated are the probabilities? What are the label-noise effects? What happens if parcel boundaries change? Why is the map a replay? How would this extend to sugarcane or Pakistan? What are the licensing and ethical considerations? Which result surprised you most? How do you know it is reproducible?

## 8. Definition of done (stage 1)

Audited, licensed, reproducible France pipeline from raw parquet to web map; honest evaluation with baselines, design studies and a calibrated deep model, every result tied to a registered experiment; in-season curve and `predict_as_of`; web app verified in a browser plus fallback demo; tests passing; clean-clone reproducibility check passing; disk under budget; documentation and thesis sections drafted; extension point for new label sources demonstrated by a second adapter or a documented stub.
