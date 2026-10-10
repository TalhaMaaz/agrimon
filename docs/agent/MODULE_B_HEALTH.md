# MODULE B: NEAR-REAL-TIME CROP HEALTH MONITORING

PRIORITY: Module B is important to the user (Oct 2026) and is the main showcase of present-day operation. Starts after Module A reaches Milestone M1 (plan for week 12); the near-real-time pipeline here also serves Module A's Tier 2 present-day demo (MODULE_A section 0b), so design the present-day data path once. Module B consumes Module A's crop labels per parcel.

## 1. Honest framing (read first)

- Sentinel-2 at 10 m and Sentinel-1 radar can reveal that a field is growing differently from what is expected for its crop and time of year. They generally cannot diagnose a specific disease or pest. Do not promise diagnosis. Define "health" in measurable terms and say what the system cannot tell.
- "Real time" means near real time: the system updates when new satellite acquisitions arrive. Sentinel-2 revisits roughly every 5 days with a two-satellite constellation (verify the current constellation and actual availability latency from the catalogue and record measured latency). Clouds create gaps, so radar and gap handling matter.
- Ground truth for "health" is scarce. A large part of this module is deciding how to validate.

## 2. B-Phase 0: Definition workshop (Gate B0)

Teach first (Primer on phenology baselines, anomaly detection, radar basics), then work with the user to answer, in writing:
1. What decisions would a user make from the health layer (irrigation, scouting, insurance flags)?
2. What does "unhealthy" mean operationally: slower growth than expected, canopy decline, water stress, lodging, flooding, late sowing? Pick a short list.
3. Update frequency and acceptable latency.
4. Output form: a per-parcel health index, an anomaly score, categorical flags, explanations.
5. How will each output be validated (the project has no ground truth of its own, so prefer retrospective documented events, synthetic anomaly injection, weather agreement, and expert review)? List real options: retrospective known events (drought or flood seasons, documented), synthetic anomaly injection, agreement with weather indicators, expert review of examples, (farm-visit ground truth is out of scope for the prototype; see DATASET_DISCOVERY section 8).
6. Which crops and region (depends on Module A's extension).

Write requirements R-B-xx and design studies DS-B-xx. Gate B0 passes when the definition is approved and at least one realistic validation strategy exists.

## 3. Approach layers (build in this order; each layer must beat the simpler one or be dropped)

1. **Expected-behaviour baseline per crop and region.** Build a typical seasonal curve (for example NDVI over time since sowing or by date) from history, using Module A's predicted or declared crop labels. Account for multi-year variability.
2. **Optical anomaly score.** Compare a parcel's current curve with its crop's expected curve (z-score or similar), after smoothing and gap filling. Compare to neighbouring parcels of the same crop to separate weather-wide effects from field-specific problems.
3. **Radar signal.** Add Sentinel-1 time series for cloud-independent monitoring.
4. **Weather and soil-moisture context.** Rainfall, temperature, reanalysis, soil moisture (verify sources and licences) to explain anomalies and avoid false alarms.
5. **Supervised stress classifier** only if labelled stress data exist (verified). Otherwise do not build one.

## 4. Pipeline (near real time)

```
 new S2/S1 scenes --> ingest + mask + harmonise --> per-parcel features (append)
        --> gap fill/smooth --> compare with crop baseline --> health score + flags
        --> store (versioned) --> API --> web map health layer + parcel history chart
```
Requires a scheduler and a small backend (store plus API). Record the choice in an ADR with pros and cons (for example scheduled jobs writing static tiles versus a service with a database). Measure and report end-to-end latency. Keep jobs idempotent and resumable. Use scheduled tasks rather than a long-lived foreground process.

## 5. Contract (document in `docs/architecture/interfaces.md`)

Output table per parcel and date: parcel_id, date, crop (from Module A, with probability), health_index, anomaly_score, flags, data_sources_used, cloud_gap_days, baseline_version, model_version. Contract tests in `tests/contracts/`.

## 6. Evaluation

- Define metrics per validation strategy: detection rate and false alarm rate on injected anomalies; agreement with documented events; stability (no flicker on noisy data); latency.
- Report false alarms honestly. A monitoring system that cries wolf is unusable.
- Threats to validity: no ground truth, baseline built from few years, cloud gaps, mixed pixels, crop misclassification propagating from Module A.

## 7. Anti-patterns

- Claiming disease diagnosis from 10 m imagery.
- Comparing a parcel against the wrong crop baseline because Module A was wrong, without carrying the classification uncertainty forward.
- Ignoring cloud gaps and presenting stale values as current.
- Building a supervised model on invented labels.
- Declaring "real time" without measuring latency.
- Flagging weather-driven field-wide change as a per-field problem without a neighbour comparison.
- Evaluating anomaly detection on the same events used to tune thresholds.

## 8. Teaching hooks

Phenology baselines; smoothing and gap filling (for example Savitzky-Golay or Whittaker, verify which is appropriate); anomaly scoring; radar basics and backscatter intuition; weather indices; validating without labels; scheduled pipelines and idempotency.
