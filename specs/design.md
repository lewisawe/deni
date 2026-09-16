# Deni: Design

> Spec 2 of 3. Frozen 14 Sep 2026. Realizes requirements.md. Fuller rationale in
> ../architecture.md.

## Architecture overview

```
                 ┌───────────────────────────┐
  Web chat UI ──►│                           │
  (EN/SW/Sheng)  │      FastAPI backend      │──► AWS Bedrock (Converse)
                 │   (one service, stateless │     Nova 2 Lite / Nova Pro
  USSD  ────────►│    re: user data)         │
  (Africa's      │                           │──► (no user-data persistence)
   Talking       │  cost engine (deterministic)
   sandbox) ────►│  licence check            │
                 │  recourse router          │──► bundled data packs (JSON/SQLite)
                 │  doc generator            │      lenders / products / rules /
                 └───────────────────────────┘      forums / strings / templates
```

- One backend serves both surfaces; the USSD callback and the chat API call the same
  core services. (R8)
- Money math and legal facts are deterministic; AI only parses, translates, phrases,
  and drafts. (R1, R6, R14)
- No server-side user-data store; case files live client-side. (R10)

## Components

### 1. Cost engine (deterministic): R1
- Pure functions: `total_payable`, `total_cost_over_principal`, `effective_rate/apr`,
  `markup_vs_cash`. Inputs: principal/cash price, deposit, instalment, frequency,
  term, fees. Outputs: figures + a structured breakdown of the arithmetic.
- Fully unit-tested. This is the trust core; it must be provably correct and it must
  expose its working (R1 "show the arithmetic").

### 2. Offer parser (AI): R2
- Nova 2 Lite (multimodal) extracts offer fields from pasted SMS text or an uploaded
  screenshot into the cost-engine input schema.
- Output validated against the schema; low-confidence fields flagged for user
  confirmation before compute. Never auto-proceeds on uncertainty.

### 3. Licence & findings check: R3, R7
- Looks up the lender in `lenders.json` (dated CBK licensed-DCP list + named
  companies + any regulator/court finding with citation).
- Returns status + source + data-date + conditional enforcement note if unlicensed.

### 4. Risk descriptor: R4
- From `products.json`, states the default consequence for the product's security type
  (device lock / repossession / joint-registration / group guarantee).

### 5. Alternative finder: R5
- Filters `products.json` for licensed products in the same category, ranks by true
  cost via the cost engine, returns the cheapest one or two.

### 6. Recourse router (deterministic decision, AI phrasing): R6, R13
- Maps a user's described problem to a scenario key in `rules.json`.
  - Scenario detection: Nova Pro classifies free-text into a fixed scenario set; the
    *rule, forum, condition, and citation are read from `rules.json`*, never generated.
- Returns: legal statement (from data) + forum (from `forums.json`) + condition +
  citation/date + the complaint template id.

### 7. Document generator (AI fills fixed template): R6, R10
- Nova Pro fills a fixed complaint/demand/dispute template with the user's facts.
- Legal basis, addressee, and citations are hard-coded in the template; the model
  supplies only the narrative/fact fields. Redacts identifying data by default.
- Emits a case reference (client-generated) + evidence checklist.

### 8. i18n layer: R11
- `strings/en.json`, `strings/sw.json`, `strings/sheng.json`. All UI + explanation
  scaffolding keyed. Adding a language = adding a file (proves FR/PT/AR scalability).
- AI explanations generated in the selected language (Nova supports 200+).

### 9. Channels
- **Chat UI (R2, R9):** SPA, Tailwind, text-first; number/icon-first result cards;
  audio playback of the explanation; high-contrast + ARIA/screen-reader semantics.
- **USSD (R8):** Africa's Talking sandbox channel (`*384*NNNN#`); backend callback
  implements the `CON`/`END` stateless-replay protocol; offers true-cost decode +
  licence check as a menu tree. Real against the AT gateway simulator; labelled
  "sandbox" (R14).

## Data model (the substance: hand-built, each field sourced), R7, R12

Per-country pack (Kenya first), each file isolatable for R12:

- `lenders.json`: name, type, cbk_licensed{bool,date,source}, findings[{body,summary,
  citation,date}].
- `products.json`: lender, category (app-cash|payg-device|moto-car|microfinance),
  cash_price?, deposit, instalment{amount,frequency}, term, fees[], security_type,
  security_note, sources[].
- `rules.json`: scenario_key → {law_statement, condition, forum_key, citation, date}.
- `forums.json`: forum_key → {name, channel, address, what_to_include, template_id}.
- `templates/`: complaint/demand/dispute bodies with fixed legal basis + fillable
  fact slots.
- `strings/{en,sw,sheng}.json`: UI + explanation scaffolding.

## AI integration (AWS Bedrock): R14

- Access: set `AWS_PROFILE` and `AWS_REGION` in your environment; region `us-east-1` (verified working 14 Sep).
- Converse API. Model IDs (verified):
  - Parse/explain/translate → `us.amazon.nova-2-lite-v1:0` (fallback bare
    `amazon.nova-lite-v1:0`).
  - Classify scenario / draft docs → `us.amazon.nova-pro-v1:0`.
- Guardrails: schema-validate parser output; scenario/rule/citation come from data;
  model temperature low for extraction/classification; never persist prompts.

## Requirements → components trace

| Req | Component(s) |
|---|---|
| R1 | Cost engine |
| R2 | Offer parser + chat UI confirm step |
| R3 | Licence check + lenders.json |
| R4 | Risk descriptor + products.json |
| R5 | Alternative finder |
| R6 | Recourse router + rules.json + forums.json + doc generator |
| R7 | All data carry source+date; UI renders them |
| R8 | USSD channel + shared core |
| R9 | Chat UI a11y (icon-first, audio, contrast, ARIA) |
| R10 | Stateless backend, client-side case files, redaction |
| R11 | i18n layer |
| R12 | Per-country pack isolation |
| R13 | Recourse router always returns a next action |
| R14 | Bedrock Nova usage + honesty labelling |

## Key design decisions (and why)

1. **AI never computes money or states law.** Correctness + traceability + no
   hallucinated law. Biggest trust decision.
2. **One backend, two channels.** Chat and USSD share the cost/licence/recourse core;
   no duplicated logic.
3. **Per-country pack.** Scalability is a data swap, demonstrated by the isolation, not
   claimed.
4. **Stateless re: user data.** Privacy by architecture, not policy.
5. **Deterministic scenario→rule mapping.** The model picks the bucket; the law is
   read from data. Wrong classification is recoverable; hallucinated law is not.
