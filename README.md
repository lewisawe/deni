# Deni

**Know the real cost before you borrow.**

Deni tells a Kenyan borrower what a loan will really cost, whether the lender is
legally allowed to lend to or pursue them, and what they can do about harassment or
repossession — over a WhatsApp-style chat and USSD, in English, Kiswahili, and Sheng.

Built for the OSF × Andela "Information you can trust" hackathon.
Cross-track: **Transparency & Accountability** (primary) + **Safety, Reporting &
Protection** + **Stability & Social Cohesion**.

## What it does

Deni covers the whole loan lifecycle:

- **Before** — Pick a loan or paste the lender's SMS. Deni computes the **true cost**
  (total paid vs value received, markup %, and APR), shows the working, checks whether
  the lender is on **CBK's licensed list**, states **what they can take** if you
  default (device lock, repossession, seized collateral, group liability), and offers a
  **cheaper licensed alternative**.
- **During** — Describe a problem (harassment, contacts scraped, repossession,
  misleading terms, an unlicensed lender chasing you). Deni tells you **what Kenyan law
  says**, **which public body** handles it (ODPC, CBK, CAK, courts, CRB), and drafts a
  **complaint with a case reference**.
- **After** — Wrongful CRB listing or seized asset: Deni prepares the dispute/demand
  and the evidence checklist.

Covers app cash loans and asset financing: PAYG devices (M-KOPA-type), motorbike/car
financing (Watu/Mogo-type), and secured microfinance (KWFT-type).

## How it works

- **The money math is deterministic** — computed in code and shown, never by AI. The
  number is the whole point, so it is provably correct (see `backend/cost_engine.py`
  + tests).
- **AI (AWS Bedrock, Amazon Nova) assists only** — it reads a pasted SMS or screenshot
  into offer fields (you confirm before compute), explains the result in your language,
  classifies a described problem into a known scenario, and fills a fixed complaint
  template. **AI never states the law or a number on its own** — legal statements and
  citations are read from a data file.
- **Per-country data pack** (`data/ke/`) holds lenders, products, legal rules, forums,
  and complaint templates — each fact sourced and dated. Adding a country is swapping
  the pack.

## Run it (under a minute)

```bash
bash run.sh
# open http://127.0.0.1:8000
```

`run.sh` creates a venv, installs deps, and starts the server. AI features use AWS
Bedrock — set `AWS_PROFILE` and `AWS_REGION` (defaults: `simi-ops`, `us-east-1`). If
Bedrock is unreachable, the deterministic core (cost + licence + recourse via keyword
fallback) still works.

Run tests:
```bash
source .venv/bin/activate && python -m pytest backend/ -q
```

## Honesty (what Deni does NOT do)

- It **does not lend, block, freeze, or erase** anything, and cannot remove a CRB
  listing — it prepares the paperwork and points you to the body with the power.
- It is **not legal or financial advice.** Recourse is stated conditionally ("this may
  be unlawful if…") with a citation; it never promises an outcome.
- It **never calls a named lender a "scam."** It states verifiable facts: "not on
  CBK's licensed list as of <date>," or a regulator/court finding with its source.
- The **USSD** channel runs on the **Africa's Talking sandbox** (a shared test
  shortcode + simulator), not a paid production shortcode.
- Product figures are **representative** of publicly advertised structures and carry a
  data date; the cost engine computes from the shown inputs.

## Structure

```
backend/    FastAPI + cost engine + data loader + AI (Bedrock Nova) + recourse
frontend/   SPA (chat surface) + Timescale design tokens
data/ke/    Kenya pack: lenders, products, rules, forums, templates (sourced)
specs/      requirements → design → tasks → ui
```

## AI usage summary

AWS Bedrock Amazon Nova (Nova 2 Lite for parsing/explanation, Nova Pro for scenario
classification and complaint drafting), via the Converse API. The capstone idea comes
from the builder's lived experience of predatory lending in Kenya; AI supported the
build only.
