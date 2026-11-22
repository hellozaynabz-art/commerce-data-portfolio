# Retail Demand Planning: A Forecast Must Beat a Baseline

[Interactive dashboard](https://hellozaynabz-art.github.io/commerce-data-portfolio/demand-planning.html) · [Portfolio](https://hellozaynabz-art.github.io/commerce-data-portfolio/)

## Problem and product

Test whether a model can improve next-day unit-sales planning for five frequently ordered products. Built a reproducible chronological backtest and a dashboard comparing actuals, selected forecasts, and a weekly baseline.

## Evaluation

| Method | MAE (units/SKU-day) | WAPE | Mean signed error |
| --- | ---: | ---: | ---: |
| Weekly seasonal baseline | 87.67 | 100.7% | -5.25 |
| Gradient boosting for every SKU (comparison only) | 63.41 | 72.8% | -22.57 |
| Validation-selected method per SKU | 75.46 | 86.6% | -11.70 |

The selected methods reduced MAE by **13.9%** against the weekly baseline on 150 SKU-days. However, **86.6% WAPE remains high**. This is a useful benchmark, not production-ready demand planning.

## Method and leakage controls

1. Choose the five most frequently ordered UK SKUs using pre-October data only.
2. Aggregate positive units daily, Dec 2010–Nov 2011. A no-sale date becomes zero observed sales; availability is unknown.
3. Features: lags 1/7/14/28, shifted 7/28-day means, weekday, month. No target-day sales enter features.
4. Train through September; compare October validation MAE to last-week sales. Choose one method per SKU.
5. Refit through October. Evaluate **one-day-ahead** predictions for each November day using prior observed actuals. This is not a 30-day forecast from a single origin.
6. Keep the method selected on validation, even where the alternate model looks better on the test set.

2 of five products selected gradient boosting. Hyperparameters were fixed (150 iterations, 7 leaves, L2=2, seed=42). MAE is averaged across SKU-days, while the dashboard's all-product chart sums units across SKUs. WAPE = total absolute error / total observed units.

## Planning scenario

The interactive calculator multiplies average held-out predicted daily units by coverage days and a user-selected buffer. It is **illustrative**, not an inventory policy: no on-hand stock, open orders, service levels, or lead-time distribution is supplied.

## Limits and next steps

Only five SKUs and one holdout month; no stockouts, promotions, prices, holidays or bulk-order features. Actual sales are not unconstrained demand. Large errors and underforecast bias require review. Next: rolling-origin tests, prediction intervals, richer drivers, and a monitored planner pilot. No savings or stockout improvement is claimed.

## Run

From the repository root, install `requirements.txt` in a Python 3.12 environment. Run the command below. Raw data is downloaded from the official source when absent, and input hashes are verified.

```sh
python demand-planning/analysis.py
```

## Files

- `analysis.py`: selection, lag features, training, baseline, backtest.
- `backtest.csv`: every held-out prediction and actual.
- `results.json`: per-SKU method selection and evaluation.

## Source

Chen, D. (2015). Online Retail, UCI. https://doi.org/10.24432/C5BW33 · CC BY 4.0. See [data provenance](../DATA_SOURCES.md).
