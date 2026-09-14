# Deni — before / during / after, and legal recourse

> Added: 14 September 2026 (builder steering)
> Deni must cover the whole loan lifecycle, not just pre-borrow. "During" (being
> followed, harassed, facing repossession) is where fear and demand are highest, and
> where Kenyan law gives people rights they don't know they have.
>
> DISCIPLINE: Deni surfaces rights and cites the law/regulator. It is NOT legal
> advice and never promises an outcome. It says "this may be unlawful — here is what
> to check and who to contact," never "you will win." Recourse depends on facts
> (registered charge vs unregulated credit, notice served, licensed vs not).

## The three phases

### BEFORE — decide with eyes open (already built into concept.md)
- True cost vs the daily/weekly framing.
- What's at risk: device lock, repossession, jointly-registered collateral, group
  liability.
- Is the lender licensed (CBK DCP list)? Were terms disclosed (Article 46)?
- Cheaper licensed alternative.
Output: an informed go/no-go + a saved record of the terms they were shown (useful
later as evidence).

### DURING — you have the loan and things are going wrong
Scenarios and what Kenyan law actually gives the borrower:

**A. Debt-collection harassment / contacting your phonebook / threats / shaming**
- The **Data Protection Act 2019** (Art. 31(c)(d) of the Constitution) governs use
  of personal data. Scraping a borrower's contacts and messaging them is a data
  offence. The **ODPC** regulates this and **has teeth**: it audited **40 digital
  lenders** (2022) and admitted **555 of 1,030 complaints** for investigation.
- CBK DCP Regulations 2022 restrict **unethical debt-collection** by licensed DCPs
  (limits on who can be contacted, no threats/abuse).
- Deni's job: name the practice, cite the ODPC/CBK basis, and generate an **ODPC
  data-protection complaint** (+ CBK conduct complaint if a licensed DCP) with the
  evidence bundle (screenshots, timestamps) and a case reference.

**B. Repossession of a financed asset (bike / car / logbook loan)**
- Kenyan courts repeatedly declare repossessions **"illegal, null and void"** when
  done wrongly — multiple 2024 High Court rulings (KEHC 13055/2024, 12379/2024,
  409/2024), including one struck down because the **notice "was not served."**
- The general principle Deni can safely surface (not as a guarantee): a financier
  usually **cannot just grab the asset**; proper process (valid default, notice,
  and lawful seizure — often via licensed auctioneers / court process) is required,
  and self-help seizure without it has been ruled unlawful.
- Deni's job: tell the borrower **what to check** (was a proper default notice
  served? is the seizure following lawful process? are they licensed auctioneers?),
  that wrongful repossession can be challenged in court, and prepare a **demand /
  complaint** and the facts to take to a lawyer, CBK, CAK, or court. Never "your
  repossession is illegal" flat — "repossessions done without proper notice/process
  have been ruled illegal; here is what to verify."

**C. Misleading terms / unconscionable conduct (asset financiers)**
- **Competition Act** consumer-protection provisions; the **Competition Authority of
  Kenya (CAK)** found **Mogo** guilty of false/misleading representation and
  unconscionable conduct (Oct 2024) — a live, citable precedent.
- Deni's job: route a CAK consumer complaint where terms were misrepresented or
  costs not disclosed (Article 46).

**D. Unlicensed lender chasing you**
- 2026 court ruling: **unlicensed digital lenders blocked from enforcing repayment.**
- Deni's job: confirm licence status; explain that an unlicensed lender may not be
  able to lawfully enforce; prepare the CBK report.

### AFTER — the damage is done
- **Wrongful CRB listing:** you can dispute with the bureau (TransUnion, Metropol,
  Creditinfo) under the Banking (Credit Reference Bureau) Regulations 2020; if the
  lender was unlicensed or the debt disputed, the listing basis is challengeable.
  Deni drafts the dispute letter (mechanic already in ../phone-theft-architecture.md).
