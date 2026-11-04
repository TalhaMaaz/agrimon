---
type: research
status: draft
tags: [research, phase-r, literature, existing-systems, presentation]
phase: R
---

# Existing systems and literature review (for the mid-semester presentation)

Written 2026-11-04 for slides 5 (literature, existing systems) and 3 (problem statement). Search rows R3-01 to R3-07 in the [search log](search_log.md).

**How far to trust this.** Every row says how deeply the source was read:
- **read:** the full page or document text was checked.
- **page:** a vendor's marketing page only. If a feature isn't mentioned there, that doesn't prove the product lacks it.
- **abstract:** only the abstract or an index record was seen. Don't quote detailed results.

## 1. Context figures (Pakistan)

From the [Pakistan Economic Survey 2025-26, Chapter 2](https://www.finance.gov.pk/survey/chapter_26/2_Agriculture.pdf) (read; 2025-26 figures are provisional):

| Sugarcane, 2025-26 | Value |
|---|---|
| Area | 1.22 million ha (up 2.4 %) |
| Production | 89.45 million tonnes (up 6.2 %) |
| Yield | 73,200 kg/ha (up 3.7 %; 70,611 kg/ha in 2024-25) |
| Share of the economy | 0.8 % of GDP, 3.2 % of agricultural value addition |
| Role | raw material for "the 2nd largest agro-based" industry, sugar |

## 2. Comparison

| System or study | Type | Field polygons | Sugarcane | Health over time | Yield | Depth |
|---|---|---|---|---|---|---|
| SUPARCO crop monitoring (Pakistan) | Government statistics and portals | Crop field layers existed (used to verify 2015 subsidy claims) | Yes | NDVI and agro-met reporting (portal, GLAM-Pakistan) | Forecasts and estimates | read (one review) |
| EOSDA Crop Monitoring | Commercial platform | User draws or uploads them | Not mentioned on the page | Yes: 10 indices, risk alerts | Yes | page |
| OneSoil | Commercial platform | "Global field boundaries map" | Not mentioned on the page | Yes: health zones | Not stated directly | page |
| Cropin | Commercial, mostly enterprise | Not mentioned on the page | Not mentioned on the page | Yes | Yes | page |
| Di Tommaso et al. 2024 | Research: 10 m global sugarcane map | No, pixels only | Yes | No | No | read |
| Punjab sugarcane deep learning paper 2024 (*RS Applications: Society and Environment*, article 101225) | Research: pixel classifier for Punjab | Not mentioned | Yes, harvest-ready | Not mentioned | Not mentioned | abstract |
| Hu et al. 2022 | Research: regional yield, Florida and Louisiana | Not per field (regional) | Yes | No | Yes | abstract |

## 3. What each one shows

**SUPARCO** ([Akhtar, PIDE Discourse 2024](https://file.pide.org.pk/pdfpideresearch/discourse-2024-04-6-suparco-interventions-for-geospatial-monitoring-of-agricultural-crops.pdf)):
- Monitoring began in 2005 with a pilot in Bahawalpur, Rahim Yar Khan and Ghotki, covering wheat, cotton and sugarcane.
- Stakeholders listed are government bodies (provincial Crop Reporting Services, Pakistan Bureau of Statistics, the ministry, the Met Department). The purpose described is crop statistics for policy.
- Crop yield modelling used NDVI from 1 km SPOT Vegetation data.
- A PSDP project with PMAS Arid Agriculture University, running since 2020, is working towards a "decision support system at field/local scale", so field-level support is recognised as work still in progress. The review's author is from the agency's side of this work, so it isn't an independent assessment.

**Di Tommaso et al. 2024** ([ESSD 16:4931-4947](https://essd.copernicus.org/articles/16/4931/2024/)):
- Sugarcane is detected as crop pixels that stay tall for many months, using GEDI lidar and Sentinel-2.
- Covers the top 13 producing countries, 2019 to 2022, including Pakistan.
- **Pakistan: F1 0.6 with recall 0.43** against WorldCereal labels, using a threshold borrowed from India because no local calibration labels were available. Against government statistics at admin level 2, R² is 0.85.
- So even a strong global product misses a large share of Pakistani cane at point level.
- Limits relevant to us: no polygons, no health, no yield.

**Punjab paper 2024** (index record and abstract listing only):
- Sentinel-2 L2A with twelve bands and six indices over ten time stamps; labels from linear spectral unmixing; CNN and LSTM.
- It classifies **pixels**; its labels are derived rather than from a survey.

**Hu et al. 2022** (see [related work 2b](related_work_louisiana.md)):
- Regional yield from MODIS and weather data with statistical models; SiPAR performed best.

**Vendor pages** ([EOSDA](https://eos.com/products/crop-monitoring/), [OneSoil](https://onesoil.ai/en/), [Cropin](https://www.cropin.com/)), checked 2026-11-04:
- Mature general-purpose tools. Prices aren't listed on these pages.
- None of the three pages mentions sugarcane. None describes tracking the plant cane and ratoon cycle or a sugar-mill workflow.
- This is a limit of what the pages say. Before claiming more, check the vendors' documentation or ask them.

## 4. The gap, stated carefully

From the sources checked, the pieces exist separately:

```
 statistics for government .............. SUPARCO
 general field monitoring ............... EOSDA, OneSoil, Cropin
 sugarcane maps, pixel level ............ Di Tommaso 2024, Punjab 2024
 regional sugarcane yield ............... Hu 2022
```

**We found no openly documented system that combines field polygons, sugarcane classification, health monitoring that follows the cane cycle, and yield in one pipeline built to transfer to Pakistan.** That is a statement about what we found, not proof that nothing exists.

How AgriMon differs:
1. Sugarcane-specific: S01 shows the multi-year cane cycle in real field histories, so health baselines can follow the cycle stage rather than the calendar (still to be built and tested).
2. Per-field outputs on a map, not pixels or district totals.
3. Built and validated first where open data is rich (Louisiana), then adapted to Pakistan.
4. Open, documented and reproducible.

What it doesn't claim: better accuracy than these systems (nothing has been measured yet), or commercial readiness.

## 5. Draft problem statement (for you to confirm)

> Pakistan grows sugarcane on 1.22 million hectares, yet available satellite-based information is mainly aggregate statistics for government or pixel maps with no field-level view. A sugar mill or agronomist has no openly available tool that shows, per field, where the cane is, how healthy it is against the expected cane cycle, and roughly what it may yield. General commercial platforms exist, but what we could check of them isn't built around sugarcane's multi-year cycle, and the best global sugarcane map still recalls only 43 % of Pakistani cane in point validation.

**Needs your confirmation:** the claim about what mills and agronomists lack rests on your field experience in Rahim Yar Khan and the startup contact. No source above states it directly.

## 6. Still to read (publisher sites returned 403 to automated fetching)

| Paper | Why | Link |
|---|---|---|
| Hu et al. 2022 | Closest yield work; need its accuracy numbers and spatial level | https://doi.org/10.3390/rs14163870 |
| Sugarcane remote sensing review, 2021 | Survey for slide 5; authors unconfirmed | https://doi.org/10.3390/rs13204040 |
| Punjab sugarcane paper, 2024 | Closest Pakistan work; need authors and accuracy | https://www.sciencedirect.com/science/article/pii/S2352938524000892 |
| Weiss, Jacob, Duveiller 2020 meta-review | Map of the whole field | https://www.sciencedirect.com/science/article/pii/S0034425719304341 |
