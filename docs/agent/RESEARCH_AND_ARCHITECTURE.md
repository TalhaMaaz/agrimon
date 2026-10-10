# RESEARCH AND ARCHITECTURE (Phase R: do this before building)

The architecture, tools, class lists, validation scheme, model families and web stack described in this kit are STARTING HYPOTHESES from a short round of web research. They were not validated and some details may be wrong. Before building, the agent must research properly, read papers, make notes, and design the best architecture it can justify. In the defence the user must be able to prove each choice, so every choice needs evidence the user can point to.

## 1. Principles

1. Hypothesis first, then evidence. A design choice is one of: **hypothesis** (written down, not tested), **validated** (supported by cited papers and/or our own small experiment), **rejected** (with reasons). Nothing is "decided" without a status.
2. The kit's choices (parcel-level classification, Sentinel-2 via STAC, per-parcel time series, LightGBM then TempCNN, spatial block validation, PMTiles map, expected-curve health baselines) are candidates, not instructions. Replace them if the research says something better exists, and say why.
3. Prefer small, cheap spikes over opinions. A day of experiment on a tiny sample beats a week of speculation.
4. Stage 1 builds the full application on open data from a country with good field polygons and labels, but the architecture must anticipate Stage 2 (Pakistan, at the end of the FYP: scarce labels, smallholder fields, monsoon clouds, local ground truth). Ask of each choice: does this survive the move to Pakistan? Record the answer in the hypothesis register's "Pakistan relevance" column.
4a. Standards first. The user's goal is to learn how this kind of system is built properly (PROJECT_CONTEXT section 1a). For each component, find out what the established practice is (in surveys, benchmark papers, specifications, widely used tools), name the source, and prefer it unless the evidence says otherwise. When we deviate, say why.
5. Honest negative results are part of the proof.
6. Verified references only. Read the paper before citing it.

## 2. Phase R workflow

```
 questions list --> literature search --> read + note --> synthesis matrix
        |                                                       |
        v                                                       v
  architecture hypotheses  <---------------------------- evidence per hypothesis
        |
        v
  small spikes (tiny experiments) --> compare alternatives (pros/cons)
        |
        v
  architecture dossier + ADRs  --> Checkpoint R (user approves)
```

**Step 1: Design questions.** Write the list of questions the architecture must answer, for example: what is the unit of classification (pixel, parcel, patch)? Which imagery and which sensors? How to handle clouds in tropical Brazil and monsoon Pakistan? How to split data honestly? Which model families suit small labelled sets? How to calibrate? How to define and validate "health" without ground truth? How to run near-real-time on a laptop and a lab PC? Which web stack for maps and a time slider? How should the system be shaped to be reusable for Pakistan? Which country's open data should Stage 1 use (dataset search, DATASET_DISCOVERY)? For each component, what is the standard practice, and who says so? Keep the list in `docs/architecture/design_questions.md`.

**Step 2: Literature search.** For each question search arXiv, Google Scholar, journals (Remote Sensing of Environment, ISPRS Journal, Remote Sensing, IEEE JSTARS, Earth System Science Data, Scientific Data), benchmark and dataset papers, and project documentation (STAC, Planetary Computer, TorchGeo, etc.). Use forward and backward citation chasing from the seed papers in READING_LIST.md. Record queries and dates in `docs/research/search_log.md`. Prefer recent surveys first to map the field, then specific methods.

**Step 3: Read and note.** For each paper that matters, read it (abstract, figures, conclusion, then methods) and write a note from the template `docs/_templates/paper-note.md` in `docs/research/papers/`. Explain any maths in plain words first. Mark reading depth: skimmed, read, studied. Do not cite what you have not opened. Teach the user the main papers in the TEACHING_PROTOCOL style; the user reads the key ones too.

**Step 4: Synthesis matrix.** `docs/research/synthesis_matrix.md`: rows = design questions, columns = candidate approaches, cells = what the evidence says (with citations), conditions (region, crop, data size), and gaps. Include evidence against the kit's starting choices.

**Step 5: Spikes.** For the highest-risk choices run tiny experiments, each logged as an experiment with a stated question and decision rule: for example, does a parcel-level LightGBM on 100 fields already separate classes? how much do clouds cost in the Brazil study area? does random vs spatial split change scores? is the STAC stream fast enough? Keep spikes small (hours, not weeks). Throwaway code goes in `notebooks/exploration/`; anything reusable is rewritten properly later.

**Step 6: Architecture dossier.** `docs/architecture/architecture_dossier.md`: for each major component, the options considered with pros and cons, the choice, the evidence (papers and spikes), the status (validated, provisional, rejected), the risk, the plan to validate provisional items, and how it carries over to Pakistan. Include ASCII diagrams (system context, data flow, module contracts, deployment). Each decision gets an ADR linking the dossier and the evidence.

**Step 7: Checkpoint R.** Report to the user: what was read, what changed from the kit's hypotheses, what is validated and what is still provisional, the architecture, and the proposed first build steps. Ask the user to approve. Then continue to Phase 0 (repository and workflow) and Module A.

## 3. Hypothesis register

`docs/architecture/hypothesis_register.md`, one row per hypothesis:

| ID | Hypothesis | Source | Status | Evidence | Pakistan relevance |
|---|---|---|---|---|---|
| H-01 | Classify at parcel level using per-parcel aggregated time series | Starting kit | hypothesis | | |
| H-02 | Sentinel-2 L2A through STAC (Planetary Computer) is the primary imagery source | Starting kit | hypothesis | | |
| H-03 | Spatial block validation plus a held-out region/year is needed for honest scores | Starting kit | hypothesis | Roberts et al. 2017 (to be read) | |
| H-04 | LightGBM baseline then TempCNN/attention models are the right model ladder | Starting kit | hypothesis | | |
| H-05 | Radar (Sentinel-1) is needed under cloud | Starting kit | hypothesis | | |
| H-06 | Health is best expressed as deviation from an expected crop curve | Starting kit | hypothesis | | |
| H-07 | A static web map (MapLibre and PMTiles) suffices for the demo | Starting kit | hypothesis | | |
| H-08 | Brazil-Crop is a suitable first dataset | Web research | hypothesis | | |
| H-09 | The repository layout in PROJECT_CONTEXT section 8 is adequate | Starting kit | hypothesis | | |

Add rows as new hypotheses appear. Statuses change only with evidence.

## 4. Defence proof

For the defence, every major choice must be answerable with: what alternatives existed, why this one, what evidence (paper, experiment, spike) supports it, what would change the decision, and what its limits are. The architecture dossier, the hypothesis register, the synthesis matrix and the ADRs are the proof trail. `/viva-drill` questions are drawn from them.

## 5. Anti-patterns

- Treating the kit's suggestions as facts.
- Choosing a technology because it is fashionable (for example a foundation model, a heavy framework, a database) without evidence it solves a problem we have.
- Reading only abstracts and then citing.
- Running large experiments to settle a question a small spike could answer.
- Architecture that cannot work for Pakistan (for example depends on dense open polygons or labelled history).
- Over-engineering: Stage 1 is a prototype; choose the simplest architecture that is defensible and extensible.
- Skipping Phase R "because the kit already decided".
