# Deni — 7-day build plan (demo-first)

> Frozen 14 Sep 2026. Deadline 21 Sep 23:59 UTC. Solo build. Competitor already has a
> working MVP, so: ship a thin end-to-end demo early, then deepen. Build backward from
> the demo script.

## Principle

Working demo > clean code. One continuous 60–90s run must work end-to-end by Day 3,
then everything else is depth and polish. Submit v1 early (Day 5), refine to deadline.

## The demo script we build backward from

1. "I'm about to take this M-KOPA phone / Watu bike / this app loan." Paste the offer.
2. Deni shows the **true total vs cash price + effective rate** — the shock number.
3. Deni flags **licence status** + what's at risk (lock/repossession/collateral).
4. "They're now calling my contacts / threatening to take the bike." → Deni states
   the law (Data Protection Act / repossession must follow process), names the forum
   (ODPC / CAK / court), and **generates the complaint** with a case reference.
5. Close: "Know the real cost, know your rights, in the language you speak, on any
   phone." Show the USSD version doing the same cost check.

## Days

**Day 1 — data + skeleton.** Hand-build `lenders.json`, `products.json` (all named
products, sourced), `rules.json`, `forums.json`, complaint templates. FastAPI skeleton
+ endpoints stubbed. Deterministic cost/APR function with unit tests (this must be
correct). Chat UI shell.

**Day 2 — before flow, end to end, no AI yet.** Typed offer → cost engine → licence
check → result card, in the chat UI. Hard-code one product path so the shock number
renders. This is the spine.

**Day 3 — AI in + during flow. TARGET: full demo runs end to end.** Wire Bedrock
Converse: Nova Lite parses a pasted SMS and explains in Kiswahili; Nova Pro maps a
"what's happening" description to a scenario and drafts a complaint. Recourse router
returns forum + citation + case reference. By end of Day 3 the 5-step script works.

**Day 4 — USSD surface + all products + after flow.** USSD simulator running the cost
check. Fill in all named products (M-KOPA, Watu, Mogo, KWFT, app loans). CRB dispute +
lawyer-packet generation. English/Kiswahili toggle everywhere.

**Day 5 — polish + submit v1.** Tighten the UI (calm, serious, monochrome — the
GovTrust lesson), add sources/citations + dates on every claim, "not legal advice"
banners, offline fallback for the AI step. **Upload submission v1** (repo + rough
demo + draft deck + written summary). Being in early beats perfect.

**Day 6 — demo video + deck + written summary.** Record the 60–90s run (+ a backup
take). Pitch deck: problem (8M CRB-listed), the shock number, before/during/after,
cross-track, AI usage (Nova), scalability (per-country pack). Written summary: track,
sources, trust/accuracy approach, how AI was used.

**Day 7 — buffer + refine.** Fix demo bugs, re-record if needed, refine deck, verify
the repo clones and runs in a minute (README + run script). Final submit before 23:59
UTC.

## Scope guard (do not exceed)

- IN: named products, before/during/after, cost engine, licence check, recourse
  router + 4 complaint templates, chat + USSD, EN/SW, AI parse+explain+draft.
- OUT: live scraping, real regulator/CRB integration, accounts, other countries
  (show the config pattern on the "what's next" slide), every lender.

## Risks + mitigations

- **AI live-call fails on stage** → recorded fallback of the AI step; cost engine and
  router work offline regardless.
- **APR math wrong** → unit tests Day 1; the number is the whole pitch, it must be
  right and shown.
- **Defamation / legal over-claim** → template layer enforces "may be unlawful,
  verify X" + citations; never "scam", never a promised outcome.
- **Bedrock access/region** → request Nova model access in us-east-1 on Day 1 (access
  is per-region and can take time).

## Immediate next actions

1. Verify Bedrock Nova access is enabled in us-east-1 (request if not).
2. Scaffold the repo (FastAPI + static frontend + data files + run script).
3. Build the cost engine + tests and the data files first.
