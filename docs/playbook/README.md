---
type: index
status: living
tags: [playbook, pakistan, standards]
---

# Playbook: standards that transfer to Pakistan

Why this exists: Stage 1 builds the full application on a country with good open data. The point is to learn how this kind of system is built properly, so that Stage 2 (Pakistan, end of the FYP) and any later product start from known standards instead of guesses. See [PROJECT_CONTEXT section 1a](../agent/PROJECT_CONTEXT.md).

## Rules

- One note per stage of the lifecycle (table below), created when the first real lesson exists. No empty placeholder notes.
- Each entry has four parts: **the standard** (what good practice is), **evidence** (verified paper, spec or tool docs, linked to `references.bib` or the paper notes), **what we did in Stage 1**, and **Pakistan transfer** (works as is / needs change / doesn't transfer, and why).
- Written when a phase finishes, from the lab notebook, ADRs and paper notes. It summarises them and doesn't replace them.
- Startup-only topics (sales, pricing, company setup) are out of scope.

## Lifecycle

```
 data sourcing -> labels & field boundaries -> imagery & features -> modelling
       |                                                               |
       v                                                               v
 licences & terms <- serving & web map <- MLOps & monitoring <- validation
```

| Stage | Note | Fed by |
|---|---|---|
| Data sourcing and licences | (not yet) | Phase R dataset search, `DATASET_DISCOVERY.md` |
| Labels and field boundaries | (not yet) | Dataset audit, label adapter (#10, #11) |
| Imagery and features | (not yet) | Imagery pilot (#12) |
| Modelling | (not yet) | Baselines, deep models (#13) |
| Validation without our own ground truth | (not yet) | Spatial-block validation, Module B gate B0 |
| MLOps, pipelines, near-real-time | (not yet) | Module B |
| Serving and web map | (not yet) | Module A export, web app |
| Ground-truth collection (Pakistan) | (not yet) | `DATASET_DISCOVERY.md` section 8 |
