# Deni — Requirements

> Spec 1 of 3 (requirements → design → tasks). Frozen 14 Sep 2026.
> OSF × Andela hackathon. Cross-track: Transparency (primary) + Safety + Stability.
> Source docs: ../concept.md, ../lifecycle-and-recourse.md, ../scope-asset-financing.md,
> ../pre-build-audit.md.

## Product summary

Deni tells a Kenyan borrower what a loan will really cost, what the lender can take if
they miss a payment, and whether what they were told is legal — before they sign,
while things go wrong, and after harm is done — over a WhatsApp-style chat and a
functional USSD flow, in English, Kiswahili, and Sheng. When warranted, it prepares a
complaint to the correct public body (CBK, ODPC, CAK, courts, CRB) with a case
reference.

## Users

- **Primary:** a low-to-middle-income Kenyan considering or holding consumer credit —
  app cash loan, PAYG device (M-KOPA-type), motorbike/car financing (Watu/Mogo-type),
  or secured/group microfinance (KWFT-type). Often on a feature phone or low data,
  varied literacy, English/Kiswahili/Sheng speaker.
- **Secondary:** a helper (friend, chief, paralegal, CSO worker) assisting a borrower.

## Requirements (EARS-style acceptance criteria)

### R1 — True-cost decode (BEFORE) [Transparency]
- WHEN a user enters a loan offer (deposit, instalment amount, frequency, term, fees),
  THE SYSTEM SHALL compute and display the total amount payable, the total cost over
  the cash/principal, and an effective interest figure (APR where a term is defined).
- WHEN a cash price is known for an asset-financed product, THE SYSTEM SHALL display
  the markup vs cash price as an amount and a percentage.
- THE SYSTEM SHALL show the arithmetic used, not just the result.
- THE SYSTEM SHALL NOT use the AI model to compute any monetary figure; all money math
  is deterministic code.

### R2 — Offer capture by multiple inputs [Accessibility]
- WHEN a user types the numbers, THE SYSTEM SHALL accept structured entry.
- WHEN a user pastes an SMS offer or uploads a screenshot, THE SYSTEM SHALL use the AI
  model to extract the offer fields and SHALL display them for user confirmation
  before computing.
- WHEN extraction is uncertain, THE SYSTEM SHALL ask the user to confirm or correct the
  fields rather than proceeding silently.

### R3 — Licence & disclosure check [Transparency / gov engagement]
- WHEN a lender is identified, THE SYSTEM SHALL check it against a bundled, dated CBK
  licensed-Digital-Credit-Provider dataset and state licensed / not-on-list, with the
  data date and source.
- IF the lender is not on the licensed list, THE SYSTEM SHALL state that an unlicensed
  digital lender may not be able to lawfully enforce repayment (citing the 2026 ruling)
  and SHALL phrase this as conditional information, not a guarantee.
- WHERE a regulator or court finding against a named lender exists in the dataset, THE
  SYSTEM SHALL surface it with its citation and date.

### R4 — What's at risk [Transparency / Safety]
- WHEN a product is asset-secured, THE SYSTEM SHALL state plainly what can happen on
  default: device remote-lock, repossession, jointly-registered collateral seizure, or
  group-member liability, as applicable to that product.

### R5 — Cheaper alternative (forward arc) [Stability]
- WHEN an offer is costly or the lender unlicensed, THE SYSTEM SHALL show at least one
  licensed alternative with its true cost, so the user leaves with a better option.

### R6 — Know-your-rights + recourse routing (DURING/AFTER) [Safety / gov engagement]
- WHEN a user describes a problem (harassment, contacts scraped, threats,
  repossession, misleading terms, unlicensed lender chasing them, wrongful CRB
  listing), THE SYSTEM SHALL map it to a known scenario and return: what Kenyan law
  says, the responsible public body, the condition under which recourse applies, and a
  source citation with date.
- THE SYSTEM SHALL route to the correct forum per scenario: ODPC (data abuse), CBK
  (DCP conduct / unlicensed), CAK (misleading terms), court (wrongful repossession),
  CRB (wrongful listing).
