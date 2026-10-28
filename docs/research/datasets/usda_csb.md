---
type: dataset
status: adopted-provisional
tags: [dataset, csb, usda, louisiana, phase-r]
phase: R
---

# USDA NASS Crop Sequence Boundaries (CSB), edition 2018-2025

| Item | Value (checked 2026-10-27) |
|---|---|
| Publisher | USDA National Agricultural Statistics Service (NASS), with ERS |
| Page | https://www.nass.usda.gov/Research_and_Science/Crop-Sequence-Boundaries/index.php |
| File | `NationalCSB_2018-2025_rev23.zip`, 3,758,027,335 bytes; Esri File Geodatabase `CSB1825.gdb` (5.4 GB unzipped), layer `national1825` |
| Licence | "considered public domain and free to redistribute" (`NationalCSB_2018-2025_rev23_metadata.htm`, in the zip) |
| Extent | contiguous US; 15,973,095 fields (MultiPolygon) |
| CRS | Albers Conic Equal Area, NAD83, metres (lat. of centre 23, long. of centre -96, standard parallels 29.5 and 45.5) |
| Columns | `CSBID`, `CSBYEARS`, `CSBACRES`, `CDL2018`..`CDL2025` (dominant CDL code per year), `STATEFIPS`, `STATEASD`, `ASD`, `CNTY`, `CNTYFIPS`, `INSIDE_X`, `INSIDE_Y`, `ORIG_FID`, `Shape_Length`, `Shape_Area` |
| How made | delineated from historic CDL rasters (crop sequences), so boundaries "reflect crops grown rather than ownership or tax parcels" |
| Code list | CDL categorisation codes parsed from NASS metadata (e.g. `metadata_la23.htm`); 45 = Sugarcane |

## Local copies (git-ignored, kept)

- `data/raw/csb/NationalCSB_2018-2025_rev23.zip` and the unzipped folder `data/raw/csb/NationalCSB_2018-2025_rev23/`.
- `data/interim/csb/csb1825_louisiana.parquet`: Louisiana (`STATEFIPS = '22'`), 206,389 fields, 88 MB. Made with `pyogrio.read_dataframe(..., where="STATEFIPS = '22'")`, about 2 minutes.
- `data/reference/cdl_codes.csv`: 134 code-name pairs.

## Known limits

- Labels are model output: the dominant CDL class per field, so they inherit CDL errors (rubric criterion 2; H-24).
- Boundaries are fixed for the 8-year edition, and they come from 30 m pixels, so they're smooth and may merge real fields.
- No harvest or planting dates.

Used by: [S01](../spikes/S01_csb_fields.md).
