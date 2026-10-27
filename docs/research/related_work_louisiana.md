---
type: research
status: living
tags: [research, phase-r, related-work, louisiana, sugarcane]
phase: R
---

# Related work: sugarcane remote sensing in Louisiana

Question (user, 2026-10-27): is there existing work in Louisiana of the same nature as ours? Search rows R2-01 to R2-05 in the [search log](search_log.md). Reading depth for every item is **metadata or abstract only**: no paper has been read in full yet, so nothing here can be cited for its results until it is (CLAUDE.md rule 6).

## 1. Answer in short

The search found no study or system that does what ours does for Louisiana, which is field-level crop type, health and yield from Sentinel-2 in one application. It found related work for each piece:

```
 our capability        closest Louisiana work found                         type
 --------------        ------------------------------                       ----
 P-2 crop type         Di Tommaso et al. 2024: global 10 m sugarcane map     peer-reviewed data paper
                       (GEDI + Sentinel-2), includes Louisiana
 P-3 health            NASS Hurricane Laura assessment 2020: Sentinel-1      government report
                       flood layer over Louisiana cane; event reports        news / extension
                       (Ida 2021, freeze Feb 2021, Francine 2024)
 P-4 yield             Hu et al. 2022: regional yield, MODIS + weather,      peer-reviewed article
                       Florida and Louisiana 2008-2016
                       LSU handheld-sensor NDVI yield study (Sensors 2012)   peer-reviewed, ground sensor
```

A search can't prove that nothing exists, so we state it carefully: "we found no published work combining...", and we repeat the search before the thesis.

## 2. Items

### 2a. Di Tommaso, Wang, Strey, Lobell 2024, "Mapping sugarcane globally at 10 m resolution using Global Ecosystem Dynamics Investigation (GEDI) and Sentinel-2", Earth System Science Data 16:4931-4947, DOI 10.5194/essd-16-4931-2024

Checked from the article page on 2026-10-27:
- 10 m sugarcane maps for 2019 to 2022 in the main producing countries.
- Trained with GEDI (a lidar on the space station that measures canopy height) and Sentinel-2.
- Data on Zenodo (DOI 10.5281/zenodo.10871164) and as an Earth Engine asset; the article is CC BY 4.0, and the dataset licence was not stated on the page.
- For the US, the paper reports CDL sugarcane precision and recall above 93 % for Louisiana (2019-2022), measured against FSA labels.
- Its own map versus CDL across the US: precision 0.85, recall 0.82, F1 0.84. Against 2018 NASS county statistics: R² 0.9 for Louisiana.

Why it matters:
- (1) An **independent** sugarcane map, not trained on CDL. Comparing CDL with it lets us check our labels without circularity (H-24).
- (2) A peer-reviewed source confirming CDL's sugarcane quality in Louisiana.
- (3) "NASS county data" suggests county or parish sugarcane **area** statistics exist (DQ-22; whether parish **yield** exists is still unverified).

### 2b. Hu, Shi, Zha, Zeng 2022, "Regional Yield Estimation for Sugarcane Using MODIS and Weather Data: A Case Study in Florida and Louisiana, United States of America", Remote Sensing 14(16):3870, DOI 10.3390/rs14163870 (open access, CC BY)

Checked from the OpenAlex metadata and abstract on 2026-10-27:
- Yields estimated for 2008 to 2016 with three statistical models (CNDVI, K-M, SiPAR) driven by MODIS and weather data.
- Robustness was tested with parameters taken from Reunion Island and south-western China.
- SiPAR (which includes solar radiation) performed best; K-M missed low yields because it ignores temperature and water stress.
- The abstract gives no accuracy numbers and doesn't say whether the yields are state or parish level. The full text is needed (the MDPI page returned 403 to the fetch tool).

Why it matters: the closest existing work to P-4, and a candidate **baseline approach** for regional yield. It also points to Réunion as a sugarcane research site.

### 2c. "Estimating Sugarcane Yield Potential Using an In-Season Determination of Normalized Difference Vegetative Index", Sensors 2012, 12(6):7529 (PMC3435988)

Seen in search results only (authors not yet confirmed):
- A handheld GreenSeeker NDVI sensor at St. Gabriel and Jeanerette, Louisiana, 2008 to 2011.
- NDVI divided by thermal variables predicted cane tonnage and sugar yield with r² of 0.48 and 0.42.

Why it matters: shows NDVI relates to Louisiana cane yield and when in the season (a growing-degree-day window). It is a ground sensor, not a satellite.

### 2d. USDA NASS, Hurricane Laura Assessment Report (2020)

Seen in search results only:
- A Sentinel-1 radar "inundation layer" (15 Aug to 4 Sep 2020) over Louisiana cropland, including about 469,000 acres of sugarcane.
- About 3.7 % of that acreage was estimated under water; marked "not official NASS estimates".

Why it matters: a government use of Sentinel-1 for crop damage, and a **documented event** for testing the health layer (P-3, DQ-18).

### 2e. Documented stress events (news and extension reports, not papers)

- **Hurricane Ida (2021):** about 118,000 acres of sugarcane affected; projected yield losses of 16 to 29 % in the affected area (LSU / Sugar League projection, via Agweek).
- **February 2021 freeze:** more than 60 hours below freezing; the northern cane belt was more exposed (LSU AgCenter).
- **Hurricanes Delta (2020) and Francine (2024):** lodging and flooding.

Why it matters: candidate validation events for the health layer. Each must be confirmed from a primary source (NASS, LSU AgCenter) before use.

### 2f. Review to read: "Remote Sensing Applications in Sugarcane Cultivation: A Review", Remote Sensing 2021, 13(20):4040, DOI 10.3390/rs13204040

Seen in search results only. Reported to note that Landsat and Sentinel-2 support reliable sugarcane mapping, and that most yield studies used coarse NDVI series (MODIS, SPOT-VGT). Authors to confirm. A good first survey paper for the sugarcane side of Phase R.

## 3. What this means for the project

- **Novelty, stated carefully:** field-level crop type, health and yield for Louisiana sugarcane from Sentinel-2, in one application, appears not to have been published.
- **Standards exist piece by piece:**
  - an independent sugarcane map, to check our labels;
  - regional yield models with weather (SiPAR);
  - radar for flood damage;
  - NDVI timing for yield.
- **Next reading:** the 2f review (survey first), then Di Tommaso 2024 and Hu 2022 in full.
