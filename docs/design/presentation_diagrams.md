---
type: architecture
status: draft
tags: [architecture, phase-r, presentation, diagrams]
phase: R
---

# Diagrams and methodology for the mid-semester presentation (draft, 2026-11-06)

These are the slide 6 and 7 drafts. Everything here is the **proposed** design: the kit's starting hypotheses (H-01 to H-24), not yet approved at Checkpoint R. The slides must say "proposed". ASCII here, redrawn as images for the deck.

## 1. Development methodology

**Iterative and incremental, phase-gated:** an Agile-style flow, adapted for one developer.

```
 Phase R ──> Module A ──> Module B ──> Module C ──> Stage 2 (Pakistan)
 research    crop type    health       yield        adapt and rebuild
    │            │            │            │
    └── each phase: Phase Brief ─> approve ─> build in small issues ─> review ─> gate
```

- **Work items:** GitHub issues; each change on a branch, as a draft pull request, with CI checks (tests, lint, secret scan).
- **Gates:** each phase starts with a written Phase Brief (design, risks, plan) and ends at a gate (checkpoint) with evidence.
- **Why not Waterfall:** the data and the method are uncertain. Spikes (small experiments) settle each design question before building, and a plan that is fixed up front would break at the first data surprise. S01 already changed the plan.

## 2. Workflow (data to map)

```
 ┌────────────┐   ┌────────────┐   ┌──────────────┐
 │ CSB fields │   │ CDL labels │   │ Sentinel-2   │  (Planetary Computer STAC;
 │ (polygons) │   │ (crop map) │   │ L2A imagery  │   Earth Engine optional)
 └─────┬──────┘   └─────┬──────┘   └──────┬───────┘
       └────────┬───────┘                 │
                ▼                         ▼
        1. field + label table    2. per-field time series
           (study parish)            (cloud-masked indices:
                │                     NDVI, red-edge, SWIR)
                └───────────┬─────────────┘
                            ▼
        3. Module A: classify cane / non-cane per field
                            ▼
        4. Module B: compare each field to the expected
           cane-cycle curve and its neighbours -> health flag
                            ▼
        5. Module C: parish yield model or feasibility note
           (checked against NASS statistics)
                            ▼
        6. export per-field results -> web map (crop, health, yield)
```

## 3. Expected system architecture

```
   offline / scheduled (Python)                     delivery (browser)
 ┌─────────────────────────────────────┐        ┌───────────────────────┐
 │ ingestion   STAC client, GEE client │        │ web map (MapLibre)    │
 │      │      (behind one interface)  │        │  - crop layer         │
 │      ▼                              │        │  - health layer       │
 │ feature store  per-field series     │ files  │  - yield layer        │
 │      │        (GeoParquet)          ├───────►│  - date slider        │
 │      ▼                              │ tiles  │  - pop-up: history    │
 │ models  A classify / B health / C   │ (PMTiles)                     │
 │      │                              │        └───────────────────────┘
 │      ▼                              │
 │ exports  per-field predictions      │
 └─────────────────────────────────────┘
   config (YAML), experiment tracking, tests, CI
```

Design rules: imagery access sits behind one interface (STAC by default; Earth Engine optional, because of its noncommercial terms). Imagery is streamed, never stored as whole scenes. Modules exchange data through documented file contracts.

## 4. Use-case diagram (text form)

```
            ┌──────────────────── AgriMon web map ────────────────────┐
            │                                                         │
 Agronomist ├── (view fields on the map)                              │
 / mill     ├── (see crop type per field) ──── includes ── (filter    │
 officer    │                                              low conf.) │
            ├── (see health status and history of a field)            │
            ├── (pick a date or season)                               │
            ├── (see indicative yield per field or parish)            │
            │                                                         │
 Developer  ├── (run the pipeline for a region) ── includes ──        │
 (Talha)    │        (fetch imagery) (classify) (compute health)      │
            ├── (evaluate models on held-out data)                    │
            └─────────────────────────────────────────────────────────┘
 External systems: Sentinel-2 catalogue (STAC), Earth Engine, USDA NASS data
```

## 5. Technology stack (proposed, slide 7)

| Layer | Proposed | Why | Status |
|---|---|---|---|
| Language and data | Python 3.12; geopandas, rasterio, xarray | Standard geospatial Python stack; in use (S01, S02) | in use |
| Imagery access | pystac-client + Planetary Computer (Sentinel-2 L2A); Earth Engine API optional | Free, open catalogue; GEE for bulk extraction under noncommercial terms | PC reachable; GEE login done, project to set |
| Storage | GeoParquet files (+ DuckDB for queries) instead of a database server | Per-field tables are small; no server to run; reproducible | hypothesis (DQ-16) |
| ML | scikit-learn / LightGBM baselines, then PyTorch (TempCNN, attention) | Literature model ladder; fits a 6 GB GPU | hypothesis (H-04, DQ-13) |
| Frontend | MapLibre GL JS + PMTiles (static) | Open-source maps, no API key, no backend | hypothesis (H-07, DQ-15) |
| Environment | conda-forge (mamba), pinned lock file | GDAL, PROJ and GEOS installed together | in use |
| Tools | Git, GitHub (issues, PRs, CI), VS Code, Jupyter, Obsidian, Claude Code | Reviewable history; documented teaching notes | in use |
