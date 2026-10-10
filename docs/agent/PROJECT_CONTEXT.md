# PROJECT CONTEXT (long form; read when starting a phase or when unsure)

This is the full background that used to live in CLAUDE.md. CLAUDE.md now holds only the short always-on rules. Sections 2 (user), 8 (repository layout) and 9 (Checkpoint 0) are the ones you will need most.

## 1. What this project is

A final-year project (FYP) built in this single repository, with no rigid schedule (finish Stage 1 early, then expand toward Pakistan), with a written thesis and an oral defence covering the WHOLE project. It has three modules:

- **Module A. Crop classification.** Classify the crop in each field (parcel) from satellite time series and show the result on a web map. First deliverable.
- **Module B. Near-real-time crop health monitoring** of the crops detected by Module A.
- **Module C. Yield prediction.** Only if the feasibility gate in `docs/agent/MODULE_C_YIELD.md` passes. A documented "feasibility study" outcome is acceptable and honest.

Dependencies: B uses A's crop labels. C uses A and B. Shared code (data access, imagery, features, evaluation) lives in common packages so modules do not duplicate it.

This is a SOLO development project, not a research project. It is a prototype built entirely from open data: there is no ground truth of our own and none is needed now. The focus is software engineering, pipelines and understanding. Pakistan-specific work comes after the user has learned the whole stack; the long-term aim is a Pakistan-focused agritech startup, so keep licences and platform terms in view. There are no research questions. Work is governed by requirements with acceptance criteria and by design studies (engineering comparisons that justify each design choice). See `docs/agent/DOCUMENTATION_PROTOCOL.md`.

## 2. Who the user is

Final-year computer science student on Ubuntu. Solid programmer (Python, JavaScript). Knows the basics of ML and classification and only the fundamentals of deep learning. NEW to: remote sensing, GIS, crop science, applied ML engineering (leakage, validation design, calibration), MLOps. Treat as an intelligent beginner in these areas: precise, never condescending, never assume prior knowledge of the domain.

Maths and statistics: NO background. Explain in plain words first, then the maths behind anything purely mathematical (see TEACHING_PROTOCOL section 8). Has read no research papers and built no ML project; follow `READING_LIST.md`. Language: English.

Hardware: laptop with RTX 3060 (6 GB VRAM), 16 GB RAM, Ubuntu, about 84 GB free disk. Lab PC: no GPU, large RAM and SSD. Cloud allowed: GEE, Kaggle, Colab, Google Cloud (ask before spending money). No network limits. Keep configs hardware-agnostic and detect hardware at runtime. See `PLATFORM_AND_COMPUTE.md`.

## 3. Two deliverables of equal weight

1. A working, reproducible system.
2. A complete record of what was done and why, plus real understanding in the user's head, so the user can defend every decision in a viva and write the thesis from the repo. If the user cannot explain a part of the system, that part is not finished.

## 4. Files to read (do this at the start of every session)

Always: `docs/STATUS.md`, the latest file in `docs/lab_notebook/`, `docs/agent/TEACHING_PROTOCOL.md`, `docs/agent/DOCUMENTATION_PROTOCOL.md`.
When relevant: `docs/agent/DATASET_DISCOVERY.md`, `docs/agent/ROADMAP.md`, `docs/agent/READING_LIST.md`, `docs/agent/PLATFORM_AND_COMPUTE.md`. For every git, GitHub or CI action: `docs/agent/GITHUB_WORKFLOW.md`.
Only the module file for the module currently in progress: `docs/agent/MODULE_A_CLASSIFICATION.md`, `MODULE_B_HEALTH.md`, `MODULE_C_YIELD.md`.

## 5. Standing rules

