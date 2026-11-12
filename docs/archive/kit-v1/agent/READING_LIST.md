# READING LIST (curated, ranked, with honest verification status)

Purpose: the papers and resources that explain how this project should be carried out and what the standard practice is at each step, so that Stage 2 (Pakistan, end of the FYP) can be planned from evidence (see PROJECT_CONTEXT section 1a). Papers read get notes good enough to reuse without re-reading. The user has read no papers yet, so this list is ordered as a path, not a pile.

## 0. How to read this file

Verification column meanings:
- **Landing page seen**: the title, authors/venue and link were confirmed from a landing page or index during kit preparation. Volume, pages and DOI must still be confirmed by the agent before the item enters `references.bib`.
- **Title and link only**: a search result showed this title and link. Content, region and claims are NOT verified. The agent must open it and confirm before relying on it.
- **Not yet verified**: believed to exist from general knowledge; no link was confirmed. The agent must find and verify it or drop it.

Rule for the agent (CLAUDE.md rule 6): nothing enters `references.bib` until its metadata is verified at the source. Any item below can be wrong in detail.

How to read a paper as a beginner (the agent teaches this at the first reading session): abstract, then figures and tables, then conclusion, then introduction, then methods. Aim for "what problem, what data, what method, what result, what limits" in five lines. Write those five lines in `docs/learning/my_understanding/papers/`.

## 1. Tier 1: read first (the spine of the project)

| # | Item | Why it matters | Verification |
|---|---|---|---|
| 1 | Drusch et al. 2012, "Sentinel-2: ESA's Optical High-Resolution Mission for GMES Operational Services", Remote Sensing of Environment, DOI 10.1016/j.rse.2011.11.026 | The satellite you will use for everything: bands, resolution, revisit | DOI and venue seen via Crossref result |
| 2 | Pelletier, Webb, Petitjean 2019, "Temporal Convolutional Neural Network for the Classification of Satellite Image Time Series", Remote Sensing 11(5):523, arXiv 1811.10166 | The simple deep model (TempCNN) used as the main neural baseline; shows why time matters more than space for crops | Landing pages seen (MDPI, arXiv) |
| 3 | Roberts et al. 2017, "Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure", Ecography, DOI 10.1111/ecog.02881 | Why random train/test splits lie on geographic data, and what to do instead. Single most important evaluation paper for this project | Landing pages seen |
| 4 | Olofsson et al. 2014, "Good practices for estimating area and assessing accuracy of land change", Remote Sensing of Environment, DOI 10.1016/j.rse.2014.02.015 | How to report map accuracy honestly, and why area estimates need correction | DOI and venue seen via Crossref result |
| 5 | Weiss, Jacob, Duveiller 2020, "Remote sensing for agricultural applications: A meta-review", Remote Sensing of Environment | Map of the whole field: what works, what does not, across crop type, health, yield | Landing pages seen (HAL, JRC). Volume and pages to confirm |
| 6 | Garnot et al. 2020, "Satellite Image Time Series Classification with Pixel-Set Encoders and Temporal Self-Attention", CVPR 2020, arXiv 1911.07757 | Attention models for crop time series; introduces the PASTIS-line of work | Landing pages seen (arXiv, CVF) |

## 2. Tier 2: datasets and benchmarks (read when you reach the matching phase)

