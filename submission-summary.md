# Deni: Written Summary

> OSF × Andela "Information you can trust". Submission summary (4 parts).

## 1. Track

Cross-track. **Transparency & Accountability** is the primary track: Deni makes a loan's
true cost and a lender's licence status visible and understandable, and routes a
borrower to the public body that can hold the lender to account. It also delivers
**Safety, Reporting & Protection** (anonymous, on-device redaction; a complaint with a
case reference; a direct cease-and-desist letter to stop harassment) and **Stability &
Social Cohesion** (a helper workspace so a paralegal, chief, or CSO worker can support
several borrowers at once).

## 2. Information sources

Every civic fact in Deni is read from a per-country data file, each entry carrying a
source URL and a date. Kenya sources include: the Data Protection Act 2019 and the ODPC
(data misuse and abusive collection); the CBK Act and the Digital Credit Providers
Regulations 2022 (digital-lender licensing); the Competition Act and a Competition
Authority of Kenya finding (misleading terms); Kenyan High Court judgments on Kenya Law
(repossession, secured-microfinance enforcement); the Banking (Credit Reference Bureau)
Regulations 2020 (bureau disputes); and the Small Claims Court Act 2016 (money recovery).
The South Africa pack uses the National Credit Act 34 of 2005 and the NCR, POPIA and the
Information Regulator, and the Small Claims Courts Act. Lender records separate an
**official finding** (a named regulator or court, with its decision citation) from a
**reported concern** (press or research, labelled as such). A source-integrity checker
(`backend/check_sources.py`) verifies every citation URL is live before submission.

## 3. Approach to trust and accuracy

Two rules make the output trustworthy rather than merely plausible.

First, **the money is deterministic code, never AI.** The true cost, markup, and APR are
computed in `backend/cost_engine.py` and the arithmetic is shown on screen, so the number
is provably correct and reproducible. It has unit tests.

Second, **the law is read from sourced data, never generated.** Legal statements and
citations live in the data packs; the AI model only classifies a described problem into a
known scenario and phrases the fixed result. It never states a legal conclusion or a
figure on its own.

Everything else follows from those rules: every claim shows a source and a date; the
licence register shows its as-of date and links to the official list so a user can verify
today's status; recourse is phrased conditionally ("this may be unlawful if…") and never
promises an outcome; named lenders carry only verifiable facts, never the word "scam"; and
an unmatched problem still returns a general-body safety net rather than a dead end. The
product does not lend, block, freeze, or erase anything, and it says so.

Privacy protects accuracy of a different kind: there is no login, nothing the user enters
is stored on the server, and the problem text is redacted on the user's device (and again
server-side, covering WhatsApp and USSD) before it is classified.

## 4. How AI tools were used to build it

The capstone idea comes from the builder's lived experience of predatory lending in
Kenya. AI supported the build only, and deliberately.

The project was built spec-first: AI coding tools drafted and refined three frozen
documents (requirements → design → tasks), and every later change traces back to a
requirement. AI helped assemble the per-country data packs into a fixed, sourced shape
(each fact human-verified), factor the civic logic so the web, WhatsApp, and USSD channels
call one engine, and write the tests that keep the deterministic core correct across
refactors. The one architectural rule the specs enforce, that AI never states a number or
the law, is the reason the output can be trusted.

At runtime, Deni uses AWS Bedrock (Amazon Nova) for four narrow jobs only: reading a
pasted SMS or an uploaded screenshot into offer fields (which the user confirms before any
computation), explaining a computed result in the user's language, classifying a described
problem into a known scenario, and filling a fixed complaint template. If Bedrock is
unreachable, the deterministic core, the cost engine, licence check, rights library,
keyword-based recourse, redaction, and the USSD flow, all still work.