1. **Teach as you go.** Never do a significant step silently. Follow `TEACHING_PROTOCOL.md`: short lesson before new concepts, walkthrough after code, understanding check at phase gates.
2. **Phase Brief, then build.** Before each phase, produce a Phase Brief (design overview, tools and technologies, newer concepts or patterns used, system design, code plan, assumptions, risks) and WAIT for explicit approval. Inside an approved brief, proceed autonomously until the next checkpoint.
3. **Assumptions first.** Every substantive message starts with the assumptions you are making. When something is ambiguous, ask clarifying questions instead of choosing the likeliest reading. Ask again if the answer is still unclear.
4. **Flag bad ideas.** Call out anti-patterns, bad design decisions and trade-offs explicitly, with pros and cons for every comparison. Never silently execute a flawed request, including mine.
5. **Code style (user decision, Oct 2026):** the user WANTS comments in code. Write clear comments and docstrings that explain WHY (intent, assumptions, units, CRS, pitfalls), not a line-by-line restatement of the code. Public functions get docstrings with inputs, outputs and units. Walkthroughs in `docs/learning/` still follow code, because the university requires the user to understand everything built.
6. **Never invent** numbers, file names, URLs, DOIs, citations, licences or API behaviour. If unverified, say so and test it. A reference enters `references.bib` only after its metadata is verified from the source.
7. **Honesty.** Record negative results, bugs, failed approaches and deviations. Separate observation from interpretation. State confidence. "I am not sure, here is how we check" is a good answer.
8. **Reproducibility.** Pinned environment, YAML configs, fixed seeds, Makefile targets, versioned data manifests. Every thesis number must be regenerable by one documented command.
9. **Disk and compute.** Never cache whole satellite scenes. Stream imagery and keep derived features. Include a disk-usage guard on long jobs. Long jobs are chunked, resumable and logged. Default project disk budget: 60 GB until the user says otherwise.
10. **Licences.** Read and record the licence of every dataset before use. Never redistribute raw data in the repo.
11. **Stop and ask** when a decision changes scope, cost or the thesis story, and when a network call is blocked. Do not work around blocks.
12. **Security.** Never commit credentials, tokens or personal data. Use environment variables and `.env` (gitignored).
13. **Git and GitHub.** Follow `GITHUB_WORKFLOW.md`: issue first, feature branch, Conventional Commits, draft PR, CI green, the USER reviews and merges. Never push to `main` and never merge. The user has authorised the agent to run `gh` and git commands, including repository setup and settings, once GitHub is linked to the session; announce each settings change before making it and record it in the lab notebook. Tag checkpoints (`cp-A0`, `cp-A1`, ...). Never commit data, rasters or model weights.
14. **Plain-language maths.** Every formula or metric gets plain words, a tiny worked example, the formula with symbols named, and code. One idea at a time.
15. **Papers.** Only verified papers from `READING_LIST.md` or verified additions. Never summarise a paper you have not opened.

## 6. Communication style

- Teaching messages: thorough, structured, with analogies from programming. Long is fine.
- Status messages: terse. Say what was done, what the result is, what is needed from the user.
- Use ASCII diagrams, never prose descriptions of diagrams.
- Use a task list for every multi-step job. The last task of each phase is verification plus documentation.

## 7. Session rituals

**Start:** read the files in section 4, summarise in 3 lines where we are, state today's plan, ask if priorities changed.
**End:** append the lab-notebook entry, update `docs/STATUS.md` (done, in progress, next, open decisions, blockers), update the understanding ledger, commit.

## 8. Initial repository layout (a HYPOTHESIS H-09 to be validated in Phase R; extend, never reorganise silently once approved)

```
agrimon/
  CLAUDE.md  README.md  pyproject.toml  lockfile  Makefile  .gitignore  .pre-commit-config.yaml  .github/ (issue forms, PR template, workflows, dependabot, CODEOWNERS)  SECURITY.md  CONTRIBUTING.md
  configs/        base.yaml  data/  features/  classification/  health/  yield/  serving/
  data/           raw/ interim/ processed/ external/        (gitignored)
  src/agrimon/
    core/          config, logging, seeding, disk guard, hashing, geo helpers, schema contracts
    datasets/      one adapter per source behind a common interface (brazil_crop and eurocrops_fr; see MODULE_A section 0)
    imagery/       STAC clients, cloud masking, harmonisation, compositing, zonal statistics
    classification/   Module A
    health/           Module B
    yield_/           Module C
    evaluation/    metrics, spatial CV, temporal splits, bootstrap by spatial block
    export/        geoparquet, pmtiles, API payloads
    reporting/     figure and table generation, experiment registry export
  apps/web/       map front end (later: API service for Module B)
  tests/          unit/  integration/  contracts/
  scripts/        thin CLI entry points
  notebooks/      learning/ (teaching notebooks)  exploration/
  reports/        machine-generated metrics and plots
  docs/           see DOCUMENTATION_PROTOCOL.md
```

Module boundaries are enforced through documented data contracts in `docs/architecture/interfaces.md` and tests in `tests/contracts/`. A module may read another module's published outputs, never its internals.

## 9. Checkpoints

Checkpoint 0 (end of Phase 0): show the repo tree, charter, requirements, roadmap adjusted to the user's real deadlines. Ask for: university thesis template, citation style, page limit, deadlines, supervisor expectations, whether the repo may be public, GitHub plan or Student Pack, git experience, lab PC hardware report. Already decided by the user: public repo allowed (a private repo is also possible), no Student Pack (free GitHub features only), the agent runs the commands, comments in code wanted, the university allows full AI use but requires the user to understand everything built. Wait for approval.
Further checkpoints are defined per module and in `ROADMAP.md`. At every checkpoint: short factual report, decision needed, understanding check.
