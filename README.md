# Deni

**Know your rights as a borrower.**

Deni helps a borrower understand what a lender can and can't legally do, check whether
the lender is licensed, see what a loan really costs, and take action with the right
public body, over the web, WhatsApp, and USSD, in English, Kiswahili, and Sheng. It
leads with rights and public facts, then backs them with the true-cost math. Built for
Kenya, and it already runs for South Africa by swapping a data pack.

Built for the OSF × Andela "Information you can trust" hackathon.
Cross-track: **Transparency & Accountability** (primary) + **Safety, Reporting &
Protection** + **Stability & Social Cohesion**.

## What it does

Deni turns rights and public facts into something an ordinary person can act on, across
the whole loan lifecycle:

- **Know your rights**: Browse, in plain language, what a lender can and can't legally
  do (call your contacts, seize an asset, list you with a bureau), each answer backed by
  the specific law and the public body that enforces it, with a source and date. Every
  right links straight into taking action on it.
- **Check a lender**: Look up whether a lender is on the licensing register (CBK in
  Kenya, the NCR in South Africa), and see the regulator and court findings on record
  against them, each sourced and dated. A public fact and a paper trail, made instant.
- **Check a loan's true cost**: Pick a loan or paste the lender's SMS. Deni computes the
  **true cost** (total paid vs value received, markup %, and APR), shows the working,
  states what they can take if you default, and offers a cheaper licensed alternative
  with the exact money you would save.
- **Take action**: Describe a problem (harassment, contacts scraped, repossession,
  misleading terms, an unlicensed lender, a wrongful bureau listing, or money to
  recover). Deni tells you what the law says, names **every** public body that applies
  (a single problem often has more than one), gives an interactive evidence checklist
  and the exact filing channel, and drafts a **complaint or claim you can edit in place
  and share** (copy, WhatsApp, image, or PDF) with a case reference.

Covers app cash loans and asset financing: PAYG devices (M-KOPA-type), motorbike/car
financing (Watu/Mogo-type), and secured microfinance (KWFT-type).

## Channels

Same civic engine, met where the user is:

- **Web** (`/app`): the full experience.
- **WhatsApp**: conversational near-full. Paste a loan and get the cost; type a lender
  name and get its status and findings; describe a problem and get the law, the body,
  and a prepared complaint. Works against the Twilio WhatsApp sandbox.
- **USSD**: the essentials on any feature phone with no internet: true cost of listed
  products, lender licence check, and read your rights. Runs on the Africa's Talking
  sandbox.

See `INTEGRATION.md` for the exact sandbox setup for both channels.

## Two countries, one engine (scalability)

Everything country-specific (lenders, products, rights, forums, templates, the
licensing authority, the currency, example lenders) lives in a per-country data pack.
`data/ke/` is Kenya; `data/za/` is South Africa. The app has a country selector, and
switching it changes every surface: the regulator named (CBK vs NCR), the law cited,
the currency shown (KES vs rand), the public bodies routed to. Adding a country is
adding a folder, not changing code.

## How it works

- **The money math is deterministic**: computed in code and shown, never by AI. The
  number is the whole point, so it is provably correct (see `backend/cost_engine.py`
  + tests).
- **AI (AWS Bedrock, Amazon Nova) assists only**: it reads a pasted SMS or screenshot
  into offer fields (you confirm before compute), explains the result in your language,
  classifies a described problem into a known scenario, and fills a fixed complaint
  template. **AI never states the law or a number on its own.** Legal statements and
  citations are read from a data file; the money is code.
- **Per-country data pack** holds lenders, products, legal rules, forums, and complaint
  templates, each fact sourced and dated.

## Run it (under a minute)

```bash
bash run.sh
# open http://127.0.0.1:8000
```

`run.sh` creates a venv, installs deps, and starts the server. AI features use AWS
Bedrock. Set `AWS_PROFILE` and `AWS_REGION` (default region `us-east-1`). If Bedrock is
unreachable, the deterministic core (cost + licence + recourse via keyword fallback)
still works.

Run tests:
```bash
source .venv/bin/activate && python -m pytest backend/ -q
```

## Honesty (what Deni does NOT do)

- It **does not lend, block, freeze, or erase** anything, and cannot remove a bureau
  listing. It prepares the paperwork and points you to the body with the power.
- It is **not legal or financial advice.** Recourse is stated conditionally ("this may
  be unlawful if…") with a citation; it never promises an outcome.
- It **never calls a named lender a "scam."** It states verifiable facts ("not on the
  licensed register as of <date>") or a regulator/court finding with its source.
- The **USSD** and **WhatsApp** channels run on provider **sandboxes** (Africa's
  Talking and Twilio), not a paid production shortcode or an approved WhatsApp Business
  number.
- The South Africa pack is a **demonstration pack**: it names real bodies and the real
  legal pattern with sources, at a lighter depth than the Kenya pack. Figures are
  representative and carry a data date; the cost engine computes from the shown inputs.

## Structure

```
backend/    FastAPI: cost engine, data-pack loader, AI (Bedrock Nova),
            recourse router, USSD + WhatsApp channels
frontend/   landing page + SPA (rights / lender / cost / action) + Timescale tokens
data/ke/    Kenya pack: lenders, products, rules, forums, templates (sourced)
data/za/    South Africa pack (demonstration): same shape, real SA bodies
specs/      requirements -> design -> tasks -> ui
INTEGRATION.md   USSD + WhatsApp sandbox setup
SUGGESTIONS.md   roadmap and ideas
```

## AI usage summary

AWS Bedrock Amazon Nova (Nova 2 Lite for parsing/explanation, Nova Pro for scenario
classification and complaint drafting), via the Converse API. The model extracts,
translates, classifies, and fills fixed templates; it never computes a figure or states
the law on its own. The capstone idea comes from the builder's lived experience of
predatory lending in Kenya; AI supported the build only.
