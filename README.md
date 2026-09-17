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
  and share** (copy, WhatsApp, image, or PDF) with a case reference. Your description is
  **redacted on your device** (phone numbers, IDs, names stripped) before anything is
  sent, and the text is never stored on the server.
- **Stop the contact now**: alongside the slow regulator complaint, Deni drafts a
  **cease-and-desist letter you send straight to the lender** demanding the abusive
  contact stop, immediate and protective, backed by the Data Protection Act (Kenya) or
  POPIA (South Africa).
- **Helper workspace**: a chief, paralegal, or CSO worker helping several borrowers can
  keep those cases in one place, **on their device only**, and run the same engine per
  person.

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

See `../INTEGRATION.md` for the exact sandbox setup for both channels.

## Two countries, one engine (scalability)

Everything country-specific (lenders, products, rights, forums, templates, the
licensing authority, the currency, the languages, example lenders) lives in a
per-country data pack. `data/ke/` is Kenya; `data/za/` is South Africa. The app has a
country selector, and switching it changes every surface: the regulator named (CBK vs
NCR), the law cited, the currency shown (KES vs rand), the languages offered (Kenya:
English, Kiswahili, Sheng; South Africa: English), and the public bodies routed to.
Adding a country is adding a folder, not changing code.

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
```

Supporting docs live one level up, alongside the submission package:
`../INTEGRATION.md` (USSD + WhatsApp sandbox setup), `../SUGGESTIONS.md` (roadmap),
and `../submission/` (demo script, pitch deck, written summary).

## AI usage summary

Two separate things, kept separate on purpose.

**AI in the running product (assists only).** AWS Bedrock Amazon Nova (Nova 2 Lite for
parsing/explanation, Nova Pro for scenario classification and complaint drafting), via
the Converse API. The model extracts, translates, classifies, and fills fixed
templates; it never computes a figure or states the law on its own. The capstone idea
comes from the builder's lived experience of predatory lending in Kenya; AI supported
the build only.

## How AI coding tools built Deni

The idea is the builder's own. AI was the tool that turned it into working software,
and the workflow was deliberate, not vibe-coding.

- **Spec-first, in three frozen documents.** The build ran through `specs/`:
  `requirements.md` (EARS-style acceptance criteria, one per constraint and track) ,
  then `design.md` (architecture, the money-is-code / AI-assists-only boundary), then
  `tasks.md` (an executable, demo-first plan where each task names its requirement refs
  and a demo checkpoint). AI drafted and refined each document against the brief, and
  every later change traces back to a requirement.
- **The boundary was a design decision AI enforced, not a happy accident.** The rule
  "the model never states a number or a law" is written into the specs and realized in
  code: `cost_engine.py` computes, the data packs hold every legal statement and
  citation, and the model only rephrases or fills slots. That is what makes the output
  verifiable.
- **Data packs were generated then human-checked.** AI helped assemble the per-country
  packs (lenders, products, rules, forums, templates) into a fixed shape, each fact
  carrying a source URL and a date. A human verified the sources; the code treats the
  files as the source of truth.
- **Tests came with the logic.** The parts that must be correct have tests
  (`backend/test_cost_engine.py`, `backend/test_whatsapp.py`), so the deterministic core
  is provably right and refactors (like making the licence check country-agnostic) were
  safe.
- **One engine, many surfaces.** AI helped factor the civic logic so the web app,
  WhatsApp, and USSD all call the same functions, and so adding a country is adding a
  `data/<cc>/` folder rather than changing code.
