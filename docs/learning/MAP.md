---
type: map
status: living
tags: [map, start-here]
---

# MAP: where am I, what is this, what do I need to know

This is the human-facing front page of the project. Open it first in Obsidian every working day. The agent keeps the status lines current; you keep the checkboxes honest.

Related: [STATUS](../STATUS.md) | [Weekly rhythm](WEEKLY_RHYTHM.md) | [Obsidian guide](OBSIDIAN_GUIDE.md) | [Understanding ledger](understanding_ledger.md) | [Glossary](../glossary.md) | [Reading list](../agent/READING_LIST.md) | [Roadmap](../agent/ROADMAP.md)

## 1. Right now (agent updates at /session-end)

- Current phase: Stage 1, Phase R (research and architecture), step 1 done in draft (issue #6)
- This week's goal: review design questions and hypothesis register; L01 Sentinel-2; first paper
- Waiting for me: merge PR #18 (CI fix) first, then #20, #16, #14; L00 check questions; code licence choice
- The one concept I must understand this week: how to read a paper ([L00](lessons/L00_how_to_read_a_paper.md))

## 2. The whole system in one picture (a starting hypothesis; the validated version lives in `../architecture/architecture_dossier.md` after Phase R)

```
 OPEN DATA                    PIPELINE                          PRODUCT
 ---------                    --------                          -------
 field polygons  --+
 + crop labels     |   +------------------+
 (Brazil-Crop)     +-->| label adapter    |--> clean parcels + spatial splits
                       +------------------+              |
 Sentinel-2 images --> STAC stream --> cloud mask --> composites --> per-parcel
 (Planetary Computer)                                      time series (parquet)
                                                                |
                      +------------------------+----------------+
                      |                        |
              MODULE A: classify        MODULE B: health
              LightGBM, TempCNN         expected-curve baseline,
              calibrated probabilities  anomaly score, radar, weather
                      |                        |
                      +-----------+------------+
                                  |
                          MODULE C: yield (low priority: feasibility note)
                                  |
                       export (GeoParquet -> PMTiles)
                                  |
                       web map: crop colour, date slider,
                       health layer, popups
```

## 3. Concept map: what to learn, in order

Tick a box only when you could explain it to the examiner without notes (use `/teach-back <concept>`).

### Foundations (before any model)
- [ ] Satellite imagery: Sentinel-2, bands, resolution, revisit, tiles
- [ ] Vector vs raster; coordinate reference systems; GeoParquet
- [ ] Reflectance, clouds, scene classification layer, processing baselines
- [ ] Vegetation indices (NDVI and friends) and crop phenology
- [ ] Parcels as samples, time series as features, labels and label noise
- [ ] Averages, spread, probability, percentages (plain-language maths 1)

### Evaluation (before trusting any number)
- [ ] Confusion matrix, precision, recall, F1, macro vs micro
- [ ] Class imbalance
- [ ] Leakage and spatial autocorrelation; spatial block splits; held-out region
- [ ] Seeds, variance, confidence intervals, bootstrap

### Models
- [ ] Why a baseline comes first; gradient boosting
- [ ] 1D convolutions over time (TempCNN)
- [ ] Attention for sequences
- [ ] Softmax, cross-entropy, gradient descent
- [ ] Calibration and temperature scaling

### Product and engineering
- [ ] In-season prediction (`predict_as_of`)
- [ ] Vector tiles, PMTiles, web maps
- [ ] Git branches, PRs, CI, rulesets, releases
- [ ] Reproducibility: configs, seeds, manifests

### Later modules (B is a priority; C is a short note)
- [ ] Smoothing and gap filling; phenology baselines; anomaly scores
- [ ] Radar basics (Sentinel-1)
- [ ] Validation without labels
- [ ] Regression metrics; leave-one-year-out; prediction intervals

## 4. Reading order (papers)

See [Reading list](../agent/READING_LIST.md). Next unread item: Drusch et al. 2012 (Sentinel-2). Keep five-line summaries in `my_understanding/papers/`.

## 5. Where things live

```
docs/
  STATUS.md                where the project is
  learning/                you are here: map, rhythm, ledger, lessons, your notes
  concepts/                one explainer per key concept
  decision_log/            ADRs: why we chose X over Y
  lab_notebook/            one file per session
  phase_reports/           one per finished phase
  experiments/             one per experiment, plus the registry
  requirements/            requirements, design studies, verification matrix
  defence/                 viva questions, demo script
  thesis/                  chapters
  agent/                   rules for Claude (you rarely need these)
  _templates/              note templates
```

## 6. If I feel lost

1. Run `/session-start` and read the three-line summary.
2. Open the [Understanding ledger](understanding_ledger.md) and pick one "shaky" item.
3. Run `/teach-back <that concept>`.
4. If a diff or file feels opaque, ask the agent for a walkthrough and do not merge until you can explain it.
