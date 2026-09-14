# Deni — concept spec

> Frozen: 14 September 2026 · OSF × Andela Hackathon
> Name: *Deni* = "debt" (Kiswahili). Track: Cross-track (Transparency + Stability +
> Safety).

## One sentence

Deni tells a Kenyan borrower what a loan will really cost, what the lender can take if
they miss a payment, and whether what they were told is legal — before they sign —
over USSD/WhatsApp, and prepares a filed complaint to the right regulator with a
receipt when the lender is unlicensed, misled them, or is collecting abusively.

Scope covers all consumer credit secured on an asset or livelihood, not just app cash
loans: PAYG devices (M-KOPA-type phones/TVs/solar), motorbike/car asset financing
(Watu/Mogo-type), and secured/group microfinance (KWFT-type). See
`scope-asset-financing.md` for categories, named examples, and sources.

## The unifying question

*"What will this really cost me, what can they take, and is what they told me legal?"*
Every category answers the same three: **true cost** (vs the daily/weekly framing that
hides it), **what's at risk** (device lock, repossession, jointly-registered
collateral, group-member liability), and **is it legal** (licensed? disclosed per
Article 46? any regulator/court finding against them?).

## The problem (evidence in idea-scorecard.md)

Over 8 million Kenyans are CRB-blacklisted, most over mobile loans, many under US$2.
~50 loan apps operate; the majority are unlicensed. Borrowers cannot see the true
cost at the moment of borrowing — "borrow 1,000, repay 1,150 in 30 days" reads as
"15%" but is ~292% APR. The University of Nairobi names the exact gap: borrowers
cannot understand the true cost of borrowing. A 2026 court ruled unlicensed apps
cannot enforce repayment — so "is this lender licensed?" now has legal weight the
borrower never knew to check.

## The core honest claim (state this in README + pitch)

