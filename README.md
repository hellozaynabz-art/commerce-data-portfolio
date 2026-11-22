# Zaynab Zennour · Retail & Ecommerce Data Portfolio

[Explore the portfolio](https://hellozaynabz-art.github.io/commerce-data-portfolio/) · [About Zaynab](https://hellozaynabz-art.github.io/commerce-data-portfolio/about.html) · [Contact](https://hellozaynabz-art.github.io/commerce-data-portfolio/contact.html)

Three independent, completed public-data projects. Each includes executable analysis, actual computed results, an interactive dashboard, data definitions, and honest limitations. These are portfolio studies, not employer datasets or claims of production impact.

| Project | Business question | Evidence | Open |
| --- | --- | --- | --- |
| Revenue & retention | Where does revenue come from, and who returns? | £8,558,034.76 net merchandise sales analyzed; 62.6% observed repeat-buyer share | [Code](revenue-retention) · [Dashboard](https://hellozaynabz-art.github.io/commerce-data-portfolio/revenue-retention.html) |
| Retail demand planning | Does a model beat a weekly baseline? | 13.9% lower held-out MAE for validation-selected methods | [Code](demand-planning) · [Dashboard](https://hellozaynabz-art.github.io/commerce-data-portfolio/demand-planning.html) |
| Ecommerce conversion | How does a score threshold change precision and recall? | 0.337 average precision vs. 0.207 baseline | [Code](conversion-intelligence) · [Dashboard](https://hellozaynabz-art.github.io/commerce-data-portfolio/conversion-intelligence.html) |

## Live AI demos

[Try the chatbot, agent, reusable skill, and connected retail plugin](https://hellozaynabz-art.github.io/commerce-data-portfolio/ai-demos.html). Visitors can describe their own tasks. See [AI_DEMOS.md](AI_DEMOS.md) for scopes, privacy, review controls, and usage limits.

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

`python run_all.py` runs each analysis and exports `portfolio-data.json`. `build_site.py` regenerates the eight public pages from the results. The three data projects run without an API key. The live AI demos use a separate protected service; no key is included here.

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