- **Asset already taken:** the illegal-repossession case law (above) supports a suit
  for return/damages; Deni assembles the timeline + notices + payment record for a
  lawyer.
- **Data already abused:** ODPC complaint for the misuse; may attract penalties.

## The right forum for each problem (Deni's router)

| Problem | Forum | Basis |
|---|---|---|
| Contacts scraped, harassment, shaming | **ODPC** | Data Protection Act 2019 |
| Licensed DCP misconduct / abusive collection | **CBK** | CBK (DCP) Regulations 2022 |
| Unlicensed lender operating / chasing you | **CBK** + courts | CBK Act s.33S; 2026 ruling |
| Misleading terms, undisclosed cost | **CAK** | Competition Act; Article 46 |
| Wrongful repossession | Court (+ demand letter) | case law: KEHC 2024 rulings |
| Wrongful CRB listing | **CRB** (TransUnion/Metropol/Creditinfo) | CRB Regs 2020, LN 55/2020 |

## What this changes about Deni

- Deni becomes a **loan-lifecycle rights companion**: informed decision (before),
  know-your-rights + stop-the-harm routing (during), and recover/dispute (after).
- The "during" phase directly answers the builder's question: someone **being
  followed/harassed** opens Deni, describes what's happening, and gets (1) the plain
  statement of what the law says, (2) the specific forum, (3) a prepared complaint +
  evidence checklist + case reference. Over WhatsApp/USSD, no login.
- This is also the **strongest cross-track proof**: Safety (protection during
  harassment/threats), Transparency (the legal facts made accessible), Stability
  (defusing a debt crisis before it wrecks a household).

## Hard discipline (repeat in README + UI + demo)

- Not legal advice. "This may be unlawful / you may have grounds — verify X, contact
  Y." Never promise a win.
- Sourced only. Cite the Act, regulation, regulator, or a real ruling. Show the date.
- Recourse is conditional: state the condition ("if no proper notice was served…",
  "if the lender is unlicensed…").

## Sources

- ODPC audited 40 digital lenders; 555/1,030 complaints admitted:
  https://www.cliffedekkerhofmeyr.com/export/sites/cdh/news/publications/2022/Practice/TMT/Downloads/Technology-Media-Telecommunications-Alert-11-October-2022.pdf
- Data Protection Act 2019 (Art. 31 basis), ODPC mandate + complaint procedure (LN
  264/2021): https://www.odpc.go.ke/data-protection-laws-kenya/
- CBK (DCP) Regulations 2022, s.33S licensing + conduct:
  https://www.cliffedekkerhofmeyr.com/export/sites/cdh/news/publications/2025/Practice/Banking-Finance-Projects/Downloads/Banking-Finance-Projects-Alert-27-February-2025.pdf
- Repossession "illegal, null and void" — 2024 High Court rulings:
  https://new.kenyalaw.org/akn/ke/judgment/kehc/2024/13055/eng@2024-10-22/source.pdf ·
  https://new.kenyalaw.org/akn/ke/judgment/kehc/2024/12379/eng@2024-10-08/source.pdf ·
  https://new.kenyalaw.org/akn/ke/judgment/kehc/2024/409/eng@2024-01-25/source
- Repossession struck down, notice not served:
  https://new.kenyalaw.org/akn/ke/judgment/kehc/2006/2727/eng@2006-03-01/source.pdf
- CAK found Mogo (misleading/unconscionable conduct):
  https://www.dawan.africa/news/mogo-faces-fresh-scrutiny-as-parliament-turns-spotlight-on-kenyas-asset-financing-industry
- Unlicensed lenders blocked from enforcing repayment (2026):
  https://weetracker.com/2026/07/27/kenyan-court-delivers-blow-to-unlicensed-loan-apps-seeking-debt-repayment/
- CRB dispute basis (LN 55/2020): https://new.kenyalaw.org/akn/ke/act/ln/2020/55/eng@2020-04-17/source
