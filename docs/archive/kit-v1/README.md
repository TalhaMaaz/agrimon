---
type: archive
status: archived
tags: [kit-v1, archive]
---

# Kit v1 archive

Files from the original project kit that the solo workflow (kit v2, 2026-11-12) no longer uses. Nothing here was deleted; each file was moved unchanged. The full kit v1 state is also kept at git tag `kit-v1`.

| File | Original location | What it was |
|---|---|---|
| `START_HERE.md` | repo root | Overview of the kit and the first message to Claude Code |
| `SETUP_GUIDE.md` | repo root | How the kit was installed (Claude Code, Git, GitHub, Obsidian) |
| `CODE_OF_CONDUCT.md` | repo root | Standard open-source conduct policy |
| `CONTRIBUTING.md` | repo root | Contribution rules for a team project |
| `SECURITY.md` | repo root | Vulnerability reporting policy |
| `devcontainer/devcontainer.json` | `.devcontainer/` | GitHub Codespaces environment recipe (never used) |
| `CLAUDE_v1.md` | `CLAUDE.md` | The kit v1 rules file, as it was just before kit v2 |
| `STATUS_v1.md` | `docs/STATUS.md` | The long kit v1 status page |
| `agent/` | `docs/agent/` | The 13 kit v1 protocols (project context, roadmap, module notes, teaching, documentation, GitHub, datasets, compute, reading list) |
| `HANDOFF.md` | `docs/HANDOFF.md` | Last handoff note |
| `lab_notebook/` | `docs/lab_notebook/` | Session notebook entries, 2026-10-10 to 2026-11-10 |
| `templates/` | `docs/_templates/` | Note templates (ADR, concept, lab notebook, paper, teach-back) |
| `machines/` | `docs/machines/` | Laptop (Photon) setup notes |
| `kit_audit.md` | `docs/architecture/kit_audit.md` | The 2026-10-27 audit of kit v1 |
| `learning/` | `docs/learning/` | MAP (and canvas), understanding ledger, weekly rhythm, Obsidian guide |

Older notes (for example `docs/learning/foundation/F1_big_picture.md` and `docs/learning/briefings/B01_the_whole_picture.md`) still mention these files at their original locations; this table is where to find them now.

Also removed in kit v2, recoverable from tag `kit-v1`: the nine slash commands and three subagents in `.claude/`, and the extra GitHub workflows, Dependabot, CODEOWNERS, issue templates and `scripts/bootstrap_github.sh`.
