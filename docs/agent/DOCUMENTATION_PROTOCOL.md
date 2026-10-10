# DOCUMENTATION PROTOCOL

The repository is the single source for the thesis and the viva. It will be used across many sessions over a long stretch, so documentation must let a fresh session (or the user after a break) pick up without loss.

All documentation is Markdown in formal academic English, readable by someone who was not in the room.

## 1. Development-project framing (no research questions)

Use these instead:

- **Requirements** (`docs/requirements/requirements_register.md`): ID (R-A-01, R-B-01, ...), statement, priority (must, should, could), rationale, acceptance criterion, verification method (test, experiment, demo, review), status. Numeric performance targets are agreed with the user after baselines exist; do not invent them.
- **Design studies** (`docs/requirements/design_studies/DS-X-NN-<slug>.md`): an engineering comparison that justifies a design choice. Template: decision to make; options; evaluation criteria agreed in advance; experiment IDs; results; decision; link to ADR. Examples: random versus spatial validation, model family, temporal resolution, parcel buffer, class granularity.
- **Verification matrix** (`docs/requirements/verification_matrix.md`): requirement to evidence (test, experiment, figure). Generated or updated each phase.

## 1b. Note format (Obsidian-compatible)

All notes in `docs/` start with YAML frontmatter (`type`, `status`, `tags`, plus `module`, `phase`), link to each other with standard relative Markdown links, and use ASCII diagrams. `docs/` is opened as an Obsidian vault by the user; templates are in `docs/_templates/`. Pandoc and GitHub must still render everything, so no wikilinks and no plugin-only syntax.

## 2. Phase Exit Rule

A phase is not finished until all of these exist and are committed:
1. Phase report `docs/phase_reports/<module>_NN_<name>.md`: Objective; Rationale (why this step, why now); Method; Implementation (modules, commands); Results (numbers with experiment IDs); Problems and fixes; Limitations; Decisions (ADR links); Open questions; Thesis mapping (chapter and section).
2. Lab-notebook entry.
3. ADRs for every non-trivial decision.
4. Updated experiment registry, requirements status, verification matrix, assumptions register, risk register, glossary, understanding ledger.
5. Draft of the matching thesis section.
6. Concept notes and walkthroughs for everything new.
7. Passing tests and a clean `make` of figures and tables.

## 3. Document inventory

| Path | Purpose |
|---|---|
| `docs/STATUS.md` | Living state: current module and phase, done, in progress, next steps, open decisions, blockers, disk and compute used. Updated at the end of every session. |
| `docs/00_project_charter.md` | Problem, motivation, the three modules, scope and out-of-scope, objectives, success criteria, constraints, stakeholders. |
| `docs/requirements/` | Requirements register, design studies, verification matrix. |
| `docs/architecture/` | `design_questions.md`, `hypothesis_register.md`, `architecture_dossier.md` (Phase R), `overview.md`, `interfaces.md` (data contracts between modules), `data_flow.md` (ASCII diagrams), `deployment.md`. |
| `docs/decision_log/ADR-NNNN-<slug>.md` | One per decision. Context; options with pros and cons; decision; rationale; consequences; evidence; status; date. Never overwrite: supersede with a new ADR that links back. |
| `docs/phase_reports/` | One per phase. |
| `docs/lab_notebook/YYYY-MM-DD.md` | Per session: what, why, commands, outputs, surprises, next. |
| `docs/experiments/` | `registry.md` (generated from the tracker) and one `<MODULE>-EXP-NNNN.md` per experiment: goal, config and hash, git commit, data version, seeds, metrics, plots, conclusion, requirement or design study served. |
| `docs/research/` | `search_log.md`, `synthesis_matrix.md`, `papers/` (one note per paper), `dataset_catalogue.md`, `datasets/<id>.md`, `related_work.md`, `unverified_references.md`. |
| `docs/data/` | `data_dictionary.md`, `licences.md`, `lineage.md` (counts retained and dropped at each step, with reasons). |
| `docs/concepts/` | One explainer per key concept: definition, intuition via programming analogy, why used here, alternatives with pros and cons, pitfalls, references. |
| `docs/learning/` | Curriculum, lessons, walkthroughs, quizzes, understanding ledger, user's notes. See TEACHING_PROTOCOL. |
| Registers | `assumptions_register.md`, `risk_register.md`, `claims_register.md`, `threats_to_validity.md`, `glossary.md`. |
| `docs/defence/` | `viva_questions.md`, `demo_script.md`, `slide_outline.md`, `limitations_and_future_work.md`. |
| `docs/thesis/` | Chapters, bibliography, figures, tables, build output. |
| `docs/reproducibility.md`, `docs/CHANGELOG.md` | Clean-machine instructions; dated list of notable changes. |

