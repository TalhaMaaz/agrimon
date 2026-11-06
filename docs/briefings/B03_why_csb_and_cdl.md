---
type: briefing
status: final
tags: [briefing, datasets, csb, cdl, louisiana, phase-r]
phase: R
date: 2026-11-06
---

# B03: Why CSB and CDL, and what we checked in them

This is a snapshot from 2026-11-06, after spikes S01 and S02. Reading time is about 15 minutes. It answers three questions: why these two datasets, what we checked, and why each check mattered. The details are in [S01](../research/spikes/S01_csb_fields.md), [S02](../research/spikes/S02_cdl_labels.md) and the [dataset catalogue](../research/dataset_catalogue.md).

---

## 1. What we needed from the data

The data choice started from the app, not from the datasets. The app must show (product spec, P-1 to P-4):

| Capability | What the data must give us |
|---|---|
| P-1 field polygons on a map | real field shapes, for past years **and** a recent year (for the live health layer) |
| P-2 crop type per field | a label per field per year, ideally including sugarcane, over several years (to train on some years and test on others) |
| P-3 health per field | many years of history per field (to learn the "normal" curve), plus documented events (hurricanes, freezes) to test against |
| P-4 yield | yield statistics for the same area and years |
| all | a licence that allows a thesis and published maps |

So the question wasn't "which dataset has sugarcane?" but **"which region has all of this at once?"**

## 2. Why the US stack won

Four candidates were compared on 2026-10-27:

| Candidate | Fields | Sugarcane labels | Years | Recent polygons | Yield | Verdict |
|---|---|---|---|---|---|---|
| **US: CSB + CDL (Louisiana)** | yes, annual | yes | 2008–2025 | yes, to 2025 | state level confirmed (parish still to check) | **chosen** |
| La Réunion (France) | probably | yes, farmer-declared | annual | probably | unverified | parked: parcel-level access couldn't be confirmed |
| Brazil-Crop | 5,477 fields | yes, ground survey | two seasons per region (2020–21) | no | unverified | too few years; no recent fields |
| EuroCrops / France | yes, annual | **no sugarcane** | many | yes | unverified | fallback only |

The US stack was the only one where we could **verify** every row. It is also **public domain**: no limits on the thesis, maps or later use.

## 3. Why two datasets, not one

```
 farmers report their crops to USDA (FSA)   <- the closest thing to ground truth (confidential)
          | used to train and test
          v
 CDL: a crop map, one 30 m pixel = one crop code, every year      (made by a classifier)
          | 8 years of CDL grouped into shapes with the same crop history
          v
 CSB: field polygons, each with a crop label for each of 8 years  (made by an algorithm)
```

| | CSB | CDL |
|---|---|---|
| What it is | field **shapes** with 8 years of labels | a **pixel** map of crops, one per year |
| What it gives us | the fields our app draws, classifies and monitors | the detail behind each label, and USDA's published accuracy |
| Its weakness | each label is only the **majority** class in the field; shapes are smoothed | knows nothing about fields |

The app works per field, so we need the CSB. The CSB's labels are just summaries of the CDL, so we need the CDL to check them and to know how accurate they are.

## 4. What we checked, and why

### 4a. Before downloading

| Check | Result | Why it mattered |
|---|---|---|
| **Licence** | Both: "public domain and free to redistribute" (read in each file's own metadata) | Rule 10: no dataset is used before its licence is recorded. Public domain means no restrictions on the thesis or later use |
| **CDL sugarcane accuracy** (USDA metadata, checked against farmer reports) | Louisiana: producer's accuracy 94.1–95.0 %, user's accuracy 95.8–96.4 % (2020, 2022, 2023) | The labels come from a model, so we needed proof that the model is good for **sugarcane** specifically, not just overall |
| **Years available** | CSB editions to 2018–2025; CDL every year | Several years are needed for honest testing and for health baselines |

What the accuracy numbers mean:
- **Producer's accuracy:** of the real cane, how much did the CDL find?
- **User's accuracy:** of what the CDL calls cane, how much really is cane?

### 4b. S01: the CSB fields (Iberia parish)

| Check (rule set before looking) | Result | Why it mattered |
|---|---|---|
| ≥ 1,000 cane fields every year | ✅ lowest year 3,963 | Enough fields to train on some years and test on others |
| Median cane field ≥ 0.5 ha (50 Sentinel-2 pixels) | ✅ 4.65 ha, about 465 pixels | Fields must be big enough for the satellite to see clearly, without the edges dominating |
| A label for every field in all 8 years | ✅ none missing | A missing year can't be used for training or testing |
| Area stated vs area of the shape | ✅ ratio 1.0000 | A cheap check that the file is internally consistent |

What S01 also revealed:
- **The cane cycle shows in the data:** usually 3–4 years of cane, then a fallow year. Sugarcane can't be treated as a yearly crop.
- **In Iberia, most "non-cane" fields are fallow cane land.** A cane vs non-cane model could look better here than it really is, so we may need a second, more mixed parish.
- **The field shapes are smoothed by USDA's algorithm,** not surveyed.

### 4c. S02: the CSB labels against the CDL pixels

| Check (rule set before looking) | Result | Why it mattered |
|---|---|---|
| Median "cane" field is ≥ 90 % cane pixels | ✅ 94.9 % | A "majority" label could mean 51 % cane; we needed to know how mixed fields really are |
| ≥ 90 % of cane fields are at least 70 % cane | ✅ 94.9 % of fields | Few badly mixed fields means the labels are usable as they are |
| ≥ 80 % of the CDL's cane falls inside CSB fields | ✅ 87.3 % | The polygons must cover most of the crop, or the map would miss cane |
| Do the two datasets line up? | ✅ same coordinate system; cane pixels sit inside the outlines | Misaligned data would put labels on the wrong fields |

What S02 also revealed:
- **The impurity is at the field edges.** After shrinking every field by one pixel (30 m), the typical cane field is **100 %** cane. So when we read Sentinel-2 values, we shrink each field inward first.
- **The CSB label matches our own pixel count for 99.5 % of fields.** That is expected, since both come from the CDL, so it shows the files are consistent, not that the labels are true.

## 5. What these checks do NOT prove (say this in the defence)

1. **The labels are model output, not ground truth.** The best evidence of truth is USDA's own accuracy check against farmer reports, measured per pixel.
2. **Circularity.** The CDL was made partly from **Sentinel-2**, the same satellite our model uses. So our model partly learns to copy another Sentinel-2 model. We state this, and plan to compare against an independent sugarcane map (Di Tommaso 2024) that wasn't trained on the CDL.
3. **One parish, one year (2023) for the purity check.** Other years and parishes are not yet checked.
4. **CSB fields are approximations.** A "field" can merge several real fields that share a history.

## 6. What's next

| Spike | Checks |
|---|---|
| S03 Sentinel-2 | Can we get imagery for these fields, how cloudy is Louisiana, and does cane look different from other land over the year? |
| S04 yield | Do yield figures exist per parish, or only per state? |

## 7. Check yourself

1. Why couldn't we use the CDL alone for our app?
2. Why couldn't we use the CSB alone, without checking against the CDL?
3. What do "producer's accuracy" and "user's accuracy" each tell you?
4. Why does 99.5 % agreement between CSB and CDL **not** show that the labels are correct?
5. Why did we shrink fields inward, and what did that show?

## 8. Questions and answers

(Your questions go here.)
