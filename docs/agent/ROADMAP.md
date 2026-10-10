# ROADMAP (a direction, not a schedule)

The user's instruction (Oct 2026): do not plan hard around weeks. The goal is to finish the general prototype early, then expand the scope and build a Pakistan-specific system. So this file gives stages, outcomes and gates in order. It carries no week numbers and no fixed durations. Time is tracked as it is spent (lab notebook, STATUS), and the order changes whenever evidence says it should. Deadlines (thesis, defence) are a constraint to record when the user knows them; they are not a plan.

## 1. Two stages

```
 STAGE 1: general prototype (now)            STAGE 2: Pakistan (after Stage 1)
 -------------------------------             ----------------------------------
 any open dataset in the world               Pakistan-specific data and needs:
 learn the whole stack                       labels (scarce), field boundaries,
 prove the architecture                      irrigated smallholder fields, wheat/
 modules A and B (C = short note)            rice/cotton/sugarcane calendars,
 demo on old fields; present-day stretch     monsoon cloud and radar, ground truth,
                                             local partners, startup concerns
```

Stage 1 exists to make Stage 2 cheaper and better. Anything learned in Stage 1 that does not transfer should be written down as such. Stage 2 will need different things (data collection, partnerships, possibly different models); its detailed plan is written at the end of Stage 1 from what was learned, not now.

## 2. Stage 1 outcomes in order

| Step | Outcome | Gate to move on |
|---|---|---|
| R | Research and architecture design: papers read, notes written, architecture hypotheses validated or replaced, architecture dossier approved (see RESEARCH_AND_ARCHITECTURE.md) | Checkpoint R |
| 0 | Repository, GitHub workflow, CI, documentation system, charter, requirements | Checkpoint 0 |
| A | Module A pipeline: dataset audit and choice, labels and splits, imagery to features, baselines, deep models, in-season prediction, export, web map on old fields | Milestone M1 |
| B | Module B: definition of "health" and validation plan, expected-curve baselines, anomaly scoring, radar and weather inputs, near-real-time scheduled pipeline, health layer on the map | Gate B0, then Milestone M3 |
| Demo | Tier 1 replay on old fields; Tier 2 present-day run if a pilot works | Milestone M5 |
| C | Short yield feasibility note; a small prototype only if open data and time allow | Gate C0 |
| Thesis | Word thesis, reproducibility check, defence pack | Final checkpoint |
| Bridge | Pakistan Bridge Report: what Stage 2 needs, based on what was learned | Part of the thesis |

Steps can overlap and be reordered. Finishing early is a goal: when a step is done, move on; do not fill time. Optional work (second dataset, extra ablations) is done only if it buys understanding or a better defence.

## 3. Gates

- **Checkpoint R.** The architecture dossier is approved by the user. Each major design choice is marked validated (with evidence), provisional (with a plan to validate), or rejected.
- **Gate: first dataset.** Brazil-Crop passes the audit rules in MODULE_A section 0, or another dataset is chosen. No self-collected data is planned in Stage 1.
- **Gate B0.** "Health" is defined operationally and at least one realistic validation strategy exists.
- **Gate C0.** Default outcome is a feasibility note. Anything more needs the user's approval.

## 4. Re-planning rules

- Review at the weekly review. State what happened and what the evidence now suggests; do not defend an old plan.
- If something takes much longer than expected, say so, show the cause, and propose cutting scope in this order: Module C beyond the note, second dataset, optional ablations. Do not cut documentation, evaluation honesty or the validation of architecture choices.
- Protect the order A then B. Module C is cut first.
- Because the defence requires proof of every decision, speed never justifies skipping the evidence for a choice. It justifies choosing smaller choices.

## 5. Compute planning

Laptop (RTX 3060 6 GB, 16 GB RAM, about 84 GB disk) for development and small models; lab PC (no GPU, large RAM and SSD, reachable remotely) for heavy extraction; Kaggle or Colab for GPU runs if needed; Earth Engine (noncommercial, university work) as an optional extraction backend. See PLATFORM_AND_COMPUTE.md. Stream imagery and keep only derived per-parcel features. Record where each experiment ran.