| Item | Why | Verification |
|---|---|---|
| "EuroCrops: The Largest Harmonized Open Crop Dataset Across the European Union", Scientific Data (Sep 2023); arXiv 2302.10202; PMC10495462 | Reference example of how a good open crop-label dataset is built and documented; the benchmark for the France pipeline-proving run. Authors to be read from the landing page | Landing pages seen (PMC, arXiv, DOAJ) |
| "CropHarvest: a global satellite dataset for crop type classification", NeurIPS 2021 Datasets and Benchmarks | Global, small, pixel-level; useful for transfer to Pakistan-like regions; shows what low-data crop mapping looks like | PDF link seen at NeurIPS proceedings; authors to be read from the PDF |
| "Fields of The World: A Machine Learning Benchmark Dataset For Global Agricultural Field Boundary Segmentation", arXiv 2409.16252 | Field boundary segmentation benchmark across many countries; relevant for the future step "find the field boundaries yourself", which Pakistan will need because open polygons are scarce | Landing page seen; authors to confirm |
| Oldoni, Kuhl, Prudente, Sanches, Mercante, Queiroz et al. 2026, "Brazil-Crop dataset: a benchmark for agricultural remote sensing applications", Zenodo, DOI 10.5281/zenodo.18461147 (CC BY 4.0) | The primary dataset recommended for the Brazil target (see DATASET_DISCOVERY) | Landing page read; see section 5 of that file |
| Zheng, Luciano, Dong, Yuan 2022, "High-resolution map of sugarcane cultivation in Brazil using a phenology-based method", Earth System Science Data 14:2065-2080, Figshare DOI 10.6084/m9.figshare.14213909 | 30 m sugarcane maps for 2016 to 2019, 91.47 percent overall accuracy for 2018. Use as an independent cross-check, not as training truth | Landing page read |

## 3. Tier 3: Pakistan and South Asia (read before designing the Pakistan phase)

Honest status: I found these through search and saw only their titles and links. Do not quote claims from them until the agent has opened and verified each.

| Item | Why it might matter | Verification |
|---|---|---|
| "Early Identification of Crop Type for Smallholder Farming Systems Using Deep Learning on Time-Series Sentinel-2 Imagery", Sensors 2023, 23(4):1779, DOI 10.3390/s23041779 | Smallholder setting with early (in-season) identification; check the study region before using it as a Pakistan reference | Title and link only |
| "A comprehensive deep learning approach for harvest ready sugarcane pixel classification in Punjab, Pakistan using Sentinel-2 multispectral imagery", ScienceDirect S2352938524000892 | Directly about sugarcane in Punjab | Title and link only |
| "Crop type classification in smallholder agriculture of central and South Asia using Sentinel-1/2 data fusion", ScienceDirect S2352938526001400 | Radar plus optical for South Asian smallholders | Title and link only |
| Pakistan Zenodo crop archive (record 22806700, noted in earlier research) | Possible Pakistan labels | Not yet verified; may be a wrong ID. Agent must find and verify |

## 4. Tier 4: later modules (read at gates B0 and C0)

| Item | Why | Verification |
|---|---|---|
| Schwalbert et al., satellite-based soybean yield forecast with machine learning and weather data in southern Brazil (2020) | A Brazil yield-forecasting example with satellite plus weather features; shows realistic error sizes | Search results only pointed to related Brazil soybean work (TUM, IBM, arXiv 1806.09244). Exact paper not confirmed. Not yet verified |
| Garnot et al., L-TAE, "Lightweight Temporal Self-Attention for Classifying Satellite Image Time Series" | Smaller attention model suited to a 6 GB GPU | Code repository seen (VSainteuf/lightweight-temporal-attention-pytorch); paper metadata not confirmed |
| Guo et al. 2017, "On Calibration of Modern Neural Networks", ICML | Why predicted probabilities are often overconfident, and temperature scaling | Not yet verified |
| Rußwurm and Körner, self-attention for raw optical satellite time series classification (BreizhCrops line of work) | Another baseline family, plus a regional benchmark idea | Not yet verified |
| Veloso et al. 2017, Sentinel-1 and Sentinel-2 for crop monitoring | Why radar helps under cloud, which matters for tropical Brazil and monsoon Pakistan | Not yet verified |
| Picoli et al. 2018, big earth observation time series for land use mapping in Mato Grosso, Brazil | Brazilian time-series classification practice | Not yet verified |
| Rudorff et al. 2010, Canasat sugarcane monitoring in São Paulo | Brazilian sugarcane mapping history | Not yet verified |
| Wadoux et al. 2021 and Ploton et al. 2020, spatial autocorrelation and map validation | Deeper treatment of why spatial validation matters | Not yet verified |

## 5. Beginner foundations (maths, statistics, ML)

You said you have no maths or statistics background. These are the standard, free or widely available resources I could confirm.

