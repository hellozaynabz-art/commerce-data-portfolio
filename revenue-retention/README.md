# Revenue & Retention: Retail Decision Dashboard

[Interactive dashboard](https://hellozaynabz-art.github.io/commerce-data-portfolio/revenue-retention.html) · [Portfolio](https://hellozaynabz-art.github.io/commerce-data-portfolio/)

## Problem and product

Help a retail team reconcile sales and credits, identify customer concentration, and design lifecycle experiments. Built a Python cleaning pipeline, executed SQL metrics, an interactive market/metric filter, customer segments, and observed cohort analysis.

## Measured findings

- **£8,558,034.76 net merchandise sales** across Jan–Nov 2011: £8,841,679.90 positive sales less £283,645.14 credit lines.
- **62.6% observed repeat-buyer share** among 4,168 identified customers.
- **86.5% of gross sales have a customer ID.** Anonymous sales remain in revenue reporting and are excluded from customer analysis.
- Raw audit: 5,268 exact duplicate rows and 135,080 rows missing CustomerID. Final Jan–Nov merchandise population: 464,227 lines.

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

## Run

From the repository root, install `requirements.txt` in a Python 3.12 environment. Run the command below. Raw data is downloaded from the official source when absent, and input hashes are verified.

```sh
python revenue-retention/analysis.py
```

## Files

- `analysis.py`: end-to-end cleaning, SQL execution, cohorts, and reconciliation.
- `metrics.sql`: executed monthly metric query.
- `monthly-revenue.csv`, `customer-segments.csv`, `cohort-retention.csv`, `top-products.csv`: computed evidence.
- `results.json`: complete dashboard payload and audit summary.

## Source

Chen, D. (2015). Online Retail, UCI. https://doi.org/10.24432/C5BW33 · CC BY 4.0. See [data provenance](../DATA_SOURCES.md). Independent portfolio study, not employer work.
