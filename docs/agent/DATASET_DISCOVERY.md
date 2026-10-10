# DATASET DISCOVERY PROTOCOL

Standing mandate: actively explore datasets that fit the project goals. Do not wait to be asked. A better dataset can change the project more than a better model.

## 1. Cadence

- Phase 0: initial survey for all three modules (seeded below).
- Start of every module and of every major phase: targeted discovery for that module.
- Monthly: refresh. New releases appear; check old candidates again.
- Any time a dataset is cited in a paper you read and looks relevant, add it as a candidate.

## 2. What we are looking for

**Module A (classification)**
- Field polygons plus per-field crop labels, open licence, enough years, Sentinel-2 era (2017 onward gives usable global L2A coverage; verify per region).
- The Stage 1 country is chosen by this search, not fixed in advance. Priority order: (1) proper field polygons with reliable per-field labels, open licence; (2) sugarcane as an explicit class; (3) conditions closer to Pakistan (irrigated, smallholder, similar crops) as a tiebreaker. Current preference from kit research: Brazil (a hypothesis until the audit).
- Stage 2 (Pakistan, end of the FYP): track Pakistani, South Asian and similar irrigated smallholder datasets in every round, even if unusable now, so Stage 2 starts from a known list. No ground truth of our own is required at this stage; open data only.
- Additional crops common in the target region (wheat, rice, cotton, maize, and similar).

**Module B (health monitoring)**
- Any ground truth of crop stress, disease, drought, flood, lodging or hail events with date and location.
- Long vegetation time series for building expected-behaviour baselines.
- Complementary signals: Sentinel-1 radar, weather reanalysis, rainfall, soil moisture, land surface temperature.
- Crop calendars and phenology references per crop and region.

**Module C (yield)**
- Field-level or farm-level yield records with location, crop, season (best).
- District or county statistics (coarse but widely available).
- Yield-monitor data, harvest records, insurance or extension-service data.
- Weather and soil covariates.

## 3. Where to look

