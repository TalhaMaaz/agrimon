---
type: status
status: living
tags: [status]
---

# STATUS

Updated 2026-11-12 · laptop (Photon)

- **Now:** kit v2 in place (short CLAUDE.md, LOG, slim GitHub, tidy docs). PR #35 waits for the user's merge.
- **Done last:** mid-semester presentation given; user reported on 2026-11-12 that it went well. Data checks S01 and S02 passed earlier.
- **Next:** decide the new kit's commands and helpers; then Stage 1 preprocessing: imagery (Sentinel-2) and NASS yield checks, then model selection.
- **Waiting on:** replies from SUPARCO and NUST (Pakistani field boundaries for Stage 2).
- **Branch:** `chore/kit-v2` (PR #35).

## Open decisions (user)

- Exact study area and years for Stage 1 (Iberia parish checked so far).
- Crop task: binary cane vs non-cane, or multi-class shown as cane vs non-cane (DQ-14).
- Baseline model: the deck says Random Forest; the hypothesis register still says LightGBM (H-04). Run both or pick one.
- Code licence (MIT or Apache-2.0), needed before the first code milestone.
- Confirm that the company's 8 lakh digitised acres include JDW's 4.5 lakh (speaker notes, slide 8).

## Disk (2026-11-06)

`data/raw/csb` 3.76 GB zip + 5.4 GB unzipped; `data/raw/cdl` 2.06 GB zip + 7.9 GB unzipped; `data/interim` under 0.2 GB; conda environment 2.3 GB.

Previous, longer STATUS: [archive/kit-v1/STATUS_v1.md](archive/kit-v1/STATUS_v1.md).
