# AgriMon: crop intelligence platform (working name)

Kit v2 (2026-11-12). The previous, longer rules are in `docs/archive/kit-v1/CLAUDE_v1.md`; the old protocols, module notes and reading list are in `docs/archive/kit-v1/agent/` and are read only when a task needs them.

## Project

Solo final-year project: one repo, a thesis and a viva covering everything.
- **Stage 1 (now):** build the full application on open US data. Decided 2026-10-27: Louisiana, with USDA CSB field boundaries, CDL crop labels, Sentinel-2 imagery and NASS yields.
- **Stage 2 (end of the FYP):** adapt it to the Pakistani data that exists.
- **Module A:** sugarcane (crop type) classification of field parcels from Sentinel-2 time series, on a web map. First deliverable.
- **Module B:** near-real-time crop health against the expected cane cycle. Important to the user.
- **Module C:** yield. Not important; a model or a short feasibility note.
- Demo: replay on old fields (must); present-day fields (stretch).

Why (user, 2026-10-10): the FYP exists to give Talha the skills and standards to build this kind of system end to end. A prototype on open data only: no ground truth of our own. Long-term (context only, not FYP scope): a Pakistan agritech startup selling to sugar mills, so keep licences and platform terms in view.

## User

Talha, final-year CS student, Ubuntu, Python and JavaScript, basic ML. New to remote sensing, GIS, crop science and applied ML engineering; no maths or statistics background. Laptop: RTX 3060 6 GB, 16 GB RAM. Lab PC: big RAM, no GPU, remote. Kaggle and Colab; Earth Engine (noncommercial, university work only). Claude Pro plan: keep sessions focused. The university allows full AI use but requires Talha to understand everything built. English only.

## How we work

- **Session start:** read `docs/STATUS.md` and the latest entry in `docs/LOG.md`. Nothing else unless the task needs it.
- **Claude is the primary developer.** Small things: just do them. Before a big build step: a plan of five lines or fewer in chat, then wait for the user's OK.
- **Teaching only on request.** When the user asks to learn or understand something, teach properly: plain words, a small worked example, then the formula and code. Defence summaries, viva prep and explanations are also on request.
- **Session end (or a natural stopping point):** append an entry to `docs/LOG.md` (date, what was done, decisions and why, numbers and results, problems, next), refresh `docs/STATUS.md`, commit and push the branch. Claude writes these; the user does not have to.

## Rules

1. Architecture, tools, models and class lists are hypotheses until evidence supports them (`docs/design/hypothesis_register.md`). Every design choice needs evidence the user can present at the defence.
2. State assumptions. Ask instead of guessing. Flag bad ideas and trade-offs, including the user's.
3. Never invent numbers, URLs, DOIs, citations, licences or API behaviour. Verify, or say it is unverified.
4. Record negative results and deviations honestly; keep observation and interpretation separate.
5. Code comments explain why (intent, units, CRS, pitfalls); public functions have docstrings.
6. Reproducible: pinned environment, configs, fixed seeds, versioned data.
7. Never cache whole satellite scenes; stream and keep per-field features. Long jobs are chunked, resumable and logged. No fixed disk budget; note disk use in STATUS.
8. Record each dataset's licence before use. Never commit data, rasters, weights, credentials or `.env`.
9. Stop and ask when scope, cost or the thesis story changes, or when a network call is blocked. Do not work around blocks.
10. Git: one branch per milestone (`build/<milestone>`), small Conventional Commits pushed often, one draft PR per finished milestone with green CI. Issues only for real bugs or work the user wants listed. PRs merge with a merge commit (no squash) so commit hashes stay traceable. Never push to `main`, never merge: the user reviews and merges. Announce every repository-settings change.
11. If the user cannot explain a part of the system, that part is not finished.

## Repo map

```
docs/STATUS.md        where we are now
docs/LOG.md           Claude's log of every session
docs/research/        datasets, data checks (spikes), literature, Pakistan playbook
docs/design/          requirements, SRS, product spec, design questions, hypotheses
docs/presentations/   presentation material
docs/learning/        lessons, foundation guides, glossary, briefings
docs/archive/kit-v1/  the old kit (reference only)
notebooks/            exploration notebooks and figure scripts
data/, papers/        local only, never committed
```

Tools: no slash commands or subagents yet (being redesigned; kit v1's are at git tag `kit-v1`). Hooks in `.claude/hooks/` block pushes to `main`, merges, force pushes and commits of data or secrets, and run ruff after Python edits.

## Obsidian

`docs/` is the user's Obsidian vault. Notes Claude writes there start with YAML frontmatter (`type`, `status`, `tags`), use relative Markdown links (no wikilinks) and ASCII diagrams. Never write in `docs/learning/my_understanding/` (the user's own notes).

## Style

Status messages: short (done, result, what is needed from the user). Teaching, when asked: thorough and structured, with coding analogies.
