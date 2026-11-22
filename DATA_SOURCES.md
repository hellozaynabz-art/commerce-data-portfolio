# Data sources and transformations

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
