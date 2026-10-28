---
type: index
status: living
tags: [briefings, start-here]
---

# Briefings: staying attached to the project

Why this folder exists (user, 2026-10-27): the agent does most of the building, so the user needs a place to catch up on **what is going on, what is planned, and why**, without reading every file in the repo. Each briefing is written on request, when the user asks to be brought up to speed, and is meant to be read top to bottom, then questioned.

How it differs from the other places:

| Place | Answers | Written by |
|---|---|---|
| `briefings/` (here) | "Where are we, what's the plan, why did we do it?" A guided read across the whole project at one point in time | agent, on request |
| `STATUS.md` | "What's the state right now?" Terse, overwritten | agent, every session |
| `lab_notebook/` | "What happened in session X?" A log | agent, every session |
| `learning/lessons/` | "Explain concept X" | agent, before a new concept |
| `learning/my_understanding/` | "What do I understand?" | the user only |

## Rules

- One file per briefing: `Bxx_<topic>.md`, dated in its frontmatter. Briefings are snapshots: an old one is not rewritten when the plan changes; a new briefing says what changed.
- Every claim links to the file that holds the evidence, so a briefing never becomes the only source of a fact.
- Questions the user asks after reading go in the briefing's "Questions and answers" section, so the answers are kept.

## Index

| # | Briefing | Date | Covers |
|---|---|---|---|
| B02 | [Spike S01, explained line by line](B02_spike_s01_walkthrough.md) | 2026-10-28 | The CSB dataset and its columns, how we got Louisiana, every notebook cell, the statistics, what we found and why it matters |
| B01 | [The whole picture](B01_the_whole_picture.md) | 2026-10-27 | Why the project exists, the master plan, how we work, everything done so far and why, the knowledge base, what we know, what's next |
