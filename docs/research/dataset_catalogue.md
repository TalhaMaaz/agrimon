---
type: research
status: living
tags: [research, phase-r, datasets, catalogue]
phase: R
---

# Dataset catalogue

Candidates for the Stage 1 region, scored against the [product spec](../architecture/product_spec.md) section 4 (capabilities P-1 to P-4) and the rubric in `docs/agent/DATASET_DISCOVERY.md` section 4 (criterion 11, module and demo coverage, is weighted double). A candidate may be a **stack**: several sources over one region. Only facts checked at the source are written as facts; everything else is marked *unverified*.

Round 1: 2026-10-27, search log rows R1-01 to R1-08. Status values: candidate, verified, adopted, rejected.

## 1. Coverage summary

```
                         P-1 polygons      P-2 crop labels    P-3 health        P-4 yield
                         (labelled+recent) (cane? years)      (history+recent)  (statistics)
 S-US  US sugarcane belt   yes, annual       yes, cane, many    yes               state level yes;
       (FL / LA): CSB+CDL  (model-derived)   years (model)                        county unverified
 S-RE  La Reunion:         likely, annual    yes, cane,         likely            unverified
       RPG (+ CIRAD)       (unverified)      declared (unverif.)
 S-BR  Brazil-Crop         labelled seasons  yes, cane, 2 seas. weak (no recent   IBGE municipal
       (+ IBGE PAM)        only (2020-21)    per region         labelled fields)  unverified
 S-EU  EuroCrops / FR RPG  yes, annual       no cane (sugar     yes               unverified
       (cane-free)         (not re-checked)  beet analogue)
```

## 2. Candidates

### S-US: US sugarcane belt (Florida, Louisiana), status: candidate (strongest coverage so far)

| Source | What was checked (2026-10-27) | Not verified |
|---|---|---|
| USDA NASS Crop Sequence Boundaries (CSB) | Field boundaries "across the contiguous U.S.", built by NASS with ERS from satellite imagery and public data. 11 eight-year editions from 2008-2015 to 2018-2025; the 2018-2025 data were released 2026-03-27; v2024 is hosted on Zenodo. Boundaries "reflect crops grown rather than ownership or tax parcels". Called "open source"; code on GitHub ([NASS CSB page](https://www.nass.usda.gov/Research_and_Science/Crop-Sequence-Boundaries/index.php)) | Licence name; per-year crop attributes; file sizes; boundary accuracy |
| USDA NASS Cropland Data Layer (CDL) | Code 45 is Sugarcane. Florida 2022: producer's accuracy 96.5 %, user's accuracy 96.2 % for sugarcane; overall 87.4 % (crop classes). Trained and validated on FSA Common Land Unit data. "Public domain and free to redistribute" ([FL 2022 metadata](https://data.nass.usda.gov/Research_and_Science/Cropland/metadata/metadata_fl22.htm)) | Louisiana sugarcane accuracy; other years |
| NASS sugarcane yield statistics | State-level yields for Florida and Louisiana in net tons per acre appear in archived NASS sugarcane reports (for example 2005, 2007) | County or parish level yields in Quick Stats |

- **Strengths:** every capability has a source; annual polygons up to 2025 allow a recent-season health layer; many years for health baselines and held-out-year splits; public domain; a sugarcane industry with mills (aligns with the product).
- **Concerns:**
  - The labels are **model output** (CDL), so there is a circularity risk (rubric criterion 2): a model trained on CDL partly learns CDL's errors. The sugarcane accuracy is high, but it must be stated in the thesis.
  - Large mechanised farms, unlike Pakistan.
  - The CSB boundaries are themselves derived from CDL.

### S-RE: La Reunion (France), status: candidate (needs verification first)

| Source | What was checked (2026-10-27) | Not verified |
|---|---|---|
| Registre Parcellaire Graphique (RPG) | National RPG on data.gouv.fr is under "Licence Ouverte / Open Licence 2.0"; updated annually; open versions describe anonymised blocks ("îlots") with a majority crop group. IGN's change log: from the 2024 edition the RPG is version 3.0 with seven sub-products, including parcels. A DAAF Reunion / Agreste study (2024) compares RPG 2019 and 2023 for sugarcane and says CAP declarations cover 95 % of the island's cane area | Whether the open RPG includes La Reunion at **parcel** level with crop codes; which years; download route |
| CIRAD reference database 2017 (Dupuy, Gaetano, Le Mézo, Data in Brief) | 6,256 annotated polygons for a 2017 land-use map; hierarchical nomenclature from 4 to 34 classes; Dataverse doi:10.18167/DVN1/TOARDN (seen in search results) | Whether sugarcane is a class; licence |

- **Strengths:** sugarcane is the main crop; the labels are **farmer declarations** (better provenance than model output); smaller fields, closer to Pakistan than the US; the island has sugar mills; annual updates.
- **Concerns:**
  - Parcel-level open access is unverified; the open RPG may give only blocks.
  - A mountainous tropical island, so heavy cloud (Sentinel-1 likely needed).
  - Yield statistics unverified.

### S-BR: Brazil-Crop (+ IBGE PAM), status: verified (dataset); stack incomplete

- Zenodo record 18461147, checked 2026-10-27: 5,477 field geometries (1,769 Campo Verde, MT; 3,708 Paraná); 30 classes including sugarcane; CC BY 4.0; four campaigns from 2020-01-13 to 2021-06-12 (two per region); field vectors 16 MB (MT 7.2 MB, PR 9.0 MB) of 10.4 GB total (the rest is photos). Geometry type not stated.
- **Strengths:** ground survey (best label provenance); sugarcane.
- **Concerns:**
  - No recent-season polygons, so the live health layer must reuse 2020-21 boundaries (H-23).
  - Only two seasons per region.
  - Few fields per class across 30 classes.
  - IBGE municipal yield statistics are unverified.
- **Role:** a strong second dataset or fallback for P-2.

### S-EU: EuroCrops or metropolitan France RPG, status: candidate (not re-checked in round 1)

- Annual declared parcels over many years; no sugarcane; sugar beet is grown and processed by sugar factories, so it is a possible industry analogue. Kept as the cane-free fallback (user, 2026-10-27: a cane-free dataset is acceptable if it covers the modules much better).

### Stage 2 lead (not for Stage 1)

- Zenodo 22806700, "Sentinel-2 Field-Level Crop Phenology Time Series in Pakistan (85,618 Fields, 79 Districts, Rabi & Kharif)", CC BY 4.0, 2026-09-17. Recorded only; not downloaded (user, 2026-10-27).

## 3. Recommendation after round 1

1. **Verify S-RE first.** If the open RPG gives La Reunion parcels with crop codes over several years, it combines declared labels, sugarcane and smaller fields, which is the best fit to the spec on paper.
2. **Verify S-US in parallel:** CSB attributes, county yields, a small CSB sample for one sugarcane county (under 500 MB, ask first). It already covers every capability, at the cost of model-derived labels.
3. Keep **S-BR** as the ground-truth second dataset and **S-EU** as the cane-free fallback.
4. Decide at Checkpoint R with rubric scores (DQ-01); record an ADR.
