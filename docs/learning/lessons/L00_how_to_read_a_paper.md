---
type: lesson
status: draft
tags: [lesson, papers, phase-r]
phase: R
---

# L00: How to read a research paper

Format: in-flow lesson (TEACHING_PROTOCOL 3.1). Needed before the first paper in [the reading list](../../agent/READING_LIST.md).

## What is a research paper?

A paper is a structured argument: "here is a problem, here is what we did, here is the evidence, here are the limits." It isn't a textbook. It assumes the reader knows the field, so a beginner can't read it from top to bottom like documentation and expect to follow it.

Typical sections:

```
 Title + Abstract      the whole paper in ~200 words
 1 Introduction        problem, why it matters, what others did, what is new here
 2 Related work        who did what before (sometimes merged into 1)
 3 Data / Study area   what data, where, when
 4 Method              what they built (equations live here)
 5 Experiments/Results tables and figures: the evidence
 6 Discussion          what the results mean, limits
 7 Conclusion          short restatement
 References            the trail to other papers
```

## How does it work? (the reading order)

Read it the way you'd read an unfamiliar codebase. You don't start at line 1 of `utils.py`. You read the README, then the tests (what it is supposed to do), then the public interface, and only then the internals.

```
 codebase                         paper
 --------                         -----
 README                    <-->   Abstract
 tests / example outputs   <-->   Figures and tables
 CHANGELOG / summary       <-->   Conclusion
 design doc                <-->   Introduction
 source internals          <-->   Method (read last, and only if needed)
```

Order:
1. **Abstract.** What problem, what claim?
2. **Figures and tables.** The evidence. Read every caption. Ask what is compared against what, and on which data.
3. **Conclusion.** What do the authors think they showed?
4. **Introduction.** Why the problem matters, and what was missing before.
5. **Method.** Only as deep as you need. Mark the equations you don't understand and ask; I explain each in plain words first.

You won't understand everything on a first pass. That's normal, even for experienced readers.

## Why do we need it here?

Every design choice in this project needs evidence you can show in the viva. Papers are most of that evidence. Reading them properly is also the only honest way to cite them: we never cite a paper we haven't opened.

## What goes wrong?

- **Reading only the abstract.** Abstracts present results in the most favourable light. The limits are in the tables and the discussion.
- **Trusting a headline number without its conditions.** "95 % accuracy" means little until you know the region, the classes, how the data were split, and what the baseline scored.
- **Getting stuck in the maths.** Skip it on the first pass, mark it, come back.
- **Over-generalising.** A result in France doesn't automatically hold in Pakistan. Always note where and when the data came from.

## The output: five lines

After each paper, write five lines in your own words in `docs/learning/my_understanding/papers/`. That folder is yours; I don't write in it.

```
1. Problem:  what question does it answer?
2. Data:     what data, which region, which years?
3. Method:   what did they do, in one sentence?
4. Result:   the main finding, with its conditions
5. Limits:   what it does not show, or where it might not hold
```

My fuller note goes in `docs/research/papers/` (template `docs/_templates/paper-note.md`), together with the equations explained and the design decision the paper affects.

## Check yourself

1. Why do we look at the figures before reading the method?
2. A paper reports 97 % accuracy for crop classification. Name three things you would check before believing that number applies to us.
3. What goes in line 5 of the five-line summary, and why does it matter for the viva?
