# Deni — architecture

> Frozen: 14 September 2026. Decisions locked: WhatsApp-style chat + USSD; AI assists;
> all named products modelled; AI = AWS Bedrock Nova Pro/Lite.

## Locked decisions

- **Channels:** WhatsApp-style web chat (primary demo surface) **and a genuinely
  functional USSD flow via Africa's Talking sandbox** (builder has a demo account).
  The AT sandbox provides a free USSD channel (e.g. `*384*NNNN#`) tested on their
  simulator: each keypress is POSTed to our callback URL; we reply with the
  `CON`/`END` protocol. So USSD is real against a real gateway — only the shortcode
  is a shared sandbox code, not a paid live one. HONESTY: say "live on Africa's
  Talking sandbox," never imply a public dialable production shortcode.
- **Languages: English, Kiswahili, Sheng.** Config-driven string layer (one file per
  language). Sheng is deliberate — it is the street language of young urban Kenyan
  borrowers, the exact audience, and it proves the language layer is a config swap
  (the brief's FR/PT/AR scalability point: adding a language = adding a strings file,
  demonstrated live with three).
- **Government engagement is foregrounded, not incidental.** Deni's civic core is
  teaching a citizen to *use public institutions they didn't know applied to them* —
  CBK's licensed-lender register, ODPC's data-protection complaint process, CAK's
  consumer-protection process, the courts, the CRB dispute mechanism. The product's
  through-line: "here is the government body whose job this is, and here is how to
  make it act." This is the "engage with governments and public services" scope line,
  answered directly.
- **AWS access — VERIFIED 14 Sep 2026.** Profile `simi-ops`, account 888577033943,
  region **us-east-1**. Bedrock Converse tested live and working (Nova Lite returned
  in ~305ms). Set the profile's region to us-east-1 (currently blank) or pass
  `--region`/`region_name` explicitly in code.
- **AI:** AWS Bedrock Amazon Nova via the **Converse API**. Confirmed working IDs:
  - **Nova v1 (bare model ID, on-demand OK):**
    - `amazon.nova-lite-v1:0` — fast, low-cost, multimodal, 300k ctx, 200+ langs
      (incl. Kiswahili). → screenshot/SMS parsing, plain-language explanations.
    - `amazon.nova-pro-v1:0` — stronger reasoning, multimodal. → recourse routing,
      complaint drafting, ambiguous-terms interpretation.
  - **Nova 2 (available; requires an INFERENCE PROFILE ID, not the bare ID):**
    - `us.amazon.nova-2-lite-v1:0` — verified working (~390ms). Newer gen ("Lite2").
    - `us.amazon.nova-pro-v1:0` (profile) — verified working.
    - Note: bare `amazon.nova-2-lite-v1:0` fails with "on-demand throughput isn't
      supported — use an inference profile." Always use the `us.` profile prefix for
      Nova 2.
  - **Choice:** default to **Nova 2 Lite (`us.amazon.nova-2-lite-v1:0`)** for
    parse/explain and **Nova Pro (`us.amazon.nova-pro-v1:0`)** for routing/drafting.
    Both verified. Keep v1 bare IDs as a no-profile fallback.
- **Math is deterministic, not AI.** True cost / APR / total-vs-cash is computed in
  code (auditable, correct, shown). AI never computes the money figure — it only
  extracts inputs and explains outputs. This is a trust + correctness decision.

## Stack

- **Frontend:** single-page web app, plain + Tailwind (fast, low-bandwidth, no heavy
  framework). Two surfaces: chat UI and a phone-style USSD simulator. Text-first,
  works degraded.
- **Backend:** one small FastAPI (Python) service. Endpoints for parse, cost,
  licence-check, recourse-route, draft-doc. Calls Bedrock server-side (keys never in
  the browser).
- **Data:** static JSON/SQLite bundled — lender registry, product models, legal-rule
  table, forum router. No user-data persistence server-side (privacy constraint);
  case files kept client-side and exportable/printable.
- **AI calls:** `boto3` / Bedrock Converse from the backend. Region us-east-1.

Rationale: mirrors the GovTrust lesson (FastAPI + SQLite + vanilla JS = judges clone
and run in a minute), and keeps it demoable on a laptop offline except the AI calls.

## Data model (the substance — hand-built, sourced)

1. **Lender registry** (`lenders.json`): name, type (app-cash | PAYG-device |
   moto/car | microfinance), CBK-licensed (bool + date + source), any regulator/court
   finding (with citation). Includes the CBK licensed-DCP list (dated) + named
   companies: M-KOPA, Watu, Mogo, KWFT, + app lenders.
2. **Product models** (`products.json`): per named product — cash price (where
   applicable), deposit, instalment amount + frequency + term, fees, what's secured
   and how (device lock / logbook / joint-registration / group guarantee). Each field
   sourced.
3. **Legal-rule table** (`rules.json`): scenario → what the law says → condition →
   forum → citation (from lifecycle-and-recourse.md). Drives the recourse router
   deterministically; AI phrases it, code decides it.
4. **Forum router** (`forums.json`): ODPC / CBK / CAK / court / CRB — address,
   channel, what to include, complaint template ID.
5. **Complaint templates**: ODPC data-abuse, CBK conduct/unlicensed, CAK misleading
   terms, CRB dispute. AI fills facts; template + legal basis are fixed.

## AI task split (which model does what, and guardrails)

| Task | Model | Guardrail |
|---|---|---|
| Parse pasted SMS / typed offer / screenshot → structured fields | Nova Lite (multimodal) | Output validated against a schema; user confirms before use |
| Explain true cost in plain Kiswahili/English | Nova Lite | Math comes from code, not the model; model only phrases it |
| Interpret an ambiguous "what's happening to me" description → scenario | Nova Pro | Maps to a fixed scenario in rules.json; never invents a right |
| Draft the complaint/demand letter | Nova Pro | Fills a fixed template; legal basis + citation are hard-coded, not generated |

Hard rule: **AI never states a legal conclusion or a number on its own.** Numbers are
computed; legal statements come from `rules.json` with citations. The model rephrases
and translates. This keeps every claim traceable (trust constraint) and avoids the
model hallucinating law — critical given the recourse content.

## Core flows

**Before:** user gives an offer (type/paste/snap) → Nova Lite parses → code computes
true cost + total-vs-cash → licence check against registry → Nova Lite explains in
chosen language → show cheaper licensed option. Save terms record.

**During:** user describes the problem → Nova Pro maps to scenario → code pulls the
legal rule + forum + condition from `rules.json` → Nova Pro drafts the complaint from
the fixed template with user's facts → issue case reference + evidence checklist.

**After:** same router → CRB dispute / lawyer packet / ODPC complaint generated.

## Privacy / trust (constraint fit)

- No login; no server-side storage of a user's loan or complaint data.
- Bedrock calls send only what's needed; no persistence of prompts beyond the request.
- Every displayed claim carries a source/citation and a date.
- "Not legal advice" + conditional phrasing enforced in the template layer.

## Demo posture

- Laptop, chat UI open (borrowed-device realism, like the borrower has no data on
  their own phone). USSD simulator shown alongside for the basic-phone story.
- Pre-seeded named products so the AI parsing + the shock number + the licence flag +
  the recourse letter all land in one continuous 60–90s run.
- Offline-tolerant except the Bedrock call; have a recorded fallback of the AI step.
