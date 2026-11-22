# Ecommerce Conversion Intelligence: Evaluate the Trade-off

[Interactive dashboard](https://hellozaynabz-art.github.io/commerce-data-portfolio/conversion-intelligence.html) · [Portfolio](https://hellozaynabz-art.github.io/commerce-data-portfolio/)

## Problem and product

Understand session patterns associated with purchase, and expose what changing a decision threshold does to precision, recall, and review volume. Built and compared logistic regression and random forest, with a later-month holdout and a browser threshold explorer.

## Model card

- **Task:** retrospective binary session classification; target `Revenue`.
- **Population:** 12,330 UCI ecommerce sessions, each described as a different user.
- **Train:** observed months before October, 7,056 rows.
- **Validation:** October, 549 rows.
- **Test:** November–December, 4,725 rows, held out from fitting/model selection.
- **Selected model:** Random forest by October average precision.
- **Test AP:** 0.3375, versus 0.2066 constant-score baseline.
- **Test ROC AUC:** 0.7084; **Brier score:** 0.1549, versus 0.1710 constant training-rate baseline.
- **Locked threshold:** 0.227459, set at the 80th percentile of validation scores before refitting and testing.
- **At that threshold:** 35.9% precision, 34.0% recall, 924 flagged test sessions.

## Design decisions

`PageValues` is excluded because it is tied to transaction value and may leak outcome information. `Month` defines the split and is not a model input. Identical feature vectors are retained: UCI says rows belong to distinct users, and there is no session ID proving duplication.

Numerical fields receive median imputation and scaling; categorical codes are one-hot encoded with unknown-category handling. Preprocessing is fitted on training data only. Candidate models are evaluated on October AP. The chosen model is refit on pre-test rows, while the validation-chosen threshold stays fixed.

The dashboard's threshold slider is **exploratory**. Selecting a new threshold after viewing holdout performance requires new validation data. The published locked-threshold outcome remains separate.

Permutation importance reports mean AP reduction over three shuffles per feature on the holdout. It is diagnostic, not causal or a basis for retuning on the test set.

## Limits and appropriate use

Completed-session durations, bounce/exit metrics, and aggregate browsing features may be unavailable at a live decision point. This is **not an early-session intervention model**. Exact timestamps and real-time feature availability are unknown. Holiday-season shift, modest precision, and uncalibrated scores limit deployment. Most flagged sessions at the locked threshold do not purchase.

Next: collect point-in-time features, calibrate on a separate validation period, test across seasons, then run a randomized intervention experiment. No conversion lift or revenue gain is claimed.

## Run

From the repository root, install `requirements.txt` in a Python 3.12 environment. Run the command below. Raw data is downloaded from the official source when absent, and input hashes are verified.

```sh
python conversion-intelligence/analysis.py
```

## Files

- `analysis.py`: preprocessing, model comparison, validation, holdout, importance.
- `holdout-predictions.csv`: month, visitor type, actual outcome, and model score.
- `session-summary.csv`: observed session counts and purchase rates.
- `results.json`: complete metrics, confusion counts, and thresholds.

## Source

Sakar, C. & Kastro, Y. (2018). Online Shoppers Purchasing Intention Dataset, UCI. https://doi.org/10.24432/C5F88Q · CC BY 4.0. See [data provenance](../DATA_SOURCES.md).
