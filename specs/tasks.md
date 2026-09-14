# Deni — Tasks

> Spec 3 of 3. Frozen 14 Sep 2026. Executable plan realizing design.md.
> Demo-first: a full end-to-end run must work by end of Task 6, then depth + polish.
> Each task states its requirement refs and a demo checkpoint (what works when done).

## Phase 1 — Spine (money is provably correct before anything else)

### T1. Repo scaffold + run script
- FastAPI backend, static SPA frontend, `data/` packs dir, `run.sh`, README stub.
- Bedrock client wrapper (boto3, region us-east-1, profile-aware) — not called yet.
- **Demo:** `bash run.sh` serves the app locally; health endpoint responds.
- Refs: design "Architecture".

### T2. Cost engine + unit tests  [R1]
- Pure functions: total_payable, total_cost_over_principal, effective_rate/APR,
  markup_vs_cash, with a structured arithmetic breakdown.
- Unit tests incl. the canonical case ("borrow 1,000 repay 1,150 / 30 days" → APR),
  and a PAYG daily case ("deposit + X/day × 365 vs cash price" → markup).
- **Demo:** tests pass; calling the engine returns the shock number + its working.
- Refs: R1. This is the trust core — do it first, correctly.

### T3. Data packs (Kenya), sourced  [R3,R4,R7,R12]
- `lenders.json` (CBK licensed-DCP list dated + M-KOPA, Watu, Mogo, KWFT, 1–2 app
  lenders; findings incl. CAK-vs-Mogo, the 2026 unlicensed ruling).
- `products.json` (one modelled product per named lender, every field sourced).
- `rules.json`, `forums.json` (from ../lifecycle-and-recourse.md, with citations+dates).
- `templates/` (ODPC, CBK, CAK, CRB) with fixed legal basis + fact slots.
- **Demo:** licence check + risk descriptor + recourse rule resolve from data for each
  named product, with sources.

## Phase 2 — Before flow, end to end (no AI yet)

### T4. Before flow in chat UI  [R1,R3,R4,R5,R7,R13]
- Structured offer entry → cost engine → licence check → risk → cheaper alternative →
  result card (number/icon-first) with sources/dates + "not legal advice".
- **Demo:** type an M-KOPA offer, see true cost + markup + licence + what's at risk +
  a cheaper licensed option. The core shock beat works without AI.
- Refs: R1,R3,R4,R5,R7,R13.

### T5. i18n layer (EN/SW/Sheng)  [R11]
- Strings extracted to `strings/{en,sw,sheng}.json`; language selector; all T4 UI
  keyed.
- **Demo:** flip the before flow across three languages.

## Phase 3 — AI + during flow  (TARGET: full demo runs end to end)

### T6. Bedrock wired: parse + explain  [R2,R14]
- Nova 2 Lite: parse pasted SMS / screenshot → offer schema → user-confirm step;
  generate the plain-language explanation in the selected language.
- **Demo:** paste a real SMS offer, confirm parsed fields, get the explained shock
  number in Sheng. ← end-to-end "before" with AI.

### T7. Recourse router + doc generator  [R6,R10,R13]
- Nova Pro classifies a free-text "what's happening" into a scenario; rule/forum/
  citation read from data; Nova Pro fills the fixed complaint template; emit case ref
  + evidence checklist; redact by default.
- **Demo:** "they're calling my contacts / threatening to take the bike" → law +
  forum (ODPC/CAK/court) + generated complaint + case reference. ← "during" works.
  **After Task 7 the full 5-step demo script runs.**

## Phase 4 — Second channel, breadth, after flow

### T8. USSD via Africa's Talking sandbox  [R8]
- Create sandbox USSD channel; implement callback (CON/END stateless replay); menu:
  true-cost decode + licence check. Label as sandbox.
- **Demo:** run the cost check + licence check through the AT USSD simulator.

### T9. All named products + AFTER flow  [R6, scope]
- Complete products for M-KOPA, Watu, Mogo, KWFT, app loans. Add CRB dispute letter +
  lawyer-packet generation (after).
- **Demo:** any named product runs; wrongful-CRB-listing produces a dispute letter.

### T10. Accessibility pass  [R9]
- Audio output of the explanation (Nova 2 Sonic or TTS); high-contrast; ARIA/screen-
  reader semantics; icon-first cards verified at small size.
- **Demo:** result read aloud; usable with a screen reader; legible tiny.

## Phase 5 — Submit + polish

### T11. Submit v1 (Day 5)  [R14, brief]
- Repo public + README (what it does, how to run in <1 min, honesty notes incl. USSD
  sandbox + "not legal advice"). Rough demo, draft deck, draft written summary.
- Upload submission v1; refine to deadline.

### T12. Demo video + deck + written summary (Day 6)
- 60–90s video (+ backup take). Deck (PDF): problem (8M CRB-listed), the shock number,
  before/during/after, gov-engagement framing, cross-track, Nova usage, per-country
  scalability. Written summary: track, sources, trust/accuracy approach, AI usage,
  idea provenance (builder's lived experience).

### T13. Buffer + final submit (Day 7)
- Fix demo bugs; re-record if needed; verify clone-and-run; final submit < 23:59 UTC.

## Guardrails carried through every task
- AI never computes money or states law/citations (R1,R6,R14).
- Every claim shows source + date (R7).
- No login; no server-side user data; redact packets (R10).
- Label sandbox/simulated elements honestly; never promise a legal outcome (R14,R6).

## Critical path to a working demo
T1 → T2 → T3 → T4 → T6 → T7 = full 5-step run. T5, T8, T9, T10 deepen and broaden;
T11–T13 package. Protect the T1→T7 path; everything else is negotiable under time
pressure.
