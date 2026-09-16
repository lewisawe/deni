"""Builds a shareable 'Deni report': the receipt a borrower keeps (the action+receipt
pattern). Plain-text canonical form; the frontend renders it to image/PDF and offers
WhatsApp/copy. Kept server-side so text is consistent and sources are attached."""
from __future__ import annotations

import datetime as _dt
import uuid


def _today() -> str:
    return _dt.date.today().isoformat()


def cost_receipt(evaluation: dict, lang: str = "en") -> dict:
    """Receipt for a BEFORE cost check."""
    c = evaluation["cost"]
    lic = evaluation.get("licence", {})
    prod = evaluation.get("product", {})
    cur = evaluation.get("currency", {}).get("symbol", "KES")
    ref = "DENI-" + uuid.uuid4().hex[:8].upper()
    lines = [
        "DENI: LOAN COST CHECK",
        f"Ref: {ref}   Date: {_today()}",
        "",
    ]
    if prod.get("label"):
        lines.append(f"Loan: {prod['label']}")
    lines += [
        f"You pay: {cur} {c['total_paid']} for {cur} {c['principal']} of value",
        f"True cost: {cur} {c['total_cost']}  ({c['markup_pct']}% more)",
        f"APR: {c['apr_pct']}%",
    ]
    if lic:
        lines.append(f"Lender licence: {lic.get('status', 'n/a')}. {lic.get('note','')}")
    if evaluation.get("at_risk", {}).get("note"):
        lines.append(f"At risk: {evaluation['at_risk']['note']}")
    if evaluation.get("alternative"):
        a = evaluation["alternative"]
        lines.append(f"Cheaper licensed option: {a['label']} at {a['cost']['apr_pct']}% APR")
    lines += [
        "",
        "Computed by Deni. The math is shown in-app. Not financial or legal advice.",
        f"Data date: {evaluation.get('data_date', _today())}",
    ]
    return {"ref": ref, "kind": "cost", "text": "\n".join(lines),
            "sources": evaluation.get("sources", [])}


def recourse_receipt(recourse: dict) -> dict:
    """Receipt for a DURING/AFTER recourse action (includes the complaint)."""
    ref = recourse.get("case_ref") or ("DENI-" + uuid.uuid4().hex[:8].upper())
    lines = [
        "DENI: YOUR RIGHTS & COMPLAINT",
        f"Case ref: {ref}   Date: {_today()}",
        "",
        f"Situation: {recourse.get('title', '')}",
        f"The law: {recourse.get('law_statement', '')}",
        f"Applies if: {recourse.get('condition', '')}",
        f"Go to: {recourse.get('forum', {}).get('name', '')}",
        f"Basis: {recourse.get('citation', '')} ({recourse.get('citation_date', '')})",
        "",
        "--- PREPARED COMPLAINT ---",
        recourse.get("complaint", ""),
        "",
        "Prepared by Deni. Not legal advice. Verify before filing.",
    ]
    return {"ref": ref, "kind": "recourse", "text": "\n".join(lines),
            "sources": [recourse.get("citation")] if recourse.get("citation") else []}
