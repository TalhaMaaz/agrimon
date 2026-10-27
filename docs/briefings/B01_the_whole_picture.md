---
type: briefing
status: final
tags: [briefing, start-here, phase-r]
phase: R
date: 2026-10-27
---

# B01: The whole picture

Snapshot as of 2026-10-27, after session 3 and PR #27. Reading time: about 30 to 40 minutes. Read it top to bottom once, then come back with questions; the answers will be added to section 13.

Contents:
1. The project in one paragraph
2. Why the project exists
3. The master plan
4. What the finished Stage 1 application looks like
5. How we work, and why it's set up this way
6. Everything we've done so far, and why
7. Decisions made so far
8. The knowledge base: where everything lives
9. What we know (facts with evidence) and what we don't know yet
10. Concepts you need right now
11. What happens next
12. Decisions waiting for you
13. Questions and answers
14. Check yourself

---

## 1. The project in one paragraph

We are building a web application that shows farm fields on a map, says which fields are **sugarcane**, shows how **healthy** each field is, and estimates **yield**, all from free satellite imagery (Sentinel-2) and open datasets. We first build it for **Louisiana, USA**, because the US publishes exactly the data we need: yearly field boundaries and accurate crop labels. Building it there teaches us the whole pipeline and the professional standards. At the end of the FYP we take what we learned to **Pakistan**, where the data are much poorer.

---

## 2. Why the project exists

```
 original idea          problem                     solution
 -------------          -------                     --------
 crop intelligence      Pakistan has no good        STAGE 1: build the full app where
 for Pakistan     -->   open field polygons    -->  the data are good (Louisiana)
                        with crop labels            STAGE 2: adapt it to what Pakistan
                                                    has (end of the FYP)
```

Three motivations, in your words (2026-10-10), recorded in [PROJECT_CONTEXT section 1a](../agent/PROJECT_CONTEXT.md):

1. **Grades and the thesis.** The FYP must be finished, written up and defended in a viva, where you must explain every part.
2. **Skills and standards (the real reason).** You want to learn how this kind of system is built **properly**, end to end: data, labels, imagery, models, validation, serving, shipping. So in every step we ask "what is the standard way, and who says so?", and we write down what transfers to Pakistan in [`docs/playbook/`](../playbook/README.md).
3. **After university (context only).** A startup selling this kind of application to Pakistani sugar mills. It is **not FYP scope**. It only explains two preferences: sugarcane matters, and licences must not block later commercial use.

---

## 3. The master plan

```
 STAGE 1 (now)                                                  STAGE 2 (end of FYP)
 Louisiana, US                                                  Pakistan
 -------------------------------------------------------------  -------------------
 R  research and architecture  <-- WE ARE HERE                  adapt to Pakistani
 0  repository, tooling, charter, requirements                  data; build what is
 A  crop type: field map, sugarcane vs rest                     possible today
 B  health layer per field (important to you)
 C  yield estimate (priority decided later)
 Demo  replay on past seasons (must); present-day run (stretch)
 Thesis + defence pack
 Bridge report: what Stage 2 needs  --------------------------> opens Stage 2
```

Rules of the plan ([ROADMAP](../agent/ROADMAP.md)):
- **No week-by-week schedule.** You asked for outcomes and gates, not weeks. When a step is done, move on; finishing early is the goal.
- **Gates.** We move on only when a step's gate is passed. The first gate is **Checkpoint R**, where you approve the architecture.
- **Order.** A before B; C is cut first if time runs short.
- **Note:** the ROADMAP and module files still contain the kit's older wording. Rewriting them is the next re-planning step (section 11). Where they disagree with this briefing, this briefing and the [kit audit](../architecture/kit_audit.md) are newer.

### What is Phase R, and why do it before writing code?

The kit came with many ready-made choices: which dataset, which models, which web stack. They came from a short round of web research, **not** from evidence. In the viva you must defend every choice with evidence, so Phase R turns those guesses into proven (or replaced) decisions:

```
 design questions --> literature + dataset search --> read and note papers
        |                                                     |
        v                                                     v
 hypotheses (guesses) <------------- evidence -------- synthesis matrix
        |
        v
 small experiments ("spikes") --> architecture dossier + ADRs --> Checkpoint R (you approve)
```

- **Design question (DQ):** something the architecture must answer, for example "how do we split data so scores are honest?" There are 23, in [design_questions.md](../architecture/design_questions.md).
- **Hypothesis (H):** a candidate answer, with a status: *hypothesis* (written down), *provisional* (partly supported), *validated* (supported by evidence) or *rejected*. There are 24, in [hypothesis_register.md](../architecture/hypothesis_register.md).
- **ADR (architecture decision record):** a short file per decision: the options, the choice, the evidence and what would change it. This is the proof trail for the viva.

---

## 4. What the finished Stage 1 application looks like

From your answers on 2026-10-27, in [product_spec.md](../architecture/product_spec.md):

```
 +--------------------------------------------------------------+
 |  web map                                    [date / season]  |
 |   +------+   +-----+        layers:                          |
 |   | cane |   | non |        [x] crop type (field polygons)   |
 |   +------+   +-----+        [x] health (per field)           |
 |        +---------+          [ ] yield estimate               |
 |        |  cane   |          click a field -> crop, confidence,|
 |        +---------+          health history, yield            |
 +--------------------------------------------------------------+
```

| Capability | Priority | What it needs from the data |
|---|---|---|
| P-1 field polygons | must | field boundaries for past seasons **and** a recent season |
| P-2 crop type (sugarcane vs non-sugarcane preferred) | must | crop labels per field, several years |
| P-3 health layer | must | years of imagery history per field, weather, documented events (droughts, hurricanes) to test against |
| P-4 yield estimate | open | yield statistics for the same region (field, farm or parish level) |

**Why we wrote this spec first.** The kit planned bottom-up: pick a dataset, build classification, then think about the rest. Planned that way, the dataset (Brazil-Crop) could do crop type but not the health layer or yield. Planning top-down (the interface first, then the data the interface needs, then the dataset that has that data) avoids building half an application. This was the main finding of the audit.

---

## 5. How we work, and why it's set up this way

### 5a. Who does what

```
 Claude (developer)                        You (owner, reviewer)
 ------------------                        ---------------------
 researches, writes code and docs          decide scope and priorities
 opens issues, branches, draft PRs         review the diff, ask questions
 explains every concept and change         merge (only you can)
 never pushes to main, never merges        must be able to explain everything
```

**Why.** The university allows full AI use but requires you to understand everything that's built. So I build, and you stay the decision-maker and the one who can explain it. Rule 13 in CLAUDE.md: if you can't explain a part, that part isn't finished.

### 5b. The repository is the memory

Chats with Claude are temporary. I forget between sessions, and the chat history lives on one machine. So everything that matters is written into the repo: [STATUS](../STATUS.md) (where we are), [HANDOFF](../HANDOFF.md) (how to resume), the [lab notebook](../lab_notebook/) (what happened each session), ADRs (why we decided). Any session on any machine can resume from them.

### 5c. The Git workflow

```
 issue (#N) -> branch -> commits -> push -> draft PR -> CI checks -> you review -> you squash-merge
```

**Why.** The same flow professional teams use (one of the "standards" you want to learn). Every change is reviewable, reversible and linked to a reason.

### 5d. The guards