Open data portals and catalogues (Source Cooperative, Zenodo, Hugging Face datasets, Microsoft Planetary Computer catalogue, Google Earth Engine catalogue, Copernicus services, national agriculture and statistics agencies, FAO and related agencies), data-availability statements in papers, benchmark repositories (for example TorchGeo's dataset list), and competition archives. Search for sugarcane, the target region, and each module's needs. Prefer primary sources over blog posts. Do not scrape sites whose terms forbid it.

## 4. Evaluation rubric (score 0 to 3 each; record the reasoning, not only the number)

1. Relevance to the module and target region
2. **Label provenance**: ground survey > farmer declaration > expert digitisation > model output. Model-derived labels carry circularity risk: training on them teaches the earlier model's mistakes. Flag it.
3. Geometry: field polygons > points > rasters
4. Temporal fit with available imagery and seasons covered
5. Class coverage (sugarcane, key crops)
6. Size and class balance
7. Licence clarity and permissiveness for a thesis and for any later publication
8. Documentation and reported validation quality
9. Accessibility and ease of use (format, size, stability of hosting)
10. Maintenance and versioning

## 5. Verification checklist before adoption

1. Open the landing page. Record title, publisher, DOI or URL, retrieval date, version, licence, citation.
2. Read the licence and any use restrictions. Record in `docs/data/licences.md`.
3. Download a small sample only (under 500 MB without user approval). For larger downloads, report size and ask.
4. Inspect: CRS, geometry validity, label schema, class counts, years, spatial extent, missing values.
5. Sanity-check against imagery: plot NDVI time series per class on a sample and check they look agronomically plausible.
6. Check for duplicates, overlaps and obvious label errors.
7. Write `docs/research/datasets/<id>.md` and update the catalogue.
8. If adopted, write an ADR and register the dataset version and checksum.

## 6. Catalogue format

`docs/research/dataset_catalogue.md` table columns: ID, name, module, region, years, geometry, label type, provenance, classes (sugarcane?), size, licence, rubric total, status (candidate, verified, adopted, rejected), reason, retrieved on.

## 7. Seed candidates (details read from landing pages in kit preparation; still re-verify in the audit)

| Candidate | What I read | Concerns |
|---|---|---|
| **Brazil-Crop** (Zenodo 10.5281/zenodo.18461147, CC BY 4.0, Feb 2026) | 5,477 field geometries (Campo Verde MT 1,769; Paraná 3,708), about 30 classes incl. sugarcane, soybean, corn, cotton, wheat, pasture; campaigns Jan 2020 to Jun 2021; Shapefile and GeoPackage; ground survey with photos; no imagery included | Geometry type not stated on page; many rare classes; single-snapshot labels per campaign; two distant regions; very new, no independent use found |
| EuroCrops v2.0 France | Large declared-parcel GeoParquet, multi-year, harmonised taxonomy | No sugarcane; declared not surveyed; Europe-centred |
| Campo Verde database (IEEE DataPort 10.21227/H2804B) | 513 fields, 14 classes, 2015/16, Shapefile plus S1 and Landsat-8 | Login needed; licence not stated; no sugarcane in class list as read |
| Goiatuba early-season reference (Zenodo 10.5281/zenodo.17612590, CC BY 4.0) | 580 polygons, Goiás, Nov 2025, includes sugarcane, soybean, maize, pasture, pivot cropland | One date at season start; class list incomplete on page |
| Zheng et al. 2022 Brazil sugarcane map (Figshare 10.6084/m9.figshare.14213909) | 30 m raster, 2016 to 2019, overall accuracy 91.47 percent (2018) | Modelled raster; use for cross-checks only; dataset licence not stated on page |
| Sugarcane yield, NE São Paulo (Hugging Face 10.57967/hf/6862; Data in Brief 2026) | 12 plots, 6 farms, yield per plot, 2,157 Sentinel-2 RGB images | Tiny; CC BY-NC 4.0 (non-commercial) |
| PASTIS family | France benchmark | Small, patch-based |
| Pakistan Sentinel-2 field time series (Zenodo record 22806700) | Earlier research claimed sugarcane, Rabi 2022 and Kharif 2023, CC BY 4.0 | Not verified; record ID and claims may be wrong; polygons not confirmed |
| AgriFieldNet India | Ground-surveyed fields incl. sugarcane | Raster chips; imbalance; licence to verify |
| Queensland QLUMP | Sugarcane in Australia | Modelled labels, circular |
| Fields of The World | Field boundaries across many countries | Little crop type information; relevant for Pakistan boundary extraction |
| IBGE municipal agricultural statistics (PAM) | Brazil municipal crop area and yield by year, possible Module C regional yield labels | Not yet checked: access route, licence, granularity. Coarse (municipality) |
| Fall-back: USDA CSB with CDL | Large, public domain | Labels derived from a model |
| To investigate | CropHarvest, Sen4AgriNet, AgriSen-COG, TimeSen2Crop, MapBiomas, Canasat, Brazil Data Cube, Sentinel-1 and weather and soil-moisture sources, Pakistan crop calendars and district statistics | Everything unknown |

## 8. Ground-truth collection (OUT OF SCOPE for the FYP prototype; kept for the Pakistan startup phase)

The user has no ground truth and does not need any now. Do not start collection. Use this section only to write the Pakistan Bridge Report and, later, a real collection plan.

Public data for sugarcane health and yield in a specific region may not exist. If the user can obtain access to real farms, propose and design a ground-truth collection protocol as a Module B and C enabler:
- Field boundary by GPS walk or drawn on imagery, crop type, variety, sowing or planting date, ratoon or plant crop, irrigation events, fertiliser, observed stress events with dates and photos, harvest date, measured yield.
- A simple mobile collection tool (for example open-source form tools; verify current options), a data dictionary, and consent from the farm owners about data use and publication.
- Sampling plan: number of fields, crops, seasons, and what statistical power that gives. State plainly what it can and cannot support.
- Write the protocol to `docs/research/ground_truth_protocol.md` and discuss it with the user before any collection starts. Data on private farms needs permission and care about location privacy in public outputs.

## 9. Output to the user

When you find something promising, report: what it is, why it matters, rubric scores, risks, what you verified and what you did not, and a recommendation. Never present an unverified dataset as settled.
