# Deni — scope expansion: asset financing & microfinance

> Added: 14 September 2026 (builder steering)
> Deni is NOT just app cash loans. The biggest, best-documented harms are in
> asset-backed credit: phones/TVs (M-KOPA), motorbikes/cars (Watu, Mogo), and
> secured microfinance (KWFT-type). These add repossession and asset seizure on top
> of hidden cost — a stronger, more visceral problem than cash-loan APR alone.

## The four harm categories Deni should cover

### 1. PAYG device financing — M-KOPA and similar (phones, TVs, fridges, solar)
- Model: small deposit + **daily repayments** over ~a year; the asset is financed
  and **secured against itself**.
- The hidden mechanic: the device is **locked remotely if a single daily payment is
  missed** — GSMA's own writeup states the lock exists specifically to avoid
  "costly repossession." Kenyan press: "miss a single daily payment, the handset is
  remotely disabled, rendering it useless until arrears are cleared."
- The hidden cost: daily-payment framing hides the total markup vs cash price. This
  is under live regulatory scrutiny over hidden costs.
- **Deni's job:** convert "deposit + KSh X/day for 365 days" into **total paid vs
  cash price** and an effective interest figure. Show the markup the daily framing
  hides.

### 2. Motorbike / car asset financing — Watu, Mogo (boda-boda BNPL)
- Model: finance a motorbike/tuk-tuk/car, weekly/daily payments, **tracker fitted,
  repossession on arrears**.
- Documented harm:
  - Boda-boda riders **petitioned Parliament** alleging excessive rates and
    **failure to disclose loan terms, repayment obligations, and costs** — framed as
    violating **Article 46** (consumer rights) of the Constitution.
  - MPs **invited operators who lost motorcycles** to submit complaints over rogue
    lenders; legislation called for.
  - The **Competition Authority of Kenya found Mogo** in violation of the
    Competition Act for **"false and misleading representations and unconscionable
    conduct"** in its loan products (Oct 2024).
  - Repossession over small arrears documented (e.g. a KSh 13,000 case; tracker
    used to disable/locate).
- **Deni's job:** total cost vs cash price; disclosure gaps; whether the financier's
  conduct/terms match what regulators (CAK, CBK where applicable) require; the
  repossession terms in plain language *before* signing.

### 3. Secured microfinance — KWFT and similar (group + collateral lending)
- Model: microfinance/DTM loans secured by **household assets or a vehicle
  registered in the lender's joint name**, and **group guarantee** (co-members
  liable).
- Documented: **Kenya Women Finance Bank Ltd v Mburu [2026] KEHC 5105** — a car
  (KCN 925C) provided as collateral, registered jointly with the lender, enforced
  via court process. Real, current, citable.
- The harm: borrowers often don't grasp that default can mean a **jointly-registered
  asset seized**, or that a **fellow group member's default** exposes their own
  assets. Asset seizure and social/collateral pressure, not just interest.
- **Deni's job:** make the collateral and group-liability terms explicit before
  signing — "if you or a group member defaults, this asset can be taken" — and cite
  the mechanism.

### 4. PAYG solar (same pattern, rural)
- Streamline investigation: PAYG solar marketed as affordable clean energy became a
  **high-interest consumer debt trap** across Kenya/Uganda/Tanzania; defaults now
  stress rural microfinance. Same lock-and-markup mechanic as devices. Include as a
  covered category; do not build a separate flow for the sprint.

## What this changes about Deni

- **Deni is a "true cost + your rights" tool for ALL consumer credit secured on an
  asset or livelihood**, not a cash-loan APR calculator. The unifying question:
  *"What will this really cost me, what can they take, and is what they told me
  legal?"*
- Adds a repossession/seizure dimension the cash-loan version lacked. This is more
  visceral and more visual for the demo: not just a scary APR, but "miss a payment →
  your bike, your phone, your collateral is gone, and here's whether they disclosed
  that."
- Broadens the regulator map: **CBK** (DCPs), **Competition Authority of Kenya**
  (misleading representation / unconscionable conduct — the Mogo route),
  **ODPC** (tracker/data misuse), courts.
- **Sharpens the demo.** Best beat now has two blades:
  1. Cost: "KSh X/day for a year = KSh Y total for a phone that costs KSh Z cash —
     a __% markup."
  2. Rights: "Miss one daily payment and the phone locks. Default on the KWFT loan
     and the car in your name can be taken. Did they disclose that? Here's the law."

## Discipline (unchanged, extended)

- **Named companies, sourced facts only.** State what a regulator/court found (CAK
  found Mogo in violation; the KEHC ruling exists), or state the disclosed terms and
  the math. Never invent conduct. Never call a company a "scam" or allege "violence"
  without a cited finding — describe documented practices (remote lock, repossession,
  court enforcement) with sources.
- Model 1–2 named products per category for the demo with sources; do not claim
  coverage of all.

## Sources

- Boda-boda riders petition Parliament, non-disclosure, Article 46:
  https://www.tuko.co.ke/business-economy/economy/636812-boda-boda-riders-cry-foul-bike-loans-mps-order-probe-high-interest-rates/
- MPs invite operators who lost motorcycles to complain re rogue lenders:
  https://www.tuko.co.ke/business-economy/544635-kenya-mps-invite-boda-boda-operators-lost-motorcycles-submit-complaints-rogue-lenders/
- CAK found Mogo — false/misleading representation, unconscionable conduct:
  https://www.dawan.africa/news/mogo-faces-fresh-scrutiny-as-parliament-turns-spotlight-on-kenyas-asset-financing-industry
- Mogo repossession / tracker case:
  https://nyakundireport.com/p/12166/mogo-caught-in-kes-13000-motorcycle-repossession-case-after-informing-the-rider-that-their-tracker-was-disabled
- Boda-boda BNPL debt (Watu/Mogo, Rest of World):
  https://restofworld.org/2023/bike-theft-kenya-bnpl/
- Watu Kenya (financier, primary):
  https://watuafrica.com/country/kenya/
- M-KOPA lock-on-missed-payment (GSMA):
  https://www.gsma.com/mobilefordevelopment/wp-content/uploads/2022/04/M-KOPA-Applying-the-pay-as-you-go-model-to-smartphones-in-Africa.pdf
- Device remote-disable on one missed daily payment; hidden-cost scrutiny:
  https://mjengohub.co.ke/articles/finance/state-interventions-loom-as-mobile-phone-credit-schemes-face-regulatory-scrutiny-over-hidden-costs
- KWFT collateral car jointly registered, court enforcement — KEHC 5105 (2026):
  https://new.kenyalaw.org/akn/ke/judgment/kehc/2026/5105/eng@2026-04-22/source.pdf
- PAYG solar debt trap (regional):
  https://streamlinefeed.co.ke/news/rural-off-grid-solar-payg-microfinance-default-crisis-2026
