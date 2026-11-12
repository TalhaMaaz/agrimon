---
type: guide
status: living
tags: [obsidian, setup]
---

# Using Obsidian with this project

## 1. What Obsidian is for here

The `docs/` folder is the vault. Obsidian gives you fast navigation, backlinks, a graph view and a canvas over the same Markdown files that Git versions and the thesis is built from. The files stay plain Markdown, so nothing is locked into Obsidian.

Pros: free to use, local files, great for learning notes and linking concepts. Cons: it is a second tool to learn; some features (wikilinks, plugins) are Obsidian-only and do not render on GitHub or in Pandoc, which is why this kit uses standard Markdown links.

## 2. Setup (about 10 minutes)

1. Install Obsidian from obsidian.md.
2. Open Obsidian, choose "Open folder as vault", and select the repository's `docs/` folder.
3. A starter `.obsidian/` configuration ships with the kit. Check Settings, Files and links:
   - "Use [[Wikilinks]]": OFF (standard Markdown links keep GitHub and Pandoc working; the shipped config tries to set this, but confirm it in the settings, because I could not test it).
   - "Automatically update internal links": ON (renaming a file fixes links).
   - New link format: relative path to file.
4. Open `learning/MAP.md` and pin it. Open `learning/MAP.canvas` for the visual map.
5. Set Templates (core plugin) folder to `_templates` if it is not already set.
6. Optional: turn on Daily notes, folder `lab_notebook`, date format `YYYY-MM-DD`, template `lab-notebook`.

## 3. Who writes what

| Location | Written by | Notes |
|---|---|---|
| `learning/my_understanding/` | You only | Your own words. The agent never writes here |
| `learning/` lessons, walkthroughs, ledger | Agent | You read, question and annotate |
| `concepts/`, `decision_log/`, `phase_reports/`, `experiments/`, `lab_notebook/` | Agent, reviewed by you | These feed the thesis |
| `_templates/` | Kit | Copy with Obsidian's Insert template |

Rule: do not edit agent-written files directly in Obsidian without telling the agent; changes go through a branch and PR like everything else. Put your thoughts in `my_understanding/` or in a note that links to the agent's file.

## 4. Conventions the agent follows (so notes work well in Obsidian)

- Every note starts with YAML frontmatter: `type`, `status`, `tags`, plus `module` and `phase` where relevant.
- Standard relative Markdown links between notes, for example `[ADR-0003](../decision_log/ADR-0003-first-dataset.md)`.
- Tags are lowercase and few: `#concept`, `#adr`, `#paper`, `#lesson`, `#shaky`, `#solid`, `#module-a`, `#module-b`, `#module-c`.
- One concept per note in `concepts/`, named by the concept (`spatial-block-validation.md`).
- Diagrams are ASCII in code blocks (they render everywhere).
- Maths in plain words first; formulas as LaTeX between `$$` markers (Obsidian renders it; GitHub also renders `$$`).

## 5. Using the tools

- **Backlinks panel**: on any concept note, see every place it is used. This is how you find "where did we use calibration?".
- **Graph view**: filter by tag `#concept` to see how ideas connect; orphans are concepts nothing uses (probably not needed) or notes you forgot to link.
- **Canvas** (`learning/MAP.canvas`): drag the pipeline map around, add your own sticky notes and links. Canvas files are JSON and can be committed.
- **Search**: `tag:#shaky` lists concepts you marked as shaky in the ledger.
- **Quick checklist**: the checkboxes in MAP.md are yours; tick them only after a successful `/teach-back`.

## 6. Git and Obsidian together

- The vault is part of the Git repository. Commit changes from the terminal or through the agent, on a branch.
- `.obsidian/workspace*.json` (open panes, window layout) and caches change constantly and are device-specific; the kit's `.gitignore` excludes them. Shared settings (`app.json`, `core-plugins.json`, `graph.json`, templates) are committed.
- Obsidian Sync is not needed: Git (push and pull) is your sync and your history. Sync does not happen automatically, so pull before you start and push at the end.
- Community plugins are optional. If you install any (for example Dataview for dashboards), record it in an ADR and note that CI and GitHub will not render them.

## 7. Suggested first hour

1. Open MAP.md and read sections 2 and 3.
2. Open the canvas and rearrange it until it makes sense to you.
3. Create your first note in `my_understanding/` from the `teach-back` template: "What is a satellite time series?" in your own words.
4. Tick nothing yet.
