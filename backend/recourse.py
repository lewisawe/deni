"""DURING/AFTER recourse (Deni R6,R13). Classify a user's problem into a known
scenario, read the LAW from data (never AI-generated), and fill a fixed complaint
template. AI classifies + fills fact slots only. Not legal advice."""
from __future__ import annotations

import re
import uuid

from . import ai
from .data_pack import get_forum, get_scenario, load_pack

# Keyword fallback so the router works even if Bedrock is down (graceful degradation).
_KEYWORDS = {
    "harassment_contacts": ["contact", "phonebook", "calling every", "shame", "harass", "abuse", "threaten", "messaging my"],
    "repossession": ["repossess", "take my", "took my", "grab", "tow", "seize", "boda", "bike", "car", "logbook", "auction"],
    "misleading_terms": ["mislead", "hidden", "didn't tell", "not disclose", "lied", "cheat", "trick"],
    "unlicensed_chasing": ["unlicensed", "not licensed", "chasing", "enforce", "illegal lender"],
    "wrongful_crb": ["crb", "blacklist", "listed", "credit bureau", "cleared"],
    "small_claims_recovery": ["refund", "recover my money", "get my money back", "overpaid", "overpayment", "owe me", "they owe", "claim my money", "sue for", "small claims"],
}

_CLASSIFY_SYSTEM = (
    "Classify a Kenyan borrower's problem into exactly one key from this set: "
    "harassment_contacts, repossession, misleading_terms, unlicensed_chasing, "
    "wrongful_crb, small_claims_recovery. Use small_claims_recovery when the person "
    "wants to recover a sum of money (a refund, an overpayment, or the value of a "
    "loss). Return JSON: {\"scenario\": <key or null>, \"facts\": {"
    "\"lender_name\": <string or null>, \"what_happened\": <short phrase>, "
    "\"dates\": <string or null>}}. Use null if nothing matches."
)


def _classify(text: str) -> tuple[str | None, dict]:
    if ai.available():
        try:
            d = ai.converse_json(ai.MODEL_PRO, _CLASSIFY_SYSTEM, text,
                                 max_tokens=300, temperature=0.1)
            key = d.get("scenario")
            if key in _KEYWORDS:
                return key, d.get("facts", {}) or {}
        except Exception:  # noqa: BLE001 — fall back to keywords
            pass
    low = text.lower()
    for key, words in _KEYWORDS.items():
        if any(w in low for w in words):
            return key, {}
    return None, {}


def _fill_template(country: str, template_id: str, facts: dict, case_ref: str) -> str:
    tpl = load_pack(country)["templates"]["templates"].get(template_id)
    if not tpl:
        return ""
    body = tpl["body"]
    values = {
        "lender_name": facts.get("lender_name") or "[lender name]",
        "what_happened": facts.get("what_happened") or "[describe what happened]",
        "dates": facts.get("dates") or "[date(s)]",
        "data_misused": facts.get("data_misused") or "my personal data and contacts",
        "case_ref": case_ref,
        "redacted_contact": "[your contact]",
        "redacted_name": "[your name]",
        "redacted_id": "[your ID]",
        "licence_note": facts.get("licence_note") or "",
        "what_told": facts.get("what_told") or "[what you were told]",
        "actual_terms": facts.get("actual_terms") or "[the actual terms]",
        "asset": facts.get("asset") or "[the asset]",
        "notice_status": facts.get("notice_status") or "No proper default notice was served.",
        "demand": facts.get("demand") or "the immediate return of the asset",
        "bureau": facts.get("bureau") or "[TransUnion / Metropol / Creditinfo]",
        "reason": facts.get("reason") or "[why the listing is wrong]",
        "claim_amount": facts.get("claim_amount") or "[amount you are claiming]",
        "claim_basis": facts.get("claim_basis") or "[how you calculated the amount]",
        "evidence_list": facts.get("evidence_list") or "[list your evidence: agreement, payment records, messages, photos]",
    }
    # Fill {{slot}} tokens; leave unknown tokens visibly bracketed.
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(values.get(m.group(1), f"[{m.group(1)}]")), body)


def recourse(text: str, lang: str = "en", country: str = "ke") -> dict:
    """Full DURING/AFTER response: law + forum + prepared complaint + case ref."""
    key, facts = _classify(text)
    if not key:
        return {"matched": False,
                "message": "Couldn't match that to a known situation. Describe what the "
                           "lender is doing (e.g. calling your contacts, taking your bike, "
                           "wrongly listing you on CRB)."}
    scenario = get_scenario(country, key) or {}
    forum = get_forum(country, scenario.get("forum_key", "")) or {}
    case_ref = "DENI-" + uuid.uuid4().hex[:8].upper()
    complaint = _fill_template(country, forum.get("template_id", ""), facts, case_ref)
    return {
        "matched": True,
        "scenario": key,
        "title": scenario.get("title"),
        "law_statement": scenario.get("law_statement"),
        "condition": scenario.get("condition"),
        "citation": scenario.get("citation"),
        "citation_date": scenario.get("citation_date"),
        "forum": {"name": forum.get("name"), "channel": forum.get("channel"),
                  "what_to_include": forum.get("what_to_include", [])},
        "complaint": complaint,
        "case_ref": case_ref,
        "disclaimer": "This is information and a self-prepared document, not legal advice. "
                      "Recourse depends on your specific facts. Verify before acting.",
    }
