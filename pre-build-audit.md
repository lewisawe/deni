# Deni — pre-build audit (final pass against the brief)

> 14 September 2026. Adversarial read of brief.md vs the frozen concept. Ranked by
> point cost. Fix the high ones before/while building; bake the rest into build +
> deck + written summary.

## RESOLUTIONS (builder, 14 Sep 2026 — post-audit)

- **#1 Eligibility — RESOLVED.** Builder confirmed eligible.
- **#2 Government-engagement drift — RESOLVED (framing locked).** Deni foregrounds
  teaching citizens to use public institutions (CBK register, ODPC, CAK, courts, CRB
  dispute). Through-line: "here is the government body whose job this is, and how to
  make it act." Lead the deck/summary with this.
- **#3 Multilingual — RESOLVED (upgraded).** EN + Kiswahili + **Sheng**. Config-driven
  strings; three languages proves the FR/PT/AR "add a file, not a rewrite" scalability
  claim live. Sheng is audience-authentic (young urban borrowers).
- **#5 USSD honesty — RESOLVED (upgraded to real).** Builder has an **Africa's
  Talking demo/sandbox account**. USSD is genuinely functional against the AT gateway
  simulator (free sandbox channel `*384*NNNN#`, callback + CON/END protocol). Honesty
  line changes from "simulated flow" to "live on Africa's Talking sandbox; production
  needs a paid shortcode." No overclaim, stronger demo.

Still open to build in, not just claim:
- **#4 Accessibility** — build number/icon-first cards, audio output (Nova 2 Sonic or
  TTS), high-contrast, screen-reader semantics. Still a real build task.
- **#6 AI-provenance** — state in written summary (idea from builder's lived pains).
- **#7 Submission artifacts** — checklist for Day 5–6.

## HIGH — could sink the entry

### 1. Eligibility not verified (blocker, non-technical)
Brief requires: **Andela Talent Network OR Andela Learning Community member**, based
in Africa, **individual** submission. We validated the idea, never confirmed the
builder can enter. ACTION: confirm ATN/ALC membership + Africa residency before
investing build days. If not a member, resolve first.

### 2. "Engage with governments and public services" drift
Scope line: help people *improve how they engage with governments and public
services*. Deni's BEFORE flow is citizen-vs-private-company (fintech feel). Saved by
DURING/AFTER routing to **government bodies** (ODPC, CBK, CAK, courts). FIX: foreground
the government-engagement angle — Deni teaches a citizen to use a public regulator's
process they didn't know existed. Frame as "civic recourse," not "consumer app." Deck
+ summary must lead this, not bury it.

## MEDIUM — costs points on judged axes

### 3. Multilingual scope vs the continental brief
Brief names **Arabic, French, Portuguese** + local languages; Scalability is judged.
We scoped EN + Kiswahili (correct for a Kenya PoC). FIX: keep the language layer
config-driven (architecture already says this) and *show* in the deck that adding
FR/PT/AR is a config add, not a rewrite. Ship EN+SW working; demonstrate one extra
language string set (even partial) to prove the mechanism. Avoid looking Kenya-locked.

### 4. Accessibility for disabilities + low literacy is thin
Constraint 3 names disabilities, literacy, digital confidence — and Deni's audience
(feature-phone, low-income) skews exactly there. We have audio read-aloud + plain
language noted; not enough. FIX: number-first / icon-first result cards (the shock
figure readable without prose), voice/audio output as a first-class path (Nova can
generate the SW/EN explanation text; TTS or nova-2-sonic for audio), large-text and
high-contrast, keyboard/screen-reader semantics on the web surface. Put concrete
a11y items in the build scope, not as a "nice to have."

### 5. USSD honesty (avoid overclaim)
Real USSD needs a telco shortcode we can't get in a week. Plan already says
"simulated." FIX: label it clearly as a **simulation of the USSD flow** in the demo,
README, and deck. Never imply a live dialable shortcode. Same discipline as the
"Deni blocks nothing" honesty. The *point* it proves (works on a basic phone, no app,
no data) is legitimate; the mechanism is simulated — say so.

## LOW — bake into the written summary

### 6. "AI did not generate the idea" provenance
Brief bans AI-generated capstone ideas. The idea came from the builder's stated lived
pains (bribery, phone theft, predatory loans). FIX: written summary states the
provenance plainly; the ideation trail (killed generic ideas, landed on real anger)
supports it. AI supported the *build* (Nova for parse/explain/draft), which is
allowed and should be described precisely.

### 7. Submission artifacts checklist (start Day 5–6)
Four items, all due 21 Sep, updatable: public repo + clear run README; demo video
(mp4/mov/webm/avi ≤250MB); pitch deck (**PDF only** ≤100MB — cover problem, users,
solution, impact); written summary (track, information sources, trust/accuracy
approach, how AI tools were used). Track pick: **Cross-track**, led by Transparency,
anchored by Safety (see below).

## Confirmed SOLID (no change needed)

- Core insight (true cost + rights, before/during/after) — unique, evidenced.
- Prior-art position — cleanest of all candidates (github-rescan, devpost-scan).
- Deterministic-math-not-AI — strong trust/correctness decision.
- Sourced legal recourse with hedging discipline — defensible.
- Cross-track logic (one mechanic, three consequences) — breadth from focus.
- AWS Bedrock Nova access — verified live (simi-ops, us-east-1).
- 7-constraint fit — now genuinely covers all 7 once #3/#4 are built, not just
  claimed.

## Net

No fatal flaw in the idea. Two real risks are non-idea: **eligibility (#1)** and
**framing drift (#2)**. The medium items (#3 multilingual mechanism, #4 accessibility,
#5 USSD honesty) are the difference between "good" and "wins on a continental brief"
and must be built in, not bolted on. Nothing here changes the decision to build Deni.
