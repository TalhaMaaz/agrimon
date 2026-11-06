---
type: dataset
status: adopted-provisional
tags: [dataset, cdl, usda, labels, phase-r]
phase: R
---

# USDA NASS Cropland Data Layer (CDL), 2023

| Item | Value (checked 2026-11-06) |
|---|---|
| Page | https://www.nass.usda.gov/Research_and_Science/Cropland/Release/index.php |
| File | `2023_30m_cdls.zip`, 2,059,094,665 bytes; contains `2023_30m_cdls.tif` (3.2 GB, 153,811 × 96,523 pixels, `uint8`, 30 m), a `.tif.ovr` overview file (4.7 GB) and FGDC/ISO metadata |
| CRS | NAD83 / Conus Albers, identical to the CSB |
| Licence | "considered public domain and free to redistribute" (`metadata_CDL23_FGDC-STD-001-1998.htm`, in the zip) |
| Sugarcane accuracy, Louisiana 2023 | producer's accuracy 95.0 %, user's accuracy 96.4 % (`metadata_la23.htm`) |
| Other files on the release page (not downloaded) | 30 m confidence layers (2023: 6.3 GB), 10 m CDL for 2024 and 2025, 2025 cultivated layer, crop frequency 2008–2025 |

Local copy (git-ignored, kept): `data/raw/cdl/`. Used by [S02](../spikes/S02_cdl_labels.md).