- THE SYSTEM SHALL generate a pre-filled complaint/demand/dispute document for that
  forum and issue the user a case reference and an evidence checklist.
- THE SYSTEM SHALL state "this is not legal advice," phrase recourse conditionally
  ("this may be unlawful if…"), and SHALL NOT promise an outcome.
- THE SYSTEM SHALL NOT allow the AI model to state a legal conclusion or citation on
  its own; legal statements and citations come from a fixed rules dataset, the model
  only rephrases/translates.

### R7 — Trust & verification [Constraint 1]
- THE SYSTEM SHALL attach a source and a date to every factual claim (licence status,
  legal rule, product terms).
- WHERE data may change (licence list, product terms), THE SYSTEM SHALL show when it
  was last updated.

### R8 — Low bandwidth & basic devices [Constraint 2]
- THE SYSTEM SHALL provide a functional USSD flow (via Africa's Talking sandbox) that
  performs at least the true-cost decode and licence check without a smartphone,
  internet, or app install.
- THE SYSTEM SHALL keep the web surface text-first and usable on unreliable
  connections; no large downloads required to get a result.

### R9 — Accessibility & inclusion [Constraint 3]
- THE SYSTEM SHALL present results number/icon-first so the key figure is graspable
  without reading prose.
- THE SYSTEM SHALL offer an audio rendering of the explanation.
- THE SYSTEM SHALL meet high-contrast and screen-reader semantics on the web surface.

### R10 — Privacy & security [Constraint 4]
- THE SYSTEM SHALL NOT require a login.
- THE SYSTEM SHALL NOT persist a user's loan or complaint data on the server;
  case files are held client-side and are exportable/printable.
- WHEN calling the AI model, THE SYSTEM SHALL send only the data needed and SHALL NOT
  persist prompts beyond the request.
- THE SYSTEM SHALL redact identifying data by default in generated complaint packets.

### R11 — Multilingual [Constraint 5]
- THE SYSTEM SHALL operate in English, Kiswahili, and Sheng, selectable by the user.
- THE SYSTEM SHALL store all user-facing strings in a config-driven layer such that
  adding a language (e.g. French, Portuguese, Arabic) is adding a strings file, not a
  code change.

### R12 — Local relevance & adaptability [Constraint 6]
- THE SYSTEM SHALL reflect Kenyan lenders, products, regulators, and law.
- THE SYSTEM SHALL isolate country-specific data (lenders, products, rules, forums,
  fee math) into a per-country pack so another country can be added by swapping the
  pack.

### R13 — Clear next steps [Constraint 7]
- THE SYSTEM SHALL, at the end of every flow, state a concrete next action: a better
  option to take, a body to contact, a document to file, or what to carry — never end
  at "this is bad."

### R14 — AI usage & honesty [judging: AI Coding Usage; brief: idea provenance]
- THE SYSTEM SHALL use AWS Bedrock Nova for parsing, translation/explanation, scenario
  interpretation, and document drafting only.
- The project SHALL document (in the written summary) that the capstone idea came from
  the builder's lived experience, and that AI supported the build only.
- Any simulated or sandbox element (USSD sandbox shortcode) SHALL be labelled as such
  in the demo, README, and deck; no production capability shall be implied that does
  not exist.

## Out of scope (state on the "what's next" slide)

Live scraping of app stores; real regulator/CRB API integration; user accounts; every
lender/product; other countries as built packs (show the mechanism, not built packs);
in-app payments; automated filing on the user's behalf.

## Acceptance for the sprint (definition of done for the demo)

A user can, in one continuous run: enter/paste/snap an M-KOPA / Watu / Mogo / KWFT /
app-loan offer → see the true cost and markup with the math → see licence status and
what's at risk → get a cheaper licensed option → describe a "during" problem → receive
the law + forum + a generated complaint + case reference — in EN/SW/Sheng, on the chat
UI and via the USSD flow, with sources and dates on every claim and "not legal advice"
shown.
