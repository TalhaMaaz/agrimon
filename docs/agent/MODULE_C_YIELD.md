# MODULE C: YIELD PREDICTION (CONDITIONAL)

LOW PRIORITY (user, Oct 2026): Module C is not important. Default outcome is a short feasibility note (data needs, what open statistics exist, what a model could and could not claim). Build a regional prototype only if open yield statistics are found quickly and time remains after Module B. Starts only after Gate C0 (see ROADMAP). Yield prediction depends far more on data availability than on model choice. A well-documented feasibility study is an acceptable outcome and is better than a model trained on inadequate data.

## 1. Gate C0: feasibility check

Teach first (Primer: regression versus classification, yield determinants, small-data pitfalls). Then determine, with evidence:

| Level of yield data | What it supports | Concern |
|---|---|---|
| Field-level yield records (location, crop, season) | Field-level models and honest validation | Rare; needs farm access or a partner |
| Farm-level records | Aggregated features, coarse models | Matching fields to farms |
| District or county statistics | Regional regression with aggregated features | Coarse; few samples per year; ecological fallacy |
| None | Nothing credible | Report as a limitation |

Open-data prototype idea (verify before use): if municipal or district yield statistics exist for the chosen region (for example IBGE municipal agricultural statistics for Brazil; access route and licence unchecked), a regional regression from aggregated crop-area and vegetation features is a realistic prototype. It supports regional claims only, never field-level claims, and the few samples per year must be stated plainly. This keeps Module C buildable without any ground truth of our own.

Decision options: (1) go with field-level scope, (2) reduced scope with district-level regression, (3) feasibility study only: design, data requirements, a prototype on whatever exists, and an honest statement of what is needed. Record the decision as an ADR with evidence (counts of records, years, crops, spatial coverage). Ask the user before choosing.

Use DATASET_DISCOVERY for yield sources and, only if the user later gets farm access, the ground-truth collection protocol (out of scope now). Record what sample size the data gives and what that can and cannot support statistically.

## 2. Requirements seed (finalise at Gate C0)

R-C-01 produce a yield estimate with an uncertainty interval per parcel or per region; R-C-02 evaluate with leave-one-year-out and leave-region-out; R-C-03 provide in-season forecasts at several dates; R-C-04 document limits of validity.

## 3. Approach (only what the data supports)

1. Trivial baselines: historical mean, linear trend.
2. Interpretable features from time series: peak vegetation index, seasonal integral, timing of peak, growth rate, stress indicators from Module B, cumulative rainfall and temperature, growing degree days.
3. Regularised linear models and gradient boosting on those features.
4. Deep models only if data volume justifies them (usually it does not).
5. Crop-model-informed features as an optional extension (verify what is available and licensed).

Evaluation: error metrics in real units (for example tonnes per hectare), relative error, comparison to the trivial baselines, prediction intervals and their coverage, per-year and per-region breakdown. Models must beat baselines out of sample to count.

## 4. Contract

Output per parcel or region and season: id, season, crop, forecast_date, predicted_yield, lower, upper, features_version, model_version. Add to `docs/architecture/interfaces.md` and `tests/contracts/`.

## 5. Anti-patterns

- Random splits across years or neighbouring fields (leakage). Use leave-one-year-out and leave-region-out.
- Using information from after the forecast date when claiming an in-season forecast.
- Deep networks on a handful of samples.
- Reporting R-squared alone, or reporting it against a weak baseline.
- Training on district statistics and presenting field-level claims.
- Hiding that the target is noisy or biased (self-reported yields, different measurement methods).
- Letting yield forecasts depend on crop-type labels from Module A without carrying classification error forward.

## 6. Teaching hooks

Regression metrics; bias and variance with small data; feature engineering from time series; temporal validation; prediction intervals; limits of ML versus mechanistic crop models.