Deni does **not** lend, block, or erase debt. It **cannot** and should not. It is a
**transparency and evidence tool**: it turns a lender's own numbers into the true
cost, checks a public fact (is this lender on CBK's licensed list), and prepares the
paperwork the borrower or regulator already has authority to act on. Every number is
math the user can see; every claim links to a source. It never calls a named lender a
"scam" — it states "not on CBK's licensed list as of <date>."

## What it does — organized by loan lifecycle (before / during / after)

Deni is a **loan-lifecycle rights companion**. Full detail and legal grounds in
`lifecycle-and-recourse.md`; summary here.

### BEFORE — decide with eyes open (the core demo beat)
- **True-cost decode:** turn "deposit + KSh X/day for a year" or "borrow 1,000 repay
  1,150 in 30 days" into total cost + true APR vs cash price, math shown. The gap
  between what it looks like and what it is.
- **What's at risk:** device remote-lock, repossession, jointly-registered
  collateral, group-member liability — stated plainly before signing.
- **Licence + disclosure check:** match the lender to CBK's licensed-DCP list; flag
  undisclosed terms (Article 46). "Not on CBK's list as of <date>" → may not be able
  to lawfully enforce.
- **Cheaper licensed alternative** (the additive, hopeful arc).
- Output: informed go/no-go + a saved record of the terms shown (evidence for later).

### DURING — you have the loan and things are going wrong (the phase we were missing)
The user describes what's happening; Deni returns what Kenyan law says + the forum +
a prepared complaint. Covered scenarios:
- **Harassment / contacts scraped / shaming / threats** → Data Protection Act 2019;
  route to **ODPC** (which has audited lenders and admitted hundreds of complaints).
- **Repossession of a financed asset** → what to verify (proper default notice?
  lawful process? licensed auctioneers?); wrongful repossession has been ruled
  "illegal, null and void" by the High Court; prepare a demand/complaint.
- **Misleading terms / undisclosed cost** → Competition Act; route to **CAK** (which
  found Mogo in violation).
- **Unlicensed lender chasing you** → confirm status; may not lawfully enforce (2026
  ruling); report to **CBK**.

### AFTER — the damage is done
- **Wrongful CRB listing** → dispute with the bureau (CRB Regs 2020, LN 55/2020);
  Deni drafts the letter.
- **Asset already taken** → assemble timeline + notices + payment record for a
  lawyer; illegal-repossession case law supports return/damages.
- **Data already abused** → ODPC complaint.

### The forum router (Deni's core "clear next steps" engine)
Maps each problem to the right institution with the legal basis — ODPC, CBK, CAK,
courts, CRBs. See the table in `lifecycle-and-recourse.md`. Every route ends in a
prepared complaint/letter + evidence checklist + a case reference the user keeps.

**Not legal advice.** Deni states "this may be unlawful — verify X, contact Y,"
cites the law with its date, and states the condition. It never promises an outcome.

## Cross-track justification

- **Transparency & Accountability** — makes a hidden, decision-critical cost and a
  public licensing fact visible and verifiable at the moment of choice.
- **Stability & Social Cohesion** — mass CRB blacklisting and debt distress are a
  documented driver of household crisis; the tool reduces the friction *before* it
  becomes a spiral. "Prevent before it escalates," applied to debt.
- **Safety, Reporting & Protection** — protected, redacted routing of harassment /
  data-abuse complaints to the regulator.

## The 7 operating constraints (brief) — how Deni meets each

1. **Trust & verification** — APR is shown math; licence status cites CBK's list with
   the check date; every claim traceable. "Last updated" shown on the licence data.
2. **Low bandwidth & basic devices** — USSD and WhatsApp first; text-only; no app
   install; the primary audience is on feature phones and low data.
3. **Accessibility & inclusion** — plain language, audio read-aloud, English +
   Kiswahili, numbers explained not just displayed.
4. **Privacy & security** — no login; no server-side storage of a user's loan data;
   compute locally / ephemerally; complaint packets redact by default.
5. **Multilingual** — English + Kiswahili at minimum; language is a config layer so
   Sheng/other packs can be added.
6. **Local relevance** — Kenya-specific fee patterns, CBK licence registry, the 2026
   ruling; built as a per-country pack so NG/GH/TZ/ZA swap the fee math + registry.
7. **Clear next steps** — never ends at "this is bad": shows a cheaper licensed
   option, whether they can legally be pursued, and if warranted a ready complaint +
   receipt. Always a concrete next action.

## What it honestly cannot do (README + demo must say)

1. Cannot lend, block a lender, freeze a loan, or erase a CRB listing.
2. Cannot guarantee a lender is safe — only report a verifiable licence status and
   the math.
3. Cannot confirm a complaint was accepted — it prepares and the user files; status
   is user-marked.
4. Loan terms change; Deni shows the math for the numbers given and names its data
   date. It is not legal or financial advice.

## Scope for the sprint (freeze this)

**In:**
- True-cost decode for the common Kenyan structures (flat fee + term; rollover).
- Licence check against a bundled CBK licensed-DCP dataset (dated).
- 3–5 named lender products modelled for the demo, with sources.
- One channel done well for the demo (WhatsApp-style chat UI + a simulated USSD
  flow), English + Kiswahili.
- One regulator complaint template (CBK) + a case reference.

**Out (say so, put on the "what's next" slide):**
- Every lender/product; live scraping of app stores; real regulator API integration;
  accounts/logins; real CRB dispute filing; other countries (show the config pattern,
  don't build them).

## Naming / positioning

- Product: **Deni**. Tagline candidates: "Know the real cost before you borrow." /
  "Deni: the true price of the loan, in 10 seconds."
- Never pitch as "a loan calculator." Lead with the shock APR and the
  "can they even legally chase you?" licence hook.

## Open decisions before build

1. Primary demo channel: WhatsApp-style web chat (fast to build, demos great) with a
   simulated USSD screen alongside for the basic-phone story. Confirm.
2. AI usage depth: rule-based APR math (deterministic, honest) + an AI layer for
   parsing pasted SMS/screenshots and generating the Kiswahili plain-language
   explanation + the complaint draft. Confirm scope.
3. Data: hand-build the dated CBK licensed-DCP list + 3–5 modelled products now
   (source each). Confirm the product list.
