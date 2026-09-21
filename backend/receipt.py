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
    """Receipt for a DURING/AFTER recourse action: a self-contained civic record the
    borrower keeps. It names what was claimed, under which law, to which body, on what
    date, embeds the source citations, and includes the prepared document, so the paper
    trail stands on its own offline, on a basic phone, after the session is gone."""
    ref = recourse.get("case_ref") or ("DENI-" + uuid.uuid4().hex[:8].upper())
    # All applicable bodies, not just the primary: a single problem often has more.
    forums = recourse.get("forums") or (
        [recourse["forum"]] if recourse.get("forum") else [])
    lines = [
        "DENI: CIVIC ACTION RECEIPT",
        f"Case ref: {ref}   Date: {_today()}",
        "Keep this. It records what you are filing, under which law, and with whom.",
        "",
        f"Situation: {recourse.get('title', '')}",
        f"The law: {recourse.get('law_statement', '')}",
        f"Applies if: {recourse.get('condition', '')}",
        f"Legal basis: {recourse.get('citation', '')} ({recourse.get('citation_date', '')})",
        "",
        "PUBLIC BODIES THAT APPLY:",
    ]
    sources: list[str] = []
    if recourse.get("citation"):
        sources.append(recourse["citation"])
    if forums:
        for f in forums:
            tag = "" if f.get("primary", True) else " (also applies)"
            lines.append(f"  - {f.get('name', '')}{tag}")
            if f.get("channel"):
                lines.append(f"    How to file: {f['channel']}")
            prov = f.get("provenance") or {}
            src = prov.get("source")
            if src:
                lines.append(f"    Source: {src}")
                sources.append(src)
    else:
        lines.append("  - (see the app for the body to contact)")
    lines += [
        "",
        "--- PREPARED DOCUMENT ---",
        recourse.get("complaint", ""),
        "",
        f"Sources (verify these yourself):",
    ]
    # De-dup sources, keep order.
    seen: dict[str, None] = {}
    for s in sources:
        seen.setdefault(s, None)
    lines += [f"  [{i+1}] {u}" for i, u in enumerate(seen)] or ["  (none recorded)"]
    lines += [
        "",
        "Prepared by Deni. Information and a self-prepared document, not legal advice.",
        "Verify the law and the body's current details before filing.",
    ]
    return {"ref": ref, "kind": "recourse", "text": "\n".join(lines),
            "sources": list(seen)}
