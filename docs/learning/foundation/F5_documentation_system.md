---
type: lesson
status: draft
tags: [lesson, foundation, docs, obsidian]
phase: R
---

# F5: The documentation system

Previous: [F4 GitHub features](F4_github.md) | Next: [F6 A working day, and gaps](F6_a_working_day_and_gaps.md)

## What is it?

`docs/` is three things at once:

1. **The project's memory** (F1): state, decisions, progress.
2. **The raw material for the thesis and the viva**: every claim needs a trail to evidence.
3. **Your Obsidian vault**: where you read, navigate and learn.

All of it is plain Markdown with a small YAML header, so it renders on GitHub, in Obsidian and in Pandoc (for the Word thesis).

## The documents, grouped by how often they change

```
 EVERY SESSION                 EVERY DECISION / PHASE              STABLE REFERENCE
 -------------                 ----------------------              ----------------
 STATUS.md      where we are   decision_log/ADR-NNNN-*.md          agent/          rules for Claude
 HANDOFF.md     how to resume  phase_reports/                      _templates/     note templates
 lab_notebook/  the diary      architecture/ (DQs, hypotheses,     learning/OBSIDIAN_GUIDE, WEEKLY_RHYTHM
 learning/MAP.md "right now"     dossier)
 understanding_ledger.md       research/ (search log, papers)
                               requirements/, experiments/
                               registers (assumptions, risks,
                               claims, glossary)
```

| Document | Question it answers | Analogy |
|---|---|---|
| `STATUS.md` | Where are we, what's next, what's blocked? | Dashboard / README badge |
| `HANDOFF.md` | How exactly do I resume on another machine? | Shift-change note |
| `lab_notebook/YYYY-MM-DD.md` | What happened today and why? | Commit log with reasons |
| ADR (Architecture Decision Record) | Why did we choose X over Y? | Design doc with a verdict; never edited, only superseded |
| `architecture/design_questions.md` | What must the design answer? | Requirements spec for the architecture |
| `architecture/hypothesis_register.md` | What do we believe, and how sure are we? | Test-status board for beliefs |
| Phase report | What did a phase achieve, with numbers? | Sprint review |
| `understanding_ledger.md` | What do *you* understand? | Test coverage, for your head |
| `learning/MAP.md` | What should I look at today? | Home page |

Many of these don't exist yet. They're created when their phase arrives (ADRs at the first decision, phase reports at the first finished phase, and so on).

## Observation versus interpretation

The notebook and reports keep two things apart: what the data showed (**observation**) and what we think it means (**interpretation**). This is what an examiner probes. Example from the first notebook entry: "Observation: section 0 says Brazil, section 8 says France. Interpretation: the kit was edited partway through."

## Frontmatter

Every note starts like this:

```yaml
---
type: lesson          # what kind of note (lesson, adr, paper, status, ...)
status: draft         # draft, living, final, ...
tags: [lesson, foundation]
phase: R              # optional: which phase
module: A             # optional: which module
---
```

Obsidian shows it as properties and can search by it ("all notes with `type: adr`").

## Obsidian: how to open it correctly

The vault is **`docs/`**, not `docs/learning/`. The shared settings live in `docs/.obsidian/` (already in git): Markdown links on, relative paths, links updated on rename. Opening `docs/learning/` created a second, separate config at `docs/learning/.obsidian/`, which git doesn't ignore.

Fix:
1. In Obsidian: vault switcher (bottom-left), "Open folder as vault", choose `.../agrimon/docs`.
2. Delete `docs/learning/.obsidian/` (it's only Obsidian's layout state from the wrong vault).
3. Open `learning/MAP.md` and pin it.

Useful features: backlinks (where a note is referenced), graph view, `learning/MAP.canvas` (a visual map), search by tag.

## Who writes where

| Location | Writer |
|---|---|
| `learning/my_understanding/` | **You only.** Claude never writes there. Your own words become thesis background and viva prep. |
| Everything else in `docs/` | Claude writes; you review through PRs |

If you edit a Claude-written file in Obsidian, that change goes through a branch and PR like any other change.

## Links

Standard relative Markdown links (`[F4](F4_github.md)`), never Obsidian `[[wikilinks]]`, because GitHub and Pandoc don't understand wikilinks.

## What goes wrong?

- Notes written in the chat only: lost (F1).
- ADRs edited after the fact: the decision trail lies. Supersede instead.
- Interpretation written as observation: an examiner will catch it.
- The ledger marked "solid" without a check: it stops being useful as a revision list.

## Check yourself

1. What is the difference between STATUS, HANDOFF and the lab notebook?
2. Why is an ADR superseded rather than edited?
3. Which folder may Claude never write in, and why does that folder matter for the thesis?
