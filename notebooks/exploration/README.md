# Exploration notebooks (Phase R spikes)

Throwaway code for Phase R step 5 (`docs/agent/RESEARCH_AND_ARCHITECTURE.md`): small experiments that answer one design question each. Anything reusable is rewritten properly in the real package after Checkpoint R.

- Environment: `environment-spikes.yml` (exact versions in `environment-spikes.lock.txt`).
  Create with `~/miniforge3/bin/mamba env create -f environment-spikes.yml`, open with
  `~/miniforge3/envs/agrimon-spikes/bin/jupyter lab`.
- Data: everything under `data/` (git-ignored). Notebooks never write data elsewhere.
- Results: each spike's question, observation, interpretation and decision go in `docs/research/spikes/`; key figures as PNG in `docs/research/spikes/figures/`.
- Commit notebooks with outputs cleared if outputs contain large images.

| Notebook | Spike | Question |
|---|---|---|
| `01_csb_fields.ipynb` | S01 | What do CSB fields look like in a Louisiana cane parish? |
| `02_cdl_labels.ipynb` | S02 | Do CSB labels match the CDL pixels inside each field? |
| `03_sentinel2.ipynb` | S03 | Is the STAC stream usable, how cloudy is it, do cane NDVI curves differ? |
| `04_yield_stats.ipynb` | S04 | Do parish-level sugarcane yields exist? |