| Rank | Resource | Use | Verification |
|---|---|---|---|
| 1 | An Introduction to Statistical Learning (ISL), free PDF on statlearning.com; editions: R 1st (2013), R 2nd (2021), Python "ISLP" (2023) | Best plain-language treatment of classification, overfitting, cross-validation, regression. Use the Python edition | Site read; three editions with free PDFs confirmed |
| 2 | Dive into Deep Learning (d2l.ai), version 1.0.3 at time of reading; PyTorch, JAX, TensorFlow and MXNet versions; runnable in Google Colab | Fills the gap between "fundamentals of deep learning" and TempCNN and attention | Site read |
| 3 | NASA ARSET "Fundamentals of Remote Sensing" (earthdata.nasa.gov/learn/trainings/fundamentals-remote-sensing) | Self-paced online course, about 2 hours, English and Spanish; needs a free ARSET account; the page did not mention videos or slides | Page read |
| 4 | 3Blue1Brown, linear algebra topic | Visual intuition for vectors and matrices | Topic page exists on the 3Blue1Brown site; the exact series chapter count was not confirmed |

The agent teaches the needed maths inside the project (see TEACHING_PROTOCOL section on plain-language maths). Courses are optional support, not prerequisites.

## 5b. Courses, tutorials and videos (you prefer reading, and like video)

| Rank | Resource | What it gives you | Verification |
|---|---|---|---|
| 1 | ARSET Fundamentals of Remote Sensing (above) | The remote sensing vocabulary in one sitting | Page read |
| 2 | "Geospatial Data Analysis with Python", University of Washington CEE467/CEWA567 Jupyter Book (David Shean; 2024 instructor Eric Gagliano), uwgda-jupyterbook.readthedocs.io | Free notebooks: shell and git, NumPy, pandas, Matplotlib, GeoPandas and CRS, rasters with rasterio, xarray, Dask. Exactly the Python libraries this project uses. Content CC BY-SA 4.0, code MIT. Public notebooks have blank cells for students | Page read |
| 3 | Microsoft Planetary Computer example notebook for Sentinel-2 L2A (PlanetaryComputerExamples on GitHub, viewed via nbviewer) | STAC search with pystac-client, cloud filtering, signing assets, reading a window with rasterio | Page read |
| 4 | odc-stac documentation notebook "Access Sentinel 2 Data on Planetary Computer" | Loading many Sentinel-2 scenes as one array, which is how we build time series | Link seen in search only; content not read |
| 5 | StatQuest (Josh Starmer) YouTube channel, statistics and machine learning playlists | Plain-language, short videos on averages, variance, probability, cross-validation, gradient boosting, neural nets | Well-known channel; I could not confirm a specific URL or playlist in this session. The agent should find the exact playlists and verify them |
| 6 | 3Blue1Brown YouTube channel, neural networks and linear algebra series | Visual intuition for vectors, matrices and how networks learn | Same: channel known, exact series links not verified |

How to combine them: ISL or d2l chapters for the idea, a StatQuest video for the intuition, the UW notebooks for the library, then the project step that uses all three. The agent teaches each Python library the first time it appears (see TEACHING_PROTOCOL section 10).

## 6. Suggested reading order

```
Week 1-2   Drusch 2012 (skim)      -> what the satellite gives you
Week 2-3   ISL chapters on classification and resampling (alongside Phase A-0..A-2)
Week 3-4   Roberts 2017            -> before you design splits (Phase A-2)
Week 5-7   Pelletier 2019          -> before TempCNN (Phase A-5)
Week 7-9   Olofsson 2014           -> before final evaluation reporting
Week 9-11  Garnot 2020             -> attention models
Month 4    Weiss 2020 meta-review  -> big picture, before Module B
Month 4+   Tier 3 Pakistan papers  -> verified one by one
Month 5+   Tier 4 as the gates arrive
```

## 7. Agent tasks for this file

1. At Checkpoint 0, verify every Tier 1 item at the source and create `references.bib` entries.
2. Verify Tier 2 and Tier 3 items as their phases approach; delete any that cannot be verified.
3. Each reading session: summarise in plain English, explain the maths used (section "plain-language maths"), connect it to a design decision in this repo, and record the five-line summary.
4. Keep a short "papers I have actually read" log. Never cite a paper in the thesis that has not been opened.
