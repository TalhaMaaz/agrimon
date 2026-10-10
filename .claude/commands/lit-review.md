---
description: Research a design question in the literature, read and note papers, update the synthesis matrix
argument-hint: [design question]
---

Research this design question: $ARGUMENTS

1. Read `docs/agent/RESEARCH_AND_ARCHITECTURE.md`, `docs/agent/READING_LIST.md`, `docs/architecture/hypothesis_register.md` and `docs/research/synthesis_matrix.md` if they exist.
2. State assumptions first. Restate the question and the related hypotheses (H-xx) it tests. Ask me anything unclear before searching.
3. Search (arXiv, Google Scholar, journals, project documentation). Log queries and dates in `docs/research/search_log.md`. Prefer a recent survey first, then specific methods. Use forward and backward citation chasing.
4. Open and read each paper you will rely on. Verify title, authors, year, venue and DOI at the source before adding it to `references.bib`; otherwise list it in `docs/research/unverified_references.md`. Write a note per paper from `docs/_templates/paper-note.md` in `docs/research/papers/`, with maths explained in plain words first.
5. Update the synthesis matrix: candidate approaches, what the evidence says, conditions (region, crop, data size), gaps, and evidence against the kit's starting choices. Say which approach is the established practice (and who established it), and whether the evidence holds for Pakistani conditions (smallholder, irrigated, monsoon cloud, scarce labels). Update the status of affected hypotheses.
6. Propose at most three small spikes (cheap experiments) that would settle what the literature cannot, each with a question and a decision rule.
7. Report briefly: what you read, what changed, what is still unknown. Teach me the two most important papers in plain words, one concept at a time. Put changes on a branch and do not merge.