## 4. Figures and tables

Produced only by scripts in `src/agrimon/reporting/` via `make figures` and `make tables`. Vector (PDF or SVG) plus 300 dpi PNG, colour-blind-safe palettes, labelled axes with units, captions in sidecar files, stable IDs referenced by the thesis and the claims register.

## 5. Claims discipline

Every quantitative or qualitative claim intended for the thesis is entered in `claims_register.md` with its evidence pointer (experiment, figure, table, citation). No claim enters the thesis without an entry. Where evidence does not exist, the draft carries `TODO(EVIDENCE: what is missing)`.

## 6. References

Only verified references enter `references.bib`. Verify title, authors, year, venue and DOI from the source. Otherwise list in `docs/research/unverified_references.md`. Never fabricate citations.

## 7. Thesis structure (Pandoc-ready Markdown; adapt to the university template at Checkpoint 0)

1. Introduction (problem, motivation, objectives, contributions, structure)
2. Background (remote sensing, crop phenology, ML concepts used)
3. Related work (datasets, crop classification, crop monitoring, yield prediction)
4. Requirements and analysis (requirements register, constraints, design studies method)
5. System architecture and data (modules, contracts, datasets, licences, lineage)
6. Module A: crop classification (design, implementation, evaluation)
7. Module B: crop health monitoring
8. Module C: yield prediction (or feasibility study if the gate fails)
9. Integration and web platform
10. Evaluation and discussion (requirement verification, threats to validity, lessons learned)
11. Conclusion and future work

Draft each section right after its phase finishes. Complete prose with citation keys and figure references. Do not write conclusions the evidence does not support. The university accepts a Word thesis. Draft in Markdown, build DOCX with Pandoc using a `--reference-doc` template that carries the university's styles (headings, fonts, margins), a CSL file for the citation style, and `citeproc` with `references.bib`. Pandoc will not fully reproduce a cover page, automatic table of contents, page numbering or caption numbering; finish those by hand in Word in the final week and keep the Markdown as the source of truth until then. Alternative: write directly in Word late in the project, pasting from Markdown (simpler, but loses regenerable figures and citations). Ask at Checkpoint 0 for the university's Word template.

## 8. Long-project maintenance

- **Weekly:** review `STATUS.md`, risk register, roadmap versus reality. Report slippage plainly and propose re-planning.
- **Monthly:** documentation audit. Check that ADRs match the code, claims have evidence, links work, the registry is current, and `reproducibility.md` still works on a clean clone.
- **Versioning:** tag checkpoints and module milestones. Record dataset versions and checksums in `configs/` and `docs/data/`. When a design changes, supersede the ADR and note the change in `CHANGELOG.md` with the reason.
- **Experiment IDs** are prefixed by module (A-EXP-0001, B-EXP-0001, C-EXP-0001) and never reused.
- **Threats to validity** are updated whenever a new dataset, region or module is added.
- **Viva questions** are extended each phase with questions that phase would provoke, each answered with evidence pointers.

## 9. Honesty in documentation

Record what failed and why. A defence is stronger when the student can explain mistakes. Separate observation (what the data showed) from interpretation (what we think it means).
