# Deni

> Know the real cost before you borrow.

Deni tells a Kenyan borrower what a loan will really cost, what the lender can take if
they miss a payment, and whether what they were told is legal — before they sign —
over USSD/WhatsApp. Covers app cash loans, PAYG devices (M-KOPA-type), motorbike/car
financing (Watu/Mogo-type), and secured microfinance (KWFT-type). When the lender is
unlicensed, misled them, or is collecting abusively, it prepares a filed complaint to
the right regulator with a receipt.

Built for the OSF × Andela "Information you can trust" hackathon (cross-track:
Transparency + Stability + Safety). Deadline 21 Sep 2026.

## Status: concept frozen, pre-build

## Docs

| File | What |
|------|------|
| `idea-scorecard.md` | Evidence-backed validation vs alternatives. Verdict: BUILD. |
| `concept.md` | Full concept: mechanisms, cross-track fit, 7-constraint fit, honest limits, scope. |
| `scope-asset-financing.md` | The four harm categories (PAYG devices, moto/car, microfinance, solar), named examples, sources. |
| `lifecycle-and-recourse.md` | Before/during/after coverage + Kenyan legal recourse per scenario, forum router, sources. |
| `pre-build-audit.md` | Final pass against the brief: gaps, resolutions, what's solid. |
| `architecture.md` | Stack, data model, AI task split, verified AWS/Nova facts. |
| `build-plan.md` | 7-day demo-first plan. |
| `specs/requirements.md` | Spec 1: EARS requirements (R1–R14). |
| `specs/design.md` | Spec 2: architecture, components, data models, req→component trace. |
| `specs/tasks.md` | Spec 3: ordered demo-first task list (T1–T13). |
| `specs/ui.md` | UI/UX: split-surface use of the Timescale design system + a11y overrides. |

Research that led here lives one level up: `../lending-direction.md` (friction +
regulatory evidence), `../winner-patterns.md` (what wins African/Asia/LatAm civic
hackathons), `../github-rescan.md` + `../devpost-scan.md` (prior art),
`../selection-constraints.md`, `../prevention-check.md`.

## The pitch in 10 seconds (two blades: cost + rights)

Cost: "This M-KOPA phone is KSh 60/day for a year — that's KSh 21,900 for a handset
that costs KSh 12,000 cash. An 82% markup the daily price hides."

Rights: "Miss one daily payment and it locks. Default on the KWFT loan and the car
registered in your name can be taken. This app isn't on CBK's licensed list — which
means it may not even be legal for them to chase you."

## Open decisions (blockers for the build plan)

1. **Primary demo channel** — WhatsApp-style web chat (fast, demos well) + a
   simulated USSD screen for the basic-phone story? 
2. **AI scope** — deterministic APR math + AI for (a) parsing pasted SMS/screenshots,
   (b) Kiswahili plain-language explanation, (c) drafting the regulator complaint?
3. **Data** — confirm the 3–5 named lender products to model for the demo, and that
   we hand-build a dated CBK licensed-DCP list with sources.

Answer these three and the next docs are: `build-plan.md` (7-day, demo-first) and
`architecture.md` (stack + data model), then code.

## Non-negotiables (from the research)

- Never pitch as "a calculator." Lead with the shock APR + the licence/legal hook.
- Never call a named lender a "scam." State "not on CBK's licensed list as of <date>."
- Basic-phone reachable (USSD/WhatsApp), English + Kiswahili, no login, local-only
  data. These are scored constraints, not nice-to-haves.
- Every number is shown math; every claim links to a source.