- **Hooks**: scripts on your laptop that stop *me* from pushing to `main`, merging, force-pushing, or committing data or secrets. In session 2 they wrongly blocked harmless commands, so we rewrote and tested them (#22).
- **GitHub ruleset**: a server-side rule that applies to everyone, you included. A PR needs green `ci` and must be up to date with `main`.

**Why both.** The hooks guard the agent; the ruleset guards the repository.

### 5e. Evidence rules

I may never invent a number, URL, citation or licence. Facts are checked at the source and marked unverified until they are. That's why the dataset catalogue says "verified" or "unverified" next to every fact.

---

## 6. Everything we've done so far, and why

| When | What | Why |
|---|---|---|
| Kit preparation (before 2026-10-10) | The kit was built with Claude: rules (CLAUDE.md), protocols (`docs/agent/`), slash commands, hooks, CI, issues #6 to #13, milestones | Start with a working system for teaching, documentation and Git, so the project is run like a professional one from day one |
| Session 1, 2026-10-10 | First design questions and hypothesis register; lesson L00 (how to read a paper) | Phase R step 1: write down what must be answered before building |
| Session 2, 2026-10-10 | Foundation guide F0 to F6; a practice run of the full Git workflow; fixed CI (#18); recorded your vision across the kit (#20); fixed the hook's false alarms with 39 tests (#22); merged Dependabot #1 to #5 | You wanted to learn the kit hands-on. CI was failing on every PR, so nothing could be merged. The vision (two stages, learning standards) wasn't in the kit yet |
| Session 3, 2026-10-27 | Merged #23 to #26; **audited the kit** ([kit_audit.md](../architecture/kit_audit.md)); wrote the **product spec**; revised the questions and hypotheses; **first dataset search**; you chose the **US stack**, starting with **Louisiana** (#27) | You asked to re-evaluate everything the kit preloaded against the bigger plan: one region whose data carry the whole application and match the end-product interface |

### What the audit found (short version)

| # | Finding | What we did |
|---|---|---|
| F-01 | No definition of what the finished app shows | Wrote the product spec |
| F-02 | Datasets were scored only for crop classification | Added "module coverage" to the rubric (weighted double) |
| F-03 | Sugarcane was treated as an annual crop | New DQ-21; hypothesis H-20 (expected to fail) |
| F-04 | Yield was called "not important" without a product reason | Priority left open until we know what yield data exists (DQ-22) |
| F-05 to F-08 | France-specific text, milestone order against the roadmap, stale issues, an outdated Pakistan note | To be fixed in the roadmap rewrite |
| F-09 | No dates recorded | You chose to keep the dates private; the one known constraint is the intro presentation |

---

## 7. Decisions made so far

| Decision | Status | Reason | Where |
|---|---|---|---|
| Two stages; Stage 1 only for now | decided (you, 2026-10-10) | Pakistan lacks the data; learn the standards first | [PROJECT_CONTEXT 1a](../agent/PROJECT_CONTEXT.md) |
| Plan from the product interface down | decided (you, 2026-10-27) | So one dataset carries the whole app | [product_spec](../architecture/product_spec.md) |
| US data stack (USDA CSB boundaries + CDL labels) | decided (you, 2026-10-27); ADR at Checkpoint R | The only candidate verified to cover all four capabilities; labels are accurate for sugarcane | [dataset_catalogue](../research/dataset_catalogue.md) |
| Start with Louisiana | decided (you, 2026-10-27) | Cane grown alongside other crops (a realistic cane vs non-cane task); hurricanes and droughts give documented events for testing the health layer | same |
| Leave Pakistan data until Stage 2 | decided (you, 2026-10-27) | Focus | [kit_audit F-07](../architecture/kit_audit.md) |
| Other datasets only where a capability needs them | decided (you, 2026-10-27) | Avoid extra work without a reason | catalogue section 2a |
| Cane vs non-cane, or multi-class? | **open** (DQ-14, H-19) | Binary may look simpler, but "non-cane" mixes many crops | design questions |
| Yield priority | **open** (DQ-22) | Depends on what yield statistics exist for Louisiana | design questions |
| Code licence (MIT or Apache-2.0) | **open**, needed before scaffolding (#7) | Public code needs a licence | STATUS |

---

## 8. The knowledge base: where everything lives

```
 agrimon/
   CLAUDE.md            the always-on rules I follow (you can read them)
   START_HERE.md        entry point to the kit
   .claude/             my tools: slash commands, read-only helper agents, hooks
   .github/             CI, security scanning, Dependabot, PR and issue templates
   docs/  (your Obsidian vault)
     briefings/         YOU ARE HERE: catch-up documents like this one
     STATUS.md          where the project is, right now
     HANDOFF.md         how to resume on any machine
     lab_notebook/      one file per session: what we did, commands, surprises
     learning/          MAP (your front page), lessons, foundation guide F0-F6,
                        understanding ledger, my_understanding/ (only you write here)
     architecture/      kit audit, product spec, design questions, hypotheses
                        (later: the architecture dossier)
     research/          dataset catalogue, search log (later: paper notes,
                        synthesis matrix)
     playbook/          standards that transfer to Pakistan (empty: filled as phases end)
     agent/             protocols I follow: roadmap, Phase R method, module plans,
                        teaching, documentation, GitHub workflow, datasets, compute
     glossary.md        terms
     _templates/        templates for notes, ADRs, the lab notebook
```

**What to read, and when:**

| You want to know | Open |
|---|---|
| Where are we? | [STATUS](../STATUS.md), or [MAP](../learning/MAP.md) in Obsidian |
| The whole story | a briefing (this folder) |
| What happened in one session | that day's [lab notebook](../lab_notebook/) entry |
| Why a choice was made | the ADR (none yet), the [hypothesis register](../architecture/hypothesis_register.md), the [catalogue](../research/dataset_catalogue.md) |
| What I'm supposed to understand | [understanding ledger](../learning/understanding_ledger.md) |
| How I (Claude) am told to work | `docs/agent/` (optional reading) |

---

## 9. What we know (facts with evidence) and what we don't know yet

### Known (checked at the source)

| Fact | Source |
|---|---|
| **CSB** (Crop Sequence Boundaries, USDA NASS): field boundaries for the contiguous US, in 11 eight-year editions from 2008-2015 to 2018-2025. The 2018-2025 data were released 2026-03-27. They are built from the CDL and are called "open source" | NASS CSB page |
| **CDL** (Cropland Data Layer, USDA NASS): a yearly 30 m crop map; sugarcane is code 45; "public domain and free to redistribute" | NASS metadata |
| CDL sugarcane accuracy: producer's 94.1 to 97.2 %, user's 94.8 to 96.4 % (Louisiana 2020, 2022, 2023; Florida 2020, 2022). Checked against farmer-reported Farm Service Agency field data, per pixel | NASS metadata ([table](../research/dataset_catalogue.md)) |
| NASS publishes state-level sugarcane yields for Louisiana and Florida | archived NASS reports |
| Brazil-Crop: 5,477 fields, 30 classes including sugarcane, CC BY 4.0, 2020-2021 only | Zenodo |
| A Pakistan dataset exists: 85,618 fields, sugarcane included, CC BY 4.0 (polygons not mentioned) | Zenodo; parked for Stage 2 |

### Not known yet (the next session's work)

- Exactly what CSB files contain: crop per year? file sizes? licence wording?
- Whether NASS publishes sugarcane yields per **parish** (Louisiana's word for county), or only per state. This decides P-4.
- Whether the weekly NASS crop condition reports rate sugarcane (possible health validation).
- Whether our imagery source (Microsoft Planetary Computer) works. The test failed because the network dropped.
- How many cane fields Louisiana has, and how big they are.

---

## 10. Concepts you need right now

One at a time, plain words first. Each will get a proper lesson when we use it.

### 10a. Sentinel-2

A pair of European satellites that photograph the whole Earth's land every few days, free of charge. They don't only see red, green and blue: they record 13 "bands" of light, including near-infrared, which healthy plants reflect strongly. Main bands are 10 m per pixel, so a 1-hectare field (100 m x 100 m) covers about 100 pixels.

*Coding analogy:* each image is a 3-D array `[band, row, column]`; a series of images over a season is `[time, band, row, column]`.

### 10b. Field polygons and labels

- A **polygon** is the outline of a field, stored as a list of coordinates (a vector shape).
- A **label** is the answer for that field ("sugarcane").
- Machine learning needs many (field, label) pairs to learn from.
- CSB gives the polygons and CDL gives the labels.

### 10c. Producer's vs user's accuracy

Imagine 100 real sugarcane fields, and a map that labels 98 fields as sugarcane.

```
                         map says cane     map says other
 really cane                  94                 6        -> producer's = 94/100 = 94 %
 really other                  4                 -           (6 missed: omission)
                         user's = 94/98 = 96 %
                         (4 false alarms: commission)
```

- **Producer's accuracy:** of the real cane, how much did the map find? (from the map **maker's** side)
- **User's accuracy:** of what the map calls cane, how much really is cane? (from the map **user's** side)

### 10d. Model-derived labels and circularity

CDL is itself the output of a USDA machine-learning model. If we train our model on CDL, it partly learns CDL's mistakes ("circularity"). It's acceptable here because CDL's sugarcane accuracy is about 95 %. We will (1) say so openly, (2) measure label consistency ourselves (does a field get the same label year after year?), and (3) never claim our model beats "the truth" when the truth is CDL.

### 10e. Sugarcane is not an annual crop

- Most crops (soybean, wheat) are planted and harvested within one season.
- Sugarcane is **semi-perennial**: once planted, it grows for about a year or more. After harvest it regrows from the stubble left in the ground (a **ratoon** crop), for several cycles, before it is replanted.

This changes three things:
- what a "label for this season" means;
- what a "normal" growth curve looks like for the health layer;
- when a yield estimate makes sense.

That's design question DQ-21.

### 10f. Why we split data carefully (preview)

Neighbouring fields look alike: same soil, same weather. If training fields and test fields are neighbours, the model gets an easy test and the score looks better than it really is. So we test on fields far away, or in a different year. This will probably be the most-asked viva question (DQ-10), and it gets a full lesson later.

---

## 11. What happens next

```
 next session                                then                       before the presentation
 ------------                                ----                       -----------------------
 Louisiana data check:                       literature at survey       presentation content:
 - CSB contents, small sample (ask first)    depth: crop type, health   problem, plan, deliverables,
 - parish yields? (decides P-4)              signals, sugarcane yield   what can / cannot be done,
 - field counts and sizes                    roadmap rewrite (module    risks; slides; /viva-drill
 - imagery source test                       files, milestones, issues) rehearsal
```

The **intro presentation** (about two weeks after 2026-10-27) sets the pace. It needs: the problem and motivation (section 2), the plan (section 3), the deliverables (section 4), what can and cannot be done (still to be researched: for example, no disease diagnosis from 10 m imagery, honest limits of CDL labels), and the risks.

---

## 12. Decisions waiting for you

1. Approve the small Louisiana sample download (under 500 MB) when I propose it.
2. Delete the three merged branches still on GitHub (`docs/6-close-session-2`, `dependabot/.../labeler-7`, `dependabot/.../codeql-action-4`).
3. Later: the code licence (MIT or Apache-2.0), before scaffolding.

---

## 13. Questions and answers

(Your questions after reading go here, with the answers.)

### Q1 (2026-10-27): Where did the briefings folder go while I was reading it?

It never left; it was on a different **branch**. B01 was in PR #28 on branch `docs/6-briefings`, not yet merged into `main`. For your next question I switched the laptop to a new branch made from `main`, and Git swaps the files on disk to match whichever branch is checked out. `main` didn't have `docs/briefings/` yet, so Obsidian saw it vanish. Switching back (`git switch docs/6-briefings`) brought it back.

```
 main ----------------------------------  (no briefings/ yet)
        \-- docs/6-briefings  (B01 here, PR #28)
        \-- docs/6-louisiana-related-work  (PR #29)
 the laptop shows ONE branch at a time; switching changes the files you see
```

Once PR #28 is merged, the folder is on `main` and stays visible on every branch made after that. Lesson for me: don't switch branches under a document you're reading. Keep the reading branch checked out, or ask you to merge first.

### Q2 (2026-10-27): Why exactly did we choose the US dataset?

Short answer: it's the only candidate we could **verify** covers all four capabilities of the app, with labels accurate enough for sugarcane and no licence restrictions. You made the decision on 2026-10-27; it will be confirmed by an ADR at Checkpoint R.

**1. The test it had to pass.** Since the audit, the dataset isn't chosen for crop classification alone. It must carry the whole app ([product spec](../architecture/product_spec.md) section 4):

| Capability | What the US stack gives | Brazil-Crop | La Réunion | Europe |
|---|---|---|---|---|
| P-1 polygons, past **and** recent | CSB: yearly field boundaries in editions up to 2018-2025 | 2020-21 only | probably yearly, **unverified** | yearly |
| P-2 crop labels, sugarcane | CDL every year since 2008, sugarcane at about 95 % accuracy | survey labels, two seasons per region | declared, **unverified** | no sugarcane |
| P-3 health: history + recent fields + events | many years of labelled fields; hurricanes, freezes, droughts documented | no recent fields, 2 seasons | cloudy island, unverified | yes |
| P-4 yield | state yields confirmed; parish data likely (area confirmed by Di Tommaso 2024) | unverified | unverified | unverified |
| Licence | public domain | CC BY 4.0 | open licence, unverified at parcel level | varies |

Only the US column has no "unverified" and no "no".

**2. Why the many years matter.** They aren't about having more data; each one is needed for something specific:
- **Honest evaluation:** we can train on some years and test on a year the model never saw (the "held-out year"). With two seasons, as in Brazil-Crop, that's barely possible.
- **Health layer:** "is this field unhealthy?" means "is it growing worse than a normal cane field at this stage?" To know "normal", we need many past seasons of healthy cane.
- **Live demo and near-real-time health:** these need field boundaries for a **recent** season, so today's satellite images can be read per field. CSB goes up to 2025; Brazil-Crop stops in 2021.

**3. Why the labels are good enough.** CDL sugarcane: producer's accuracy 94.1 to 97.2 %, user's accuracy 94.8 to 96.4 % (Louisiana 2020, 2022, 2023; Florida 2020, 2022), checked against farmer-reported FSA field records. A peer-reviewed paper (Di Tommaso et al. 2024) independently reports above 93 % for Louisiana.

**4. Why public domain matters.** No restriction on the thesis, on publishing maps, or on later commercial use (the reason licences are "kept in view").

**5. Why Louisiana within the US.**
- Cane grows next to soybean, rice and corn, so cane vs non-cane is a real task, not a trivial one.
- There are well-documented stress events to test the health layer.
- Related work exists to compare against: Hu et al. 2022 for yield, NASS flood mapping ([related work](../research/related_work_louisiana.md), PR #29).

**What we gave up (say these in the viva):**
- **Labels come from a model, not ground survey.** Our model partly learns CDL's mistakes (circularity). Mitigation: CDL's cane error is about 5 %; we check the labels against the independent GEDI-based map and against year-to-year consistency; we never claim to beat "the truth".
- **The boundaries come from a model too.** CSB is built from CDL, so a field outline can be imperfect.
- **The accuracy is per pixel**, not per field, and may be slightly optimistic.
- **Least like Pakistan.** Large mechanised farms, unlike Pakistani smallholdings. The pipeline and the standards transfer; the trained model doesn't. That's expected in Stage 1.

**What would change the decision** (checked in the next session's Louisiana data check):
- CSB files turn out not to carry a crop per year.
- Too few or too small cane fields in Louisiana.
- Cloud cover too heavy for usable time series.
- Licence wording that differs from "public domain".

---

## 14. Check yourself

1. In one sentence each: why Stage 1, why the US, why Louisiana?
2. What is the difference between a design question, a hypothesis and an ADR?
3. Why did we write the product spec before choosing a dataset?
4. Explain producer's and user's accuracy with your own made-up numbers.
5. Why does sugarcane's ratoon cycle matter for the health layer?
6. Who can merge a PR, and what two things stop me from pushing to `main`?
