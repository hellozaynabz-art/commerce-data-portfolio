# Live AI demos

[Open the demo page](https://hellozaynabz-art.github.io/commerce-data-portfolio/ai-demos.html)

One page, four choices:

- **Chatbot:** plain-language answers from fictional Everyday Shop return, delivery, and product policies, plus grounded explanations of the retail projects.
- **Agent:** model-selected shop-order, policy, payment, and historical project-data tools. Sample order #1042 has a duplicate $84 charge; #1043 has a delayed delivery. The agent can also explain forecast reliability or shopper-model tradeoffs. A fictional duplicate-charge reversal requires verified evidence and a human decision. No actual payments are possible.
- **Reusable skill:** three recipes (project brief, project review, stakeholder update) applied by a live model to the visitor's own task. Exports a reviewable SKILL.md draft; nothing is installed.
- **Connected plugin:** live function calling over computed public retail-project metrics, forecast evaluation, and conversion results. It is a working integration demo, not a browser extension or a connection to the visitor's store.

## Architecture

GitHub Pages serves the interface. The browser sends requests to Zaynab's existing protected AI service, which calls OpenAI's Responses API using a server-side key. No API key is in this repository. The service exposes `/api/demo`, `/api/decision`, and `/api/health`; its source is maintained separately.

Requests accept up to 800 characters; chatbot follow-ups include up to six previous messages. Agents/plugins can make at most five model calls per run. The existing shared daily budget is 20 model calls, and each visitor is limited to six runs per hour. Quotas and review decisions use durable storage. Limits are shared with the earlier portfolio's demos.

The service validates source identifiers and tool arguments, rejects arbitrary tools, bounds response length, and never exposes upstream error bodies. Prompts are not application-logged; OpenAI requests use `store:false`. OpenAI's API data policies still apply. A configured connection does not guarantee remaining quota; usage errors are shown explicitly without simulated fallback.

## Review and privacy

Use sample information. Model output can be wrong; source citations, tool results, and generated skill text can be inspected before downloading. Plugin data is historical UCI data, not live store information. Skill output is a draft, not an installed extension. Human approvals record a simulated receipt only.

Chat history stays in page memory. Start fresh, change demo, or leave the page to discard it. Result downloads contain the submitted task and AI output but exclude approval tokens.

## Verification

Service tests cover existing behavior, new-mode validation, strict tool permissions, verified citations, malformed output, context limits, durable quotas, and approval replay handling. Separate bounded live-model tests verify shop policies, duplicate-payment review, forecast evidence, a skill artifact, and retail-plugin results. Browser checks cover all four modes, downloads, review actions, loading/errors, and mobile navigation.

## Retail context and project connections

The new page sends `scenario: "retail"` for chatbot and agent requests. Earlier portfolio clients keep the existing Harbor behavior by default. Fictional shop orders are never joined to the historical UCI project datasets. The UI links to the revenue, forecasting, and conversion case studies and states that the demo does not prove business lift. Chatbot questions use supplied policy documents; the agent can inspect only the two sample orders and the allowlisted historical project tools. A failed payment lookup retries once and then requires human review.
