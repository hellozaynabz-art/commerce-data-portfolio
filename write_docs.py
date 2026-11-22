from pathlib import Path
import json
R=Path(__file__).resolve().parent
D={s:json.loads((R/s/'results.json').read_text()) for s in ['revenue-retention','demand-planning','conversion-intelligence']}
rev=D['revenue-retention']['summary'];fore=D['demand-planning']['summary'];conv=D['conversion-intelligence']['summary']
base='https://hellozaynabz-art.github.io/commerce-data-portfolio/'
(R/'README.md').write_text(f'''# Zaynab Zennour · Retail & Ecommerce Data Portfolio

[Explore the portfolio]({base}) · [About Zaynab]({base}about.html) · [Contact]({base}contact.html)

Three independent, completed public-data projects. Each includes executable analysis, actual computed results, an interactive dashboard, data definitions, and honest limitations. These are portfolio studies, not employer datasets or claims of production impact.

| Project | Business question | Evidence | Open |
| --- | --- | --- | --- |
| Revenue & retention | Where does revenue come from, and who returns? | £{rev['net_sales']:,.2f} net merchandise sales analyzed; {rev['repeat_share']:.1%} observed repeat-buyer share | [Code](revenue-retention) · [Dashboard]({base}revenue-retention.html) |
| Retail demand planning | Does a model beat a weekly baseline? | {fore['mae_change']:.1%} lower held-out MAE for validation-selected methods | [Code](demand-planning) · [Dashboard]({base}demand-planning.html) |
| Ecommerce conversion | How does a score threshold change precision and recall? | {conv['test']['average_precision']:.3f} average precision vs. {conv['baseline']['average_precision']:.3f} baseline | [Code](conversion-intelligence) · [Dashboard]({base}conversion-intelligence.html) |

## Reproduce everything

Python 3.12 was used for the recorded run. Create an isolated environment, install the pinned requirements, and run:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python common.py
python run_all.py
python write_docs.py
python build_site.py
python -m unittest -v test_projects.py
python -m http.server 8765
```

Open `http://localhost:8765`. The first run downloads two official UCI archives (about 24 MB total); later runs use the local cache. A recorded SHA-256 mismatch stops the build for review. Raw archives are excluded from Git. Model fitting is deterministic with seed 42; small numerical variation across hardware is possible.

`python run_all.py` runs each analysis and exports `portfolio-data.json`. `build_site.py` regenerates the seven public pages from the results. No paid API, account, database server, or secret is needed.

## Repository map

- `revenue-retention/`: Python analysis, executed SQL, revenue/cohort/segment CSVs, results, project notes.
- `demand-planning/`: chronological backtest, model comparison, forecast CSV, project notes.
- `conversion-intelligence/`: training/evaluation, holdout scores, feature importance, project notes.
- `common.py`: source downloads, checksums, common retail preparation.
- `DATA_SOURCES.md` and `data-provenance.json`: provenance, licenses, and exact input hashes.
- `test_projects.py`: reconciliation, leakage, split, and evaluation checks.
- Root HTML, CSS, and JavaScript: buildless, responsive portfolio and dashboards.

## Important distinctions

The dashboards use computed public-data results. The forecasting and classification projects train real machine-learning models; they do not call an LLM. Results are historical and are not live store data. Proposed business actions are recommendations to test, not realized savings or causal lift. The existing [AI chatbot and agent studio](https://hellozaynabz-art.github.io/analytics-portfolio/ai-products.html) is a separate project and remains unchanged.

Published with GitHub Pages from the repository root. No tracking or visitor data collection is implemented.

## Credits and licensing

Original code and design: MIT. Dataset-derived outputs: CC BY 4.0, with the original UCI citations in [DATA_SOURCES.md](DATA_SOURCES.md). Layout inspiration: Edward Ofori’s portfolio; all analysis and written project content here were created for this portfolio. No project results or visuals were copied from the reference.
''')
(R/'DATA_SOURCES.md').write_text('''# Data sources and transformations

## Online Retail

Chen, D. (2015). *Online Retail*. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

- Official page: https://archive.ics.uci.edu/dataset/352/online+retail
- License: Creative Commons Attribution 4.0 International (CC BY 4.0).
- 541,909 invoice-line records from a UK-based non-store retailer, December 2010 to December 2011; many customers are wholesalers. Values are in GBP.
- The local audit finds missing CustomerID values, despite the current UCI metadata summary saying no missing values. The workbook is the analytical source of truth.
- Common preparation: remove exact duplicate rows; keep stock codes matching five digits with optional letter, positive unit prices, and nonzero quantities. Exclude service/manual codes. Preserve negative credit lines for revenue reporting; positive non-cancelled lines form purchase/unit-sales analysis.
- Revenue analysis uses Jan–Nov 2011 to avoid incomplete December; forecasting uses Dec 2010–Nov 2011 and UK positive sales.
- Public outputs contain aggregates, SKU names, and daily product forecasts. Customer-level identifiers and raw transaction rows are not published.

## Online Shoppers Purchasing Intention

Sakar, C. & Kastro, Y. (2018). *Online Shoppers Purchasing Intention Dataset*. UCI Machine Learning Repository. https://doi.org/10.24432/C5F88Q

- Official page: https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset
- License: Creative Commons Attribution 4.0 International (CC BY 4.0).
- 12,330 sessions; UCI describes each session as a different user within one year.
- Keep identical feature rows because no session ID exists to establish duplication. Exclude PageValues to reduce target-leakage risk; reserve Month for chronological splitting.
- Published score outputs contain only month, visitor type, binary outcome, and model score—no user identifiers.

## Provenance and scope

Archives were retrieved and analyzed in November 2026. `data-provenance.json` records the exact download URLs, archive SHA-256 hashes, citations, and row counts. `common.py` checks existing hashes before reuse. Dataset-derived tables and visualizations are adaptations under CC BY 4.0. Original sources do not endorse this portfolio.

License details: https://creativecommons.org/licenses/by/4.0/

Historical observations do not establish current retail behavior or causal business impact. No private employer, client, or visitor data is used in these analyses.
''')
common='''## Run

From the repository root, install `requirements.txt` in a Python 3.12 environment. Run the command below. Raw data is downloaded from the official source when absent, and input hashes are verified.

'''
(R/'revenue-retention'/'README.md').write_text(f'''# Revenue & Retention: Retail Decision Dashboard

[Interactive dashboard]({base}revenue-retention.html) · [Portfolio]({base})

## Problem and product

Help a retail team reconcile sales and credits, identify customer concentration, and design lifecycle experiments. Built a Python cleaning pipeline, executed SQL metrics, an interactive market/metric filter, customer segments, and observed cohort analysis.

## Measured findings

- **£{rev['net_sales']:,.2f} net merchandise sales** across Jan–Nov 2011: £{rev['gross_sales']:,.2f} positive sales less £{rev['credit_value']:,.2f} credit lines.
- **{rev['repeat_share']:.1%} observed repeat-buyer share** among {rev['known_customers']:,} identified customers.
- **{rev['identified_revenue_share']:.1%} of gross sales have a customer ID.** Anonymous sales remain in revenue reporting and are excluded from customer analysis.
- Raw audit: {rev['duplicate_rows']:,} exact duplicate rows and {rev['missing_customer_rows']:,} rows missing CustomerID. Final Jan–Nov merchandise population: {rev['filtered_lines']:,} lines.

## How it works

1. Load the UCI workbook, verify checksum, and audit missingness/duplicates.
2. Deduplicate exact invoice lines; exclude non-product codes, free items, and zero quantities. Preserve credit-line signs.
3. Calculate monthly revenue in SQLite using `metrics.sql`; reconcile with Python totals.
4. Group identified positive-sale customers by distinct order count and recency at 1 Dec 2011.
5. Build cohorts by first purchase **observed within the reporting window**, measuring subsequent monthly purchasing.
6. Export CSV and JSON for a dependency-free browser dashboard.

## Definitions and decisions

- Gross sales: positive quantities × positive unit price, non-cancelled merchandise lines.
- Credits: absolute value of negative merchandise lines. These are **not matched product returns**.
- Net sales: signed merchandise value; not profit.
- Repeat buyer: at least two distinct positive-sale invoices during Jan–Nov.
- Active: last purchase within 60 days of 1 Dec; lapsed: more than 60 days.
- First observed cohort month is not necessarily true acquisition; all cohort calculations exclude missing IDs.

## Recommendation and limits

Test tailored outreach for active-repeat and lapsed-repeat groups, with randomized controls and net revenue/unsubscribe guardrails. Investigate high credit-value periods. **No measured uplift is claimed.** Exact duplicate removal is an assumption; repeated legitimate lines could be lost. Bulk orders are retained. One historical retailer with wholesale behavior cannot represent the broader market.

{common}```sh
python revenue-retention/analysis.py
```

## Files

- `analysis.py`: end-to-end cleaning, SQL execution, cohorts, and reconciliation.
- `metrics.sql`: executed monthly metric query.
- `monthly-revenue.csv`, `customer-segments.csv`, `cohort-retention.csv`, `top-products.csv`: computed evidence.
- `results.json`: complete dashboard payload and audit summary.

## Source

Chen, D. (2015). Online Retail, UCI. https://doi.org/10.24432/C5BW33 · CC BY 4.0. See [data provenance](../DATA_SOURCES.md). Independent portfolio study, not employer work.
''')
(R/'demand-planning'/'README.md').write_text(f'''# Retail Demand Planning: A Forecast Must Beat a Baseline

[Interactive dashboard]({base}demand-planning.html) · [Portfolio]({base})

## Problem and product

Test whether a model can improve next-day unit-sales planning for five frequently ordered products. Built a reproducible chronological backtest and a dashboard comparing actuals, selected forecasts, and a weekly baseline.

## Evaluation

| Method | MAE (units/SKU-day) | WAPE | Mean signed error |
| --- | ---: | ---: | ---: |
| Weekly seasonal baseline | {fore['baseline']['mae']:.2f} | {fore['baseline']['wape']:.1%} | {fore['baseline']['bias_units']:.2f} |
| Gradient boosting for every SKU (comparison only) | {fore['model']['mae']:.2f} | {fore['model']['wape']:.1%} | {fore['model']['bias_units']:.2f} |
| Validation-selected method per SKU | {fore['selected']['mae']:.2f} | {fore['selected']['wape']:.1%} | {fore['selected']['bias_units']:.2f} |

The selected methods reduced MAE by **{fore['mae_change']:.1%}** against the weekly baseline on 150 SKU-days. However, **{fore['selected']['wape']:.1%} WAPE remains high**. This is a useful benchmark, not production-ready demand planning.

## Method and leakage controls

1. Choose the five most frequently ordered UK SKUs using pre-October data only.
2. Aggregate positive units daily, Dec 2010–Nov 2011. A no-sale date becomes zero observed sales; availability is unknown.
3. Features: lags 1/7/14/28, shifted 7/28-day means, weekday, month. No target-day sales enter features.
4. Train through September; compare October validation MAE to last-week sales. Choose one method per SKU.
5. Refit through October. Evaluate **one-day-ahead** predictions for each November day using prior observed actuals. This is not a 30-day forecast from a single origin.
6. Keep the method selected on validation, even where the alternate model looks better on the test set.

{fore['ml_selected']} of five products selected gradient boosting. Hyperparameters were fixed (150 iterations, 7 leaves, L2=2, seed=42). MAE is averaged across SKU-days, while the dashboard's all-product chart sums units across SKUs. WAPE = total absolute error / total observed units.

## Planning scenario

The interactive calculator multiplies average held-out predicted daily units by coverage days and a user-selected buffer. It is **illustrative**, not an inventory policy: no on-hand stock, open orders, service levels, or lead-time distribution is supplied.

## Limits and next steps

Only five SKUs and one holdout month; no stockouts, promotions, prices, holidays or bulk-order features. Actual sales are not unconstrained demand. Large errors and underforecast bias require review. Next: rolling-origin tests, prediction intervals, richer drivers, and a monitored planner pilot. No savings or stockout improvement is claimed.

{common}```sh
python demand-planning/analysis.py
```

## Files

- `analysis.py`: selection, lag features, training, baseline, backtest.
- `backtest.csv`: every held-out prediction and actual.
- `results.json`: per-SKU method selection and evaluation.

## Source

Chen, D. (2015). Online Retail, UCI. https://doi.org/10.24432/C5BW33 · CC BY 4.0. See [data provenance](../DATA_SOURCES.md).
''')
(R/'conversion-intelligence'/'README.md').write_text(f'''# Ecommerce Conversion Intelligence: Evaluate the Trade-off

[Interactive dashboard]({base}conversion-intelligence.html) · [Portfolio]({base})

## Problem and product

Understand session patterns associated with purchase, and expose what changing a decision threshold does to precision, recall, and review volume. Built and compared logistic regression and random forest, with a later-month holdout and a browser threshold explorer.

## Model card

- **Task:** retrospective binary session classification; target `Revenue`.
- **Population:** {conv['raw_sessions']:,} UCI ecommerce sessions, each described as a different user.
- **Train:** observed months before October, {conv['train_sessions']:,} rows.
- **Validation:** October, {conv['validation_sessions']:,} rows.
- **Test:** November–December, {conv['test_sessions']:,} rows, held out from fitting/model selection.
- **Selected model:** {conv['chosen_model']} by October average precision.
- **Test AP:** {conv['test']['average_precision']:.4f}, versus {conv['baseline']['average_precision']:.4f} constant-score baseline.
- **Test ROC AUC:** {conv['test']['roc_auc']:.4f}; **Brier score:** {conv['test']['brier']:.4f}, versus {conv['baseline']['brier']:.4f} constant training-rate baseline.
- **Locked threshold:** {conv['locked_threshold']:.6f}, set at the 80th percentile of validation scores before refitting and testing.
- **At that threshold:** {conv['locked_result']['precision']:.1%} precision, {conv['locked_result']['recall']:.1%} recall, {conv['locked_result']['flagged']:,} flagged test sessions.

## Design decisions

`PageValues` is excluded because it is tied to transaction value and may leak outcome information. `Month` defines the split and is not a model input. Identical feature vectors are retained: UCI says rows belong to distinct users, and there is no session ID proving duplication.

Numerical fields receive median imputation and scaling; categorical codes are one-hot encoded with unknown-category handling. Preprocessing is fitted on training data only. Candidate models are evaluated on October AP. The chosen model is refit on pre-test rows, while the validation-chosen threshold stays fixed.

The dashboard's threshold slider is **exploratory**. Selecting a new threshold after viewing holdout performance requires new validation data. The published locked-threshold outcome remains separate.

Permutation importance reports mean AP reduction over three shuffles per feature on the holdout. It is diagnostic, not causal or a basis for retuning on the test set.

## Limits and appropriate use

Completed-session durations, bounce/exit metrics, and aggregate browsing features may be unavailable at a live decision point. This is **not an early-session intervention model**. Exact timestamps and real-time feature availability are unknown. Holiday-season shift, modest precision, and uncalibrated scores limit deployment. Most flagged sessions at the locked threshold do not purchase.

Next: collect point-in-time features, calibrate on a separate validation period, test across seasons, then run a randomized intervention experiment. No conversion lift or revenue gain is claimed.

{common}```sh
python conversion-intelligence/analysis.py
```

## Files

- `analysis.py`: preprocessing, model comparison, validation, holdout, importance.
- `holdout-predictions.csv`: month, visitor type, actual outcome, and model score.
- `session-summary.csv`: observed session counts and purchase rates.
- `results.json`: complete metrics, confusion counts, and thresholds.

## Source

Sakar, C. & Kastro, Y. (2018). Online Shoppers Purchasing Intention Dataset, UCI. https://doi.org/10.24432/C5F88Q · CC BY 4.0. See [data provenance](../DATA_SOURCES.md).
''')
print('Wrote repository and project documentation.')
