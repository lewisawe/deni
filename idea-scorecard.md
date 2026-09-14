# Idea Scorecard — Deni (OSF × Andela Hackathon)

> Validated: 14 September 2026 · Brief: ../brief.md · Deadline: 21 Sep 2026, 23:59 UTC
> Solo build · Judged on Uniqueness / Scalability / AI Coding Usage / Presentation (equal weight)

## The idea in one line

**Deni** tells a Kenyan borrower the *true* cost of a mobile loan and whether the
lender is even legally allowed to chase them — over USSD/WhatsApp, before they tap
accept — and if the lender is unlicensed or harassing, hands them a ready-to-file
complaint to CBK/ODPC with a receipt.

## Candidates compared (survivors of the ideation gauntlet)

| Idea | One-liner | Prior art (repos) | Clone verdict | Closest competitor | Friction evidence | Tech fit | Demo | Build risk | Impact | Tech | Creativity | Verdict |
|------|-----------|-------------------|---------------|--------------------|-------------------|----------|------|------------|--------|------|------------|---------|
| **Deni (loan true-cost + license check)** | true APR + is-lender-licensed, pre-borrow, USSD | **0** across 17 phrasings | **uncontested** | Western APR calculators only (no KE/mobile-money) | 8M+ CRB-listed; UoN names the exact gap | core | **strong** | low-med | 5 | 4 | 5 | **BUILD** |
| Money → grievance → conflict (procurement) | citizen files grievance on vanished county funds | 0 on GitHub | contested | GovTrust (DevPost, procurement platform) | protests over funds real | core | strong | medium | 4 | 4 | 4 | Fallback |
| Eviction notice validity + tribunal | test notice against statute, route to BPRT | 0 KE | contested (global genre) | TenantShield (won a hackathon) | 3 tribunal rulings in 12mo | core | strong | medium | 4 | 4 | 4 | Fallback |
| Community tension early-warning | anon signal → mediator | dozens adjacent | **saturated** | CEWARN/Uwiano, SOS-by-SMS, PeaceLens | real | incidental-ish | weak | high | 3 | 2 | KILL |
| Phone-theft debt containment | freeze/route after snatch | 0 | uncontested | BOMAVEDA (2nd place), LostPhoneKE | real | core | strong | low-med | 3 | 4 | 4 | KILL (individual harm) |

**Cap logic:** Deni has no fatal weakness. The conflict idea is capped by saturation +
weak demo. Phone-theft is capped by being individual harm (fails the collective test
the winners all pass). Eviction/procurement are strong fallbacks capped one notch by
an adjacent competitor each.

## Deni scored on the hackathon's own four axes

- **Uniqueness — 5/5.** Zero GitHub prior art across 17 phrasings; the only nearby
  repos are UK/US calculators. No Kenyan/African mobile-lending true-cost tool
  exists. The *assembly* (true-APR + CBK-license check + USSD + regulator routing) is
  unoccupied on GitHub, DevPost, and the Kenyan hackathon exemplar pool.
- **Scalability — 5/5.** Predatory mobile lending + credit-bureau blacklisting is
  continent-wide (NG, GH, TZ, ZA, UG). Core mechanic (parse offer → true APR →
  license lookup) is country-agnostic; only the fee math and the license registry
  swap per country. Clean per-country config pattern.
- **AI Coding Usage — 4/5.** Real, demoable AI: parse messy loan T&Cs / SMS offers /
  screenshots into a normalized true APR + total cost; classify licensed vs
  unlicensed; generate plain-language Kiswahili/English explanations; draft the
  regulator complaint. Distinct from GovTrust's procurement scoring. (4 not 5 only
  because the core APR math is deterministic, not ML — which is correct and honest.)
- **Presentation — 5/5 potential.** The demo beat is the strongest we found:
  "borrow 1,000, repay 1,150 in 30 days" → **~292% APR** on screen in 10 seconds.
  Visual, visceral, universal. Risk: must not be pitched as "a calculator."

## The 7-point validation checklist (per idea-validation.md)

1. **Prior-art count:** 0 repos across 17 concept phrasings (see ../github-rescan.md
   + ../lending-direction.md). Generic terms surface only Western calculators.
2. **5+ clones test:** PASS (uncontested). No substantially identical project on
   GitHub, DevPost, or in the HakiHack Kenya exemplar list.
3. **Closest competitor:** none direct. Adjacent: generic Western APR calculators
   (no mobile-money, no license check, no KE); GovTrust (procurement, supply-side).
   Neither competes for this lane.
4. **Real friction:** 8M+ Kenyans CRB-listed over mobile loans; loans often < US$2;
   harassment documented as "traumatising"; UoN policy brief names "true cost of
   borrowing" as the gap. Strong, cited (../lending-direction.md).
5. **Sponsor/brief fit:** CORE, cross-track. Transparency (hidden cost visible),
   Stability (mass blacklisting + debt distress as household-crisis driver), Safety
   (harassment reporting + protected routing). Hits all 7 operating constraints
   (see concept.md).
6. **Demo feasibility:** STRONG. MVP shippable in < half the remaining time; one
   crisp beat (offer in → true APR + license verdict out in seconds).
7. **Build risk:** LOW-MEDIUM. No backend auth needed; deterministic APR math;
   license list is a static/scrapeable dataset; USSD/WhatsApp simulatable for demo.
   Main risks are data accuracy and defamation discipline — both mitigable (scope to
   named products, cite sources, "not on CBK list as of <date>" not "scam").

## Evidence log

- 0/17 prior-art: gh searches 14 Sep 2026, account lewisawe — ../github-rescan.md,
  ../lending-direction.md
- 8M+ CRB listed: https://rightforeducation.org/2025/10/30/burden-of-digital-lending-in-kenya/
- Loans under ~$2, 2.7M (CBK): http://www.xinhuanet.com/english/2019-07/12/c_138218844.htm
- "true cost of borrowing" gap (UoN): https://ids.uonbi.ac.ke/sites/ids.uonbi.ac.ke/files/publications/other-policy-briefs/committee-of-fiscal-studies,-university-of-nairobi-policy-brief,-adam-&-upadhyaya_2022_series,-8.pdf
- CBK DCP licensing; majority unlicensed: https://www.connectingafrica.com/fintech/majority-of-kenya-s-mobile-lenders-are-unlicensed
- 2026 court blocks unlicensed apps from enforcing repayment: https://weetracker.com/2026/07/27/kenyan-court-delivers-blow-to-unlicensed-loan-apps-seeking-debt-repayment/
- Harassment "traumatising": https://www.theguardian.com/global-development/2022/oct/12/traumatising-how-rogue-digital-loan-apps-in-kenya-intimidate-borrowers

## Recommendation

**BUILD Deni.** It is the only survivor with no fatal cap and the cleanest prior art,
the best-evidenced friction, an intrinsic basic-phone channel, genuine cross-track
fit, a non-state adversary (low duty-of-care), and the strongest 10-second demo. The
one risk to watch is framing: lead every artifact with the shock APR and the
"can they even legally chase you" hook, never with the word "calculator."
